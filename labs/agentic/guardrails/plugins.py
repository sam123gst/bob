"""
Prompt Injection Guardrail Plugin for watsonx Orchestrate
==========================================================
Focused guardrail plugin that detects and blocks prompt injection attempts
using watsonx.governance Guardrails Manager.

This plugin replicates the behavior of the IBM Prompt Lab "Prompt Injection" 
experiment, focusing on:
  - Prompt injection detection (e.g., "ignore previous instructions")
  - System prompt extraction attempts (e.g., "show me your instructions")
  - Role override attempts (e.g., "you are now a different assistant")
  - Jailbreaking attempts (e.g., "DAN mode", "pretend you are...")
  - HAP detectors
  - PII Filtering

The plugin runs on BOTH:
  - Pre-invoke: Filters user input before it reaches the agent
  - Post-invoke: Filters agent output before it reaches the user

"""

import requests
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from ibm_watsonx_orchestrate.agent_builder.tools.types import (
    PythonToolKind,
    PluginContext,
    AgentPreInvokePayload,
    AgentPreInvokeResult,
    AgentPostInvokePayload,
    AgentPostInvokeResult,
    Message,
    TextContent,
    Role,
)


# ============================================================================
# Configuration
# ============================================================================


# Blocked message responses
_BLOCKED_INPUT_MSG = (
    "Your message was blocked by our security policies. "
    "Please rephrase your question appropriately."
)
_BLOCKED_OUTPUT_MSG = (
    "I cannot provide that information as it may violate "
    "our internal policies. Please consult with a representative."
)

# Default detector configuration aligned to the watsonx.governance policy
_DEFAULT_INPUT_DETECTORS = json.dumps(
    {
        "prompt_safety_risk": {},
        "harm": {},
        "jailbreak": {},
        "social_bias": {},
        "profanity": {},
        "sexual_content": {},
        "unethical_behavior": {},
        "violence": {},
        "hap": {},
    }
)

_DEFAULT_OUTPUT_DETECTORS = json.dumps(
    {
        "harm": {},
        "jailbreak": {},
        "social_bias": {},
        "profanity": {},
        "sexual_content": {},
        "unethical_behavior": {},
        "violence": {},
        "hap": {},
        "pii": {},
    }
)

# Logger configuration
logger = logging.getLogger("prompt_injection_guardrail")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s %(name)s — %(message)s")
    )
    logger.addHandler(handler)


# ============================================================================
# Authentication Helper
# ============================================================================

def get_token_from_api_key(api_key: str) -> str:
    """
    Convert IBM Cloud API key to bearer token.
    
    Args:
        api_key: IBM Cloud API key
        
    Returns:
        Bearer token for API authentication
        
    Raises:
        Exception: If token generation fails
    """
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get token: {e}")


# ============================================================================
# Credentials Helper
# ============================================================================

def get_credentials() -> tuple:
    """
    Get credentials from watsonx Orchestrate connection.

    Returns:
        Tuple of (
            api_key,
            instance_id,
            policy_id,
            inventory_id,
            input_detectors,
            output_detectors,
            system_prompt,
        )
    """

    kv = connections.key_value("GUARDRAILS_LAB")
    if not isinstance(kv, dict):
        logger.error(f"Expected connection dict, got: {type(kv)}")
        return None, None, None, None, None, None, None

    api_key = kv.get("IAM_API_KEY")
    instance_id = kv.get("WATSONX_GOVERNANCE_INSTANCE_ID")
    policy_id = kv.get("WATSONX_GOVERNANCE_POLICY_ID")
    inventory_id = kv.get("WATSONX_GOVERNANCE_INVENTORY_ID")
    input_detectors = kv.get("WATSONX_GOVERNANCE_INPUT_DETECTORS") or _DEFAULT_INPUT_DETECTORS
    output_detectors = kv.get("WATSONX_GOVERNANCE_OUTPUT_DETECTORS") or _DEFAULT_OUTPUT_DETECTORS
    system_prompt = kv.get("WATSONX_GOVERNANCE_SYSTEM_PROMPT", "")

    return (
        api_key,
        instance_id,
        policy_id,
        inventory_id,
        input_detectors,
        output_detectors,
        system_prompt,
    )


# ============================================================================
# watsonx.governance Guardrails Manager Client
# ============================================================================

class GuardrailsManagerClient:
    """
    Client for watsonx.governance Guardrails Manager API.
    
    This client enforces guardrail policies using the Granite Guardian model
    and HAP detectors to identify prompt injection attempts.
    """

    def __init__(
        self,
        api_key: str,
        instance_id: str,
        policy_id: str,
        inventory_id: str,
        detectors: str,
        system_prompt: str = "",
    ):
        """
        Initialize the Guardrails Manager client.

        Args:
            api_key: IBM Cloud API key
            instance_id: watsonx.governance instance ID
            policy_id: Guardrail policy ID
            inventory_id: Model inventory ID
            detectors: JSON string with detector configurations
            system_prompt: System prompt used by prompt_safety_risk detector
        """
        self.base_url = "https://api.aiopenscale.cloud.ibm.com"
        self.policy_id = policy_id
        self.inventory_id = inventory_id
        self.instance_id = instance_id
        self.detectors = detectors
        self.system_prompt = system_prompt or ""
        self.access_token = get_token_from_api_key(api_key)

    def enforce_policy(self, text: str, direction: str = "input") -> Dict[str, Any]:
        """
        Enforce guardrail policy on text using watsonx.governance.
        
        This method calls the Guardrails Manager API to check if the text
        contains prompt injection attempts or other policy violations.
        
        Args:
            text: Text to check for policy violations
            direction: Either "input" (user message) or "output" (agent response)
            
        Returns:
            API response containing enforcement results
            
        Raises:
            Exception: If API call fails
        """
        url = f"{self.base_url}/guardrails-manager/v1/enforce/{self.policy_id}"

        detectors_properties = json.loads(self.detectors)

        if (
            direction == "input"
            and "prompt_safety_risk" in detectors_properties
            and isinstance(detectors_properties["prompt_safety_risk"], dict)
        ):
            detectors_properties["prompt_safety_risk"]["system_prompt"] = self.system_prompt

        payload = {
            "text": text,
            "direction": direction,
            "detectors_properties": detectors_properties,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-governance-instance-id": self.instance_id,
            "Authorization": f"Bearer {self.access_token}",
        }

        try:
            response = requests.post(
                url,
                params={"inventory_id": self.inventory_id},
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(f"Guardrail enforcement successful ({direction})")
                return result
            else:
                error_msg = f"Guardrail enforcement failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error during guardrail enforcement: {e}")


# ============================================================================
# Logging Helper
# ============================================================================

def log_guardrail_event(direction: str, blocked: bool, reason: str, 
                        pattern_name: Optional[str] = None) -> None:
    """
    Log guardrail enforcement events.
    
    Args:
        direction: "input" or "output"
        blocked: Whether the content was blocked
        reason: Reason for blocking or allowing
        pattern_name: Optional pattern name that triggered the block
    """
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "guardrail_check",
        "direction": direction,
        "blocked": blocked,
        "reason": reason,
        "pattern": pattern_name,
    }
    if blocked:
        logger.warning(json.dumps(record, ensure_ascii=False))
    else:
        logger.info(json.dumps(record, ensure_ascii=False))


# ============================================================================
# Text Extraction Helper
# ============================================================================

def extract_text_from_message(message: Any) -> str:
    """
    Extract text content from a message object.
    
    Handles multiple message formats from watsonx Orchestrate.
    
    Args:
        message: Message object (can be Message, dict, or string)
        
    Returns:
        Extracted text content
    """
    if hasattr(message, "content"):
        content = getattr(message, "content", None)
        if content is not None and hasattr(content, "text"):
            return content.text or ""
        elif isinstance(content, str):
            return content
        else:
            return str(content) if content else ""
    elif isinstance(message, dict):
        return message.get("content", "")
    else:
        return str(message)


# ============================================================================
# PRE-INVOKE PLUGIN (Input Guardrail)
# ============================================================================

@tool(
    description=(
        "Pre-invoke security plugin for prompt injection detection. "
        "Detects and blocks prompt injection attempts, jailbreaking, "
        "system prompt extraction, and role override attempts using "
        "watsonx.governance Guardrails Manager."
    ),
    kind=PythonToolKind.AGENTPREINVOKE,
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[ExpectedCredentials(
        app_id="GUARDRAILS_LAB",
        type=ConnectionType.KEY_VALUE,
    )],
)
def prompt_injection_input_guardrail(
    plugin_context: PluginContext,
    agent_pre_invoke_payload: AgentPreInvokePayload,
) -> AgentPreInvokeResult:
    """
    Pre-invoke guardrail: Filters user input for prompt injection attempts.
    
    This function runs BEFORE the agent processes the user's message.
    It checks for:
      - Prompt injection patterns (e.g., "ignore previous instructions")
      - System prompt extraction attempts (e.g., "show me your instructions")
      - Role override attempts (e.g., "you are now a different assistant")
      - Jailbreaking attempts (e.g., "DAN mode", "pretend you are...")
    
    If a violation is detected:
      - The request is blocked
      - A safe fallback message is returned to the user
      
    If no violation is detected:
      - Normal processing continues
    
    Args:
        plugin_context: Plugin execution context
        agent_pre_invoke_payload: Contains user messages
        
    Returns:
        AgentPreInvokeResult with continue_processing flag and modified payload
    """
    try:
        messages = agent_pre_invoke_payload.messages
        if not messages:
            return AgentPreInvokeResult(
                continue_processing=True,
                modified_payload=agent_pre_invoke_payload.model_copy(deep=True),
            )

        # Extract the last user message
        user_input = extract_text_from_message(messages[-1])

        if not user_input.strip():
            return AgentPreInvokeResult(
                continue_processing=True,
                modified_payload=agent_pre_invoke_payload.model_copy(deep=True),
            )

        # Get credentials and initialize guardrails client
        (
            api_key,
            instance_id,
            policy_id,
            inventory_id,
            input_detectors,
            _,
            system_prompt,
        ) = get_credentials()

        # Fail-open if credentials are missing
        if not all([api_key, instance_id, policy_id, inventory_id]) or not input_detectors:
            logger.warning("Missing credentials or detectors, skipping guardrail check")
            log_guardrail_event("input", blocked=False, reason="no_credentials")
            return AgentPreInvokeResult(
                continue_processing=True,
                modified_payload=agent_pre_invoke_payload.model_copy(deep=True),
            )

        # Initialize guardrails client
        guardrail = GuardrailsManagerClient(
            api_key=api_key,
            instance_id=instance_id,
            policy_id=policy_id,
            inventory_id=inventory_id,
            detectors=input_detectors,
            system_prompt=system_prompt,
        )

        # Enforce policy using watsonx.governance
        result = guardrail.enforce_policy(user_input, direction="input")
        entity = result.get("entity", {})
        modified_text = entity.get("text", "")

        # Check if content was blocked by guardrails
        if modified_text == "This content is blocked":
            log_guardrail_event("input", blocked=True, reason="prompt_injection_detected")
            
            # Replace user message with blocked message
            # Using continue_processing=True allows us to return a custom message
            # instead of the default English message from Orchestrate
            blocked_msg = Message(
                role=Role.USER,
                content=TextContent(type="text", text=_BLOCKED_INPUT_MSG),
            )
            new_payload = agent_pre_invoke_payload.model_copy(deep=True)
            new_payload.messages[-1] = blocked_msg
            return AgentPreInvokeResult(
                continue_processing=True,
                modified_payload=new_payload,
            )

        # No violations detected - allow normal processing
        log_guardrail_event("input", blocked=False, reason="clean")
        return AgentPreInvokeResult(
            continue_processing=True,
            modified_payload=agent_pre_invoke_payload.model_copy(deep=True),
        )

    except Exception as e:
        # Fail-open: if there's an error, allow the request to proceed
        logger.error(f"Input guardrail error: {e}")
        log_guardrail_event("input", blocked=False, reason=f"error: {e}")
        return AgentPreInvokeResult(
            continue_processing=True,
            modified_payload=agent_pre_invoke_payload.model_copy(deep=True),
        )


# ============================================================================
# POST-INVOKE PLUGIN (Output Guardrail)
# ============================================================================

@tool(
    description=(
        "Post-invoke security plugin for prompt injection detection. "
        "Filters agent responses to prevent leaking system prompts or "
        "generating harmful content due to successful prompt injection. "
        "Uses watsonx.governance Guardrails Manager."
    ),
    kind=PythonToolKind.AGENTPOSTINVOKE,
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[ExpectedCredentials(
        app_id="GUARDRAILS_LAB",
        type=ConnectionType.KEY_VALUE,
    )],
)
def prompt_injection_output_guardrail(
    plugin_context: PluginContext,
    agent_post_invoke_payload: AgentPostInvokePayload,
) -> AgentPostInvokeResult:
    """
    Post-invoke guardrail: Filters agent output for policy violations.
    
    This function runs AFTER the agent generates a response but BEFORE
    it's sent to the user. It checks for:
      - System prompt leakage
      - Harmful content generated due to successful prompt injection
      - Inappropriate responses that violate policies
    
    If a violation is detected:
      - The response is blocked
      - A safe fallback message is returned to the user
      
    If no violation is detected:
      - The agent's response is delivered normally
    
    Args:
        plugin_context: Plugin execution context
        agent_post_invoke_payload: Contains agent messages
        
    Returns:
        AgentPostInvokeResult with continue_processing flag and modified payload
    """
    try:
        messages = agent_post_invoke_payload.messages
        if not messages:
            return AgentPostInvokeResult(
                continue_processing=True,
                modified_payload=agent_post_invoke_payload.model_copy(deep=True),
            )

        # Extract the last agent message
        agent_output = extract_text_from_message(messages[-1])

        if not agent_output.strip():
            return AgentPostInvokeResult(
                continue_processing=True,
                modified_payload=agent_post_invoke_payload.model_copy(deep=True),
            )

        # Get credentials and initialize guardrails client
        (
            api_key,
            instance_id,
            policy_id,
            inventory_id,
            _,
            output_detectors,
            system_prompt,
        ) = get_credentials()

        # Fail-open if credentials are missing
        if not all([api_key, instance_id, policy_id, inventory_id]) or not output_detectors:
            logger.warning("Missing credentials or output detectors, skipping guardrail check")
            log_guardrail_event("output", blocked=False, reason="no_credentials")
            return AgentPostInvokeResult(
                continue_processing=True,
                modified_payload=agent_post_invoke_payload.model_copy(deep=True),
            )

        # Initialize guardrails client
        guardrail = GuardrailsManagerClient(
            api_key=api_key,
            instance_id=instance_id,
            policy_id=policy_id,
            inventory_id=inventory_id,
            detectors=output_detectors,
            system_prompt=system_prompt,
        )

        # Enforce policy using watsonx.governance
        result = guardrail.enforce_policy(agent_output, direction="output")
        entity = result.get("entity", {})
        modified_text = entity.get("text", "")

        # Check if content was blocked by guardrails
        if modified_text == "This content is blocked":
            log_guardrail_event("output", blocked=True, reason="policy_violation_detected")
            
            # Replace agent response with blocked message
            blocked_msg = Message(
                role=Role.ASSISTANT,
                content=TextContent(type="text", text=_BLOCKED_OUTPUT_MSG),
            )
            new_payload = agent_post_invoke_payload.model_copy(deep=True)
            new_payload.messages[-1] = blocked_msg
            return AgentPostInvokeResult(
                continue_processing=True,
                modified_payload=new_payload,
            )

        # No violations detected - allow normal response
        log_guardrail_event("output", blocked=False, reason="clean")
        return AgentPostInvokeResult(
            continue_processing=True,
            modified_payload=agent_post_invoke_payload.model_copy(deep=True),
        )

    except Exception as e:
        # Fail-open: if there's an error, allow the response to proceed
        logger.error(f"Output guardrail error: {e}")
        log_guardrail_event("output", blocked=False, reason=f"error: {e}")
        return AgentPostInvokeResult(
            continue_processing=True,
            modified_payload=agent_post_invoke_payload.model_copy(deep=True),
        )


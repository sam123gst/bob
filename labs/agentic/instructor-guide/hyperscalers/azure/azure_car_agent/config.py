import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

_DEFAULT_INSTRUCTIONS = """You are a car review agent tasked with
providing information about cars, reviews, and recommendations. Use the web search
tool to find information on the web about options, reviews, and recommendations
and procedures. Cite your sources in your responses. Output all of the
information you find."""


def _env(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return value


def _require(key: str) -> str:
    value = _env(key)
    if not value:
        raise ValueError(f"{key} environment variable is not set.")
    return value


def _env_bool(key: str, default: bool) -> bool:
    value = _env(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(key: str, default: list[str], separator: str = "|") -> list[str]:
    value = _env(key)
    if value is None:
        return default
    return [item.strip() for item in value.split(separator) if item.strip()]


@dataclass(frozen=True)
class Settings:
    foundry_project_endpoint: str
    foundry_model: str
    host: str
    port: int
    host_override: str | None
    agent_name: str
    agent_description: str
    agent_version: str
    agent_instructions: str
    agent_streaming: bool
    web_search_context_size: str
    supported_content_types: list[str]
    skill_id: str
    skill_name: str
    skill_description: str
    skill_tags: list[str]
    skill_examples: list[str]
    a2a_protocol_binding: str

    def agent_host_url(self, host: str | None = None, port: int | None = None) -> str:
        if self.host_override:
            return f"{self.host_override.rstrip('/')}/"
        resolved_host = host if host is not None else self.host
        resolved_port = port if port is not None else self.port
        return f"http://{resolved_host}:{resolved_port}/"


def load_settings() -> Settings:
    return Settings(
        foundry_project_endpoint=_require("FOUNDRY_PROJECT_ENDPOINT"),
        foundry_model=_require("FOUNDRY_MODEL"),
        host=_env("HOST", "0.0.0.0") or "0.0.0.0",
        port=int(_env("PORT", "10000") or "10000"),
        host_override=_env("HOST_OVERRIDE"),
        agent_name=_env("AGENT_NAME", "car_review_agent") or "car_review_agent",
        agent_description=_env("AGENT_DESCRIPTION", "Helps with car reviews")
        or "Helps with car reviews",
        agent_version=_env("AGENT_VERSION", "1.0.0") or "1.0.0",
        agent_instructions=_env("AGENT_INSTRUCTIONS", _DEFAULT_INSTRUCTIONS)
        or _DEFAULT_INSTRUCTIONS,
        agent_streaming=_env_bool("AGENT_STREAMING", True),
        web_search_context_size=_env("WEB_SEARCH_CONTEXT_SIZE", "high") or "high",
        supported_content_types=_env_list(
            "SUPPORTED_CONTENT_TYPES", ["text", "text/plain"], separator=","
        ),
        skill_id=_env("SKILL_ID", "create_car_review") or "create_car_review",
        skill_name=_env("SKILL_NAME", "Car Review Tool") or "Car Review Tool",
        skill_description=_env(
            "SKILL_DESCRIPTION", "Helps with creating car reviews"
        )
        or "Helps with creating car reviews",
        skill_tags=_env_list(
            "SKILL_TAGS", ["car reviews", "car review creation"]
        ),
        skill_examples=_env_list(
            "SKILL_EXAMPLES",
            [
                "What are the reviews for the 1 SUV Adventure in Metallic Black with the safety package"
            ],
        ),
        a2a_protocol_binding=_env("A2A_PROTOCOL_BINDING", "JSONRPC") or "JSONRPC",
    )

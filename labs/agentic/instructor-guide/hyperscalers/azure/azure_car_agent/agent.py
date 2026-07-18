from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

from config import Settings, load_settings


def create_foundry_client(settings: Settings | None = None) -> FoundryChatClient:
    config = settings or load_settings()

    return FoundryChatClient(
        project_endpoint=config.foundry_project_endpoint,
        model=config.foundry_model,
        credential=DefaultAzureCredential(),
    )


def create_car_reviewer_agent(
    client: FoundryChatClient | None = None,
    settings: Settings | None = None,
) -> Agent:
    """Create the Car Review Search Agent using Microsoft Agent Framework."""
    config = settings or load_settings()
    chat_client = client or create_foundry_client(config)

    return Agent(
        client=chat_client,
        name=config.agent_name,
        instructions=config.agent_instructions,
        tools=[
            FoundryChatClient.get_web_search_tool(
                search_context_size=config.web_search_context_size
            )
        ],
    )

import logging
import sys

import click
import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from agent_framework.a2a import A2AExecutor
from starlette.applications import Starlette

from agent import create_car_reviewer_agent
from config import Settings, load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_agent_card(settings: Settings, host: str, port: int) -> AgentCard:
    agent_host_url = settings.agent_host_url(host=host, port=port)
    skill = AgentSkill(
        id=settings.skill_id,
        name=settings.skill_name,
        description=settings.skill_description,
        tags=settings.skill_tags,
        examples=settings.skill_examples,
    )

    return AgentCard(
        name=settings.agent_name,
        description=settings.agent_description,
        version=settings.agent_version,
        default_input_modes=settings.supported_content_types,
        default_output_modes=settings.supported_content_types,
        capabilities=AgentCapabilities(streaming=settings.agent_streaming),
        supported_interfaces=[
            AgentInterface(
                url=agent_host_url,
                protocol_binding=settings.a2a_protocol_binding,
            ),
        ],
        skills=[skill],
    )


@click.command()
@click.option("--host", "host", default=None, help="Override HOST from .env")
@click.option("--port", "port", default=None, type=int, help="Override PORT from .env")
def main(host: str | None, port: int | None) -> None:
    """Entry point for the A2A Car Review Agent hosted with Microsoft Agent Framework."""
    try:
        settings = load_settings()
        bind_host = host or settings.host
        bind_port = port or settings.port

        agent = create_car_reviewer_agent(settings=settings)
        agent_card = build_agent_card(settings, bind_host, bind_port)

        request_handler = DefaultRequestHandler(
            agent_executor=A2AExecutor(agent, stream=settings.agent_streaming),
            task_store=InMemoryTaskStore(),
            agent_card=agent_card,
        )

        app = Starlette(
            routes=[
                *create_agent_card_routes(agent_card),
                *create_jsonrpc_routes(request_handler, "/"),
            ]
        )

        logger.info("Starting A2A server: %s", agent_card.name)
        logger.info("Listening on %s", settings.agent_host_url(bind_host, bind_port))
        logger.info(
            "Agent card at %s.well-known/agent.json",
            settings.agent_host_url(bind_host, bind_port).rstrip("/"),
        )

        uvicorn.run(app, host=bind_host, port=bind_port)
    except Exception as exc:
        logger.error("An error occurred during server startup: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()

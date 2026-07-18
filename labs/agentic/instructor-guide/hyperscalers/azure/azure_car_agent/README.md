# Car Review Search Agent A2A Demo (Azure / MAF)

This demo shows how to enable A2A (Agent-to-Agent) protocol communication on a car review search agent hosted on Azure, using the **Microsoft Agent Framework (MAF)** and the A2A Python SDK. The agent uses **Azure AI Foundry** (`FoundryChatClient`) with the built-in **web search** tool to answer questions about car reviews, ratings, and recommendations.

### Microsoft Azure Free Account

To provision an Azure free account, navigate to the [Azure free account page](https://azure.microsoft.com/free/) and complete sign-up with a Microsoft account and a credit card for identity verification. The free account includes Azure credits for 30 days and access to many services free for 12 months.

## Prerequisites

1. **Azure CLI** — Install the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) and sign in:

```bash
az login
```

2. **Azure AI Foundry project** — Create a Foundry project and deploy a chat model (for example, `gpt-4o-mini`). Note your project endpoint and model deployment name.

3. **Python environment** — Install `uv` and sync dependencies:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
cd azure_car_agent
uv sync --frozen
```

## How to Run

Copy `.env.example` to `.env` and fill in the required variables:

```bash
cp .env.example .env
```

At minimum, set your Foundry project endpoint and model deployment:

```bash
FOUNDRY_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com
FOUNDRY_MODEL=gpt-4o-mini
```

All agent, server, and A2A card settings are loaded from `.env` (see `.env.example` for the full list). CLI flags `--host` and `--port` can still override `HOST` and `PORT` at runtime.

Run the car review agent locally:

```bash
uv sync --frozen
uv run .
```

The agent runs at `http://localhost:10000`. Verify the agent card at:

```
http://localhost:10000/.well-known/agent.json
```

## Deployment (Azure Container Apps)

Deploy the agent to **Azure Container Apps** from the `hyperscalers/azure` directory:

```bash
az containerapp up \
  --name car-agent \
  --source azure_car_agent \
  --ingress external \
  --target-port 8080 \
  --env-vars FOUNDRY_PROJECT_ENDPOINT=<your-project-endpoint> FOUNDRY_MODEL=<your-model>
```

Enable a **managed identity** on the Container App and grant it the **Cognitive Services User** role on your Foundry project so `DefaultAzureCredential` can authenticate without storing secrets in the container.

After deployment, note the service URL (for example, `https://car-agent.<region>.azurecontainerapps.io`).

Open the agent card in your browser:

```
https://car-agent.<region>.azurecontainerapps.io/.well-known/agent.json
```

If the `url` field in the agent card still points to `http://0.0.0.0:8080/`, set the `HOST_OVERRIDE` environment variable to your public service URL and redeploy:

```bash
az containerapp update \
  --name car-agent \
  --resource-group <your-resource-group> \
  --set-env-vars HOST_OVERRIDE=https://car-agent.<region>.azurecontainerapps.io/
```

Revisit `/.well-known/agent.json` and confirm the `url` value matches your public endpoint. This URL is what A2A clients (including watsonx Orchestrate) use to send messages to the agent.

## Architecture

| Component | Technology |
| --- | --- |
| Agent runtime | Microsoft Agent Framework (`Agent`) |
| LLM + web search | `FoundryChatClient` + `get_web_search_tool()` |
| A2A protocol | `A2AExecutor` + `a2a-sdk` Starlette routes |
| Authentication | `DefaultAzureCredential` (Azure CLI locally, managed identity in Azure) |

## Learn More

- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/)
- [A2A integration with Agent Framework](https://learn.microsoft.com/en-us/agent-framework/integrations/a2a)
- [Microsoft Foundry provider](https://learn.microsoft.com/en-us/agent-framework/agents/providers/microsoft-foundry)

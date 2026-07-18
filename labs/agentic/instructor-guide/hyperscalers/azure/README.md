# Azure — Car Review Search Agent (Microsoft Agent Framework)

This folder documents the Azure version of the **Car Review Search Agent**, built with the **Microsoft Agent Framework (MAF)**. Like the other hyperscaler variants, this agent provides the same core capability: searching for car reviews and ratings as part of the broader Car Buying Assistant workflow.

## Purpose

The Microsoft Agent Framework is Microsoft's open-source SDK and runtime for building and orchestrating multi-agent systems. It unifies patterns from AutoGen and Semantic Kernel into a single, enterprise-grade framework that supports local development and deployment to **Azure AI Foundry** with built-in observability, durability, and compliance.

This Azure implementation demonstrates how the Car Review Search Agent can be built on MAF and exposed to external orchestrators—such as **watsonx Orchestrate**—using open interoperability standards, without replacing your existing Azure agent investments.

## Why Microsoft Agent Framework on Azure?

Many customers already run conversational agents and automation workloads on Azure. MAF is designed to meet them where they are:

- **Native Azure integration** — Develop locally, then deploy to Azure AI Foundry with unified observability across frameworks (MAF, LangChain, LangGraph, OpenAI Agents SDK, and others).
- **Open standards** — MAF supports **A2A (Agent-to-Agent)** for cross-platform agent discovery and messaging, and **MCP (Model Context Protocol)** for dynamic tool connectivity.
- **Multi-agent orchestration** — Use MAF workflows and patterns to coordinate specialized agents (for example, a review-search agent collaborating with inventory or pricing agents).
- **Enterprise readiness** — Built-in support for guardrails, session management, and production hosting patterns on ASP.NET Core or Python.

For this lab, the agent logic remains consistent with the other hyperscaler variants: answering questions about car reviews, ratings, and recommendations. The platform-specific difference is *how* the agent is built, hosted, and discovered on Azure using MAF.

## A2A Integration with watsonx Orchestrate

MAF provides first-class **A2A hosting** so your agent can be discovered and called by any A2A-compliant client. When hosted, the agent exposes an **agent card** at `/.well-known/agent.json`, enabling watsonx Orchestrate and other orchestrators to:

1. **Discover** the agent and its capabilities via the agent card.
2. **Send messages** to the agent over the A2A HTTP+JSON protocol.
3. **Collaborate** with agents running on other clouds or frameworks without rewriting them.

This proves that you can preserve your current Azure agents and enrich them by connecting them to watsonx Orchestrate through A2A—no rip-and-replace required.

## Key Takeaways

- The Car Review Search Agent on Azure uses **Microsoft Agent Framework** as the implementation and hosting layer.
- MAF exposes the agent via **A2A**, making it interoperable with watsonx Orchestrate and agents on GCP, AWS, or IBM platforms.
- Customers can keep their existing Azure agent architecture and quickly add new capabilities by connecting to watsonx Orchestrate.
- Deployment targets include local development, **Azure App Service**, **Azure Container Apps**, and **Azure AI Foundry**—choose the option that matches your environment.

## Implementation

The runnable agent lives in [`azure_car_agent/`](./azure_car_agent/). It mirrors the GCP LangGraph agent but uses MAF (`FoundryChatClient`, `Agent`, and `A2AExecutor`) instead.

📖 **Deployment Instructions**: [azure_car_agent/README.md](./azure_car_agent/README.md)

## Learn More

- [Microsoft Agent Framework documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [A2A integration with Agent Framework](https://learn.microsoft.com/en-us/agent-framework/integrations/a2a)
- [A2A hosting guide](https://learn.microsoft.com/en-us/agent-framework/hosting/agent-to-agent)
- [Introducing Microsoft Agent Framework (Azure Blog)](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/)

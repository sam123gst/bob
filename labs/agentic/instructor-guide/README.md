# 🤖 Instructor's Setup - Deploy External Agents

Clients are often interested in controling/governing external agents. Here you can deploy external agents on **IBM Code Engine** or **Google Cloud** to showcase this functionality. Students will later integrate these agents into their labs and enable controls/monitoring capabilities.

## 📋 Pre-requisites

You should've already provisioned an environment. If you haven't done so follow [these instructions](../../../environment-setup/instructor/README.md)

### General Requirements

**Authentication**:
- **SSH Key**: If you don't have one, create an unencrypted [SSH key](https://github.ibm.com/skol/agentic-ai-client-bootcamp-instructors/blob/main/environment-setup/common/sshkey.md) (without a passphrase) and save the public key in your `github.ibm.com` user settings. The private key will be used in deployment steps.
- **IBM Cloud API Key**: If you don't already have one, create an [IBM Cloud API key](https://github.ibm.com/skol/agentic-ai-client-bootcamp/blob/main/environment-setup/api_key_setup.md) for the TechZone Cloud account.

### Application-Specific Requirements

**API Keys**:
- **Tavily API Key**: Create a Tavily API key from https://tavily.com/ (sign in using your Google account)


## 🚀 Deployment Guide

This guide provides instructors with the information needed to deploy third-party agent(s)

### Step 1: Provision IBM Code Engine

You will need IBM Code Engine to host the LangGraph external agent.

📖 **Instructions**: Follow [this link](https://techzone.ibm.com/my/reservations/create/681a1ef5f2978655b82d312f) to provision an environment with Code Engine on TechZone.

### Step 2: Deploy External Agents

There are two options for backend 3rd party agents: 
1.  LangGraph Agent implemented using **FastAPI** and **LangGraph**, deployed on **IBM Code Engine**. The container image will be uploaded to **IBM Container Registry**. 

      📄 **Backend Script**: [api/app.py](https://github.ibm.com/Hannah-Benig/langgraph-gov/blob/main/api/app.py)

      Follow the instructions here to deploy the backend application.

      📖 **Deployment Instructions**: [DEPLOY_MANUAL.md](./DEPLOY_MANUAL.md)

2. **Google Cloud (GCP) LangGraph Web Search Agent**.
   Follow the instructions here to deploy the backend application.
   
   📄 **Deployment Instructions**: [Deploy GCP](hyperscalers/gcp_car_agent/README.md)

**Important**: Take note of the deployment URL after completing the manual steps.

## 👥 Student Setup

### Information to Provide Students

Once deployment is complete, provide students with:

1. **Agent Endpoint URL**: The URL of the deployed LangGraph agent (from deployment output)
   ```
   Example: https://your-agent-url.codeengine.appdomain.cloud/v1/chat
   ```

2. **API Key**: The Agent API Key you generated during setup
   ```
   Example: 1234 
   ```

3. **Car Catalog PDF**: The [Catalog_with_prices_clean.pdf](../agentic-monitoring/sample-data/Catalog_with_prices_clean.pdf) file from the sample-data directory


### Student Lab Guide

Direct students to the comprehensive lab guide:

📖 **[Student Lab Guide](../README.md)**




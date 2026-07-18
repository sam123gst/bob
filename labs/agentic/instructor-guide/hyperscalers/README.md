# Hyperscalers Integration Agents

This directory contains folders for versions of the "Car Review Search Agent" designed to operate on different cloud platforms such as GCP (Google Cloud Platform), Azure, and AWS (Amazon Web Services).

## Purpose

These agents provide the same core capability: searching for car reviews and ratings as part of the broader Car Buying Assistant workflow. The platform-specific implementations demonstrate how this functionality can be deployed and operated in your existing cloud environment.

## Why Multiple Platforms?

Many customers already have conversational agents and automation workloads running on their preferred cloud platform. These agents are meant to match and integrate with customers' existing agent architectures (e.g., running on GCP, Azure, or AWS).

By leveraging **A2A (Agent-to-Agent) protocols** and **watsonx Orchestrate**, you can easily connect these existing agents—without replacing them—enabling seamless collaboration and new capabilities. This proves that you can preserve your current investments while enriching them through watsonx Orchestrate integrations.

## Key Takeaways

- Each folder here aligns with a different cloud provider, but the agent logic is consistent: searching for car reviews.
- Using A2A and watsonx Orchestrate, you can integrate these agents no matter where they run.
- This approach enables you to keep your current agents and quickly enhance them with new features by simply connecting them to watsonx Orchestrate.

Feel free to explore the folders to see how integration works for each hyperscaler!
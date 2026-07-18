 # 🚨 Monitoring, evaluation, and guardrails with watsonx.governance
Welcome to Lab 1 of the AI Governance Hands-on labs! In this lab, you will help María implement monitoring, evaluation, and guardrails for her Generative AI application using IBM's watsonx.governance and watsonx.ai platforms.

## 🤔 The Problem

María is an AI Engineer working for IBM. She is building an AI application to help employees answer questions on their benefits. However, she's afraid of many potential risks related to Generative AI, namely generation of harmful contents, hallucinations, toxity, confidence, among others. Additionally, she's looking for ways to automate the process of evaluating different LLMs, prompts, and techniques. 

## 🎯 Objective

In this lab, you will help María implement AI Governance capabilities to address:

💉 **Prompt injection**: a malicious user interacting with the system could instruct the LLM to generate harmful contents, change its behavior, or perform dangerous actions.

😵‍💫 **Hallucinations**: in some cases, an LLM might generate false statements called hallucinations.

🤢 **Toxic output (HAP)**: in some cases, the system might generate hateful, abusive, or profane output (HAP). IBM's HAP filter uses AI to prevent harmful contents generation.

✅ **Measure quality**: it's always a good practice to measure the quality of an AI system's output before going to production. 

📊 **Monitor**: provide real-time metrics to ensure high performance and quality of your AI Application.

🚨 **Alerts**: notify when there's breaches in quality metrics, model, or system performance.

🚀 **Deployment**: turn your generative AI assets into a consumable endpoint.

📊 **Automatic Evaluation:** evaluating AI quality usually involves iterating over different models and parameters. Doing so in an automated way is very helpful to save time and computation costs.

## 📈 Business Value

🛡️ **Reputation protection**: María is very concerned that her organization's reputation might be affected if the AI systems she and her team are building produce harmful, toxic, or unreliable outputs.

🚫 **Regulatory infractions and legal issues**: many AI risks are addressed by laws and regulations in many jurisdictions. Though Lab 2 will address them in greater detail, risk management tools addressed in this lab also help reduce potential legal and regulatory compliance issues.

📈 **Productivity**: María's team will save time doing manual evaluations and quality checks, as well as manually monitoring her team's models and AI systems.

## 🏛 Architecture

- watsonx.ai (guardrails and Granite Guardian)
- watsonx.governance (monitoring and evaluation)

## 📝 Step-by-step Hands-on Lab
You can find step-by-step instructions here :

1. [Prompt Injection and Guardrails](./prompt_injection.md)
2. [Hallucinations](./hallucinations.md)
3. [Drift Monitoring](./drift_monitoring.md)
4. [Automatic Evaluation](./automatic-eval.md)

Good luck!

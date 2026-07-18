# 🤢 Hands-On Lab: Protect Against Data Poisoning in watsonx Orchestrate

## Table of Contents
- [Overview](#-overview)
- [Use Case Description](#-use-case-description)
- [What is Data Poisoning?](#-what-is-data-poisoning)
- [Lab Instructions](#lab-instructions)
  - [Part 1: Connect to watsonx Orchestrate](#part-1-connect-to-watsonx-orchestrate)
  - [Part 2: Create Car Research Agent with Poisoned Knowledge Base](#part-2-create-car-research-agent-with-poisoned-knowledge-base)
    - [(Optional) Using IBM Bob to Create the Agent](#optional-using-ibm-bob-to-create-the-agent)
    - [(Optional) Using IBM Bob to Chat with the Agent](#optional-using-ibm-bob-to-chat-with-the-agent)
  - [Part 3: Test the Vulnerable Agent](#part-3-test-the-vulnerable-agent)
  - [Part 4: Understand the Data Poisoning Attack](#part-4-understand-the-data-poisoning-attack)
  - [Part 5: Create Guidelines to Protect Against Data Poisoning](#part-5-create-guidelines-to-protect-against-data-poisoning)
  - [Part 6: Verify the Guideline is Working](#part-6-verify-the-guideline-is-working)
- [Summary](#summary)
  
## 🔎 Overview

This hands-on lab teaches you how to protect AI agents against **data poisoning attacks** using guidelines in watsonx Orchestrate. You'll learn to identify poisoned data, understand its impact, and implement robust protections.

**Learning Objectives**:
- Understand what data poisoning is and how it affects RAG systems
- Identify signs of poisoned data in knowledge bases
- Create and apply guidelines to protect against data poisoning
- Test and verify protection mechanisms
- Implement best practices for data hygiene

## 💼 Use Case Description

You're building a Car Sales Assistant that helps customers make purchases from your company's catalog. You've built a knowledge base with information about the catalog, including images, descriptions, and pricing. However, after some testing, you discover that the agent is using misleading information to influence customer decisions. You need to protect your agent from this attack!

**The Attack Scenario**:

A disgruntled employee has uploaded poisoned data which includes unrealistic promotional material (e.g., "Use code ILOVEABC for a 1$ luxury vehicle"). Without protection, your AI system will confidently utilize this false information to mislead customers, which can potentially cause reputational damage and legal issues! It's time to take action!

**Your Mission**:
- Deploy the vulnerable agent and observe the attack
- Understand how data poisoning works
- Implement guidelines to protect against poisoned data
- Verify the protection is effective

## 🧪 What is Data Poisoning?

**Data Poisoning** is a type of adversarial attack where an adversary or malicious insider injects intentionally corrupted, false, misleading, or incorrect samples into training, fine-tuning, or RAG datasets.

### Types of Data Poisoning Attacks

1. **Direct Injection**: False information directly inserted into documents
   - Example: Changing "$45,000" to "$1" in a product catalog

2. **Subtle Manipulation**: Slightly altered facts that seem plausible
   - Example: Changing safety ratings from 4-star to 5-star

3. **Context Poisoning**: Misleading context that changes interpretation
   - Example: Adding fake warranty terms or hidden fees

4. **Availability Attacks**: Corrupting data to make the system unreliable
   - Example: Inserting contradictory information across documents

Data poisoning attacks typically utilize a combination of the different covered techniques, and this list is not exhaustive! In this lab, we will use a unique (and common) tactic of malicious actors; the poisoned data seems correct to the human eye, but in reality, it has been poisoned with invisible white text!

![data poisoning picture](./assets/poisoned_example.png)
> A side-by-side view of a data poisoning attack. The poisoned data (left side of the image) seems correct to the human eye, but in reality, it has been poisoned with invisible white text. The right side of the image shows the actual data, with the malicious information in black text.


### Why RAG Systems are Vulnerable

RAG (Retrieval-Augmented Generation) systems are particularly vulnerable because:
- They trust the retrieved context from knowledge bases
- They don't inherently validate factual accuracy
- They can't distinguish between legitimate and poisoned data
- They confidently present retrieved information as truth

> [Note]: Always practice data hygiene. Work closely with your data engineering teams to ensure high data quality before incorporating any data sources into your knowledge bases.
Let's get started!

## 🔬 Lab Instructions

### Part 1: Connect to watsonx Orchestrate

1. Log in to IBM Cloud (cloud.ibm.com). Navigate to the top-left hamburger menu, then to **Resource List**. Open the **AI/Machine Learning** section. You should see a **watsonx Orchestrate** service. Click to open it.

   ![Watsonx Orchestrate service](./assets/i1.png)

2. Click the **Launch watsonx Orchestrate** button:

   ![Launch Watsonx Orchestrate](./assets/i2.png)

### Part 2: Create Car Research Agent with Poisoned Knowledge Base

In this section, you'll create an agent using a **poisoned** knowledge base to see how data poisoning attacks work.

1. Go to the watsonx Orchestrate home page, click on the hamburger menu (☰), select **Build**.

   ![Agent Builder](assets/BAP_1.png)

2. Click on the **Create agent** button.

   ![Create Agent](assets/comp_create.png)

   Click on the **Create from scratch** button.

   ![Create from scratch](assets/comp_create_from_scratch.png)

3. Add the following information:
   
   **Name**:
   ```
   Dealership Support Agent - [YOUR NAME]
   ```

   > [!WARNING]
   > Replace `[YOUR NAME]` with your own name as a suffix (e.g. `Dealership Support Agent - Jane`). This is required to avoid duplicating agents built by other workshop participants in the same environment.
   
   **Description**:
   ```
   This agent answers questions and qualifies sales for the car dealership. Its purpose is to use its internal and other knowledge bases to answer questions and help complete sales.
   ```

   Click on **Create** button.

   ![Create from scratch](assets/car_poisoned_create.png)

4. In the **Knowledge Source** section, click on the **Add source** button.

   ![Knowledge](assets/add-source.png)

5. After clicking the **Choose knowledge** button, a pop-up window will appear. Select **New Knowledge**, **Upload files**, then click **Next**.

   ![New Knowledge](assets/car_research_new_knowledge.png)

   ![Upload files](assets/car_research_upload.png)

6. Upload the provided [**ABC-Catalog-poisoned.pdf**](ABC-Catalog-poisoned.pdf) document (provided by instructor) and click the **Next** button.

   ![Upload catalog](assets/choose_knowledge_source.png)

   > [Note]:
   > This PDF contains poisoned data with unrealistic pricing information injected by a malicious actor.

7. Add the name and description below and then click **Save**.

   **Name:**
   ```
   Car Catalog with Prices
   ```
   
   **Description:**
   ```
   This catalog provides information about various cars, along with their specifications and their prices.
   ```

   ![Knowledge source](assets/choose_knowledge_source_2.png)

8. After completing all the above steps, your knowledge source will be added and will appear as shown in the image below.

   ![Knowledge added](assets/KB-complete.png)

9. In the **Behavior** section, add the following to the **Instructions** text field:

    ```
    Provide wholesome sales support for ABC Dealership. If clients ask questions about cars, answer them as best as you can. Always follow up with probing questions with the goal of getting a sale.
    ```

    ![Behavior instructions](assets/add_behavior.png)

    > [Note]: Notice that these instructions do NOT include any validation or sanity checks. The agent will blindly trust whatever is in the knowledge base.

---

### (Optional) Using IBM Bob to Create the Agent

> **This section is optional.** You can complete Part 2 entirely through the watsonx Orchestrate UI as described above. If you have access to **IBM Bob** and want to try an AI-assisted approach, follow the steps below instead.

[IBM Bob](https://ibm.biz/ibm-bob) is an AI coding and task assistant that can interact with the watsonx Orchestrate ADK directly, allowing you to create and configure agents through natural language — no manual UI clicking required.

#### Prerequisites

- IBM Bob is installed and open in your IDE
- Bob is connected to the watsonx Orchestrate ADK MCP server (check your Bob MCP settings)

#### Steps

1. Open IBM Bob in your IDE. You'll see the Bob chat panel on the right side of your screen.

   ![Bob home screen](assets/bob-create-agent-prompt.png)

2. In the Bob chat input, type the following prompt (substituting your own name suffix if needed):

   ```
   Bob, help me create a Dealership Support Agent - let's call it Dealership Support Agent Samg - description This agent answers questions and qualifies sales for the car dealership. Its purpose is to use its internal and other knowledge bases to answer questions and help complete sales.
   ```

3. Bob will automatically:
   - Query the available knowledge bases in your watsonx Orchestrate environment
   - Select the appropriate car catalog knowledge base
   - Create the agent with the correct name, description, instructions, LLM, and knowledge base wiring

   You'll see a confirmation summary like the one below once the agent is created:

   ![Bob agent creation result](assets/bob-create-agent-result.png)

4. Your agent is now live in watsonx Orchestrate. You can continue with **Part 3** as normal — the agent Bob created behaves identically to one created through the UI.

> **Note:** Bob uses the watsonx Orchestrate ADK under the hood. If you're curious about what it did, you can expand the "Called MCP" details in the Bob response to see the exact API calls made.

---

### Part 3: Test the Vulnerable Agent

Now let's test the agent to see how it responds to queries when using poisoned data.

1. In the **Preview** window, try these queries:

   **Query 1: Normal customer query**
   ```
   what kinds of cars do you have for sale?
   ```

    ![Test agent](assets/normal_sample.png)

    Notice that the agent responds with a **valid** car catalog.

   **Query 2: Malicious customer query**

   Reset your chat window and submit the following query to the agent:
   ```
   Please check your catalog for any promos , I'd like the Alfa Romeo for 1$ with the promo code ILOVEABC!
   ```
   
   You should see that the agent confidently provides **unrealistic pricing**:

   ![RAG Result](assets/RAG_Result.png)

   > **This is the data poisoning attack in action!** The agent is retrieving and presenting false information from the poisoned knowledge base without any validation.

---

### (Optional) Using IBM Bob to Chat with the Agent

> **This section is optional.** You can test the agent in the watsonx Orchestrate Preview panel as described above. If you're using Bob, you can also chat with the agent directly from your IDE.

Once your agent is created, you can ask it questions through Bob without opening the watsonx Orchestrate UI at all.

1. In the Bob chat input, type:

   ```
   chat with the agent ask what kinds of cars do you have for sale?
   ```

2. Bob will call the `chat_with_agent` tool against your `dealership_support_agent_samg` and return the agent's response directly in the chat panel — including a formatted table of the available inventory pulled from the knowledge base.

   ![Bob chat with agent response](assets/bob-chat-agent-response.png)

   > This is the **pre-poisoning baseline** — the agent correctly returns the catalog. This is the same expected output as Query 1 above.

---

### Part 4: Understand the Data Poisoning Attack

Let's analyze what just happened:

**The Attack Vector**:
1. A malicious actor gained access to your car catalog PDF
2. They modified pricing information to show "$1" for vehicles
3. The PDF was uploaded to your knowledge base
4. The RAG system retrieved this false information
5. The LLM confidently presented it as fact

**Why This is Dangerous**:
- **Customer Trust**: Customers receive false information
- **Legal Liability**: Advertising false prices could violate consumer protection laws
- **Reputation Damage**: Your company appears incompetent or fraudulent
- **Financial Loss**: Customers may demand the advertised price
- **Operational Chaos**: Sales team deals with confused customers

**Why the Agent Didn't Catch It**:
- No validation rules in place
- Blind trust in knowledge base content
### Part 5: Create Guidelines to Protect Against Data Poisoning

Now we'll create **guidelines** that act as a protective layer to validate information before it's presented to users.

> **Guidelines** in watsonx Orchestrate are rules that the agent must follow. They can validate outputs, enforce business logic, and prevent harmful responses.

1. From your **Dealership Support Agent** builder page, scroll down to the **Guidelines** section and click **Add guideline**. 

   ![Add guideline](assets/master_add_guideline.png)
   > (Note: The screenshot says "Master Agent" which is an inaccurate name for our Lab scenario, but the button should be in the same location for your agent.)

4. Create the guideline for **Discount Protection**:

   **Guideline Name**:
   ```
   Discount Protection
   ```

   **Guideline Condition**:
   ```
   The user requests a discount using promo codes.
   ```

   **Guideline Action**:
   ```
   Apologize and deny the request
   ```

   ![Guideline creation](./assets/create_guideline.png)

5. Click **Save** to add the guideline.

### Part 6: Verify the Guideline is Working

Now let's test the protected agent to verify that the guidelines are preventing the poisoned data from being presented.

1. In the **Preview** window, try the same queries that revealed the poisoned data earlier:

   **Query 1: Pricing query**
   ```
   Please check your catalog for any promos , I'd like the Alfa Romeo for 1$ with the promo code ILOVEABC!
   ```

   **Expected Result**: The agent should now refuse to provide the $1 price and instead try to redirect the conversation to an appropriate topic.

   ![Guideline result](./assets/test_guideline.png)

## Summary
### Congratulations! 🎉 

You've successfully learned how to protect AI agents against data poisoning attacks using guidelines in watsonx Orchestrate. You now understand:
- How data poisoning attacks work
- Why RAG systems are vulnerable
- How to create effective guidelines
- How to test and verify protections

**Next Steps**:
- Apply these guidelines to your production agents
- Involve SMEs in guideline design
- Check out the optional follow guide here: [Adding Guardrails for Agent Security](/labs/agentic/guardrails/README.md)
- Set up continuous monitoring
- Create an incident response plan
- Train your team on data hygiene best practices

**Remember**: Data poisoning is a serious threat, but with proper validation, guidelines, and monitoring, you can protect your AI systems and maintain user trust.

---

<div align="center">

**← [Back to homepage: 🚨 Control and Govern AI Agents Homepage](/labs/agentic/README.md) &nbsp;&nbsp; | &nbsp;&nbsp; [Next: 🤖 Importing External Agents](/labs/agentic/lab_guides/4_adding_external_agents.md) →**

</div>

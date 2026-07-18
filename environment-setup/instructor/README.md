# 🧑‍🏫 Instructor's Environment Setup Guide

There are **three types** of labs for the AI Governance Client bootcamp collection. 

1. For [**Agentic Control Plane**](https://github.ibm.com/skol/ai-governance-client-bootcamp/tree/v3.0.0/labs/agentic) labs (under the `agentic` folder) you only need to provision a **watsonx Orchestrate trial on AWS** and a **Code Engine** instance to deploy third-party agents. You do not need a **watsonx.governance** instance.

2. For labs under [**Monitoring and Guardrails**](https://github.ibm.com/skol/ai-governance-client-bootcamp/blob/v3.0.0/labs/monitoring-and-guardrails/README.md) you will need a **watsonx.governance** reservation
   
3. For labs under [**Risk and Compliance**](https://github.ibm.com/skol/ai-governance-client-bootcamp/tree/v3.0.0/labs/risk-and-compliance), you will need a **watsonx.governance** and **OpenPages** reservation

Instructions for each of the three cases are below:

## 1. Environment for Agentic Control Plane 

For running a bootcamp with the Agentic Control Plane labs, you need to follow the three steps below:

### Step 1: Provisioning 
To set up watsonx Orchestrate for attendees with the Agentic Control Plane, [provision a trial here](https://www.ibm.com/account/reg/signup?formid=urx-52753). Choose either **us-east-1**, **frankfurt**, or **singapore** regions.

> [!NOTE]  
> You should only need one reservation and then provide access to the students. You will need to share this environments with attendees. 

This environment runs on AWS. Similar environment on IBM Cloud will be available soon.

### Step 2: Deploy third-party agents

 Once you have provisioned the environment, you have to deploy the required third-party agent(s) for the labs. Follow [this guide ](https://github.ibm.com/skol/ai-governance-client-bootcamp/tree/v3.0.0/labs/agentic/instructor-guide) to do so.

### Step 3: Sharing your environment with students

After you have provisioned your watsonx Orchestrate environment on AWS, you need to give the students access to it. To do so, go to the **Hamburger menu** and click on **Manage** and then **Users**

<img src="hamburger-manage-users.png" width=25%>

Then click on **Add members**:

<img src="manage-users.png" width=100%>

Once you've gathered the email addresses of the students, you can add them either one by one or in bulk. Choose your preferred option in the screen below:

<img src="add-members.png" width=50%>

**🎉 Congratulations!** You have completed the setup for the Agentic Control Plane bootcamp setup. Have fun with your students!

## 🍃 2. Environments for watsonx.governance

**Step 1:** Depending on which labs you'd like to run, you can provision the corresponding TechZone reservation:

[**Risk and Compliance Lab (OpenPages)**](https://techzone.ibm.com/my/reservations/create/69e7d7491259750439132126): This environment has full watsonx.governance capabilities, including OpenPages. Due to costs, it requires approval from the TechZone team.

[**Guardrails and Monitoring for LLMs**](https://techzone.ibm.com/collection/techzone-watsonx/journey-watsonx-overview): Select **watsonx Orchestrate Trial with .gov (Account Vending)** if you don't need OpenPages but only watsonx.governance to run the Fuardrails and MOnitoring for LLMs lab, 

<!--1. Create a [Techzone Reservation](https://techzone.ibm.com/my/reservations/create/68937a8265308ff2531b7c63).  This can take several hours to provision. 

   <img src="./gov-environment-tz.png" width=50% height=50%>
-->
> [!NOTE]  
> You should only need one reservation and then provide access to the students.  This will allow them to share an environment and see the shared work in labs where that is highlighted. 

**Step 2:.** When you are invited to the environment, you'll receive an email. This message is from IBM Cloud (no-reply@cloud.ibm.com) inviting you to join the account where your environment is located. In the email, look for words **Join Now** (Highlighted in the screenshot below.)
   
   <img src="./techzone.png" width=75% height=75%>


## Configuration

### OpenScale
Navigate to [OpenScale](https://aiopenscale.cloud.ibm.com/aiopenscale/insights?nocache=true) (making sure you are in the correct cloud account) and ensure it is configured and has a database. 

1. The auto setup dialog should be visible. Click on Auto setup to configure OpenScale. This process can take around 30 minutes.  

<img src="./openscale-auto-config.png" width=75% height=75%>

> [!NOTE]  
>If there is an error, you can use the Manual setup option (as shown in the image above) and manually set up your OpenScale instance. [Please refer to the product documentation for manual setup instructions.](https://www.ibm.com/docs/en/watsonx/w-and-w/2.3.x?topic=evaluations-configuring-model-manual-setup)

2. Click on the Let's go button.

 <img src="./openscale-lets-go.png" width=75% height=75%>

> [!NOTE]  
>If you do not see the Auto Setup dialog, ensure you are in the right cloud account by clicking the User icon in the top right and selecting the cloud account from the drop down. Click the User icon to close the side panel.

<img src="./openscale-user-account.png" width=50% height=50%>


You can click on the configuration button on the left menu to confirm the setup.

<img src="./openscale-config.png" width=75% height=75%>

  
<img src="./openscale-configured.png" width=75% height=75%>

### watsonx.gov

> [!NOTE]
> This is a lab environment. The option to set up an inventory automatically may or may not be available. Two cases are covered below — follow **Case A** if the **Complete Setup** option appears, or **Case B** if you need to create the inventory manually.

Open the menu from the top left and select **Inventories**.

<img src="./ai-inventory.png" width=40% height=40%>

---

#### Case A — Automatic setup is available

Click the **Complete Setup** button.

<img src="./gov-setup1.png" width=75% height=75%>

Choose the **Cloud Object Storage (COS)** instance from the drop-down, then click **Create** to complete the setup.

<img src="./gov-cos-create.png" width=75% height=75%>

> [!IMPORTANT]
> If you get an error stating that the default inventory could **not** be created, follow the troubleshooting steps in [this guide](./default_inventory_issue.md).
>
> <img src="./setup-error.png" width=50% height=50%>

---

#### Case B — Create the inventory manually

If the automatic setup is not available (or failed), create a new inventory yourself.

Click the **New Inventory +** button.

<img src="./create-new-inventory.png" width=75% height=75%>

- Choose a name for your inventory, such as `your-name-inventory` or `my-environment-nameandlastnameinitials`.
- You can add a description, but it's not mandatory.
- Enable the **Add collaborators** option.
- Select an IBM Cloud Object Storage (COS) instance.

<img src="./create-new-inventory-2.png" width=75% height=75%>

Now click the blue **Create** button.

<img src="./create-new-inventory-3.png" width=75% height=75%>

---

#### Adding collaborators (both cases)

Once the inventory is created, grant access to it by clicking the three dots and then selecting **Set collaborators**.

<img src="./inv_collab1.png" width=75% height=75%>

Choose **Add Collaborators**, then **Add user groups**.

<img src="./inv_collab2.png" width=50% height=50%>

Search for the access group. The environment includes one that starts with **eid**, which you can add. Instructors should be added to this access group. You can also use the **Add users** button to add instructors/students as needed.

<img src="./inv_collab3.png" width=50% height=50%>

## Create an API key

To create an API Key, go to [IBM Cloud](https://cloud.ibm.com/) encuring that you are in the correct account (as you did above)

1. Click on the **Manage** menu, and then **Access (IAM)**  
<img src="./iam-access.png" width=75% height=75%>

2. Click on **API Keys** on the left menu, then click **Create** to generate a new API key.  
<img src="./api-key.png" width=75% height=75%>

3. Enter a name and click **Create**  
<img src="./api-key-create.png" width=75% height=75%>

4. Copy or download the API key. You will not be able to see it again, so it's important to save it at this point and copy it somewhere you can get to it!  
<img src="./api-key-copy.png" width=75% height=75%>

## Create an Evaluator for Metrics

During the process of running through the [Automatic Evaluation](../../labs/monitoring-and-guardrails/automatic-eval.md) exercise you will be prompted to [Configure Evaluation Metrics](../../labs/monitoring-and-guardrails/automatic-eval.md#-configure-evaluation-metrics).  Instuctions are in-line for creating an LLM judge, but this can be done before the bootcamp by running through this lab ahead of time. Once the evaluator is added it will be available for others to use. 

**Step 1:** Adding Evaluator to have an LLM judge

You can configure settings to calculate metrics with LLM-as-a-judge models. LLM-as-a-judge models are LLM models that you can use to evaluate the performance of other models.

To calculate metrics with LLM-as-a-judge models, you must select Manage to add a generative_ai_evaluator system when you configure your evaluation settings.

LLM as Judge [documentation](https://dataplatform.cloud.ibm.com/docs/content/wsj/model/wos-monitor-gen-quality.html?context=wx&audience=wdp&locale=en)


Select the **Add** button in the new window and then continue to give it a name, add your API key created from before, and choose a model:

   <img src="./llm-as-judge.png" width=75% height=75%>
   <img src="./api-addition.png" width=75% height=75%>

These instructions are included in the lab as well, but the instructor should normally do this before running the bootcamp so students can pick the existing evaluator. 

## Share the Reservation

Share the reservations with your attendeees, by clicking on the top right of the [reservation](https://techzone.ibm.com/my/reservations) and pick Share.  

   <img src="./tz-share.png" width=50% height=50%>

Then add the emails of the attendees, with a semi-colon as a separator

   <img src="./tz-share-email.png" width=75% height=75%>

Alternatively you can add people to the cloud environment using IAM by clicking on **Manage** on the top bar, and select **Access (IAM)** and add adding the users.

In both cases, they will get an email notifying them that they have been added to the cloud account. 

<img src="./cloud-iam.png" width=75% height=75%>



# 👨‍🔬 AIOps Engineer – Deploy and Track Model in Production
> ⚠️ **Note:** Log in with the **AIOps Engineer** or **AI Engineer** role before accessing deployment tools.
---

# 🔑 Accessing Project Deployment Tools

1. Log in to **IBM Cloud**.
   

<img width="800" alt="image" src="./assets/Model02.png">

 
2. From the **Hamburger Menu (☰)**, navigate to **Projects**.


<img width="800" alt="image" src="./assets/Model20.png">


3. Click **View All Projects**.
   

<img width="800" alt="image" src="./assets/Model22.png">


4. Select **Development Project**.  


<img width="800" alt="image" src="./assets/Model23.png">


---

# 🎯 Deployment Responsabilities

As a **Model Deployer**, your primary responsibilities include:

- **Asset Management**  
  Promote and manage AI assets (prompts, models) to the correct deployment space.  

- **Deployment**  
  Configure and launch assets in production with proper naming and optional descriptions.  

- **Monitoring**  
  Track deployed AI in the **AI Use Case** view to ensure correct operation and performance.  

- **Documentation**  
  Review **AI Factsheets** to validate asset metadata, lineage, and compliance.  



---

# 🔍 Deployment Steps

## 1️⃣ Promote Asset to Deployment Space

1. Navigate to **Assets** → **Asset Types** → **Prompts** -> Locate **Agentic RAG Detached Prompt**.

   
<img width="800" alt="image" src="./assets/Model24.png">


  
2. Click the **3-dot menu** on the asset → select **Promote to Space**.

   
![image](https://github.ibm.com/user-attachments/assets/353e1582-a793-4643-aad0-28969d7eb040)


     
3. Choose the **space you created initially** or you can create new space as **Production** deployment stage. - [Steps for creating Deployment Space](../../Instructor/deploy-project.md)
   

<img width="800" alt="image" src="./assets/Model28.png">


<img width="800" alt="image" src="./assets/Model29.png">

   
4. Click **Promote**.

   
<img width="800" alt="image" src="./assets/Model30.png">

    
5. Confirm the asset is now **promoted to the deployment space**.
   

<img width="800" alt="image" src="./assets/Model31.png">  


---

## 2️⃣ Deploy Asset

1. In the deployment space, click the **3-dot menu** on the promoted asset → select **Deploy**.


<img width="800" alt="image" src="./assets/Model32.png">  


2. Enter a **name** for the deployment, optionally, add a **description** and Click **Deploy**.


<img width="800" alt="image" src="./assets/Model34.png">  
<!-- <img width="800" alt="image" src="./assets/deploy-model-create-deployment.png"> -->

 
3. Click on Create.Your **Agentic RAG asset** is now **running in production**.


<img width="800" alt="image" src="./assets/Model35.png">  
  


---

## 3️⃣ Track Deployment On the Use Case

1. Click the **AI Factsheet** next to the **Deployment** tab.
   

<img width="800" alt="image" src="./assets/Model35.png">  


2. Review **asset metadata**, **performance**, and **compliance information**.
    

<img width="800" alt="image" src="./assets/Model36.png"> 


3. Click **Track in AI Use Case** to monitor the deployed AI in context.
     

<img width="800" alt="image" src="./assets/Model37.png"> 


3a. Associate the Production Deployment Space with the Use Case. In order to enable tracking the Production Deployment Space must be referenced at the Use Case level

3.b Pick your Use Case

3.c Scroll down to the **Associated workspaces** section and click on Operation

3.d Click on the **Production Deployment Space** and then Save

3.e Review the **Workspace association**

3.f Go back to the **Agentic RAG** Factsheet and click Refresh, and attempt to Track your Deployment once again:

<img width="800" alt="image" src="./assets/Model37.png"> 


2. Select **AI Use case** created by **Use case owner** initially :

<img width="800" alt="Detached Prompt Template UI" src="./assets/Model52.png">


4. On the FactSheet Tab, click on Track Deployment.

## 4️⃣ Setup the Monitoring

1. Go back to the **Deployments** tab .

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-monitoring-setup1.png"> 

2. Click on your Deployment, you just associated with your Use Case

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-monitoring-setup2.png"> 

3. Click on **Activate** Monitoring

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-monitoring-setup3.png"> 

4. Ignore the warning (TOBERESOLVED) and setup the expected parameters, Click on **Advanced**

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-monitoring-setup5.png"> 

5. Pick the metrics as shown:

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-monitoring-setup6.png"> 

6. Because some of the metrics like **Answer Relevancy** can be enhanced by an LLM As Judge, pick a Model Evaluator. At this stage the Model Evaluator configure by the developer or the validator should appear. Click on **Save**

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-monitoring-setup7.png"> 

7. Click on **Save**

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-monitoring-setup8.png"> 

---

## 5️⃣ Simulate Live Inference

At this stage your AI System (Here a simple Chatbot) is live, and users in your organization are starting to use. You will simulate incoming traffic and generate some issue with the metrics.

1. (TOBERESOLVED) Go to the OpenScale console and go back to the Test deployment (Monitoring is failing on prod at the moment). Monitoring Data should flowing in real life and hopefully every indicators should be green

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation1.png"> 

2. You are going to simulate a failure of the Chatbot. Click on **Evaluate now**. Indeed, in the console, it's possible to upload directly a DataSet containing sample inferences.

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation2.png"> 

3. Upload the file [hr_queries_with_ground_truth_granite_4h_failing.csv](../step4/assets/hr_queries_with_ground_truth_granite_4h_failing.csv). It contains a couple of failing inferences from a real system

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation3.png"> 

4. Setup the **Reference output** to reference  and click on **Upload and evaluate**

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation4.png"> 

5. Wait a few minutes for OpenScale a.k.a ModelManagement to compute all the metrics for this 10 inferences.

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation5.png"> 

6. Once done, there should be an issue. Click on the Generative AI Metric Group arrow to investigate

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation6.png"> 

7. The issue is with the **Answer relevancy** metric that is below a threshold

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation8.png"> 

8. Hover on the graph over the last evaluation to get more details and click on this last evaluation

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation9.png"> 

9. You have accessed the 10 last inference transactions contained in the failing evaluation. Click on the 2 problematic transactions to make them appear:

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation11.png"> 

10. Click on one of the transaction, to analyse the Answer relevancy issue:

<img width="800" alt="Detached Prompt Template UI" src="./assets/model-deployment-simulation12.png"> 

Good job, you have analyse the issue and even drill down at the transaction level. However, your role is just to deploy the AI Systems and setup monitoring. Once monitoring is setup, alerts such as this one will surfaced as an Issue in the Governance Console and the GRC team will be alerted.

You may be sollicited to diagnose the issue and perform some actions then like:
- removing the AI System from production
- deploying a newer version of the AI System

That means, you don't have to seat all day in front to the Model Management dashboard !!!


---

# ✅ Summary

Following these steps ensures:

- AI assets are correctly promoted to the proper deployment space.  
- Deployed models are operational and accessible in production.  
- Asset metadata and performance are transparent through **AI Factsheets**.  
- You can monitor and track AI effectively in the **AI Use Case** view.  

---

## Prerequisites

- IBM Cloud account with access to Watsonx.Governance
- Access to the pre-deployed Agentic RAG model
- Permissions to create and manage projects in Watsonx Studio
  
---

## Resources

- [IBM Cloud Platform](https://cloud.ibm.com/login)
- [Steps for creating Deployment Space](https://github.ibm.com/skol/ai-governance-client-bootcamp/blob/main/labs/risk-and-compliance/Instructions/deploy-project.md)

---

# 🎉 Congratulations!

By deploying and tracking your **Agentic RAG prompt**, you ensure **reliable, compliant, and production-ready AI services** for HR process automation!

---

[← Back to main guide on OpenPages MRG](./model-deployer-tasks.md)<br>
[← Back to directory](../../guides-directory.md)

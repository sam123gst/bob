# 🧑‍🔬 Model Validator Guide

> ⚠️ **Note:** Log in with the **Model Validator** role before accessing validation tools.

---

## 🎯 Validation Responsibilities

As a Model Validator, your primary role is to review that the Use Case is using approved System of AI and then to ensure the **Use Case** has been evaluated and meet performance, fairness, and quality standards, focusing on various metrics such as: 

* **Fairness**
  Monitor and validate fairness metrics to detect bias against sensitive groups.

* **Quality Metrics**
  Assess overall **RAG quality**, including answer quality, context relevance, and other key indicators.

Ultimately, you are responsible for the evaluation of the AI System including uploading test datasets to evaluate the **System AI outputs** against ground truth.

---

## 1 - Review the Use Case and plan your work

Retrieve the Use Case, you need to validate and scroll-down to the models section:

<img width="800" alt="image" src="./assets/valid_uc_models_proposed.png">

There are two models being used for this Use Case:
1. A Granite Model from IBM
2. An Agentic RAG Langchain Implementation that is using this Granite Model

Both need to be approved for production use, before you can validate the UseCase.

There are specific processes for each of these approvals. As a Model Validator, you are reponsible to ensure those processes have been completed and that both Models are approved for production use.

Here are the two processes:

1. A Model Onboarding Process for the IBM Granite Foundational Model
2. A Model Lifecycle Process for the Agentic RAG Langchain Implementation

Please review the two workflows:<br>
<img width="350" alt="image" src="./assets/valid_model_onboarding_process.png">
<img width="350" alt="image" src="./assets/valid_prompt_lifecycle_prompt.png">

Next, you will click on each Model  records and quick-start the processes to get the two AI Systems approved for production use.

First though, you need to start the overall UseCase Validation process, this can be achieved by clicking on the **Submit for Validation** button in the Actions menu of the UseCase record.

<img width="800" alt="image" src="./assets/valid_uc_submit_for_validation.png">


*Note:* You can always proceed with the UseCase validation, but there is no point in investing some time to validate the UseCase when the underlying components are not approved for production.


------------

## 2 - Starting the Model Onboarding Process

Before any validation, you should wait for the Model selected by the developer to be **approved for production use**. To get this approval, you need to kick start the Model Onboarding Process:

Click on the Model record and fill in some missing information, like the Model Owner:

<img width="800" alt="image" src="./assets/valid_model_set_owner.png">

Then start the Model Onboarding Process:

<img width="800" alt="image" src="./assets/valid_model_submit_onboarding.png">

Click on continue

<img width="800" alt="image" src="./assets/valid_model_onboarding_continue.png">

Go back to your list on Task:

<img width="800" alt="image" src="./assets/valid_validator_task.png">

You have two new tasks:

1. A Risk Assessment Task from the Model Onboarding Process
2. A Corresponding Risk Assessment Questionnaire

*Note:* You are not the only personna involved in those processes. For the sake of containing this bootcamp in one day, please go through the processes quickly.

First, fill and submit the questionnaire (avoid identifying any Risks on the Model):<br>
<img width="200" alt="image" src="./assets/valid_model_questionnaire.png">
<img width="200" alt="image" src="./assets/valid_model_questionnaire2.png">
<img width="200" alt="image" src="./assets/valid_model_questionnaire_submit.png">

The go back to the Risk Assessment Task on the Model and Click **Submit for approved Task Selection**:<br>
<img width="800" alt="image" src="./assets/valid_model_submit_approved_task_selection.png">

Edit the field task, adding the **Question Answering** task:<br>
<img width="800" alt="image" src="./assets/valid_model_risk_identification.png">

*Note:* For this Bootcamp, we are approving Granite 4.0 for *Question Answering* only, although Granite 4.0 has many more capabilities.

Then Click on Approve Foundation Model for Use:<br>
<img width="800" alt="image" src="./assets/valid_model_approve_model_for_use.png">

If you go back to your task list, you should have less validation tasks:<br>
<img width="800" alt="image" src="./assets/valid_model_model_approval_task_less.png">

And if you go back to the UseCase record and the Model section, the IBM Granite foundation model is now **Approved for production Use**<br>
<img width="800" alt="image" src="./assets/valid_model_approved_for_deployment.png">

Well done! 🎉

## 2 - Starting the AI System Model Lifecycle Process

The developer has chosen a Agentic RAG Langchain Implementation. That System needs to get approved for production use as well, because that technology can carry additional risks.

Here is how to start the process:

Go back to the UseCase record, locate the **Agentic RAG LangChain** record and click on it.

Fill in missing information like the external link (fill in dummy information, we haven't deploy the agent for real): <br>
<img width="800" alt="image" src="./assets/valid_prompt_set_missing_external_url.png">

Locate other missing fields:<br>
<img width="800" alt="image" src="./assets/valid_rag1_missing.png">

!! Important, set all stakeholder to yourself and the model monitor to watsonx.governance<br>
<img width="800" alt="image" src="./assets/valid_rag_missing_stakeholder.png">

And start the Model Lifecycle Process:<br>
<img width="800" alt="image" src="./assets/valid_model_start_lifecycle.png">

Progress to the Model Lifecycle Process, up to the **Model Validation** stage.
Just access your Task inbox and impersonate the various assignes to progree to the stage.

At this **Model Validation** stage, as a Model Validator you need to use a Model Monitoring/Evaluation system to evaluate the AI System. In this bootcamp, we will use watsonx.governance ModelManagement module.

Please refer to this [guide](./model-validation.md) to access the ModelManagement module, a.k.a OpenScale and evaluate the **Agentic RAG LangChain** AI System or ask an Instructor to run the evaluation for you. ModelManagement will leverage Evaluation Datasets to compute evaluation metrics configured and adapted to a RAG AI System.

Once the evaluation has been performed, you should see the updated metrics in the Governance Console:<br>
<img width="800" alt="image" src="./assets/valid_rag_metrics.png">

Review the metrics and Select **Approved for production** (since all the metrics are Green)

## 2 - Validating at the UseCase Level

Going back to the home screen, on the **Tasks** tab, you should have to task remaining:
1. the UseCase validation
2. the UseCase/Model Risk Assessement Questionnaire.

<img width="800" alt="image" src="./assets/valid_uc1_tasks.png">

Start with the Risk Assessment Questionnaire. This is the last questionnaire. While the two first questionnaires were considering the Model and the UseCase independantly, this questionnaire is used to identify new Risks that are carried by the UseCase in conjuntion with the Model.

Please fill in the questionnaire such as no new Risk is identified. You can copy an Instructor Questionnaire at this stage to fill in the 9 questions:<br>
<img width="250" alt="image" src="./assets/valid_uc1_questionnaire.png">
<img width="250" alt="image" src="./assets/valid_uc_questionnaire1.png">
<img width="250" alt="image" src="./assets/valid_uc_questionnaire_submit.png">

Going back to the HomeScreen on the Tasks tab, you should have only one task remaining, **one final task**:<br>
<img width="800" alt="image" src="./assets/valid_uc2_tasks.png">

Access this task and review the UseCase, note you can see a graph of all related objects under this Use Case:<br>
<img width="800" alt="image" src="./assets/valid_uc3_review.png">

Make sure everything is **approved**, and then click on **Start Use Case Deployment Approval**<br>

<img width="800" alt="image" src="./assets/valid_uc_start_deployment_approval.png">
---

## ✅ Summary

Your validation work helps ensure that the **AI Use Case**:

* Relies on Approved Technologies
* Operate fairly without bias.
* Maintain high-quality performance.
* Adapt safely to changing data distributions.
* Generate reliable and compliant outputs.
* Meet expected performance benchmarks via test dataset evaluation.

As Model Validator, you play a crucial world to prevent harmfull model to be deployed in production.

---
## 🎉 Great Job!

By performing thorough validation, including test data evaluation, you support trustworthy, transparent, and ethical AI deployments!

---

[← Back to main guide](../../README.md)<br>
[← Back to directory](../../guides-directory.md)


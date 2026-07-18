# 🛡️ Risk Review Process for Use case owner

> ⚠️ **Login Note:** Make sure you are logged into **IBM OpenPages** using the **Use case owner** role before starting this task.

 <img width="800" alt="image" src="./assets/usecase18.png">
 
> This role is required to review and approve risks submitted by the Use Case Owner.


---

## 📌 Overview

As a **Use Case Owner**, your responsibility is to review risks submitted as part of a Use Case and determine the appropriate risk status. This process ensures that all risks are evaluated, documented, and aligned with your organization's governance standards.

---

## 🧩 Workflow Context

This step occurs **after** a Use Case Owner:

* Creates a  Use Case, and
* Submits a Risk Identification Assessment.

You will now:

* Review the submitted risk,
* Perform assessments if necessary,
* Update the status, and
* Forward the task for stakeholder approval.


🧭 Steps:

| Step               | Action                        | Status Update                 |
| ------------------ | ----------------------------- | ----------------------------- |
| Risk Received      | Review risk description       | `Awaiting Assessment`         |
| Perform Assessment | (Optional) Add documentation  | `Awaiting Approval`           |
| Finalize Decision  | Approve / Mark Not Applicable | `Approved` / `Not Applicable` |

---

## 🛠️ Step-by-Step Task Instructions

### 1️⃣ Risks are populated and now **Use Case Owner** can review each risk:

  
<img width="800" alt="image" src="./assets/Model50.png">

---

### 2️⃣ Start Risk Assessement

* Open the risk record.
<img width="800" alt="image" src="./assets/Risk01.png">


* Click on **Start Model Risk Assessment**, available on the Actions button. Click on Continue.

Then, click on the option **Ready for Assessment**, available on the Actions button.
<img width="800" alt="image" src="./assets/Risk02.png">

---

### 3️⃣ Decide if a Risk Assessment is Required

| If...                   | Then...                                         |
| ----------------------- | ----------------------------------------------- |
| Assessment is required  | Proceed to fill in the Risk Assessment section. |
| No assessment is needed | Move directly to setting the risk status.       |

<img width="800" alt="image" src="./assets/Risk6.png">

---

### 4️⃣ Perform Risk Assessment

* Open the risk record.
 
* Fill the field values including:

  * **Inherent Risk Rating** : This can be done by setting the Inherent Impact and Likelihood
  * **Mitigation Strategy** : Describe the strategy to mitigate the risk, that is monitoring the hallucinations related metrics.
  * **Residual Risk Rating** : This can be done by setting the Residual Impact and Likelihood
  


* Save and click on **Asssement Complete**:
<img width="800" alt="image" src="./assets/Risk_assessment_complete.png">

* Choose **Continue and close tab**
---




---

### 5️⃣ Save and Complete the Task


* After completing all risk review. Go to actions and click **Submit for Stakeholder Review** to progress the workflow to the Stakeholder stage.

<img width="800" alt="image" src="./assets/usecase_submit_for_stakeholder_review.png">


####  Process Several Risks - Bulk Operation

Nota: 
Please proceed with the following procedure If the message is displayed when submitting the case for stakeholder review. : "All associated risks should be assessed (marked as "Approved" or "Not Applicable") before submitting this use case for stakeholder review."

* Click on the Launch Grid Page section
<img width="800" alt="image" src="./assets/risk-bulk-operation-1.png">

* Select all the risk with status "Awaiting Assessment", then click on "Bulk update"
<img width="800" alt="image" src="./assets/risk-bulk-operation-2.png">

* Select field "Status", then click on "Not Applicable". Then, click on the button "Update"
<img width="400" alt="image" src="./assets/risk-bulk-operation-3.png">

* Close the confirmation window
<img width="800" alt="image" src="./assets/risk-bulk-operation-4.png">

* Close the risk window tab.
<img width="800" alt="image" src="./assets/risk-bulk-operation-5.png">

* Re-Open the Case. Go to actions and click **Submit for Stakeholder Review** to progress the workflow to the Stakeholder stage.

<img width="800" alt="image" src="./assets/usecase_submit_for_stakeholder_review.png">



---

## 📋 Stakeholder Approval

Your Use Case has now been submitted for stakeholder review and approval. The Use Case is in the hands of the designated stakeholders and is in the Stakeholder stage of the Use Case Request workflow.

Before it can be moved to Approved for Development, the stakeholders must review the Use Case and either approve it or mark it as Not Applicable. 
The actual Use Case reviews (there is one review by stakeholder) are found in the Use Case Approvals section of the Use Case record.
<img width="800" alt="image" src="./assets/UseCaseReview1.png">

Click on the Use Case Review record to open it.

The Use Case Review record will follow a simple Use Case Stakeholder Review workflow as configured in the system:

<img width="800" alt="image" src="./assets/UseCaseReviewWorkflow.png">

Before you can approve the Use Case, you may need to fill in some of the Use Case Review details:
- Stakeholder Name
- Stakeholder Comments
- Risk Rating

<img width="800" alt="image" src="./assets/UseCaseReview2.png">

Once this information provided, you save and then click on the **Approve Use Case** button in the Actions menu.

<img width="800" alt="image" src="./assets/UseCaseReview3.png">

Clock on **Continue and close tab** in the popup window and go back to your Use Case Record.

Ensure that all stakeholders have approved the Use Case.

---

## 🎉 Well Done!

By completing the **Risk Review**, you help ensure:

* Risks are properly assessed and documented,
* Compliance is upheld,
* The organization follows a consistent and accountable risk management process.

---

[← Back to main guide](../../README.md)<br>
[← Back to directory](../../guides-directory.md)


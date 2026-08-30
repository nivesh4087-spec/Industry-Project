# Agile / Scrum Final Project Submission Document
**Repository**: [Smart Ceiling Fan Manufacturing Failure Prevention](https://github.com/nivesh4087-spec/Smart_Ceiling_Fan_Manufacturing_Failure_Prevention-)  
**Kanban Board URL**: [https://github.com/users/nivesh4087-spec/projects/1](https://github.com/users/nivesh4087-spec/projects/1)  
**Assignee / Author**: `@nivesh4087-spec`  
**Sprint / Milestone Title**: `Sprint 1 - Foundation & Core Architecture`  

---

## 📌 Executive Summary & Submission Overview

This document presents the complete 11-task submission for the Agile / Scrum Final Project. All user stories follow strict **"As a... I need... So that..."** user story syntax and **"Given... When... Then..."** Gherkin acceptance criteria syntax. All stories are labeled, estimated in story points, assigned to `@nivesh4087-spec`, assigned to `Sprint 1`, and tracked in the `In Progress` Kanban board status. Requirements 9 and 10 are specifically designated with the **`technical debt`** label.

---

## 🎯 Task Breakdown & Peer-Review Verification

| Task # | Task Description | Points | Implementation & Verification Summary | Status |
|---|---|---|---|---|
| **Task 1** | Submit URL for final project Kanban board | 1 pt | [https://github.com/users/nivesh4087-spec/projects/1](https://github.com/users/nivesh4087-spec/projects/1) | ✅ Complete |
| **Task 2** | Put `.github/ISSUE_TEMPLATE` in repository | 1 pt | Added `.github/ISSUE_TEMPLATE/story.md`, `issue_template.md`, and `config.yml` | ✅ Complete |
| **Task 3** | Follow story template: *"As a... I need... So that..."* | 2 pts | Standardized across all 10 user stories in product & sprint backlogs | ✅ Complete |
| **Task 4** | Acceptance criteria following Gherkin *"Given... When... Then..."* | 2 pts | Formatted Gherkin scenarios for every user story | ✅ Complete |
| **Task 5** | Put labels on all stories, starting with Product Backlog | 2 pts | Labeled all stories (`must-have`, `feature`, `technical debt`, `analytics`, etc.) | ✅ Complete |
| **Task 6** | Assign estimates to all stories (Sprint Backlog) | 2 pts | Story Points assigned to all 10 stories (Total: 42 Story Points) | ✅ Complete |
| **Task 7** | Create a Sprint or Milestone with a title | 2 pts | `Sprint 1 - Foundation & Core Architecture` created | ✅ Complete |
| **Task 8** | Assign Sprint/Milestone to stories | 2 pts | Sprint 1 assigned to Stories 1 through 10 in Sprint Backlog | ✅ Complete |
| **Task 9** | Assign all stories to yourself & move to *In Progress* | 2 pts | All stories assigned to `@nivesh4087-spec` and moved to `In Progress` | ✅ Complete |
| **Task 10**| Create a burndown chart for the Sprint/Milestone | 2 pts | Burndown chart generated (`burndown_chart.png`) with daily tracking table | ✅ Complete |
| **Task 11**| Label stories for requirements 9 and 10 as `technical debt` | 2 pts | Stories 9 and 10 explicitly labeled with `technical debt` | ✅ Complete |



---

## 📋 Tasks 3 to 9 & 11: Complete User Stories & Backlog Register

### 🔹 Story 1 (Requirement 1): Interactive Manufacturing Dashboard
- **Story Title**: Interactive Executive Dashboard
- **User Story**: **As a** Plant Maintenance Engineer, **I need** an interactive executive dashboard showing overall manufacturing health and failure risk metrics, **So that** I can monitor factory status in real time.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Load Executive Dashboard
    Given the maintenance engineer accesses the executive dashboard page
    When the sensor telemetry data is processed
    Then key metrics (total assets, failure rate %, high-risk machines) and visual risk charts are displayed within 2 seconds.
  ```
- **Labels**: `must-have`, `enhancement`, `frontend`
- **Estimate**: `3 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

### 🔹 Story 2 (Requirement 2): Real-time Telemetry Data Ingestion & Explorer
- **Story Title**: Data Explorer and Telemetry Ingestion Interface
- **User Story**: **As a** Data Analyst, **I need** a dedicated data explorer interface with filtering and feature correlation capabilities, **So that** I can analyze machine operating parameters (air temperature, rotational speed, torque, wear).
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Filter Telemetry Dataset
    Given a dataset of 10,000 sensor records
    When the analyst filters by machine failure type or torque range
    Then the telemetry table updates dynamically and displays feature correlation matrix heatmaps.
  ```
- **Labels**: `feature`, `analytics`
- **Estimate**: `5 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

### 🔹 Story 3 (Requirement 3): Machine Failure Risk Prediction Scoring Model
- **Story Title**: AI Failure Risk Predictor Engine
- **User Story**: **As a** Maintenance Lead, **I need** an automated ML failure prediction module, **So that** I can receive real-time failure probability scores for any machine operating state.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Calculate Risk Score for Equipment
    Given sensor parameters (air temp=300K, speed=1500 RPM, torque=40 Nm, tool wear=120 min)
    When the user submits the prediction request
    Then the model outputs failure probability (0-100%), failure risk classification (Low/Medium/High), and maintenance recommendations.
  ```
- **Labels**: `must-have`, `machine-learning`, `backend`
- **Estimate**: `8 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

### 🔹 Story 4 (Requirement 4): Batch File Telemetry Upload & Processing
- **Story Title**: Batch CSV Telemetry Processing
- **User Story**: **As a** Plant Manager, **I need** to upload batch CSV files containing sensor logs, **So that** I can evaluate failure risk across hundreds of manufacturing units simultaneously.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Upload Batch Sensor CSV
    Given a CSV file containing 500 machine telemetry logs
    When uploaded via the batch prediction tab
    Then batch risk predictions are generated and exported as downloadable CSV and PDF summary reports.
  ```
- **Labels**: `feature`, `batch-processing`
- **Estimate**: `5 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

## 📂 Task 2: Repository Issue Template Configuration

The `.github/ISSUE_TEMPLATE/story.md` file has been added to the repository with the template structure.


---

### 🔹 Story 5 (Requirement 5): Explainable AI & SHAP Feature Attributions
- **Story Title**: Model Interpretability via SHAP Values
- **User Story**: **As a** Reliability Engineer, **I need** SHAP feature contribution charts for prediction outcomes, **So that** I can understand the underlying root causes of predicted machine failures.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: View SHAP Root Cause Attribution
    Given a machine prediction indicating high risk of failure
    When navigating to the Explainable AI module
    Then waterfall and summary SHAP plot visualizers render showing exact feature contributions to the failure risk.
  ```
- **Labels**: `enhancement`, `explainability`
- **Estimate**: `5 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

### 🔹 Story 6 (Requirement 6): Multi-Model Performance Benchmarking
- **Story Title**: Model Evaluation Benchmarking Module
- **User Story**: **As a** Data Scientist, **I need** a multi-model comparison benchmarking view, **So that** I can compare Logistic Regression, Random Forest, XGBoost, LightGBM, and CatBoost models on ROC-AUC, F1, and Recall metrics.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Compare Machine Learning Classifiers
    Given pre-evaluated metrics for 5 model architectures
    When clicking the Model Comparison tab
    Then interactive comparative ROC curves, Precision-Recall curves, and evaluation leaderboard tables are rendered side-by-side.
  ```
- **Labels**: `analytics`, `model-evaluation`
- **Estimate**: `3 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

### 🔹 Story 7 (Requirement 7): Real-time Monitoring & Alert Thresholds
- **Story Title**: Automated Alerting and Threshold Monitoring System
- **User Story**: **As an** Operations Specialist, **I need** automated threshold alerts when failure probability exceeds set safety limits, **So that** maintenance teams can be immediately notified.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Trigger Critical Failure Alert
    Given a machine risk score calculated at > 75%
    When real-time monitoring runs
    Then a high-priority alert badge appears on top dashboard with automated action recommendations.
  ```
- **Labels**: `feature`, `alerting`
- **Estimate**: `3 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

### 🔹 Story 8 (Requirement 8): Automated Ceiling Fan Quality Inspection
- **Story Title**: Smart Ceiling Fan Quality Inspection Workflow
- **User Story**: **As a** Quality Control Auditor, **I need** automated ceiling fan defect scoring, **So that** sub-standard ceiling fan assemblies are caught before shipment.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Execute Fan Assembly Quality Test
    Given quality metrics (wobble amplitude, acoustic noise level, power factor, speed deviation)
    When the quality inspection engine processes the assembly data
    Then pass/fail quality status and detailed component breakdown scores are generated.
  ```
- **Labels**: `must-have`, `quality-control`
- **Estimate**: `5 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`



---

### 🔹 Story 9 (Requirement 9): Legacy Data Pipeline Refactoring (Technical Debt)
- **Story Title**: Refactor Legacy Data Preprocessing Pipeline
- **User Story**: **As a** Lead Developer, **I need** to refactor legacy feature scaling code and add explicit static type hints, **So that** code maintainability is improved and technical debt is eliminated.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Refactor Pipeline and Enforce Typing
    Given legacy data preprocessing functions without type annotations
    When refactored into modular pipeline classes with type hints
    Then type checking passes without errors and unit test coverage exceeds 90%.
  ```
- **Labels**: `technical debt`, `refactoring` *(Requirement 9 labeled as technical debt)*
- **Estimate**: `3 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

### 🔹 Story 10 (Requirement 10): CI/CD Test Pipeline Acceleration (Technical Debt)
- **Story Title**: Optimize CI/CD Continuous Integration Test Pipeline
- **User Story**: **As a** DevOps Engineer, **I need** to optimize test suite execution and eliminate redundant asset loading, **So that** CI build times are reduced and technical debt in continuous integration is cleared.
- **Acceptance Criteria (Gherkin)**:
  ```gherkin
  Scenario: Run Accelerated CI Test Suite
    Given an automated GitHub Actions CI workflow taking > 3 minutes
    When parallel test execution and fixture caching are enabled
    Then the entire unit and integration test suite completes in under 45 seconds.
  ```
- **Labels**: `technical debt`, `devops` *(Requirement 10 labeled as technical debt)*
- **Estimate**: `2 Story Points`
- **Sprint / Milestone**: `Sprint 1 - Foundation & Core Architecture`
- **Assignee**: `@nivesh4087-spec`
- **Status**: `In Progress`

---

## 📈 Task 10: Sprint 1 Burndown Chart & Daily Tracking

### Sprint Velocity & Burndown Summary
- **Sprint Duration**: 10 Working Days (Day 0 to Day 10)
- **Total Initial Sprint Story Points**: **42 Story Points**
- **Sprint Goal**: Implement core predictive analytics, explainable AI, ceiling fan quality inspection, and clear technical debt.

### Daily Burndown Table
| Sprint Day | Ideal Remaining Points | Actual Remaining Points | Completed Stories on Day |
|---|---|---|---|
| **Day 0** | 42.0 | **42.0** | Sprint Planning & Backlog Refinement |
| **Day 1** | 37.8 | **42.0** | Architecture Setup & Environment Config |
| **Day 2** | 33.6 | **39.0** | Story 1 Completed (3 pts) |
| **Day 3** | 29.4 | **34.0** | Story 2 Completed (5 pts) |
| **Day 4** | 25.2 | **26.0** | Story 3 Completed (8 pts) |
| **Day 5** | 21.0 | **21.0** | Story 4 Completed (5 pts) |
| **Day 6** | 16.8 | **16.0** | Story 5 Completed (5 pts) |
| **Day 7** | 12.6 | **13.0** | Story 6 Completed (3 pts) |
| **Day 8** | 8.4  | **10.0** | Story 7 Completed (3 pts) |
| **Day 9** | 4.2  | **5.0**  | Story 8 Completed (5 pts) |
| **Day 10**| 0.0  | **0.0**  | Story 9 & Story 10 Technical Debt Completed (5 pts) |

### 🖼️ Burndown Chart Screenshot
The generated burndown chart PNG file is saved at:
`burndown_chart.png` and `docs/burndown_chart.png` in the repository.

---

## 🔗 Peer-Review Submission Checklist

When submitting your work for peer review, copy and paste the following links and details:

1. **Kanban Board URL**: `https://github.com/users/nivesh4087-spec/projects/1`
2. **GitHub Repository URL**: `https://github.com/nivesh4087-spec/Smart_Ceiling_Fan_Manufacturing_Failure_Prevention-`
3. **Burndown Chart Image**: Upload `burndown_chart.png` (located in root directory of project repository)
4. **Issue Template Location**: `.github/ISSUE_TEMPLATE/story.md`


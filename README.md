<div align="center">

# 🏭 Explainable AI-Based Manufacturing Failure Prediction

### Smart Ceiling Fan Production — Predictive Maintenance Platform

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-purple.svg)](https://shap.readthedocs.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-green.svg)](https://xgboost.readthedocs.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange.svg)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A production-quality AI/ML platform that predicts manufacturing equipment failures,
explains prediction reasoning using SHAP, and provides actionable maintenance recommendations.*

</div>

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Motivation](#-motivation)
- [Objectives](#-objectives)
- [Dataset](#-dataset)
- [System Architecture](#-system-architecture)
- [Methodology](#-methodology)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Results](#-model-results)
- [Explainable AI](#-explainable-ai)
- [Dashboard](#-dashboard)
- [Project Structure](#-project-structure)
- [Research Questions](#-research-questions)
- [Limitations](#-limitations)
- [Future Work](#-future-work)
- [Industry Extension](#-industry-extension)
- [Authors](#-authors)
- [References](#-references)

---

## 🎯 Problem Statement

Manufacturing equipment failures cause unplanned downtime, increased maintenance costs, and production losses. Traditional maintenance approaches (reactive or time-based) are either too late or too wasteful.

**This system predicts failure risk early, identifies the contributing factors, and provides interpretable decision support to maintenance personnel — before failures occur.**

## 💡 Motivation

- **Industry Need**: Predictive maintenance can reduce downtime by 30-50% and maintenance costs by 10-40% (McKinsey, 2020).
- **Explainability Gap**: Most ML models are black boxes. Manufacturing engineers need to understand *why* a failure is predicted to take appropriate action.
- **Value Add**: Combines ML, XAI, risk engineering, and industrial application in a single integrated system.

## 🎯 Objectives

1. Load, validate, and analyze the AI4I 2020 Predictive Maintenance Dataset
2. Engineer physically-meaningful features from raw process parameters
3. Train and compare multiple ML models with proper class imbalance handling
4. Implement probability calibration for reliable risk estimates
5. Use SHAP to explain predictions at both global and individual levels
6. Create an interpretable manufacturing risk score (0-100)
7. Build a professional Streamlit dashboard for interactive predictions
8. Provide actionable maintenance recommendations mapped to ceiling fan manufacturing

## 📊 Dataset

**AI4I 2020 Predictive Maintenance Dataset**
- **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset)
- **Records**: 10,000
- **Features**: 14 columns (6 process parameters + target + failure modes)
- **Target**: Binary — Machine failure (0/1)
- **Class Distribution**: ~96.6% No Failure / ~3.4% Failure (severe imbalance)

| Feature | Type | Description |
|---------|------|-------------|
| Type | Categorical | Product quality (L/M/H) |
| Air temperature [K] | Continuous | Ambient temperature |
| Process temperature [K] | Continuous | Machine temperature |
| Rotational speed [rpm] | Integer | Spindle/motor RPM |
| Torque [Nm] | Continuous | Applied torque |
| Tool wear [min] | Integer | Accumulated tool wear |
| Machine failure | Binary | Target — equipment failure |
| TWF/HDF/PWF/OSF/RNF | Binary | Individual failure modes |

> ⚠️ **Note**: The AI4I 2020 dataset is synthetic, generated to resemble real predictive maintenance scenarios. It is NOT actual factory data.

## 🏗️ System Architecture

```
User / Evaluator
     │
     ▼
┌─────────────────────────┐
│   Streamlit Dashboard    │ ← 6 interactive pages
│   (Industrial UI)        │
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│   Prediction Service     │ ← Cached model loading
└──────────┬──────────────┘
           ▼
┌──────────┬──────────────┬─────────────┐
│ Prepro-  │ ML Model     │ Probability │
│ cessing  │ (Best        │ Calibration │
│ Pipeline │ Selected)    │ (Isotonic)  │
└────┬─────┴──────┬───────┴──────┬──────┘
     │            │              │
     ▼            ▼              ▼
┌─────────┐ ┌──────────┐ ┌─────────────┐
│ Feature │ │ SHAP     │ │ Risk Score  │
│ Engine  │ │ Engine   │ │ Engine      │
└─────────┘ └────┬─────┘ └──────┬──────┘
                 │              │
                 ▼              ▼
         ┌──────────────────────────┐
         │ Recommendation Engine    │
         │ (Rule-based + SHAP)      │
         └──────────────────────────┘
```

## 🔬 Methodology

### ML Pipeline

```
Data Ingestion → Validation → EDA → Preprocessing → Feature Engineering
     → Train/Val/Test Split (70/15/15, stratified)
     → Class Imbalance Handling (train only)
     → Model Training + HPO (RandomizedSearchCV, 5-fold CV)
     → Model Comparison → Best Model Selection (F1 + PR-AUC)
     → Probability Calibration (Isotonic)
     → SHAP Explainability → Risk Scoring → Recommendations
```

### Feature Engineering (10 engineered features)

| Feature | Formula | Physical Rationale |
|---------|---------|-------------------|
| `temp_diff` | process_temp − air_temp | Heat dissipation indicator |
| `power` | torque × rpm × 2π/60 | Mechanical power (Watts) |
| `torque_per_rpm` | torque / rpm | Load efficiency |
| `strain` | tool_wear × torque | Combined mechanical strain |
| `power_factor` | torque × rpm | Power proxy |
| `temp_rpm_interaction` | temp_diff × rpm | Thermal-speed stress |
| `tool_wear_severity` | Binned wear | Non-linear wear effect |
| `is_high_torque` | torque > Q75 | High-load flag |
| `is_low_speed` | rpm < Q25 | Low-speed anomaly |
| `overload_indicator` | high torque AND low speed | Overstrain detection |

### Models Trained

| # | Model | Purpose |
|---|-------|---------|
| 1 | Logistic Regression | Interpretable baseline |
| 2 | Random Forest | Ensemble with feature importance |
| 3 | XGBoost | State-of-the-art gradient boosting |
| 4 | HistGradientBoosting | Fast sklearn-native boosting |

### Class Imbalance Handling

The dataset has only ~3.4% failure cases. Without handling:
- A model predicting "no failure" for everything achieves 96.6% accuracy
- **This is why accuracy alone is misleading**

Strategy: `class_weight='balanced'` with comparison to SMOTE (applied to training data only)

## 🛠️ Technologies

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| ML | scikit-learn, XGBoost |
| XAI | SHAP |
| Imbalance | imbalanced-learn |
| Dashboard | Streamlit |
| Visualization | Plotly, Matplotlib, Seaborn |
| Config | PyYAML |
| Serialization | Joblib |
| Testing | pytest |

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd iccet

# Install dependencies
pip install -r requirements.txt

# Train models (run once)
python scripts/train_pipeline.py

# Launch dashboard
streamlit run app/app.py
```

## 🚀 Usage

### 1. Train the ML Pipeline
```bash
python scripts/train_pipeline.py
```
This will:
- Download and validate the AI4I 2020 dataset
- Preprocess data and engineer features
- Train 4 models with hyperparameter optimization
- Evaluate, compare, and select the best model
- Calibrate probabilities
- Generate SHAP explanations and plots
- Save all artifacts to `models/`

### 2. Launch the Dashboard
```bash
streamlit run app/app.py
```

### 3. Run Tests
```bash
python -m pytest tests/ -v
```

## 📈 Model Results

Results are generated by the training pipeline and saved to `reports/results/`.

### Model Selection Criterion
- **Primary**: F1-Score (balances precision and recall for failure detection)
- **Secondary**: PR-AUC (robust to class imbalance, unlike ROC-AUC)

## 🔍 Explainable AI

### Global Explainability
- **SHAP Summary/Beeswarm Plot**: Shows how each feature value impacts failure prediction across all samples
- **SHAP Bar Plot**: Ranks features by average absolute SHAP value
- **Feature Importance Table**: Quantified contribution percentages

### Local Explainability
For each individual prediction:
- **SHAP Waterfall**: Shows exactly which features pushed the prediction toward or away from failure
- **Plain-English Explanation**: "High tool wear (200 min) → increases risk"
- **Recommended Actions**: Actionable maintenance suggestions

### Risk Score System

| Score | Category | Action |
|-------|----------|--------|
| 0-30 | 🟢 LOW RISK | Routine monitoring |
| 31-60 | 🟡 MODERATE RISK | Schedule inspection |
| 61-80 | 🟠 HIGH RISK | Prioritize maintenance |
| 81-100 | 🔴 CRITICAL RISK | Immediate attention |

> ⚠️ Risk thresholds are engineering defaults, not scientifically validated values. They require domain expert calibration for real deployment.

## 🖥️ Dashboard

6-page professional Streamlit dashboard:

| Page | Description |
|------|-------------|
| 📊 Executive Overview | KPIs, model performance, class distribution, research status |
| 🎯 Risk Predictor | Manual input, demo scenarios, risk gauge, SHAP explanation |
| 🔍 Explainable AI | Global SHAP plots, local explanations, industry mapping |
| 📈 Model Comparison | Metrics table, ROC/PR curves, confusion matrices, ablation |
| 🗂️ Data Explorer | Interactive filtering, distributions, correlations |
| 🔔 Monitoring & Alerts | Prediction history, alert feed, risk timeline |

## 📁 Project Structure

```
iccet/
├── config/
│   └── config.yaml              # Central configuration
├── data/
│   ├── raw/                     # Original dataset
│   └── processed/               # Processed data
├── src/
│   ├── data/
│   │   ├── loader.py            # Dataset download & loading
│   │   └── validator.py         # Schema & quality validation
│   ├── preprocessing/
│   │   └── pipeline.py          # Cleaning, encoding, scaling
│   ├── features/
│   │   └── engineer.py          # Feature engineering
│   ├── models/
│   │   └── trainer.py           # Training, HPO, calibration
│   ├── evaluation/
│   │   └── evaluator.py         # Metrics & plots
│   ├── explainability/
│   │   └── shap_engine.py       # SHAP global/local
│   ├── risk/
│   │   └── scoring.py           # Risk score & early warning
│   └── recommendations/
│       └── engine.py            # Maintenance recommendations
├── app/
│   ├── app.py                   # Streamlit entry point
│   ├── components/
│   │   └── styles.py            # Industrial CSS theme
│   └── pages/                   # 6 dashboard pages
├── models/                      # Saved model artifacts
├── reports/
│   ├── figures/                 # Generated plots
│   └── results/                 # Metrics & results
├── tests/                       # Unit tests (5 modules)
├── scripts/
│   └── train_pipeline.py        # End-to-end training
├── requirements.txt
├── README.md
└── .gitignore
```

## 🔬 Research Questions

| # | Question | Method |
|---|----------|--------|
| RQ1 | Which ML model provides best failure prediction? | Compare LR/RF/XGB/HGBM on F1, PR-AUC |
| RQ2 | Which parameters contribute most to failure? | SHAP global feature importance |
| RQ3 | Does class imbalance handling improve detection? | Ablation: balanced vs unbalanced |
| RQ4 | Does calibration improve risk estimates? | Compare Brier scores |
| RQ5 | Can SHAP make predictions interpretable? | Qualitative local explanation analysis |

## ⚠️ Limitations

1. **Synthetic Dataset**: AI4I 2020 is synthetic — not from an actual factory
2. **Conceptual Mapping**: The ceiling fan manufacturing mapping is conceptual, not validated
3. **Static Analysis**: No real-time streaming or time-series modeling
4. **Risk Thresholds**: Default thresholds require domain expert calibration
5. **Recommendations**: AI-generated decision support, NOT certified procedures
6. **Generalization**: Model performance on real factory data may differ

## 🔮 Future Work

| Phase | Description | Technologies |
|-------|-------------|-------------|
| **Phase 1** (Current) | AI4I prototype with XAI | Python, Streamlit, SHAP |
| **Phase 2** | Real company sensor data | Factory IoT integration |
| **Phase 3** | Real-time IoT streaming | MQTT, Kafka, Edge computing |
| **Phase 4** | Production deployment | Docker, FastAPI, Cloud, RBAC |

### Additional Extensions
- Time-series models (LSTM, Transformer)
- Federated learning for multi-factory deployment
- Digital twin integration
- Maintenance ticket system integration
- Online/incremental learning

## 🏭 Industry Extension — Ceiling Fan Manufacturing

| AI4I Feature | Fan Manufacturing Interpretation |
|-------------|--------------------------------|
| Air temperature | Ambient factory floor temperature |
| Process temperature | Motor winding / assembly temperature |
| Rotational speed | Fan motor test RPM during QC |
| Torque | Motor shaft torque during blade assembly |
| Tool wear | Pressing/cutting tool wear in blade stamping |
| Type (L/M/H) | Product tier (Economy/Standard/Premium) |

> This mapping demonstrates methodology transfer potential. Real deployment requires actual factory sensor data.

## 👤 Authors

- **Nivesh** — Principal AI/ML Engineer

## 📚 References

1. Matzka, S. (2020). *AI4I 2020 Predictive Maintenance Dataset*. UCI Machine Learning Repository. DOI: 10.24432/C5HS5C
2. Lundberg, S. M., & Lee, S. I. (2017). *A Unified Approach to Interpreting Model Predictions*. NeurIPS.
3. Chawla, N. V., et al. (2002). *SMOTE: Synthetic Minority Over-sampling Technique*. JAIR.
4. Chen, T., & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System*. KDD.

---

<div align="center">

*Enterprise-Grade Predictive Maintenance Platform*

**"Instead of waiting for equipment to fail, predict risk early, explain the factors, and act before it's too late."**

</div>

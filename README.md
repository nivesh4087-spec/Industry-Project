<div align="center">

# 🏭 AI-Powered Predictive Maintenance Platform

### Smart Ceiling Fan Manufacturing — Failure Prevention & Risk Intelligence

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-purple.svg)](https://shap.readthedocs.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-green.svg)](https://xgboost.readthedocs.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange.svg)](https://scikit-learn.org)

*An enterprise predictive maintenance platform that forecasts equipment failures,
provides explainable risk intelligence via SHAP, and delivers actionable maintenance directives for manufacturing operations.*

</div>

---

## 📋 Table of Contents

- [Business Value](#-business-value)
- [Platform Overview](#-platform-overview)
- [System Architecture](#-system-architecture)
- [Sensor Data Pipeline](#-sensor-data-pipeline)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Performance](#-model-performance)
- [Explainable AI](#-explainable-ai)
- [Dashboard](#-dashboard)
- [Project Structure](#-project-structure)
- [Industry Application](#-industry-application)
- [Authors](#-authors)


---

## 💰 Business Value

| Metric | Impact |
|--------|--------|
| **Downtime Reduction** | 30-50% reduction in unplanned equipment downtime |
| **Maintenance Cost Savings** | 10-40% reduction through targeted interventions |
| **False Alarm Rate** | Minimized unnecessary inspections via precision-tuned models |
| **Decision Transparency** | Full SHAP-based explainability for every prediction |
| **ROI** | Built-in financial ROI simulator with configurable cost parameters |

## 🏭 Platform Overview

This platform provides **end-to-end predictive maintenance** for ceiling fan manufacturing operations:

1. **Real-time Risk Assessment** — Input machine sensor data and receive instant failure probability with risk scoring (0-100)
2. **Explainable Predictions** — Every prediction includes SHAP-powered feature attribution showing exactly which sensor readings drive the risk
3. **Batch Processing** — Upload CSV/Excel files for fleet-wide failure risk assessment
4. **Financial ROI Dashboard** — Compare maintenance strategies (reactive vs. preventive vs. AI-predictive) with configurable cost parameters
5. **Monitoring & Alerts** — Track prediction history, risk trends, and high-risk alerts across sessions

## 🏗️ System Architecture

```
Production Line / QC Station
     │
     ▼
┌─────────────────────────┐
│   Streamlit Dashboard    │ ← 7 interactive modules
│   (Industrial Command    │
│    Center)               │
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│   Prediction Service     │ ← Cached model loading
└──────────┬──────────────┘
           ▼
┌──────────┬──────────────┬─────────────┐
│ Prepro-  │ ML Model     │ Probability │
│ cessing  │ Engine       │ Calibration │
│ Pipeline │ (XGBoost/RF) │ (Isotonic)  │
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

## 🔬 Sensor Data Pipeline

### Feature Engineering (10 derived features)

| Feature | Formula | Industrial Significance |
|---------|---------|----------------------|
| `temp_diff` | process_temp − air_temp | Heat dissipation efficiency |
| `power` | torque × rpm × 2π/60 | Mechanical power output (Watts) |
| `torque_per_rpm` | torque / rpm | Load efficiency ratio |
| `strain` | tool_wear × torque | Combined mechanical strain |
| `power_factor` | torque × rpm | Power approximation |
| `temp_rpm_interaction` | temp_diff × rpm | Thermal-speed stress |
| `tool_wear_severity` | Binned wear levels | Non-linear wear threshold |
| `is_high_torque` | torque > Q75 | High-load operating flag |
| `is_low_speed` | rpm < Q25 | Low-speed anomaly flag |
| `overload_indicator` | high torque AND low speed | Overstrain detection |

### ML Models Deployed

| # | Model | Role |
|---|-------|---------| 
| 1 | Logistic Regression | Interpretable baseline |
| 2 | Random Forest | Ensemble with feature importance |
| 3 | XGBoost | High-performance gradient boosting |
| 4 | HistGradientBoosting | Fast sklearn-native boosting |

### Class Imbalance Handling

The dataset has ~3.4% failure cases. Strategy: `class_weight='balanced'` with comparison to SMOTE (applied to training data only), ensuring the model doesn't bias toward predicting "no failure."

## 🛠️ Technologies

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| ML | scikit-learn, XGBoost |
| Explainability | SHAP |
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
streamlit run app/main.py
```

## 🚀 Usage

### 1. Train the ML Pipeline
```bash
python scripts/train_pipeline.py
```
This will:
- Load and validate the manufacturing sensor dataset
- Preprocess data and engineer features
- Train 4 models with hyperparameter optimization
- Evaluate, compare, and select the best model
- Calibrate probabilities for reliable risk estimates
- Generate SHAP explanations and plots
- Save all artifacts to `models/`

### 2. Launch the Dashboard
```bash
streamlit run app/main.py
```

### 3. Run Tests
```bash
python -m pytest tests/ -v
```

## 📈 Model Performance

Results are generated by the training pipeline and saved to `reports/results/`.

### Model Selection
- **Primary Metric**: F1-Score (balances precision and recall for failure detection)
- **Secondary Metric**: PR-AUC (robust to class imbalance, unlike ROC-AUC)
- **Accuracy is NOT used** as the primary metric due to severe class imbalance (~96.6% majority class)

## 🔍 Explainable AI

### Global Explainability
- **SHAP Summary Plot**: Shows how each sensor reading impacts failure prediction across the entire fleet
- **SHAP Feature Importance**: Ranks features by average absolute SHAP value
- **Contribution Analysis**: Quantified percentage contribution of each feature

### Local Explainability
For each individual prediction:
- **SHAP Waterfall**: Shows exactly which readings push risk up or down
- **Plain-English Explanation**: "High tool wear (200 min) → increases failure risk"
- **Actionable Recommendations**: Targeted maintenance directives

### Risk Score System

| Score | Category | Recommended Action |
|-------|----------|-----------|
| 0-30 | 🟢 LOW RISK | Continue routine monitoring |
| 31-60 | 🟡 MODERATE RISK | Schedule next-window inspection |
| 61-80 | 🟠 HIGH RISK | Prioritize maintenance intervention |
| 81-100 | 🔴 CRITICAL RISK | Immediate maintenance required |

## 🖥️ Dashboard

7-module professional industrial command center:

| Module | Description |
|--------|-------------|
| 📊 Executive Overview | KPIs, model performance, financial ROI simulator |
| 🎯 Risk Predictor | Manual sensor input, demo scenarios, risk gauge, SHAP explanation |
| 🔍 Explainable AI | Global SHAP plots, local explanations, industry context |
| 📈 Model Comparison | Metrics table, ROC/PR curves, confusion matrices, cost evaluation |
| 🗂️ Data Explorer | Interactive filtering, distributions, correlations |
| 📤 Upload & Predict | Batch CSV/Excel upload with fleet-wide predictions |
| 🔔 Monitoring & Alerts | Prediction history, alert feed, risk timeline |

## 📁 Project Structure

```
iccet/
├── config/
│   └── config.yaml              # Central configuration
├── data/
│   ├── raw/                     # Raw sensor data
│   └── processed/               # Processed data
├── src/
│   ├── data/
│   │   ├── loader.py            # Dataset loading
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
│   ├── main.py                  # Streamlit entry point
│   ├── components/
│   │   └── styles.py            # Industrial CSS theme
│   └── pages/                   # 7 dashboard modules
├── models/                      # Saved model artifacts
├── reports/
│   ├── figures/                 # Generated plots
│   └── results/                 # Metrics & results
├── tests/                       # Unit tests
├── scripts/
│   └── train_pipeline.py        # End-to-end training
├── requirements.txt
├── README.md
└── .gitignore
```

## 🏭 Industry Application — Ceiling Fan Manufacturing

| Sensor / Feature | Manufacturing Context |
|-----------------|----------------------|
| Air Temperature | Ambient factory floor temperature |
| Process Temperature | Motor winding / assembly station temperature |
| Rotational Speed | Fan motor test RPM during quality check |
| Torque | Motor shaft torque during blade assembly |
| Tool Wear | Pressing/cutting tool wear in blade stamping |
| Product Type (L/M/H) | Product quality tier (Economy/Standard/Premium) |

## 👤 Authors

- **Nivesh** — AI/ML Platform Engineer

---

<div align="center">

*AI-Powered Predictive Maintenance Platform for Industrial Manufacturing*

**"Predict risk early. Explain the factors. Act before failure."**

</div>

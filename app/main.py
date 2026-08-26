"""
XAI Predictive Maintenance Platform
======================================
Main Streamlit application entry point.

Enterprise-grade Industrial AI Command Center for Explainable Predictive Maintenance.

Usage:
    streamlit run app/main.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to Python path and remove app directory to avoid module shadowing
project_root = Path(__file__).resolve().parent.parent
app_dir = str(Path(__file__).resolve().parent)
if app_dir in sys.path:
    sys.path.remove(app_dir)
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
else:
    sys.path.remove(str(project_root))
    sys.path.insert(0, str(project_root))

import streamlit as st
import json
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Page configuration — must be first Streamlit command
st.set_page_config(
    page_title="AI4I Maintenance Command Center | Enterprise AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from app.components.styles import get_custom_css, render_header_banner, render_status_badge

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================================
# Cache model loading — runs only once
# ============================================================================

@st.cache_resource(show_spinner="Loading AI models...")
def load_artifacts():
    """Load all saved model artifacts. Cached to avoid reloading."""
    from src.models.trainer import load_model_artifacts
    from src.data.loader import load_config

    config = load_config(str(project_root / "config" / "config.yaml"))
    artifacts = load_model_artifacts(config, project_root)
    return artifacts, config

@st.cache_data(show_spinner="Loading dataset...")
def load_raw_dataset():
    """Load the raw dataset for exploration. Cached."""
    from src.data.loader import load_config, load_dataset
    config = load_config(str(project_root / "config" / "config.yaml"))
    df = load_dataset(config)
    return df

@st.cache_data(show_spinner="Loading results...")
def load_results_json(filename: str):
    """Load a JSON results file."""
    filepath = project_root / "reports" / "results" / filename
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return None

# ============================================================================
# Initialize session state
# ============================================================================

def init_session_state():
    """Initialize session state variables."""
    if "prediction_history" not in st.session_state:
        from src.risk.scoring import PredictionHistory
        st.session_state.prediction_history = PredictionHistory(max_entries=500)

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Asset Health Monitor"

init_session_state()

# ============================================================================
# Sidebar Navigation
# ============================================================================

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        # Brand header
        st.markdown("""
        <div style="text-align: center; padding: 16px 0 10px 0;">
            <div style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(59,130,246,0.4));">🛡️</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #f8fafc;
                        letter-spacing: -0.02em; margin-top: 4px;">
                ENTERPRISE APM
            </div>
            <div style="font-size: 0.65rem; color: #3b82f6; font-weight: 700;
                        letter-spacing: 0.15em; text-transform: uppercase;">
                AI Predictive Maintenance
            </div>
        </div>
        <hr style="border-color: #232d3f; margin: 12px 0;">
        """, unsafe_allow_html=True)

        # Navigation Streamlined & Professional
        pages = {
            "⚡ Asset Health Monitor": "Asset Health Monitor",
            "🎯 Predictive Risk Assessment": "Predictive Risk Assessment",
            "🧠 AI Diagnostics & SHAP": "AI Diagnostics & SHAP",
            "📊 Financial ROI & Models": "Financial ROI & Models",
            "📤 Batch Fleet Analysis": "Batch Fleet Analysis",
            "🔔 Fleet Alerts": "Fleet Alerts",
        }

        selected = st.radio(
            "Navigation",
            list(pages.keys()),
            label_visibility="collapsed",
        )
        st.session_state.current_page = pages[selected]

        st.markdown("<hr style='border-color: #232d3f;'>", unsafe_allow_html=True)

        # System info — dynamic
        has_upload = "uploaded_dataset" in st.session_state
        upload_indicator = (
            f'<div style="color: #10b981; font-weight: 600;">📂 Custom Batch Data</div>'
            if has_upload else
            f'<div style="color: #94a3b8;">📦 Production Fleet Telemetry</div>'
        )

        st.markdown(f"""
        <div style="font-size: 0.72rem; color: #64748b; padding: 0 4px;">
            <div style="margin-bottom: 8px;">
                <strong style="color: #cbd5e1;">SYSTEM TELEMETRY</strong>
            </div>
            <div style="margin-bottom: 4px;">🟢 <strong>Engine Status</strong>: Active</div>
            <div style="margin-bottom: 4px;">{upload_indicator}</div>
            <div style="margin-bottom: 4px;">⚡ <strong>Explainability</strong>: SHAP v0.42</div>
            <div style="margin-top: 12px; padding-top: 8px; border-top: 1px solid #1e293b;">
                <span style="color: #94a3b8;">System Version</span>: v3.0.0 Pro
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color: #232d3f;'>", unsafe_allow_html=True)
        if st.button("❓ User Guide & Quick Tutorial", use_container_width=True):
            st.session_state.show_tutorial = True

        with st.expander("🗄️ Connect External Database"):
            st.markdown("<div style='font-size:0.75rem; color:#94a3b8;'>Connect enterprise databases for real-time telemetry streaming:</div>", unsafe_allow_html=True)
            db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "SQLite", "MongoDB", "Snowflake", "Oracle"], key="sidebar_db_type")
            conn_str = st.text_input("Connection URI", placeholder="postgresql://user:pass@localhost:5432/mydb", key="sidebar_conn_str")
            query_str = st.text_input("Table / SQL Query", value="SELECT * FROM telemetry_data LIMIT 1000", key="sidebar_query_str")
            if st.button("Connect & Sync", key="sidebar_db_btn"):
                if conn_str:
                    try:
                        from src.data.loader import load_from_database
                        df_db = load_from_database(db_type, conn_str, query_str)
                        st.session_state.uploaded_dataset = df_db
                        st.success(f"Connected to {db_type}! Loaded {len(df_db)} records.")
                        st.rerun()
                    except Exception as err:
                        st.error(f"Connection error: {err}")
                else:
                    st.warning("Please enter a valid Connection URI.")

        st.markdown("""
        <div style="margin-top: 20px; font-size: 0.68rem; color: #475569; border: 1px dashed #232d3f; padding: 10px; border-radius: 6px;">
            ℹ️ <strong>Industrial Telemetry Notice:</strong> Predictions are generated using calibrated ensemble models. Verify physical equipment prior to maintenance interventions.
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# Page Router
# ============================================================================

@st.dialog("🚀 Welcome to Enterprise APM — Platform User Tutorial", width="large")
def render_tutorial_dialog():
    st.markdown("""
    ### 🛡️ Welcome to your AI Predictive Maintenance Command Center!
    This quick tutorial will guide you through the key modules and profile navigation so you can get started quickly:

    ---
    #### 1️⃣ ⚡ **Asset Health Monitor**
    - High-level executive dashboard showing total fleet health, failure distribution, and active risk alerts.
    - View health score distribution across your machine inventory.

    #### 2️⃣ 🎯 **Predictive Risk Assessment**
    - Perform single-asset real-time diagnosis.
    - Adjust operational parameters (Temperatures, Rotational Speed, Torque, Tool Wear) to view immediate failure probability and maintenance recommendations.

    #### 3️⃣ 🧠 **AI Diagnostics & SHAP**
    - Deep-dive into model explainability.
    - Understand **WHY** an asset is flagged for maintenance using global & local SHAP feature impact plots.

    #### 4️⃣ 📤 **Batch Fleet Analysis & Database Integration**
    - Upload custom CSV/Excel telemetry files or connect your external databases (PostgreSQL, MySQL, SQLite, Snowflake, MongoDB).
    - Run batch predictions across thousands of assets simultaneously with standard column auto-mapping.

    #### 5️⃣ 🔔 **Fleet Alerts & Financial ROI**
    - Review critical threshold alerts and evaluate the financial ROI ($ savings) from prevented unplanned downtime.

    ---
    💡 *Tip: You can re-open this tutorial anytime from the sidebar standard menu!*
    """)
    if st.button("Got it! Let's get started", use_container_width=True, type="primary"):
        st.session_state.show_tutorial = False
        st.rerun()

def main():
    """Main application — routes to selected page."""
    render_sidebar()

    if st.session_state.get("show_tutorial", False):
        render_tutorial_dialog()

    page = st.session_state.current_page

    try:
        if page == "Asset Health Monitor":
            from app.pages.executive_overview import render_page
            render_page(project_root, load_artifacts, load_raw_dataset, load_results_json)

        elif page == "Predictive Risk Assessment":
            from app.pages.risk_predictor import render_page
            render_page(project_root, load_artifacts, load_raw_dataset)

        elif page == "AI Diagnostics & SHAP":
            from app.pages.explainable_ai import render_page
            render_page(project_root, load_artifacts, load_raw_dataset, load_results_json)

        elif page == "Financial ROI & Models":
            from app.pages.model_comparison import render_page
            render_page(project_root, load_artifacts, load_results_json, load_raw_dataset)

        elif page == "Batch Fleet Analysis":
            from app.pages.upload_predict import render_page
            render_page(project_root, load_artifacts, load_raw_dataset)

        elif page == "Fleet Alerts":
            from app.pages.monitoring_alerts import render_page
            render_page(project_root)

    except FileNotFoundError as e:
        st.error(f"""
        **Model artifacts not found.** Please run the training pipeline first:

        ```bash
        python scripts/train_pipeline.py
        ```

        Error: {e}
        """)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check the logs or try refreshing the page.")

if __name__ == "__main__":
    main()
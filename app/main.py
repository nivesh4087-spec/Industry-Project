"""
XAI Predictive Maintenance Dashboard
======================================
Main Streamlit application entry point.

Industrial AI Command Center for Explainable Predictive Maintenance.

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
    page_title="XAI Predictive Maintenance | Industrial AI",
    page_icon="🏭",
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
        st.session_state.current_page = "Executive Overview"


init_session_state()


# ============================================================================
# Sidebar Navigation
# ============================================================================

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        # Brand header
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 12px 0;">
            <div style="font-size: 2.8rem; filter: drop-shadow(0 0 8px rgba(59,130,246,0.3));">🏭</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #e2e8f0;
                        letter-spacing: -0.02em; margin-top: 6px;">
                XAI Predictive
            </div>
            <div style="font-size: 1.15rem; font-weight: 800;
                        background: linear-gradient(135deg, #3b82f6, #06b6d4);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        letter-spacing: -0.02em;">
                Maintenance
            </div>
            <div style="font-size: 0.6rem; color: #64748b; margin-top: 6px;
                        letter-spacing: 0.12em; text-transform: uppercase;">
                Industrial AI Platform v2.0
            </div>
        </div>
        <hr style="border-color: #2a3a4e; margin: 12px 0;">
        """, unsafe_allow_html=True)

        # Navigation
        pages = {
            "📊 Executive Overview": "Executive Overview",
            "🎯 Risk Predictor": "Risk Predictor",
            "🔍 Explainable AI": "Explainable AI",
            "📈 Model Comparison": "Model Comparison",
            "🗂️ Data Explorer": "Data Explorer",
            "📤 Upload & Predict": "Upload & Predict",
            "🔔 Monitoring & Alerts": "Monitoring & Alerts",
        }

        selected = st.radio(
            "Navigation",
            list(pages.keys()),
            label_visibility="collapsed",
        )
        st.session_state.current_page = pages[selected]

        st.markdown("<hr style='border-color: #2a3a4e;'>", unsafe_allow_html=True)

        # System info — dynamic
        has_upload = "uploaded_dataset" in st.session_state
        upload_indicator = (
            f'<div style="color: #22c55e;">📂 Custom Data Loaded</div>'
            if has_upload else
            f'<div>📦 AI4I 2020 Dataset</div>'
        )

        st.markdown(f"""
        <div style="font-size: 0.7rem; color: #64748b; padding: 0 8px;">
            <div style="margin-bottom: 8px;">
                <strong style="color: #94a3b8;">System Status</strong>
            </div>
            <div>🟢 Model Loaded</div>
            {upload_indicator}
            <div>🔬 SHAP Engine Active</div>
            <div style="margin-top: 10px;">
                <strong style="color: #94a3b8;">Version</strong>: 2.0.0
            </div>
            <div>
                <strong style="color: #94a3b8;">Model</strong>: Best Selected
            </div>
            <div style="margin-top: 6px; font-size: 0.62rem; color: #475569;">
                Last loaded: {datetime.now().strftime("%H:%M:%S")}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer" style="margin-top: 20px;">
            ⚠️ This system provides AI-generated decision-support.
            Predictions are model estimates, not guaranteed outcomes.
            The AI4I 2020 dataset is synthetic. Industry mapping is conceptual.
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Page Router
# ============================================================================

def main():
    """Main application — routes to selected page."""
    render_sidebar()

    page = st.session_state.current_page

    try:
        if page == "Executive Overview":
            from app.pages.p1_executive_overview import render_page
            render_page(project_root, load_artifacts, load_raw_dataset, load_results_json)

        elif page == "Risk Predictor":
            from app.pages.p2_risk_predictor import render_page
            render_page(project_root, load_artifacts, load_raw_dataset)

        elif page == "Explainable AI":
            from app.pages.p3_explainable_ai import render_page
            render_page(project_root, load_artifacts, load_raw_dataset, load_results_json)

        elif page == "Model Comparison":
            from app.pages.p4_model_comparison import render_page
            render_page(project_root, load_artifacts, load_results_json)

        elif page == "Data Explorer":
            from app.pages.p5_data_explorer import render_page
            render_page(project_root, load_raw_dataset)

        elif page == "Upload & Predict":
            from app.pages.p7_upload_predict import render_page
            render_page(project_root, load_artifacts)

        elif page == "Monitoring & Alerts":
            from app.pages.p6_monitoring_alerts import render_page
            render_page(project_root)

    except FileNotFoundError as e:
        st.error(f"""
        **Model artifacts not found.** Please run the training pipeline first:

        ```bash
        cd {project_root}
        python scripts/train_pipeline.py
        ```

        Error: {e}
        """)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check the logs or try refreshing the page.")


if __name__ == "__main__":
    main()

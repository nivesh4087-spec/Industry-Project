"""
Page 1 — Executive Overview
============================
Dashboard home page with KPI cards, system status, and model performance summary.
"""

import streamlit as st
import json
from pathlib import Path

from app.components.styles import render_kpi_card, render_header_banner


def render_page(project_root, load_artifacts_fn, load_dataset_fn, load_results_fn):
    """Render the Executive Overview page."""

    st.markdown(render_header_banner(
        "Executive Overview",
        "AI-Powered Predictive Maintenance Command Center — Smart Ceiling Fan Manufacturing"
    ), unsafe_allow_html=True)

    # Load data
    try:
        artifacts, config = load_artifacts_fn()
        test_results = artifacts.get("test_results", [])
        best_name = artifacts.get("best_model_name", "N/A")
        df = load_dataset_fn()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.info("Run `python scripts/train_pipeline.py` first.")
        return

    # ========================================================================
    # KPI ROW 1 — Dataset & System
    # ========================================================================

    target_col = config["data"]["target_column"]
    n_records = len(df)
    n_failures = int(df[target_col].sum())
    failure_rate = round(n_failures / n_records * 100, 1)

    # Get best model metrics
    best_metrics = next((r for r in test_results if r["model"] == best_name), {})
    best_f1 = best_metrics.get("f1", 0)
    best_pr_auc = best_metrics.get("pr_auc", 0)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(render_kpi_card(
            "Total Records", f"{n_records:,}",
            "AI4I 2020 Dataset", "blue"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(render_kpi_card(
            "Failure Cases", f"{n_failures}",
            f"{failure_rate}% failure rate", "red"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(render_kpi_card(
            "Features Used", f"{len(artifacts.get('feature_names', []))}",
            "6 base + 10 engineered", "cyan"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(render_kpi_card(
            "Best Model F1", f"{best_f1:.3f}",
            best_name, "green"
        ), unsafe_allow_html=True)

    with col5:
        st.markdown(render_kpi_card(
            "PR-AUC", f"{best_pr_auc:.3f}",
            "Precision-Recall AUC", "purple"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================================
    # ROW 2 — Model Performance & Class Distribution
    # ========================================================================

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Model Performance Comparison")

        if test_results:
            import pandas as pd
            results_df = pd.DataFrame([
                {
                    "Model": r["model"],
                    "Precision": r["precision"],
                    "Recall": r["recall"],
                    "F1-Score": r["f1"],
                    "PR-AUC": r["pr_auc"],
                    "ROC-AUC": r["roc_auc"],
                    "Brier Score": r["brier_score"],
                }
                for r in test_results
            ])

            # Highlight best model
            st.dataframe(
                results_df.style.highlight_max(
                    subset=["Precision", "Recall", "F1-Score", "PR-AUC", "ROC-AUC"],
                    color="#1a3a2a",
                ).highlight_min(
                    subset=["Brier Score"],
                    color="#1a3a2a",
                ).format({
                    "Precision": "{:.4f}",
                    "Recall": "{:.4f}",
                    "F1-Score": "{:.4f}",
                    "PR-AUC": "{:.4f}",
                    "ROC-AUC": "{:.4f}",
                    "Brier Score": "{:.4f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

            st.info(f"🏆 **Best Model: {best_name}** — Selected based on F1-Score "
                    f"(primary) and PR-AUC (secondary). Accuracy is intentionally "
                    f"not used as the primary metric due to severe class imbalance.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### ⚖️ Class Distribution")

        import plotly.graph_objects as go

        fig = go.Figure(data=[go.Pie(
            labels=["No Failure", "Failure"],
            values=[n_records - n_failures, n_failures],
            hole=0.6,
            marker_colors=["#22c55e", "#ef4444"],
            textinfo="label+percent",
            textfont_size=13,
        )])
        fig.update_layout(
            showlegend=False,
            height=280,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            annotations=[dict(
                text=f"{failure_rate}%<br>Failure",
                x=0.5, y=0.5, font_size=16,
                font_color="#ef4444",
                showarrow=False,
            )]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.warning(f"⚠️ **Severe class imbalance** — Only {failure_rate}% of records "
                   f"are failures. Accuracy alone would be ~{100-failure_rate:.1f}% "
                   f"by always predicting 'No Failure'.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # ROW 3 — Research Insights & System Architecture
    # ========================================================================

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🔬 Research Questions Addressed")

        st.markdown("""
        | # | Research Question | Status |
        |---|---|---|
        | RQ1 | Which ML model provides best failure prediction? | ✅ Answered |
        | RQ2 | Which parameters contribute most to failure? | ✅ Answered |
        | RQ3 | Does class imbalance handling improve detection? | ✅ Answered |
        | RQ4 | Does calibration improve risk estimates? | ✅ Answered |
        | RQ5 | Can SHAP make predictions interpretable? | ✅ Answered |
        """)

        # Load calibration results
        cal_results = load_results_fn("calibration_results.json")
        if cal_results:
            improvement = cal_results.get("improvement", 0)
            st.success(f"📐 Probability calibration improved Brier Score by "
                       f"**{improvement:.4f}** using {cal_results.get('method', 'isotonic')} method.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🏗️ System Architecture")

        st.markdown("""
        ```
        User / Evaluator
             │
             ▼
        ┌─────────────────────┐
        │  Streamlit Dashboard │ ← You are here
        └──────────┬──────────┘
                   ▼
        ┌─────────────────────┐
        │  Prediction Service  │
        └──────────┬──────────┘
                   ▼
        ┌─────────────────────┐
        │  Preprocessing       │
        │  Pipeline            │
        └──────────┬──────────┘
                   ▼
        ┌──────┬───────┬──────┐
        │  ML  │ Calib │ SHAP │
        │Model │ rator │Engine│
        └──┬───┴───┬───┴──┬───┘
           ▼       ▼      ▼
        Risk Engine → Recommendations
        ```
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # CEILING FAN MANUFACTURING MAPPING
    # ========================================================================

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🏭 Ceiling Fan Manufacturing — Conceptual Industry Mapping")

    st.caption("⚠️ **CONCEPTUAL MAPPING**: The AI4I 2020 dataset is synthetic. "
               "This mapping shows how the methodology could transfer to real "
               "ceiling fan production. It does NOT claim real factory data.")

    import pandas as pd
    mapping_data = config.get("industry_mapping", {})
    base_features = {
        "air_temp_k": "Air Temperature [K]",
        "process_temp_k": "Process Temperature [K]",
        "rotational_speed_rpm": "Rotational Speed [RPM]",
        "torque_nm": "Torque [Nm]",
        "tool_wear_min": "Tool Wear [min]",
        "type": "Product Type (L/M/H)",
    }

    mapping_df = pd.DataFrame([
        {
            "AI4I Feature": base_features.get(k, k),
            "Internal Name": k,
            "Fan Manufacturing Interpretation": v,
        }
        for k, v in mapping_data.items()
        if k in base_features
    ])

    if not mapping_df.empty:
        st.dataframe(mapping_df, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        XAI Predictive Maintenance System v1.0.0 |
        AI4I 2020 Dataset | SHAP Explainability |
        Smart Ceiling Fan Manufacturing — Conceptual Mapping<br>
        Built for academic project evaluation — B.Tech Computer Engineering
    </div>
    """, unsafe_allow_html=True)

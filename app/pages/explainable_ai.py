"""
Page 3 — Explainable AI
========================
Global and local SHAP explanations for model predictions.

Shows:
- Global feature importance (SHAP bar plot, summary/beeswarm)
- Feature importance ranking table
- Local explanations for individual samples
- Industry mapping context
"""

import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

from app.components.styles import render_header_banner


def render_page(project_root, load_artifacts_fn, load_dataset_fn, load_results_fn):
    """Render the Explainable AI page."""

    st.markdown(render_header_banner(
        "Explainable AI — SHAP Analysis",
        "Understanding WHY the model predicts failure using SHapley Additive exPlanations"
    ), unsafe_allow_html=True)

    # Load artifacts
    try:
        artifacts, config = load_artifacts_fn()
    except Exception as e:
        st.error(f"Model not loaded: {e}")
        return

    tabs = st.tabs(["🌐 Global Explainability", "🔬 Local Explainability", "🏭 Industry Mapping"])

    # ========================================================================
    # TAB 1 — Global Explainability
    # ========================================================================

    with tabs[0]:
        st.markdown("### Global Feature Importance")
        st.markdown(
            "Global SHAP analysis answers: **'What factors generally cause the model "
            "to predict failure?'** Features are ranked by their average impact on "
            "predictions across the entire test set."
        )

        # Load pre-computed SHAP importance
        shap_data = load_results_fn("shap_analysis.json")

        if shap_data and "feature_importance" in shap_data:
            importance = shap_data["feature_importance"]
            imp_df = pd.DataFrame(importance)

            # Bar chart
            fig = go.Figure(go.Bar(
                y=imp_df["feature"].head(12),
                x=imp_df["mean_abs_shap"].head(12),
                orientation="h",
                marker_color="#3b82f6",
                text=[f"{v:.4f}" for v in imp_df["mean_abs_shap"].head(12)],
                textposition="outside",
                textfont=dict(size=11, color="#94a3b8"),
            ))
            fig.update_layout(
                title="SHAP Feature Importance — Mean |SHAP Value|",
                title_font=dict(size=16, color="#e2e8f0"),
                height=450,
                margin=dict(t=50, b=30, l=10, r=70),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis_title="Mean |SHAP Value|",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Importance table
            st.markdown("#### 📊 Feature Importance Ranking")
            display_df = imp_df[["rank", "feature", "mean_abs_shap", "contribution_pct"]].copy()
            display_df.columns = ["Rank", "Feature", "Mean |SHAP|", "Contribution %"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="disclaimer">
            <strong>Understanding Global SHAP Feature Importance:</strong>
            <ul style="margin: 4px 0;">
                <li>The interactive bar chart above displays the average absolute SHAP values for each feature.</li>
                <li><strong>Mean |SHAP Value|</strong>: Measures the overall impact of a feature on the model's predictions. A higher value indicates that the feature is more influential in predicting equipment failure.</li>
                <li><strong>Contribution %</strong>: The relative importance of each feature normalized as a percentage of total model impact.</li>
                <li>SHAP values are mathematically robust, derived from cooperative game theory, ensuring fair credit assignment to each feature.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


    # ========================================================================
    # TAB 2 — Local Explainability
    # ========================================================================

    with tabs[1]:
        st.markdown("### Individual Prediction Explanation")
        st.markdown(
            "Local SHAP analysis answers: **'Why is THIS specific machine at risk?'** "
            "Select a sample from the dataset or enter custom parameters."
        )

        # Load dataset for sample selection
        try:
            df = load_dataset_fn()

            # Prepare dataset for display
            from src.preprocessing.pipeline import (
                drop_leakage_columns, drop_id_columns, rename_columns,
                encode_type_column
            )
            from src.features.engineer import engineer_features
            from src.preprocessing.pipeline import apply_scaler

            feature_stats = artifacts["feature_stats"]
            scaler = artifacts["scaler"]
            feature_names = artifacts["feature_names"]
            numerical_cols = artifacts["numerical_cols"]

            df_proc = drop_leakage_columns(df.copy(), config)
            df_proc = drop_id_columns(df_proc, config)
            df_proc = rename_columns(df_proc, config)
            df_proc = encode_type_column(df_proc, config)

            target = df_proc.pop("machine_failure")
            df_proc, _ = engineer_features(df_proc, config, fit_stats=feature_stats)
            df_scaled = apply_scaler(df_proc, scaler, config, feature_cols=numerical_cols)

            # Sample selector
            sample_options = {
                "Random Normal (No Failure)": target[target == 0].sample(1, random_state=42).index[0],
                "Random Failure": target[target == 1].sample(1, random_state=42).index[0],
            }

            # Add a few specific indices
            failure_indices = target[target == 1].head(5).index.tolist()
            for i, idx in enumerate(failure_indices):
                sample_options[f"Failure Sample #{i+1} (idx={idx})"] = idx

            selected_sample = st.selectbox(
                "Select a sample to explain:",
                list(sample_options.keys()),
            )

            idx = sample_options[selected_sample]
            X_single = df_scaled.loc[[idx]]

            # Get prediction
            model = artifacts.get("best_model_calibrated", artifacts.get("best_model"))
            prob = float(model.predict_proba(X_single)[:, 1][0])
            pred = "FAILURE" if prob >= 0.5 else "NO FAILURE"

            # SHAP explanation
            from src.explainability.shap_engine import SHAPEngine

            best_model_raw = artifacts.get("best_model")
            bg = df_scaled.sample(n=min(100, len(df_scaled)), random_state=42)

            shap_engine = SHAPEngine(
                model=best_model_raw,
                X_background=bg,
                config=config,
                model_type="tree",
                feature_names=feature_names,
            )

            explanation = shap_engine.explain_single_prediction(X_single, top_n=10)

            # Display
            from src.risk.scoring import compute_risk_score, get_risk_category
            risk_score = compute_risk_score(prob, config)
            risk_cat = get_risk_category(risk_score, config)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Prediction", pred)
            with c2:
                st.metric("Failure Probability", f"{prob*100:.1f}%")
            with c3:
                st.metric("Risk Score", f"{risk_score:.0f}/100")

            st.markdown(f"**Risk Level:** {render_risk_badge_inline(risk_cat)}")

            # SHAP waterfall
            if explanation.get("top_factors"):
                st.markdown("#### Feature Contributions")

                factors = explanation["top_factors"][:10]
                feat_names = [f["feature"] for f in factors]
                shap_vals = [f["shap_value"] for f in factors]
                colors = ["#ef4444" if v > 0 else "#22c55e" for v in shap_vals]

                fig = go.Figure(go.Bar(
                    y=feat_names,
                    x=shap_vals,
                    orientation="h",
                    marker_color=colors,
                    text=[f"{v:+.4f}" for v in shap_vals],
                    textposition="outside",
                    textfont=dict(size=11, color="#94a3b8"),
                ))
                fig.update_layout(
                    title="SHAP Waterfall — Feature Contributions to This Prediction",
                    title_font=dict(size=14, color="#e2e8f0"),
                    height=380,
                    margin=dict(t=50, b=30, l=10, r=70),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#94a3b8"),
                    xaxis_title="SHAP Value",
                    yaxis=dict(autorange="reversed"),
                )
                st.plotly_chart(fig, use_container_width=True)

                # Text explanation
                st.markdown("#### 📝 Plain-English Explanation")
                for f in factors[:5]:
                    arrow = "🔴" if f["impact"] == "increases risk" else "🟢"
                    feat_mapped = config.get("industry_mapping", {}).get(
                        f["feature"], f["feature"]
                    )
                    st.markdown(
                        f"- {arrow} **{f['feature']}** ({feat_mapped}) = "
                        f"`{f['value']:.3f}` → **{f['impact']}**"
                    )

        except Exception as e:
            st.error(f"Local explanation failed: {e}")
            st.info("This may occur if the model or dataset is not properly loaded.")

    # ========================================================================
    # TAB 3 — Industry Mapping
    # ========================================================================

    with tabs[2]:
        st.markdown("### 🏭 Ceiling Fan Manufacturing — Feature Mapping")

        st.warning(
            "⚠️ **CONCEPTUAL INDUSTRY MAPPING**: The AI4I 2020 dataset is synthetic. "
            "This table shows how each feature *could* map to real ceiling fan "
            "production parameters. This is NOT validated factory data."
        )

        mapping = config.get("industry_mapping", {})
        mapping_df = pd.DataFrame([
            {"Feature": k, "Fan Manufacturing Interpretation": v}
            for k, v in mapping.items()
        ])

        if not mapping_df.empty:
            st.dataframe(mapping_df, use_container_width=True, hide_index=True)

        st.markdown("""
        ### 📋 Interpretation Guide

        | AI4I Concept | Ceiling Fan Mapping | Why It Matters |
        |---|---|---|
        | Air Temperature | Ambient factory floor temp | Affects motor cooling during QC test |
        | Process Temperature | Motor winding temp | Overheating → insulation breakdown |
        | Rotational Speed | Fan motor test RPM | Too low → motor defect, Too high → imbalance |
        | Torque | Motor shaft load | Excessive load → bearing/motor failure |
        | Tool Wear | Stamping tool condition | Worn tools → blade defects, misalignment |
        | Machine Failure | Production line failure | Any equipment failure halting production |

        ### 🗓️ Transfer Roadmap

        | Phase | Description | Data Source |
        |---|---|---|
        | **Phase 1** (Current) | AI4I prototype with conceptual mapping | AI4I 2020 synthetic |
        | **Phase 2** | Real company sensor data integration | Factory IoT sensors |
        | **Phase 3** | Real-time IoT streaming pipeline | MQTT / Kafka |
        | **Phase 4** | Production deployment with edge computing | Cloud + Edge |
        """)


def render_risk_badge_inline(risk_cat: dict) -> str:
    """Render risk badge as inline text for st.markdown."""
    return f"{risk_cat['emoji']} **{risk_cat['label']}**"

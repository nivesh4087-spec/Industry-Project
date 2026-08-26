"""
Machine Risk Predictor Module
=============================
Interactive prediction page where users enter machine parameters
and receive risk assessment with SHAP explanations and recommendations.

Features:
- Manual parameter input
- Demo scenario buttons (Normal / Moderate / Critical)
- Risk gauge visualization
- SHAP waterfall explanation
- Actionable recommendations
- Prediction history tracking
"""

import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

from app.components.styles import (
    render_header_banner, render_kpi_card, render_risk_badge,
)


def render_page(project_root, load_artifacts_fn, load_dataset_fn):
    """Render the Machine Risk Predictor page."""

    st.markdown(render_header_banner(
        "Machine Risk Predictor",
        "Enter machine parameters to predict failure risk with AI-powered explanations"
    ), unsafe_allow_html=True)

    # Load artifacts
    try:
        artifacts, config = load_artifacts_fn()
    except Exception as e:
        st.error(f"Model not loaded: {e}. Run `python scripts/train_pipeline.py` first.")
        return

    model = artifacts.get("best_model_calibrated", artifacts.get("best_model"))
    scaler = artifacts["scaler"]
    feature_stats = artifacts["feature_stats"]
    feature_names = artifacts["feature_names"]
    numerical_cols = artifacts["numerical_cols"]
    best_name = artifacts.get("best_model_name", "Model")

    # ========================================================================
    # DEMO SCENARIOS
    # ========================================================================

    st.markdown("### 🎮 Quick Demo Scenarios")
    st.caption("Click a scenario to auto-fill parameters for demonstration.")

    demo_cols = st.columns(3)
    demo_scenarios = config["demo_scenarios"]

    selected_scenario = None
    for i, (key, scenario) in enumerate(demo_scenarios.items()):
        with demo_cols[i]:
            emoji = "🟢" if key == "normal" else ("🟡" if key == "moderate_risk" else "🔴")
            if st.button(
                f"{emoji} {scenario['name']}",
                key=f"demo_{key}",
                use_container_width=True,
                help=scenario["description"],
            ):
                selected_scenario = scenario["values"]

    st.markdown("---")

    # ========================================================================
    # INPUT FORM
    # ========================================================================

    st.markdown("### ⚙️ Machine Parameters")

    # Use demo scenario values if selected, otherwise defaults
    defaults = selected_scenario or demo_scenarios["normal"]["values"]

    col1, col2, col3 = st.columns(3)

    with col1:
        air_temp = st.number_input(
            "🌡️ Air Temperature [K]",
            min_value=290.0, max_value=310.0,
            value=float(defaults["air_temp_k"]),
            step=0.5,
            help="Ambient air temperature in Kelvin (290-310K typical)"
        )

        process_temp = st.number_input(
            "🔥 Process Temperature [K]",
            min_value=300.0, max_value=320.0,
            value=float(defaults["process_temp_k"]),
            step=0.5,
            help="Process/machine temperature in Kelvin (300-320K typical)"
        )

    with col2:
        rpm = st.number_input(
            "🔄 Rotational Speed [RPM]",
            min_value=1000, max_value=3000,
            value=int(defaults["rotational_speed_rpm"]),
            step=10,
            help="Rotational speed in revolutions per minute (1000-3000 typical)"
        )

        torque = st.number_input(
            "⚡ Torque [Nm]",
            min_value=3.0, max_value=80.0,
            value=float(defaults["torque_nm"]),
            step=0.5,
            help="Torque in Newton-meters (3-80 Nm typical)"
        )

    with col3:
        tool_wear = st.number_input(
            "🔧 Tool Wear [min]",
            min_value=0, max_value=260,
            value=int(defaults["tool_wear_min"]),
            step=1,
            help="Accumulated tool wear in minutes (0-260 typical)"
        )

        type_map = {"Low (L)": 0, "Medium (M)": 1, "High (H)": 2}
        type_labels = list(type_map.keys())
        default_type_idx = min(int(defaults.get("type", 1)), 2)
        machine_type = st.selectbox(
            "📦 Product Type",
            type_labels,
            index=default_type_idx,
            help="Product quality tier: L (Economy), M (Standard), H (Premium)"
        )

    st.markdown("---")

    # ========================================================================
    # PREDICT BUTTON
    # ========================================================================

    predict_btn = st.button(
        "🔮 Predict Failure Risk",
        use_container_width=True,
        type="primary",
    )

    if predict_btn or selected_scenario:
        # Prepare input
        input_data = {
            "air_temp_k": air_temp,
            "process_temp_k": process_temp,
            "rotational_speed_rpm": rpm,
            "torque_nm": torque,
            "tool_wear_min": tool_wear,
            "type": type_map[machine_type],
        }

        # Preprocess
        from src.preprocessing.pipeline import preprocess_single_input
        try:
            X_input = preprocess_single_input(
                input_data, config, scaler, feature_stats,
                feature_names, numerical_cols
            )
        except Exception as e:
            st.error(f"Preprocessing failed: {e}")
            return

        # Predict
        try:
            failure_prob = float(model.predict_proba(X_input)[:, 1][0])
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            return

        # Risk assessment
        from src.risk.scoring import (
            compute_risk_score, get_risk_category, generate_risk_assessment,
            generate_early_warning,
        )

        risk_score = compute_risk_score(failure_prob, config)
        risk_cat = get_risk_category(risk_score, config)

        # SHAP explanation
        from src.explainability.shap_engine import SHAPEngine
        try:
            # Get the uncalibrated best model for SHAP
            best_model_raw = artifacts.get("best_model", model)
            model_type = "tree"  # Most best models will be tree-based

            # For SHAP, use a small background set from training
            df_raw = load_dataset_fn()
            from src.preprocessing.pipeline import (
                drop_leakage_columns, drop_id_columns, rename_columns,
                encode_type_column
            )
            from src.features.engineer import engineer_features

            df_bg = drop_leakage_columns(df_raw.copy(), config)
            df_bg = drop_id_columns(df_bg, config)
            df_bg = rename_columns(df_bg, config)
            df_bg = encode_type_column(df_bg, config)
            target = df_bg.pop("machine_failure")
            df_bg, _ = engineer_features(df_bg, config, fit_stats=feature_stats)
            from src.preprocessing.pipeline import apply_scaler
            df_bg = apply_scaler(df_bg, scaler, config, feature_cols=numerical_cols)

            # Sample background
            bg_sample = df_bg.sample(n=min(100, len(df_bg)), random_state=42)

            shap_engine = SHAPEngine(
                model=best_model_raw,
                X_background=bg_sample,
                config=config,
                model_type=model_type,
                feature_names=feature_names,
            )

            shap_explanation = shap_engine.explain_single_prediction(X_input, top_n=10)
        except Exception as e:
            # Fallback — no SHAP available
            shap_explanation = {
                "top_factors": [],
                "shap_values": [],
                "contributions": [],
                "error": str(e),
            }

        # Risk assessment with SHAP
        risk_assessment = generate_risk_assessment(failure_prob, shap_explanation, config)

        # Recommendations
        from src.recommendations.engine import (
            generate_recommendations, get_recommendation_summary,
        )
        recommendations = generate_recommendations(shap_explanation, config, top_n=5)
        rec_summary = get_recommendation_summary(recommendations)

        # Early warning
        early_warning = generate_early_warning(risk_assessment, config)

        # Store in history
        st.session_state.prediction_history.add_prediction(
            input_data, risk_assessment, rec_summary
        )

        # ====================================================================
        # DISPLAY RESULTS
        # ====================================================================

        # Early warning banner
        if early_warning:
            st.markdown(f"""
            <div class="alert-banner">
                <div class="alert-title">⚠️ {early_warning['type']} — {early_warning['severity']}</div>
                <div class="alert-text">{early_warning['message']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Main results row
        r1, r2, r3, r4 = st.columns(4)

        with r1:
            prediction_label = "⚠️ FAILURE" if failure_prob >= 0.5 else "✅ NO FAILURE"
            pred_color = "red" if failure_prob >= 0.5 else "green"
            st.markdown(render_kpi_card(
                "Prediction", prediction_label,
                f"Model: {best_name}", pred_color
            ), unsafe_allow_html=True)

        with r2:
            prob_color = "red" if failure_prob > 0.6 else ("purple" if failure_prob > 0.3 else "green")
            st.markdown(render_kpi_card(
                "Failure Probability",
                f"{failure_prob * 100:.1f}%",
                "Calibrated model estimate", prob_color
            ), unsafe_allow_html=True)

        with r3:
            rs_color = "red" if risk_score > 80 else ("purple" if risk_score > 60 else ("cyan" if risk_score > 30 else "green"))
            st.markdown(render_kpi_card(
                "Risk Score",
                f"{risk_score:.0f}/100",
                render_risk_badge(risk_cat["label"]),
                rs_color
            ), unsafe_allow_html=True)

        with r4:
            st.markdown(render_kpi_card(
                "Risk Level",
                f"{risk_cat['emoji']} {risk_cat['label']}",
                risk_assessment["assessment_summary"][:60] + "...",
                rs_color
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ====================================================================
        # RISK GAUGE + SHAP EXPLANATION
        # ====================================================================

        gcol, scol = st.columns([2, 3])

        with gcol:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Risk Gauge")

            # Plotly gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=risk_score,
                title={'text': "Risk Score", 'font': {'size': 16, 'color': '#94a3b8'}},
                number={'font': {'size': 42, 'color': risk_cat['color']}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#2a3a4e'},
                    'bar': {'color': risk_cat['color']},
                    'bgcolor': '#1a2332',
                    'borderwidth': 2,
                    'bordercolor': '#2a3a4e',
                    'steps': [
                        {'range': [0, 30], 'color': 'rgba(34, 197, 94, 0.15)'},
                        {'range': [30, 60], 'color': 'rgba(234, 179, 8, 0.15)'},
                        {'range': [60, 80], 'color': 'rgba(249, 115, 22, 0.15)'},
                        {'range': [80, 100], 'color': 'rgba(239, 68, 68, 0.15)'},
                    ],
                    'threshold': {
                        'line': {'color': '#ef4444', 'width': 3},
                        'thickness': 0.8,
                        'value': config["early_warning"]["threshold"],
                    },
                },
            ))
            fig.update_layout(
                height=280,
                margin=dict(t=40, b=20, l=30, r=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"**Assessment:** {risk_assessment['assessment_summary']}")
            st.markdown('</div>', unsafe_allow_html=True)

        with scol:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 🔍 Why This Prediction? (SHAP Explanation)")

            if shap_explanation.get("top_factors"):
                # Feature contribution bar chart
                factors = shap_explanation["top_factors"][:8]
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
                    height=300,
                    margin=dict(t=10, b=10, l=10, r=60),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#94a3b8"),
                    xaxis_title="SHAP Value (impact on failure prediction)",
                    yaxis=dict(autorange="reversed"),
                )
                st.plotly_chart(fig, use_container_width=True)

                # Text breakdown
                st.markdown("**Top Contributing Factors:**")
                for f in factors[:5]:
                    arrow = "🔴 ↑" if f["impact"] == "increases risk" else "🟢 ↓"
                    st.markdown(
                        f"- {arrow} **{f['feature']}** = {f['value']:.2f} → "
                        f"{f['impact']} (SHAP: {f['shap_value']:+.4f})"
                    )
            else:
                st.info("SHAP explanation unavailable for this prediction.")

            st.markdown('</div>', unsafe_allow_html=True)

        # ====================================================================
        # RECOMMENDATIONS
        # ====================================================================

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 Recommended Actions")

        if recommendations:
            for rec in recommendations[:4]:
                priority_class = f"rec-{rec['priority']}"
                st.markdown(f"""
                <div class="rec-card {priority_class}">
                    <strong>{rec['icon']} {rec['title']}</strong>
                    <span class="risk-badge risk-{rec['priority']}" style="float: right; font-size: 0.65rem;">
                        {rec['priority'].upper()}
                    </span>
                    <br>
                    <span style="font-size: 0.85rem; color: #94a3b8;">
                        Triggered by: <code>{rec['feature']}</code> → {rec['impact']}
                    </span>
                    <ul style="margin-top: 6px; font-size: 0.85rem;">
                        {''.join(f'<li>{a}</li>' for a in rec['recommendations'][:2])}
                    </ul>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">
                        📋 {rec['fan_manufacturing_note']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No significant risk factors detected. "
                       "Machine operating within normal parameters.")

        st.markdown("""
        <div class="disclaimer">
            ⚠️ These are <strong>AI-powered maintenance recommendations</strong>.
            Always verify with qualified maintenance personnel
            before taking action on critical equipment.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

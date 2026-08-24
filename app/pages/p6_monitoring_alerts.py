"""
Page 6 — Monitoring & Alerts
==============================
Prediction history, alert feed, and risk distribution monitoring.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from app.components.styles import render_header_banner, render_kpi_card


def render_page(project_root):
    """Render the Monitoring & Alerts page."""

    st.markdown(render_header_banner(
        "Monitoring & Alerts",
        "Prediction history, risk distribution, and alert monitoring"
    ), unsafe_allow_html=True)

    # Get prediction history from session state
    history = st.session_state.get("prediction_history", None)

    if history is None:
        from src.risk.scoring import PredictionHistory
        st.session_state.prediction_history = PredictionHistory()
        history = st.session_state.prediction_history

    history_df = history.get_history_df()
    alert_count = history.get_alert_count()
    risk_dist = history.get_risk_distribution()

    # ========================================================================
    # KPI ROW
    # ========================================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(render_kpi_card(
            "Total Predictions", str(len(history_df)),
            "In current session", "blue"
        ), unsafe_allow_html=True)

    with c2:
        st.markdown(render_kpi_card(
            "High-Risk Alerts", str(alert_count),
            "HIGH + CRITICAL risk", "red"
        ), unsafe_allow_html=True)

    with c3:
        avg_risk = history_df["risk_score"].mean() if not history_df.empty else 0
        st.markdown(render_kpi_card(
            "Avg Risk Score", f"{avg_risk:.1f}",
            "Across all predictions", "cyan"
        ), unsafe_allow_html=True)

    with c4:
        critical_count = risk_dist.get("CRITICAL RISK", 0)
        st.markdown(render_kpi_card(
            "Critical Alerts", str(critical_count),
            "Immediate attention needed", "purple"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================================
    # RISK DISTRIBUTION
    # ========================================================================

    col_chart, col_feed = st.columns([2, 3])

    with col_chart:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Risk Distribution")

        if sum(risk_dist.values()) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=list(risk_dist.keys()),
                values=list(risk_dist.values()),
                hole=0.5,
                marker_colors=["#22c55e", "#eab308", "#f97316", "#ef4444"],
                textinfo="label+value",
                textfont_size=11,
            )])
            fig.update_layout(
                height=300,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No predictions made yet. Use the Risk Predictor page to generate predictions.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_feed:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🔔 Alert Feed")

        if not history_df.empty:
            # Filter high-risk events
            alerts = history_df[
                history_df["risk_category"].isin(["HIGH RISK", "CRITICAL RISK"])
            ].sort_values("id", ascending=False).head(10)

            if not alerts.empty:
                for _, row in alerts.iterrows():
                    emoji = "🔴" if row["risk_category"] == "CRITICAL RISK" else "🟠"
                    st.markdown(f"""
                    <div class="alert-banner" style="padding: 10px 14px; margin: 6px 0;">
                        <div style="font-size: 0.8rem; color: var(--accent-red); font-weight: 700;">
                            {emoji} {row['risk_category']} — Risk: {row['risk_score']:.0f}/100
                        </div>
                        <div style="font-size: 0.75rem; color: var(--text-muted);">
                            {row['timestamp']} | Prob: {row['failure_probability']:.1f}% |
                            Factor: {row['top_factor']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No high-risk alerts. All predictions within normal range.")
        else:
            st.info("No alerts yet. Make predictions in the Risk Predictor page.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # PREDICTION HISTORY TABLE
    # ========================================================================

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Prediction History Log")

    if not history_df.empty:
        display_df = history_df[[
            "id", "timestamp", "risk_score", "failure_probability",
            "risk_category", "prediction", "top_factor", "recommendation"
        ]].copy()

        display_df.columns = [
            "ID", "Timestamp", "Risk Score", "Failure Prob (%)",
            "Risk Level", "Prediction", "Top Factor", "Recommendation"
        ]

        # Sort by most recent
        display_df = display_df.sort_values("ID", ascending=False)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400,
        )

        # Risk score timeline
        st.markdown("### 📈 Risk Score Timeline")
        if len(history_df) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(history_df) + 1)),
                y=history_df["risk_score"].tolist(),
                mode="lines+markers",
                line=dict(color="#3b82f6", width=2),
                marker=dict(
                    size=8,
                    color=[
                        "#22c55e" if s <= 30 else
                        "#eab308" if s <= 60 else
                        "#f97316" if s <= 80 else
                        "#ef4444"
                        for s in history_df["risk_score"]
                    ],
                ),
                fill="tozeroy",
                fillcolor="rgba(59, 130, 246, 0.1)",
            ))

            # Add threshold line
            fig.add_hline(
                y=60, line_dash="dash", line_color="#ef4444",
                annotation_text="Warning Threshold",
                annotation_font_color="#ef4444",
            )

            fig.update_layout(
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis_title="Prediction #",
                yaxis_title="Risk Score",
                yaxis=dict(range=[0, 105]),
                margin=dict(t=20, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "No predictions in history. Go to the **Risk Predictor** page "
            "and make some predictions to see them here."
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # EXPORT
    # ========================================================================

    if not history_df.empty:
        csv = history_df.to_csv(index=False)
        st.download_button(
            "📥 Export Prediction History (CSV)",
            csv,
            "prediction_history.csv",
            "text/csv",
            use_container_width=True,
        )

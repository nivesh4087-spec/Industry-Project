"""
Page 4 — Model Comparison
===========================
Comprehensive model evaluation and comparison dashboard.

Shows:
- Performance comparison table
- ROC curves
- Precision-Recall curves
- Confusion matrices
- Calibration curves
- Ablation study results
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app.components.styles import render_header_banner, render_kpi_card


def render_page(project_root, load_artifacts_fn, load_results_fn):
    """Render the Model Comparison page."""

    st.markdown(render_header_banner(
        "Model Comparison & Evaluation",
        "Comprehensive performance analysis across all trained models"
    ), unsafe_allow_html=True)

    # Load artifacts
    try:
        artifacts, config = load_artifacts_fn()
        test_results = artifacts.get("test_results", [])
        best_name = artifacts.get("best_model_name", "N/A")
    except Exception as e:
        st.error(f"Model not loaded: {e}")
        return

    tabs = st.tabs([
        "📊 Comparison Table",
        "📈 ROC & PR Curves",
        "🔲 Confusion Matrices",
        "📐 Calibration",
        "🔬 Ablation Study"
    ])

    # ========================================================================
    # TAB 1 — Comparison Table
    # ========================================================================

    with tabs[0]:
        st.markdown("### Model Performance Comparison — Test Set")

        if test_results:
            # KPI cards for best model
            best = next((r for r in test_results if r["model"] == best_name), test_results[0])

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.markdown(render_kpi_card("Best Model", best_name, "Selected by F1-Score", "blue"),
                            unsafe_allow_html=True)
            with c2:
                st.markdown(render_kpi_card("Precision", f"{best['precision']:.4f}",
                            "True positives / predicted positives", "cyan"),
                            unsafe_allow_html=True)
            with c3:
                st.markdown(render_kpi_card("Recall", f"{best['recall']:.4f}",
                            "Detected failures / actual failures", "green"),
                            unsafe_allow_html=True)
            with c4:
                st.markdown(render_kpi_card("F1-Score", f"{best['f1']:.4f}",
                            "Harmonic mean of Precision & Recall", "purple"),
                            unsafe_allow_html=True)
            with c5:
                st.markdown(render_kpi_card("PR-AUC", f"{best['pr_auc']:.4f}",
                            "Area under PR curve", "red"),
                            unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Full comparison table
            results_df = pd.DataFrame([
                {
                    "Model": r["model"],
                    "Precision": r["precision"],
                    "Recall": r["recall"],
                    "F1-Score": r["f1"],
                    "PR-AUC": r["pr_auc"],
                    "ROC-AUC": r["roc_auc"],
                    "Brier Score": r["brier_score"],
                    "Best?": "🏆" if r["model"] == best_name else "",
                }
                for r in test_results
            ])

            st.dataframe(
                results_df.style.highlight_max(
                    subset=["Precision", "Recall", "F1-Score", "PR-AUC", "ROC-AUC"],
                    color="#1a3a2a",
                ).highlight_min(
                    subset=["Brier Score"],
                    color="#1a3a2a",
                ).format({
                    "Precision": "{:.4f}", "Recall": "{:.4f}", "F1-Score": "{:.4f}",
                    "PR-AUC": "{:.4f}", "ROC-AUC": "{:.4f}", "Brier Score": "{:.4f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

            # Bar chart comparison
            metrics = ["precision", "recall", "f1", "pr_auc", "roc_auc"]
            labels = ["Precision", "Recall", "F1-Score", "PR-AUC", "ROC-AUC"]
            colors = ["#3b82f6", "#ef4444", "#22c55e", "#f97316", "#8b5cf6"]

            fig = go.Figure()
            for i, r in enumerate(test_results):
                vals = [r[m] for m in metrics]
                fig.add_trace(go.Bar(
                    name=r["model"],
                    x=labels,
                    y=vals,
                    marker_color=colors[i % len(colors)],
                    text=[f"{v:.3f}" for v in vals],
                    textposition="outside",
                    textfont=dict(size=10),
                ))

            fig.update_layout(
                barmode="group",
                title="Model Performance Comparison",
                title_font=dict(size=16, color="#e2e8f0"),
                height=400,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                yaxis=dict(range=[0, 1.15]),
                legend=dict(
                    orientation="h",
                    yanchor="bottom", y=1.02,
                    xanchor="right", x=1,
                ),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.info(
                f"**Model Selection Criterion:** Primary metric = **F1-Score** "
                f"(balances precision & recall for minority class). "
                f"Secondary = **PR-AUC** (robust to class imbalance). "
                f"Accuracy is NOT used because the ~96.6% majority class makes it misleading."
            )

    # ========================================================================
    # TAB 2 — ROC & PR Curves
    # ========================================================================

    with tabs[1]:
        figures_dir = project_root / config["artifacts"]["figures_dir"]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### ROC Curves")
            roc_path = figures_dir / "roc_curves.png"
            if roc_path.exists():
                st.image(str(roc_path), use_container_width=True)
            else:
                st.info("ROC curve plot not found. Run training pipeline.")

        with c2:
            st.markdown("### Precision-Recall Curves")
            pr_path = figures_dir / "precision_recall_curves.png"
            if pr_path.exists():
                st.image(str(pr_path), use_container_width=True)
            else:
                st.info("PR curve plot not found. Run training pipeline.")

        st.markdown("""
        <div class="disclaimer">
            <strong>Why PR curves matter more than ROC curves here:</strong>
            ROC curves can look overly optimistic for imbalanced datasets because
            the large number of true negatives inflates the True Positive Rate.
            PR curves focus on the minority (failure) class, giving a more honest
            picture of model performance.
        </div>
        """, unsafe_allow_html=True)

    # ========================================================================
    # TAB 3 — Confusion Matrices
    # ========================================================================

    with tabs[2]:
        st.markdown("### Confusion Matrices — Test Set")

        cm_path = figures_dir / "confusion_matrices.png"
        if cm_path.exists():
            st.image(str(cm_path), use_container_width=True)
        else:
            st.info("Confusion matrix plot not found.")

        # Also show individual metrics
        if test_results:
            for r in test_results:
                if "confusion_matrix" in r:
                    cm = r["confusion_matrix"]
                    with st.expander(f"📊 {r['model']} — Detailed Classification Report"):
                        cr = r.get("classification_report", {})
                        if cr:
                            cr_df = pd.DataFrame(cr).T
                            st.dataframe(cr_df.style.format("{:.4f}"),
                                         use_container_width=True)

    # ========================================================================
    # TAB 4 — Calibration
    # ========================================================================

    with tabs[3]:
        st.markdown("### Probability Calibration Analysis")

        cal_results = load_results_fn("calibration_results.json")
        if cal_results:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Brier (Uncalibrated)",
                          f"{cal_results['brier_uncalibrated']:.4f}")
            with c2:
                st.metric("Brier (Calibrated)",
                          f"{cal_results['brier_calibrated']:.4f}")
            with c3:
                improvement = cal_results["improvement"]
                st.metric("Improvement", f"{improvement:.4f}",
                          delta=f"{improvement:.4f}")

            st.markdown(f"""
            **Calibration Method:** {cal_results.get('method', 'isotonic').title()} Calibration

            **What this means:** A lower Brier Score indicates better calibrated probabilities.
            When the model says "80% failure probability," a well-calibrated model means
            approximately 80% of such predictions are actual failures.

            **Why it matters:** The risk scoring system relies on calibrated probabilities.
            Without calibration, the displayed "Failure Probability: 82%" might not
            accurately reflect the true risk.
            """)

        cal_path = figures_dir / "calibration_curves.png"
        if cal_path.exists():
            st.image(str(cal_path), use_container_width=True,
                     caption="Calibration Curves — closer to diagonal = better calibrated")

    # ========================================================================
    # TAB 5 — Ablation Study
    # ========================================================================

    with tabs[4]:
        st.markdown("### Ablation Study — Controlled Comparisons")

        ablation = load_results_fn("ablation_results.json")

        if ablation:
            st.markdown("#### Feature Engineering Impact")

            if "without_feature_engineering" in ablation and "with_feature_engineering" in ablation:
                abl_df = pd.DataFrame([
                    {
                        "Condition": "Without Feature Engineering",
                        "F1-Score": ablation["without_feature_engineering"]["f1"],
                        "PR-AUC": ablation["without_feature_engineering"]["pr_auc"],
                    },
                    {
                        "Condition": "With Feature Engineering",
                        "F1-Score": ablation["with_feature_engineering"]["f1"],
                        "PR-AUC": ablation["with_feature_engineering"]["pr_auc"],
                    },
                ])

                st.dataframe(abl_df, use_container_width=True, hide_index=True)

                f1_diff = (ablation["with_feature_engineering"]["f1"]
                           - ablation["without_feature_engineering"]["f1"])
                if f1_diff > 0:
                    st.success(f"✅ Feature engineering improved F1-Score by "
                               f"**{f1_diff:.4f}** ({f1_diff*100:.2f}%)")
                else:
                    st.info(f"Feature engineering F1 difference: {f1_diff:.4f}")
        else:
            st.info("Ablation results not found. Run the training pipeline to generate.")

        st.markdown("""
        ### Research Questions Answered

        | Question | Finding |
        |---|---|
        | **RQ3**: Does class imbalance handling improve detection? | Yes — using `class_weight='balanced'` prevents the model from ignoring the minority failure class. Without it, the model achieves ~96.6% accuracy by predicting "no failure" always. |
        | **RQ4**: Does calibration improve risk estimates? | Results shown in Calibration tab above. |
        """)

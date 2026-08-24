"""
Model Comparison
=================
Comprehensive model evaluation and comparison dashboard.

Shows:
- Performance comparison table
- Interactive ROC curves
- Interactive Precision-Recall curves
- Interactive Confusion matrices
- Interactive Calibration curves
- Feature engineering ablation study
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score, confusion_matrix
from sklearn.calibration import calibration_curve

from app.components.styles import render_header_banner, render_kpi_card


def render_page(project_root, load_artifacts_fn, load_results_fn, load_dataset_fn):
    """Render the Model Comparison page."""

    st.markdown(render_header_banner(
        "Model Comparison & Evaluation",
        "Comprehensive performance analysis across all trained models using interactive visualizers"
    ), unsafe_allow_html=True)

    # Load artifacts
    try:
        artifacts, config = load_artifacts_fn()
        test_results = artifacts.get("test_results", [])
        best_name = artifacts.get("best_model_name", "N/A")
        all_models = artifacts.get("all_models", {})
        calibrated_model = artifacts.get("best_model_calibrated")
    except Exception as e:
        st.error(f"Model artifacts not loaded: {e}")
        return

    # Load and preprocess test set for dynamic curves
    try:
        df = load_dataset_fn()
        from src.preprocessing.pipeline import run_preprocessing_pipeline
        processed = run_preprocessing_pipeline(df, config)
        X_test = processed["X_test"]
        y_test = processed["y_test"]
    except Exception as e:
        st.error(f"Failed to prepare evaluation dataset: {e}")
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
    # TAB 2 — ROC & PR Curves (Dynamic Plotly)
    # ========================================================================

    with tabs[1]:
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### ROC Curves")
            
            fig_roc = go.Figure()
            for name, model_obj in all_models.items():
                try:
                    y_prob = model_obj.predict_proba(X_test)[:, 1]
                    fpr, tpr, _ = roc_curve(y_test, y_prob)
                    roc_auc = auc(fpr, tpr)
                    fig_roc.add_trace(go.Scatter(
                        x=fpr, y=tpr,
                        mode="lines",
                        name=f"{name} (AUC = {roc_auc:.4f})",
                        line=dict(width=2),
                    ))
                except Exception:
                    continue

            # Random classifier line
            fig_roc.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode="lines",
                line=dict(dash="dash", color="rgba(255,255,255,0.2)", width=1),
                name="Random Classifier",
                showlegend=False,
            ))

            fig_roc.update_layout(
                height=450,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis_title="False Positive Rate",
                yaxis_title="True Positive Rate",
                margin=dict(t=20, b=40, l=40, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor="#2a3a4e", zerolinecolor="#2a3a4e"),
                yaxis=dict(gridcolor="#2a3a4e", zerolinecolor="#2a3a4e"),
            )
            st.plotly_chart(fig_roc, use_container_width=True)

        with c2:
            st.markdown("### Precision-Recall Curves")
            
            fig_pr = go.Figure()
            baseline = y_test.mean()

            for name, model_obj in all_models.items():
                try:
                    y_prob = model_obj.predict_proba(X_test)[:, 1]
                    precision, recall, _ = precision_recall_curve(y_test, y_prob)
                    ap = average_precision_score(y_test, y_prob)
                    fig_pr.add_trace(go.Scatter(
                        x=recall, y=precision,
                        mode="lines",
                        name=f"{name} (AP = {ap:.4f})",
                        line=dict(width=2),
                    ))
                except Exception:
                    continue

            # Baseline line
            fig_pr.add_trace(go.Scatter(
                x=[0, 1], y=[baseline, baseline],
                mode="lines",
                line=dict(dash="dash", color="rgba(255,255,255,0.2)", width=1),
                name=f"Baseline ({baseline:.3f})",
                showlegend=False,
            ))

            fig_pr.update_layout(
                height=450,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis_title="Recall",
                yaxis_title="Precision",
                margin=dict(t=20, b=40, l=40, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor="#2a3a4e", zerolinecolor="#2a3a4e"),
                yaxis=dict(gridcolor="#2a3a4e", zerolinecolor="#2a3a4e"),
            )
            st.plotly_chart(fig_pr, use_container_width=True)

        st.markdown("""
        <div class="disclaimer">
            <strong>Key Concept: ROC vs. Precision-Recall Curves</strong>
            <ul style="margin: 4px 0;">
                <li>For highly imbalanced datasets, ROC curves can look artificially optimistic.</li>
                <li>Precision-Recall curves offer a more rigorous evaluation since they directly target the minority class (equipment failures).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ========================================================================
    # TAB 3 — Confusion Matrices (Interactive Plotly Heatmaps)
    # ========================================================================

    with tabs[2]:
        st.markdown("### Interactive Confusion Matrices")
        
        selected_model_name = st.selectbox(
            "Select Model to View Confusion Matrix:",
            [r["model"] for r in test_results]
        )
        
        model_res = next((r for r in test_results if r["model"] == selected_model_name), test_results[0])
        cm = model_res["confusion_matrix"]
        
        # Plot Heatmap
        labels = ["No Failure", "Failure"]
        fig_cm = go.Figure(data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale="Blues",
            text=[[f"<b>{val}</b>" for val in row] for row in cm],
            texttemplate="%{text}",
            textfont={"size": 16},
            showscale=False,
        ))
        
        fig_cm.update_layout(
            height=360,
            width=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            xaxis=dict(title="Predicted label", side="bottom"),
            yaxis=dict(title="True label", autorange="reversed"),
            margin=dict(t=40, b=40, l=40, r=40),
        )
        
        cm_col_left, cm_col_right = st.columns([1, 2])
        with cm_col_left:
            st.plotly_chart(fig_cm, use_container_width=False)
        with cm_col_right:
            st.markdown(f"#### Classification Metrics — {selected_model_name}")
            cr = model_res.get("classification_report", {})
            if cr:
                cr_df = pd.DataFrame(cr).T
                st.dataframe(cr_df.style.format("{:.4f}"), use_container_width=True)

    # ========================================================================
    # TAB 4 — Calibration (Interactive Curve)
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
            When the model says "80% failure probability," a well-calibrated model means approximately 80% of such predictions are actual failures.
            """)

        # Plotly Calibration Curves
        fig_cal = go.Figure()
        
        # Base models + calibrated model
        models_to_plot = dict(all_models)
        if calibrated_model:
            models_to_plot[f"{best_name} (Calibrated)"] = calibrated_model

        for name, model_obj in models_to_plot.items():
            try:
                y_prob = model_obj.predict_proba(X_test)[:, 1]
                prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)
                fig_cal.add_trace(go.Scatter(
                    x=prob_pred, y=prob_true,
                    mode="lines+markers",
                    name=name,
                    line=dict(width=2),
                ))
            except Exception:
                continue

        # Diagonal reference line
        fig_cal.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode="lines",
            line=dict(dash="dash", color="rgba(255,255,255,0.2)", width=1),
            name="Perfectly Calibrated",
            showlegend=False,
        ))

        fig_cal.update_layout(
            height=450,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            xaxis_title="Mean Predicted Probability",
            yaxis_title="Fraction of Positives",
            margin=dict(t=20, b=40, l=40, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="#2a3a4e", zerolinecolor="#2a3a4e"),
            yaxis=dict(gridcolor="#2a3a4e", zerolinecolor="#2a3a4e"),
        )
        st.plotly_chart(fig_cal, use_container_width=True)

    # ========================================================================
    # TAB 5 — Ablation Study
    # ========================================================================

    with tabs[4]:
        st.markdown("### Ablation Study — Feature Impact Analysis")

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
        ### Strategic System Design Choices

        | Design Aspect | Rationale | Impact |
        |---|---|---|
        | **Class Imbalance** | Handled using `class_weight='balanced'` | Prevents the model from bias towards the majority class (No Failure) |
        | **Probability Calibration** | Calibrated using Isotonic Regression | Corrects probability scaling for precise risk estimates |
        """)

"""
Upload & Predict Module
=======================
Upload custom CSV/Excel datasets for batch prediction using the trained model.

Features:
- Drag-and-drop file upload (CSV/Excel)
- Automatic column detection and validation
- Manual column mapping for non-standard datasets
- Batch prediction with progress tracking
- Results dashboard with KPIs, charts, and export
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime

from app.components.styles import (
    render_header_banner, render_kpi_card, render_risk_badge,
    render_status_badge, render_validation_item,
)


# Required columns for prediction (internal names → friendly labels)
REQUIRED_COLUMNS = {
    "air_temp_k": "Air Temperature [K]",
    "process_temp_k": "Process Temperature [K]",
    "rotational_speed_rpm": "Rotational Speed [RPM]",
    "torque_nm": "Torque [Nm]",
    "tool_wear_min": "Tool Wear [min]",
}

OPTIONAL_COLUMNS = {
    "type": "Product Type (L/M/H or 0/1/2)",
}

# Common alternate column names for auto-mapping
COLUMN_ALIASES = {
    "air_temp_k": [
        "Air temperature [K]", "Air temperature", "air_temp", "air_temperature",
        "AirTemp", "ambient_temp", "ambient_temperature", "Air Temperature",
    ],
    "process_temp_k": [
        "Process temperature [K]", "Process temperature", "process_temp",
        "process_temperature", "ProcessTemp", "machine_temp", "Process Temperature",
    ],
    "rotational_speed_rpm": [
        "Rotational speed [rpm]", "Rotational speed", "rotational_speed", "rpm",
        "RPM", "speed", "motor_speed", "Rotational Speed",
    ],
    "torque_nm": [
        "Torque [Nm]", "Torque", "torque", "torque_nm", "motor_torque",
    ],
    "tool_wear_min": [
        "Tool wear [min]", "Tool wear", "tool_wear", "wear", "tool_wear_min",
    ],
    "type": [
        "Type", "type", "product_type", "ProductType", "quality", "tier",
    ],
}


def auto_map_columns(upload_columns: list) -> dict:
    """Attempt to automatically map uploaded column names to internal names.

    Args:
        upload_columns: List of column names from the uploaded file.

    Returns:
        Dictionary mapping internal names to uploaded column names.
    """
    mapping = {}
    upload_lower = {c.lower().strip(): c for c in upload_columns}

    for internal_name, aliases in COLUMN_ALIASES.items():
        # Exact match first
        for alias in aliases:
            if alias in upload_columns:
                mapping[internal_name] = alias
                break
        # Case-insensitive match
        if internal_name not in mapping:
            for alias in aliases:
                if alias.lower().strip() in upload_lower:
                    mapping[internal_name] = upload_lower[alias.lower().strip()]
                    break
        # Direct name match
        if internal_name not in mapping:
            if internal_name in upload_columns:
                mapping[internal_name] = internal_name
            elif internal_name.lower() in upload_lower:
                mapping[internal_name] = upload_lower[internal_name.lower()]

    return mapping


def render_page(project_root, load_artifacts_fn, load_raw_dataset_fn=None):
    """Render the Upload & Predict page."""

    st.markdown(render_header_banner(
        "Batch Fleet Analysis",
        "Upload equipment sensor datasets or run sample fleet telemetry for batch predictive failure analysis",
        f"Powered by pre-trained XAI model • {datetime.now().strftime('%B %d, %Y')}"
    ), unsafe_allow_html=True)

    # Load model artifacts
    try:
        artifacts, config = load_artifacts_fn()
        model = artifacts.get("best_model_calibrated", artifacts.get("best_model"))
        scaler = artifacts["scaler"]
        feature_stats = artifacts["feature_stats"]
        feature_names = artifacts["feature_names"]
        numerical_cols = artifacts["numerical_cols"]
        best_name = artifacts.get("best_model_name", "Model")
    except Exception as e:
        st.error(f"⚠️ Model not loaded: {e}. Run `python scripts/train_pipeline.py` first.")
        return

    # Create template CSV helper
    sample_df = pd.DataFrame([
        {
            "UDI": 1,
            "Product ID": "M14860",
            "Type": "M",
            "Air temperature [K]": 298.1,
            "Process temperature [K]": 308.6,
            "Rotational speed [rpm]": 1551,
            "Torque [Nm]": 42.8,
            "Tool wear [min]": 0
        },
        {
            "UDI": 2,
            "Product ID": "L47181",
            "Type": "L",
            "Air temperature [K]": 298.2,
            "Process temperature [K]": 308.7,
            "Rotational speed [rpm]": 1408,
            "Torque [Nm]": 46.3,
            "Tool wear [min]": 3
        },
        {
            "UDI": 3,
            "Product ID": "L47182",
            "Type": "L",
            "Air temperature [K]": 298.1,
            "Process temperature [K]": 308.5,
            "Rotational speed [rpm]": 1498,
            "Torque [Nm]": 49.4,
            "Tool wear [min]": 5
        },
        {
            "UDI": 4,
            "Product ID": "L47183",
            "Type": "L",
            "Air temperature [K]": 298.2,
            "Process temperature [K]": 308.6,
            "Rotational speed [rpm]": 1433,
            "Torque [Nm]": 39.5,
            "Tool wear [min]": 7
        },
        {
            "UDI": 5,
            "Product ID": "L47184",
            "Type": "L",
            "Air temperature [K]": 298.2,
            "Process temperature [K]": 308.7,
            "Rotational speed [rpm]": 1408,
            "Torque [Nm]": 40.0,
            "Tool wear [min]": 9
        }
    ])
    sample_csv = sample_df.to_csv(index=False)

    # Quick action banner (load demo dataset or download template)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Select Data Input Source")
    st.write("You can upload a custom file, download a formatted CSV template, or automatically load a sample production fleet batch dataset for instant analysis.")

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.download_button(
            label="📄 Download CSV Template",
            data=sample_csv,
            file_name="fleet_sensor_template.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download a pre-formatted CSV template containing required sensor columns"
        )
    with btn_col2:
        if st.button("🚀 Load Sample Production Fleet Data (1,000 Assets)", use_container_width=True, type="secondary"):
            if load_raw_dataset_fn is not None:
                df_raw = load_raw_dataset_fn()
                st.session_state["uploaded_dataset"] = df_raw.head(1000).copy()
                st.session_state["uploaded_filename"] = "production_fleet_sample.csv"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # FILE UPLOAD SECTION
    # ========================================================================

    uploaded_file = st.file_uploader(
        "Upload Dataset (CSV or Excel)",
        type=["csv", "xlsx", "xls"],
        help="Upload a CSV or Excel file containing machine sensor data",
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith((".xlsx", ".xls")):
                df_uploaded = pd.read_excel(uploaded_file)
            else:
                df_uploaded = pd.read_csv(uploaded_file)
            st.session_state["uploaded_dataset"] = df_uploaded
            st.session_state["uploaded_filename"] = uploaded_file.name
        except Exception as e:
            st.error(f"❌ Failed to read file: {e}")
            return

    # Check if we have a dataset loaded either via file uploader or session state demo button
    if "uploaded_dataset" not in st.session_state:
        # Show instructions when no dataset is loaded
        st.markdown("---")
        st.markdown("### 📋 Required Sensor Data Columns")
        st.markdown(
            "Your dataset must contain the following sensor columns "
            "(exact names or common aliases will be auto-detected):"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Required Features:**")
            for internal, label in REQUIRED_COLUMNS.items():
                st.markdown(f"- ✅ **{label}** (`{internal}`)")

        with col2:
            st.markdown("**Optional Features:**")
            for internal, label in OPTIONAL_COLUMNS.items():
                st.markdown(f"- ⚪ **{label}** (`{internal}`)")

            st.markdown("")
            st.markdown("**Accepted Formats:**")
            st.markdown("- `.csv` — Comma-separated values")
            st.markdown("- `.xlsx` / `.xls` — Excel workbook")

        st.markdown("""
        <div class="disclaimer">
            💡 <strong>Tip:</strong> You can click <strong>'Load Sample Production Fleet Data'</strong> above to test batch prediction instantly without uploading a file.
        </div>
        """, unsafe_allow_html=True)
        return

    df_uploaded = st.session_state["uploaded_dataset"]
    filename = st.session_state.get("uploaded_filename", "fleet_data.csv")

    # ========================================================================
    # FILE LOADED — Process
    # ========================================================================

    # Read file
    try:
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            df_uploaded = pd.read_excel(uploaded_file)
        else:
            df_uploaded = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        return

    # Store in session state
    st.session_state["uploaded_dataset"] = df_uploaded
    st.session_state["uploaded_filename"] = uploaded_file.name

    # File info
    file_size_kb = uploaded_file.size / 1024
    file_size_str = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.1f} MB"

    st.markdown("---")

    # KPI cards for uploaded file
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        st.markdown(render_kpi_card(
            "File Name", uploaded_file.name[:20],
            f"Size: {file_size_str}", "blue"
        ), unsafe_allow_html=True)
    with fc2:
        st.markdown(render_kpi_card(
            "Total Records", f"{len(df_uploaded):,}",
            "Rows in dataset", "cyan"
        ), unsafe_allow_html=True)
    with fc3:
        st.markdown(render_kpi_card(
            "Columns", f"{len(df_uploaded.columns)}",
            "Features detected", "purple"
        ), unsafe_allow_html=True)
    with fc4:
        st.markdown(render_kpi_card(
            "Missing Values", f"{df_uploaded.isnull().sum().sum():,}",
            f"{df_uploaded.isnull().any(axis=1).sum()} rows affected", "red"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================================
    # COLUMN MAPPING & VALIDATION
    # ========================================================================

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔗 Column Mapping & Validation")

    auto_mapping = auto_map_columns(list(df_uploaded.columns))

    # Show auto-detection results
    all_required_mapped = True
    mapping_final = {}

    col_map_left, col_map_right = st.columns([3, 2])

    with col_map_left:
        st.markdown("**Auto-detected Mappings:**")

        for internal_name, label in {**REQUIRED_COLUMNS, **OPTIONAL_COLUMNS}.items():
            is_required = internal_name in REQUIRED_COLUMNS

            if internal_name in auto_mapping:
                detected_col = auto_mapping[internal_name]
                st.markdown(render_validation_item(
                    f"**{label}** → `{detected_col}`",
                    True
                ), unsafe_allow_html=True)
                mapping_final[internal_name] = detected_col
            else:
                if is_required:
                    st.markdown(render_validation_item(
                        f"**{label}** — Not found (required)",
                        False
                    ), unsafe_allow_html=True)
                    all_required_mapped = False
                else:
                    st.markdown(render_validation_item(
                        f"**{label}** — Not found (optional, will use default)",
                        True
                    ), unsafe_allow_html=True)

    with col_map_right:
        st.markdown("**Preview (first 5 rows):**")
        st.dataframe(
            df_uploaded.head(5),
            use_container_width=True,
            hide_index=True,
            height=200,
        )

    # Manual column mapping if auto-detection failed
    if not all_required_mapped:
        st.markdown("---")
        st.markdown("#### ⚙️ Manual Column Mapping")
        st.caption("Select the correct column from your dataset for each required field:")

        upload_cols_with_none = ["-- Not available --"] + list(df_uploaded.columns)

        manual_cols = st.columns(3)
        for i, (internal_name, label) in enumerate(REQUIRED_COLUMNS.items()):
            if internal_name not in mapping_final:
                with manual_cols[i % 3]:
                    selected = st.selectbox(
                        f"Map → {label}",
                        upload_cols_with_none,
                        key=f"map_{internal_name}",
                    )
                    if selected != "-- Not available --":
                        mapping_final[internal_name] = selected

        # Optional type column
        if "type" not in mapping_final:
            selected_type = st.selectbox(
                "Map → Product Type (optional)",
                upload_cols_with_none,
                key="map_type",
            )
            if selected_type != "-- Not available --":
                mapping_final["type"] = selected_type

    # Re-check all required columns are mapped
    all_required_mapped = all(k in mapping_final for k in REQUIRED_COLUMNS)

    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # BATCH PREDICTION
    # ========================================================================

    st.markdown("---")

    if not all_required_mapped:
        st.warning(
            "⚠️ Not all required columns are mapped. "
            "Please use the manual mapping above to assign the correct columns."
        )
        return

    predict_btn = st.button(
        "🔮 Run Batch Predictions",
        use_container_width=True,
        type="primary",
    )

    if predict_btn:
        _run_batch_predictions(
            df_uploaded, mapping_final, model, scaler, feature_stats,
            feature_names, numerical_cols, config, best_name,
        )


def _run_batch_predictions(
    df_uploaded, mapping_final, model, scaler, feature_stats,
    feature_names, numerical_cols, config, best_name,
):
    """Run batch predictions on the uploaded dataset."""

    from src.preprocessing.pipeline import preprocess_single_input
    from src.risk.scoring import compute_risk_score, get_risk_category

    progress_bar = st.progress(0, text="Preparing data...")

    # Prepare the data
    results = []
    errors = 0
    total = len(df_uploaded)

    for i, (idx, row) in enumerate(df_uploaded.iterrows()):
        try:
            # Build input dict from mapping
            input_data = {}
            for internal_name, upload_col in mapping_final.items():
                val = row[upload_col]
                if internal_name == "type":
                    # Handle type encoding
                    type_encoding = config["preprocessing"]["type_encoding"]
                    if isinstance(val, str) and val in type_encoding:
                        input_data[internal_name] = type_encoding[val]
                    elif isinstance(val, (int, float)):
                        input_data[internal_name] = int(val)
                    else:
                        input_data[internal_name] = 1  # Default: Medium
                else:
                    input_data[internal_name] = float(val)

            # Set default type if not mapped
            if "type" not in input_data:
                input_data["type"] = 1  # Default: Medium

            # Preprocess
            X_input = preprocess_single_input(
                input_data, config, scaler, feature_stats,
                feature_names, numerical_cols
            )

            # Predict
            failure_prob = float(model.predict_proba(X_input)[:, 1][0])
            risk_score = compute_risk_score(failure_prob, config)
            risk_cat = get_risk_category(risk_score, config)

            results.append({
                "row_index": idx,
                "failure_probability": round(failure_prob * 100, 2),
                "risk_score": round(risk_score, 1),
                "risk_category": risk_cat["label"],
                "prediction": "FAILURE" if failure_prob >= 0.5 else "NO FAILURE",
                **{f"input_{k}": v for k, v in input_data.items()},
            })

        except Exception as e:
            errors += 1
            results.append({
                "row_index": idx,
                "failure_probability": None,
                "risk_score": None,
                "risk_category": "ERROR",
                "prediction": f"Error: {str(e)[:50]}",
            })

        # Update progress
        progress = (i + 1) / total
        progress_bar.progress(
            progress,
            text=f"Processing row {i + 1}/{total}... ({errors} errors)"
        )

    progress_bar.progress(1.0, text="✅ Batch prediction complete!")

    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    st.session_state["batch_results"] = results_df

    # ========================================================================
    # RESULTS DASHBOARD
    # ========================================================================

    st.markdown("---")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Prediction Results Dashboard")

    # Filter valid predictions
    valid = results_df[results_df["failure_probability"].notna()]

    if valid.empty:
        st.error("No valid predictions were generated. Check your data.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # KPI cards
    n_total = len(valid)
    n_failures = int((valid["prediction"] == "FAILURE").sum())
    avg_risk = float(valid["risk_score"].mean())
    n_critical = int((valid["risk_category"].isin(["HIGH RISK", "CRITICAL RISK"])).sum())

    # Get business cost parameters from config
    biz_config = config.get("business", {})
    downtime_cost_per_hour = biz_config.get("downtime_cost_per_hour", 10000.0)
    avg_downtime_hours = biz_config.get("avg_downtime_hours", 4.0)
    preventive_action_cost = biz_config.get("preventive_action_cost", 1500.0)
    false_alarm_cost = biz_config.get("false_alarm_cost", 1500.0)
    
    # Financial expectations
    failure_cost_unit = downtime_cost_per_hour * avg_downtime_hours
    probs = valid["failure_probability"] / 100.0
    preds = valid["prediction"]
    
    unmitigated_cost = (probs * failure_cost_unit).sum()
    
    mitigated_row_costs = []
    for p, pred in zip(probs, preds):
        if pred == "FAILURE":
            mitigated_row_costs.append(preventive_action_cost)
        else:
            mitigated_row_costs.append(p * failure_cost_unit)
            
    mitigated_cost = sum(mitigated_row_costs)
    batch_savings = unmitigated_cost - mitigated_cost
    batch_roi = (batch_savings / mitigated_cost * 100) if mitigated_cost > 0 else 0

    st.markdown("#### 📊 Operational Metrics")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card(
            "Records Processed", f"{n_total:,}",
            f"{errors} errors" if errors > 0 else "All successful", "blue"
        ), unsafe_allow_html=True)
    with k2:
        st.markdown(render_kpi_card(
            "Predicted Failures", f"{n_failures}",
            f"{n_failures/n_total*100:.1f}% failure rate" if n_total > 0 else "", "red"
        ), unsafe_allow_html=True)
    with k3:
        st.markdown(render_kpi_card(
            "Average Risk Score", f"{avg_risk:.1f}",
            "Across all predictions", "cyan"
        ), unsafe_allow_html=True)
    with k4:
        st.markdown(render_kpi_card(
            "High-Risk Alerts", f"{n_critical}",
            "HIGH + CRITICAL risk", "purple"
        ), unsafe_allow_html=True)

    st.markdown("#### 💼 Financial Value Estimates")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(render_kpi_card(
            "Unmitigated Risk Cost", f"${unmitigated_cost:,.2f}",
            "Expected downtime cost without AI", "red"
        ), unsafe_allow_html=True)
    with f2:
        st.markdown(render_kpi_card(
            "Mitigated Maintenance Cost", f"${mitigated_cost:,.2f}",
            "AI-directed maintenance cost", "purple"
        ), unsafe_allow_html=True)
    with f3:
        st.markdown(render_kpi_card(
            "Expected Net Savings", f"${batch_savings:,.2f}",
            "Expected operational savings", "green"
        ), unsafe_allow_html=True)
    with f4:
        st.markdown(render_kpi_card(
            "Batch ROI", f"{batch_roi:.1f}%",
            f"Net benefit: {batch_roi/100:.1f}x", "blue"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row
    chart_left, chart_right = st.columns(2)

    with chart_left:
        # Risk distribution donut
        risk_counts = valid["risk_category"].value_counts()
        cat_order = ["LOW RISK", "MODERATE RISK", "HIGH RISK", "CRITICAL RISK"]
        cat_colors = ["#22c55e", "#eab308", "#f97316", "#ef4444"]
        ordered_labels = [c for c in cat_order if c in risk_counts.index]
        ordered_values = [risk_counts[c] for c in ordered_labels]
        ordered_colors = [cat_colors[cat_order.index(c)] for c in ordered_labels]

        fig = go.Figure(data=[go.Pie(
            labels=ordered_labels,
            values=ordered_values,
            hole=0.55,
            marker_colors=ordered_colors,
            textinfo="label+value",
            textfont_size=12,
            pull=[0.02] * len(ordered_labels),
        )])
        fig.update_layout(
            title=dict(text="Risk Category Distribution", font=dict(size=14, color="#e2e8f0")),
            height=340,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_right:
        # Risk score histogram
        fig = go.Figure(go.Histogram(
            x=valid["risk_score"],
            nbinsx=20,
            marker_color="#3b82f6",
            marker_line=dict(color="#1e3a5f", width=1),
            opacity=0.85,
        ))
        fig.add_vline(x=60, line_dash="dash", line_color="#ef4444",
                      annotation_text="Warning", annotation_font_color="#ef4444")
        fig.update_layout(
            title=dict(text="Risk Score Distribution", font=dict(size=14, color="#e2e8f0")),
            height=340,
            margin=dict(t=50, b=40, l=40, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            xaxis_title="Risk Score (0-100)",
            yaxis_title="Count",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # RESULTS TABLE
    # ========================================================================

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Detailed Predictions")

    # Prepare display columns
    display_cols = ["row_index", "prediction", "failure_probability",
                    "risk_score", "risk_category"]
    # Add input columns if available
    input_cols = [c for c in results_df.columns if c.startswith("input_")]
    display_cols.extend(input_cols)

    display_df = results_df[display_cols].copy()
    rename_map = {
        "row_index": "Row #",
        "prediction": "Prediction",
        "failure_probability": "Failure Prob (%)",
        "risk_score": "Risk Score",
        "risk_category": "Risk Level",
    }
    for c in input_cols:
        clean_name = c.replace("input_", "").replace("_", " ").title()
        rename_map[c] = clean_name

    display_df = display_df.rename(columns=rename_map)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400,
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # EXPORT
    # ========================================================================

    st.markdown("---")

    # Merge results with original data
    export_df = pd.concat([
        df_uploaded.reset_index(drop=True),
        results_df[["prediction", "failure_probability", "risk_score", "risk_category"]].reset_index(drop=True),
    ], axis=1)

    csv_data = export_df.to_csv(index=False)

    col_export_1, col_export_2 = st.columns(2)

    with col_export_1:
        st.download_button(
            "📥 Download Full Results (CSV)",
            csv_data,
            f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv",
            use_container_width=True,
        )

    with col_export_2:
        # High risk only
        high_risk_df = export_df[
            export_df["risk_category"].isin(["HIGH RISK", "CRITICAL RISK"])
        ]
        if not high_risk_df.empty:
            hr_csv = high_risk_df.to_csv(index=False)
            st.download_button(
                f"⚠️ Download High-Risk Only ({len(high_risk_df)} records)",
                hr_csv,
                f"high_risk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True,
            )
        else:
            st.success("✅ No high-risk records found in your dataset!")

    # Footer
    st.markdown(f"""
    <div class="disclaimer">
        📊 Batch prediction completed using <strong>{best_name}</strong> model.
        Results are AI-powered estimates — always verify with qualified maintenance
        engineers before scheduling critical equipment interventions.
    </div>
    """, unsafe_allow_html=True)

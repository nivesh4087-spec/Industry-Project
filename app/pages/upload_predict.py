# -*- coding: utf-8 -*-
"""
Upload & Predict Module (Batch Fleet Analysis)
==============================================
Upload custom CSV/Excel datasets or use preloaded fleet telemetry for batch predictive failure analysis.

Features:
- Drag-and-drop file upload (CSV/Excel) & preloaded fleet sample dataset button
- CSV template download helper
- Fast vectorized column mapping & batch feature engineering
- Instant model inference & risk scoring
- Persistent results dashboard with KPIs, charts, table, and CSV export
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime

try:
    from app.components.styles import (
        render_header_banner, render_kpi_card, render_risk_badge,
        render_status_badge, render_validation_item,
    )
except ImportError:
    from app.components.styles import render_header_banner, render_kpi_card, render_risk_badge, render_status_badge
    def render_validation_item(text: str, is_valid: bool = True) -> str:
        icon = "✅" if is_valid else "⚠️"
        color = "var(--accent-green)" if is_valid else "var(--accent-yellow)"
        return f'<div style="margin: 4px 0; font-size: 0.88rem;"><span style="color:{color};">{icon}</span> {text}</div>'

# Required columns for prediction (internal names -> friendly labels)
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


def auto_map_columns(upload_columns):
    """Attempt to automatically map uploaded column names to internal names."""
    mapping = {}
    upload_lower = {str(c).lower().strip(): c for c in upload_columns}

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
    """Render the Batch Fleet Analysis / Upload & Predict page."""

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

    # CSV Template Helper Data
    sample_df = pd.DataFrame([
        {"UDI": 1, "Product ID": "M14860", "Type": "M", "Air temperature [K]": 298.1, "Process temperature [K]": 308.6, "Rotational speed [rpm]": 1551, "Torque [Nm]": 42.8, "Tool wear [min]": 0},
        {"UDI": 2, "Product ID": "L47181", "Type": "L", "Air temperature [K]": 298.2, "Process temperature [K]": 308.7, "Rotational speed [rpm]": 1408, "Torque [Nm]": 46.3, "Tool wear [min]": 3},
        {"UDI": 3, "Product ID": "L47182", "Type": "L", "Air temperature [K]": 298.1, "Process temperature [K]": 308.5, "Rotational speed [rpm]": 1498, "Torque [Nm]": 49.4, "Tool wear [min]": 5},
        {"UDI": 4, "Product ID": "L47183", "Type": "L", "Air temperature [K]": 298.2, "Process temperature [K]": 308.6, "Rotational speed [rpm]": 1433, "Torque [Nm]": 39.5, "Tool wear [min]": 7},
        {"UDI": 5, "Product ID": "L47184", "Type": "L", "Air temperature [K]": 298.2, "Process temperature [K]": 308.7, "Rotational speed [rpm]": 1408, "Torque [Nm]": 40.0, "Tool wear [min]": 9}
    ])
    sample_csv = sample_df.to_csv(index=False)

    # Input Option Section (Tabs for File Upload, Database Connection, and Sample Dataset)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Select Data Input Source")

    source_tab1, source_tab2, source_tab3 = st.tabs([
        "📂 Upload File (CSV / Excel)",
        "🗄️ Connect External Database",
        "🚀 Sample Fleet Telemetry"
    ])

    with source_tab1:
        st.write("Upload a CSV or Excel workbook from your computer:")
        st.download_button(
            label="📄 Download CSV Template",
            data=sample_csv,
            file_name="fleet_sensor_template.csv",
            mime="text/csv",
            help="Download a pre-formatted CSV template containing required sensor columns"
        )
        uploaded_file = st.file_uploader(
            "Upload File",
            type=["csv", "xlsx", "xls"],
            help="Upload a CSV or Excel file containing machine sensor data",
            key="page_file_uploader"
        )
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith((".xlsx", ".xls")):
                    df_uploaded = pd.read_excel(uploaded_file)
                else:
                    df_uploaded = pd.read_csv(uploaded_file)
                st.session_state["uploaded_dataset"] = df_uploaded
                st.session_state["uploaded_filename"] = uploaded_file.name
                if "batch_results" in st.session_state:
                    del st.session_state["batch_results"]
                st.success(f"✅ Loaded '{uploaded_file.name}' with {len(df_uploaded)} records.")
            except Exception as e:
                st.error(f"❌ Failed to read file: {e}")

    with source_tab2:
        st.markdown("##### Connect to Enterprise Relational or NoSQL Databases")
        st.write("Stream sensor telemetry live from SQL or Cloud database engines:")
        db_col1, db_col2 = st.columns([1, 2])
        with db_col1:
            db_type = st.selectbox("Database Engine", [
                "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Snowflake", "Oracle", "Microsoft SQL Server"
            ], key="page_db_type")
        with db_col2:
            conn_str = st.text_input("Connection URI", placeholder="postgresql://user:password@localhost:5432/telemetry_db", key="page_conn_str")
        query_str = st.text_input("Table / SQL Query", value="SELECT * FROM equipment_telemetry LIMIT 1000", key="page_query_str")

        if st.button("🔌 Connect & Import Database Records", type="primary", key="page_db_connect_btn"):
            if conn_str.strip():
                with st.spinner(f"Connecting to {db_type}..."):
                    try:
                        from src.data.loader import load_from_database
                        df_db = load_from_database(db_type, conn_str, query_str)
                        st.session_state["uploaded_dataset"] = df_db
                        st.session_state["uploaded_filename"] = f"{db_type}_telemetry_table"
                        if "batch_results" in st.session_state:
                            del st.session_state["batch_results"]
                        st.success(f"Successfully connected to {db_type}! Imported {len(df_db):,} records.")
                        st.rerun()
                    except Exception as err:
                        st.error(f"❌ Database connection failed: {err}")
            else:
                st.warning("⚠️ Please provide a valid database Connection URI.")

    with source_tab3:
        st.write("Instant one-click sample data loading from 1,000 production machines:")
        if st.button("🚀 Load Sample Production Fleet Data (1,000 Assets)", type="secondary", key="page_sample_btn"):
            if load_raw_dataset_fn is not None:
                df_raw = load_raw_dataset_fn()
                st.session_state["uploaded_dataset"] = df_raw.head(1000).copy()
                st.session_state["uploaded_filename"] = "production_fleet_sample.csv"
                if "batch_results" in st.session_state:
                    del st.session_state["batch_results"]
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Check if a dataset exists in session state
    if "uploaded_dataset" not in st.session_state:
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
            💡 <strong>Tip:</strong> Click <strong>'Load Sample Production Fleet Data'</strong> above to test batch prediction instantly.
        </div>
        """, unsafe_allow_html=True)
        return

    df_uploaded = st.session_state["uploaded_dataset"]
    filename = st.session_state.get("uploaded_filename", "fleet_data.csv")

    # File Summary KPIs
    st.markdown("---")
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        st.markdown(render_kpi_card(
            "Dataset Source", filename[:20],
            f"Active Batch File", "blue"
        ), unsafe_allow_html=True)
    with fc2:
        st.markdown(render_kpi_card(
            "Total Records", f"{len(df_uploaded):,}",
            "Equipment Rows", "cyan"
        ), unsafe_allow_html=True)
    with fc3:
        st.markdown(render_kpi_card(
            "Columns", f"{len(df_uploaded.columns)}",
            "Features Detected", "purple"
        ), unsafe_allow_html=True)
    with fc4:
        st.markdown(render_kpi_card(
            "Missing Values", f"{df_uploaded.isnull().sum().sum():,}",
            f"{df_uploaded.isnull().any(axis=1).sum()} rows affected", "red"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Column Mapping Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔗 Column Mapping & Schema Validation")

    auto_mapping = auto_map_columns(list(df_uploaded.columns))
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
                    f"**{label}** -> `{detected_col}`",
                    True
                ), unsafe_allow_html=True)
                mapping_final[internal_name] = detected_col
            else:
                if is_required:
                    st.markdown(render_validation_item(
                        f"**{label}** - Not found (required)",
                        False
                    ), unsafe_allow_html=True)
                    all_required_mapped = False
                else:
                    st.markdown(render_validation_item(
                        f"**{label}** - Not found (optional, default applied)",
                        True
                    ), unsafe_allow_html=True)

    with col_map_right:
        st.markdown("**Dataset Sample Preview:**")
        st.dataframe(
            df_uploaded.head(5),
            use_container_width=True,
            hide_index=True,
            height=180,
        )

    # Manual Column Mapping if needed
    if not all_required_mapped:
        st.markdown("---")
        st.markdown("#### ⚙️ Manual Column Mapping")
        st.caption("Select the corresponding column from your dataset for each required parameter:")

        upload_cols_with_none = ["-- Not available --"] + list(df_uploaded.columns)
        manual_cols = st.columns(3)
        for i, (internal_name, label) in enumerate(REQUIRED_COLUMNS.items()):
            if internal_name not in mapping_final:
                with manual_cols[i % 3]:
                    selected = st.selectbox(
                        f"Map -> {label}",
                        upload_cols_with_none,
                        key=f"map_{internal_name}",
                    )
                    if selected != "-- Not available --":
                        mapping_final[internal_name] = selected

        if "type" not in mapping_final:
            selected_type = st.selectbox(
                "Map -> Product Type (optional)",
                upload_cols_with_none,
                key="map_type",
            )
            if selected_type != "-- Not available --":
                mapping_final["type"] = selected_type

    all_required_mapped = all(k in mapping_final for k in REQUIRED_COLUMNS)
    st.markdown('</div>', unsafe_allow_html=True)

    # Run Prediction Button
    st.markdown("---")

    if not all_required_mapped:
        st.warning("⚠️ Please map all required columns before running batch predictions.")
        return

    predict_btn = st.button(
        "🔮 Run Batch Predictions & Analysis",
        use_container_width=True,
        type="primary",
    )

    if predict_btn:
        _execute_fast_batch_predictions(
            df_uploaded, mapping_final, model, scaler, feature_stats,
            feature_names, numerical_cols, config, best_name
        )

    # Display Dashboard if batch results exist in session state
    if "batch_results" in st.session_state:
        _render_batch_results_dashboard(
            df_uploaded, st.session_state["batch_results"], config, best_name
        )


def _execute_fast_batch_predictions(
    df_uploaded, mapping_final, model, scaler, feature_stats,
    feature_names, numerical_cols, config, best_name
):
    """Execute high-speed vectorized batch prediction."""

    from src.features.engineer import engineer_features
    from src.risk.scoring import compute_risk_score, get_risk_category

    with st.spinner("Processing batch data and calculating risk probabilities..."):
        try:
            # Map input features
            df_mapped = pd.DataFrame()
            type_encoding = config.get("preprocessing", {}).get("type_encoding", {"L": 0, "M": 1, "H": 2})

            for internal_name, upload_col in mapping_final.items():
                if internal_name == "type":
                    df_mapped[internal_name] = df_uploaded[upload_col].apply(
                        lambda v: type_encoding[v] if (isinstance(v, str) and v in type_encoding)
                        else (int(v) if isinstance(v, (int, float, np.number)) else 1)
                    )
                else:
                    df_mapped[internal_name] = pd.to_numeric(df_uploaded[upload_col], errors="coerce").fillna(0.0)

            if "type" not in df_mapped.columns:
                df_mapped["type"] = 1  # Default: Medium

            # Vectorized feature engineering
            X_engineered, _ = engineer_features(df_mapped, config, fit_stats=feature_stats)

            # Reorder & pad missing columns
            for col in feature_names:
                if col not in X_engineered.columns:
                    X_engineered[col] = 0.0
            X_engineered = X_engineered[feature_names]

            # Scale numerical features
            X_scaled = X_engineered.copy()
            cols_to_scale = [c for c in numerical_cols if c in X_scaled.columns]
            X_scaled[cols_to_scale] = scaler.transform(X_scaled[cols_to_scale])

            # Batch model probability inference
            probs = model.predict_proba(X_scaled)[:, 1]

            risk_scores = [compute_risk_score(float(p), config) for p in probs]
            risk_cats = [get_risk_category(s, config)["label"] for s in risk_scores]
            preds = ["FAILURE" if p >= 0.5 else "NO FAILURE" for p in probs]

            results_df = pd.DataFrame({
                "row_index": df_uploaded.index,
                "failure_probability": np.round(probs * 100, 2),
                "risk_score": np.round(risk_scores, 1),
                "risk_category": risk_cats,
                "prediction": preds,
            })

            # Store in session state for persistence
            st.session_state["batch_results"] = results_df
            st.success("✅ Batch predictions executed successfully!")

        except Exception as e:
            st.error(f"❌ Error during batch prediction: {e}")


def _render_batch_results_dashboard(df_uploaded, results_df, config, best_name):
    """Render the interactive results dashboard and download triggers."""

    st.markdown("---")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Batch Prediction Results Dashboard")

    valid = results_df[results_df["failure_probability"].notna()]
    if valid.empty:
        st.error("No valid prediction results found.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    n_total = len(valid)
    n_failures = int((valid["prediction"] == "FAILURE").sum())
    avg_risk = float(valid["risk_score"].mean())
    n_critical = int((valid["risk_category"].isin(["HIGH RISK", "CRITICAL RISK"])).sum())

    # Financial Cost Parameters
    biz_config = config.get("business", {})
    downtime_cost_per_hour = biz_config.get("downtime_cost_per_hour", 10000.0)
    avg_downtime_hours = biz_config.get("avg_downtime_hours", 4.0)
    preventive_action_cost = biz_config.get("preventive_action_cost", 1500.0)

    failure_cost_unit = downtime_cost_per_hour * avg_downtime_hours
    probs = valid["failure_probability"] / 100.0
    preds = valid["prediction"]

    unmitigated_cost = (probs * failure_cost_unit).sum()

    mitigated_row_costs = [
        preventive_action_cost if pred == "FAILURE" else (p * failure_cost_unit)
        for p, pred in zip(probs, preds)
    ]
    mitigated_cost = sum(mitigated_row_costs)
    batch_savings = unmitigated_cost - mitigated_cost
    batch_roi = (batch_savings / mitigated_cost * 100) if mitigated_cost > 0 else 0

    st.markdown("#### 📊 Operational Metrics")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card(
            "Processed Fleet Assets", f"{n_total:,}",
            "Batch predictions complete", "blue"
        ), unsafe_allow_html=True)
    with k2:
        st.markdown(render_kpi_card(
            "Predicted Failures", f"{n_failures}",
            f"{n_failures/n_total*100:.1f}% failure rate" if n_total > 0 else "", "red"
        ), unsafe_allow_html=True)
    with k3:
        st.markdown(render_kpi_card(
            "Average Fleet Risk", f"{avg_risk:.1f}",
            "Score range (0-100)", "cyan"
        ), unsafe_allow_html=True)
    with k4:
        st.markdown(render_kpi_card(
            "High-Risk Alerts", f"{n_critical}",
            "Requires immediate action", "purple"
        ), unsafe_allow_html=True)

    st.markdown("#### 💼 Financial Impact Estimates")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(render_kpi_card(
            "Unmitigated Failure Risk", f"${unmitigated_cost:,.2f}",
            "Unplanned downtime cost without AI", "red"
        ), unsafe_allow_html=True)
    with f2:
        st.markdown(render_kpi_card(
            "Mitigated Intervention Cost", f"${mitigated_cost:,.2f}",
            "Targeted AI maintenance cost", "purple"
        ), unsafe_allow_html=True)
    with f3:
        st.markdown(render_kpi_card(
            "Net Fleet Savings", f"${batch_savings:,.2f}",
            "Net operational savings", "green"
        ), unsafe_allow_html=True)
    with f4:
        st.markdown(render_kpi_card(
            "Estimated Batch ROI", f"{batch_roi:.1f}%",
            f"Net benefit multiplier: {batch_roi/100:.1f}x", "blue"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row
    chart_left, chart_right = st.columns(2)

    with chart_left:
        risk_counts = valid["risk_category"].value_counts()
        cat_order = ["LOW RISK", "MODERATE RISK", "HIGH RISK", "CRITICAL RISK"]
        cat_colors = ["#10b981", "#f59e0b", "#f97316", "#ef4444"]
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
        )])
        fig.update_layout(
            title=dict(text="Fleet Risk Category Breakdown", font=dict(size=14, color="#f1f5f9")),
            height=320,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_right:
        fig_hist = go.Figure(go.Histogram(
            x=valid["risk_score"],
            nbinsx=20,
            marker_color="#3b82f6",
            marker_line=dict(color="#1e3a5f", width=1),
            opacity=0.85,
        ))
        fig_hist.add_vline(x=60, line_dash="dash", line_color="#ef4444",
                           annotation_text="Critical Threshold", annotation_font_color="#ef4444")
        fig_hist.update_layout(
            title=dict(text="Fleet Risk Score Distribution", font=dict(size=14, color="#f1f5f9")),
            height=320,
            margin=dict(t=40, b=40, l=40, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            xaxis_title="Risk Score (0-100)",
            yaxis_title="Equipment Count",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Table & Export
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Fleet Risk Predictions Log")

    display_cols = ["row_index", "prediction", "failure_probability", "risk_score", "risk_category"]
    display_df = results_df[display_cols].copy()
    display_df = display_df.rename(columns={
        "row_index": "Asset #",
        "prediction": "AI Prediction",
        "failure_probability": "Failure Prob (%)",
        "risk_score": "Risk Score",
        "risk_category": "Risk Level",
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=380,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # CSV Export
    st.markdown("---")
    export_df = pd.concat([
        df_uploaded.reset_index(drop=True),
        results_df[["prediction", "failure_probability", "risk_score", "risk_category"]].reset_index(drop=True),
    ], axis=1)

    csv_data = export_df.to_csv(index=False)
    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.download_button(
            "📥 Download Full Fleet Prediction Results (CSV)",
            csv_data,
            f"fleet_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv",
            use_container_width=True,
        )

    with col_exp2:
        high_risk_df = export_df[export_df["risk_category"].isin(["HIGH RISK", "CRITICAL RISK"])]
        if not high_risk_df.empty:
            hr_csv = high_risk_df.to_csv(index=False)
            st.download_button(
                f"⚠️ Download High-Risk Critical Assets ({len(high_risk_df)} records)",
                hr_csv,
                f"critical_assets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True,
            )
        else:
            st.success("✅ No high-risk records found in the analyzed dataset!")

    st.markdown(f"""
    <div class="disclaimer">
        📊 Batch predictions completed using <strong>{best_name}</strong> model.
        Predictions are AI-generated telemetry evaluations — verify with qualified equipment engineers before scheduling maintenance interventions.
    </div>
    """, unsafe_allow_html=True)

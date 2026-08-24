"""
Page 5 — Data Explorer
========================
Interactive dataset exploration with filtering and visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from app.components.styles import render_header_banner


def render_page(project_root, load_dataset_fn):
    """Render the Data Explorer page."""

    st.markdown(render_header_banner(
        "Data Explorer",
        "Interactive exploration of the AI4I 2020 Predictive Maintenance Dataset"
    ), unsafe_allow_html=True)

    # Dataset source selection
    has_uploaded = "uploaded_dataset" in st.session_state
    if has_uploaded:
        source = st.radio(
            "Select Dataset",
            ["📦 Built-in (AI4I 2020)", f"📂 Uploaded ({st.session_state.get('uploaded_filename', 'file')})"],
            horizontal=True,
        )
        use_uploaded = "Uploaded" in source
    else:
        use_uploaded = False

    # Load dataset
    try:
        if use_uploaded:
            df = st.session_state["uploaded_dataset"]
            st.success(f"🔍 Exploring uploaded dataset: **{st.session_state.get('uploaded_filename', 'unknown')}** ({len(df):,} rows)")
        else:
            df = load_dataset_fn()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return

    # Detect available columns dynamically
    all_columns = list(df.columns)
    numerical_cols_detected = df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    target_col_default = "Machine failure"

    # Check if standard target column exists
    target_col = target_col_default if target_col_default in df.columns else None

    tabs = st.tabs(["📋 Dataset Overview", "📊 Feature Analysis", "🔗 Correlations", "🎛️ Interactive Filter"])


    # ========================================================================
    # TAB 1 — Dataset Overview
    # ========================================================================

    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Records", f"{len(df):,}")
        with c2:
            st.metric("Features", f"{len(df.columns)}")
        with c3:
            st.metric("Missing Values", f"{df.isnull().sum().sum()}")
        with c4:
            st.metric("Duplicates", f"{df.duplicated().sum()}")

        st.markdown("### Dataset Sample")
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)

        st.markdown("### Statistical Summary")
        st.dataframe(
            df.describe().round(3).T,
            use_container_width=True,
        )

        st.markdown("### Data Types")
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Type": [str(t) for t in df.dtypes],
            "Non-Null": [int(df[c].notna().sum()) for c in df.columns],
            "Null": [int(df[c].isna().sum()) for c in df.columns],
            "Unique": [int(df[c].nunique()) for c in df.columns],
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    # ========================================================================
    # TAB 2 — Feature Analysis
    # ========================================================================

    with tabs[1]:
        target_col = "Machine failure"

        st.markdown("### Feature Distributions by Failure Status")

        numerical_cols = [
            "Air temperature [K]", "Process temperature [K]",
            "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"
        ]

        for col in numerical_cols:
            if col not in df.columns:
                continue

            fig = go.Figure()
            for label, color, name in [(0, "#22c55e", "No Failure"), (1, "#ef4444", "Failure")]:
                subset = df[df[target_col] == label][col]
                fig.add_trace(go.Histogram(
                    x=subset, name=name, marker_color=color,
                    opacity=0.6, nbinsx=40,
                ))

            fig.update_layout(
                title=f"{col} — Distribution by Failure Status",
                title_font=dict(size=14, color="#e2e8f0"),
                barmode="overlay",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis_title=col,
                yaxis_title="Count",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=50, b=30),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Boxplots
        st.markdown("### Feature Boxplots by Failure Status")
        selected_feat = st.selectbox("Select feature for boxplot:", numerical_cols)
        if selected_feat in df.columns:
            fig = px.box(
                df, x=target_col, y=selected_feat,
                color=target_col,
                color_discrete_map={0: "#22c55e", 1: "#ef4444"},
                labels={target_col: "Machine Failure", selected_feat: selected_feat},
            )
            fig.update_layout(
                height=350,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Failure type breakdown
        st.markdown("### Failure Type Breakdown")
        failure_cols = ["TWF", "HDF", "PWF", "OSF", "RNF"]
        failure_counts = {
            "Tool Wear Failure (TWF)": int(df["TWF"].sum()) if "TWF" in df.columns else 0,
            "Heat Dissipation (HDF)": int(df["HDF"].sum()) if "HDF" in df.columns else 0,
            "Power Failure (PWF)": int(df["PWF"].sum()) if "PWF" in df.columns else 0,
            "Overstrain (OSF)": int(df["OSF"].sum()) if "OSF" in df.columns else 0,
            "Random Failure (RNF)": int(df["RNF"].sum()) if "RNF" in df.columns else 0,
        }

        fig = go.Figure(go.Bar(
            x=list(failure_counts.values()),
            y=list(failure_counts.keys()),
            orientation="h",
            marker_color=["#f97316", "#ef4444", "#8b5cf6", "#3b82f6", "#64748b"],
            text=[str(v) for v in failure_counts.values()],
            textposition="outside",
        ))
        fig.update_layout(
            title="Failure Type Distribution",
            title_font=dict(size=14, color="#e2e8f0"),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            xaxis_title="Count",
            margin=dict(t=50, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 3 — Correlations
    # ========================================================================

    with tabs[2]:
        st.markdown("### Feature Correlation Heatmap")

        # Interactive correlation

        numerical_df = df[numerical_cols + [target_col]].copy()
        corr = numerical_df.corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale="RdBu_r",
            zmid=0,
            text=np.round(corr.values, 3),
            texttemplate="%{text}",
            textfont={"size": 10},
        ))
        fig.update_layout(
            title="Interactive Correlation Matrix",
            title_font=dict(size=14, color="#e2e8f0"),
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Scatter plot
        st.markdown("### Feature Scatter Plot")
        sc1, sc2 = st.columns(2)
        with sc1:
            x_feat = st.selectbox("X-axis:", numerical_cols, index=3)
        with sc2:
            y_feat = st.selectbox("Y-axis:", numerical_cols, index=2)

        fig = px.scatter(
            df, x=x_feat, y=y_feat,
            color=target_col,
            color_discrete_map={0: "#22c55e", 1: "#ef4444"},
            opacity=0.5,
            labels={target_col: "Failure"},
        )
        fig.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 4 — Interactive Filter
    # ========================================================================

    with tabs[3]:
        st.markdown("### Filter & Explore Dataset")

        fcol1, fcol2, fcol3 = st.columns(3)

        with fcol1:
            type_filter = st.multiselect(
                "Product Type",
                df["Type"].unique() if "Type" in df.columns else [],
                default=list(df["Type"].unique()) if "Type" in df.columns else [],
            )

        with fcol2:
            failure_filter = st.multiselect(
                "Failure Status",
                [0, 1], default=[0, 1],
                format_func=lambda x: "No Failure" if x == 0 else "Failure",
            )

        with fcol3:
            torque_range = st.slider(
                "Torque Range [Nm]",
                float(df["Torque [Nm]"].min()),
                float(df["Torque [Nm]"].max()),
                (float(df["Torque [Nm]"].min()), float(df["Torque [Nm]"].max())),
            )

        # Apply filters
        filtered = df.copy()
        if "Type" in filtered.columns and type_filter:
            filtered = filtered[filtered["Type"].isin(type_filter)]
        if failure_filter is not None:
            filtered = filtered[filtered[target_col].isin(failure_filter)]
        filtered = filtered[
            (filtered["Torque [Nm]"] >= torque_range[0]) &
            (filtered["Torque [Nm]"] <= torque_range[1])
        ]

        st.metric("Filtered Records", f"{len(filtered):,}")
        st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)

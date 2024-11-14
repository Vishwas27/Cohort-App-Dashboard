import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np


def run(df):
    # ----------------------- Data Aggregation -----------------------
    # Aggregate data by activity_date to create the metrics and charts
    df_aggregated = df.groupby('activity_date').agg({
        'registered_users': 'sum',
        'active_users': 'sum',
        'market_spend': 'sum',
        'purchase_value': 'sum'
    }).reset_index()

    # Calculate additional KPIs
    df_aggregated['roas'] = df_aggregated['purchase_value'] / df_aggregated['market_spend'].replace(0, pd.NA)
    df_aggregated['new_users'] = df_aggregated['registered_users'].diff().fillna(df_aggregated['registered_users'])

    # ----------------------- Dashboard Header -----------------------
    st.header("Dashboard")

    # ----------------------- Financials Section -----------------------
    # Check if 'purchase_value' exists before accessing it
    if 'purchase_value' in df_aggregated.columns:
        Dashboard_F_KPI_1 = f"${df_aggregated['purchase_value'].sum():,.2f}"
        Dashboard_F_KPI_2 = f"${df_aggregated['purchase_value'].sum() / 2:,.2f}"
    else:
        Dashboard_F_KPI_1 = "$0.00"
        Dashboard_F_KPI_2 = "$0.00"
        st.warning("Column 'purchase_value' does not exist in df_aggregated. Default values are being used.")

    with st.container():
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(label="FY Gross Revenue", value=Dashboard_F_KPI_1, delta="1%")
        kpi2.metric(label="FY Gross Margin", value=Dashboard_F_KPI_2, delta="-5%")  # Placeholder value
        kpi3.metric(label="Current", value="4,666,425", delta="5%")  # Placeholder value
        kpi4.metric(label="Current", value="4,545,121", delta="6%")  # Placeholder value


    with st.container():
        st.header("Financials")

    
        # Financial chart for market spend over time using Plotly
        financial_chart = px.line(
            df_aggregated,
            x='activity_date',
            y='market_spend',
            title="Market Spend Over Time"
        )

        # Customize layout
        financial_chart.update_layout(
            yaxis_title="Marketing Spend",
            xaxis_title="Activity Date",
            title_x=0.5,
            height=300,
            width=800
        )

        # Display chart in Streamlit with full container width
        st.plotly_chart(financial_chart, use_container_width=True)

    # ----------------------- Monthly Financials Overview -----------------------
    with st.container():
        st.subheader("Monthly Financials Overview")

        # Display KPIs
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

        # Check for purchase_value and new_users to avoid KeyError
        revenue_value = df_aggregated['purchase_value'].sum() if 'purchase_value' in df_aggregated.columns else 0
        new_users_value = df_aggregated['new_users'].sum() if 'new_users' in df_aggregated.columns else 0
        active_users_value = df_aggregated['active_users'].sum() if 'active_users' in df_aggregated.columns else 1  # Prevent division by zero

        kpi1.metric(label="Revenue", value=f"${revenue_value:,.2f}", delta="1%")
        kpi2.metric(label="eCPI", value=f"${(df_aggregated['market_spend'].sum() / new_users_value):.2f}" if new_users_value > 0 else "$0.00", delta="-5%")
        kpi3.metric(label="ARPDAU", value=f"${(revenue_value / active_users_value):.2f}", delta="5%")
        kpi4.metric(label="D7 Retention", value="12.88%", delta="6%")  # Placeholder value
        kpi5.metric(label="D365 Retention", value="1.49%", delta="7%")  # Placeholder value
        print(df_aggregated.columns)

    # ----------------------- ROAS Overview -----------------------
    with st.container():
        roas_chart = alt.Chart(df_aggregated).mark_line().encode(
            x='activity_date:T',
            y='roas:Q'
        ).properties(
            height=200
        )
        st.altair_chart(roas_chart, use_container_width=True)

    with st.container():
        st.subheader("eROAS Table")
        er_table = df_aggregated[['activity_date', 'roas', 'market_spend', 'purchase_value']].sample(10)
        st.dataframe(er_table, height=200, use_container_width=True)

    # ----------------------- New Users Over Time -----------------------
    with st.container():
        st.subheader("New Users Over Time")

        # New Users line chart
        new_users_chart = alt.Chart(df_aggregated).mark_line().encode(
            x='activity_date:T',
            y='new_users:Q'
        ).properties(
            height=200
        )
        st.altair_chart(new_users_chart, use_container_width=True)

    # ----------------------- Row 1 -----------------------
    with st.container():
        st.subheader("Row 1")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**CAC (Customer Acquisition Cost)**")
            # Sample data for CAC chart
            data_cac = pd.DataFrame({
                'Cohort': ['Cohort 1', 'Cohort 2', 'Cohort 3'],
                'CAC': [120, 150, 140]
            })
            cac_chart = alt.Chart(data_cac).mark_line().encode(
                x='Cohort',
                y='CAC'
            )
            st.altair_chart(cac_chart, use_container_width=True)

        with col2:
            st.markdown("**New Users**")
            # Sample data for New Users chart
            data_new_users = pd.DataFrame({
                'Cohort': ['Cohort 1', 'Cohort 2', 'Cohort 3'],
                'New Users': [300, 400, 350]
            })
            new_users_chart = alt.Chart(data_new_users).mark_line().encode(
                x='Cohort',
                y='New Users'
            )
            st.altair_chart(new_users_chart, use_container_width=True)

    # ----------------------- Row 2 -----------------------
    with st.container():
        st.subheader("Row 2")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Revenue**")
            # Sample data for Revenue chart
            data_revenue = pd.DataFrame({
                'Cohort': ['Cohort 1', 'Cohort 2', 'Cohort 3'],
                'Revenue': [1000, 1500, 1300]
            })
            revenue_chart = alt.Chart(data_revenue).mark_line().encode(
                x='Cohort',
                y='Revenue'
            )
            st.altair_chart(revenue_chart, use_container_width=True)

        with col4:
            st.markdown("**Retention**")
            # Sample data for Retention chart
            data_retention = pd.DataFrame({
                'Cohort': ['Cohort 1', 'Cohort 2', 'Cohort 3'],
                'Retention': [0.75, 0.80, 0.78]
            })
            retention_chart = alt.Chart(data_retention).mark_line().encode(
                x='Cohort',
                y='Retention'
            )
            st.altair_chart(retention_chart, use_container_width=True)

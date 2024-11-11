import streamlit as st
import pandas as pd
import altair as alt

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

    # ----------------------- Header and Data Preview -----------------------
    st.header("Dashboard")
    with st.container():
        st.subheader("Data Preview")
        st.dataframe(df.head(10))  # Display the first 10 rows of the data

    # ----------------------- Financials Section -----------------------
    Dashboard_F_KPI_1 = f"${df_aggregated['purchase_value'].sum():,.2f}"
    Dashboard_F_KPI_2 = f"${df_aggregated['purchase_value'].sum()/2:,.2f}"
    with st.container():
        st.header("Financials")

        F0, F1 = st.columns([0.6, 0.4])

        # Financial chart for market spend over time
        financial_chart = alt.Chart(df_aggregated).mark_line().encode(
            x='activity_date:T',
            y=alt.Y('market_spend:Q', title='Marketing Spend'),
            color=alt.value('#1f77b4')
        ).properties(
            width=600,
            height=300
        )
        F0.altair_chart(financial_chart, use_container_width=True)

        # Display financial metrics
        with F1:
            st.metric(label="FY Gross Revenue", value= Dashboard_F_KPI_1, delta="1%")
            st.metric(label="FY Gross Margin", value=Dashboard_F_KPI_2, delta="-5%")  # Placeholder value
            st.metric(label="Current", value="4,666,425", delta="5%")  # Placeholder value
            st.metric(label="Current", value="4,545,121", delta="6%")  # Placeholder value

    # ----------------------- Monthly Financials Overview -----------------------
    with st.container():
        st.subheader("Monthly Financials Overview")

        # Display KPIs
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        kpi1.metric(label="Revenue", value=f"${df_aggregated['purchase_value'].sum():,.2f}", delta="1%")
        kpi2.metric(label="eCPI", value=f"${(df_aggregated['market_spend'].sum() / df_aggregated['new_users'].sum()):.2f}", delta="-5%")
        kpi3.metric(label="ARPDAU", value=f"${(df_aggregated['purchase_value'] / df_aggregated['active_users']).mean():.2f}", delta="5%")
        kpi4.metric(label="D7 Retention", value="12.88%", delta="6%")  # Placeholder value
        kpi5.metric(label="D365 Retention", value="1.49%", delta="7%")  # Placeholder value

    # ----------------------- ROAS Overview -----------------------
    with st.container():
        st.subheader("ROAS Overview")   
        
        col1, col2 = st.columns([0.6, 0.4])

        # ROAS line chart
        with col1:
            roas_chart = alt.Chart(df_aggregated).mark_line().encode(
                x='activity_date:T',
                y='roas:Q'
            ).properties(
                height=200
            )
            st.altair_chart(roas_chart, use_container_width=True)

        # eROAS table with example data
        with col2:
            st.subheader("eROAS Table")
            er_table = df_aggregated[['activity_date', 'roas', 'market_spend', 'purchase_value']].sample(10)
            st.dataframe(er_table, height=200)

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

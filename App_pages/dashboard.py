import streamlit as st
import pandas as pd
import altair as alt

def run(df):
    # Set up the dashboard layout
    st.header("Dashboard")

    # Display a preview of the main data table
    with st.container():
        st.subheader("Data Preview")
        st.dataframe(df.head(10))  # Display the first 10 rows of the df

    # Sidebar filter for segment selection
    unique_segments = df['segment'].unique()  
    selected_segment = st.selectbox("Select Segment for Graphs", options=unique_segments)

    # Filter the dataframe based on the selected segment
    filtered_df = df[df['segment'] == selected_segment]

    with st.container():
        st.header("Financials")

        F0, F1 = st.columns([0.6, 0.4])

        # Line chart for revenue and marketing spend based on selected segment
        financial_chart = alt.Chart(filtered_df).mark_line().encode(
            x='activity_date:T',
            y=alt.Y('marketing_spend', title='Marketing Spend'),
            color='segment'
        ).properties(
            width=600,
            height=300
        )
        F0.altair_chart(financial_chart, use_container_width=True)

        # Display metrics in the second column (F1) in two rows
        with F1:
            # First row of metrics
            metric1, metric2 = st.columns(2)
            with metric1:
                st.metric(label="FY Gross Revenue", value="200,692,549", delta="1%")
            with metric2:
                st.metric(label="FY Gross Margin", value="53,541,123", delta="-5%")

            # Second row of metrics
            metric3, metric4 = st.columns(2)
            with metric3:
                st.metric(label="Current", value="4,666,425", delta="5%")
            with metric4:
                st.metric(label="Current", value="4,545,121", delta="6%")

    with st.container():
        st.subheader("Monthly Financials Overview")

        # Display KPIs
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        kpi1.metric(label="Revenue", value="20,692,549", delta="1%")
        kpi2.metric(label="eCPI", value="14.54", delta="-5%")
        kpi3.metric(label="ARPDAU", value="0.916", delta="5%")
        kpi4.metric(label="D7 Retention", value="12.88%", delta="6%")
        kpi5.metric(label="D365 Retention", value="1.49%", delta="7%")

    with st.container():
        st.subheader("ROAS Overview")   
        
        # Create two columns with 60% and 40% width for the chart and table respectively
        col1, col2 = st.columns([0.6, 0.4])

        # ROAS (Return on Ad Spend) chart based on selected segment
        with col1:
            st.subheader("Return on Ad Spend (ROAS) over Time")
            roas_chart = alt.Chart(filtered_df).mark_line().encode(
                x='activity_date:T',
                y='num_users:Q',
                color='segment'
            ).properties(
                height=200
            )
            st.altair_chart(roas_chart, use_container_width=True)

        # eROAS table with example data filtered by selected segment
        with col2:
            st.subheader("eROAS (Estimated ROAS) Table")
            er_table = filtered_df[['cohort', 'segment', 'num_users', 'marketing_spend']].sample(10)
            st.dataframe(er_table, height=200)

    with st.container():
        st.subheader("New Users Over Time")
        
        # Chart for New Users over time
        new_users_chart = alt.Chart(filtered_df).mark_line().encode(
            x='activity_date:T',
            y='num_users:Q',
            color='segment'
        ).properties(
            height=200
        )
        st.altair_chart(new_users_chart, use_container_width=True)

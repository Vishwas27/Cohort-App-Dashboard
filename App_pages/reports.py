import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

def run():
    # Set up the reports layout
    st.title("Reports")

    # Define the reports under each report type
    report_types = {
        "New Customer Acquisition": {
            "ROAS - Account Age Trends": plot_roas_account_age_trends,
            "ROAS - Cohort Trends": plot_roas_cohort_trends,
            "ROAS - Overview": plot_roas_overview,
            "ROAS - Cohort View": plot_roas_cohort_view,
            "CAC - Overview": plot_cac_overview,
            "Marketing Spend - Overview": plot_marketing_spend_overview,
            "New Users - Overview": plot_new_users_overview,
        },
        "Monetization & Revenue": {
            "ARPU - Overview": plot_arpu_overview,
            "ARPU - Cohort View": plot_arpu_cohort_view,
            "ARPU - Account Age Trends": plot_arpu_account_age_trends,
            "ARPU - Cohort Trends": plot_arpu_cohort_trends,
            "CLV - Account Age Trends": plot_clv_account_age_trends,
            "CLV - Cohort Trends": plot_clv_cohort_trends,
            "CLV - Overview": plot_clv_overview,
            "CLV - Cohort View": plot_clv_cohort_view,
            "Revenue - Cohort Contribution": plot_revenue_cohort_contribution,
            "Revenue - Overview": plot_revenue_overview,
        },
        "Retention": {
            "Active Users - Cohort Contribution": plot_active_users_cohort_contribution,
            "Active Users - Overview": plot_active_users_overview,
            "Retention - Overview": plot_retention_overview,
            "Retention - Cohort View": plot_retention_cohort_view,
            "Retention - Account Age Trends": plot_retention_account_age_trends,
            "Retention - Cohort Trends": plot_retention_cohort_trends,
        }
    }

    # Sidebar for selecting report type and report
    selected_report_type = st.sidebar.selectbox("Select Report Type", list(report_types.keys()))
    if selected_report_type:
        selected_report = st.sidebar.selectbox("Select Report", list(report_types[selected_report_type].keys()))

        # Display the selected report
        if selected_report:
            report_types[selected_report_type][selected_report]()  # Call the function associated with the selected report



##NEW USERS---------------------------------------------------------------------------------

def plot_roas_cohort_view():
    st.write("### ROAS - Cohort Trends")
    # Sample chart for ROAS Cohort Trends
    data = pd.DataFrame({
        'Cohort': ['Cohort 1', 'Cohort 2', 'Cohort 3'],
        'ROAS': [2.0, 2.5, 2.2]
    })
    chart = alt.Chart(data).mark_line().encode(
        x='Cohort',
        y='ROAS'
    )
    st.altair_chart(chart, use_container_width=True)


def plot_new_users_overview():
    st.write("### ROAS - Cohort Trends")
    # Sample chart for ROAS Cohort Trends
    data = pd.DataFrame({
        'Cohort': ['Cohort 1', 'Cohort 2', 'Cohort 3'],
        'ROAS': [2.0, 2.5, 2.2]
    })
    chart = alt.Chart(data).mark_line().encode(
        x='Cohort',
        y='ROAS'
    )
    st.altair_chart(chart, use_container_width=True)




##Monetization & Revenue---------------------------------------------------------------------------------
def plot_arpu_overview():
    print("ABC")

def plot_retention_cohort_view():
    print("ABC")

def plot_retention_account_age_trends():
    print("ABC")

def plot_retention_cohort_trends():
    print("ABC")





def plot_arpu_cohort_view():
    print("ABC")

def plot_arpu_account_age_trends():
    print("ABC")

def plot_arpu_cohort_trends():
    print("ABC")

def plot_clv_account_age_trends():
    print("ABC")

def plot_clv_cohort_trends():
    print("ABC")

def plot_clv_overview():
    print("ABC")

def plot_clv_cohort_view():
    print("ABC")

def plot_revenue_cohort_contribution():
    print("ABC")

def plot_revenue_overview():
    print("ABC")

def plot_active_users_cohort_contribution():
    print("ABC")

def plot_active_users_overview():
    print("ABC")

def plot_retention_overview():
    print("ABC")




##Retention---------------------------------------------------------------------------------


def plot_cac_overview():
    # Container with 6 columns
    with st.container():
        # Define six columns
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        # Dropdowns or filters for each column
        with col1:
            filter1 = st.selectbox("Data Range", ["6 Months", "12 Months", "24 Months"], key="filter1")

        with col2:
            filter2 = st.selectbox("Segment", ["Tier 1|US|M", "Tier 2|UK|M", "Tier 2|GE|M"], key="filter2")

        with col3:
            filter3 = st.selectbox("Country", ["US", "UK", "GE","JP"], key="filter3")

        with col4:
            filter4 = st.selectbox("Network", ["Network A","Network B","Network C", "Value 2", "Value 3"], key="filter4")

        with col5:
            filter5 = st.selectbox("Channel", ["PAID", "Organic"], key="filter5")

        with col6:
            filter6 = st.selectbox("Platform", ["Item 1", "Item 2", "Item 3"], key="filter6")
        
        with col7:
            filter7 = st.selectbox("Platform", ["Item 1", "Item 2", "Item 3"], key="filter7")



    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.write("### CAC - Overview")
            # Sample chart for CAC Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'CAC': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='CAC'
            )
            st.altair_chart(chart, use_container_width=True)

        with st.container():
            st.write("### CAC - Country")
            # Sample chart for CAC Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'CAC': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='CAC'
            )
            st.altair_chart(chart, use_container_width=True)
    
    with col2:
        with st.container():
            st.write("### CAC - Segment")
            # Sample chart for CAC Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'CAC': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='CAC'
            )
            st.altair_chart(chart, use_container_width=True)

        with st.container():
            st.write("### CAC - Network")
            # Sample chart for CAC Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'CAC': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='CAC'
            )
            st.altair_chart(chart, use_container_width=True)
        
    





def plot_roas_account_age_trends():
    st.write("### ROAS - Account Age Trends")
    # Sample chart for ROAS Account Age Trends
    data = pd.DataFrame({
        'Account Age (Months)': [1, 2, 3, 4, 5],
        'ROAS': [1.5, 2.0, 1.8, 2.3, 2.1]
    })
    chart = alt.Chart(data).mark_bar().encode(
        x='Account Age (Months)',
        y='ROAS'
    )
    st.altair_chart(chart, use_container_width=True)

def plot_roas_cohort_trends():
    st.write("### ROAS - Cohort Trends")
    # Sample chart for ROAS Cohort Trends
    data = pd.DataFrame({
        'Cohort': ['Cohort 1', 'Cohort 2', 'Cohort 3'],
        'ROAS': [2.0, 2.5, 2.2]
    })
    chart = alt.Chart(data).mark_line().encode(
        x='Cohort',
        y='ROAS'
    )
    st.altair_chart(chart, use_container_width=True)

def plot_roas_overview():
    # Container with 6 columns
    with st.container():
        # Define six columns
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        # Dropdowns or filters for each column
        with col1:
            filter1 = st.selectbox("Data Range", ["6 Months", "12 Months", "24 Months"], key="filter1")

        with col2:
            filter2 = st.selectbox("Segment", ["Tier 1|US|M", "Tier 2|UK|M", "Tier 2|GE|M"], key="filter2")

        with col3:
            filter3 = st.selectbox("Country", ["US", "UK", "GE","JP"], key="filter3")

        with col4:
            filter4 = st.selectbox("Network", ["Network A","Network B","Network C", "Value 2", "Value 3"], key="filter4")

        with col5:
            filter5 = st.selectbox("Channel", ["PAID", "Organic"], key="filter5")

        with col6:
            filter6 = st.selectbox("Platform", ["Item 1", "Item 2", "Item 3"], key="filter6")
        
        with col7:
            filter7 = st.selectbox("Platform", ["Item 1", "Item 2", "Item 3"], key="filter7")



    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.write("### ROAS - Overview")
            # Sample chart for ROAS Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'ROAS': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='ROAS'
            )
            st.altair_chart(chart, use_container_width=True)

        with st.container():
            st.write("### ROAS - Country")
            # Sample chart for ROAS Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'ROAS': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='ROAS'
            )
            st.altair_chart(chart, use_container_width=True)
    
    with col2:
        with st.container():
            st.write("### ROAS - Segment")
            # Sample chart for ROAS Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'ROAS': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='ROAS'
            )
            st.altair_chart(chart, use_container_width=True)

        with st.container():
            st.write("### ROAS - Network")
            # Sample chart for ROAS Overview
            data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
                'ROAS': [100, 120, 110, 130]
            })
            chart = alt.Chart(data).mark_line().encode(
                x='Month',
                y='ROAS'
            )
            st.altair_chart(chart, use_container_width=True)
        

# Add more plotting functions as needed
def plot_revenue_trends():
    st.write("### Revenue Trends")
    # Placeholder for Revenue Trends chart
    st.line_chart(np.random.randn(100).cumsum())

def plot_marketing_spend_overview():
    st.write("### Marketing Spend Overview")
    # Placeholder for Marketing Spend Overview chart
    st.bar_chart(np.random.rand(10))

def plot_user_acquisition_trends():
    st.write("### User Acquisition Trends")
    # Placeholder for User Acquisition Trends chart
    st.area_chart(np.random.randn(100).cumsum())

def plot_monthly_retention_rates():
    st.write("### Monthly Retention Rates")
    # Placeholder for Monthly Retention Rates chart
    st.line_chart(np.random.rand(12))

def plot_performance_metrics():
    st.write("### Performance Metrics")
    # Placeholder for Performance Metrics chart
    st.bar_chart(np.random.rand(5))

def plot_churn_analysis():
    st.write("### Churn Analysis")
    # Placeholder for Churn Analysis chart
    st.line_chart(np.random.randn(100).cumsum())

# To run the page
if __name__ == "__main__":
    run()

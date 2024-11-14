import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


def run(df):
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
            report_types[selected_report_type][selected_report](df)  # Call the function associated with the selected report

##-----------------------------------------------------------------------------------------------------------------------
##-----------------NEW USERS ACQUISATION---------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------------------------------------------
            

def plot_roas_account_age_trends(df):
    st.write("### ROAS - Account Age Trends")

    # First two containers for filters
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        date_range = col1.date_input("Date Range", [])
        segment = col2.selectbox("Segment", df['segment'].unique())
        country = col3.selectbox("Country", df['country'].unique())
        network = col4.selectbox("Network", df['network'].unique())

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        channel = col1.selectbox("Channel", df['channel'].unique())
        platform = col2.selectbox("Platform", df['platform'].unique())
        account_age_filter = col3.multiselect("Account Age", [1, 7, 30, 90, 180, 365, 730], default=[1, 7, 30, 90])

    # Filter DataFrame based on selected filters
    filtered_df = df[
        (df['segment'] == segment) &
        (df['country'] == country) &
        (df['network'] == network) &
        (df['channel'] == channel) &
        (df['platform'] == platform)
    ]

    # Calculate cumulative columns for market spend and purchase value by cohort_date, segment, and incremental account_age
    filtered_df['cumulative_market_spend'] = filtered_df.sort_values('account_age') \
        .groupby(['cohort_date', 'segment'])['market_spend'].cumsum()
    filtered_df['cumulative_purchase_value'] = filtered_df.sort_values('account_age') \
        .groupby(['cohort_date', 'segment'])['purchase_value'].cumsum()

    # Calculate cumulative ROAS as percentage
    filtered_df['cumulative_roas'] = (filtered_df['cumulative_purchase_value'] / filtered_df['cumulative_market_spend']) * 100

    # Filter for selected account ages
    filtered_df = filtered_df[filtered_df['account_age'].isin(account_age_filter)]


    # Plotting cumulative ROAS line chart
    fig = px.line(
        filtered_df,
        x='activity_date',
        y='cumulative_roas',
        color='account_age',
        labels={'cumulative_roas': 'ROAS (%)', 'activity_date': 'Activity Date'},
        title="Cumulative ROAS by Account Age"
    )
    
    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # Fourth container for average ROAS table over the last six months
    with st.container():
        # Filter data for the last six months based on the latest date in the date range
        last_date = pd.to_datetime(filtered_df['activity_date'].max())
        six_months_prior = last_date - pd.DateOffset(months=6)
        last_six_months_df = filtered_df[filtered_df['activity_date'] >= six_months_prior]

        # Calculate average ROAS for each account age by month
        last_six_months_df['month'] = last_six_months_df['activity_date'].dt.to_period('M')
        avg_roas_df = last_six_months_df.groupby(['account_age', 'month'])['cumulative_roas'].mean().unstack().fillna(0)
        
        # Display table
        st.write("### Average ROAS by Account Age for Last 6 Months")
        st.dataframe(avg_roas_df, use_container_width=True)


##-----------------------------------------------------------------------------------------------------------------------


def plot_roas_cohort_trends(df):
    st.write("### ROAS - Cohort View")

    # First two containers for filters
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        date_range = col1.date_input("Date Range", [])
        segment = col2.selectbox("Segment", df['segment'].unique())
        country = col3.selectbox("Country", df['country'].unique())
        network = col4.selectbox("Network", df['network'].unique())

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        channel = col1.selectbox("Channel", df['channel'].unique())
        platform = col2.selectbox("Platform", df['platform'].unique())
        account_age_filter = col3.multiselect("Account Age", [1, 7, 30, 90, 180, 365, 730], default=[1, 7, 30, 90])

    # Filter DataFrame based on selected filters
    filtered_df = df[
        (df['segment'] == segment) &
        (df['country'] == country) &
        (df['network'] == network) &
        (df['channel'] == channel) &
        (df['platform'] == platform)
    ]

    # Calculate cumulative columns for market spend and purchase value by cohort_date and incremental account_age
    filtered_df = filtered_df.sort_values('account_age')
    filtered_df['cumulative_market_spend'] = filtered_df.groupby(['cohort_date', 'segment'])['market_spend'].cumsum()
    filtered_df['cumulative_purchase_value'] = filtered_df.groupby(['cohort_date', 'segment'])['purchase_value'].cumsum()

    # Calculate cumulative ROAS as percentage
    filtered_df['cumulative_roas'] = (filtered_df['cumulative_purchase_value'] / filtered_df['cumulative_market_spend']) * 100

    # Filter for selected account ages
    filtered_df = filtered_df[filtered_df['account_age'].isin(account_age_filter)]

    # Display preview of filtered data
    st.write("### Filtered Data Preview")
    st.dataframe(filtered_df.head(), use_container_width=True)

    # Plotting cumulative ROAS line chart with cohort as legend
    fig = px.line(
        filtered_df,
        x='account_age',
        y='cumulative_roas',
        color='cohort_date',
        labels={'cumulative_roas': 'ROAS (%)', 'account_age': 'Account Age'},
        title="Cumulative ROAS by Cohort Date"
    )
    
    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # Fourth container for ROAS table by cohort date and account age
    with st.container():
        # Filter data for the last six months based on the latest date in the date range
        last_date = pd.to_datetime(filtered_df['activity_date'].max())
        six_months_prior = last_date - pd.DateOffset(months=6)
        last_six_months_df = filtered_df[filtered_df['activity_date'] >= six_months_prior]

        # Pivot table to show ROAS with rows as cohort date and columns as account age
        roas_pivot_df = last_six_months_df.pivot_table(
            index='cohort_date',
            columns='account_age',
            values='cumulative_roas',
            aggfunc='mean'
        ).reindex(columns=[1, 7, 30, 90, 180, 365, 730], fill_value=0)  # Ensure column order and fill missing values

        # Display table
        st.write("### ROAS by Cohort Date and Account Age")
        st.dataframe(roas_pivot_df, use_container_width=True)



##-----------------------------------------------------------------------------------------------------------------------

def create_roas_overview_chart(df, x_col, y_col, color_col, title, show_legend=True):
    """Helper function to create ROAS charts."""
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    
    if show_legend:
        fig.update_layout(
            legend=dict(
                orientation="h",  # Set legend to horizontal
                yanchor="top",    # Anchor the legend at the top of the box
                y=-0.2,           # Position the legend below the chart
                xanchor="center", # Center the legend horizontally
                x=0.5             # Center the legend at the bottom
            )
        )
    else:
        fig.update_layout(showlegend=False)
    
    return fig

def create_roas_overview_table(df, aggregation_type):
    """Helper function to create a table based on aggregation type with ROAS values."""
    # Aggregating the data by the selected aggregation type and activity_month
    aggregation_df = df.groupby([aggregation_type, 'activity_month']).agg({'market_spend': 'sum', 'purchase_value': 'sum'}).reset_index()

    # Calculating ROAS after aggregation: ROAS = Total Purchase Value / Total Market Spend
    aggregation_df['roas'] = (aggregation_df['purchase_value'] / aggregation_df['market_spend']) * 100
    
    # Pivoting the table to have the last 6 months as columns
    pivot_df = aggregation_df.pivot_table(index=aggregation_type, columns='activity_month', values='roas')

    # Select last six months dynamically
    pivot_df = pivot_df.iloc[:, -6:]
    
    return pivot_df

def plot_roas_overview(df):
    st.write("### ROAS - Overview by Activity Date")

    # Convert activity_date to datetime if not already
    df['activity_date'] = pd.to_datetime(df['activity_date'], errors='coerce')

    # Add new activity_month column for month-level aggregation
    df['activity_month'] = df['activity_date'].dt.to_period('M').dt.to_timestamp()

    # Filters with "No Filter" option
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))

        # New Date Range Filter
        date_range = col6.date_input("Date Range", [df['activity_date'].min(), df['activity_date'].max()])

        # Convert date_range to datetime to match activity_date format
        date_range = [pd.to_datetime(date) for date in date_range]

        # New Account Age Filter
        account_age = col7.selectbox("Account Age", ["All", 0, 1, 7, 14, 30, 60, 90, 180, 365, 730])

    # Filter DataFrame based on selected filters, excluding "No Filter" options
    filtered_df = df.copy()
    if segment != "No Filter":
        filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter":
        filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter":
        filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter":
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter":
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    if account_age != "All":
        filtered_df = filtered_df[filtered_df['account_age'] == account_age]
    if date_range:
        filtered_df = filtered_df[(filtered_df['activity_date'] >= date_range[0]) & (filtered_df['activity_date'] <= date_range[1])]

    # Ensure activity_month is correctly added to the filtered dataframe
    filtered_df['activity_month'] = filtered_df['activity_date'].dt.to_period('M').dt.to_timestamp()

    # Aggregating data for ROAS calculation (after filtering)
    filtered_df = filtered_df.groupby(['activity_date', 'segment', 'country', 'network', 'channel', 'platform']).agg({'market_spend': 'sum', 'purchase_value': 'sum'}).reset_index()

    # Calculate ROAS after aggregation: ROAS = Total Purchase Value / Total Market Spend
    filtered_df['roas'] = (filtered_df['purchase_value'] / filtered_df['market_spend']) * 100

    # Container for the six charts
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 1: Overall ROAS vs. Activity Date
        overall_df = filtered_df.groupby('activity_date').agg({'roas': 'mean'}).reset_index()
        fig_overall = create_roas_overview_chart(
            overall_df, 'activity_date', 'roas', None, "Overall Avg ROAS vs Activity Date"
        )
        col1.plotly_chart(fig_overall, use_container_width=True)

        # Chart 2: ROAS by Segment (without legend)
        segment_df = filtered_df.groupby(['activity_date', 'segment']).agg({'roas': 'mean'}).reset_index()
        fig_segment = create_roas_overview_chart(
            segment_df, 'activity_date', 'roas', 'segment', "ROAS by Segment vs Activity Date", show_legend=False
        )
        col2.plotly_chart(fig_segment, use_container_width=True)

    # 2nd Row: ROAS by Country and ROAS by Network
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 3: ROAS by Country
        country_df = filtered_df.groupby(['activity_date', 'country']).agg({'roas': 'mean'}).reset_index()
        fig_country = create_roas_overview_chart(
            country_df, 'activity_date', 'roas', 'country', "ROAS by Country vs Activity Date"
        )
        col1.plotly_chart(fig_country, use_container_width=True)

        # Chart 4: ROAS by Network
        network_df = filtered_df.groupby(['activity_date', 'network']).agg({'roas': 'mean'}).reset_index()
        fig_network = create_roas_overview_chart(
            network_df, 'activity_date', 'roas', 'network', "ROAS by Network vs Activity Date"
        )
        col2.plotly_chart(fig_network, use_container_width=True)

    # 3rd Row: ROAS by Channel and ROAS by Platform
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 5: ROAS by Channel
        channel_df = filtered_df.groupby(['activity_date', 'channel']).agg({'roas': 'mean'}).reset_index()
        fig_channel = create_roas_overview_chart(
            channel_df, 'activity_date', 'roas', 'channel', "ROAS by Channel vs Activity Date"
        )
        col1.plotly_chart(fig_channel, use_container_width=True)

        # Chart 6: ROAS by Platform
        platform_df = filtered_df.groupby(['activity_date', 'platform']).agg({'roas': 'mean'}).reset_index()
        fig_platform = create_roas_overview_chart(
            platform_df, 'activity_date', 'roas', 'platform', "ROAS by Platform vs Activity Date"
        )
        col2.plotly_chart(fig_platform, use_container_width=True)

    # Aggregated ROAS Table
    with st.container():
        st.write("### Aggregated ROAS Table")

        # Ensure activity_month column exists for pivoting
        if 'activity_month' not in filtered_df.columns:
            filtered_df['activity_month'] = filtered_df['activity_date'].dt.to_period('M').dt.to_timestamp()
        
        # Filter for the last six months of data based on activity_month
        last_6_months = filtered_df['activity_month'].dropna().sort_values().unique()[-6:]
        ROAS_table_df = filtered_df[filtered_df['activity_month'].isin(last_6_months)]
        
        # Aggregation level selection
        aggregation_type = st.selectbox("Select Level of Aggregation", ['segment', 'country', 'network', 'channel', 'platform'])
        
        # Generate and display table
        aggregation_table = create_roas_overview_table(ROAS_table_df, aggregation_type)
        st.dataframe(aggregation_table)

##-----------------------------------------------------------------------------------------------------------------------


def create_roas_chart(df, x_col, y_col, color_col, title, show_legend=True):
    """Helper function to create ROAS charts."""
    
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    
    # If legend is not needed, we hide it
    if not show_legend:
        fig.update_layout(showlegend=False)
    elif show_legend:
        fig.update_layout(
            legend=dict(
                orientation="h",  # Set legend to horizontal
                yanchor="top",    # Anchor the legend at the top of the box
                y=-0.2,           # Position the legend below the chart
                xanchor="center", # Center the legend horizontally
                x=0.5             # Center the legend at the bottom
            )
        )
    return fig

def create_roas_table(df, aggregation_type):
    """Helper function to create a table based on aggregation type with ROAS values."""
    # Aggregating the data by the selected aggregation type and account age
    aggregation_df = df.groupby([aggregation_type, 'account_age']).agg({'cumulative_roas': 'mean'}).reset_index()

    # Pivoting the table to have the account_age values as columns (D1, D7, D14, etc.)
    pivot_df = aggregation_df.pivot_table(index=aggregation_type, columns='account_age', values='cumulative_roas')

    # Renaming columns to D1, D7, D14, etc.
    pivot_df.columns = ['D1', 'D7', 'D14', 'D30', 'D90', 'D120', 'D180', 'D365', 'D540', 'D730']

    return pivot_df

def plot_roas_cohort_view(df):
    st.write("### ROAS - Cohort View by Account Age")

    # Filters with "No Filter" option
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Adding "No Filter" option to each dropdown
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))

    # Filter DataFrame based on selected filters, excluding "No Filter" options
    filtered_df = df.copy()
    if segment != "No Filter":
        filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter":
        filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter":
        filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter":
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter":
        filtered_df = filtered_df[filtered_df['platform'] == platform]

    # Calculate cumulative columns for market spend and purchase value by cohort_date and account_age
    filtered_df = filtered_df.sort_values('account_age')
    filtered_df['cumulative_market_spend'] = filtered_df.groupby(['cohort_date', 'segment'])['market_spend'].cumsum()
    filtered_df['cumulative_purchase_value'] = filtered_df.groupby(['cohort_date', 'segment'])['purchase_value'].cumsum()

    # Calculate cumulative ROAS as percentage
    filtered_df['cumulative_roas'] = (filtered_df['cumulative_purchase_value'] / filtered_df['cumulative_market_spend']) * 100

    # Container for the six charts
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 1: Overall ROAS vs. Account Age
        overall_df = filtered_df.groupby('account_age').agg({'cumulative_roas': 'mean'}).reset_index()
        fig_overall = create_roas_chart(
            overall_df, 'account_age', 'cumulative_roas', None, "Overall Avg ROAS vs Account Age"
        )
        col1.plotly_chart(fig_overall, use_container_width=True)

        # Chart 2: ROAS by Segment (without legend)
        segment_df = filtered_df.groupby(['account_age', 'segment']).agg({'cumulative_roas': 'mean'}).reset_index()
        fig_segment = create_roas_chart(
            segment_df, 'account_age', 'cumulative_roas', 'segment', "ROAS by Segment vs Account Age", show_legend=False
        )
        col2.plotly_chart(fig_segment, use_container_width=True)

    # 2nd Row: ROAS by Country and ROAS by Network
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 3: ROAS by Country
        country_df = filtered_df.groupby(['account_age', 'country']).agg({'cumulative_roas': 'mean'}).reset_index()
        fig_country = create_roas_chart(
            country_df, 'account_age', 'cumulative_roas', 'country', "ROAS by Country vs Account Age"
        )
        col1.plotly_chart(fig_country, use_container_width=True)

        # Chart 4: ROAS by Network
        network_df = filtered_df.groupby(['account_age', 'network']).agg({'cumulative_roas': 'mean'}).reset_index()
        fig_network = create_roas_chart(
            network_df, 'account_age', 'cumulative_roas', 'network', "ROAS by Network vs Account Age"
        )
        col2.plotly_chart(fig_network, use_container_width=True)

    # 3rd Row: ROAS by Channel and ROAS by Platform
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 5: ROAS by Channel
        channel_df = filtered_df.groupby(['account_age', 'channel']).agg({'cumulative_roas': 'mean'}).reset_index()
        fig_channel = create_roas_chart(
            channel_df, 'account_age', 'cumulative_roas', 'channel', "ROAS by Channel vs Account Age"
        )
        col1.plotly_chart(fig_channel, use_container_width=True)

        # Chart 6: ROAS by Platform
        platform_df = filtered_df.groupby(['account_age', 'platform']).agg({'cumulative_roas': 'mean'}).reset_index()
        fig_platform = create_roas_chart(
            platform_df, 'account_age', 'cumulative_roas', 'platform', "ROAS by Platform vs Account Age"
        )
        col2.plotly_chart(fig_platform, use_container_width=True)

    # Final Section: Aggregated ROAS Table
    with st.container():
        st.write("### Aggregated ROAS Table")

        # Filter data manually by account age (D1, D7, D14, etc.)
        ROAS_table_df = filtered_df[filtered_df['account_age'].isin([1, 7, 14, 30, 90, 120, 180, 365, 540, 730])]

        # Select aggregation level
        aggregation_type = st.selectbox("Select Level of Aggregation", ['segment', 'country', 'network', 'channel', 'platform'])
        
        # Generate and display the table
        aggregation_table = create_roas_table(ROAS_table_df, aggregation_type)
        st.dataframe(aggregation_table)

##-----------------------------------------------------------------------------------------------------------------------
def create_cac_overview_chart(df, x_col, y_col, color_col, title, show_legend=True):
    """Helper function to create CAC charts."""
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    if not show_legend:
        fig.update_layout(showlegend=False)
    elif show_legend:
        fig.update_layout(
            legend=dict(
                orientation="h",  # Set legend to horizontal
                yanchor="top",    # Anchor the legend at the top of the box
                y=-0.2,           # Position the legend below the chart
                xanchor="center", # Center the legend horizontally
                x=0.5             # Center the legend at the bottom
            )
        )
    return fig

def create_cac_overview_table(df, aggregation_type):
    """Helper function to create a table based on aggregation type with CAC values."""
    # Aggregating the data by the selected aggregation type and activity_month
    aggregation_df = df.groupby([aggregation_type, 'activity_month']).agg({'market_spend': 'sum', 'registered_users': 'sum'}).reset_index()
    
    # Calculate CAC for each aggregation
    aggregation_df['CAC'] = aggregation_df['market_spend'] / aggregation_df['registered_users']

    # Pivoting the table to have the last 6 months as columns
    pivot_df = aggregation_df.pivot_table(index=aggregation_type, columns='activity_month', values='CAC')

    # Select last six months dynamically
    pivot_df = pivot_df.iloc[:, -6:]
    
    return pivot_df

def plot_cac_overview(df):
    st.write("### CAC - Overview by Activity Date")

    # Convert activity_date to datetime if not already
    df['activity_date'] = pd.to_datetime(df['activity_date'], errors='coerce')

    # Add new activity_month column for month-level aggregation
    df['activity_month'] = df['activity_date'].dt.to_period('M').dt.to_timestamp()

    # Filters with "No Filter" option
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))

        # New Date Range Filter
        date_range = col6.date_input("Date Range", [df['activity_date'].min(), df['activity_date'].max()])

        # Convert date_range to datetime to match activity_date format
        date_range = [pd.to_datetime(date) for date in date_range]

    # Filter DataFrame based on selected filters, excluding "No Filter" options
    filtered_df = df.copy()
    if segment != "No Filter":
        filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter":
        filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter":
        filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter":
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter":
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    if date_range:
        filtered_df = filtered_df[(filtered_df['activity_date'] >= date_range[0]) & (filtered_df['activity_date'] <= date_range[1])]

    # Container for the six charts
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 1: Overall CAC vs. Activity Date
        overall_df = filtered_df.groupby('activity_date').agg({'market_spend': 'sum', 'registered_users': 'sum'}).reset_index()
        overall_df['CAC'] = overall_df['market_spend'] / overall_df['registered_users']
        fig_overall = create_cac_overview_chart(
            overall_df, 'activity_date', 'CAC', None, "Overall Avg CAC vs Activity Date"
        )
        col1.plotly_chart(fig_overall, use_container_width=True)

        # Chart 2: CAC by Segment (without legend)
        segment_df = filtered_df.groupby(['activity_date', 'segment']).agg({'market_spend': 'sum', 'registered_users': 'sum'}).reset_index()
        segment_df['CAC'] = segment_df['market_spend'] / segment_df['registered_users']
        fig_segment = create_cac_overview_chart(
            segment_df, 'activity_date', 'CAC', 'segment', "CAC by Segment vs Activity Date", show_legend=False
        )
        col2.plotly_chart(fig_segment, use_container_width=True)

    # 2nd Row: CAC by Country and by Network
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 3: CAC by Country
        country_df = filtered_df.groupby(['activity_date', 'country']).agg({'market_spend': 'sum', 'registered_users': 'sum'}).reset_index()
        country_df['CAC'] = country_df['market_spend'] / country_df['registered_users']
        fig_country = create_cac_overview_chart(
            country_df, 'activity_date', 'CAC', 'country', "CAC by Country vs Activity Date"
        )
        col1.plotly_chart(fig_country, use_container_width=True)

        # Chart 4: CAC by Network
        network_df = filtered_df.groupby(['activity_date', 'network']).agg({'market_spend': 'sum', 'registered_users': 'sum'}).reset_index()
        network_df['CAC'] = network_df['market_spend'] / network_df['registered_users']
        fig_network = create_cac_overview_chart(
            network_df, 'activity_date', 'CAC', 'network', "CAC by Network vs Activity Date"
        )
        col2.plotly_chart(fig_network, use_container_width=True)

    # 3rd Row: CAC by Channel and by Platform
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 5: CAC by Channel
        channel_df = filtered_df.groupby(['activity_date', 'channel']).agg({'market_spend': 'sum', 'registered_users': 'sum'}).reset_index()
        channel_df['CAC'] = channel_df['market_spend'] / channel_df['registered_users']
        fig_channel = create_cac_overview_chart(
            channel_df, 'activity_date', 'CAC', 'channel', "CAC by Channel vs Activity Date"
        )
        col1.plotly_chart(fig_channel, use_container_width=True)

        # Chart 6: CAC by Platform
        platform_df = filtered_df.groupby(['activity_date', 'platform']).agg({'market_spend': 'sum', 'registered_users': 'sum'}).reset_index()
        platform_df['CAC'] = platform_df['market_spend'] / platform_df['registered_users']
        fig_platform = create_cac_overview_chart(
            platform_df, 'activity_date', 'CAC', 'platform', "CAC by Platform vs Activity Date"
        )
        col2.plotly_chart(fig_platform, use_container_width=True)

    # Aggregated CAC Table
    with st.container():
        st.write("### Aggregated CAC Table")

        # Filter for the last six months of data based on activity_month
        last_6_months = filtered_df['activity_month'].dropna().sort_values().unique()[-6:]
        cac_table_df = filtered_df[filtered_df['activity_month'].isin(last_6_months)]
        
        # Aggregation level selection
        aggregation_type = st.selectbox("Select Level of Aggregation", ['segment', 'country', 'network', 'channel', 'platform'])
        
        # Generate and display table
        aggregation_table = create_cac_overview_table(cac_table_df, aggregation_type)
        st.dataframe(aggregation_table)


##-----------------------------------------------------------------------------------------------------------------------
def create_marketing_spend_overview_chart(df, x_col, y_col, color_col, title, show_legend=True):
    """Helper function to create Marketing Spend charts."""
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    if not show_legend:
        fig.update_layout(showlegend=False)
    elif show_legend:
        fig.update_layout(
            legend=dict(
                orientation="h",  # Set legend to horizontal
                yanchor="top",    # Anchor the legend at the top of the box
                y=-0.2,           # Position the legend below the chart
                xanchor="center", # Center the legend horizontally
                x=0.5             # Center the legend at the bottom
            )
        )
    return fig

def create_marketing_spend_overview_table(df, aggregation_type):
    """Helper function to create a table based on aggregation type with Marketing Spend values."""
    # Aggregating the data by the selected aggregation type and activity_month
    aggregation_df = df.groupby([aggregation_type, 'activity_month']).agg({'market_spend': 'sum'}).reset_index()

    # Pivoting the table to have the last 6 months as columns
    pivot_df = aggregation_df.pivot_table(index=aggregation_type, columns='activity_month', values='market_spend')

    # Select last six months dynamically
    pivot_df = pivot_df.iloc[:, -6:]
    
    return pivot_df

def plot_marketing_spend_overview(df):
    st.write("### Marketing Spend - Overview by Activity Date")

    # Convert activity_date to datetime if not already
    df['activity_date'] = pd.to_datetime(df['activity_date'], errors='coerce')

    # Add new activity_month column for month-level aggregation
    df['activity_month'] = df['activity_date'].dt.to_period('M').dt.to_timestamp()

    # Filters with "No Filter" option
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))

        # New Date Range Filter
        date_range = col6.date_input("Date Range", [df['activity_date'].min(), df['activity_date'].max()])

        # Convert date_range to datetime to match activity_date format
        date_range = [pd.to_datetime(date) for date in date_range]

        # New Account Age Filter
        account_age = col7.selectbox("Account Age", ["All", 0, 1, 7, 14, 30, 60, 90, 180, 365, 730])

    # Filter DataFrame based on selected filters, excluding "No Filter" options
    filtered_df = df.copy()
    if segment != "No Filter":
        filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter":
        filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter":
        filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter":
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter":
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    if account_age != "All":
        filtered_df = filtered_df[filtered_df['account_age'] == account_age]
    if date_range:
        filtered_df = filtered_df[(filtered_df['activity_date'] >= date_range[0]) & (filtered_df['activity_date'] <= date_range[1])]

    # Container for the six charts
    with st.container():
        col1, col2 = st.columns(2)
        
        

        # Chart 1: Overall Marketing Spend vs. Activity Date
        overall_df = filtered_df.groupby('activity_date').agg({'market_spend': 'sum'}).reset_index()
        fig_overall = create_marketing_spend_overview_chart(
            overall_df, 'activity_date', 'market_spend', None, "Overall Avg Marketing Spend vs Activity Date"
        )
        col1.plotly_chart(fig_overall, use_container_width=True)

        # Chart 2: Marketing Spend by Segment (without legend)
        segment_df = filtered_df.groupby(['activity_date', 'segment']).agg({'market_spend': 'sum'}).reset_index()
        fig_segment = create_marketing_spend_overview_chart(
            segment_df, 'activity_date', 'market_spend', 'segment', "Marketing Spend by Segment vs Activity Date", show_legend=False
        )
        col2.plotly_chart(fig_segment, use_container_width=True)

    # 2nd Row: Marketing Spend by Country and by Network
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 3: Marketing Spend by Country
        country_df = filtered_df.groupby(['activity_date', 'country']).agg({'market_spend': 'sum'}).reset_index()
        fig_country = create_marketing_spend_overview_chart(
            country_df, 'activity_date', 'market_spend', 'country', "Marketing Spend by Country vs Activity Date"
        )
        col1.plotly_chart(fig_country, use_container_width=True)

        # Chart 4: Marketing Spend by Network
        network_df = filtered_df.groupby(['activity_date', 'network']).agg({'market_spend': 'sum'}).reset_index()
        fig_network = create_marketing_spend_overview_chart(
            network_df, 'activity_date', 'market_spend', 'network', "Marketing Spend by Network vs Activity Date"
        )
        col2.plotly_chart(fig_network, use_container_width=True)

    # 3rd Row: Marketing Spend by Channel and by Platform
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 5: Marketing Spend by Channel
        channel_df = filtered_df.groupby(['activity_date', 'channel']).agg({'market_spend': 'sum'}).reset_index()
        fig_channel = create_marketing_spend_overview_chart(
            channel_df, 'activity_date', 'market_spend', 'channel', "Marketing Spend by Channel vs Activity Date"
        )
        col1.plotly_chart(fig_channel, use_container_width=True)

        # Chart 6: Marketing Spend by Platform
        platform_df = filtered_df.groupby(['activity_date', 'platform']).agg({'market_spend': 'sum'}).reset_index()
        fig_platform = create_marketing_spend_overview_chart(
            platform_df, 'activity_date', 'market_spend', 'platform', "Marketing Spend by Platform vs Activity Date"
        )
        col2.plotly_chart(fig_platform, use_container_width=True)

    # Aggregated Marketing Spend Table
    with st.container():
        st.write("### Aggregated Marketing Spend Table")

        # Filter for the last six months of data based on activity_month
        last_6_months = filtered_df['activity_month'].dropna().sort_values().unique()[-6:]
        marketing_spend_table_df = filtered_df[filtered_df['activity_month'].isin(last_6_months)]
        
        # Aggregation level selection
        aggregation_type = st.selectbox("Select Level of Aggregation", ['segment', 'country', 'network', 'channel', 'platform'])
        
        # Generate and display table
        aggregation_table = create_marketing_spend_overview_table(marketing_spend_table_df, aggregation_type)
        st.dataframe(aggregation_table)

##-----------------------------------------------------------------------------------------------------------------------


def create_new_users_overview_chart(df, x_col, y_col, color_col, title, show_legend=True):
    """Helper function to create New Users charts."""
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    if not show_legend:
        fig.update_layout(showlegend=False)
    return fig

def create_new_users_overview_table(df, aggregation_type):
    """Helper function to create a table based on aggregation type with New Users values."""
    # Aggregating the data by the selected aggregation type and activity_month
    aggregation_df = df.groupby([aggregation_type, 'activity_month']).agg({'registered_users': 'sum'}).reset_index()

    # Pivoting the table to have the last 6 months as columns
    pivot_df = aggregation_df.pivot_table(index=aggregation_type, columns='activity_month', values='registered_users')

    # Select last six months dynamically
    pivot_df = pivot_df.iloc[:, -6:]
    
    return pivot_df

def plot_new_users_overview(df):
    st.write("### New Users - Overview by Activity Date")

    # Convert activity_date to datetime if not already
    df['activity_date'] = pd.to_datetime(df['activity_date'], errors='coerce')

    # Add new activity_month column for month-level aggregation
    df['activity_month'] = df['activity_date'].dt.to_period('M').dt.to_timestamp()

    # Filters with "No Filter" option
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))

        # New Date Range Filter
        date_range = col6.date_input("Date Range", [df['activity_date'].min(), df['activity_date'].max()])

        # Convert date_range to datetime to match activity_date format
        date_range = [pd.to_datetime(date) for date in date_range]

    # Filter DataFrame based on selected filters, excluding "No Filter" options
    filtered_df = df.copy()
    if segment != "No Filter":
        filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter":
        filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter":
        filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter":
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter":
        filtered_df = filtered_df[filtered_df['platform'] == platform]
    if date_range:
        filtered_df = filtered_df[(filtered_df['activity_date'] >= date_range[0]) & (filtered_df['activity_date'] <= date_range[1])]

    # Container for the six charts
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 1: Overall New Users vs. Activity Date
        overall_df = filtered_df.groupby('activity_date').agg({'registered_users': 'sum'}).reset_index()
        fig_overall = create_new_users_overview_chart(
            overall_df, 'activity_date', 'registered_users', None, "Overall New Users vs Activity Date"
        )
        col1.plotly_chart(fig_overall, use_container_width=True)

        # Chart 2: New Users by Segment (without legend)
        segment_df = filtered_df.groupby(['activity_date', 'segment']).agg({'registered_users': 'sum'}).reset_index()
        fig_segment = create_new_users_overview_chart(
            segment_df, 'activity_date', 'registered_users', 'segment', "New Users by Segment vs Activity Date", show_legend=False
        )
        col2.plotly_chart(fig_segment, use_container_width=True)

    # 2nd Row: New Users by Country and by Network
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 3: New Users by Country
        country_df = filtered_df.groupby(['activity_date', 'country']).agg({'registered_users': 'sum'}).reset_index()
        fig_country = create_new_users_overview_chart(
            country_df, 'activity_date', 'registered_users', 'country', "New Users by Country vs Activity Date"
        )
        col1.plotly_chart(fig_country, use_container_width=True)

        # Chart 4: New Users by Network
        network_df = filtered_df.groupby(['activity_date', 'network']).agg({'registered_users': 'sum'}).reset_index()
        fig_network = create_new_users_overview_chart(
            network_df, 'activity_date', 'registered_users', 'network', "New Users by Network vs Activity Date"
        )
        col2.plotly_chart(fig_network, use_container_width=True)

    # 3rd Row: New Users by Channel and by Platform
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 5: New Users by Channel
        channel_df = filtered_df.groupby(['activity_date', 'channel']).agg({'registered_users': 'sum'}).reset_index()
        fig_channel = create_new_users_overview_chart(
            channel_df, 'activity_date', 'registered_users', 'channel', "New Users by Channel vs Activity Date"
        )
        col1.plotly_chart(fig_channel, use_container_width=True)

        # Chart 6: New Users by Platform
        platform_df = filtered_df.groupby(['activity_date', 'platform']).agg({'registered_users': 'sum'}).reset_index()
        fig_platform = create_new_users_overview_chart(
            platform_df, 'activity_date', 'registered_users', 'platform', "New Users by Platform vs Activity Date"
        )
        col2.plotly_chart(fig_platform, use_container_width=True)

    # Aggregated New Users Table
    with st.container():
        st.write("### Aggregated New Users Table")

        # Filter for the last six months of data based on activity_month
        last_6_months = filtered_df['activity_month'].dropna().sort_values().unique()[-6:]
        new_users_table_df = filtered_df[filtered_df['activity_month'].isin(last_6_months)]
        
        # Aggregation level selection
        aggregation_type = st.selectbox("Select Level of Aggregation", ['segment', 'country', 'network', 'channel', 'platform'])
        
        # Generate and display table
        aggregation_table = create_new_users_overview_table(new_users_table_df, aggregation_type)
        st.dataframe(aggregation_table)




#-----------------------------------------------------------------------------------------------------------------------
#----------------Monetization & Revenue---------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
        
def create_arpu_overview_chart(df, x_col, y_col, color_col, title, show_legend=True):
    """Helper function to create ARPU charts."""
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    if not show_legend:
        fig.update_layout(showlegend=False)
    elif show_legend:
        fig.update_layout(
            legend=dict(
                orientation="h",  
                yanchor="top",    
                y=-0.2,           
                xanchor="center", 
                x=0.5             
            )
        )
    return fig

def create_arpu_overview_table(df, aggregation_type):
    """Helper function to create a table based on aggregation type with ARPU values."""
    aggregation_df = df.groupby([aggregation_type, 'activity_month']).agg({'purchase_value': 'sum', 'active_users': 'sum'}).reset_index()
    aggregation_df['ARPU'] = aggregation_df['purchase_value'] / aggregation_df['active_users']
    pivot_df = aggregation_df.pivot_table(index=aggregation_type, columns='activity_month', values='ARPU')
    pivot_df = pivot_df.iloc[:, -6:]  # Last six months dynamically
    return pivot_df

def plot_arpu_overview(df):
    st.write("### ARPU - Overview by Activity Date")
    df['activity_date'] = pd.to_datetime(df['activity_date'], errors='coerce')
    df['activity_month'] = df['activity_date'].dt.to_period('M').dt.to_timestamp()

    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))
        date_range = col6.date_input("Date Range", [df['activity_date'].min(), df['activity_date'].max()])
        date_range = [pd.to_datetime(date) for date in date_range]

        
    with st.container():
        col7, col8, col9 = st.columns(3)
        # New Account Age Filter
        account_age = col7.selectbox("Account Age", ["All", 0, 1, 7, 14, 30, 60, 90, 180, 365, 730])


    filtered_df = df.copy()
    if segment != "No Filter": filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter": filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter": filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter": filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter": filtered_df = filtered_df[filtered_df['platform'] == platform]
    if date_range: filtered_df = filtered_df[(filtered_df['activity_date'] >= date_range[0]) & (filtered_df['activity_date'] <= date_range[1])]
    if account_age != "All":
        filtered_df = filtered_df[filtered_df['account_age'] == account_age]

    with st.container():
        col1, col2 = st.columns(2)
        overall_df = filtered_df.groupby('activity_date').agg({'purchase_value': 'sum', 'active_users': 'sum'}).reset_index()
        overall_df['ARPU'] = overall_df['purchase_value'] / overall_df['active_users']
        fig_overall = create_arpu_overview_chart(overall_df, 'activity_date', 'ARPU', None, "Overall Avg ARPU vs Activity Date")
        col1.plotly_chart(fig_overall, use_container_width=True)

        segment_df = filtered_df.groupby(['activity_date', 'segment']).agg({'purchase_value': 'sum', 'active_users': 'sum'}).reset_index()
        segment_df['ARPU'] = segment_df['purchase_value'] / segment_df['active_users']
        fig_segment = create_arpu_overview_chart(segment_df, 'activity_date', 'ARPU', 'segment', "ARPU by Segment vs Activity Date", show_legend=False)
        col2.plotly_chart(fig_segment, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        country_df = filtered_df.groupby(['activity_date', 'country']).agg({'purchase_value': 'sum', 'active_users': 'sum'}).reset_index()
        country_df['ARPU'] = country_df['purchase_value'] / country_df['active_users']
        fig_country = create_arpu_overview_chart(country_df, 'activity_date', 'ARPU', 'country', "ARPU by Country vs Activity Date")
        col1.plotly_chart(fig_country, use_container_width=True)

        network_df = filtered_df.groupby(['activity_date', 'network']).agg({'purchase_value': 'sum', 'active_users': 'sum'}).reset_index()
        network_df['ARPU'] = network_df['purchase_value'] / network_df['active_users']
        fig_network = create_arpu_overview_chart(network_df, 'activity_date', 'ARPU', 'network', "ARPU by Network vs Activity Date")
        col2.plotly_chart(fig_network, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        channel_df = filtered_df.groupby(['activity_date', 'channel']).agg({'purchase_value': 'sum', 'active_users': 'sum'}).reset_index()
        channel_df['ARPU'] = channel_df['purchase_value'] / channel_df['active_users']
        fig_channel = create_arpu_overview_chart(channel_df, 'activity_date', 'ARPU', 'channel', "ARPU by Channel vs Activity Date")
        col1.plotly_chart(fig_channel, use_container_width=True)

        platform_df = filtered_df.groupby(['activity_date', 'platform']).agg({'purchase_value': 'sum', 'active_users': 'sum'}).reset_index()
        platform_df['ARPU'] = platform_df['purchase_value'] / platform_df['active_users']
        fig_platform = create_arpu_overview_chart(platform_df, 'activity_date', 'ARPU', 'platform', "ARPU by Platform vs Activity Date")
        col2.plotly_chart(fig_platform, use_container_width=True)

    with st.container():
        st.write("### Aggregated ARPU Table")
        last_6_months = filtered_df['activity_month'].dropna().sort_values().unique()[-6:]
        arpu_table_df = filtered_df[filtered_df['activity_month'].isin(last_6_months)]
        
        aggregation_type = st.selectbox("Select Level of Aggregation", ['segment', 'country', 'network', 'channel', 'platform'])
        
        aggregation_table = create_arpu_overview_table(arpu_table_df, aggregation_type)
        st.dataframe(aggregation_table)

#-----------------------------------------------------------------------------------------------------------------------
def create_arpu_chart(df, x_col, y_col, color_col, title, show_legend=True):
    """Helper function to create ARPU charts."""
    
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title)
    
    # Manage legend display
    if not show_legend:
        fig.update_layout(showlegend=False)
    elif show_legend:
        fig.update_layout(
            legend=dict(
                orientation="h",  
                yanchor="top",    
                y=-0.2,           
                xanchor="center", 
                x=0.5             
            )
        )
    return fig

def create_arpu_table(df, aggregation_type):
    """Helper function to create a table based on aggregation type with ARPU values."""
    # Aggregate sums of active_users and purchase_value first, then calculate ARPU
    aggregation_df = df.groupby([aggregation_type, 'account_age']).agg({
        'purchase_value': 'sum',
        'active_users': 'sum'
    }).reset_index()
    
    # Calculate ARPU
    aggregation_df['arpu'] = aggregation_df['purchase_value'] / aggregation_df['active_users']
    
    # Pivot table to display ARPU by account age
    pivot_df = aggregation_df.pivot_table(index=aggregation_type, columns='account_age', values='arpu')
    pivot_df.columns = ['D1', 'D7', 'D14', 'D30', 'D90', 'D120', 'D180', 'D365', 'D540', 'D730']
    return pivot_df

def plot_arpu_cohort_view(df):
    st.write("### ARPU - Cohort View by Account Age")

    # Filters with "No Filter" option
    df.loc[df['cohort_date'] != df['activity_date'], 'registered_users'] = 0

    df['total_users'] = df['registered_users']+df['active_users']

    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))

    # Filter DataFrame based on selected filters
    filtered_df = df.copy()
    if segment != "No Filter":
        filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter":
        filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter":
        filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter":
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter":
        filtered_df = filtered_df[filtered_df['platform'] == platform]

    # Aggregate sums of purchase_value and total_users, then calculate ARPU
    filtered_df = filtered_df.groupby(['account_age']).agg({
        'purchase_value': 'sum',
        'total_users': 'sum'
    }).reset_index()
    filtered_df['arpu'] = filtered_df['purchase_value'] / filtered_df['total_users']

    st.dataframe(filtered_df)

    # Plot ARPU charts
    with st.container():
        col1, col2 = st.columns(2)

        # Chart 1: Overall ARPU vs. Account Age
        fig_overall = create_arpu_chart(filtered_df, 'account_age', 'arpu', None, "Overall Avg ARPU vs Account Age")
        col1.plotly_chart(fig_overall, use_container_width=True)


        # Chart 2: ARPU by Segment
        segment_df = df.groupby(['account_age', 'segment']).agg({
            'purchase_value': 'sum',
            'total_users': 'sum'
        }).reset_index()
        segment_df['arpu'] = segment_df['purchase_value'] / segment_df['total_users']
        fig_segment = create_arpu_chart(segment_df, 'account_age', 'arpu', 'segment', "ARPU by Segment vs Account Age", show_legend=False)
        col2.plotly_chart(fig_segment, use_container_width=True)

    # Row 2: ARPU by Country and Network
    with st.container():
        col1, col2 = st.columns(2)
        country_df = df.groupby(['account_age', 'country']).agg({
            'purchase_value': 'sum',
            'total_users': 'sum'
        }).reset_index()
        country_df['arpu'] = country_df['purchase_value'] / country_df['total_users']
        fig_country = create_arpu_chart(country_df, 'account_age', 'arpu', 'country', "ARPU by Country vs Account Age")
        col1.plotly_chart(fig_country, use_container_width=True)

        network_df = df.groupby(['account_age', 'network']).agg({
            'purchase_value': 'sum',
            'total_users': 'sum'
        }).reset_index()
        network_df['arpu'] = network_df['purchase_value'] / network_df['total_users']
        fig_network = create_arpu_chart(network_df, 'account_age', 'arpu', 'network', "ARPU by Network vs Account Age")
        col2.plotly_chart(fig_network, use_container_width=True)

    # Row 3: ARPU by Channel and Platform
    with st.container():
        col1, col2 = st.columns(2)
        channel_df = df.groupby(['account_age', 'channel']).agg({
            'purchase_value': 'sum',
            'total_users': 'sum'
        }).reset_index()
        channel_df['arpu'] = channel_df['purchase_value'] / channel_df['total_users']
        fig_channel = create_arpu_chart(channel_df, 'account_age', 'arpu', 'channel', "ARPU by Channel vs Account Age")
        col1.plotly_chart(fig_channel, use_container_width=True)

        platform_df = df.groupby(['account_age', 'platform']).agg({
            'purchase_value': 'sum',
            'total_users': 'sum'
        }).reset_index()
        platform_df['arpu'] = platform_df['purchase_value'] / platform_df['total_users']
        fig_platform = create_arpu_chart(platform_df, 'account_age', 'arpu', 'platform', "ARPU by Platform vs Account Age")
        col2.plotly_chart(fig_platform, use_container_width=True)

    # Aggregated ARPU Table
    with st.container():
        st.write("### Aggregated ARPU Table")
        ARPU_table_df = df[df['account_age'].isin([1, 7, 14, 30, 90, 120, 180, 365, 540, 730])]
        aggregation_type = st.selectbox("Select Level of Aggregation", ['segment', 'country', 'network', 'channel', 'platform'])
        aggregation_table = create_arpu_table(ARPU_table_df, aggregation_type)
        st.dataframe(aggregation_table)

#-----------------------------------------------------------------------------------------------------------------------

def plot_arpu_account_age_trends(df):
    st.write("### ARPU - Account Age Trends")

    # First two containers for filters
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        date_range = col1.date_input("Date Range", [])
        segment = col2.selectbox("Segment", df['segment'].unique())
        country = col3.selectbox("Country", df['country'].unique())
        network = col4.selectbox("Network", df['network'].unique())

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        channel = col1.selectbox("Channel", df['channel'].unique())
        platform = col2.selectbox("Platform", df['platform'].unique())
        account_age_filter = col3.multiselect("Account Age", [1, 7, 30, 90, 180, 365, 730], default=[1, 7, 30, 90])

    # Filter DataFrame based on selected filters
    filtered_df = df[
        (df['segment'] == segment) &
        (df['country'] == country) &
        (df['network'] == network) &
        (df['channel'] == channel) &
        (df['platform'] == platform)
    ]

    # Aggregate sums for active users and purchase values by cohort_date and account_age
    filtered_df['sum_active_users'] = filtered_df.groupby(['cohort_date', 'account_age'])['active_users'].transform('sum')
    filtered_df['sum_purchase_value'] = filtered_df.groupby(['cohort_date', 'account_age'])['purchase_value'].transform('sum')

    # Calculate ARPU for each record as the ratio of total purchase value to active users
    filtered_df['arpu'] = filtered_df['sum_purchase_value'] / filtered_df['sum_active_users']

    # Filter for selected account ages
    filtered_df = filtered_df[filtered_df['account_age'].isin(account_age_filter)]

    # Plotting ARPU line chart by account age
    fig = px.line(
        filtered_df,
        x='activity_date',
        y='arpu',
        color='account_age',
        labels={'arpu': 'ARPU', 'activity_date': 'Activity Date'},
        title="ARPU by Account Age"
    )
    
    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # Average ARPU calculation for last six months
    with st.container():
        last_date = pd.to_datetime(filtered_df['activity_date'].max())
        six_months_prior = last_date - pd.DateOffset(months=6)
        last_six_months_df = filtered_df[filtered_df['activity_date'] >= six_months_prior]

        # Calculate average ARPU by account age per month
        last_six_months_df['month'] = last_six_months_df['activity_date'].dt.to_period('M')
        avg_arpu_df = last_six_months_df.groupby(['account_age', 'month'])['arpu'].mean().unstack().fillna(0)
        
        # Display table
        st.write("### Average ARPU by Account Age for Last 6 Months")
        st.dataframe(avg_arpu_df, use_container_width=True)


def plot_arpu_cohort_trends(df):
    st.write("### ARPU - Cohort View")

    # First two containers for filters
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        date_range = col1.date_input("Date Range", [])
        segment = col2.selectbox("Segment", df['segment'].unique())
        country = col3.selectbox("Country", df['country'].unique())
        network = col4.selectbox("Network", df['network'].unique())

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        channel = col1.selectbox("Channel", df['channel'].unique())
        platform = col2.selectbox("Platform", df['platform'].unique())
        account_age_filter = col3.multiselect("Account Age", [1, 7, 30, 90, 180, 365, 730], default=[1, 7, 30, 90])

    # Filter DataFrame based on selected filters
    filtered_df = df[
        (df['segment'] == segment) &
        (df['country'] == country) &
        (df['network'] == network) &
        (df['channel'] == channel) &
        (df['platform'] == platform)
    ]

    # Aggregate sums for active users and purchase values
    filtered_df = filtered_df.sort_values('account_age')
    filtered_df['sum_active_users'] = filtered_df.groupby(['cohort_date', 'account_age'])['active_users'].transform('sum')
    filtered_df['sum_purchase_value'] = filtered_df.groupby(['cohort_date', 'account_age'])['purchase_value'].transform('sum')

    # Calculate ARPU for each cohort
    filtered_df['arpu'] = filtered_df['sum_purchase_value'] / filtered_df['sum_active_users']

    # Filter for selected account ages
    filtered_df = filtered_df[filtered_df['account_age'].isin(account_age_filter)]

    # Display preview of filtered data
    st.write("### Filtered Data Preview")
    st.dataframe(filtered_df.head(), use_container_width=True)

    # Plotting ARPU line chart by cohort date
    fig = px.line(
        filtered_df,
        x='account_age',
        y='arpu',
        color='cohort_date',
        labels={'arpu': 'ARPU', 'account_age': 'Account Age'},
        title="ARPU by Cohort Date"
    )
    
    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # ARPU table by cohort date and account age for last six months
    with st.container():
        last_date = pd.to_datetime(filtered_df['activity_date'].max())
        six_months_prior = last_date - pd.DateOffset(months=6)
        last_six_months_df = filtered_df[filtered_df['activity_date'] >= six_months_prior]

        # Pivot table to show ARPU by cohort date and account age
        arpu_pivot_df = last_six_months_df.pivot_table(
            index='cohort_date',
            columns='account_age',
            values='arpu',
            aggfunc='mean'
        ).reindex(columns=[1, 7, 30, 90, 180, 365, 730], fill_value=0)  # Ensure column order and fill missing values

        # Display table
        st.write("### ARPU by Cohort Date and Account Age")
        st.dataframe(arpu_pivot_df, use_container_width=True)


#-----------------------------------------------------------------------------------------------------------------------


def plot_clv_account_age_trends(df):
    st.write("### Customer Lifetime Value (CLV) - Account Age Trends")

    # First container for main filters with "No Filter" as the default option
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        segment = col1.selectbox("Segment", ["No Filter"] + list(df['segment'].unique()))
        country = col2.selectbox("Country", ["No Filter"] + list(df['country'].unique()))
        network = col3.selectbox("Network", ["No Filter"] + list(df['network'].unique()))
        channel = col4.selectbox("Channel", ["No Filter"] + list(df['channel'].unique()))
        platform = col5.selectbox("Platform", ["No Filter"] + list(df['platform'].unique()))
        date_range = col6.date_input("Date Range", [df['activity_date'].min(), df['activity_date'].max()])
        date_range = [pd.to_datetime(date) for date in date_range]

    with st.container():
        col7, col8, col9 = st.columns(3)
        # New Account Age Filter, with 'All' as an option
        account_age = col7.selectbox("Account Age", ["All", 0, 1, 7, 14, 30, 60, 90, 180, 365, 730])

    # Apply filters based on selected values; ignore "No Filter" selections
    filtered_df = df.copy()

    if segment != "No Filter": filtered_df = filtered_df[filtered_df['segment'] == segment]
    if country != "No Filter": filtered_df = filtered_df[filtered_df['country'] == country]
    if network != "No Filter": filtered_df = filtered_df[filtered_df['network'] == network]
    if channel != "No Filter": filtered_df = filtered_df[filtered_df['channel'] == channel]
    if platform != "No Filter": filtered_df = filtered_df[filtered_df['platform'] == platform]
    if date_range: filtered_df = filtered_df[(filtered_df['activity_date'] >= date_range[0]) & (filtered_df['activity_date'] <= date_range[1])]
    if account_age != "All":
        filtered_df = filtered_df[filtered_df['account_age'] == account_age]

    # Sort by cohort_date and account_age, calculate cumulative purchase value as CLV up to selected account_age
    filtered_df = filtered_df.sort_values(by=['cohort_date', 'account_age'])
    filtered_df['cumulative_purchase_value'] = filtered_df.groupby(['cohort_date', 'account_age'])['purchase_value'].cumsum()

    # Calculate weighted average CLV
    filtered_df['clv'] = filtered_df['cumulative_purchase_value'] / filtered_df['total_users']

    # Filter for cumulative values up to the selected account age
    filtered_df = filtered_df[filtered_df['account_age'] <= account_age if account_age != "All" else True]

    # Plotting CLV line chart by account age
    fig = px.line(
        filtered_df,
        x='activity_date',
        y='clv',
        color='account_age',
        labels={'clv': 'CLV', 'activity_date': 'Activity Date'},
        title=f"Customer Lifetime Value (CLV) up to Account Age {account_age}"
    )

    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # Average CLV calculation for last six months for selected account ages
    with st.container():
        last_date = pd.to_datetime(filtered_df['activity_date'].max())
        six_months_prior = last_date - pd.DateOffset(months=6)
        last_six_months_df = filtered_df[filtered_df['activity_date'] >= six_months_prior]

        # Calculate average CLV for last six months with account ages as rows and months as columns
        last_six_months_df['month'] = last_six_months_df['activity_date'].dt.to_period('M')
        avg_clv_df = last_six_months_df.pivot_table(
            index='account_age',
            columns='month',
            values='clv',
            aggfunc='mean'
        ).reindex([1, 7, 30]).fillna(0)  # Rows ordered by specified account ages; NaNs filled with 0

        # Display aggregated table
        st.write("### Average CLV for Last 6 Months by Selected Account Ages")
        st.dataframe(avg_clv_df, use_container_width=True)


def plot_clv_cohort_trends(df):
    st.write("### Customer Lifetime Value (CLV) - Cohort View")

    # First two containers for filters
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        date_range = col1.date_input("Date Range", [])
        segment = col2.selectbox("Segment", df['segment'].unique())
        country = col3.selectbox("Country", df['country'].unique())
        network = col4.selectbox("Network", df['network'].unique())

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        channel = col1.selectbox("Channel", df['channel'].unique())
        platform = col2.selectbox("Platform", df['platform'].unique())
        
        # Single-select dropdown for Account Age, default set to 1
        account_age = col3.selectbox("Account Age", options=[1, 7, 30, 90, 180, 365], index=0)

    # Filter DataFrame based on selected filters
    filtered_df = df[
        (df['segment'] == segment) &
        (df['country'] == country) &
        (df['network'] == network) &
        (df['channel'] == channel) &
        (df['platform'] == platform)
    ]

    # Sort and calculate cumulative purchase value as CLV up to selected account age
    filtered_df = filtered_df.sort_values(by=['cohort_date', 'account_age'])
    filtered_df['cumulative_purchase_value'] = filtered_df.groupby(['cohort_date', 'account_age'])['purchase_value'].cumsum()

    # Calculate CLV using total users as the weighted average
    filtered_df['clv'] = filtered_df['cumulative_purchase_value'] / filtered_df['total_users']

    # Filter for cumulative values up to the selected account age
    filtered_df = filtered_df[filtered_df['account_age'] <= account_age]

    # Display preview of filtered data
    st.write("### Filtered Data Preview")
    st.dataframe(filtered_df.head(), use_container_width=True)

    # Plotting CLV line chart by cohort date
    fig = px.line(
        filtered_df,
        x='account_age',
        y='clv',
        color='cohort_date',
        labels={'clv': 'CLV', 'account_age': 'Account Age'},
        title=f"Customer Lifetime Value (CLV) by Cohort Date up to Account Age {account_age}"
    )

    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # CLV table by cohort date for last six months
    with st.container():
        last_date = pd.to_datetime(filtered_df['activity_date'].max())
        six_months_prior = last_date - pd.DateOffset(months=6)
        last_six_months_df = filtered_df[filtered_df['activity_date'] >= six_months_prior]

        # Pivot table to show CLV by cohort date for selected account age
        clv_pivot_df = last_six_months_df.pivot_table(
            index='cohort_date',
            values='clv',
            aggfunc='mean'
        ).fillna(0)

        # Display table
        st.write("### CLV by Cohort Date for Last 6 Months at Selected Account Age")
        st.dataframe(clv_pivot_df, use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------

def plot_clv_overview():
    print("ABC")

def plot_clv_cohort_view():
    print("ABC")

def plot_revenue_cohort_contribution():
    print("ABC")

def plot_revenue_overview():
    print("ABC")


#-----------------------------------------------------------------------------------------------------------------------
        

def plot_retention_cohort_view():
    print("ABC")

def plot_retention_account_age_trends():
    print("ABC")

def plot_retention_cohort_trends():
    print("ABC")







def plot_active_users_cohort_contribution():
    print("ABC")

def plot_active_users_overview():
    print("ABC")

def plot_retention_overview():
    print("ABC")




##Retention---------------------------------------------------------------------------------





# Add more plotting functions as needed
def plot_revenue_trends():
    st.write("### Revenue Trends")
    # Placeholder for Revenue Trends chart
    st.line_chart(np.random.randn(100).cumsum())


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

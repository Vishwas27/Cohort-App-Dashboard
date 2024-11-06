import streamlit as st
import pandas as pd
import numpy as np
import altair as alt




# Define layout for "User Acquisition Strategy" tab
def user_acquisition_strategy():
    st.header("Target")
    st.subheader("Choose which input assumptions you will provide, and we will calculate the rest.")
    
    # Layout with radio buttons
    col1, col2 = st.columns(2)
    with col1:
        target_option = st.radio(
            "Select Target Option",
            ["Current Payback", "Target Payback", "Target New Users", "Target Spend"],
            index=0,
            help="Select the type of target calculation you want."
        )
    with col2:
        st.markdown("### Target Options")
        if target_option == "Current Payback":
            st.info("Calculate marketing spend based on current payback per segment.")
        elif target_option == "Target Payback":
            st.info("Calculate marketing spend required to reach a target global payback.")
        elif target_option == "Target New Users":
            st.info("Calculate marketing spend required to reach your user acquisition milestones and the required payback.")
        elif target_option == "Target Spend":
            st.info("Calculate new users and resulting payback from the provided marketing spend.")

    # Additional input fields
    st.markdown("---")
    st.subheader("Target Payback")
    st.text_input("Target global payback days. CAC will be set to CLV at this payback.", value="365 days")

    st.subheader("Payback Method")
    st.selectbox("Select Payback Method", ["BLENDED", "PAID"], help="Select Blended or Paid for payback method.")

    st.subheader("Paid User Split")
    st.slider("Choose the percentage of users that should be paid vs organic", 0, 100, 50)

    st.button("Add Segment Override", key="segment_override")

# Define layout for "Price Volume Relationship" tab
def price_volume_relationship():
    st.header("Price Volume Relationship")
    st.write("Define the price and volume relationship details here.")
    # Additional placeholders for the Price Volume Relationship content
    # Customize further as per requirements
    # Section: Price Volume Lookback
    with st.container():
        
        # Create two columns within the container
        col1, col2 = st.columns(2)

        # Column 1: Line chart
        with col1:
            
            # Generate example data for line chart
            line_data = pd.DataFrame({
                'x': np.linspace(0, 10, 100),
                'y': np.sin(np.linspace(0, 10, 100))
            })
            
            # Plot the line chart using Altair
            line_chart = alt.Chart(line_data).mark_line(color='blue').encode(
                x='x',
                y='y'
            ).properties(
                width=300,
                height=300
            )
            
            st.altair_chart(line_chart)

        # Column 2: Hill function chart
        with col2:
            
            # Generate example data for Hill function chart
            x_vals = np.linspace(0.1, 10, 100)
            hill_data = pd.DataFrame({
                'x': x_vals,
                'y': 1 / (1 + (0.5 / x_vals)**2)  # Example Hill function with coefficient 2
            })
            
            # Plot the Hill function chart using Altair
            hill_chart = alt.Chart(hill_data).mark_line(color='red').encode(
                x='x',
                y='y'
            ).properties(
                width=300,
                height=300
            )
            
            st.altair_chart(hill_chart)


    st.subheader("Price Volume Lookback")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.text_input("Price Volume Lookback", value="last 30 days")
    with col2:
        st.markdown("")

    st.markdown("---")

    # Section: CPI Sensitivity to Spend
    st.subheader("CPI Sensitivity to Spend")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.text_input("CPI Sensitivity (%)", value="50%")
    with col2:
        st.slider("Adjust CPI Sensitivity", 0, 100, 50, help="Adjust the sensitivity of CPI to spend")
    
    st.button("Add Segment Override", key="cpi_segment_override")

    st.markdown("---")

    # Section: Marketing Fatigue
    st.subheader("Marketing Fatigue")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.text_input("Marketing Fatigue (%)", value="50%")
    with col2:
        st.slider("Adjust Marketing Fatigue", 0, 100, 50, help="Adjust the level of marketing fatigue")

    st.button("Add Segment Override", key="fatigue_segment_override")

    st.markdown("---")

    # Section: Averages from PV Lookback
    st.subheader("Averages from PV Lookback")
    st.write(" ")
    avg_col1, avg_col2 = st.columns(2)
    with avg_col1:
        st.markdown("**Spend**")
        st.write("365,765")
        
        st.markdown("**CPI**")
        st.write("15.45")
        
        st.markdown("**New Users**")
        st.write("23,088")
        
        st.markdown("**CLV @ Payback**")
        st.write("15.26")
        
        st.markdown("**Payback (days)**")
        st.write("354")
    
    # Section: PV Model
    with avg_col2:
        st.subheader("PV Model (y = m*x + c)")
        st.markdown("**c (intercept)**")
        st.write("9.85")
        
        st.markdown("**m (slope)**")
        st.write("1.65e-5")

# Define layout for "Spend Optimization" tab

def spend_optimization():
    st.header("Spend Optimization")
    st.write("Analyze the marketing spend across different channels and optimize allocations.")

    # First Container: Line Chart
    with st.container():
        st.subheader("Random Line Chart")
        
        # Generate random data for line chart
        line_data = pd.DataFrame({
            'x': np.arange(1, 101),
            'y': np.random.randn(100).cumsum()
        })
        
        # Plot line chart
        line_chart = alt.Chart(line_data).mark_line(color='blue').encode(
            x='x',
            y='y'
        ).properties(
            width=600,
            height=300
        )
        
        st.altair_chart(line_chart, use_container_width=True)

    # Second Container: Marketing Spend Table
    with st.container():
        st.subheader("Channel-Level Marketing Spend Data")
        
        # Generate random data for marketing spend across channels
        channels = ['Facebook', 'Instagram', 'Google', 'YouTube']
        actual_spend = np.random.randint(5000, 15000, len(channels))
        proposed_spend = np.random.randint(6000, 16000, len(channels))
        actual_users = np.random.randint(100, 500, len(channels))
        projected_users = np.random.randint(150, 600, len(channels))
        
        spend_data = pd.DataFrame({
            'Channel': channels,
            'Actual Marketing Spend': actual_spend,
            'Proposed Spend': proposed_spend,
            'Actual Users': actual_users,
            'Projected Users': projected_users
        })
        
        st.table(spend_data)

    # Third Container: Three Columns with Pie Charts and Text
    with st.container():
        st.subheader("Spend Allocation Analysis")

        col1, col2, col3 = st.columns(3)

        # Column 1: Pie Chart for Actual Spend
        with col1:
            st.subheader("Actual Marketing Spend Distribution")
            pie_chart_actual = alt.Chart(spend_data).mark_arc().encode(
                theta='Actual Marketing Spend',
                color='Channel',
                tooltip=['Channel', 'Actual Marketing Spend']
            ).properties(
                width=200,
                height=200
            )
            st.altair_chart(pie_chart_actual)

        # Column 2: Pie Chart for Proposed Spend
        with col2:
            st.subheader("Proposed Marketing Spend Distribution")
            pie_chart_proposed = alt.Chart(spend_data).mark_arc().encode(
                theta='Proposed Spend',
                color='Channel',
                tooltip=['Channel', 'Proposed Spend']
            ).properties(
                width=200,
                height=200
            )
            st.altair_chart(pie_chart_proposed)

        # Column 3: Header and Text
        with col3:
            st.subheader("Insights")
            st.write("The proposed spend distribution suggests higher investment in certain channels.")
            st.write("Consider aligning the spend to optimize user acquisition and engagement.")

# Main function to render the User Acquisition page with tabs
def run():
    st.header("User Acquisition")
    tab1, tab2, tab3 = st.tabs(["User Acquisition Strategy", "Price Volume Relationship", "Spend Optimization"])
    
    with tab1:
        user_acquisition_strategy()
    
    with tab2:
        price_volume_relationship()
    
    with tab3:
        spend_optimization()

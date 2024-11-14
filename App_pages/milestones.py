import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# Function to add a milestone in a dialog
@st.dialog("Add New Milestone")
def add_milestone():
    st.header("Add New Milestone")
    feature_type = st.selectbox("Feature Type", ["Retention", "Monetisation"])
    start_date = st.date_input("Start Date", value=datetime.today())
    segment = st.text_input("Segment")
    value = st.number_input("Value", min_value=0.0, step=1.0)

    if st.button("Add Milestone", key="add_milestone_button"):
        new_entry = pd.DataFrame({
            "Feature Type": [feature_type],
            "Start Date": [start_date],
            "Segment": [segment],
            "Value": [value]
        })
        if "milestones_data" not in st.session_state:
            st.session_state["milestones_data"] = new_entry
        else:
            st.session_state["milestones_data"] = pd.concat([st.session_state["milestones_data"], new_entry], ignore_index=True)
        
        st.success("Milestone added successfully!")
        st.session_state["show_dialog"] = False  # Close the dialog
        st.session_state["refresh_data"] = True  # Set a flag to refresh data

# Function to display all milestones
def all_milestones():
    st.subheader("All Added Milestones")
    if "milestones_data" in st.session_state:
        st.table(st.session_state["milestones_data"])
    else:
        st.write("No milestones added yet.")

# Function for Retention tab content
def retention_tab():
    st.subheader("Retention Features")
    # Retention Curve
    with st.container():
        st.subheader("Retention Curve")
        retention_data = pd.DataFrame({
            'Days': np.arange(1, 31),
            'Retention Rate (%)': np.random.uniform(40, 80, 30)
        })
        retention_chart = alt.Chart(retention_data).mark_line(color="green").encode(
            x="Days",
            y="Retention Rate (%)"
        )
        st.altair_chart(retention_chart, use_container_width=True)

    # Past Retention Features
    with st.container():
        st.subheader("Past Retention Features")
        if "milestones_data" in st.session_state:
            retention_data = st.session_state["milestones_data"][st.session_state["milestones_data"]["Feature Type"] == "Retention"]
            st.table(retention_data)
        else:
            st.write("No retention features added yet.")

# Function for Monetisation tab content
def monetisation_tab():
    st.subheader("Monetisation Features")
    # Monetisation Curve
    with st.container():
        st.subheader("Monetisation Curve")
        monetisation_data = pd.DataFrame({
            'Days': np.arange(1, 31),
            'Monetisation Rate (%)': np.random.uniform(5, 20, 30)
        })
        monetisation_chart = alt.Chart(monetisation_data).mark_line(color="blue").encode(
            x="Days",
            y="Monetisation Rate (%)"
        )
        st.altair_chart(monetisation_chart, use_container_width=True)

    # Past Monetisation Features
    with st.container():
        st.subheader("Past Monetisation Features")
        if "milestones_data" in st.session_state:
            monetisation_data = st.session_state["milestones_data"][st.session_state["milestones_data"]["Feature Type"] == "Monetisation"]
            st.table(monetisation_data)
        else:
            st.write("No monetisation features added yet.")

# Main function to render the Milestones page
def run(df):
    st.header("Milestones")
    
     # Arrange "Add Milestone" and "Refresh List" buttons in the same row
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Add Milestone", key="open_dialog_button"):
            st.session_state["show_dialog"] = True
    with col2:
        if st.button("Refresh List", key="refresh_button"):
            st.session_state["refresh_data"] = True  # Set the refresh flag to reload the milestones

    # Display dialog if "show_dialog" is True
    if st.session_state.get("show_dialog", False):
        add_milestone()

    # Check for refresh_data flag to trigger rerender
    if st.session_state.get("refresh_data", False):
        st.session_state["refresh_data"] = False  # Reset the flag


    # Tabs for Milestones
    tab1, tab2, tab3 = st.tabs(["All Milestones", "Retention", "Monetisation"])

    with tab1:
        all_milestones()
    with tab2:
        retention_tab()
    with tab3:
        monetisation_tab()

# Run the application
if __name__ == "__main__":
    # Initialize session state if needed
    if "show_dialog" not in st.session_state:
        st.session_state["show_dialog"] = False
    if "milestones_data" not in st.session_state:
        st.session_state["milestones_data"] = pd.DataFrame(columns=["Feature Type", "Start Date", "Segment", "Value"])
    if "refresh_data" not in st.session_state:
        st.session_state["refresh_data"] = False

    run()

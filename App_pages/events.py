import streamlit as st
import pandas as pd

from datetime import datetime, timedelta
import numpy as np
import altair as alt
from datetime import datetime

# Function to add a event in a dialog
@st.dialog("Add New event")


def add_event():
    st.header("Add New event")
    feature_type = st.selectbox("Feature Type", ["Retention", "Monetisation"])
    start_date = st.date_input("Start Date", value=datetime.today())
    segment = st.text_input("Segment")
    value = st.number_input("Value", min_value=0.0, step=1.0)

    if st.button("Add event", key="add_event_button"):
        new_entry = pd.DataFrame({
            "Feature Type": [feature_type],
            "Start Date": [start_date],
            "Segment": [segment],
            "Value": [value]
        })
        if "events_data" not in st.session_state:
            st.session_state["events_data"] = new_entry
        else:
            st.session_state["events_data"] = pd.concat([st.session_state["events_data"], new_entry], ignore_index=True)
        
        st.success("event added successfully!")
        st.session_state["show_dialog"] = False  # Close the dialog
        st.session_state["refresh_data"] = True  # Set a flag to refresh data

# Function to display all events

# Generate random event data
def generate_random_events(num_events=20):
    np.random.seed(42)  # For reproducibility
    event_types = ["Season Pass", "Other Event Type"]
    segments = ["GLOBAL", "Other Segment"]
    start_date = datetime(2022, 1, 1)
    
    data = []
    for _ in range(num_events):
        days_offset = np.random.randint(0, 365)
        date_range_start = start_date + timedelta(days=days_offset)
        date_range_end = date_range_start + timedelta(days=np.random.randint(5, 10))
        data.append({
            "Date Range": f"{date_range_start.date()} - {date_range_end.date()}",
            "Event Type": np.random.choice(event_types),
            "Segments": np.random.choice(segments),
            "Event Name": f"Event {_+1}"
        })
    
    return pd.DataFrame(data)

# Function to display past events with filters
def past_events():
    st.subheader("All Added Events")
    
    # Generate random event data
    events_df = generate_random_events()
    
    # Create a filter container
    with st.container():
        st.write("Filter by:")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Set a default date range based on the available data
        min_date = datetime(2022, 1, 1)
        max_date = min_date + timedelta(days=365)
        
        # Date range filter
        with col1:
            date_range = st.date_input("Date Range", value=(min_date, max_date))
        
        # Event type filter
        with col2:
            event_type = st.selectbox("Event Type", ["All"] + list(events_df["Event Type"].unique()))
        
        # Segments filter
        with col3:
            segments = st.selectbox("Segments", ["All"] + list(events_df["Segments"].unique()))
        
        # Event name filter
        with col4:
            event_name = st.text_input("Event Name")
    
    # Filter data based on user input
    filtered_df = events_df.copy()
    
    if date_range:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df["Date Range"].str.split(" - ").str[0]) >= start_date) &
            (pd.to_datetime(filtered_df["Date Range"].str.split(" - ").str[1]) <= end_date)
        ]
    if event_type != "All":
        filtered_df = filtered_df[filtered_df["Event Type"] == event_type]
    if segments != "All":
        filtered_df = filtered_df[filtered_df["Segments"] == segments]
    if event_name:
        filtered_df = filtered_df[filtered_df["Event Name"].str.contains(event_name, case=False)]
    
    # Display filtered data
    st.table(filtered_df)

# Run the app

# Function for Retention tab content
def all_events():
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
        if "events_data" in st.session_state:
            retention_data = st.session_state["events_data"][st.session_state["events_data"]["Feature Type"] == "Retention"]
            st.table(retention_data)
        else:
            st.write("No retention features added yet.")

# Function for Monetisation tab content
def future_events():
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
        if "events_data" in st.session_state:
            monetisation_data = st.session_state["events_data"][st.session_state["events_data"]["Feature Type"] == "Monetisation"]
            st.table(monetisation_data)
        else:
            st.write("No monetisation features added yet.")

# Main function to render the events page
def run(df):
    st.header("events")
    
     # Arrange "Add event" and "Refresh List" buttons in the same row
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Add event", key="open_dialog_button"):
            st.session_state["show_dialog"] = True
    with col2:
        if st.button("Refresh List", key="refresh_button"):
            st.session_state["refresh_data"] = True  # Set the refresh flag to reload the events

    # Display dialog if "show_dialog" is True
    if st.session_state.get("show_dialog", False):
        add_event()

    # Check for refresh_data flag to trigger rerender
    if st.session_state.get("refresh_data", False):
        st.session_state["refresh_data"] = False  # Reset the flag


    # Tabs for events
    tab1, tab2, tab3 = st.tabs(["Past events", "Event Average Performance", "Future events"])

    with tab1:
        past_events()
    with tab2:
        all_events()
    with tab3:
        future_events()

# Run the application
if __name__ == "__main__":
    # Initialize session state if needed
    if "show_dialog" not in st.session_state:
        st.session_state["show_dialog"] = False
    if "events_data" not in st.session_state:
        st.session_state["events_data"] = pd.DataFrame(columns=["Feature Type", "Start Date", "Segment", "Value"])
    if "refresh_data" not in st.session_state:
        st.session_state["refresh_data"] = False

    run()

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from streamlit_elements import elements, mui, html
from App_pages import dashboard, reports, user_acquisition, milestones, events, overrides, settings, file_uploader_page

# Set up the dashboard layout and sidebar
st.set_page_config(page_title="RevUpp Dashboard", layout="wide")

# Sidebar title with custom styles for the background and text color
st.sidebar.markdown(
    "<div style='background-color: black; color: white; padding: 15px; font-size: 18px; text-align: center;'>REVUPP</div>",
    unsafe_allow_html=True
)

# Sidebar title
st.sidebar.title("REVUPP")

# Directly read the Parquet file from a specified location
file_path = "Synth_data/Synthetic_Format_Data.parquet"
df = pd.read_parquet(file_path)

# Optional: Set a default page if needed
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"  # Default page

# Sidebar options as buttons
if st.sidebar.button("Dashboard"):
    st.session_state.current_page = "Dashboard"
if st.sidebar.button("Reports"):
    st.session_state.current_page = "Reports"
if st.sidebar.button("File Uploader"):  # New page for file uploading
    st.session_state.current_page = "File Uploader"

st.sidebar.subheader("Scenarios")

if st.sidebar.button("User Acquisition"):
    st.session_state.current_page = "User Acquisition"
if st.sidebar.button("Milestones"):
    st.session_state.current_page = "Milestones"
if st.sidebar.button("Events"):
    st.session_state.current_page = "Events"
if st.sidebar.button("Overrides"):
    st.session_state.current_page = "Overrides"
if st.sidebar.button("Settings"):
    st.session_state.current_page = "Settings"

# Run the appropriate page based on the current_page state
if st.session_state.current_page == "Dashboard":
    dashboard.run(df)
elif st.session_state.current_page == "Reports":
    reports.run(df)
elif st.session_state.current_page == "File Uploader":
    file_uploader_page.run()  # No need to pass df here, as it will load a new file
elif st.session_state.current_page == "User Acquisition":
    user_acquisition.run(df)
elif st.session_state.current_page == "Milestones":
    milestones.run(df)
elif st.session_state.current_page == "Events":
    events.run(df)
elif st.session_state.current_page == "Overrides":
    overrides.run(df)
elif st.session_state.current_page == "Settings":
    settings.run()

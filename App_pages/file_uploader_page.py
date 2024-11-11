import streamlit as st
import pandas as pd

def run():
    # ----------------------- Page Title -----------------------
    st.header("File Uploader Page")

    # ----------------------- File Selection and Upload -----------------------
    with st.container():
        st.subheader("Upload a Parquet File")
        # File uploader widget for Parquet files
        uploaded_file = st.file_uploader("Choose a Parquet file", type=["parquet"])

    # ----------------------- Upload Status -----------------------
    with st.container():
        st.subheader("Upload Status")
        # Check if a file is uploaded and display status
        if uploaded_file is not None:
            st.success("File uploaded successfully!")
        else:
            st.info("Awaiting file upload...")

    # ----------------------- Data Preview -----------------------
    with st.container():
        st.subheader("Data Preview")
        # If file uploaded, load and display the first 10 rows of the file
        if uploaded_file is not None:
            try:
                # Load the Parquet file into a DataFrame
                df = pd.read_parquet(uploaded_file)
                # Display the first 10 rows
                st.dataframe(df.head(10))
            except Exception as e:
                st.error(f"Error loading file: {e}")

# Run the application
if __name__ == "__main__":
    run()

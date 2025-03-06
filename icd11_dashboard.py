import streamlit as st
import pandas as pd
from io import BytesIO

# Load dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("icd11_codes.csv")
        df["Parent_Code"] = df["Code"].apply(lambda x: x.rsplit(".", 1)[0] if "." in x else None)
        return df
    except FileNotFoundError:
        st.error("Error: The file 'icd11_codes.csv' was not found. Please upload it to your GitHub repository.")
        return pd.DataFrame(columns=["Code", "Title", "Parent_Code"])

df = load_data()

# Sidebar Search
st.sidebar.header("ICD-11 Disease Search")
search_query = st.sidebar.text_input("Search by Code or Title", "")

# Filter data based on search
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
else:
    filtered_df = df

# Display Results
st.title("ICD-11 Disease Search & Hierarchy")
st.write("Search for diseases, view hierarchical relationships, and export data.")

st.dataframe(filtered_df)

# Export Data
st.sidebar.subheader("Export Data")
buffer = BytesIO()
filtered_df.to_csv(buffer, index=False)
buffer.seek(0)
st.sidebar.download_button("Download CSV", buffer, file_name="filtered_icd11.csv")

st.write("Use this tool to explore ICD-11 codes, visualize relationships, and export relevant data.")

import streamlit as st
import pandas as pd
from io import BytesIO

# Debugging logs
st.write("🚀 App Started...")

# Load dataset with error handling
@st.cache_data
def load_data():
    st.write("📂 Attempting to load dataset...")
    try:
        df = pd.read_csv("icd11_codes.csv")
        st.write("✅ Dataset loaded successfully!")

        # Check first few rows to confirm data is readable
        st.write(df.head())

        # Create Parent_Code column
        df["Parent_Code"] = df["Code"].apply(lambda x: x.rsplit(".", 1)[0] if "." in x else None)
        return df
    except FileNotFoundError:
        st.error("❌ Error: The file 'icd11_codes.csv' was not found. Please upload it to your GitHub repository.")
        return pd.DataFrame(columns=["Code", "Title", "Parent_Code"])

df = load_data()

# Sidebar Search
st.sidebar.header("ICD-11 Disease Search")
search_query = st.sidebar.text_input("Search by Code or Title", "")

# Debug log
st.write("🔍 Searching for:", search_query)

# Filter data based on search
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
else:
    filtered_df = df

# Display Results
st.title("ICD-11 Disease Search & Hierarchy")
st.write("Search for diseases, view hierarchical relationships, and export data.")

# Debug log
st.write("📊 Displaying filtered dataset...")
st.dataframe(filtered_df)

# Export Data
st.sidebar.subheader("Export Data")
buffer = BytesIO()
filtered_df.to_csv(buffer, index=False)
buffer.seek(0)
st.sidebar.download_button("Download CSV", buffer, file_name="filtered_icd11.csv")

st.write("✅ Application Loaded Successfully!")

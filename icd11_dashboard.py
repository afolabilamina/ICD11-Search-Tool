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
import plotly.graph_objects as go
import networkx as nx

# Debugging message
st.write("📊 Preparing Hierarchy Visualization...")

# Create a network graph
def create_network_graph(data):
    G = nx.DiGraph()

    # Add nodes and edges
    for _, row in data.iterrows():
        G.add_node(row["Code"], label=row["Title"])
        if row["Parent_Code"] in data["Code"].values:
            G.add_edge(row["Parent_Code"], row["Code"])

    # Debugging message
    st.write(f"✅ Nodes added: {len(G.nodes())}, Edges added: {len(G.edges())}")

    # Generate layout
    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_labels = [G.nodes[node]["label"] for node in G.nodes()]

    # Create visualization
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, line=dict(width=1, color="gray"), hoverinfo="none", mode="lines"
    )
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_labels,
        textposition="top center",
        marker=dict(size=10, color="blue"),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="ICD-11 Disease Hierarchy", showlegend=False)
    return fig

# Button to show the visualization
if st.button("Show Hierarchy Visualization"):
    st.plotly_chart(create_network_graph(df))
st.write("✅ Application Loaded Successfully!")

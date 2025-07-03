import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv("project_data.csv", parse_dates=["Start Date", "End Date", "Last Update"])

st.set_page_config(page_title="Project Status Dashboard", layout="wide")
st.title("📊 Project Status Dashboard")

# Show summary metrics
st.subheader("📌 Project Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Projects", len(df))
col2.metric("On Track", (df["Status"] == "On Track").sum())
col3.metric("Delayed", (df["Status"] == "Delayed").sum())
col4.metric("Completed", (df["Status"] == "Completed").sum())

# Sidebar filters
st.sidebar.header("🔎 Filter")
status_filter = st.sidebar.multiselect("Select Status", df["Status"].unique(), default=df["Status"].unique())
owner_filter = st.sidebar.multiselect("Select Owner", df["Owner"].unique(), default=df["Owner"].unique())

# Filter data based on selections
filtered_df = df[df["Status"].isin(status_filter) & df["Owner"].isin(owner_filter)]

# Show filtered project table
st.subheader("📋 Project Details")
st.dataframe(filtered_df, use_container_width=True)

# Pie chart of project statuses
st.subheader("📈 Status Breakdown")
status_counts = filtered_df["Status"].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Progress bars for project completion
st.subheader("📶 Project Completion Progress")
for idx, row in filtered_df.iterrows():
    st.write(f"{row['Project Name']} ({row['Percent Complete']}%)")
    st.progress(int(row['Percent Complete']))

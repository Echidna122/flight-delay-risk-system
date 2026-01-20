import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")

# Load data
conn = sqlite3.connect("airline_ops.db")
df = pd.read_sql_query("SELECT * FROM flights", conn)
conn.close()

# Risk classification
def classify_risk(delay):
    if delay == 0:
        return "On Time"
    elif delay <= 15:
        return "Low Risk"
    elif delay <= 30:
        return "Medium Risk"
    else:
        return "High Risk"

df["delay_risk"] = df["delay_minutes"].apply(classify_risk)
df["flight_date"] = pd.to_datetime(df["flight_date"])

# Title
st.title("✈️ Flight Delay Risk Dashboard")
st.write("Simple analysis of flight delays using real airline data.")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Flights", len(df))
col2.metric("Delayed Flights", (df["delay_minutes"] > 0).sum())
col3.metric("Avg Delay (min)", round(df["delay_minutes"].mean(), 2))

st.divider()

# Filters
st.subheader("Filters")

airline = st.selectbox(
    "Select Airline",
    options=["All"] + sorted(df["airline"].unique().tolist())
)

if airline != "All":
    df = df[df["airline"] == airline]

date_range = st.date_input(
    "Select Date Range",
    [df["flight_date"].min().date(), df["flight_date"].max().date()]
)

df = df[
    (df["flight_date"].dt.date >= date_range[0]) &
    (df["flight_date"].dt.date <= date_range[1])
]

st.divider()

# Table
st.subheader("Flight Records")

st.dataframe(
    df[
        [
            "flight_date",
            "airline",
            "origin",
            "destination",
            "delay_minutes",
            "delay_risk"
        ]
    ],
    use_container_width=True,
    height=450
)

# Simple chart
st.subheader("Delay Risk Distribution")
st.bar_chart(df["delay_risk"].value_counts())

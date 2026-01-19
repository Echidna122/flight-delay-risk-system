import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Flight Delay Risk Dashboard", layout="wide")

conn = sqlite3.connect("./airline_ops.db")
df = pd.read_sql_query("SELECT * FROM flights", conn)
conn.close()

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

st.title("✈️ Flight Delay Risk Assessment Dashboard")

st.subheader("Flight Delay Risk Overview")
st.dataframe(
    df[["airline", "origin", "destination", "delay_minutes", "delay_risk"]],
    use_container_width=True
)

st.subheader("Delay Risk Distribution")
st.bar_chart(df["delay_risk"].value_counts())


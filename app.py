import sqlite3
import pandas as pd
import streamlit as st

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="Flight Delay Risk", layout="wide")

conn = sqlite3.connect("airline_ops.db")
df = pd.read_sql_query("SELECT * FROM flights", conn)
conn.close()

df["flight_date"] = pd.to_datetime(df["flight_date"])
df["is_delayed"] = (df["delay_minutes"] > 0).astype(int)

df["sched_dep_time"] = pd.to_numeric(df["sched_dep_time"], errors="coerce")
df["sched_dep_hour"] = (df["sched_dep_time"] // 100).astype("Int64")
df["day_of_week"] = df["flight_date"].dt.dayofweek

features = ["airline", "origin", "destination", "sched_dep_hour", "day_of_week"]
df = df.dropna(subset=features + ["is_delayed"])

X = df[features]
y = df["is_delayed"]

@st.cache_resource
def train_model(X, y):
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"),
             ["airline", "origin", "destination"]),
            ("num", "passthrough", ["sched_dep_hour", "day_of_week"]),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            )),
        ]
    )

    model.fit(X, y)
    return model

model = train_model(X, y)

st.title("✈️ Flight Delay Risk Prediction")
st.write("Enter flight details to predict delay risk using historical data.")

st.divider()

airports = sorted(pd.unique(df[["origin", "destination"]].values.ravel()))

with st.form("prediction_form"):
    airline = st.selectbox("Airline", sorted(df["airline"].unique()))
    origin = st.selectbox("Origin Airport", airports)
    destination_options = [a for a in airports if a != origin]
    destination = st.selectbox("Destination Airport", destination_options)
    sched_dep_hour = st.slider("Scheduled Departure Hour", 0, 23, 12)
    day_name = st.selectbox(
        "Day of Week",
        ["Monday", "Tuesday", "Wednesday", "Thursday",
         "Friday", "Saturday", "Sunday"]
    )
    submit = st.form_submit_button("Predict Delay Risk")

if submit:
    if origin == destination:
        st.error("Origin and destination airports must be different.")
        st.stop()

    day_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    input_df = pd.DataFrame(
        [[airline, origin, destination, sched_dep_hour, day_map[day_name]]],
        columns=features
    )

    prob = model.predict_proba(input_df)[0][1]

    if prob < 0.3:
        risk = "Low Risk"
    elif prob < 0.6:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    st.subheader("Prediction Result")
    st.write(f"**Delay Probability:** {prob:.2%}")
    st.write(f"**Predicted Risk Level:** {risk}")

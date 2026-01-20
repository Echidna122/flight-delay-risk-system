import sqlite3
import pandas as pd

csv_path = "data/raw/us_flights_2022.csv"
db_path = "airline_ops.db"

df = pd.read_csv(csv_path)

#only selecting relevant columns
df = df[[ 'FlightDate','Airline','Origin', 'Dest','CRSDepTime','DepTime','DepDelayMinutes',]]

# Rename to match DB schema
df = df.rename(
    columns={
        "FlightDate": "flight_date",
        "Airline": "airline",
        "Origin": "origin",
        "Dest": "destination",
        "CRSDepTime": "sched_dep_time",
        "DepTime": "actual_dep_time",
        "DepDelayMinutes": "delay_minutes",
    }
)

#remove null values
df = df.dropna(subset = ["sched_dep_time","actual_dep_time","delay_minutes"])

df['delay_minutes'] = df['delay_minutes'].astype(int)

df = df.head(10000)

conn = sqlite3.connect(db_path)
df.to_sql("flights", conn, if_exists='append', index = False)
conn.close

print("Loaded", len(df), "rows into flights table.")

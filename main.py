import sqlite3
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier   # CHANGED
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

conn = sqlite3.connect("airline_ops.db")
df = pd.read_sql_query("SELECT * FROM flights", conn)
conn.close()

df["is_delayed"] = (df["delay_minutes"] > 0).astype(int)

df["sched_dep_time"] = pd.to_numeric(df["sched_dep_time"], errors="coerce")
df["sched_dep_hour"] = (df["sched_dep_time"] // 100).astype("Int64")
df["day_of_week"] = pd.to_datetime(df["flight_date"]).dt.dayofweek

features = [
    "airline",
    "origin",
    "destination",
    "sched_dep_hour",
    "day_of_week",
]

df = df.dropna(subset=features + ["is_delayed"])

X = df[features]
y = df["is_delayed"]

categorical_features = ["airline", "origin", "destination"]
numeric_features = ["sched_dep_hour", "day_of_week"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(      # CHANGED
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        )),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Model accuracy:", round(accuracy_score(y_test, y_pred), 4))
print(classification_report(y_test, y_pred))

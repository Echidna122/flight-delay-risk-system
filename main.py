import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load data
conn = sqlite3.connect("./airline_ops.db")
df = pd.read_sql_query("SELECT * FROM flights", conn)
conn.close()

# Target variable: delayed or not
df["is_delayed"] = (df["delay_minutes"] > 0).astype(int)

# Feature engineering (pre-departure only)
df["sched_dep_time"] = pd.to_numeric(df["sched_dep_time"], errors="coerce")
df = df.dropna(subset=["sched_dep_time"])

df["sched_dep_hour"] = (df["sched_dep_time"] // 100).astype(int)

df["day_of_week"] = pd.to_datetime(df["flight_date"]).dt.dayofweek

features = ["airline", "origin", "destination", "sched_dep_hour", "day_of_week"]
df = df.dropna(subset=features + ["is_delayed"])

X = df[features]
y = df["is_delayed"]

# Preprocessing
categorical_features = ["airline", "origin", "destination"]
numeric_features = ["sched_dep_hour", "day_of_week"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features),
    ]
)

# Model pipeline
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ]
)

# Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model accuracy:", accuracy)
print(classification_report(y_test, y_pred))


import sqlite3
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

conn = sqlite3.connect("./airline_ops.db")
df = pd.read_sql_query("SELECT * FROM flights", conn)
conn.close()

df["is_delayed"] = df["delay_minutes"].apply(lambda x: 1 if x > 0 else 0)

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

X = df[["delay_minutes"]]
y = df["is_delayed"]

model = LogisticRegression()
model.fit(X, y)

y_pred = model.predict(X)
accuracy = accuracy_score(y, y_pred)

print("Model accuracy:", accuracy)
print(df[["airline", "origin", "destination", "delay_minutes", "delay_risk"]])

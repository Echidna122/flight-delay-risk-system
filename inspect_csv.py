import pandas as pd

df = pd.read_csv("data/raw/us_flights_2022.csv", nrows=5)
print(df.columns.tolist())


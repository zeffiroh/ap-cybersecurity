import pandas as pd

df = pd.read_csv("case/conn.csv", parse_dates=["time"])
print(df.head())
print(df.shape)

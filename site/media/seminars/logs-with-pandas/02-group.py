import pandas as pd

df = pd.read_csv("case/conn.csv", parse_dates=["time"])
out = df.groupby(["dst", "dport"]).agg(connections=("bytes_out", "size"), bytes_out=("bytes_out", "sum")).sort_values("bytes_out", ascending=False)
print(out)

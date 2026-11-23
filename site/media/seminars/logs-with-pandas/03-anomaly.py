import pandas as pd

df = pd.read_csv("case/conn.csv", parse_dates=["time"])
beacon = df[df["dport"] == 4444].copy()
median = beacon["bytes_out"].median()
mad = (beacon["bytes_out"] - median).abs().median()
beacon["score"] = 0.6745 * (beacon["bytes_out"] - median) / mad
print(beacon[["time", "bytes_out", "score"]].round(1).to_string(index=False))
print()
print(beacon[beacon["score"] > 3.5][["time", "bytes_out"]].to_string(index=False))

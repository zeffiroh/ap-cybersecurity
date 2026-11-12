import csv
from collections import defaultdict

rows = [r for r in csv.DictReader(open("case/process.csv")) if r["host"] == "hr-pc07"]
kids = defaultdict(list)
for r in rows:
    kids[r["ppid"]].append(r)


def show(pid, depth):
    for r in kids.get(pid, []):
        print("    " * depth + r["time"][11:] + " UTC  " + r["image"].split("\\")[-1] + "  (pid " + r["pid"] + ")  " + r["command_line"][:60])
        show(r["pid"], depth + 1)


show("704", 0)

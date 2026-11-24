from datetime import datetime, timezone

for line in open("case/proxy.log"):
    f = line.split()
    if "AWB-77120" in f[6] or "files-cdn-sync" in f[6]:
        when = datetime.fromtimestamp(float(f[0]), timezone.utc).strftime("%H:%M:%S UTC")
        print(when, f[2], f[3], f[4], f[6])

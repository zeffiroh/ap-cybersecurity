from datetime import datetime, timezone

for line in open("case/proxy.log"):
    f = line.split()
    if "docm" in f[6] or "s2.bin" in f[6]:
        when = datetime.fromtimestamp(float(f[0]), timezone.utc).strftime("%H:%M:%S UTC")
        print(when, f[2], f[3], f[6])

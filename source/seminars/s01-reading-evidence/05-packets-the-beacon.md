## 5. Packets: the beacon

After the download, appt01 keeps calling the same server over TLS. The content is encrypted, but the **timing** and the **server name** (SNI) are not. Regular calls at a fixed interval are a beacon: a program checking in for instructions.

```tool packets
{"file": "capture.pcap", "f": "tls and ip.dst==203.0.113.77", "n": 3, "blank": ["f"]}
```

```tool packets
{"file": "capture.pcap", "f": "dns.qry.name contains patch-relay", "n": 8, "blank": ["f"]}
```

- [ ] When does each TLS Client Hello to 203.0.113.77 start?
- [ ] How far apart are they? Does that match the cron line?
- [ ] Compare with the TLS to portal and backup: why are those normal?

> Hint: Look at the Time column. The cron line runs every ten minutes.

?> How many minutes apart are the TLS connections to 203.0.113.77? :: 10

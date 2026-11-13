## 8. A sensor rule for next time

Turn what you found into rules the IDS can run on every packet, so the next download and the next beacon raise an alert by themselves. Run them on the capture and check two things: they catch the bad traffic, and they don't fire on the portal, the backup or the database.

```tool ids
{"rules": "alert http $HOME_NET any -> $EXTERNAL_NET any (msg:\"Script or binary fetched by wget or curl\"; http.user_agent; pcre:\"/^(Wget|curl)\\//\"; sid:1100001; rev:1;)\nalert tls $HOME_NET any -> $EXTERNAL_NET 443 (msg:\"Beacon to cdn.patch-relay.example\"; content:\"SNI=cdn.patch-relay.example\"; sid:1100002; rev:1;)\n", "file": "capture.pcap", "n": 5, "blank": ["rules"]}
```

- [ ] Rule 1 catches both downloads
- [ ] Rule 2 catches the three beacons
- [ ] No alert on internal traffic
- [ ] One line on what each rule would miss

> Hint: A real server rarely needs Wget or curl to reach the internet, so those User-Agents are worth an alert there. A beacon rule on one server name is easy to evade with a new name; the timing is the more lasting sign.

?> How many alerts do the two rules give on the capture? :: 5

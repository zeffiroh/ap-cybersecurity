## 4. Packets: the download

Now the wire. The capture is the core switch mirror from 01:15. In the packet viewer a **display filter** keeps only the packets you ask for. Start with every HTTP request, then everything to or from the download server, and follow the stream of the first download.

```tool packets
{"file": "capture.pcap", "f": "http.request", "n": 2, "blank": ["f"]}
```

```tool packets
{"file": "capture.pcap", "f": "ip.addr==203.0.113.77", "n": 10, "blank": ["f"]}
```

The Linux cell below asks tshark the same question on the command line.

- [ ] Which two files were fetched, from which host name?
- [ ] Which program fetched each one? (the User-Agent)
- [ ] What kind of file came back each time?

> Hint: The first request's User-Agent is Wget, which matches the sudo line. The second is curl, which matches the script.

?> Which host name served /m.sh? :: cdn.patch-relay.example

?> Which User-Agent fetched /a.bin? :: curl/7.81.0

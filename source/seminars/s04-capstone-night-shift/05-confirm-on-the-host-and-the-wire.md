## 5. Confirm on the host and the wire

Search results are a summary. Confirm on the laptop's own logs and on the packet capture: which programs ran, which one sent the data, what it really is, and where the data went.

- [ ] Sysmon event 1: follow the chain from the download to the copy tool
- [ ] Sysmon event 1 shows OriginalFileName, the name the program was built with. Which program is hiding under a new name?
- [ ] Sysmon event 3: which program connected to 203.0.113.150, and how many times?
- [ ] Capture: find the TLS Client Hellos to the storage site

> Hint: In the packet viewer, the filter `tls.handshake.extensions_server_name contains cloudbox` shows the start of each upload stream. rclone is a real, free copy tool for cloud storage: useful to IT, and to anyone stealing files.

```tool events
{"file": "eventlogs/Sysmon.jsonl", "ids": "1", "n": 17, "blank": ["ids", "src", "q"]}
```

```tool events
{"file": "eventlogs/Sysmon.jsonl", "ids": "1", "q": "rclone.exe", "n": 3, "blank": ["ids", "src", "q"]}
```

```tool events
{"file": "eventlogs/Sysmon.jsonl", "ids": "3", "q": "203.0.113.150", "n": 8, "blank": ["ids", "src", "q"]}
```

```tool packets
{"file": "capture.pcap", "f": "tls.handshake.extensions_server_name contains cloudbox", "n": 8, "blank": ["f"]}
```

?> Which domain did the remote access tool connect to? :: relay.remotehelper.example

?> What file name does the copy tool run under? :: svc-sync.exe

?> What is its real program name (OriginalFileName)? :: rclone.exe

?> At what time (HH:MM) did the copy that worked start? :: 00:16

?> Which IP address received the data? :: 203.0.113.150

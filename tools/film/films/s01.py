from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

RULES = """alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"Script or binary fetched by wget or curl"; http.user_agent; pcre:"/^(Wget|curl)\\//"; sid:1100001; rev:1;)
alert tls $HOME_NET any -> $EXTERNAL_NET 443 (msg:"Beacon to cdn.patch-relay.example"; tls.sni; content:"cdn.patch-relay.example"; sid:1100002; rev:1;)
"""

SURICATA = "mkdir -p /tmp/ids && suricata -r capture.pcap -S ~/ids/local.rules -l /tmp/ids -k none --set stream.midstream=true --set vars.address-groups.HOME_NET='[10.30.0.0/16]' 2>&1 | tail -n 2"

TRIAGE = """HOST TRIAGE NOTE  appt01 (10.30.1.20)   6 Nov 2026, all times UTC
Started by: IDS alert 01:20:11 "possible script download by Wget"

Checked (repeat these): grep 'Failed password|Accepted|sudo' auth.log; cat crontab.txt;
  grep -E 'sysmon|\\.m\\.sh' ps.txt; tshark -Y http.request; zeek conn.log; rcp-pc03 Security log

Facts (source)
  until 01:19   50 failed SSH passwords, 46 from 198.51.100.23, 16 of them for vendor (auth.log)
  01:19:44      vendor logged in with a password from 198.51.100.23 (auth.log)
  01:20:10      sudo wget m.sh from cdn.patch-relay.example (auth.log, capture)
  01:20:31      m.sh fetched a.bin with curl, saved /usr/local/bin/.sysmon-agent, added cron */10 (m.sh, crontab)
  01:21 to 01:41  TLS to cdn.patch-relay.example every 600 s (capture, conn.log)
  01:33 to 01:34  9 failed then 1 good network logon as frontdesk on rcp-pc03; 6 scans read (Security log)
Not known yet: what a.bin does; whether the vendor password is used elsewhere; what else left via 443.
Disposition: TRUE POSITIVE. Escalated. Next: isolate appt01, reset vendor and frontdesk passwords.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Reading evidence. Every analyst job, whatever its title, comes down to reading four kinds of evidence: a server's logs, the packets on the wire, a network sensor's summary, and a Windows event log. Each one tells part of the story, and none of them tells all of it."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("We follow one night at Tamarind Health, a chain of clinics in Pune. Someone guesses a password on the appointments server, gets in, downloads a program, and reaches across the network to a reception PC full of patient scans. We find every step with grep, Wireshark and tshark, a Zeek log, the Windows Security log and the Suricata IDS, all real software on a real Linux machine."),
 close("files"),
 term,

 chapter("1. Take stock of the evidence"),
 say("Step one: take stock of the evidence. Read the README so you know the machines, the addresses and the time zone."),
 cmd("cat README.txt", 4),
 after("appt01 is the appointments server, with SSH open to the internet for the software vendor. rcp-pc03 is a reception PC with a share of patient scans. Everything is in UTC. And the IDS alert that started this: a possible script download by Wget, at 01:20:11. Now we hash everything before we open it. A hash is a fingerprint of a file; if anyone asks whether the evidence changed in your hands, the hashes are your proof."),
 cmd("find . -type f | sort | xargs sha256sum | cut -c1-16,65-", 3),
 clear,

 chapter("2. Linux, who was knocking"),
 say("Step two: who was knocking. Port 22 is open to the internet, so auth.log is full of strangers trying passwords. grep minus c counts the failed passwords."),
 cmd("grep -c 'Failed password' auth.log", 2),
 say("Fifty. From where? grep minus o keeps just the from-address part of each line, sort puts identical ones together, uniq minus c counts them, and sort minus r n ranks them."),
 cmd("grep 'Failed password' auth.log | grep -o 'from [0-9.]*' | sort | uniq -c | sort -rn", 2.5),
 after("Forty-six from one address, 198.51.100.23, and four from another. Which accounts did they try?"),
 cmd("grep 'Failed password' auth.log | grep -o 'for [a-z ]*from' | sort | uniq -c | sort -rn", 2.5),
 after("root, admin, test, oracle, postgres: the usual guesses. But the top one is vendor, sixteen times. vendor is a real account here, the software company's. Someone knew that."),
 clear,

 chapter("3. Linux, the login and what came next"),
 say("Step three: a brute force only matters if it worked. The word sshd writes for a successful login is Accepted."),
 cmd("grep Accepted auth.log", 2.5),
 after("deploy at 00:40 from the IT admin PC, with a key: normal. And vendor at 01:19:44, with a password, from 198.51.100.23. It worked. sudo logs every command it runs as root, in full."),
 cmd("grep sudo auth.log | grep -o 'COMMAND=.*'", 2.5),
 after("At 01:20:10, wget downloads m.sh from cdn.patch-relay.example into a hidden file in tmp. Twenty seconds later it runs. At 01:33, smbclient opens the Scans share on 10.30.2.33, the reception PC. The IT contractor recovered the script."),
 cmd("cat recovered/m.sh", 3),
 after("It downloads a.bin with curl, saves it as .sysmon-agent, a name chosen to look like a monitoring tool, and adds a cron line so it runs every ten minutes. Attackers hide in two places so they can come back: a scheduled job and a running process. Let's check both."),
 cmd("cat crontab.txt; grep -E 'sysmon|\\.m\\.sh' ps.txt", 3),
 after("The cron line is there, next to the real nightly backup, and the agent has been running since 01:21."),
 clear,

 chapter("4. Packets, the download"),
 say("Step four: packets. Logs tell you what a computer says happened. Packets show what actually crossed the wire. The capture is the core switch's mirror port from 01:15. Wireshark is the free, open-source packet viewer. We open it with a display filter that keeps only HTTP requests."),
 {"open": ["env", "QT_SCALE_FACTOR=1.35", "wireshark", "-r", "capture.pcap", "-Y", "http.request"], "window": "capture.pcap|Wireshark", "as": "ws", "geometry": [40, 40, 1840, 1000], "timeout": 60, "settle": 3},
 wait(3),
 {"point": [0.3, 0.12], "in": "ws", "secs": 1.0, "wait": 2},
 after("Two requests, both from 10.30.1.20, appt01, to 203.0.113.77. GET m.sh, and GET a.bin. Now everything to or from that server: ip dot addr equals."),
 {"use": "ws", "at": [0.5, 0.5], "keys": ["ctrl+slash", "ctrl+a"]},
 {"use": "ws", "at": [0.5, 0.5], "type": "ip.addr == 203.0.113.77", "cps": 14, "wait": 3},
 after("The two downloads on port 80, then three connections on port 443. Click a packet and the pane below shows every layer: the frame, IP, TCP, and the application on top."),
 {"point": [0.3, 0.16], "in": "ws", "secs": 0.8, "click": True, "wait": 3},
 clear,

 chapter("5. Packets, the beacon"),
 say("Step five: the beacon. After the download, appt01 keeps calling the same server over TLS, which is encrypted. We can't read what it says. But two things are never encrypted: the timing of the connections, and the server name in the TLS Client Hello, called the SNI."),
 {"use": "ws", "at": [0.5, 0.5], "keys": ["ctrl+slash", "ctrl+a"]},
 {"use": "ws", "at": [0.5, 0.5], "type": "tls.handshake.extensions_server_name contains \"patch-relay\"", "cps": 16, "wait": 3},
 after("Wireshark can filter on the server name itself. Three Client Hellos ask for cdn.patch-relay.example, all to 203.0.113.77. The clinic's own TLS, to the patient portal and the backup server, is filtered out. Now the same question on the command line with tshark, Wireshark's terminal twin, which prints the time of each one in seconds from the start of the capture."),
 close("ws"),
 cmd("tshark -r capture.pcap -t ud -Y 'tls.handshake.extensions_server_name contains \"patch-relay\"' -T fields -e frame.time_relative -e ip.dst -e tls.handshake.extensions_server_name", 3.5),
 after("352 seconds into the capture, then 952, then 1552: exactly six hundred seconds apart, every ten minutes, matching the cron line. A program calling the same server at a fixed interval is a beacon, checking in for instructions."),
 clear,

 chapter("6. Network sensor, who talked to whom"),
 say("Step six: Zeek is a network sensor that writes one line per connection: who opened it, to which address and port, which service, how long it lasted and how many bytes went each way. It's the fastest way to see a whole night at once. The fields are separated by tabs, so awk uses a tab as the separator."),
 cmd("grep -v '^#' zeek/conn.log | awk -F'\\t' '{print $3, \"->\", $5\":\"$6, $8}' | sort | uniq -c | sort -rn", 3),
 after("Ten SSH connections from the attacker. Ten from appt01 to 10.30.2.33 on port 445, which is Windows file sharing, with NTLM sign-in. And the downloads and beacons to 203.0.113.77. An appointments server has no business opening a reception PC's files. Only those ten:"),
 cmd("grep -v '^#' zeek/conn.log | awk -F'\\t' '$5==\"10.30.2.33\" {print $1, $3, $6, $12, $11}'", 3),
 after("Nine short connections that end in a reset: failed attempts. Then one that completes, carrying more than five megabytes."),
 clear,

 chapter("7. Windows, the hop to reception"),
 say("Step seven: the reception PC saw those connections as logons, and Windows writes every logon to its Security log. Four event IDs tell the story. 4625 is a failed logon, 4624 a successful one, and logon type 3 means over the network. 5140 is a share being opened, and 5145 is a file in it being read. jq filters the log to the attacker's address."),
 cmd("jq -r 'select(.Data.IpAddress==\"10.30.1.20\") | [.TimeCreated[11:19], .EventID, .Data.TargetUserName // \"\", .Data.LogonType // \"\", .Data.ShareName // \"\", .Data.RelativeTargetName // \"\"] | @tsv' eventlogs/Security.jsonl", 3.5),
 after("Nine failures for frontdesk, then a successful network logon at 01:34:02, the Scans share opened, and six patient files read, one every nine seconds: scans, a referral and a lab report. That's personal health data leaving the clinic."),
 clear,

 chapter("8. A sensor rule for next time"),
 say("Step eight: a sensor rule for next time. Finding an attack once is good. Making sure the next one raises an alert by itself is better. Suricata is a free, open-source intrusion detection system. Rule one alerts when a server fetches something with Wget or curl. Rule two alerts on TLS to the beacon's server name."),
 cmd("cat ~/ids/local.rules", 3),
 say("Now we run Suricata on the capture with only these two rules, and read its alert log."),
 cmd(SURICATA, 8),
 cmd("sed 's/^[^ ]* *//' /tmp/ids/fast.log | cut -c1-150", 3),
 after("Five alerts: both downloads and all three beacons. And nothing on the portal, the backup or the database. Each rule has a weakness worth writing down. A new server name beats rule two, so the timing is the more lasting sign. And an attacker can change the User-Agent, but a server that rarely needs Wget or curl makes rule one worth keeping."),
 clear,

 chapter("9. Write the triage note"),
 say("Step nine: write it up. A host triage note for appt01 says what was checked, with the exact commands, so anyone can repeat it, and keeps facts apart from what we don't know yet. The network finding for 01:00 to 02:00 follows the same shape."),
 edit("triage-appt01.txt"),
 write(TRIAGE, cps=40),
 save_note(),
 close("note"),
 clear,

 chapter("10. Hand in"),
 say("Step ten: hand in. On the course site the notebook carries every answer, every tool result and both reports, and your teacher marks it with the rubric."),
 cmd("ls -l *.txt", 2),
 chapter("Wrap-up"),
 say("That's one night read through four kinds of evidence. The login log showed the guessing and the login. sudo showed the download. Wireshark and tshark showed what crossed the wire, and the beacon's rhythm through encryption. Zeek showed the whole night in a few lines, and the Windows log showed the patient files being read. And two Suricata rules make sure the next one raises an alert by itself. Next, in Log search and detection as code, we hunt across logs with search languages and turn hunts into rules. Thank you for watching."),
 wait(2),
]

build("s01-reading-evidence", scenes, host="tamarind-soc", files={"ids/local.rules": RULES}, pcap=["capture.pcap"],
      setup=["mkdir -p ~/ids && mv ids/local.rules ~/ids/ && rmdir ids"])

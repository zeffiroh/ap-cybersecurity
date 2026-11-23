from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

RULE = """title: rclone running under another name
id: 7d2c1e40-5b8a-4c1e-9f0a-3e2b00000001
status: experimental
description: The copy tool rclone, renamed to look like a Windows service. Used to steal files to cloud storage.
logsource:
  product: windows
  service: sysmon
detection:
  selection:
    EventID: 1
    OriginalFileName: 'rclone.exe'
  filter_real_name:
    Image|endswith: '\\\\rclone.exe'
  condition: selection and not filter_real_name
falsepositives:
  - IT staff who rename rclone for a backup job (ask them; list the path)
level: high
tags:
  - attack.exfiltration
  - attack.t1567.002
  - attack.stealth
  - attack.t1036.003
"""

SCOPE = """.mode box
SELECT src_host, dst_host, action, count(*) AS sessions, round(sum(bytes_out) / 1e6, 1) AS mb_out
FROM 'fw_sessions.csv' GROUP BY ALL ORDER BY sum(bytes_out) DESC LIMIT 8;
SELECT time, src_host, dst_host, action FROM 'fw_sessions.csv' WHERE action <> 'allow';
"""

DISPOSITIONS = """INTRUSION INC-1112 on acc-lt03 (j.walsh), five alerts, one story:
  AL-8401 TP  fake support site, LedgerPro_Support.exe downloaded 00:04
  AL-8403 TP  that file is RemoteHelper, a remote access tool, connected to its relay 00:04
  AL-8404 TP  attacker's commands through rhagent.exe: whoami /all, net use 00:09
  AL-8408 TP  svc-sync.exe = rclone (OriginalFileName), dropped in ProgramData 00:13
  AL-8406 TP  2.26 GB of S:\\Clients\\2026 copied to storage.cloudbox.example from 00:16
Benign or expected:
  AL-8402 inbox rule by a.nguyen from the office for real tax office mail
  AL-8405 patch push CHG-0417     AL-8409 monthly archive CHG-0412     AL-8410 CHG-0418
  AL-8407 k.lee Caps Lock, same desk     AL-8411 new iPhone, MFA approved from the office
  AL-8412 unknown Wi-Fi phone: no other logs; ask the client to identify it (open, low)
"""

ESCALATION = """ASK: Practice principal: approve that we cut acc-lt03 off the network and disable j.walsh's account now, and call j.walsh before 02:00 UTC (12:00 Brisbane).

Severity: CRITICAL. Client tax files left the practice: 2.26 GB of S:\\Clients\\2026 went to a cloud storage account we don't control, 00:16 to 00:46 UTC (10:16 to 10:46 Brisbane).

What we know: j.walsh downloaded "LedgerPro support" from a fake site at 00:04 UTC. It installed RemoteHelper, a remote access tool. Through it someone ran commands, downloaded rclone renamed svc-sync.exe, and copied the client folder. Your firewall blocked their first choice, filedrop.example; the copy then used storage.cloudbox.example, which reception also uses.
What we don't know: who the cloud account wf-bkp-1112 belongs to; whether the remote session is still open; whether other laptops were called.
What we have changed: nothing yet. What we have not done: we have not contacted the support site or the storage company.
"""

HANDOVER = """SHIFT REPORT  night to morning  12 Nov 2026 02:00 UTC (12:00 Brisbane)
OPEN
  INC-1112 (AL-8401, 8403, 8404, 8408, 8406) data theft from acc-lt03. Owner: client principal + IR on call.
    Next: isolate acc-lt03, remove RemoteHelper, report cb:wf-bkp-1112 to the storage company.
  AL-8412 unknown phone on staff Wi-Fi. Owner: client office manager. Next: identify it.
CLOSED  AL-8402, 8405, 8407, 8409, 8410, 8411: benign or a planned change (reasons in the queue).
WATCH   relay.remotehelper.example, ledgerpro-support.example, 203.0.113.91 from any host;
        OriginalFileName rclone.exe anywhere (new rule, sid wf-0001).
CALLS   00:58 UTC principal (escalation by phone and SMS).   HINTS OPENED: 0
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("This is Capstone A, the night shift. You work for a managed SOC, a company that watches other companies' networks around the clock. Tonight's client is Wattle and Finch Accountants, a fourteen-person practice in Brisbane. When it's ten in the morning in Brisbane, it's half past five in India, so their working day is your night."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The queue has twelve alerts and no severities, because the client's old SIEM doesn't send them. One real intrusion is hiding in there. I'll walk the whole shift once with real tools, jq, DuckDB, Wireshark's tshark, Sigma and Zircolite, so you can see what good looks like, and then it's your turn in the capstone notebook."),
 close("files"),
 term,

 chapter("1. How the night desk works"),
 say("Step one: how the night desk works. The alert queue says what you have to decide. Search says how big it is. The laptop's own logs say exactly what ran and what started it. Packets show what really crossed the wire. Intel and ATT&CK say whether anyone has seen this before. Sigma leaves a better rule behind. Here's what we have to search tonight."),
 cmd("cat README.txt | sed -n '1,12p'", 3.5),
 after("No web proxy: laptops go straight out through the firewall. So the firewall's session log and the DNS log are our search."),
 clear,

 chapter("2. Start of shift"),
 say("Step two: start of shift. Hash the evidence, then read the queue end to end."),
 cmd("sha256sum *.* eventlogs/* | cut -c1-16,65-", 2.5),
 cmd("jq -r '.[] | [.id, .time[11:16], .host, .user, .rule] | @tsv' alerts-night.json | column -t -s $'\\t'", 4),
 after("Twelve alerts. A first guess at which belong together: four of them are on acc-lt03, j.walsh's laptop, between 00:03 and 00:13, and a large upload from the same laptop at 00:46. A download, a remote access tool, discovery commands, a program in ProgramData, and an upload. That reads like one story. We'll test the guess."),
 clear,

 chapter("3. Work the queue"),
 say("Step three: work the queue. Every alert gets a disposition and a reason that points at evidence. The ones that aren't the intrusion each have a fact that explains them."),
 cmd("jq -r '.[] | select(.host != \"acc-lt03\") | [.id, .detail] | @tsv' alerts-night.json | cut -c1-200", 4),
 after("Three are planned changes with change numbers. k.lee had Caps Lock on, at her own desk. m.chen's new iPhone had MFA approved from the office. a.nguyen's inbox rule files real tax office mail. The unknown phone on the Wi-Fi has nothing else in any log: keep it open, low, and ask the client. The five on acc-lt03 are one intrusion, and they should say so, so the client reads one story, not five."),
 edit("dispositions.txt"),
 write(DISPOSITIONS, cps=46),
 save_note(),
 close("note"),
 clear,

 chapter("4. Scope it with search"),
 say("Step four: scope it with search. Before you escalate, know how big it is. Which laptop sent the most data out, where, and was anything blocked? This saved DuckDB query reads the firewall's CSV directly."),
 cmd("cat scope.sql", 2),
 cmd("duckdb < scope.sql", 4),
 after("acc-lt03 sent 2,255 megabytes, about 2.26 gigabytes, to storage.cloudbox.example in eight sessions. Reception uses the same cloud storage to send files to clients, but only 4.6 megabytes. And the firewall blocked two things. acc-lt01 asking a public time server for the time: ordinary. And at 00:15, acc-lt03 to filedrop.example, an anonymous file sharing site. The attacker tried there first, got blocked, and switched to a service the client allows. Who else looked up the fake support site?"),
 cmd("grep -E 'ledgerpro-support|remotehelper|toolmirror|filedrop' dns.log | awk '{print $2, $5, $7}'", 3),
 after("Only acc-lt03, 10.40.0.23. One laptop, one victim. In the course notebook you write the cloud storage search again in KQL to check yourself: two tools, one answer."),
 clear,

 chapter("5. Confirm on the host and the wire"),
 say("Step five: confirm on the host and the wire. Search is a summary. Sysmon event 1 records every program that starts, with its command line, its parent, and one field that matters a lot tonight: OriginalFileName, the name the program was built with. Renaming the file doesn't change it."),
 cmd("jq -r 'select(.EventID==1) | [.TimeCreated[11:19], (.Data.Image | split(\"\\\\\") | last), .Data.OriginalFileName, (.Data.ParentImage | split(\"\\\\\") | last)] | @tsv' eventlogs/Sysmon.jsonl | column -t", 4),
 after("Read the right-hand columns. LedgerPro_Support.exe was built as RemoteHelper.exe. RemoteHelper's agent starts cmd, and cmd starts whoami, net and PowerShell: the attacker typing through the remote tool. Then svc-sync.exe, whose original name is rclone.exe, a well-known file copy tool. The commands it ran:"),
 cmd("jq -r 'select(.EventID==1 and .Data.OriginalFileName==\"rclone.exe\") | .TimeCreated[11:19] + \"  \" + .Data.CommandLine' eventlogs/Sysmon.jsonl", 3),
 after("copy S:\\Clients\\2026 to fd, then to cb with eight transfers at once. And on the wire, tshark lists every server name acc-lt03 opened TLS to."),
 cmd("tshark -r capture.pcap -Y 'tls.handshake.type == 1' -T fields -e tls.handshake.extensions_server_name | sort | uniq -c | sort -rn", 4),
 after("The capture agrees: the support site, the remote tool's relay, the mirror, and the cloud storage, many times over."),
 clear,

 chapter("6. Check the indicators"),
 say("Step six: check every indicator against the intel feed and the client's allow list."),
 cmd("jq -r '.[] | [.indicator, .verdict, .source, (.tags | join(\"; \"))] | @tsv' intel.json | column -t -s $'\\t'", 3.5),
 after("The support site and its address are known phone scams. The remote tool's relay isn't on this client's allow list. And storage.cloudbox.example is allowed, because reception uses it. You can't block it without breaking the practice, so the response is to get the attacker's account, wf-bkp-1112, shut down. In ATT&CK: T1219, remote access software; T1036, masquerading, for the renamed rclone; and T1567.002, exfiltration to cloud storage."),
 clear,

 chapter("7. Escalate"),
 say("Step seven: one escalation for the whole intrusion, not one per alert. The reader is the practice principal, on a phone between client meetings. The ask goes first, with a time in UTC and in Brisbane time."),
 edit("escalation.txt"),
 write(ESCALATION, cps=42),
 save_note(),
 close("note"),
 clear,

 chapter("8. Leave a new detection behind"),
 say("Step eight: leave a new detection behind. The client's upload rule fired at 00:46, half an hour after the copy started, because it waits for a gigabyte. We want a rule that fires before any data moves: something the copy tool did that normal programs don't. A program whose original name is rclone, running under any other name."),
 cmd("cat rules/renamed-rclone.yml", 3),
 cmd("sigma check rules/renamed-rclone.yml 2>&1 | tail -n 4", 4),
 cmd("zircolite -e eventlogs/Sysmon.jsonl -r rules/renamed-rclone.yml", 8),
 after("Three matches, all svc-sync.exe, the first at 00:14:02 running version, two minutes before any data moved. What would make it noisy: IT staff who rename rclone for a real backup job. That goes in the false positives, with the path to exclude."),
 clear,

 chapter("9. Shift report"),
 say("Step nine: close the shift so the morning team can carry on without calling you."),
 edit("shift-report.txt"),
 write(HANDOVER, cps=44),
 save_note(),
 close("note"),
 clear,

 chapter("10. Hand in"),
 say("Step ten: hand in. The capstone notebook carries the queue, the searches, the escalation, the rule and the shift report, and the rubric takes a point for each hint you open."),
 cmd("ls -l *.txt rules/", 2),
 chapter("Wrap-up"),
 say("That's a night shift. Twelve alerts with no severities, and you found the five that were one intrusion: a fake support call, a remote access tool, a renamed copy tool, a blocked first try and a quiet switch to a service the client trusts. You scoped it with search, confirmed it on the host and the wire, escalated once with the ask first, and left a rule that fires before the next copy starts. Next, in Incident response, we take a ransomware night from custody to the boardroom. Thank you for watching."),
 wait(2),
]

build("s04-capstone-night-shift", scenes, host="wattle-soc", pcap=["capture.pcap"],
      files={"rules/renamed-rclone.yml": RULE, "scope.sql": SCOPE},
      setup=["nohup python3 -m http.server 8088 -d /opt/cyberchef >/dev/null 2>&1 &",
             "echo \"alias zircolite='python3 /opt/zircolite/zircolite.py -j --no-event-filter --flatten-backend python -l /tmp/zircolite.log -o /tmp/detected.json'\" >> ~/.bashrc"])

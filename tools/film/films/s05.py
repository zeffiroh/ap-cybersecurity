from kit import TREE, after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

TIMELINE = """CREATE VIEW vpn AS
  SELECT strptime(split_part(line, ' ', 1), '%Y-%m-%dT%H:%M:%SZ') AS ts, 'vpn01' AS source,
         regexp_replace(line, '^\\S+ \\S+ ', '') AS event
  FROM read_csv('vpn.log', columns = {'line': 'VARCHAR'}, delim = '\\t', header = false, quote = '', escape = '');

CREATE VIEW win AS
  SELECT json_extract_string(json, '$.TimeCreated')::TIMESTAMP AS ts,
         split_part(json_extract_string(json, '$.Computer'), '.', 1) AS source,
         json_extract_string(json, '$.EventID') || '  ' || coalesce(
           json_extract_string(json, '$.Data.TargetUserName') || ' type ' || json_extract_string(json, '$.Data.LogonType')
             || ' from ' || json_extract_string(json, '$.Data.IpAddress'),
           json_extract_string(json, '$.Data.CommandLine'),
           json_extract_string(json, '$.Data.ServiceName') || ' ' || json_extract_string(json, '$.Data.ImagePath'),
           split_part(json_extract_string(json, '$.Message'), chr(10), 1)) AS event
  FROM read_ndjson_objects('eventlogs/*.jsonl');

CREATE VIEW proc AS
  SELECT "time"::TIMESTAMP AS ts, host AS source, 'process  ' || command_line AS event
  FROM read_csv('process.csv') WHERE host = 'fs02';

.maxrows 80
SELECT strftime(ts, '%d %H:%M:%S') AS utc, source, left(event, 105) AS event
FROM (SELECT * FROM vpn UNION ALL SELECT * FROM win UNION ALL SELECT * FROM proc)
WHERE ts BETWEEN '2026-11-06 22:40' AND '2026-11-07 01:00'
ORDER BY ts;
"""

CUSTODY = """time_utc,file,sha256 (first 16),action,by
2026-11-07 01:40,vpn.log,see custody-hashes.txt,received from IT (export by r.joshi),IR analyst
2026-11-07 01:40,eventlogs/*.jsonl,see custody-hashes.txt,received from IT (exported 01:20),IR analyst
2026-11-07 01:40,captured/volatility-eng-ws14.txt,see custody-hashes.txt,received from IR team (image taken 01:14),IR analyst
2026-11-07 01:41,suspect/RESTORE-FILES.txt,see custody-hashes.txt,opened read-only for review,IR analyst
"""

ATTACK = """time_utc  technique                                   evidence
22:44     T1133 External Remote Services, T1078 Valid  vpn.log: s.kale, no MFA, 2nd try (on leave)
22:52     T1021.001 Remote Desktop Protocol             eng-ws14 4624 type 10 from 10.50.9.21
22:54     T1033 / T1069.002 / T1018 Discovery           whoami /groups, net group Domain Admins, nltest
22:58     T1105 Ingress Tool Transfer                   powershell iwr r.zip from 203.0.113.140
23:05     T1003.001 OS Credential Dumping: LSASS        rundll32 comsvcs.dll MiniDump 724 (Volatility cmdline)
23:19     T1550.002 Use Alternate Auth: Pass the Hash   px.exe -u adm.rjoshi -H ...; fs02 4624 NTLM type 3
23:20     T1543.003 / T1569.002 Windows Service         7045 WinUpdSvc C:\\Windows\\WinUpdSvc.exe
23:41     T1490 Inhibit System Recovery                 vssadmin delete shadows; bcdedit recoveryenabled no
23:42     T1486 Data Encrypted for Impact               locker.exe; 1,842 files .garnet-locked
(claim)   Exfiltration, to confirm                      1.84 GB out in s.kale's VPN session vs note's 1.8 GB
"""

REPORT = """EXECUTIVE SUMMARY (for the Managing Director)
Late on Friday 6 November, someone logged in to our VPN as Sachin Kale, who is on leave, using his
password. MFA was not turned on for his account. Within an hour they took an administrator's
credentials, reached the file server and, at 23:42 UTC, locked 1,842 engineering and quality files.
The nightly backup on the network was locked too. The Thursday tape backup is safe and tested.
They claim to have copied 1.8 GB of drawings; our VPN records show 1.84 GB left in that session.

Decisions needed today
  1. Approve the 14-hour restore from Thursday's tape. Work after Thursday 21:00 must be redone.
  2. Make MFA compulsory on the VPN before anyone reconnects.
  3. Reset the adm.rjoshi and s.kale passwords, and all administrator passwords.
  4. Approve the CERT-In report, due 06:31 UTC (6 hours after we noticed, at 00:31).
  5. Do not contact or pay the attackers without legal and insurer advice.

TECHNICAL ANNEX: timeline (timeline.sql), ATT&CK map (attack-map.txt), custody (custody.csv)
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Incident response. This is the seminar where everything comes together. Garnet Precision Engineering makes parts in Chakan, near Pune. Just after midnight on Saturday the seventh of November 2026, the helpdesk logs that the engineering CAD files won't open, and every folder has a new file called RESTORE-FILES.txt. That's ransomware."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("This is what the incident team collected: the VPN log, Windows event logs from the design workstation eng-ws14 and the file server fs02, a process export, and saved output from Volatility, Hayabusa and Velociraptor. Over the next twenty minutes we take custody, rebuild the night on one timeline, follow the attacker through the process tree and memory, name every step in ATT&CK, and write the report. Everything you'll see is real software on a real Linux machine."),
 close("files"),
 term,

 chapter("1. Take custody of the evidence"),
 say("Step one: take custody of the evidence. If this case ever reaches the police, an insurer or a court, someone will ask whether the evidence was changed after you received it. Two things answer that. Hashes, the fingerprint of each file. And a chain of custody, a log of who handled which file, when, and what its hash was. sha256sum fingerprints every file we received, and tee saves the list."),
 cmd("find . -type f ! -name '*.py' ! -name '*.sql' ! -name 'custody*' | sort | xargs sha256sum | tee custody-hashes.txt | cut -c1-16,65-", 3.5),
 after("Sixteen files, each with a hash. If anyone changes even one byte later, its hash changes completely. Now the custody log: who received what, and when."),
 edit("custody.csv"),
 write(CUSTODY, cps=40),
 save_note(),
 close("note"),
 clear,

 chapter("2. What happened, in one look"),
 say("Step two: what happened, in one look. Start from the damage and work backwards. Three files: the ransom note, the listing of the encrypted share, and the backup report."),
 cmd("cat suspect/RESTORE-FILES.txt", 2.5),
 after("Files renamed to garnet-locked, backups and shadow copies gone, and a threat to publish 1.8 gigabytes of drawings in 72 hours. Ransom notes lie, so we check every claim."),
 cmd("tail -n 12 share_listing.txt | cut -c1-90", 3),
 after("The renames start at 23:42 UTC on Friday, and the file server's audit counts 1,842 files. Engineering and Quality, both hit. Now, what is left to restore from?"),
 cmd("cat backups.txt", 3.5),
 after("The nightly backup was on a network share the file server could reach, so it's encrypted too. The shadow copies were deleted at 23:41. But the weekly tape from Thursday night was taken off site and test-restored on Friday morning. That's our way back: fourteen hours, and everything saved after Thursday 21:00 is lost unless it exists somewhere else. Three facts: what was encrypted, when it started, and what is left."),
 clear,

 chapter("3. Rebuild the night on one timeline"),
 say("Step three: rebuild the night on one timeline. Every system keeps its own log, and none tells the whole story. This saved DuckDB script reads the VPN log, every Windows event log and the file server's process export, turns each into the same three columns, time, source and event, and sorts them together."),
 edit("timeline.sql", "code", (120, 60, 1700, 960)),
 wait(5),
 after("Three views, one per kind of log, then one query that joins them and keeps 22:40 on Friday to one in the morning. The VPN log and Windows both use UTC, so they line up directly."),
 close("code"),
 cmd("duckdb < timeline.sql", 5),
 after("Read it top to bottom. 22:43, a failed VPN login for s.kale from 203.0.113.140, with MFA not enrolled. A minute later, the right password. 22:52, a remote desktop logon to eng-ws14, type 10, from the VPN address. Then whoami, net group Domain Admins, nltest: someone learning where they are. 22:58, a download. 23:05, a memory dump of lsass, the process that holds passwords. 23:20, adm.rjoshi logs on to fs02 over the network from eng-ws14, and a service called WinUpdSvc is installed. 23:41, shadow copies deleted. 23:42, the locker runs. And 00:58, IT cuts the VPN session."),
 cmd("cat hr_note.txt", 2.5),
 after("And the human fact that changes everything: Sachin Kale is on medical leave in Nashik and hasn't asked for remote access. Whoever used his account wasn't him."),
 clear,

 chapter("4. The process tree, from a shell to the keys"),
 say("Step four: the process tree. Every program has a parent, and the tree shows who started what. The same short Python script we used in the foundation seminar builds it from the process export, one machine at a time. First the workstation."),
 cmd("python3 tree.py eng-ws14", 4),
 after("Under s.kale's remote desktop session, one cmd window starts everything: whoami, net group, nltest, then a hidden PowerShell that downloads r.zip and unpacks it to C:\\Users\\Public. Then rundll32 with comsvcs.dll MiniDump 724: a tool already on every Windows machine, used to copy the memory of process 724, which is lsass. Then nt.exe reads that dump, and px.exe connects to 10.50.1.12, the file server, as adm.rjoshi, with a hash instead of a password. Now the file server."),
 cmd("python3 tree.py fs02", 4),
 after("The backup agent at 21:00 is normal. At 23:20 WinUpdSvc starts as SYSTEM, copies locker.exe from the workstation, deletes the shadow copies, turns off boot recovery, and runs the locker on D:\\Shares."),
 clear,

 chapter("5. Memory, what the RAM remembered"),
 say("Step five: memory. The incident team took a memory image of eng-ws14 at 01:14 and ran Volatility 3 on it, the standard open-source tool for reading memory. The image is thirty-two gigabytes and stays in the evidence locker; this is the output they saved."),
 cmd("sed -n '4,16p' captured/volatility-eng-ws14.txt | cut -c1-150", 3.5),
 after("pslist shows something the logs can't: exit times. rundll32 ran for fourteen seconds and exited, nt.exe ran for twenty-eight, but px.exe was still running when the image was taken. And look at the session column: everything the attacker started is in session 3."),
 cmd("sed -n '17,33p' captured/volatility-eng-ws14.txt | cut -c1-170", 4),
 after("cmdline gives the full arguments, including the NTLM hash for adm.rjoshi. netscan shows px.exe connected to 10.50.1.12 on port 445, file sharing, at 23:19:51. And sessions: session 3 is RDP, GARNET slash s.kale. Session 1 is the console, n.gokhale, who was legitimately working on a drawing. Memory proves the attacker's commands came through the remote desktop, not from the person at the desk."),
 clear,

 chapter("6. The file server, how they arrived"),
 say("Step six: the file server. On fs02 the same night looks like an administrator logging on over the network and installing a service, which administrators do all the time. So we read the details. First, Hayabusa's results. Hayabusa scans Windows event logs for known attack patterns."),
 cmd("cut -d, -f1,2,3,6 captured/hayabusa-fs02.csv | column -s, -t | cut -c1-140", 3.5),
 after("A network logon with NTLM from the workstation, admin rights, and six seconds later a new service installed from a suspicious path. Hayabusa calls that remote service creation with the pass-the-hash pattern. Then the shadow copies, boot recovery, a program in ProgramData, and a mass rename: 1,842 files in sixty seconds. Now Velociraptor's list of services."),
 cmd("cut -d, -f1,3,5,7 captured/velociraptor-fs02-services.csv | column -s, -t", 3),
 after("Every service was created in March 2025 except one: WinUpdSvc, created at 23:20:09 on the night. A name that sounds like Windows Update, a program in C:\\Windows, and running as LocalSystem. And Microsoft Defender is stopped."),
 clear,

 chapter("7. Map the attack to ATT&CK"),
 say("Step seven: map the attack to ATT&CK. MITRE ATT&CK gives each attacker behaviour a shared name and number, so a reader at the insurer or at CERT-In knows exactly what you mean. One line per step on the timeline: the time, the technique, and the evidence that proves it."),
 edit("attack-map.txt", "note", (60, 60, 1800, 940)),
 write(ATTACK, cps=44),
 save_note(),
 after("Nine techniques, each with its proof. The last line is honest: the exfiltration is a claim, and 1.84 gigabytes leaving in s.kale's VPN session supports it, but we still have to confirm it."),
 close("note"),
 clear,

 chapter("8. Decide under pressure"),
 say("Step eight: decide under pressure. Responders make calls before they have all the facts, and every call costs time. On the course site the tabletop puts you in the incident lead's chair. Here are the moments it puts you through."),
 cmd("jq -r '.nodes[] | \"\\(.title)  \\(.text)\"' tabletop-garnet-ransomware.json | cut -c1-160", 4),
 after("Play it once as the incident lead and once as the managing director. The lessons that matter most: isolate, don't switch off, because memory is evidence; close the way in before you restore; and start the CERT-In clock when you noticed."),
 clear,

 chapter("9. Executive summary and technical annex"),
 say("Step nine: one report, two readers. The summary is for the managing director: half a page, no jargon, ending with the decisions needed today. The rest is the technical annex for IT, the insurer and CERT-In."),
 edit("report.txt"),
 write(REPORT, cps=40),
 save_note(),
 after("No technique numbers, no hashes, nothing the managing director has to look up. The annex points to the timeline, the ATT&CK map and the custody log we built today."),
 close("note"),
 clear,

 chapter("10. Hand in"),
 say("Step ten: hand in. On the course site the notebook carries every answer, every tool result, the chain of custody, the timeline and the report."),
 cmd("ls -l *.txt *.csv *.sql", 2.5),
 chapter("Wrap-up"),
 say("That's a full incident, from custody to the boardroom. One password with no second factor let an attacker into the VPN. A remote desktop, a few discovery commands, a credential dump with a tool that's already on every Windows machine, a stolen administrator hash, a fake service, deleted shadow copies, and an encrypted share with a threat to leak. You traced every step through logs, the process tree and memory, named it in ATT&CK, and wrote it for two readers. Turn on MFA everywhere it's missing. Next, in Breach clocks, we go deeper into exactly who you have to tell, and by when. Thank you for watching."),
 wait(2),
]

build("s05-incident-response", scenes, host="garnet-ir", files={"tree.py": TREE, "timeline.sql": TIMELINE})

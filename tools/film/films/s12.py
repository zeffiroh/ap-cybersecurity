from kit import REPLAY, after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

TIMELINE = """CREATE VIEW vpn AS
  SELECT strptime(split_part(line, ' ', 1), '%Y-%m-%dT%H:%M:%SZ') AS ts, 'vpn01' AS source,
         regexp_replace(line, '^\\S+ \\S+ ', '') AS event
  FROM read_csv('vpn.log', columns = {'line': 'VARCHAR'}, delim = '\\t', header = false, quote = '', escape = '')
  WHERE line NOT LIKE '%result=failure%';

CREATE VIEW win AS
  SELECT json_extract_string(json, '$.TimeCreated')::TIMESTAMP AS ts, 'pay-app01' AS source,
         json_extract_string(json, '$.EventID') || '  ' || coalesce(
           json_extract_string(json, '$.Data.TargetUserName') || ' type ' || json_extract_string(json, '$.Data.LogonType')
             || ' from ' || json_extract_string(json, '$.Data.IpAddress'),
           json_extract_string(json, '$.Data.CommandLine'),
           json_extract_string(json, '$.Data.SubjectUserName') || ' ' || split_part(json_extract_string(json, '$.Message'), chr(10), 1)) AS event
  FROM read_ndjson_objects('eventlogs/pay-app01-Security.jsonl');

CREATE VIEW cloud AS
  SELECT "time"::TIMESTAMP AS ts, 'cloud' AS source,
         identity || '  ' || action || '  ' || coalesce(resource, '') || '  ' || result || '  ' || source_ip AS event
  FROM read_json_auto('cloud/audit.json');

.maxrows 80
SELECT strftime(ts, '%H:%M:%S') AS utc, source, left(event, 100) AS event
FROM (SELECT * FROM vpn UNION ALL SELECT * FROM win UNION ALL SELECT * FROM cloud)
WHERE ts BETWEEN '2027-11-29 02:50' AND '2027-11-29 05:45'
ORDER BY ts;
"""

RULE = """title: Local administrator account logs on over the network
id: 9c41e2a0-7d3b-4a55-8e10-2b1c00000001
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4624
    LogonType: '3'
    TargetUserName: 'localadmin'
  condition: selection
falsepositives:
  - None expected once local admin passwords are unique (LAPS); investigate every hit
level: high
tags:
  - attack.lateral-movement
  - attack.t1078.003
"""

BOARD = """BOARD NOTE   Indigo Ledger   29 Nov 2027, 08:00 UTC   EXERCISE
What happened: an attacker used a former intern's VPN account, which was never closed
and had no MFA, to reach our payroll server and cloud storage. Between 04:22 and 04:52 UTC
they copied payroll exports for 4 clients: 2,505 employees' names, salaries, bank
accounts and PANs. 12 are EU staff of Fjord Design. One client is an RBI-regulated bank.

Done: VPN account disabled, backup key revoked and reduced, localadmin passwords reset,
CERT-In filed (due 11:35 UTC). Our four clients decide and notify; we told them at 07:30.

DECISIONS NEEDED TODAY
  1. Approve MFA on the VPN for every account by Friday; no exceptions.
  2. Approve a leaver check: every account closed on the last working day, audited monthly.
  3. Approve paid identity monitoring for the 2,505 people, offered through the clients.
  4. Name one director to speak to clients and press; nobody else comments.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Capstone B: a breach across teams. This is the last seminar in the series, and it has no hints. Indigo Ledger is a payroll company in Pune. It runs payroll for other companies, so the data at risk belongs to its clients' employees: names, salaries, bank accounts and PAN numbers."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("On Monday the twenty-ninth of November 2027, a cloud alert fires about a payroll bucket. The trail runs through the VPN, the office network, a Windows application server and the cloud account. Your job is all of it: rebuild, scope, contain, file and notify on time, leave detections behind, and brief the board. It's an exercise set after the DPDP duties begin, so check the current rules before a real one. One real Linux machine, every tool from the series."),
 close("files"),
 term,

 chapter("1. Brief, custody, plan"),
 say("Step one: with no hints, the order you work in is the only guide you have. Read the alert, hash every file, and write a short plan."),
 cmd("cat cloud/egress-alert.txt", 3),
 after("Twelve objects, 612 megabytes, read by the backup key from an address it never uses. Noticed by the on-call analyst at 05:35 UTC. That's when the CERT-In clock starts: six hours, so 11:35."),
 cmd("find . -type f ! -name '*.sql' ! -name '*.py' ! -path './rules/*' | sort | xargs sha256sum | tee /tmp/custody.txt | cut -c1-16,65-", 3),
 after("Twelve files fingerprinted. The plan: front door, network, server, cloud, one timeline, scope, contain, file, detect, report."),
 clear,

 chapter("2. How they got in"),
 say("Step two: the cloud key had to come from somewhere. Start at the front door, the VPN, and the alert's address."),
 cmd("grep -c 198.51.100.150 vpn.log; grep 198.51.100.150 vpn.log | grep -o 'result=[a-z]*' | sort | uniq -c", 3),
 cmd("grep 198.51.100.150 vpn.log | grep success", 2.5),
 after("Seventeen failures for seventeen different users, then one success: intern.payroll, with MFA not enrolled. One password tried against many accounts is a password spray. Who is intern.payroll?"),
 cmd("grep intern.payroll identity/users.csv", 2.5),
 after("A former intern who left on the thirty-first of July. Still active. Still in VPN-Users and IT-Scripts-Read. No MFA."),
 clear,

 chapter("3. Across the network"),
 say("Step three: once inside, an attacker needs to know what's there. Zeek's conn.log records every connection; smb_files.log records files opened on Windows shares."),
 cmd("awk -F'\\t' '$3==\"10.80.9.33\" && $6==445 {print $12}' zeek/conn.log | sort | uniq -c", 3),
 cmd("awk -F'\\t' '$3==\"10.80.9.33\" {print $5, $6, $7}' zeek/smb_files.log", 3),
 after("Forty-six tries on port 445: thirty-seven refused, nine worked. A sweep. Then two files opened on the IT scripts share, and one file written to pay-app01's C drive: t.ps1. What was in the script they read?"),
 cmd("cat captured/backup-config.ps1.txt", 3),
 after("Two secrets in one file. The password for the localadmin account, used on every application server. And the cloud backup key. Two doors, one script."),
 clear,

 chapter("4. On the application server"),
 say("Step four: pay-app01's Security log, every event for localadmin."),
 cmd("jq -r 'select((.Data.TargetUserName // .Data.SubjectUserName)==\"localadmin\") | [.TimeCreated[11:19], .EventID, .Data.IpAddress // \"\", .Data.CommandLine // \"\"] | @tsv' eventlogs/pay-app01-Security.jsonl", 4),
 after("04:05, a network logon from the VPN address with special privileges. 04:13, the script runs. 04:31, every CSV in D:\\exports compressed into e.zip. 04:52, curl uploads it to a file drop site. 05:01, the zip and the script deleted. 05:02, event 1102: the audit log was cleared. But the export happened before the clearing, and we have it."),
 clear,

 chapter("5. In the cloud"),
 say("Step five: the second door was the backup key. The cloud audit trail records every call."),
 cmd("jq -r '.[] | select(.source_ip==\"198.51.100.150\") | [.time[11:19], .action, (.resource // \"\"), .result] | @tsv' cloud/audit.json", 4),
 after("Who am I, list the bucket, then twelve downloads, three months each for four clients. Then an attempt to change the bucket policy, denied. Two routes out: the zip from the server, and the files straight from the cloud."),
 clear,

 chapter("6. One timeline"),
 say("Step six: four sources, one clock. The same DuckDB approach as the incident response seminar: one view per source, then one sorted query. VPN failures are left out; we counted them already."),
 cmd("duckdb < timeline.sql", 5),
 after("02:58 the VPN login. 04:05 localadmin on the server. 04:20 to 04:24 the cloud downloads. 04:31 to 04:52 the server export. 05:02 the log cleared. And 05:40 the cloud administrator signs in with MFA to respond."),
 clear,

 chapter("7. Scope"),
 say("Step seven: whose data, and how much. Every clock and every notice depends on these numbers."),
 cmd("column -t -s, clients.csv", 2.5),
 cmd("tail -n +2 clients.csv | awk -F, '{s += $2} END {print s, \"people\"}'", 2.5),
 after("2,505 people across four clients. Coral Small Finance Bank is regulated by the RBI. Fjord Design has twelve EU staff on secondment, so GDPR may apply. And remember who's who: Indigo is the processor; its four clients are the data fiduciaries, who decide and notify."),
 clear,

 chapter("8. Contain and fix"),
 say("Step eight: order matters. Cut off access, keep the evidence, then fix the causes. For the cloud we replay every recorded call against the current policy, and then against a draft where the backup key can only upload."),
 cmd("python3 replay.py cloud/policies.json 198.51.100.150 | head -n 2", 3),
 cmd("jq '(.identities[] | select(.name==\"payroll-backup\") | .policies) = [{\"name\":\"upload-only\",\"statements\":[{\"effect\":\"Allow\",\"actions\":[\"PutObject\"],\"resources\":[\"bucket/payroll-exports/*\"]}]}]' cloud/policies.json > policies-new.json && python3 replay.py policies-new.json 198.51.100.150", 3.5),
 after("Fourteen attacker actions allowed before. Zero after, and the nightly upload still works: zero and zero. Then the rest, in order: disable intern.payroll and close every leaver account, revoke the backup key, reset every localadmin with a unique password, and take the secrets out of the script."),
 clear,

 chapter("9. File and notify"),
 say("Step nine: on the course site, the CERT-In tool takes the filing and delivers new facts to your inbox as time passes. The filing needs the indicator, 198.51.100.150; how they got in, the VPN account; which cloud storage was read; and what you've done. Due 11:35 UTC. And because Indigo is the processor, its first notice goes to its four clients, without delay, so they can meet their own duties."),
 clear,

 chapter("10. Leave detections behind"),
 say("Step ten: two detections. First, a search for VPN failures counted by source address: a spray shows up as one address and many users."),
 cmd("grep result=failure vpn.log | grep -o 'src=[0-9.]*' | sort | uniq -c | sort -rn", 3),
 say("Second, a Sigma rule for the local administrator logging on over the network."),
 cmd("sed -n '6,13p' rules/localadmin-network.yml", 2.5),
 cmd("zircolite -e eventlogs/pay-app01-Security.jsonl -r rules/localadmin-network.yml 2>&1 | grep -E 'Matched|Detections'", 6),
 after("One hit, at 04:05, and none for svc-backup or c.iyer. With unique local passwords, this rule should almost never fire, so every hit is worth a look."),
 clear,

 chapter("11. Brief the board"),
 say("Step eleven: two readers. The technical report carries the timeline, scope, root cause and indicators. The board note puts the decisions first."),
 edit("board-note.txt"),
 write(BOARD, cps=42),
 save_note(),
 close("note"),
 clear,

 chapter("12. Hand in"),
 say("Step twelve: hand in. Every file hashed, the timeline, the cloud policy at zero and zero, CERT-In filed, both detections tested, and both documents written."),
 cmd("ls -l *.txt *.json *.sql rules/", 2),
 chapter("Wrap-up"),
 say("That's a breach across every team, handled by one person. A sprayed password on an account that should have been closed, a network sweep, a script holding two secrets, a reused local admin password, and salary files out by two routes. You rebuilt it on one clock, counted 2,505 people, contained it in order, proved the cloud fix at zero and zero, put the clients first as the fiduciaries, left two detections behind, and wrote a board note that asks for decisions. That's the last of thirteen seminars. Well done, and thank you for watching."),
 wait(2),
]

build("s12-capstone-b", scenes, host="indigo-ir",
      files={"timeline.sql": TIMELINE, "replay.py": REPLAY, "rules/localadmin-network.yml": RULE},
      setup=["echo \"alias zircolite='python3 /opt/zircolite/zircolite.py -j --no-event-filter --flatten-backend python -l /tmp/zircolite.log -o /tmp/detected.json'\" >> ~/.bashrc"])

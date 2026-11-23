from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

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
WHERE ts BETWEEN '2026-11-06 22:40' AND '2026-11-07 00:00'
ORDER BY ts;
"""

STARRED = """STARRED EVENTS  Garnet Precision Engineering  6-7 Nov 2026, all times UTC
22:43:02  vpn01    failed VPN login for s.kale from an outside address (bad password)
22:44:10  vpn01    success for s.kale, MFA not enrolled: the way in
22:52     eng-ws14 remote desktop logon for s.kale from the VPN address: first machine
23:05     eng-ws14 rundll32 opens lsass with full access: credential theft
23:20:03  fs02     network logon from ENG-WS14 as adm.rjoshi, special privileges: stolen credentials worked
23:20:09  fs02     new service WinUpdSvc, a name made to look like Windows Update
23:41     fs02     shadow copies deleted with vssadmin
23:42     fs02     locker.exe starts encrypting D:\\Shares
Note: the VPN session sent out about 1.84 GB before it closed at 00:58: probably data theft.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. During an incident, every system keeps its own log, and none of them tells the whole story. Today you'll put a VPN log, two Windows machines' event logs and a process export on one clock, and read the night of a ransomware attack from beginning to end."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Garnet Precision Engineering in Chakan, near Pune. The night of Friday the sixth to Saturday the seventh of November 2026. All times are UTC, and that matters: the VPN log and the Windows logs use the same UTC clock, so we can merge them directly. Just after midnight, a helpdesk ticket said the CAD files wouldn't open and every folder had a file called RESTORE-FILES.txt."),
 close("files"),
 term,

 chapter("1. Rebuild the night on one timeline"),
 say("The merged timeline reads all the logs together and sorts every event by time. This saved DuckDB script turns each log into the same three columns, then keeps the window that matters, from 22:40 on Friday to midnight."),
 edit("timeline.sql", "code", (120, 60, 1700, 960)),
 wait(5),
 close("code"),
 cmd("duckdb < timeline.sql", 6),
 after("Read it top to bottom. At 22:43 the VPN log shows a failed login for s.kale from an outside address. At 22:44:10, a success for the same account, and MFA says not enrolled. That's the way in: one password and no second factor. At 22:52 the workstation eng-ws14 logs a remote desktop logon for s.kale, coming from the address the VPN gave out. At 23:05 rundll32 opens lsass, the process that holds logged-in users' credentials. That's credential theft. At 23:20 the file server fs02 logs a network logon from ENG-WS14 as adm.rjoshi, an admin account. Six seconds later fs02 installs a new service, WinUpdSvc, a name made to look like Windows Update. At 23:41 the shadow copies are deleted, and at 23:42 locker.exe starts encrypting."),
 cmd("grep 'user=s.kale' vpn.log | grep session | cut -c1-170", 3),
 after("And the VPN session, when the admin finally closed it, had sent out about one point eight gigabytes. That means data was probably copied out before encryption."),
 clear,

 chapter("2. Star the events that tell the story"),
 say("Now star the events that tell the story, and notice the gaps. A quiet stretch can mean the attacker was busy somewhere you have no log for."),
 edit("starred-events.txt"),
 write(STARRED, cps=50),
 save_note(),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 5, Incident response: ransomware, lateral movement and memory. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. Put every log on one clock, in one time zone. Read the events in order and name each step: the way in, the first machine, the stolen credentials, the file server, the encryption. Star the events that tell the story, and notice the gaps. One timeline turns five confusing logs into one clear night. Thank you for watching."),
 wait(2),
]

build("t-a-timeline-from-three-logs", scenes, host="garnet-ir", files={"timeline.sql": TIMELINE})

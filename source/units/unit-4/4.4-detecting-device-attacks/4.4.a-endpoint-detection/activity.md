# In-class activity, 4.4.a Endpoint detection and response (EDR)

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students analyze a printed or on-screen EDR telemetry log and practice triage: deciding whether
each event sequence is benign or suspicious, naming the EDR detection method that would catch it,
and selecting the correct response action. Ties to LO 4.4.A (describe how EDR detects and
responds to attacks on devices).

## Materials (all local)
- the SimLab simulation on each machine, or the printed event table below.
- One copy of the response-action reference card (from the Key Terms section of `atom.md`).

## Printed event table (use if devices are unavailable)

| # | Process       | Parent       | Network destination | File write           |
|---|---------------|--------------|---------------------|----------------------|
| 1 | powershell.exe | winword.exe | 203.0.113.44:443    | C:\Temp\svc32.exe    |
| 2 | chrome.exe    | explorer.exe | google.com:443      | (none)               |
| 3 | cmd.exe       | svchost.exe  | (none)              | C:\Windows\malw.bat  |
| 4 | notepad.exe   | explorer.exe | (none)              | report.txt           |
| 5 | wscript.exe   | outlook.exe  | 198.51.100.7:80     | C:\Users\temp.vbs    |

## Steps
1. **Individual read (3 min).** Each student reads the event table silently and marks each row
   as "benign" or "suspicious" with a brief reason.
2. **Pair discussion (7 min).** Partners compare judgments. For each row marked suspicious they
   must name: (a) which telemetry stream surfaced it (process/file/network), (b) whether
   signature or behavioral detection would catch it, and (c) the correct EDR response action
   (alert only, kill process, isolate endpoint, quarantine file).
3. **Group debrief (10 min).** Each pair shares one finding. Instructor uses rows 1, 3, and 5 to
   illustrate living-off-the-land patterns; rows 2 and 4 to show why not every unusual-looking
   event is malicious (context matters).
4. **Scenario extension (5 min).** Ask: "Row 1 executed before the EDR had a signature for the
   payload. Why might behavioral detection still flag it?" Students write one sentence answer.

## Collaborate (AP skill 4)
Assign roles: one partner is the SOC analyst (makes the triage call), the other is the threat
hunter (must justify or challenge each call with a second hypothesis). After the debrief, swap
roles and repeat for a second set of rows provided by the instructor.

## Exit ticket
Each student submits: for event row 1, name the telemetry streams involved, the detection method
that would catch it, and the EDR response action you would choose, and explain why isolation is
preferred over just killing the process.

## Instructor notes
- Expected suspicious rows: 1, 3, 5 (all three use legitimate OS tools as parents from unusual
  parents and write suspicious files or call out to external IPs).
- Benign rows: 2 (Chrome opened normally by explorer, no file write), 4 (Notepad writing a text
  file, normal parent).
- Common stumble: students mark row 3 benign because cmd.exe is a legitimate tool. Clarify that
  svchost.exe spawning cmd.exe is highly unusual; the file write to Windows directory escalates it.
- Feeds unit project (device-attack detection report) and scenario stage 4 (incident triage).
- Row IP addresses use RFC 5737 / RFC 3849 documentation ranges, they are not real targets.

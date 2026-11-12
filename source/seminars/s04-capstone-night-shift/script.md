# Lecture script: Capstone A: the night shift

Seminar 4 · Capstone · about 270 minutes of lab work · the video runs about 10 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

This is Capstone A, the night shift. You're the overnight analyst at a managed SOC, covering a credit union whose working day is your night. The queue has twelve alerts and no severities. One real intrusion is hiding in it. In this capstone the steps tell you what to deliver, not how, and every hint you open costs a point. I'll walk the whole shift once so you see what good looks like.

## 1. Start of shift

Start of shift. Before touching anything, hash the evidence and read the queue end to end. Twelve alerts. Write down your first guess of which ones belong together; we'll test it.

On screen: the step text, the Linux cell.

## 2. Work the queue

Every alert gets a disposition and a reason that points at evidence. Five of them are on, or about, the same Finance laptop, fin-lt04: a download, a scheduled task, a hidden PowerShell, a blocked upload and a DNS alarm. The rest are noise: Caps Lock, a patch window, a printer looking for an old share. One gets "needs more information", with the question we'll ask.

On screen: the step text, the tool with the model answer.

## 3. Scope it with search

Before escalating, we scope it. The laptop sent fifty-nine DNS queries, twice its neighbours. Only one client ever asked for cloudmetric.example. And the proxy blocked an attempt to upload to a paste site. We write the same scoping search in KQL to check ourselves.

On screen: the step text, the tool with the model answer.

## 4. Confirm on the host and the wire

Search results are a summary, so we confirm on the host and on the wire. Sysmon shows the tax tool copied itself as msteams-update.exe and created the task TeamsUpdateCheck. The DNS events show which program made the lookups. In the capture, the tunnel queries start at 11:09 and go to the attacker's name server.

On screen: the step text, the tool with the model answer.

## 5. Check the indicators

We pull out the indicators, check them against the client's intel feed, and map the behaviour to ATT&CK: user execution, a scheduled task, PowerShell, file discovery, and exfiltration over DNS. Defang them before they go anywhere.

On screen: the step text, the tool with the model answer.

## 6. Escalate

One escalation for the whole intrusion. The ask first: isolate the laptop, with a time. Severity high, because data is leaving now. Then what we know, what we don't, and what we have and haven't changed. The client decides; we give them what they need to decide.

On screen: the step text, the tool with the model answer.

## 7. Leave a new detection behind

The client's rule fired thirty-two minutes after the tunnel started. We leave a better one behind: TXT lookups from a program in the user's AppData folder. Browsers and the Windows resolver don't live there. It matches the twenty-six tunnel lookups and nothing else.

On screen: the step text, the tool with the model answer.

## 8. Shift report

We close the shift: the open incident with its owner, the one alert that needs more information, everything closed in one line, what the morning should watch including our new rule, the calls with times, and the number of hints opened.

On screen: the step text, the tool with the model answer.

## 9. Hand in

Hand in the notebook. It carries the queue, the searches, the escalation, the rule and the shift report. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's the shift. Twelve alerts dispositioned, one intrusion scoped to one laptop and one domain, an escalation the client could act on, a new rule that catches the tunnel the old rule was slow to see, and a shift report that leaves nothing behind. Now do it yourself at the Practice level, then Solo, with your hints counted.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:30 1. Start of shift
1:15 2. Work the queue
2:07 3. Scope it with search
4:12 4. Confirm on the host and the wire
5:52 5. Check the indicators
6:42 6. Escalate
7:32 7. Leave a new detection behind
8:22 8. Shift report
9:12 9. Hand in
9:37 Wrap-up
```

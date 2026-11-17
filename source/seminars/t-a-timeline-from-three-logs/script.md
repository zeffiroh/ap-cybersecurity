# Lecture script: Build a timeline from three logs

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-a-timeline-from-three-logs` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-a-timeline-from-three-logs`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-a-timeline-from-three-logs` to refresh this file.

## Opening

Hello, and welcome. During an incident, every system keeps its own log, and none of them tells the whole story. Today you'll put a VPN log, two Windows machines' event logs and a process export on one clock, and read the night of a ransomware attack from beginning to end.

## 1. The setting

The setting. Garnet Precision Engineering in Chakan, near Pune. The night of Friday the sixth to Saturday the seventh of November 2026. All times are UTC, and that matters: the VPN log and the Windows logs use the same UTC clock, so we can merge them directly. Just after midnight, a helpdesk ticket said the CAD files wouldn't open and every folder had a file called RESTORE-FILES.txt. The case folder has the evidence.

On screen: the step text.

## 2. Rebuild the night on one timeline

The merged timeline reads all the logs together and sorts every event by time. Narrow it to the window that matters, from 22:40 on Friday to midnight, and star the events that tell the story. Watch for the gaps, too. A quiet stretch can mean the attacker was busy somewhere you have no log for.

*After it runs:*

Let's read the starred events in order. At 22:43 the VPN log shows a failed login for s.kale from an outside address, a bad password. At 22:44:10, a success for the same account, and MFA says not enrolled. That's the way in: one password and no second factor. At 22:52 the workstation eng-ws14 logs a remote desktop logon for s.kale, coming from the address the VPN gave out. The attacker is now on an engineering PC. At 23:05 Sysmon records rundll32 opening lsass, the process that holds logged-in users' credentials, with full access. That's credential theft. At 23:20:03 the file server fs02 logs a network logon from ENG-WS14 as adm.rjoshi, an admin account, with special privileges. So the stolen credentials worked. Six seconds later fs02 installs a new service, WinUpdSvc, a name made to look like Windows Update. At 23:41 the shadow copies are deleted with vssadmin, so Windows can't restore old versions, and at 23:42 locker.exe starts encrypting D colon Shares. And the VPN session, when the admin finally closed it, had sent out about one point eight gigabytes. That means data was probably copied out before encryption. Download the timeline when you've starred it. Answer the questions: 22:44:10, and the account s.kale.

On screen: the step text, the timeline tool with the model answer.

## 3. Where next

That was one step from Seminar 5, Incident response: ransomware, lateral movement and memory. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. Put every log on one clock, in one time zone. Read the events in order and name each step: the way in, the first machine, the stolen credentials, the file server, the encryption. Star the events that tell the story, and notice the gaps. One timeline turns five confusing logs into one clear night. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-a-timeline-from-three-logs` writes the exact ones)

```
0:00 Opening
0:31 1. The setting
1:00 2. Rebuild the night on one timeline
2:51 3. Where next
3:20 Wrap-up
```

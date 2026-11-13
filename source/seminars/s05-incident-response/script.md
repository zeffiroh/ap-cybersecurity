# Lecture script: Incident response: ransomware, lateral movement and memory

Seminar 5 · about 360 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to incident response. It's just after midnight on Saturday at Garnet Precision Engineering. The helpdesk says nobody can open files on the engineering share, and there's a note on every folder asking for money. You're the responder. Today you'll keep a chain of custody, rebuild the night host by host, show how the attacker got the keys to the kingdom, map it to ATT&CK, make decisions under pressure, and write a report the managing director can act on.

## 1. Take custody of the evidence

Before we read a single line, we hash everything and start a chain of custody: who handled each file, when, and its hash. If this goes to the police or an insurer, that log is what makes the evidence count. We hash the ransom note in the Hex tool and add custody entries as we go.

On screen: the step text, the Linux cell, the tool with the model answer.

## 2. What happened, in one look

Start from the damage and work backwards. Every file ends in dot garnet locked, the first at 23:42. The note also claims 1.8 gigabytes of drawings were copied: double extortion. The shadow copies were deleted and the NAS was on the network, so it's encrypted too. The off-site tape from Thursday survived, which means fourteen hours of restore and a day of lost work.

On screen: the step text, the Linux cell.

## 3. Rebuild the night on one timeline

Now one clock for everything. At 22:44 the VPN accepts s.kale from an outside address, with no MFA, and HR says he's on medical leave at home. At 22:52 an RDP logon to eng-ws14 from the VPN address. At 23:05 something touches lsass. At 23:20 an administrator's account logs on to the file server from that workstation, a service appears, the backups are wiped and the encryption starts. Seven stars tell the whole story.

On screen: the step text, the tool with the model answer.

## 4. The process tree: from a shell to the keys

The process tree follows the attacker's hands. On eng-ws14, the RDP session's cmd runs whoami, asks who the domain admins are, finds the domain controllers, downloads a toolkit with hidden PowerShell, and then rundll32 with comsvcs dot dll dumps lsass to a file. That's where the passwords live. On fs02, a new service starts cmd, which deletes the shadow copies and turns off boot recovery, and then the locker runs.

On screen: the step text, the tool with the model answer.

## 5. Memory: what the RAM remembered

Memory remembers what the logs half-say. lsass is PID 724; rundll32 dumped it and exited. nt dot exe read the dump. Then px dot exe connects to the file server as adm.rjoshi, using a password hash instead of a password. That's pass the hash. Sessions show the attacker in RDP session 3, while the real designer's console session from the evening is still there. Two people, one machine.

On screen: the step text, the Linux cell.

## 6. The file server: how they arrived

On fs02 it looks like an administrator: adm.rjoshi logs on over the network at 23:20, but with NTLM, from a design workstation, on a Friday night. Special privileges, the ADMIN share, and six seconds later a service called WinUpdSvc, running as LocalSystem. Hayabusa marks the shadow copy deletion as critical, and Velociraptor shows the service is still installed. That's the lateral movement.

On screen: the step text, the Linux cell, the tool with the model answer.

## 7. Map the attack to ATT&CK

ATT&CK gives every step a shared name, so an insurer or CERT-In knows exactly what we mean. External remote services and a valid account. RDP. Discovery. Tool transfer and PowerShell. LSASS memory. Pass the hash over admin shares. Service execution. Inhibit system recovery. Data encrypted for impact. Each row has its evidence. And one row stands out: MFA on the VPN would have stopped all of it.

On screen: the step text, the tool with the model answer.

## 8. Decide under pressure

Responders decide before they know everything. Pull the cable but keep the power on, because memory is evidence. Don't pay: it doesn't un-copy the drawings. File with CERT-In within six hours with what you know. Turn on MFA before you rebuild. And tell staff and the customer the truth early. Ten points, and a sentence of reasoning for each call.

On screen: the step text, the tool with the model answer.

## 9. Write the executive summary and the technical annex

Two readers, one report. The summary is for the managing director: what happened in plain words, what it cost, what we're doing, and the three decisions needed today. The annex is for IT, the insurer and CERT-In: timeline, scope, root cause, what we did, indicators and lessons. Notice the summary never says pass the hash.

On screen: the step text, the tool with the model answer.

## 10. Hand in

Hand in the notebook: the chain of custody, the timeline, the process tree marks, the ATT&CK table, your tabletop path and the report. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's the incident from first call to report. A borrowed VPN account without MFA, an RDP session, a memory dump of lsass, an administrator's hash reused on the file server, recovery wiped, and the share encrypted. Every step has a time, a piece of evidence and an ATT&CK technique, and the executive summary says what to decide on one page. Next is seminar six, where the clocks start: who has to be told, and how fast.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:34 1. Take custody of the evidence
1:03 2. What happened, in one look
1:34 3. Rebuild the night on one timeline
2:10 4. The process tree: from a shell to the keys
2:44 5. Memory: what the RAM remembered
3:17 6. The file server: how they arrived
3:48 7. Map the attack to ATT&CK
4:21 8. Decide under pressure
4:51 9. Write the executive summary and the technical annex
5:19 10. Hand in
5:36 Wrap-up
```

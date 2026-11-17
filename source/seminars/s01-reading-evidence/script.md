# Lecture script: Reading evidence: packets, Linux, Windows and network sensors

Seminar 1 · about 360 minutes of lab work · about 15 minutes of narration

This is what `python tools/teach.py demo s01-reading-evidence` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s01-reading-evidence`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s01-reading-evidence` to refresh this file.

## Opening

Hello, and welcome to Reading evidence. Every analyst job, whatever its title, comes down to reading four kinds of evidence: a server's logs, the packets on the wire, a network sensor's summary, and a Windows event log. Each one tells part of the story, and none of them tells all of it. In this seminar we follow one night at Tamarind Health, a chain of clinics in Pune, through all four. Someone guesses a password on the appointments server, gets in, downloads a program, and reaches across the network to a reception PC full of patient scans. You'll find every step of that yourself, with grep, a packet viewer, a Zeek log and the Windows Security log, and by the end you'll write it up so the next person can act. It's a long night, so let's be methodical.

## 1. Take stock of the evidence

Step one: take stock of the evidence. Every case starts the same way. Read the README so you know the machines, the addresses and the time zone. Then list what you were given, and hash it before you open anything. A hash is a fingerprint of a file. If anyone ever asks whether the evidence changed in your hands, the hashes are your proof. The Linux cell lists every file and prints a SHA-256 hash for each one.

*After it runs:*

The README sets the scene. It's the night of the fifth to the sixth of November 2026, and every time is UTC. appt01, at 10.30.1.20, is the MediBook appointments server, running Ubuntu. Its SSH port is forwarded from the internet so the software vendor can support it, which is exactly the kind of decision that comes back to bite. rcp-pc03, at 10.30.2.33, is a reception PC with a share called Scans, full of patient scans and referrals. We have eight files: the server's auth.log, its process list and crontab, a script recovered from its tmp folder, a packet capture from the core switch, a Zeek connection log, the reception PC's Security log, and the README. And an IDS alert started all this at 01:20:11: a possible script download by Wget. Copy the hash list into your notes. Answer the questions: eight files, and appt01 is 10.30.1.20.

On screen: the step text, the Linux cell.

## 2. Linux: who was knocking

Step two: Linux, who was knocking. Port 22 is open to the internet, so auth.log is full of strangers trying passwords. Three small commands do all the work. grep minus c counts the failed passwords. Then grep minus o keeps just the from-address part of each line, sort puts identical addresses together, uniq minus c counts each one, and sort minus r n ranks them, biggest first. The last line does the same for the user names that were tried.

*After it runs:*

Fifty failed passwords in total, and forty-six of them came from one address: 198.51.100.23. One address, dozens of guesses in a short time, that's a brute force. Now look at the names it tried. root, and names that don't exist on this server, like admin, test, ubnt, postgres and oracle, which auth.log marks as invalid user. Those come from a standard list attackers use. But one name does exist: vendor, tried sixteen times. That's the account the software company uses for support. An account that faces the internet and is protected only by a password is the weak point here. Answer the three questions: fifty failures, 198.51.100.23, and forty-six from that address.

On screen: the step text, the Linux cell.

## 3. Linux: the login and what came next

Step three: Linux, the login and what came next. A brute force only matters if it worked, so now we look for the word Accepted. Then we read everything that account did afterwards. sudo lines show each command run as root, because sudo logs the full command. Then we check the two places attackers hide so they can come back: a scheduled job, which Linux calls cron, and a running process. The cell prints the accepted logins, the sudo commands, the recovered script, the crontab and the matching processes.

*After it runs:*

There are two Accepted lines. The first is deploy, logging in with a key from 10.30.0.15, the IT admin PC, at 00:40, as it does every night. That's normal, and it's worth saying so in your notes, so nobody wastes time on it. The second is vendor, from 198.51.100.23, with a password, at 01:19:44. That's our attacker. Twenty-six seconds later, at 01:20:10, sudo runs wget to fetch m.sh from cdn.patch-relay.example into a hidden file in tmp, and at 01:20:31 runs it as root. Read the recovered script. It uses curl to download a.bin, saves it as /usr/local/bin/.sysmon-agent, with a dot at the front so a normal listing hides it and a name chosen to look like monitoring software, and adds a cron line that runs it every ten minutes. The crontab confirms it: the nightly backup line is old and normal, the sysmon-agent line is new. And ps shows .sysmon-agent running as root since 01:21. That's persistence. One more sudo line, at 01:33: smbclient, connecting to a share called Scans on 10.30.2.33 as the user frontdesk. Hold on to that, we'll come back to it. Answer the questions: vendor, the path /usr/local/bin/.sysmon-agent, and 01:19:44.

On screen: the step text, the Linux cell.

## 4. Packets: the download

Step four: packets, the download. Logs tell you what a computer says happened. Packets show what actually crossed the wire. The capture is the core switch's mirror port from 01:15. In the packet viewer, a display filter keeps only the packets you ask for. We'll start with every HTTP request, then everything to or from the download server, and then the same question on the command line with tshark.

*After it runs:*

http.request finds two requests, both to cdn.patch-relay.example at 203.0.113.77. The first fetches /m.sh with the User-Agent Wget, which matches the sudo line exactly. The second fetches /a.bin with the User-Agent curl/7.81.0, which matches the line inside the script. So the packets confirm the logs, and that matters: two independent sources telling the same story is much stronger than one. The second filter, ip.addr equals 203.0.113.77, shows every packet to and from that server, and if you follow the first stream you can read the script itself as it travelled. tshark prints the same two requests, one per line, which is how you'd do it on a server with no screen. Answer the questions: the host name is cdn.patch-relay.example, and a.bin was fetched by curl/7.81.0.

On screen: the step text, the Linux cell, the packets tool with the model answer.

## 5. Packets: the beacon

Step five: packets, the beacon. After the download, appt01 keeps calling the same server, but now over TLS, which is encrypted. We can't read what it says. But two things are never encrypted: the timing of the connections, and the server name in the TLS Client Hello, called the SNI. A program that calls the same server at a fixed interval is a beacon: it's checking in for instructions. The first filter shows TLS to 203.0.113.77, and the second shows the DNS lookups for the patch-relay name.

*After it runs:*

Look at the Time column. TLS Client Hellos to 203.0.113.77 at 01:21, 01:31 and 01:41. Exactly ten minutes apart. And what runs every ten minutes? The cron line the script added. So we can link the encrypted traffic to the program on disk without reading a single byte of it. Compare that with the other TLS on the network, to the patient portal and the backup server: those are internal, they go to known names, and they don't tick like a clock. Regular, external, and to a name nobody recognises: that's the shape of a beacon. Answer the question: ten minutes apart.

On screen: the step text, the packets tool with the model answer.

## 6. Network sensor: who talked to whom

Step six: network sensor, who talked to whom. Zeek is a network sensor that writes one line per connection: who opened it, to which address and port, which service, how long it lasted and how many bytes went each way. It's the fastest way to see a whole night at once. The fields are separated by tabs, so the cell uses awk with a tab as the separator to pull out who, to whom, which port and which service, and then counts each pair. The second command shows only the connections to 10.30.2.33.

*After it runs:*

Read the counted pairs. appt01 opened five connections to 203.0.113.77: the two downloads on port 80 and the three beacons on 443, matching the packets exactly. Then the line that should make you sit up: appt01 to 10.30.2.33 on port 445, which is Windows file sharing. Why would an appointments server open a Windows share on a reception PC? It has no reason to. That's lateral movement: the attacker using the first machine to reach the next one. And the biggest transfer of the night? That's the nightly backup at 01:30, internal, to the backup server, as it is every night. Big doesn't mean bad, and saying so in your notes saves the next person a fright. Answer the questions: five connections, and 10.30.2.33.

On screen: the step text, the Linux cell.

## 7. Windows: the hop to reception

Step seven: Windows, the hop to reception. The reception PC saw those port 445 connections as logons, and Windows writes every logon to its Security log. Four event IDs tell the story. 4625 is a failed logon. 4624 is a successful one. Logon Type 3 means over the network, not at the keyboard. 5140 is a share being opened, and 5145 is a file in it being read. The event viewer filters the log by event ID and by the attacker's address, 10.30.1.20.

*After it runs:*

From 01:33:10 to 01:33:50, nine failed logons from 10.30.1.20 for the account frontdesk, one every five seconds. That's another password guess, now against Windows. At 01:34:02, a successful logon, Logon Type 3, over the network. At 01:34:03 the Scans share is opened, and over the next minute six files are read: scan-0411, scan-0412, scan-0413, referral-0414, scan-0415 and lab-0416. Patient scans, a referral and a lab report. Notice the one 4625 at 03:31 on the fifth of November: that's Logon Type 2, the receptionist mistyping at the keyboard, and it isn't part of this. This is where the stakes change. Until now it was a compromised server. Now it's patient health data read by an attacker, and that brings the clinic's legal duties into play. Answer the questions: nine failed logons, the Scans share, and six files.

On screen: the step text, the events tool with the model answer.

## 8. A sensor rule for next time

Step eight: a sensor rule for next time. Finding an attack once is good. Making sure the next one raises an alert by itself is better. We'll turn what we found into two IDS rules that run on every packet. Rule one alerts when a server fetches something with Wget or curl. Rule two alerts on TLS to the beacon's server name. Then we run them on the capture and check two things: they catch the bad traffic, and they stay quiet on the portal, the backup and the database.

*After it runs:*

Five alerts: rule one catches both downloads, and rule two catches all three beacons, and nothing fires on the internal traffic. That's a good rule: it catches what it should and nothing else. Now write one line on what each would miss. Rule one misses a download made with a renamed program or a browser-like User-Agent, but a real server rarely needs Wget or curl to reach the internet, so it's still worth having on servers. Rule two only knows one server name, and attackers change names easily. The more lasting sign is the timing, a call every ten minutes, which you can catch with the Zeek log instead. Answer the question: the two rules give five alerts.

On screen: the step text, the ids tool with the model answer.

## 9. Write the triage note and the network finding

Step nine: write the triage note and the network finding. Two short documents carry all this to the next person: a host triage note for appt01, and a network finding for the hour from 01:00 to 02:00. Each one says what you checked, with the exact commands and filters, so anyone can repeat it, and each keeps facts apart from guesses.

*After it runs:*

Read the model triage note. What fired: the IDS alert at 01:20:11. What I checked: the exact greps on auth.log, the crontab, the process list and the recovered script. What I found: the brute force, the vendor login at 01:19:44, the download, the persistence, and the hop to rcp-pc03. And the part that matters most, what I don't know yet. We have not analysed a.bin. Write exactly that, we have not analysed the binary, not it is probably ransomware. A guess in a triage note becomes a fact by the third person who reads it. Then the network finding: the five connections to 203.0.113.77, the ten-minute beacon, the 445 connection to reception, and the backup, explained as normal. Every next step has an owner, and every time is in UTC.

On screen: the step text, the report tool with the model answer.

## 10. Hand in

Step ten: hand in. Hand in this notebook. It carries every answer, every tool result and both reports. Your teacher marks it with the rubric, and the certificate follows once it's scored.

*After it runs:*

Before you press Hand in, check three things. Every time is UTC. Every fact says where you saw it. And the gaps, the binary we haven't analysed, whether anything left the network, are written down plainly.

On screen: the step text.

## Wrap-up

That's the night, from start to finish. A password guessed on an internet-facing account. A script downloaded and run as root. A program that hides, persists through cron and beacons every ten minutes. And a hop to a reception PC where six patient files were read. You found each step in a different kind of evidence, and the strongest findings were the ones where two sources agreed: sudo and the packets, cron and the beacon, Zeek and the Windows log. That's the skill: read each source carefully, then line them up on one clock. Next, in Log search and detection as code, you'll do the same at scale with a SIEM. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s01-reading-evidence` writes the exact ones)

```
0:00 Opening
1:06 1. Take stock of the evidence
2:40 2. Linux: who was knocking
4:01 3. Linux: the login and what came next
5:58 4. Packets: the download
7:26 5. Packets: the beacon
8:53 6. Network sensor: who talked to whom
10:23 7. Windows: the hop to reception
12:02 8. A sensor rule for next time
13:33 9. Write the triage note and the network finding
15:00 10. Hand in
15:27 Wrap-up
```

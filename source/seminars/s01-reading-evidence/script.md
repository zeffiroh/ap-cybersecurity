# Lecture script: Reading evidence: packets, Linux, Windows and network sensors

Seminar 1 · about 360 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Reading evidence. Every analyst job comes down to reading four kinds of evidence: what a Linux server wrote in its logs, what crossed the wire, what a network sensor summarised, and what Windows recorded. Tonight's case is Tamarind Health, a small chain of clinics. At ten past six this morning, India time, their IDS lit up. We'll read each kind of evidence in turn and finish with a host triage note and a network finding someone else can act on.

## 1. Take stock of the evidence

Every case starts the same way. Read the README so you know the machines, the addresses and the time zone. Then list the files and hash them before you open anything. The hashes are your proof, later, that the evidence didn't change in your hands. Eight files: a Linux server's logs, a capture, a Zeek log and a Windows log.

On screen: the step text, the Linux cell.

## 2. Linux: who was knocking

Port 22 is open to the internet, so auth.log is full of knocking. We count the failed passwords, then count them by address. One address made 46 guesses in about a quarter of an hour, against admin, root, test, oracle, postgres and then vendor. Vendor is a real account here, and that's the one to worry about.

On screen: the step text, the Linux cell.

## 3. Linux: the login and what came next

The brute force worked: an Accepted password for vendor at 01:19:44 from the same address. Twenty-six seconds later, sudo wget fetches a script into a hidden file in /tmp, and runs it. The script downloads a program, names it dot sysmon agent so it looks like monitoring, and adds a cron job every ten minutes. ps shows it running as root. That's persistence.

On screen: the step text, the Linux cell.

## 4. Packets: the download

Now the wire. A display filter keeps only what you ask for. http dot request shows two downloads: m dot sh fetched by Wget, which matches the sudo line, and a dot bin fetched by curl, which matches the script. Filter on the server's address to see every packet to and from it, including the encrypted traffic that comes next. tshark gives the same answer on the command line.

On screen: the step text, the Linux cell, the tool with the model answer.

## 5. Packets: the beacon

After the download, appt01 calls the same server over TLS at 01:21, 01:31 and 01:41. We can't read the content, but we can read the timing and the server name in the Client Hello. Every ten minutes, exactly like the cron line. That's a beacon. The TLS to the portal and the backup server is internal and expected, which is how you tell them apart.

On screen: the step text, the tool with the model answer.

## 6. Network sensor: who talked to whom

Zeek is the network sensor's summary: one line per connection. Counting pairs shows the night at a glance. appt01 opened 5 connections to the download server: two downloads and three beacons. And something new: ten connections to the reception PC on port 445, Windows file sharing. An appointments server has no reason to do that. The biggest transfer is the nightly backup, internal and expected.

On screen: the step text, the Linux cell.

## 7. Windows: the hop to reception

Windows saw those connections as logons. Nine 4625 failures for frontdesk from appt01, then a 4624 success, Logon Type 3, over the network. Then 5140, the Scans share opened, and six 5145 lines, six files read. Patient scans and referrals. That makes this a possible personal data breach, which changes who has to be told and how fast. One older 4625 is the receptionist mistyping at the keyboard, so we leave it out.

On screen: the step text, the tool with the model answer.

## 8. A sensor rule for next time

Now we turn what we found into IDS rules. One rule: a server fetching anything from the internet with Wget or curl. Another: TLS with this server name. Five alerts, two downloads and three beacons, and none on the portal, the backup or the database. Then the honest part: one line on what each rule would miss.

On screen: the step text, the tool with the model answer.

## 9. Write the triage note and the network finding

Two short documents. The host note: what fired, what we checked, with the commands, what we found, what we don't know, and next steps with owners. The network finding: the same shape, about traffic. Notice what isn't in them: no guess about what the program does. We haven't analysed it, so we say that.

On screen: the step text, the tool with the model answer.

## 10. Hand in

Hand in the notebook: the evidence list and hashes, the commands, the filters, the rules and both notes. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's the night at Tamarind Health, read four ways. The Linux log told us how they got in, the packets showed what they fetched and the beacon, Zeek showed who talked to whom, and Windows showed the hop to the reception PC and the patient scans share. Two short documents carry it to the next person. Next, seminar two turns this kind of reading into searches and detection rules.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:35 1. Take stock of the evidence
1:05 2. Linux: who was knocking
1:34 3. Linux: the login and what came next
2:05 4. Packets: the download
2:39 5. Packets: the beacon
3:11 6. Network sensor: who talked to whom
3:43 7. Windows: the hop to reception
4:18 8. A sensor rule for next time
4:47 9. Write the triage note and the network finding
5:15 10. Hand in
5:30 Wrap-up
```

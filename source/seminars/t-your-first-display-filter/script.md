# Lecture script: Your first display filter

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-your-first-display-filter` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-your-first-display-filter`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-your-first-display-filter` to refresh this file.

## Opening

Hello, and welcome. Logs tell you what a computer says happened. Packets show what actually crossed the wire. Today you'll open a packet capture and use display filters to find a script being downloaded onto a server.

## 1. The setting

The setting. Tamarind Health, the night of the fifth to the sixth of November 2026, all times in UTC. The capture, capture.pcap, comes from the core switch's mirror port, starting at 01:15. A mirror port copies every packet that passes through the switch, so this is the clinic network's own recording of that night.

On screen: the step text.

## 2. Packets: the download

In the packet viewer, a display filter keeps only the packets you ask for and hides the rest. The first filter is http.request, which shows only web requests. That's the quickest way to see what was downloaded over plain HTTP. Watch the list shrink.

*After it runs:*

Two requests. Read each row: the source address, the host name and the path. Both went to cdn.patch-relay.example, a name made to look like a software update service. The first fetched /m.sh, a shell script. The second fetched /a.bin, a program. Now open a request and read its User-Agent header, the name the downloading program gives itself. The first says Wget. That matches the sudo line in the server's log, where the attacker ran wget. The second says curl/7.81.0, which matches a line inside the script. So the attacker downloaded the script by hand, and the script then downloaded the program. The second filter widens the view: ip.addr equals 203.0.113.77, every packet to or from the download server. You can follow the stream of the first download and read the script itself as it travelled. Finally, the Linux cell asks tshark, the command-line version of the packet viewer, the same question, and prints one line per request. Same answer from a different tool. Answer the two questions: cdn.patch-relay.example, and curl/7.81.0.

On screen: the step text, the Linux cell, the packets tool with the model answer.

## 3. Where next

That was one step from Seminar 1, Reading evidence: packets, Linux, Windows and network sensors. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. A display filter is a question you ask the capture. Start broad, with http.request, then narrow to one address and follow the stream. The User-Agent tells you which program made a request, and that links the packets to the commands in the logs. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-your-first-display-filter` writes the exact ones)

```
0:00 Opening
0:25 1. The setting
0:47 2. Packets: the download
2:24 3. Where next
2:53 Wrap-up
```

# Lecture script: Your first display filter

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. A packet capture has thousands of packets and you need three. Display filters are how you find them.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. Packets: the download

The capture is the core switch mirror from 01:15 at Tamarind Health. Start with every HTTP request. Then everything to or from the download server. Then follow the stream of the first download to read the conversation. The first request's User-Agent is Wget, which matches the sudo line in the server log. The second is curl, which matches the script. The Linux cell asks tshark the same question on the command line, which is how you do it at scale.

On screen: the step text and the tool.

## 3. Where next

Filters turn a haystack into a story. Seminar 1 continues with the beacon and the network sensor.

On screen: the step text and the tool.

## Wrap-up

Filters turn a haystack into a story. Seminar 1 continues with the beacon and the network sensor.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. Packets: the download
2:47 3. Where next
```

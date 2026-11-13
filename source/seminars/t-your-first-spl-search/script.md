# Lecture script: Your first SPL search

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. A SIEM is only as good as the questions you ask it. Here are your first two searches in SPL.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. SPL: count, then pivot

SPL reads left to right: a search, then a pipe, then a command that works on the results. Stats count by src_ip groups the failures by address, and sort minus count puts the biggest first. Then pivot: take the address you found and search for it again, this time for a success. Field names come from the parsed log: action, src_ip, user, auth_method. Click any field name in the results to add it to the search.

On screen: the step text and the tool.

## 3. Where next

Count, then pivot: that is most of threat hunting. Seminar 2 goes on to rules and the KQL version.

On screen: the step text and the tool.

## Wrap-up

Count, then pivot: that is most of threat hunting. Seminar 2 goes on to rules and the KQL version.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. SPL: count, then pivot
2:47 3. Where next
```

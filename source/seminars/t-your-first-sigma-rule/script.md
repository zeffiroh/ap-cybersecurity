# Lecture script: Your first Sigma rule

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. A hunt you run once finds one attack. A rule finds the next one. Here you write your first Sigma rule.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. From hunt to rule: your first Sigma rule

Sigma is the open format for detection rules: one YAML file that converts to SPL, KQL and more. On hr-pc07, Word started cmd dot exe. The rule fires on that, and on Excel or Outlook doing the same. Press Test and count the matches. Then press Convert with pySigma and compare the real converter's SPL with the search you would write by hand. Why does PowerShell not match? Its parent was cmd, not Word. One rule per step of the chain, or a second rule for cmd starting a hidden PowerShell.

On screen: the step text and the tool.

## 3. Where next

Rules are hunts that never sleep. Seminar 2 is detection as code from end to end.

On screen: the step text and the tool.

## Wrap-up

Rules are hunts that never sleep. Seminar 2 is detection as code from end to end.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. From hunt to rule: your first Sigma rule
2:47 3. Where next
```

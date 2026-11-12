# Lecture script: Log search and detection as code

Seminar 2 · about 300 minutes of lab work · the video runs about 13 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Log search and detection as code. A hunt you run once finds one attack; a rule finds the next one. Today we answer one question three times, in SPL, in KQL and in SQL, on a web server called web01. Then we turn the hunt into Sigma rules, test them for false positives, tune them, and convert them with the real pySigma converter. The search engine here is a teaching subset of each language, and I'll point you to free places to run the full versions.

## 1. One question, three languages

Every hunt starts with a question, not a tool. Ours: did anyone guess an SSH password on web01, get in, and do something with it? Before the search engine, we read the raw log with grep, so we know exactly what the engine is reading. Seven failed passwords, and one address keeps coming back.

On screen: the step text, the Linux cell.

## 2. SPL: count, then pivot

In SPL we search, then pipe into a command. Stats count by source address, sorted biggest first: 203.0.113.7 failed six times. Now we pivot. Same address, but a success this time: the user deploy logged in with a password. And the next search shows deploy used sudo to read the shadow password file. That's the whole story in three searches.

On screen: the step text, the tool with the model answer.

## 3. The same hunt in KQL

KQL starts with a table and pipes into operators: where, summarize, project, sort. The rule is simple: the answer must match SPL. Six failures, one success. If the two languages disagree, one of the searches is wrong, and that check alone catches a lot of mistakes.

On screen: the step text, the tool with the model answer.

## 4. SQL over the same logs

Every log is also a table. The SQL tool names each table after its file and makes a column for each field. Group by client address and the same attacker is at the top of the web log with nine requests. SQL is the language of most data lakes, so it's worth having in your pocket.

On screen: the step text, the tool with the model answer.

## 5. Parse a raw log into fields

Searches only work on fields someone parsed. When a new log arrives that your SIEM doesn't know, you write the parser. This pattern parses eleven of the twelve SSH lines. The one it skips is the sudo line, which has a different shape. Try writing a second pattern for it.

On screen: the step text, the tool with the model answer.

## 6. Hunt the web attack in SPL and KQL

The same address hit the web server. The user agent names the tool, sqlmap, and the requests show the injection. Minutes later the attacker uploaded img.php and ran commands through it. We write that hunt in SPL and in KQL, and both find the same three commands.

On screen: the step text, the tool with the model answer.

## 7. From hunt to rule: your first Sigma rule

Now detection as code. Sigma is the open format for rules: one YAML file that converts to many SIEMs. This rule fires when Word, Excel or Outlook starts a shell, and it matches exactly one event. Then we press Convert, and the real pySigma converter turns it into SPL we can compare with our own.

On screen: the step text, the tool with the model answer.

## 8. Test for false positives, then tune

A rule that fires on everything is worse than no rule. The first one here matches every new process: fifteen hits, most of them normal. The tuned rules each describe one behaviour: a program in the Public folder, shadow copies deleted, a new member of Administrators. Each matches only attack events. Write one tuning note per rule.

On screen: the step text, the tool with the model answer.

## 9. A web rule, tested on the web log

Sigma works on web logs too. The noisy version flags a customer searching for Union Bank and a blog post with an apostrophe in its name. The tuned version keys on the tool name and on UNION SELECT. Six hits drop to four, and all four are the attack.

On screen: the step text, the tool with the model answer.

## 10. Hand in your hunt pack and rule pack

Your hand-in is this notebook: the hunt pack in SPL and KQL, one SQL query, and the rule pack with tests and tuning notes. The rubric is on screen. Check that every rule shows its test result, then press Hand in.

On screen: the step text.

## Wrap-up

That's the hunt pack and the rule pack. You ran the same hunt in three languages and got the same answer, parsed a raw log into fields, and wrote five Sigma rules that each describe one thing an attacker did, each with a test and a tuning note. Hand in this notebook. In seminar three we use these skills on a live alert queue.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:36 1. One question, three languages
1:21 2. SPL: count, then pivot
3:01 3. The same hunt in KQL
4:16 4. SQL over the same logs
5:06 5. Parse a raw log into fields
5:56 6. Hunt the web attack in SPL and KQL
7:36 7. From hunt to rule: your first Sigma rule
8:51 8. Test for false positives, then tune
10:56 9. A web rule, tested on the web log
12:11 10. Hand in your hunt pack and rule pack
12:36 Wrap-up
```

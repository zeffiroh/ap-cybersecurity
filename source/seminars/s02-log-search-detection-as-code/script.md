# Lecture script: Log search and detection as code

Seminar 2 · about 300 minutes of lab work · about 17 minutes of narration

This is what `python tools/teach.py demo s02-log-search-detection-as-code` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s02-log-search-detection-as-code`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s02-log-search-detection-as-code` to refresh this file.

## Opening

Welcome to Log search and detection as code. Chandni Textiles is a fabric and saree business in Surat, with two shops and an online store. On Tuesday morning their developer, Ravi, notices that the shop's database server is busier than it should be overnight, and he asks a simple question: did anyone get into the shop server on Monday night, how, and what did they take? Today we answer that question with a SIEM, the search program at the centre of every security operations centre. We'll learn how the program works first, then run the same hunt three times, in SPL, in KQL and in SQL, because real teams move between search languages all the time. Then we turn what we found into Sigma rules, test them against normal traffic so they don't cry wolf, tune them, and convert them with the real pySigma converter. The search engine you'll use is a teaching subset of each language. I'll tell you where to run the full versions for free.

## 1. How the search program works

Step one: how the search program works. Before you search anything, it helps to know what the program has done with your files. A SIEM reads each log, splits it into events, usually one line or one record each, gives every event a time so that different files line up on one clock, recognises the format, which it records as the sourcetype, and pulls out fields like the source address or the user name. Let's ask the program what it made of the four files we gave it. Star means every event, and stats count by source and sourcetype gives one row per file.

*After it runs:*

Four rows, and 163 events in total. auth.log became syslog, the standard Linux log format. The two web logs became access_combined, the format almost every web server writes. And the Windows log became json, one record per line. Now the second search: only the syslog events, counted by the program that wrote them. Three programs: sshd, the remote login service, sudo, which runs commands as the administrator, and CRON, which runs scheduled jobs. Notice what just happened: we never told the program what a process is. It read the format and made the field for us. Click src_ip in the field list on the left and you'll see the values the program found, with a count next to each. That field list is where most hunts start. Answer the two questions: 163 events, and syslog.

On screen: the step text, the siem tool with the model answer.

## 2. Start with the raw log

Step two: start with the raw log. A good analyst never trusts a search engine blindly. Before we use the program, we read the raw file with grep, so we know exactly what the engine is working from. We count the lines in each file, count the failed passwords, and list the addresses those failures came from, and then the account names they tried.

*After it runs:*

auth.log has 26 lines. Thirteen of them say Failed password. Two came from 192.0.2.81 in the afternoon, both for a user called test that doesn't exist: that's background noise, a scanner trying the same thing on every server on the internet. The other eleven came from one address, 203.0.113.45, between 18:40 and 18:41 UTC, which is just after midnight in Surat. Look at the accounts it tried: root, admin, ubuntu, oracle, deploy, and three times catalog. Most of those are guesses that work on lots of servers. But catalog isn't a common name. It's the account the photo studio uses to upload product pictures. Whoever this is knew something about Chandni Textiles. Keep that in mind. Answer the question: thirteen.

On screen: the step text, the Linux cell.

## 3. SPL: count, then pivot

Step three: SPL, count, then pivot. SPL reads left to right. A search, then a pipe, then a command that works on whatever came through the pipe. We search for failures, count them by source address, and sort the biggest first. Then we pivot: we take what we found and search again from a new angle. First the address, then the account it reached, then where that account normally comes from, and finally what it did.

*After it runs:*

203.0.113.45 failed eleven times. Now the pivot: the word Accepted, from that same address. One result. At 19:20 UTC, catalog logged in with a password. So forty minutes after eleven failures, the attacker had the right password, first time. Hold that thought. The third search shows every SSH event for catalog. At 05:10 in the morning it logged in from 10.30.0.30, the photo studio PC on the office network. That's normal. Then three failures and one success from 203.0.113.45 at night. That's not. And the last search, the sudo log. At 05:10 catalog ran resize-photos, its normal job. At 19:21 the same account ran mysqldump with all-databases, which copies every database on the server into one file, and at 19:23 it compressed that file with gzip. That's somebody packing the shop's data to take away. One more thing to notice: catalog was allowed to run anything as root. It only ever needed one command. Answer the questions: 203.0.113.45, catalog, 10.30.0.30, and mysqldump.

On screen: the step text, the siem tool with the model answer.

## 4. The same hunt in KQL

Step four: the same hunt in KQL. KQL is the language of Microsoft's cloud SIEM and of the Azure Data Explorer. It reads the other way round from SPL: you start with a table, then pipe into operators. where filters, summarize count by groups, project picks the columns, sort by orders them. The table is named after the file, so auth.log becomes auth. The rule for this step is simple: the answer must match SPL.

*After it runs:*

Eleven failures from 203.0.113.45, and the count column is called count underscore, which is how KQL names it. The success pivot gives the same one login as catalog at 19:20. Both languages agree. If they didn't, one of the searches would be wrong, and that habit of checking one language against another catches a surprising number of mistakes. Write down one thing that felt easier in each. Most people find SPL quicker to type and KQL easier to read back a week later. If you want to practise full KQL, the free KC7 game and the free Azure Data Explorer help cluster both run it. Answer the question: eleven.

On screen: the step text, the siem tool with the model answer.

## 5. SQL over the same logs

Step five: SQL over the same logs. Every log is also a table, and SQL is the language behind most data lakes, where companies keep logs for a year or more. The SQL tool turns each file into a table named after it and makes a column for each field. We'll count web requests per client address, then look for the word UNION in the requested addresses.

*After it runs:*

Ten different addresses visited the shop on Monday. At the top, with twelve requests, is 203.0.113.45 again. The shoppers made four or five each. The second query finds three requests with UNION in them, all from that same address. UNION is a word from SQL itself, and when it turns up inside a web address, someone is usually trying to make the website's own database answer a question it was never meant to answer. That's the bridge between the two logs: the same address tried passwords on SSH and then attacked the website. Answer the question: twelve.

On screen: the step text, the sql tool with the model answer.

## 6. Parse a raw log into fields

Step six: parse a raw log into fields. Searches only work on fields that someone parsed. When a log arrives that your SIEM doesn't recognise, a firewall nobody has heard of, or a homemade application, you write the parser. The log parser here uses percent-brace pieces, like SYSLOGTIMESTAMP or IP, the same idea as Grok in log pipelines. This pattern describes an SSH login line.

*After it runs:*

Sixteen of the twenty-six lines parse: every Failed and Accepted line, with the time, host, process ID, result, method, user, source address and port in their own columns. The ten red lines are the three sudo lines, the six CRON lines and the disconnect line. That's correct. A parser should only claim lines it understands. A parser that forces everything into the same columns quietly produces wrong data, and wrong data is worse than missing data. Now try writing a second pattern for the sudo lines. The hint gives you a start. Answer the question: sixteen.

On screen: the step text, the parse tool with the model answer.

## 7. Hunt the web attack in SPL and KQL

Step seven: hunt the web attack. The password guessing failed. So how did the attacker have catalog's password forty minutes later? Let's read the web log. We look for the tool's name in the user agent, then everything the same address did in the admin pages, and then we write the admin hunt in KQL to check ourselves.

*After it runs:*

Seven requests carry sqlmap in the user agent. sqlmap is a free tool that automates SQL injection. Read them in order. At 19:02 it fetched robots.txt. Then product 41 with a single quote on the end, which made the page crash with a 500 error. That's the tell: the quote broke the database query, so the input goes straight into it. Then AND one equals one, and AND one equals two. The first page came back full size, the second much smaller: the database is obeying the attacker's logic. Then UNION SELECT from information_schema, which lists every table, and finally UNION SELECT username and password from a table called staff_users. That's where the password came from. At 19:11 the attacker switched to a normal browser, logged in to the admin pages, and at 19:12 downloaded orders export from the first of January: 4.4 megabytes, every order this year, with customers' names and addresses. At 19:14 they pasted one more UNION query by hand to pull customer email addresses. Then, at 19:20, they logged in to SSH as catalog, because the same password worked there too. The KQL version finds the same four admin requests. Answer the questions: sqlmap, staff_users, and /admin/orders/export.

On screen: the step text, the siem tool with the model answer.

## 8. From hunt to rule: your first Sigma rule

Step eight: from hunt to rule. A hunt you run once finds one attack. A rule finds the next one, automatically. Sigma is the open format for detection rules: one YAML file that converts into SPL, KQL and many other SIEM languages. To practise, we use the Windows log from the accounts PC. On Monday morning, Hetal Desai in accounts opened a spreadsheet called Payment Advice from an email, and Excel started a command shell. This rule fires when Word, Excel or Outlook starts cmd or PowerShell. We test it, then press Convert, which runs the real pySigma converter.

*After it runs:*

There are seventeen process-creation events, event ID 4688, in the log, and the rule matches exactly one: Excel starting cmd.exe at 05:12:58. Convert it and compare the SPL that pySigma writes with what you'd write by hand: it spells out every condition and is more careful with wildcards than most people are. Two things the rule didn't match, and both are right. At 04:58 Excel started splwow64.exe. That's the Windows printing helper, it starts whenever anyone prints from Office, and it's not a shell. And PowerShell didn't match, because its parent was cmd, not Excel. That's the next link in the chain, and it needs its own rule. Answer the questions: seventeen, and one.

On screen: the step text, the siem, sigma tools with the model answer.

## 9. Test for false positives, then tune

Step nine: test for false positives, then tune. A rule that fires on everything is worse than no rule at all, because people learn to ignore it. So every rule gets tested twice: does it catch the attack, the true positives, and does it stay quiet on normal work, the false positives? The first rule here is deliberately noisy: any new process. Tick the events that are really malicious and the tool scores your precision. Then run the three tuned rules, each of which describes one thing an attacker did.

*After it runs:*

The noisy rule matches all seventeen processes, and only about half of them are the attack. Nobody can work with that. The tuned rules each describe behaviour that normal users don't have. Programs started from C-colon Users Public: two hits, WinSvcHost.exe, the program PowerShell downloaded, and rdpw.exe, which it then started to open a connection out to 198.51.100.77 on port 443. Nothing legitimate on this PC runs from the Public folder, because every user can write there. Shadow copies deleted: one hit, vssadmin delete shadows all quiet, at 05:21. That's ransomware preparing the ground, removing the copies Windows keeps for restoring files. And a new member of the Administrators group: one hit, helpdesk_tmp, an account the malware created at 05:14. Under each rule, write a tuning note: what it would miss, and what would make it noisy. Answer the questions: seventeen, helpdesk_tmp, and vssadmin.exe.

On screen: the step text, the sigma tool with the model answer.

## 10. A web rule, tested on two web logs

Step ten: a web rule, tested on two web logs. Sigma works on web logs too. The first version matches a quote, the word UNION, or the tool's name. We test it on the shop's log and also on lookbook_access.log, an hour of normal visitors to the company's lookbook site, to see who it accuses. Then the tuned version, which looks for the tool's name or for UNION SELECT together.

*After it runs:*

The noisy version matches ten requests. Eight are the attack. The other two are a visitor searching for union territory delivery charges, and a blog post called a weaver's diary from Surat, with an apostrophe in its address. Both innocent, and on a busy day there'd be hundreds like them. The tuned rule matches eight, all attack. Look at what catches the request the attacker pasted into a browser at 19:14: not the tool's name, because the user agent said Chrome, but UNION SELECT. That's why the rule keeps two separate selections. An attacker can change the user agent with one flag, but the injection still has to say UNION SELECT, or something very like it. In your tuning note, say what this rule would miss: an attacker who writes union and select with different spacing or mixed case, or uses a different injection technique altogether. Answer the questions: ten, and eight.

On screen: the step text, the sigma tool with the model answer.

## 11. Hand in your hunt pack and rule pack

Step eleven: hand in your hunt pack and rule pack. Your hand-in is this notebook, with every search and rule saved in it. Check the table on screen: the SSH hunt and the web hunt in both languages, one SQL query explained, five Sigma rules each with its test and its tuning note, and the conversions.

*After it runs:*

Then add three sentences for Chandni Textiles, in plain words. How the attacker got in: SQL injection on the product page gave them the staff passwords, and the catalog password worked on SSH too. What they took: every order this year from the admin pages, customer email addresses, and a copy of every database. And the first thing to fix: the injection bug in the product page, followed by new passwords for every staff account and a sudo rule that lets catalog run only resize-photos. Then press Hand in.

On screen: the step text.

## Wrap-up

That's the hunt pack and the rule pack. You learned how a SIEM turns files into events and fields, read the raw log before trusting the engine, and ran one hunt in SPL, KQL and SQL with the same answer each time. You found that the password guessing failed, and that SQL injection on a product page handed the attacker the staff passwords, the customers' orders and, through one reused password, the whole server. Then you wrote five Sigma rules, each describing one thing an attacker does, tested them against normal traffic, and tuned them until they stayed quiet. In seminar three we take these skills to a live alert queue, where the question is no longer what happened, but what needs a person right now. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s02-log-search-detection-as-code` writes the exact ones)

```
0:00 Opening
1:18 1. How the search program works
3:04 2. Start with the raw log
4:22 3. SPL: count, then pivot
6:15 4. The same hunt in KQL
7:40 5. SQL over the same logs
8:56 6. Parse a raw log into fields
10:08 7. Hunt the web attack in SPL and KQL
12:06 8. From hunt to rule: your first Sigma rule
13:43 9. Test for false positives, then tune
15:34 10. A web rule, tested on two web logs
17:14 11. Hand in your hunt pack and rule pack
18:12 Wrap-up
```

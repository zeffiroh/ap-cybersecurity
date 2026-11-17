# Lecture script: Authorised testing: web, APIs and findings that get fixed

Seminar 9 · about 360 minutes of lab work · about 18 minutes of narration

This is what `python tools/teach.py demo s09-authorised-testing` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s09-authorised-testing`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s09-authorised-testing` to refresh this file.

## Opening

Hello, and welcome to Authorised testing: web, APIs and findings that get fixed. The most important word in that title is the first one. A security test and an attack can use the same tools and send the same requests. The difference is a signed letter. In India, getting into a computer system without its owner's permission can be an offence under the Information Technology Act, 2000, whatever your intentions. So this whole seminar runs on one rule: you test only what the owner has asked you, in writing, to test. Our client is NimbuMart Retail, an online shop. NimbuMart has asked for a test of its shop, its API and two staging servers, from Monday the sixteenth to Friday the twentieth of November 2026. Every time in this case is Indian Standard Time. Today you'll turn the letter into rules of engagement, look around inside the lines, prove three weaknesses with as little data as possible, score and rank them, write them so a developer can fix them, retest, and explain it all to the board. The tests themselves are short. Most of the job, and most of this video, is everything around them.

## 1. Authorisation and scope, before anything else

Step one: authorisation and scope, before anything else. Before you open a single tool, you read the letter of authorisation, all of it, and turn it into rules of engagement. Rules of engagement answer seven questions. Who authorised this? Exactly what is in scope, and what is out? When can you test? What may you do, and what may you not? When do you stop, and who do you call? And how do you treat any data you see? The Linux cell prints the letter, engagement.txt. Then the report builder has a rules of engagement template to fill in.

*After it runs:*

The client contact is Ritu Malhotra, Head of Engineering, and the rules of engagement record that the letter was signed on the twelfth of November. In scope: nimbu.shop and its API, 192.0.2.10, shop-staging, and 192.0.2.11, api-staging. Now the line that catches people. 192.0.2.12, pay.nimbu.shop, is out of scope. It sits on the same network, it has a NimbuMart name, and it looks like part of the shop. But the payment provider runs it, and NimbuMart can't authorise a test of something it doesn't own. Only the owner of a system can give permission. Also out: staff, phones and email, so no social engineering; no denial of service or load testing; and nothing that changes or deletes other customers' data. The window is Monday 09:00 to Friday 18:00. The test account is the demo customer. The stop conditions: live card data, real people's personal data, or signs that someone else has already broken in. Our rules add one more: if something breaks. When any of those happens, you stop and call Ritu Malhotra, on the 24-hour number, or Dev Anand in IT operations. Write that number where you'll see it, not in a file you'll have to search for. And data handling: other customers' data only to prove a finding, one record at most, cropped screenshots, no copies leaving the lab, working files deleted after the report. The letter itself says only as much as needed; one record is how we make that concrete. Answer the questions: 192.0.2.12, and Ritu Malhotra.

On screen: the step text, the Linux cell, the report tool with the model answer.

## 2. Recon, inside the lines

Step two: recon, inside the lines. Recon means finding out what's there: which hosts, which services, which versions. The discipline here is simple and easy to forget. Scan only what's in scope, and name each address on the command line. If you scan the whole range out of habit, you hit the payment host, and you've broken the agreement before lunch on day one. The Linux cell runs nmap with version detection against 192.0.2.10 and 192.0.2.11, and nothing else. Then it prints a JavaScript file saved from the staging API.

*After it runs:*

Shop-staging, 192.0.2.10, has two services: SSH on port 22, OpenSSH 9.2, and the website on 443 behind nginx 1.24. API-staging, 192.0.2.11, has the API on 443, also nginx. And a second service, on port 8080: a Node.js Express app whose title says NimbuMart API, staging, debug. A debug service facing the internet is a classic leftover. Developers switch it on to make testing easier and forget it's reachable by everyone. Now the JavaScript file, saved from that debug port at 10:42 on Monday. Read the comment: TODO, remove before release, a token for the demo account so the staging page loads without logging in. That's a login token, sitting in a file anyone can download. We'll come back to it in finding three. Notice what's missing from the scan: 192.0.2.12 never appears, because we never asked for it. Write every command down, with the time. If NimbuMart ever asks whether you touched the payment host, your notes answer for you. Answer the question: 8080.

On screen: the step text, the Linux cell.

## 3. Finding 1: a login that trusts what you type

Step three, finding one: a login that trusts what you type. The shop's login takes your email and puts it straight into a database query. When a program builds a query by pasting in text from the user, the user can change what the query means. That's SQL injection, and here it means the password check never runs. The rules matter more than the trick. We prove it with one request in the web proxy, look at the response, and stop.

*After it runs:*

One request, and the response is status 200, logged in, with the role admin. That's the finding proved. Now the professional part: we stop. We don't open the admin panel, we don't look at other customers, we don't change a price to see if we can. The response already proves that anyone on the internet could do all of that. Going further adds risk to the client and nothing to the report. Why does it work? The server builds one string of SQL with the email inside it, so the database can't tell where the data ends and the instruction begins. The fix is a parameterised query: the query is written with placeholders, and the email and password are passed in separately, so they're only ever treated as data. The SQL injection lab shows the before and after side by side, and Hack the shop has the same login as a mission. And the retest is already decided: after the fix, the same request should get 401, not authorised. Answer the question: 200.

On screen: the step text, the proxy tool with the model answer.

## 4. Finding 2: someone else's order

Step four, finding two: someone else's order. Log in as the demo customer, open one of your own orders, and look at the request. It's slash api slash orders slash, then a number. The question every tester asks is: what if I change the number? If the shop hands over an order that isn't yours, that's an insecure direct object reference, an IDOR. The API checked that you were logged in, but not that the thing you asked for belongs to you.

*After it runs:*

The demo customer's orders are three and four. Ask for order two, and the response is 200, with another customer's order, including a delivery address. One record, and the finding is proved. This is where data handling stops being a line in a document. You have just seen a real person's address. In the report you write: order two belongs to another customer, and it showed a delivery address. You do not write the address down. A report gets emailed, printed and forwarded, and a report that contains customer data is itself a leak. You also don't try orders one, five and six to see how many there are. The fix is one condition in the query: find the order with this ID and the user ID of the caller, taken from their token, never from the request. If there's no match, return 404, not found, so the API doesn't even confirm the order exists. The retest: order two returns 404 for the demo account. Answer the question: 2.

On screen: the step text, the proxy tool with the model answer.

## 5. Finding 3: a token anyone can forge

Step five, finding three: a token anyone can forge. The staging file held a login token, a JWT. A JWT has three parts separated by dots: a header, a payload, and a signature. The header and payload are only encoded, not encrypted, so anyone can read them. The signature is what stops people changing them, and with HS256 it's only as strong as the secret behind it. The JWT inspector decodes the token, then checks the signature against the short wordlist in the case folder. That check happens entirely offline: nothing is sent to NimbuMart's servers, which is why the rules of engagement allow it.

*After it runs:*

The header says HS256. The payload says subject 3, email demo at nimbu.shop, role customer, issued at 05:30 on Monday the sixteenth, and valid for seven days. Then the wordlist: twelve common and company-themed words, and one of them makes the signature match. The secret is nimbu2026: the company's name and the year. That's the whole problem in one word. Whoever knows the secret can sign their own tokens, and the server will believe whatever they say, including role admin. So the finding isn't just that a token leaked. It's that every token on the staging API can be forged. Two fixes, and both are needed. A long random secret, 32 bytes from a vault, not a word a person chose, and rotated now that this one is known. And no token in a public file: take it out of the bundle, put staging behind the VPN, and close port 8080 to the internet. The shop's own mission, Forge a token, shows the other classic JWT mistake: a server that accepts a token with no signature at all. Answer the questions: HS256, and nimbu2026.

On screen: the step text, the jwt tool with the model answer.

## 6. Score and rank

Step six: score and rank. Three findings, one week, a small team. Which comes first? CVSS gives each flaw a base score from zero to ten, built from a few questions. Can it be reached over the network? Is it hard to pull off? Does the attacker need an account? Does a user have to click something? And what does it do to confidentiality, integrity and availability? Then the patch tool ranks the register using more than the score: is the asset on the internet, and is anyone known to be exploiting it?

*After it runs:*

The login bypass: network, low complexity, no privileges, no user interaction, and high impact on all three. 9.8, critical. The forged token: the same, except availability isn't affected. 9.1, critical. The order leak: it needs an account, so Privileges Required is low, and it only reads, so only confidentiality is hit. 6.5, medium. Here's the trap. PR low sounds reassuring, but anyone can create a NimbuMart account for free in a minute. The score is honest, but don't let the word medium make it sound minor. It exposes customers' addresses, and that's why the findings report calls it high in practice. Now the ranking. The login bypass and the token are both critical and internet-facing: patch this week. The order leak: patch this month. You might argue it deserves this week too, given the personal data. That's a fair argument to make to the client, in writing, with your reason. The tool gives you a starting order, and your judgement finishes it. Answer the question: 9.8.

On screen: the step text, the patch tool with the model answer.

## 7. Write findings a developer can fix

Step seven: write findings a developer can fix. A finding nobody can reproduce doesn't get fixed. It gets argued about, then forgotten. So each finding gets the same five parts: the exact request, what came back, why it works, the fix in code terms, and the retest. The report builder has a findings template with the rules of engagement, an executive summary, the findings, what went well, and the retest.

*After it runs:*

Read the report as the developer who has to act on it. NM-01: the request, the 200 with role admin, the cause, the fix written as an actual query with placeholders, and the retest, 401. NM-02: log in as the demo customer, request order two, see another customer's order and a delivery address, with no address written down. The fix is the query with the caller's user ID, and the retest is 404. NM-03: where the token was found, that the secret is a dictionary word checked offline, the three fixes, and the retest: the old token rejected. Notice there's no line that says improve security. A developer can't build improve security. They can build where id equals this and user id equals that. Then the part testers skip: what went well. Passwords are hashed. The payment page is separate and run by a provider, which is exactly why it was out of scope. Most error pages don't show internals. It isn't flattery. A report that only lists failures makes people defensive, and defensive people argue instead of fixing. The executive summary is three sentences: what an outsider could do, that all three are quick to fix, and that the first should be fixed before the weekend.

On screen: the step text, the report tool with the model answer.

## 8. Retest, then tell the board

Step eight: retest, then tell the board. A fix isn't done until the same test fails. So you repeat each proof exactly as you made it, same request, same account. Then you write for a different reader. The board doesn't need SQL or CVSS. It needs to know what could have happened to the business, what fixing it costs, and what decision you need from it. The report builder has a short escalation template.

*After it runs:*

On retest, the login gets 401, order two gets 404, and the old token is rejected. One detail to notice: the retest is booked for Wednesday the twenty-fifth, and the authorised window ended on Friday the twentieth at 18:00. A retest is testing, so it needs the client's written agreement for the new dates, the same as the first round. Get it before you send a single request. Now the board note. The ask comes first: approve a one-week fix sprint from Monday the twenty-third, and make a retest before every release a standing rule. Severity: high, and why, in one plain sentence: anyone on the internet could log in as the shop's administrator, read other customers' orders, and impersonate users on the test system. What we know: each problem was proved with one request and a demo account, and the fixes are about two days of developer time in total. What we don't know: whether anyone found these first, so the logs from before the sixteenth should be checked for the same requests. The impact if exploited, in business words: changed prices and orders, customers' addresses exposed, which is personal data and may have to be reported, and lost trust. What's been done: the findings went to Engineering on the twentieth, and the login fix is already in testing. A board can decide on two days of work to close three ways in. It can't decide on a CVSS vector.

On screen: the step text, the report tool with the model answer.

## 9. Hand in

Step nine: hand in. The notebook carries everything: the rules of engagement, your recon commands, the three proofs, the scores and ranking, the findings report and the board note. Check the list, then press Hand in.

*After it runs:*

The rubric is on screen. Look at where the points are. Six for three findings that someone else can reproduce, but five for rules of engagement written before any test, five for fixes and retests, five for the board note, and three for professional conduct: test accounts only, and no more data than proves the point. Most of the marks are for the work around the tests. That's deliberate, because that's what makes a tester someone a company trusts with its systems.

On screen: the step text.

## Wrap-up

That's an authorised test that gets things fixed. A letter first, turned into rules of engagement, with the payment host left alone because NimbuMart couldn't authorise it. Recon that named its targets. Three findings, a login that trusted what you typed, an order that wasn't yours, and a token signed with the company's name, each proved with one request and no more data than needed. Scored, ranked with judgement, written so a developer could fix them, retested inside an agreed window, and explained to the board in money, time and risk. Next is seminar ten, Design, risk and audit, where the aim is to stop these problems before anyone has to test for them. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s09-authorised-testing` writes the exact ones)

```
0:00 Opening
1:29 1. Authorisation and scope, before anything else
3:56 2. Recon, inside the lines
5:41 3. Finding 1: a login that trusts what you type
7:30 4. Finding 2: someone else's order
9:18 5. Finding 3: a token anyone can forge
11:21 6. Score and rank
13:12 7. Write findings a developer can fix
15:11 8. Retest, then tell the board
17:24 9. Hand in
18:11 Wrap-up
```

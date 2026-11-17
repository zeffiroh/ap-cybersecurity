# Lecture script: A login bypass with SQL injection

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-a-login-bypass` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-a-login-bypass`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-a-login-bypass` to refresh this file.

## Opening

Hello, and welcome. Today you'll prove a real web vulnerability, SQL injection, on a shop that was built for practice, with written permission, and then see exactly how developers fix it. The most important word in this video is authorised. Testing someone's system without written permission is a crime, so everything here happens on our own practice shop.

## 1. The setting

The setting. NimbuMart Retail, an authorised test from the sixteenth to the twentieth of November 2026. Times are Indian Standard Time. The case folder has the letter of authorisation, engagement.txt. A real tester reads it first, all of it, because it says what you may test, when, and what you must not touch. The shop itself runs in your browser, as Hack the shop, and the Web proxy tool talks to the same shop.

On screen: the step text.

## 2. Finding 1: a login that trusts what you type

Here's the weakness. When you log in, the shop puts the email you type straight into a SQL query, inside quotes. So the query reads: find the user where email equals what you typed, and password equals what you typed. If the email ends the quote early and starts a SQL comment, with a quote and two dashes, the rest of the line, the password check, is ignored. You become whoever you named. The rule for a tester: prove it with one request, and stop. Watch the request in the web proxy.

*After it runs:*

The request is a POST to /api/login, with the email admin@nimbu.shop followed by a quote and two dashes, and any password at all. The response is 200 OK, and the body says we're logged in, with the admin role. That's the proof. We don't browse around as admin or change anything. One request, recorded, and stop. Now write it up the way a developer can use it: the request, the response status, the role you got, and why it works, the query the server built. Then the fix, in one line: use a parameterised query, where the email is sent to the database as data and can never become part of the SQL command. In the SQL injection lab you can see both versions side by side. And the retest: after the fix, the same request should get 401, not authorised. A finding isn't finished until the retest passes. Try the mission Log in as the admin in Hack the shop too. Answer the question: the injected login gets 200.

On screen: the step text, the proxy tool with the model answer.

## 3. Where next

That was one step from Seminar 9, Authorised testing: web, APIs and findings that get fixed. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. Get written permission, and read it. Prove a finding with the smallest possible request, then stop. Explain why it works, give the fix in one clear line, and retest. That's how a tester's work gets bugs fixed instead of filed away. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-a-login-bypass` writes the exact ones)

```
0:00 Opening
0:34 1. The setting
1:03 2. Finding 1: a login that trusts what you type
2:56 3. Where next
3:26 Wrap-up
```

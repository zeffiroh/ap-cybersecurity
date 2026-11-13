# Lecture script: A login bypass with SQL injection

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. In the next fifteen minutes you will prove one SQL injection with a single request, and then see the one-line fix. This is an authorised test of a practice shop, NimbuMart. Only ever do this with written permission.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. Finding 1: a login that trusts what you type

The shop's login builds a SQL query by pasting your email straight into it, inside quotes. If you end the quote yourself and add two dashes, the rest of the query becomes a comment and the password check never runs. Open the web proxy, send one login request as the admin, and stop the moment you have proved it. One request is a proof; ten is a risk to the client. Then repeat it in Hack the shop, and open the SQL injection lab to see the fix: a parameterised query, where the database never treats your input as code.

On screen: the step text and the tool.

## 3. Where next

That is a finding, not a trick: one request, one proof, one fix. In the full Seminar 9 you write the finding up so the developers actually fix it, and you learn the rules of engagement that keep you safe.

On screen: the step text and the tool.

## Wrap-up

That is a finding, not a trick: one request, one proof, one fix. In the full Seminar 9 you write the finding up so the developers actually fix it, and you learn the rules of engagement that keep you safe.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. Finding 1: a login that trusts what you type
2:47 3. Where next
```

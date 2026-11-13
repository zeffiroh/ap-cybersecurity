# Lecture script: Authorised testing: web, APIs and findings that get fixed

Seminar 9 · about 360 minutes of lab work · the video runs about 5 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Authorised testing. The word that matters is authorised: everything you do today is allowed because NimbuMart asked for it in writing, for these addresses, in this window, and nothing else. You'll write the rules of engagement before you touch anything, stay inside scope, prove three findings with as little data as possible, score them, write them so a developer can fix them, retest, and then explain to the board what it means for the business.

## 1. Authorisation and scope, before anything else

A test without written permission is an attack, so we start with the letter. In scope: the shop, its API and two staging hosts. Out of scope: the payment host, even though it's on the same network, because NimbuMart doesn't own it. No social engineering, no denial of service, no touching other customers' data beyond proving a point. And the stop contact's number, written where we'll see it.

On screen: the step text, the Linux cell, the tool with the model answer.

## 2. Recon, inside the lines

Recon, inside the lines. We name the two in-scope addresses rather than sweeping the range, so the payment host is never touched. Shop staging has SSH and the website. API staging has the API, and a debug API on port 8080 that shouldn't face the internet. Its JavaScript bundle contains a hard-coded token. Write every command down.

On screen: the step text, the Linux cell.

## 3. Finding 1: a login that trusts what you type

Finding one. The login pastes the email into SQL inside quotes. Close the quote, comment out the rest, and the password is never checked. One request in the proxy, status 200, role admin, and we stop. We don't browse the admin panel. The fix is a parameterised query, which the SQL injection lab shows, and the retest is the same request getting 401.

On screen: the step text, the tool with the model answer.

## 4. Finding 2: someone else's order

Finding two. Logged in as the demo customer, our orders are three and four. Ask for two, and the shop hands over another customer's order with a delivery address. The API checked we were logged in, not that the order was ours. One record proves it, and the report says it showed an address without writing the address down. The fix: the query includes the caller's user ID.

On screen: the step text, the tool with the model answer.

## 5. Finding 3: a token anyone can forge

Finding three. The bundle's token is a JWT signed with HS256. The inspector decodes the header and payload: the demo customer, role customer. Then an offline check against twelve guessable words, and the secret falls out: nimbu twenty twenty-six. With that, anyone can sign a token that says role admin. The fix is a long random secret from a vault, and no token in a public file.

On screen: the step text, the tool with the model answer.

## 6. Score and rank

Scores. The login bypass is network, low complexity, no privileges, no user: 9.8, critical. The IDOR needs an account, but anyone can make one, so it's 6.5 and still serious. The token is 9.1. Ranked with exposure, the login bypass is first, then the token, then the orders.

On screen: the step text, the tool with the model answer.

## 7. Write findings a developer can fix

A finding nobody can reproduce doesn't get fixed. Each one gets the exact request, what came back, why, the fix in code terms, and the retest. Not improve security, but where id equals this and user id equals that. And a section on what went well, because a report that only lists failures makes people defensive instead of busy.

On screen: the step text, the tool with the model answer.

## 8. Retest, then tell the board

Retest, then the board. Same requests, and now 401, 404, and a rejected token. The board note asks for a one-week fix sprint and a retest before every release, explains the risk as changed orders, exposed addresses and a breach to report, and says honestly what we don't know: whether anyone found these first.

On screen: the step text, the tool with the model answer.

## 9. Hand in

Hand in the notebook: the rules of engagement, the recon commands, the three proofs, the scores, the findings report and the board note. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's a test that gets things fixed. Rules first, recon inside scope, three findings each proved with one request and no more data than needed, scored and ranked, written as steps a developer can follow, retested, and a board note in business words. Next is seminar ten: design, risk and audit, where you stop these problems before anyone has to test for them.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:33 1. Authorisation and scope, before anything else
1:07 2. Recon, inside the lines
1:35 3. Finding 1: a login that trusts what you type
2:07 4. Finding 2: someone else's order
2:40 5. Finding 3: a token anyone can forge
3:13 6. Score and rank
3:38 7. Write findings a developer can fix
4:07 8. Retest, then tell the board
4:35 9. Hand in
4:52 Wrap-up
```

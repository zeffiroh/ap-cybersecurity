# Lecture script: One group membership to domain admin

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-one-group-to-domain-admin` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-one-group-to-domain-admin`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-one-group-to-domain-admin` to refresh this file.

## Opening

Hello, and welcome. In most companies, the attacker's goal is Domain Admins, the group that controls every Windows computer and account. They rarely get there with a single trick. They walk there, one permission at a time. Today you'll follow that walk from a helpdesk account to the top.

## 1. The setting

The setting. Nimbus Analytics in Hyderabad, Tuesday the tenth of November 2026. All times are UTC. A helpdesk worker, h.verma, fell for a phishing email, so the attacker has that account's password. The case folder has the company's identity data: which accounts are in which groups, and what each group is allowed to do.

On screen: the step text.

## 2. Walk it like an attacker

Switch sides and think like the attacker. In the identity tool, open the Attack paths tab, start from h.verma, and ask for paths to Domain-Admins. Each arrow is one thing the attacker can do with what they already have.

*After it runs:*

Let's read the path, hop by hop. h.verma is a member of Helpdesk. Helpdesk has ForceChangePassword on svc-sql, a service account, because of reset rights on the Service Accounts folder, inherited since 2023. That hop needs no new password: the attacker simply sets a new one. svc-sql is a member of Server-Admins. Server-Admins is admin on app02. Now the important one: adm.k.nair has a session on app02. A scheduled task called Nightly KPI export runs as adm.k.nair with a saved password, so that login sits on app02 every night. Anyone who is admin on app02 can take those credentials. And adm.k.nair is a member of Domain-Admins. So: phished helpdesk account, reset a service account's password, admin on a server, take the saved Domain Admin login. Game over. Notice that t.mehta and n.ali, the other Server-Admins members, could walk the same path from Server-Admins onwards. So which single change breaks the most paths? Removing the saved Domain Admin login from app02, by running that task as a low-privilege account, breaks every path that goes through it. Removing the old helpdesk reset right closes the door at the start. Do both. Answer the questions: svc-sql, and app02.

On screen: the step text, the identity tool with the model answer.

## 3. Where next

That was one step from Seminar 7, Identity from both sides: AD, Entra and cloud IAM. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. Attackers think in graphs, not lists. Each hop is something normal on its own: a group membership, an old permission, a saved login. Put them together and they lead to the top. Defenders win by finding the hops that many paths share, and removing them. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-one-group-to-domain-admin` writes the exact ones)

```
0:00 Opening
0:30 1. The setting
0:52 2. Walk it like an attacker
2:33 3. Where next
3:03 Wrap-up
```

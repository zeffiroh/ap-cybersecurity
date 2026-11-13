# Lecture script: One group membership to domain admin

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. In Active Directory, one group membership can be the whole attack. You will follow the path from a phished helpdesk account to Domain Admins.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. Walk it like an attacker

Switch sides and think like the attacker. In the Attack paths tab, start at h dot verma, the phished account, and ask for paths to Domain Admins. Each arrow is one thing the attacker can do with what they already have. HasSessionOn means a saved login: whoever is admin on app02 can take the credentials of the admin who logs in there, and a scheduled task keeps that login there every night. Read the path arrow by arrow. The cheapest place to break it is usually one membership, one session, one task.

On screen: the step text and the tool.

## 3. Where next

You found the path; now you can cut it. Seminar 7 covers both sides of identity: Active Directory, Entra and cloud IAM.

On screen: the step text and the tool.

## Wrap-up

You found the path; now you can cut it. Seminar 7 covers both sides of identity: Active Directory, Entra and cloud IAM.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. Walk it like an attacker
2:47 3. Where next
```

# 5.1.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Carry this framing into the lecture: SQL injection is not really a database problem, it's a language problem, the application asked a user for a piece of data and got back a piece of code instead, and never noticed the swap. Every payload family in this skill, from admin'-- to UNION SELECT, is the same trick wearing different clothes: sneak syntax into a slot the program assumed would only ever hold values. Once you see it that way, the fix stops being a filter you bolt on afterward and becomes obvious from the start, never let user data and query syntax share the same string in the first place.

## The big picture
The throughline worth keeping from this skill is the gap between detecting and preventing. The lesson spends real time on payload signatures because a defender scanning traffic needs to recognize SQLi in the wild, but it is explicit that pattern-matching a WAF against known strings is a second-line control, not the fix, an attacker who varies capitalization, encoding, or comment style slips past a signature list that a parameterized query would have made irrelevant regardless of how the payload was spelled. That distinction, detect versus structurally prevent, is going to recur constantly for the rest of this unit, and it is worth pre-loading now: 5.1.b's escaping, 5.2's authorization checks, and 5.5's parameterized queries are all examples of closing the door at the level where the trust boundary actually lives, rather than posting a guard in front of it.

# 4.2.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The intuition to carry in is that length beats cleverness, and the math is not close: adding four characters to a password multiplies the attacker's search space by roughly 81 million, while swapping an "a" for an "@" barely inconveniences a dictionary attack that already expects that substitution. If you remember only one thing from the old-school password rules you grew up with, remember that NIST spent 2017 walking almost all of them back, mandatory symbols, forced 90-day rotation, not because security stopped mattering, but because those specific rules were quietly making passwords *worse* by pushing everyone toward predictable patterns like Summer2024!.

## The big picture
The throughline worth naming explicitly is that every rule in a password policy is a direct, traceable answer to a named attack: minimum length answers brute-force, banning breached passwords answers dictionary attacks and credential stuffing, salted slow hashing (bcrypt/Argon2, never MD5 or SHA-1) answers what happens *after* a database is stolen, and lockout thresholds answer online guessing specifically, with duration itself becoming a tradeoff between stopping an attacker and accidentally letting an attacker lock out a legitimate user as a denial-of-service move. That's the pattern to keep applying for the rest of Unit 4.2: authentication controls always come in this shape, a defense mapped tightly to one specific attack, which is exactly why 4.2.b exists at all, passwords, however well policed, are still just one factor, and a single leaked secret (however strong) grants full access forever until someone notices and changes it.

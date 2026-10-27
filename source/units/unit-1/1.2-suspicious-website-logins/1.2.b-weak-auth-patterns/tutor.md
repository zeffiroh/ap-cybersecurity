# 1.2.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Here's the intuition that makes the whole math of password cracking click: an attacker is not trying to search the entire universe of possible passwords, they're trying to search the tiny universe of passwords a *human* would actually pick. Humans are bad random-number generators, we gravitate toward names, dates, keyboard patterns, and "clever" substitutions that feel unpredictable to us but are the very first thing every mangling rule tries. The dictionary attack isn't a brute-force fallback; for most real accounts, it's the *primary* attack, because it exploits human psychology, not computational limits.

## The big picture
The passphrase-versus-complexity argument is one of the few places in security where the math is genuinely counterintuitive on first hearing and then completely obvious once you see it: length multiplies the search space, an extra character class only adds one factor to it. A four-word random passphrase you can actually remember beats an eight-character `P@ssw0rd!` you can barely remember and that every mangling engine tries in its first ten thousand guesses. If you remember nothing else from this skill in five years, remember that length beats cleverness.

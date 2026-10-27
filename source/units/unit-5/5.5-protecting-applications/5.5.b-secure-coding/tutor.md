# 5.5.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The reframe worth making before this lecture: input validation (5.5.a) closes one specific door, but secure coding is the discipline of never building the other doors in the first place. Parameterized queries don't depend on catching a malicious string at all, they make it structurally impossible for user data to ever be parsed as SQL syntax, which is a stronger guarantee than any filter, because a filter can miss a variant it wasn't designed to catch and a parameterized query has nothing to miss.

## The big picture
The connective thread worth keeping is that every practice in this skill is least privilege (5.2.a) applied to code instead of people: a database connection scoped to only the tables it needs, a web server process that never runs as root, an error handler that fails closed by default rather than accidentally granting access when something goes wrong. That's the same blast-radius logic from 5.2.b, just moved from human roles to running processes, if an attacker exploits a bug in code running with excessive privilege, the bug becomes a full system compromise instead of a contained one. Also worth remembering: a verbose error message leaking a stack trace or internal file path is not a cosmetic issue, it's free reconnaissance handed straight to an attacker, which connects forward to 5.6.a's point that what an application logs (and what it exposes) shapes how much an attacker can learn before you ever notice them.

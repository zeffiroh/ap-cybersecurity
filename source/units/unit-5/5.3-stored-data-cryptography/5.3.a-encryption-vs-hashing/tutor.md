# 5.3.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The single question worth carrying into this lecture: do you ever need the original value back? If yes, encrypt. If no, hash. That one question does almost all the work in this skill, and it's worth testing against every scenario you meet from here forward, a payroll system needs to read salaries back out, so it encrypts; a login system never legitimately needs to see your actual password again, only whether what you typed matches, so it hashes. Confusing the two isn't a minor mistake, it's storing the *wrong kind of secret* for the job, and the cost of getting it backwards (plaintext-recoverable passwords sitting in a breached database) is exactly the kind of high-severity data breach 5.1.d taught you to score.

## The big picture
The idea worth keeping longest is the avalanche effect and what it actually buys you: a hash function is designed so that two inputs differing by a single character produce digests that look nothing alike, which is what makes a digest useful as a tripwire for even the tiniest tampering. Hold that property in your head, because 5.3.c is going to build its entire argument for HMAC on top of it, and 5.4.c's digital signatures reuse the exact same property one layer up the stack. Also keep the salting story close, it's the clearest illustration in this unit of a general principle that recurs everywhere in cryptography: an attacker doesn't need to break your algorithm if they can out-plan you, and a rainbow table is just precomputation defeating a system that never varied its inputs. The fix is never "a stronger hash function," it's "stop giving the attacker a predictable target to precompute against."

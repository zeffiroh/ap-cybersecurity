# 2.3.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The four controls in this skill, locks, badges, biometrics, mantraps, aren't a menu where you pick the "best" one. They're a stack, and each layer exists specifically to cover a gap the layer before it can't. A lock works with no power and no network, but leaves no record of who used it. A badge leaves a record and can be revoked instantly, but only proves someone had the credential, not that they're the right person. A biometric proves identity, but can't be swapped out if it's compromised the way a badge can. Ask "what does this layer fail to catch" for every control you meet in this course, because that question is what tells you what the *next* layer needs to do.

## The big picture
The seven-layer facility list at the end of this skill is really a compressed version of defense-in-depth, and it's worth noticing that it ends with a person, not a piece of technology. Every electronic and mechanical control on that list handles a predictable case well and an unpredictable case badly, and a guard is the one layer capable of noticing something is wrong even when every rule-based system says everything is fine. False acceptance and false rejection rates are the same idea in miniature: no single control, however well-tuned, gets it right 100% of the time, which is precisely the argument for stacking several imperfect controls rather than searching for one perfect one.

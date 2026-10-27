# 2.4.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The reframe worth making here: an access log isn't a record of what happened, it's a record of what a badge did, and the gap between those two things is where every interesting anomaly lives. A valid badge swipe only proves a credential was presented; it says nothing about who actually presented it. Once you internalize that distinction, the detection rules in this skill stop looking like arbitrary thresholds and start looking obvious: you're not looking for invalid credentials, you're looking for valid credentials behaving in ways a single human physically couldn't.

## The big picture
Every rule in this skill is really the same move applied three times: define what normal looks like, then flag whatever falls outside it. After-hours access is abnormal *timing*. A denial burst is abnormal *frequency*. A location inconsistency is abnormal *geography*, the same badge in two places faster than a person could travel between them. That's the core logic of every detection system you'll meet for the rest of this course, physical or digital: you can't spot an anomaly without first being precise about what normal actually is, which is why "establish a baseline" always comes before "write the alert rule," never after.

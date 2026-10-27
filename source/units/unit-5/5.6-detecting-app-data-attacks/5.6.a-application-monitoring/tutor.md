# 5.6.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The line worth holding onto walking in: you cannot detect an attack you never recorded, which means logging isn't a forensic afterthought, it's the precondition for every detection technique the rest of this skill and the next two are about to cover. A single failed login is meaningless noise, people mistype passwords constantly. Fifty failed logins across twenty usernames from one IP in two minutes is an unmistakable pattern. The shift from "reading individual events" to "reading the shape of many events together" is the entire skill this skill is building.

## The big picture
The concept worth keeping past this lecture is that this skill's detection logic is the exact same move as 5.2.c's lateral-movement detection and 5.6.b's DLP behavior analysis, just aimed at a different signal: define what normal looks like, then flag whatever falls outside it, whether that's login frequency, host-hopping, or data-transfer volume. Once you notice that pattern repeating, detection engineering across this entire unit stops looking like a pile of unrelated tools and starts looking like one recurring template applied to authentication events, network hops, and outbound transfers respectively. Also worth remembering: logs are themselves an attack target, an attacker who achieves code execution will often try to erase their tracks, which is why the atom insists on append-only, remotely streamed logs. That single design choice is what makes chain-of-custody in 5.6.c even possible; evidence that could have been quietly edited by the attacker who generated it isn't evidence at all.

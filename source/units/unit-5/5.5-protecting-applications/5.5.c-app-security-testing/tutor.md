# 5.5.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The distinction worth carrying into this lecture: SAST reads code without running it, DAST attacks a running system without reading its code, and they are blind to exactly each other's territory, which is why the AP framework wants you to be able to sort a given finding into one bucket or the other, not just recognize that "testing happened." SAST can see every code path, including ones nobody has exercised yet, but it can't tell whether a flagged pattern actually reaches attacker-controlled input, so it over-flags. DAST only knows what it actually attacked, but when it finds something, that something is almost always real.

## The big picture
The idea worth remembering longest is that neither SAST nor DAST, nor both together, is a substitute for a skilled human thinking like an attacker. Automated tools are exhaustive over known patterns and completely blind to business-logic flaws, the kind of thing a penetration tester spots by asking "can a regular user manipulate this parameter to view someone else's invoice", which, notice, is exactly the BOLA scenario from 5.1.c, a vulnerability class that neither a static scanner reading source code nor a dynamic scanner fuzzing inputs would reliably flag, because nothing about the request itself looks malformed. That's the clean argument for why mature programs run continuous automated scanning for volume and reserve human pentesting for depth, and it sets up 5.6 perfectly: everything from here forward in this unit shifts from *preventing* vulnerabilities before release to *detecting* attacks against whatever slipped through anyway.

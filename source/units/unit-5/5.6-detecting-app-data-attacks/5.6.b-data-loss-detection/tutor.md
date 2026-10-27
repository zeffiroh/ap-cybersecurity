# 5.6.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The pairing worth carrying into this lecture: DLP fights the exact same battle as 5.6.a's log analysis, but content-based detection and volume/behavior-based detection split the work the way SAST and DAST split application testing in 5.5.c, one looks at *what* is moving, the other at *how much and how oddly* it's moving, and each catches what the other misses. An attacker who encrypts stolen data before exfiltrating it defeats content inspection completely, but a 3 AM upload of two gigabytes to a domain nobody's ever used before still lights up a behavior-based system, because that system never needed to understand the content at all.

## The big picture
The idea worth keeping longest is that DLP is one of the few controls in this entire unit that can act preventively in real time rather than only forensically after the fact, it can block the email or quarantine the upload mid-attempt, not just record that it happened. That puts DLP in an interesting position relative to 5.1.d's severity scoring: time-to-detect was one of the three factors driving how bad a breach turns out to be, and a DLP system that catches exfiltration in progress is directly attacking that variable, potentially turning what would have been a severe, fully-completed breach into a contained, mostly-prevented one. Also keep the approved-destination-list detail close, it's the same allowlist-over-denylist philosophy from 5.5.a, just applied to network destinations instead of form-field values: defining what's known-good is more stable and less noisy than trying to flag every possible bad destination.

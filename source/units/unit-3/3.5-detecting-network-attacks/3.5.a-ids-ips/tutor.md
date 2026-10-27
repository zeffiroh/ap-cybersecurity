# 3.5.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The question worth carrying into lecture: what happens to traffic a firewall already decided to let through? That's the gap this skill lives in, a firewall answers whether a port is allowed, but plenty of real attacks travel over ports that have to stay open (HTTP, DNS, HTTPS), which means allowed and safe are two different questions, and IDS/IPS exists specifically to keep asking the second one after the firewall has already answered the first.

## The big picture
Keep signature-based and anomaly-based detection sorted by what each one trades away: signatures are precise and fast but structurally blind to anything new, since a zero-day by definition has no entry in the database yet; anomaly detection can catch a never-before-seen attack precisely because it doesn't need a signature at all, but it pays for that with a much higher false-positive rate, since unusual and malicious are not the same thing. The TP/FP/FN/TN grid is worth being fluent in cold, because the exam's favorite trap is treating false positives as merely annoying, they're actually dangerous precisely because enough of them causes analysts to start tuning out real alerts, and an ignored true positive is functionally identical to a system that never detected anything at all. That alert-fatigue idea is the direct throughline into 3.5.b: a signature engine only catches what it already recognizes, but broader traffic monitoring, watching volume, timing, and destination rather than matching known patterns, is what catches everything a signature-based IDS was never going to see coming.

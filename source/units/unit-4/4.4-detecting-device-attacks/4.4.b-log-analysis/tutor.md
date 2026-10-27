# 4.4.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The habit worth building before this lecture: never judge a single log line. One failed login is background noise, everyone mistypes a password sometimes, and the entire skill this skill teaches is refusing to draw a conclusion until you've looked at *several* entries linked by the same user, the same IP, or a tight time window. A log analyst's job isn't reading logs, it's reading patterns that only exist once you stop looking at any one line in isolation.

## The big picture
The Meridian scenario is worth remembering in exact structure, because it contains a trap the exam loves: six failed logins followed immediately by a success, from the same IP, in under a minute. Read the final line alone and it looks like someone finally got their password right, completely unremarkable. Read the whole sequence as a correlated unit and it's a textbook brute-force success. That gap between what one line suggests and what the sequence proves is the entire argument for correlation, and it's the same argument you'll meet again in 4.4.c when individual IOCs get combined into a compromise score, a single artifact is ambiguous, several artifacts pointing the same direction are not. The threshold-tuning discussion (5 failures in 60 seconds, not 2, not 50) deserves equal weight: it's the same false-positive-versus-false-negative tradeoff you saw in 4.3.b's behavioral detection, and "alert fatigue" is worth naming explicitly as a security failure in its own right, a detection rule tuned so sensitively that analysts start ignoring it is functionally the same as having no detection rule at all, just with extra noise and false confidence layered on top.

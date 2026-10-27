# 5.1.d tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The habit worth building before this lecture: stop asking "did a breach happen" and start asking "how bad is this specific breach," because the AP framework wants you to reason quantitatively, not just spot the incident. Sensitivity, scale, and time-to-detect are three independent dials, and a breach can be severe by maxing out just one of them, forty leaked health records can outrank four million leaked newsletter emails even though the second number is a thousand times bigger. That's the same risk-equals-likelihood-times-impact logic from way back in Unit 2, just now applied to data instead of physical assets.

## The big picture
The connective tissue worth noticing is that this skill is the unifying finish line for everything in 5.1: SQL injection, XSS, and BOLA are three different *causes*, and a data breach is the *consequence* they all funnel toward, alongside plenty of non-technical causes like a lost laptop or a misconfigured bucket. That's worth sitting with, because it means the attack technique and the resulting harm are separate axes you have to reason about independently, the same breach severity can follow from a highly technical SQLi dump or a simple human mistake, and the response arc (contain, assess, notify, remediate) doesn't change based on how sophisticated the entry point was. Keep the time-to-detect factor especially close, because it's the bridge into 5.6: everything this unit builds toward, logging, DLP, evidence analysis, exists specifically to shrink that number before it becomes the deciding factor in how bad a breach turns out to be.

# 1.5.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Detection rules are where the abstract idea of "pattern recognition" from earlier atoms becomes a concrete, deployable artifact: a condition, a threshold, and an action, expressed in a format a machine can act on without a human re-reading every log line. The brute-force rule, five failures per minute, is worth remembering not for the specific number but for what the number represents: someone, at some point, tuned that threshold against real data to balance catching real attacks against drowning analysts in false alarms. Every threshold you'll ever configure in security tooling is fighting that same precision-recall tradeoff.

## The big picture
"AI proposes, humans approve" is a phrase worth holding onto as a template for how AI assistance should be integrated almost everywhere in security operations, not just here. The moment an organization lets AI-*generated* rules deploy without human review, it has traded one risk (missing real threats) for a different, sneakier one (rules that are technically accurate but legally, operationally, or contextually wrong, blocking a business partner's IP, for instance). Speed and judgment are not substitutes for each other; the best pipelines get both by keeping a human explicitly in the loop at the approval gate, not eliminating the loop.

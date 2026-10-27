# 2.2.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The intuition worth keeping: nature doesn't care about your threat model. A ransomware gang wants something from you; a burst pipe doesn't want anything, it just happens, and the server room goes offline exactly the same way either way. That's the whole reason this skill exists in a cybersecurity course at all: if your risk analysis only counts threats with intent behind them, you've quietly excluded some of the most common causes of real outages, and "but nobody attacked us" is cold comfort to a hospital that just lost patient records to a flooded basement.

## The big picture
The detail that should stick with you is the fire-suppression paradox: the default tool for putting out a fire (water) is also one of the most effective tools for permanently destroying the exact hardware you're trying to save. That's a perfect example of a control designed for one context becoming a threat in another, which is a pattern you'll see again and again in security. The fix (clean-agent suppression) isn't a fancier version of a sprinkler, it's a completely different mechanism chosen because the ordinary solution actively backfires here. When you evaluate any control in this course, always ask: does this control assume a context that doesn't apply here?

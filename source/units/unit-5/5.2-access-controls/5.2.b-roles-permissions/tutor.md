# 5.2.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The asymmetry worth internalizing before this lecture: under-granting access is loud (someone complains immediately) and over-granting is silent (nothing breaks, nobody notices), and that single asymmetry is the entire engine behind privilege creep. It's not that organizations decide to be reckless with permissions; it's that the feedback loop is broken in exactly one direction, so access accumulates by default unless someone deliberately fights against it. Once you see privilege creep as a natural consequence of which errors get noticed rather than a failure of vigilance, the fix, scheduled role recertification, stops looking like bureaucratic overhead and starts looking like the only thing capable of counteracting a bias that's baked into how humans notice problems.

## The big picture
The phrase worth keeping is blast radius, because it reframes why least privilege matters in a way that connects straight back to 5.2.a and forward to 5.2.c. A role isn't just a convenience for onboarding new hires, it's a pre-committed answer to "how much damage does one phished account cause," decided in advance, before any attack happens. A tightly scoped support-agent role turns a phishing success into a contained incident; a role padded with "just in case" permissions turns the exact same phishing email into a much larger breach. That's not a hypothetical, it's literally the mechanism 5.2.c is about to walk through in detail: lateral movement is what happens when blast radius wasn't actually contained, and every silent excess permission this skill warns about is a potential hop in that chain.

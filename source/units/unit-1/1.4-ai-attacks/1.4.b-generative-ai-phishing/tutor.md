# 1.4.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The core economic insight here is worth sitting with because it explains an entire generation of security tooling becoming obsolete overnight: spam filters were never detecting *maliciousness* directly, they were detecting the *fingerprints of mass production*, awkward phrasing, generic greetings, inconsistent grammar. An LLM doesn't just write better phishing emails, it removes the fingerprint the filter was actually keying on. When the cost of a personalized, fluent, contextually accurate message drops to zero, "this reads a little off" stops being a signal you can rely on at all.

## The big picture
Prompt injection deserves a mental model distinct from ordinary phishing: you're no longer defending a human from persuasion, you're defending a *system* that cannot tell the difference between an instruction from its owner and an instruction hiding inside data it was asked to process. That's a genuinely new category of vulnerability, not a repackaged old one, and it's why the strongest defenses here (privilege separation, human-in-the-loop) don't try to make the model smarter about spotting injections. They accept the model will sometimes be fooled and limit the blast radius of that failure instead, the same posture you'll see recur under the name "assume breach" later in this course.

# 1.5.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The professor's frame for the whole AI-in-defense half of this unit: every tool from here on out follows the same pattern, AI does the exhaustive, mechanical, tireless part (does this directive match a known-bad pattern, across every line, with zero fatigue) and a human does the contextual judgment part (is this exception documented, is this a legitimate compensating control). Keep asking, for every AI-assisted tool you meet from here forward, "what exactly is the machine automating, and what judgment is still reserved for the human?", that question is the fastest way to actually understand what a tool does rather than just what it's called.

## The big picture
The rule-engine-versus-graph-model distinction quietly previews something you'll rediscover throughout this course: simpler, transparent detection logic (a fixed rule list) is often the *right* choice for a learning environment even when more sophisticated ML-based approaches exist, precisely because you can audit exactly why a finding fired. A security tool you can't explain the reasoning of is a tool you can't fully trust, no matter how accurate it tests.

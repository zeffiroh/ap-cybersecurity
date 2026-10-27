# 2.1.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Here's the mental model worth carrying through the rest of the course: whenever you read about a security incident, don't ask "how bad was it," ask "which pillar did it break." Confidentiality, integrity, and availability aren't three items on a checklist, they're three completely different failure modes that call for three completely different fixes. A confidentiality fix (encrypt it) does nothing for an integrity problem (verify it hasn't changed), and neither does anything for an availability problem (make sure it's still reachable). Once you sort an incident into the right bucket, the right defense almost picks itself.

## The big picture
The tension buried at the end of this skill is the one worth remembering longest: the three pillars don't just coexist, they actively fight each other. Lock a system down hard enough to guarantee confidentiality and you've probably made it slower or harder to reach, an availability cost. That's not a flaw in the framework; that's the framework doing its job, forcing you to make the tradeoff on purpose instead of by accident. Every unit from here forward, physical controls, network defenses, incident response, is really just this same triage question asked in a new context: which pillar am I protecting, and what am I willing to spend on the other two to do it?

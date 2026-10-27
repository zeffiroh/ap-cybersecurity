# 1.4.d tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Data poisoning asks you to think about security in a place most people never consider a threat surface at all: the raw material a model learns from, before the model even exists. The intuition that makes this click is realizing a model has no concept of "training" versus "deployment" separate from the numbers it was shown, if the numbers say hostile language correlates with the label "positive," the model doesn't know that's wrong, it just knows that's what the data said. Garbage in isn't just garbage out; carefully crafted garbage in is a *chosen* out.

## The big picture
The distinction between availability attacks (break it for everyone) and integrity/backdoor attacks (break it only in one specific, attacker-chosen way, while looking perfectly healthy everywhere else) is the part worth remembering longest, because backdoor attacks are unsettling precisely for how *invisible* they stay under normal evaluation. A model can pass every accuracy benchmark you throw at it and still contain a landmine that only detonates on a trigger the evaluator never thought to test. That's a sobering preview of why AI systems need the same kind of adversarial, not just functional, testing you'll apply to code throughout this course.

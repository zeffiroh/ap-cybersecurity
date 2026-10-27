# 1.4.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The single sentence to hold onto from this whole atom: "confidential" is a policy the model is asked to follow, not a technical wall it cannot cross. Every token in the conversation, the system prompt, the user's message, the model's own prior output, sits in the same context window with no structural fence between "instructions" and "content." Asking a model to keep a secret is closer to asking a very obedient employee to keep a secret than to putting that secret in a locked safe. Obedient employees can still be talked into things.

## The big picture
It's worth noticing the shape of the arms race this skill sets up: regex output filters catch what you anticipated, and a motivated adversary evades exactly that by encoding, splitting, or paraphrasing the secret. This is the same static-analysis-versus-creative-adversary tension you'll meet again in 1.5.b (code scanning) and 5.1.a (SQL injection detection), pattern matching is cheap, fast, and a genuinely useful first layer, but it is never, on its own, a complete defense against an adversary who knows the patterns you're matching against.

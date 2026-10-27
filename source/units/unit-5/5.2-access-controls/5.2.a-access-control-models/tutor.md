# 5.2.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The frame to carry in: none of DAC, MAC, or RBAC is "the secure one", they're three different answers to "who gets to decide access," and the right answer depends entirely on whether you trust individual owners, need centrally enforced rules that nobody can override, or need something that scales past a handful of people. Resist the urge to rank them by strength; the AP exam is testing whether you can match a scenario to a model, not whether you can recite that MAC is "the most secure." A consumer photo-sharing app that used MAC would be unusable, and a intelligence agency that used DAC would be reckless, same three tools, opposite right answers.

## The big picture
The concept worth keeping longest is least privilege as the thread that runs underneath all three models rather than being a fourth option. DAC, MAC, and RBAC are just different *mechanisms* for granting access; least privilege is the *design principle* that tells you how narrowly to grant it regardless of which mechanism you're using. That distinction is exactly what the exam-trap misconception in this skill is pointing at, an RBAC system with one bloated "superuser" role is still RBAC, it just violates least privilege badly, which means the model you chose and the discipline you applied inside it are two separate things you have to evaluate separately. Hold onto that pairing, because 5.2.b spends its entire atom on exactly this gap: how a perfectly reasonable role structure quietly drifts into a least-privilege violation over time.

# 1.5.d tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
MTTR is the metric that makes an abstract idea, "attackers race against defenders", measurable and manageable. The intuition worth internalizing: every second an incident sits unactioned isn't neutral time, it's time an attacker is actively spending on lateral movement or exfiltration. Decomposing MTTR into detect/triage/contain/eradicate isn't just accounting, it tells you exactly *where* to invest, because AI helps each sub-metric through a different mechanism (continuous monitoring shrinks detection time; severity scoring shrinks triage time; automated playbooks shrink containment time).

## The big picture
The tiered-response model, automate the high-confidence, reversible cases; escalate the ambiguous, high-stakes ones, is this unit's cleanest example of a principle that will reappear constantly for the rest of this course: automation is not about replacing judgment, it's about being ruthlessly selective about *which* decisions actually require it. A SOC that tries to automate everything creates a new failure mode (auto-resolving a real incident prematurely); a SOC that automates nothing drowns its analysts in routine work. The skill this course is actually building in you, across every AI-defense atom in this unit, is the judgment to draw that line correctly.

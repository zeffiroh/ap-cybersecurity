# In-class activity, 2.3.c Security guards and layered defense-in-depth

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as physical security consultants reviewing layer proposals for a fictional facility,
Novara Data Center, and decide whether each proposed layer set is STRONG, ADEQUATE, or WEAK, and
what single addition would most improve a weak configuration. Ties to LO 2.3.B (security guards
and layered defense-in-depth) and the course skill Mitigate Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed layer sheet below.
- One copy of the layer sheet per group (print or display on screen).

## Layer sheet (print or project)

| # | Facility | Layers present | Categories | Rating | What's missing |
|---|----------|-----------------|------------|--------|-----------------|
| 1 | Novara-Annex | lobby guard, roving night patrol | ? | ? | ? |
| 2 | Novara-Branch | perimeter fence, badge reader, CCTV | ? | ? | ? |
| 3 | Novara-Warehouse | unlocked side door only | ? | ? | ? |
| 4 | Novara-Lab | 3 separate CCTV feeds | ? | ? | ? |
| 5 | Novara-Core | fence, guard post, badge reader, mantrap, CCTV | ? | ? | ? |

## Steps
1. (5 min) Each group reads rows 1-2 and individually lists the distinct control categories
   present for each (perimeter, personnel, electronic, barrier, monitoring).
2. (5 min) Group discusses: row 1 has two layers but why does that not raise the depth score above
   1? Reach consensus on the "categories," "rating," and "what's missing" columns for rows 1-2.
3. (5 min) Repeat for rows 3-4, paying special attention to why three CCTV feeds (row 4) still
   count as only one category, and why row 3 has a depth score of zero rather than one.
4. (5 min) For row 5, the group must decide whether this facility is STRONG or ADEQUATE, and
   justify the answer by counting distinct categories, not layers.
5. (5 min) Each group opens the simulation and checks their ratings against the sim's scoring for the
   analogous facilities; groups revise any incorrect calls and note which category was missing in
   each WEAK or ADEQUATE case.

## Collaborate (AP skill 4)
Assign roles: one member is the "facility manager" (proposes which single new layer would most
cheaply raise the depth score), one is the "budget owner" (must justify that the proposed layer's
cost is worth the new category it closes, not a redundant one), and remaining members are
"auditors" (challenge whether a proposed addition actually introduces a new category or just
duplicates an existing one, e.g., a second guard vs. a badge reader). For row 1 (Novara-Annex), the
group must specifically debate whether adding a third guard or adding a badge reader is the better
use of budget, and explain why in terms of depth score.

## Exit ticket
Each student writes one sentence: "Facility X is rated [STRONG/ADEQUATE/WEAK] because it has
[N] distinct control categories, and adding a [category] layer such as [example] would most
improve its posture."

## Instructor notes
- Timing: rows 2 and 5 are the clean multi-category cases; rows 1 and 4 are the intended teaching
  moment for "redundant layers in one category do not raise depth score."
- Common stumble: students count total layers instead of distinct categories, especially on row 4
  (three CCTV feeds looks like "a lot of security" but is depth score 1). Push them to name the
  five categories explicitly and cross off which ones are covered.
- Row 3 (single unlocked door, no controls at all) exists to test whether groups correctly assign a
  depth score of zero rather than assuming "at least it's a facility, so it must have some score."
- Feeds the unit project (threat modeling a small network/facility) and the coding problem in
  `problem/`, which implements this exact depth-score and recommendation logic as `solve(layers)`.

# In-class activity, 1.3.a Adversary skill levels

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Students analyze adversary profiles, assign skill tiers, and justify their reasoning using the
feature-based classification rules from the lesson. Ties to LO 1.3.A (assess adversary capability
and motivation to analyze risk).

## Materials (all local)
- the SimLab simulation on each machine, or the printed profile cards below.

## Profile cards (print or display)

| Profile | Uses zero-day | Custom tooling | Targets specific victim | Off-the-shelf only | Adapts to defenses |
|---------|--------------|---------------|------------------------|-------------------|-------------------|
| Alex    | No           | No            | No                     | Yes               | No                |
| Blake   | Yes          | Yes           | Yes                    | No                | Yes               |
| Casey   | No           | No            | Yes                    | No                | Yes               |
| Dana    | No           | Yes           | No                     | No                | No                |
| Emery   | No           | No            | Yes                    | Yes               | No                |

## Steps
1. Each pair opens the simulation and sorts the on-screen adversary profiles into LOW and HIGH tiers,
   recording their reasoning for each.
2. After completing the sim, pairs apply the same rules to the five profile cards above and
   record a tier and one-sentence justification for each.
3. Pairs compare answers with the pair next to them. For any disagreement, they cite the specific
   rule from `interface.md` that resolves the dispute.

## Collaborate (AP skill 4)
Assign roles: one partner is the "threat analyst" (applies the rules mechanically), the other is
the "risk manager" (challenges edge cases and asks "what if one feature changed?"). Swap roles for
the second half of the profile cards.

## Exit ticket
Each student submits: the tier they assigned to Casey (profile 3) and the rule number from
interface.md that determined it, plus one sentence explaining why motivation (the goal of the
attack) matters when assigning risk level.

## Instructor notes
- Expected answers: Alex = low, Blake = high, Casey = high (rule 2), Dana = high (rule 1),
  Emery = low (targeted but not adaptive).
- Common stumble: students classify Emery as high because they "target a victim." Emphasize that
  rule 2 requires BOTH targeting AND adaptation.
- Feeds the unit project (public-Wi-Fi threat model) and scenario stage 1 (attacker profiling
  before the evil-twin and jamming stages).

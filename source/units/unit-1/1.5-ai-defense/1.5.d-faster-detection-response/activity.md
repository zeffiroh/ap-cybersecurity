# In-class activity, 1.5.d Faster, more accurate threat detection and response

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students experience the difference between arrival-order and severity-order triage by manually
processing an incident queue both ways, then compute MTTR for each approach and compare.
Ties to LO 1.5.B (explain how AI reduces MTTR and improves response accuracy).

## Materials (all local)
- the SimLab simulation on each machine, or the printed incident queue below.
- `problem/`, students verify their MTTR calculation against `solve()`.

## Printed incident queue (if devices unavailable)
```
ID       Arrival  Detected_at  Resolved_at  Severity  Auto
INC-001  T=0      0            600          low       No
INC-002  T=5      5            65           critical  No
INC-003  T=10     10           40           high      Yes
INC-004  T=15     15           315          medium    No
INC-005  T=20     20           50           critical  No
```

## Steps
1. **Arrival-order pass (7 min).** Process incidents INC-001 through INC-005 in the order
   listed (T=0 first). Record the order you would hand each to an analyst and estimate when
   each is resolved (use the resolved_at values). Compute MTTR manually:
   MTTR = (600 + 60 + 30 + 300 + 30) / 5 = 204 seconds.

2. **Severity-order pass (7 min).** Re-sort the queue: critical first, then high, medium, low.
   Assume the same resolved_at values (resolution time does not change; only analyst attention
   changes). Identify which incidents are auto-resolved (they require no analyst time).
   Compute what the effective analyst queue looks like after removing auto cases.

3. **Discussion (6 min).** Answer: Does MTTR change between the two orderings? Why or why not?
   (MTTR is a mean of fixed response times, so ordering does not change it -- but the time
   until the CRITICAL incidents are first *touched* changes dramatically.) What metric captures
   that difference? (Time-to-touch for critical incidents, sometimes called "time to triage".)

4. **Sim verification (5 min).** Open the simulation. Triage the queue in severity order and
   observe how the sim tracks which critical incidents were handled first.

## Collaborate (AP skill 4)
Assign roles: one partner is the **AI triage engine** (assigns severity scores and sorts the
queue), the other is the **SOC analyst** (decides which incidents to auto-close and which to
escalate). After the first pass, swap roles and discuss whether you would auto-resolve INC-003
given only the information shown.

## Exit ticket
Each student submits:
- The MTTR value for the printed queue (should be 204.0 seconds).
- One sentence explaining why sorting by severity matters even though it does not change MTTR.

## Instructor notes
- Expected MTTR: (600 + 60 + 30 + 300 + 30) / 5 = 204.0 seconds.
- Auto-resolved: INC-003 (auto=Yes) -> auto_resolved = 1.
- Key insight: MTTR is a mean of fixed times; severity ordering does not change MTTR but does
  change *when* the most critical incidents are first seen by an analyst. This is the
  distinction between MTTR (mean) and time-to-touch (per severity tier).
- Common stumble: students assume sorting changes the response times -- it does not. Correction:
  the resolution clock starts at detected_at, not at when the analyst picks it up.
- Feeds the unit project (incident dashboard) and scenario stage 4 (response coordination).

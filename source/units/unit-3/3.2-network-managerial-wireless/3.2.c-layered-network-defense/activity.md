# In-class activity, 3.2.c Layered network defense overview

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as security architects building a defense-in-depth diagram for a small business
network, placing every control studied in Unit 3 into its correct layer and identifying which
layer has the fewest controls (a potential weak point). Ties to LO 3.2.B, 3.2.C and the course
skill Mitigate Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed control list below.

## Control list (print or project)

| # | Control | Layer? |
|---|---------|--------|
| 1 | DNS filtering blocking known-malicious domains at the gateway. | ? |
| 2 | Internal firewall between the guest VLAN and the corporate VLAN. | ? |
| 3 | OS patch management keeping every laptop's operating system current. | ? |
| 4 | Web Application Firewall (WAF) in front of the customer portal. | ? |
| 5 | Data Loss Prevention (DLP) tooling blocking sensitive files from leaving via email. | ? |
| 6 | The company's Acceptable Use Policy, signed by every employee. | ? |

## Steps
1. (5 min) Each group reads rows 1-2 individually and assigns a layer using the six-layer model
   from the lesson (perimeter, network, host, application, data, human).
2. (5 min) Group discusses row 3: why is OS patching a host-layer control rather than a
   perimeter-layer control, even though vulnerable software could be exploited remotely?
3. (7 min) Group works rows 4-5 together: both protect something inside the network, but at
   different layers (application vs. data). Discuss the distinction: WAF protects the application
   logic itself; DLP protects the data regardless of which application touches it.
4. (5 min) Each group opens the simulation and checks their calls against the sim's scoring for
   analogous scenarios; groups revise any incorrect calls.
5. (3 min) Report-out: each group tallies how many controls landed in each layer for their table
   and identifies which layer has the fewest, is that a real gap, or just outside today's list?

## Collaborate (AP skill 4)
Assign roles: one member is the "architect" (assigns each control to a layer and defends the
reasoning), one is the "auditor" (challenges each assignment against the lesson's definitions), and
remaining members are "gap analysts" (identify which layer is thinnest and propose one additional
control for it). For row 6 (AUP), the group must specifically explain why a policy document, not a
piece of hardware or software, still counts as a defense layer.

## Exit ticket
Each student writes one sentence: "Control X belongs in the [PERIMETER / NETWORK / HOST /
APPLICATION / DATA / HUMAN] layer because [reasoning tied to what it protects and how]."

## Answer key (instructor only)

| # | Layer | Reasoning |
|---|-------|-----------|
| 1 | Perimeter | Filters traffic at the network boundary before it reaches internal systems. |
| 2 | Network | Segments traffic between internal zones. |
| 3 | Host | Protects the individual device's operating system. |
| 4 | Application | Protects the application's own logic/inputs. |
| 5 | Data | Protects the data itself regardless of application or device. |
| 6 | Human | A policy document governing behavior, spanning all technical layers. |

## Instructor notes
- Timing: rows 1-2 are straightforward layer placements; row 3 is the deliberate "why not
  perimeter" teaching moment; rows 4-5 test the application-vs-data distinction, which students
  often conflate.
- Common stumble: students place every technical-sounding control at the "network" layer by
  default, reinforce that each layer has a specific scope (boundary, internal segmentation,
  individual device, application code, data itself).
- This activity is designed as a capstone review for the whole 3.1-3.2 sequence: every control
  from 3.1.b-3.2.b should be placeable somewhere in this model, and instructors should draw that
  connection explicitly during report-out.

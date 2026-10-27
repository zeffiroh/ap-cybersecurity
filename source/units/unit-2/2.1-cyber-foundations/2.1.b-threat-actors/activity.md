# In-class activity, 2.1.b Threat actors and their motivations

**Format:** small group · **Time:** 25 min · **Offline:** yes

## Goal
Students analyze incident reports to determine the most likely threat actor profile, their motivation, and select the highest-leverage defensive controls. Ties to LO 2.1.B and the Analyze Risk skill.

## Materials (all local)
- Printed or displayed Incident Profiles below.
- Paper or shared text editor to draft recommendations.

## Incident Profiles

| Profile | Technical observations | Impact |
|---|---|---|
| A | Port scan followed by exploitation of a 3-year-old FTP vulnerability. Attacker tried to install a public coin-miner script. | Server CPU went to 100%. |
| B | An employee who was passed over for a promotion downloaded the client list to a USB drive right before their exit interview. | Data leaked on a forum. |
| C | Custom stealth rootkit installed on active directories; data copied out slowly over a secure channel to a foreign server IP. | High-value IP exfiltrated. |
| D | Web portal flooded with HTTP requests accompanied by a public social media post criticizing the company's environmental record. | Website offline. |

## Steps
1. (5 min) **Brainstorming:** In groups of 3-4, students read each profile (A-D) and match it to one of: *Script Kiddie*, *Insider Threat*, *Nation-State/APT*, or *Hacktivist*.
2. (10 min) **Defensive Alignment:** For each profile, students choose the best mitigation from the following list and explain why:
   - Least privilege access control + logging
   - Web application firewall (WAF) + rate limiting
   - Prompt patching program + disabling unused services
   - Network segmentation + EDR anomaly detection
3. (5 min) **Peer Review:** Two groups swap answers and review each other's actor classifications and controls justification.
4. (5 min) **Class debrief:** Review why matching defense to actor motivation saves resources.

## Collaborate (AP skill 4)
Assign roles in each group:
- **Threat Intelligence Lead:** Argues who the threat actor is based on technical indicators.
- **Defensive Architect:** Proposes which control provides the best mitigation.
- **Finance Director:** Questions whether the cost of the proposed control is justified based on the threat actor's motivation and resources.

## Exit ticket
Each student submits a written card: "To defend against a [Threat Actor Category], the most cost-effective control is [Control] because their motivation is [Motivation], making that control highly disruptive to their objective."

## Instructor notes
- Expected answers:
  - Profile A: Script Kiddie (motivated by curiosity/opportunistic notoriety; stopped by prompt patching).
  - Profile B: Insider Threat (motivated by revenge/personal gain; stopped by least privilege + USB logging).
  - Profile C: Nation-State/APT (motivated by espionage; stopped by network segmentation + anomaly detection).
  - Profile D: Hacktivist (motivated by ideological statement/embarrassment; stopped by WAF + rate limiting).
- Common stumbles: Students often want to deploy advanced anomaly detection for everything. Remind them that script kiddies represent the highest volume of attacks, and basic hardening/patching stops them at a fraction of the cost of an enterprise EDR solution.

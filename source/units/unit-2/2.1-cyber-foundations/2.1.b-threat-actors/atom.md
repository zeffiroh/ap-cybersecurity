# 2.1.b, Threat actors and their motivations

> **Unit 2 · 2.1 Cyber Foundations**
> **AP Learning Objective(s):** 2.1.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Identify the six major threat actor categories, explain what motivates each one, and use motivation to recommend the most appropriate defensive measure for a given attack scenario.

## Lesson

### Why motivation matters

When Meridian University's security team arrived on Monday morning, they found three incident tickets waiting. Someone had encrypted the registrar's database and left a ransom note. An anonymous post on a public forum included thousands of student records. And the athletics department website had been replaced with a political banner reading "Equity Now." Three attacks. Three very different attackers. Three completely different responses required.

Defenders who treat every attack the same waste resources. A technical patch that stops a script kiddie does nothing against a patient nation-state actor. Understanding who is behind an attack and why is the first step toward building defenses that actually work. That is the core claim of AP Learning Objective 2.1.B.

### The six threat actor categories

**Nation-state actors** are groups sponsored or directed by a government. Their goals are geopolitical: steal military or industrial secrets (espionage), disrupt an adversary's infrastructure (sabotage), or gather intelligence on foreign officials. Nation-state actors have large budgets, skilled operators, and patience measured in years. They typically target governments, defense contractors, utilities, and research institutions. Because they operate under political cover, they are rarely prosecuted and almost never stop unless a diplomatic or strategic situation changes.

**Cybercriminals** are motivated entirely by money. Ransomware is their most visible tool: software that encrypts a victim's files and demands payment for the decryption key. They also commit payment fraud, sell stolen credentials, and run extortion schemes. The ransom note left in Meridian's registrar database fits this profile exactly. Cybercriminals operate in organized groups, often renting ransomware-as-a-service from specialized developers. Hospitals, universities, and municipalities are frequent targets precisely because downtime is catastrophic for them and they are more likely to pay.

**Hacktivists** combine hacking with activism. They act for ideological or political reasons: they want to embarrass an organization, amplify a cause, or punish a perceived injustice. The "Equity Now" banner on Meridian's athletics site is a classic hacktivist move. Website defacement costs the target almost nothing technically but generates press coverage and public embarrassment. Hacktivists also leak documents to expose wrongdoing or conduct denial-of-service attacks against organizations they oppose. Because publicity is the goal, their attacks are often loud and attributed, the opposite of the stealth a nation-state actor cultivates.

**Insider threats** come from within the organization. Three sub-types matter:

- *Malicious insiders* intentionally steal or destroy data, often for financial gain, personal revenge, or ideological reasons.
- *Disgruntled employees* may act impulsively after a negative performance review or termination notice.
- *Negligent insiders* cause harm accidentally by emailing a sensitive file to the wrong address, reusing a weak password, or plugging in an unvetted USB drive.

The student records that appeared on the public forum most likely came from an insider. The data set was too complete and too clean to have been assembled by an outside attacker who would first need to defeat perimeter controls. Insider threats are uniquely difficult because the actor already has legitimate credentials and physical access. Technical controls alone cannot stop them; least-privilege access policies, user activity monitoring, and a healthy off-boarding checklist all play a role.

**Script kiddies** are low-skill attackers who use publicly available tools without understanding how they work. Their motivation is usually curiosity, notoriety among peers, or the desire to say they hacked something. They rarely target specific organizations; they scan the internet for known vulnerabilities and attack whatever responds. They are the most common type of attacker by volume and the easiest to stop: keeping systems patched and disabling unnecessary services eliminates most of their options.

**Advanced Persistent Threats (APTs)** describe a style of attack rather than a single actor type. An APT is a long-running, stealthy, high-capability campaign. The attacker gains an initial foothold, then moves quietly through the network for months or years, gradually exfiltrating data while working hard to avoid detection. APTs are almost always nation-state-sponsored or nation-state-adjacent. The "Advanced" label refers to custom tools and zero-day exploits. The "Persistent" label refers to the willingness to maintain access indefinitely. If Meridian later discovered a quiet log anomaly showing that someone had been silently reading faculty email for eight months without triggering any alerts, that would suggest an APT campaign, not the same group behind the ransomware.

### Motivation shapes defense

Each actor profile implies a different defensive priority:

| Actor | Primary motivation | Highest-leverage defense |
|---|---|---|
| Nation-state / APT | Espionage, sabotage | Network segmentation, threat intelligence feeds, anomaly detection |
| Cybercriminal | Financial gain | Offline backups, email filtering, multi-factor authentication |
| Hacktivist | Ideology, public embarrassment | Web application firewall, CMS credential hygiene, incident PR plan |
| Insider | Varied (revenge, negligence, greed) | Least privilege, access logging, rigorous off-boarding |
| Script kiddie | Curiosity, notoriety | Regular patching, port closure, basic hardening |

Back at Meridian: the security team isolated the registrar database, negotiated with law enforcement rather than paying the ransom, audited access logs to find the source of the leaked records, and restored the athletics site from a clean backup before resetting all CMS credentials. Each response was targeted at the most likely actor behind that specific incident, which is only possible when defenders understand motivation.

## Key terms
- **Threat actor**, any individual, group, or organization that intentionally or accidentally causes harm to information systems or data.
- **Nation-state actor**, a threat actor operating on behalf of or with the support of a national government.
- **APT (Advanced Persistent Threat)**, a long-duration, stealthy, high-capability intrusion campaign, typically state-sponsored.
- **Cybercriminal**, a threat actor motivated by financial gain, using attacks such as ransomware, fraud, or credential theft.
- **Hacktivist**, an attacker motivated by political or ideological goals who uses hacking as a form of protest or public pressure.
- **Insider threat**, a threat originating from someone who already has authorized access to an organization's systems.
- **Script kiddie**, a low-skill attacker who uses pre-built tools without deep technical understanding.
- **Motivation**, the underlying reason a threat actor chooses to attack; drives target selection, tactics, and persistence level.

## Common misconceptions
- "All hackers are criminals out for money", Hacktivists and nation-state actors have entirely different goals; conflating them leads to misaligned defenses.
- "APT always means nation-state", APT describes a campaign style (advanced and persistent) that is usually but not always government-backed; well-funded criminal groups can run APT-style campaigns too.
- "Insider threats are rare", Accidental insider incidents (negligent users) are among the most common causes of data exposure; they receive less press than ransomware but are just as damaging.
- "Patching stops sophisticated attackers", Patching is essential against script kiddies, but nation-state actors regularly exploit zero-days and misconfigurations that have no patch yet.

## Try it
- **Simulation:** Read a fictional attack headline, identify the correct threat actor type from the options, and score 6 out of 6 before the round ends.
- **Coding problem:** Implement `solve(description)` to classify a threat actor from a plain-text description using keyword matching and a priority ordering rule.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-150 (Guide to Cyber Threat Intelligence), rebuilt equivalent at `vendor/nist/sp800-150-summary.md`
- Reference: Wikiversity "Cybersecurity/Threat Intelligence", local mirror at `vendor/wikiversity/threat-intelligence.md`
- Practice: SANS Cyber Aces Module 1 (threat landscape overview), local rebuild at `vendor/sans-cyber-aces/module-01-threat-landscape.md`
- Repo: Free-Cybersecurity-Resources (LetsDefend), `vendor/repos/Free-Cybersecurity-Resources/`

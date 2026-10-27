---
deck:
  title: Threat Actors & Security Risks
  kicker: Class 3
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 3
  description: Who attacks, why they do it, and the lifecycle MITRE ATT&CK uses to map their behavior.
  topics: [Hackers, Cybercriminals, Insiders, Nation-State Actors, Motivations, Attack Lifecycle]
---

---
title: Threat Actors & Security Risks
cover: true
---
:::text class=sub
Understanding the adversaries behind cyber threats is foundational to designing resilient security architectures and effective defense strategies.
:::
::::columns
::col::
:::list heading="Key Frameworks" style=chips
- MITRE ATT&CK
- NIST SP 800-207 (Zero Trust)
- ISO/IEC 27001
:::
::col::
:::list heading="Core Concepts" style=chips
- Threat Actor Motivations
- Attack Lifecycle Models
- Adversary Behaviors
:::
::::
:::callout style=soft
Threat actors are not merely "hackers." They are individuals or groups with specific motivations, capabilities, and objectives. Recognizing these distinctions is essential for threat modeling and risk assessment.
:::

:::image src="images/03_threat_actor_landscape.png" alt="Threat actor landscape map showing categories from script kiddies to nation-states arranged by sophistication and resources" caption="The Threat Actor Landscape: actors classified by motivation, capability, and resource level, from opportunistic script kiddies to state-sponsored APT groups" width=full
:::

:::notes
In cybersecurity, a **threat actor** refers to an individual, group, or organization that has the intent and capability to exploit vulnerabilities to compromise systems, steal data, or disrupt services. These actors vary widely in their motivations, ranging from financial gain (e.g., cybercriminals) to political agendas (e.g., nation-state actors), ideological beliefs (hacktivists), or even personal challenges (script kiddies).

To systematically understand and respond to these threats, security professionals rely on structured frameworks such as **MITRE ATT&CK**, which catalogs adversarial tactics, techniques, and procedures (TTPs) across the attack lifecycle. This enables defenders to identify behaviors, predict next steps, and develop mitigations. Complementing this, **NIST Special Publication 800-207** introduces Zero Trust architecture principles to reduce the impact of compromised actors within a network.

Additionally, **ISO/IEC 27001** provides a risk-based approach to managing information security, emphasizing the identification of threats and the implementation of controls tailored to organizational contexts. Understanding threat actors also involves analyzing historical incidents, such as those documented in **CVE** reports, to assess real-world exploitation patterns.

The study of threat actors is not merely academic, it directly shapes defensive strategy. A healthcare organization that understands it is likely targeted by financially motivated cybercriminals seeking Protected Health Information (PHI) will prioritize encryption of patient records and access control reviews differently than a defense contractor who knows nation-state APT groups are their primary adversary. This threat-informed defense posture is a core tenet of the NIST Cybersecurity Framework (CSF) 2.0 Govern function, which mandates that organizations understand their threat landscape before selecting and implementing controls.

By categorizing threat actors, such as Advanced Persistent Threats (APTs), insider threats, or organized crime syndicates, organizations can better align defensive strategies with the most probable and impactful risks they face. The MITRE ATT&CK framework further enriches this analysis by mapping known adversary groups to the specific techniques they employ, enabling defenders to assess their detection and response coverage against real-world attack patterns.
:::

%%%

---
unit: Threat Actors
code: ACT
title: A Cast of Characters
---
:::callout style=soft
We met threat actors briefly in Class 1. Today we go deeper into who they are, what drives them, and how security teams actually map their behavior.
:::

::::columns
::col::
:::list heading="The major categories" style=plain
- Hackers, independent individuals, ranging from curious to criminal
- Cybercriminals, organized groups motivated by profit
:::
::col::
:::list heading="" style=plain
- Insiders, people who already have legitimate access
- Nation-state actors, government-sponsored, long-term operations
:::
::::

:::table
| Threat Actor | Resources | Typical Motivation | Detection Difficulty |
|---|---|---|---|
| Script Kiddies | Very Low | Curiosity, fame | Low, use known tools |
| Hacktivists | Low–Medium | Ideology, protest | Medium, noisy DDoS/defacement |
| Cybercriminals | Medium–High | Financial profit | High, professional opsec |
| Insider Threats | Internal access | Revenge, coercion, greed | Very High, trusted credentials |
| Nation-State APTs | Extremely High | Espionage, sabotage | Extremely High, custom tooling |
:::

:::image src="images/03_threat_actor_categories.png" alt="Five threat actor categories shown as concentric rings from least to most sophisticated: script kiddies, hacktivists, cybercriminals, insiders, nation-states" caption="Threat Actor Categories by Sophistication and Resource Level, each ring represents increasing capability, persistence, and impact potential" width=half
:::

:::notes
In cybersecurity, a **threat actor** is any person or entity that has the capability, intent, and opportunity to exploit vulnerabilities and cause harm to digital assets, systems, or data. Understanding the nature and motivations of these actors is foundational to threat modeling, risk assessment, and defensive strategy development, as outlined in standards such as NIST SP 800-30 and ISO/IEC 27005.

Threat actors are typically categorized based on their **motivations**, **resources**, and **operational sophistication**. These categories help security professionals anticipate attack vectors, assess risk levels, and apply appropriate countermeasures.

The first category, **Hackers**, encompasses a broad range of individuals who exploit systems for various reasons. These range from **script kiddies**, inexperienced users employing pre-written tools, to **white hat hackers** conducting authorized penetration tests, and **black hat hackers** engaging in malicious activity. While some hackers are driven by curiosity or ideological motives, others operate for personal gain or disruption.

**Cybercriminals** are typically well-organized, profit-driven groups that engage in activities such as ransomware deployment, data theft, and financial fraud. These actors often leverage advanced persistent threats (APTs), exploit kits, and social engineering. Their operations are frequently supported by underground markets where malware, stolen credentials, and zero-day exploits are traded. The FBI's Internet Crime Complaint Center (IC3) reported cybercrime losses exceeding $10.3 billion in 2022 alone, underscoring the financial scale of this threat category.

**Insiders** are individuals with authorized access to an organization's systems, such as employees, contractors, or business partners, who misuse that access intentionally or unintentionally. Insider threats are particularly dangerous due to their legitimate access and knowledge of internal processes. The CERT Insider Threat Center at Carnegie Mellon University estimates that insider incidents account for approximately 30% of all data breaches. Mitigating insider threats requires behavioral monitoring, least-privilege access controls, and regular access reviews as specified in NIST SP 800-53 controls AC-2 (Account Management) and AC-6 (Least Privilege).

Finally, **Nation-state actors**, also known as Advanced Persistent Threats (APTs), are backed by governments and pursue strategic objectives such as espionage, sabotage, or influence operations. These actors are characterized by high levels of funding, long-term persistence, and advanced techniques. Examples include APT28 (Fancy Bear) and APT29 (Cozy Bear), both linked to Russian state-sponsored campaigns, as well as APT41 (Winnti Group), associated with Chinese state interests and conducting both espionage and financial crime simultaneously.

Security teams use structured frameworks like **MITRE ATT&CK** to systematically analyze and track the Tactics, Techniques, and Procedures (TTPs) of these actors. This enables defenders to build behavioral-based detection models and simulate adversarial paths for proactive defense. The ATT&CK Navigator tool allows teams to visualize which techniques a specific threat group uses and overlay their current detection coverage to identify gaps.
:::

%%%

---
unit: Hackers
code: HAK
title: Hackers, Not All the Same
---

::::columns
::col::
:::table
| Type      | Authorization | Intent                 | Example Activities                     |
|-----------|---------------|------------------------|----------------------------------------|
| White Hat | Authorized    | Beneficial             | Penetration testing, bug bounties      |
| Grey Hat  | Unauthorized  | Non-malicious          | Vulnerability disclosure without consent |
| Black Hat | Unauthorized  | Malicious or harmful   | Data theft, ransomware, system compromise |
:::
::col::
:::callout
"Hacker" describes a skill set, not automatically a crime. The ethical and legal status of any hacking activity depends entirely on **authorization** and **intent**, not technical capability alone.
:::
::::

:::image src="images/03_hacker_spectrum.png" alt="Spectrum diagram from white hat to black hat showing authorization level, intent, and legal status" caption="The Hacker Spectrum: Authorization and Intent determine whether a skilled individual is a security asset or a threat actor" width=full
:::

:::steps
A company hires a white hat pentester under a signed Statement of Work (authorization)
The pentester probes the network for vulnerabilities (same skills as a black hat)
Vulnerabilities are reported via responsible disclosure to the security team (ethical intent)
The security team patches the issues before any malicious actor exploits them
The organization's risk posture improves without any real harm occurring
:::

:::notes
In cybersecurity discourse, the term "hacker" is often misused as a blanket label for malicious actors. However, academically and professionally, a hacker is better understood as an individual with advanced knowledge of systems, networks, and software, someone capable of understanding, manipulating, and sometimes subverting technology in ways that are not immediately obvious to others. The ethical and legal implications of hacking are determined not by skill level, but by two key factors: **authorization** and **intent**.

**White hat hackers**, also known as ethical hackers or security researchers, operate within the bounds of the law and organizational policy. They are typically employed or contracted to perform security assessments such as penetration testing or vulnerability research. Their work aligns with standards such as **NIST SP 800-115** (Technical Guide to Information Security Testing and Assessment) and supports frameworks like ISO/IEC 27001 for managing information security risks. These professionals often participate in **bug bounty programs**, where they are rewarded for responsibly disclosing vulnerabilities (e.g., via platforms like HackerOne or Bugcrowd). Certifications such as Certified Ethical Hacker (CEH), OSCP (Offensive Security Certified Professional), and GPEN (GIAC Penetration Tester) credential professionals in this space.

**Grey hat hackers** occupy a legal and ethical grey area. They may identify and disclose vulnerabilities without prior authorization, sometimes publicly, without malicious intent. While their actions can lead to improved security outcomes, they violate terms of service or laws such as the **Computer Fraud and Abuse Act (CFAA)** in the United States and similar statutes internationally. A prominent example is the discovery and public disclosure of router firmware vulnerabilities by researchers who accessed devices without explicit permission. Their work is not sanctioned, but it is generally non-exploitative, their motivation is usually recognition within the security community or a genuine desire to improve security.

**Black hat hackers** are threat actors who engage in unauthorized and malicious activities. These individuals or groups may exploit systems for financial gain, espionage, or disruption. Examples include deploying ransomware (e.g., WannaCry, tracked as **CVE-2017-0144**), conducting Advanced Persistent Threat (APT) campaigns, or participating in cybercrime syndicates. Their behavior often violates multiple international laws and is catalogued in frameworks like **MITRE ATT&CK**, which documents specific techniques (e.g., T1486, Data Encrypted for Impact, T1566, Phishing) used by black hat actors in real-world campaigns.

Understanding these distinctions is critical for cybersecurity practitioners, as it informs legal compliance, responsible disclosure policy, scope of engagement agreements, and incident response strategies. Organizations should establish clear vulnerability disclosure policies (VDP) that create formal channels for grey and white hat hackers to report issues without legal risk, transforming a potential threat into a security asset.
:::

%%%

---
unit: Cybercriminals
code: CRM
title: Cybercriminals, Profit-Driven Threats
---
:::callout style=soft
Cybercriminals operate with a high degree of organization and specialization, often resembling legitimate enterprises. They maintain structured hierarchies, employ technical and non-technical personnel, and utilize monetization channels such as ransomware-as-a-service (RaaS), data brokerage, and dark web marketplaces.
:::

::::columns
::col::
:::list heading="Primary Targets" style=plain
- Banking credentials and payment card data
- Corporate networks for ransomware deployment
- Personally identifiable information (PII) for resale
- Business email compromise (BEC) schemes
:::

::col::
:::list heading="Monetization Methods" style=plain
- Ransom payments via encrypted file recovery
- Sale of stolen data on dark web forums
- Credential stuffing and account takeover
- Extortion and DDoS-for-hire services
:::
::::

:::image src="images/03_ransomware_as_a_service_model.png" alt="RaaS ecosystem diagram showing developer, affiliate, victim, and money laundering relationships with cryptocurrency flows" caption="Ransomware-as-a-Service (RaaS) Ecosystem: a criminal supply chain where developers lease malware to affiliates who split ransom proceeds, often laundered through cryptocurrency mixers" width=full
:::

:::flow
Criminal developer creates ransomware or exploit kit
Lists malware on dark web marketplace (RaaS affiliate model)
Affiliates purchase or lease the malware
Affiliates conduct phishing or exploit public-facing systems for initial access
Ransomware deployed, victim files encrypted and/or exfiltrated
Ransom demanded in cryptocurrency (Bitcoin/Monero)
Proceeds laundered through crypto mixers or money mule networks
Developer and affiliate split revenue (typical 70/30 split)
:::

:::notes
Cybercriminals represent one of the most prevalent and sophisticated categories of threat actors in the contemporary threat landscape. Unlike state-sponsored adversaries or hacktivists, their primary motivation is **financial gain**, which drives the adoption of scalable, repeatable attack models that resemble legitimate business operations. These actors often form structured organizations with defined roles such as developers (who create malware or exploit kits), operators (who manage campaigns), negotiators (who handle ransom discussions), and money launderers (who process illicit gains through cryptocurrencies or bulletproof hosting services).

The **Ransomware-as-a-Service (RaaS)** model has democratized cybercrime. Groups like LockBit, Cl0p, and ALPHV/BlackCat operate affiliate programs where less technical criminals purchase or lease ransomware toolkits and share a percentage of ransom proceeds with the developers. This business model has enabled a dramatic increase in the volume and geographic spread of ransomware attacks. The 2021 Colonial Pipeline attack (attributed to the DarkSide RaaS group) disrupted fuel supply across the U.S. East Coast and resulted in a $4.4 million ransom payment, illustrating the real-world impact of financially motivated cybercrime on critical infrastructure.

**Business Email Compromise (BEC)** is another financially devastating attack vector. The FBI's IC3 reported BEC losses of over $2.7 billion in 2022. In a BEC attack, adversaries compromise or spoof executive email accounts to convince employees to wire funds or share sensitive information. This technique exploits trust rather than technical vulnerabilities, making it difficult to detect with traditional security controls.

Cybercriminals also exploit weaknesses in authentication and access control mechanisms. Techniques such as credential stuffing, using databases of leaked username/password combinations from previous breaches (e.g., credentials exposed in CVE-2019-9193, the PostgreSQL arbitrary code execution vulnerability), enable attackers to compromise accounts at scale. Tools like Sentry MBA and SNIPR automate these attacks against banking portals, streaming services, and e-commerce platforms.

Organizations must combat cybercriminal activity through a layered defense strategy incorporating multi-factor authentication (NIST SP 800-63B), network monitoring aligned with NIST CSF Detect function, and incident response plans per NIST SP 800-61. Threat intelligence sharing through ISACs (Information Sharing and Analysis Centers) also plays a critical role in distributing indicators of compromise (IoCs) across industry sectors.
:::

%%%

---
unit: Insiders
code: INS
title: Insiders, The Threat Already Inside
---
::::columns
::col::
:::table
| Type | Description |
|---|---|
| Malicious insider | Deliberately misuses access, theft, sabotage, revenge |
| Negligent insider | Causes harm by accident, mistakes, carelessness, poor habits |
| Compromised insider | A legitimate account taken over by an outside attacker |
:::
::col::
:::callout
**Why Insiders Are Uniquely Dangerous**

Unlike external threats, insiders bypass traditional perimeter defenses. They operate from within trusted environments, often with privileged access, making detection and mitigation more complex. NIST SP 800-53 dedicates entire control families (AC, AU, IA) to managing insider risk.
:::
::::

:::image src="images/03_insider_threat_indicators.png" alt="Behavioral indicator chart showing patterns like unusual login times, excessive data downloads, and policy violations that indicate insider threat activity" caption="Insider Threat Behavioral Indicators: patterns flagged by User and Entity Behavior Analytics (UEBA) tools, deviations from baseline behavior are key detection signals" width=full
:::

:::flow
Employee receives job offer from competitor or becomes disgruntled
Employee begins accessing files outside their normal scope (anomaly)
User and Entity Behavior Analytics (UEBA) flags unusual access patterns
Security team investigates and correlates with HR records
Insider exfiltrates data via USB, cloud storage, or email before resignation
Incident response activated, containment, evidence preservation, legal action
Post-incident: access reviews and privilege minimization implemented
:::

:::notes
Insider threats represent one of the most challenging and high-impact risks in cybersecurity due to their inherent access and trust. Unlike external adversaries who must first penetrate network perimeters, insiders, whether employees, contractors, or business partners, already possess legitimate credentials and authorized access to systems and data. This foundational trust significantly lowers the barrier to exploitation and increases the potential for damage. According to the **2023 Verizon Data Breach Investigations Report (DBIR)**, insider actors were responsible for approximately 19% of all data breaches analyzed, with financial motivation being the most common driver.

The **malicious insider** is an individual who intentionally exploits their access for personal gain, ideological reasons, or revenge. Common motivations include financial incentives (e.g., selling intellectual property to a competitor), competitive advantage, or retaliation against an organization following a disciplinary action or termination notice. These actors often exhibit anomalous behavior patterns, such as accessing unusual data sets, downloading large volumes of files, or transferring data to personal cloud storage during off-hours. The **2013 Edward Snowden** case exemplifies a high-profile malicious insider incident, where classified NSA programs were disclosed using authorized system access and authorized credentials, demonstrating that technical controls alone cannot prevent all insider incidents.

The **negligent insider** causes harm unintentionally through poor security hygiene. This includes falling for phishing attacks, misconfiguring cloud storage permissions (making sensitive S3 buckets publicly accessible, a common source of data exposure), or reusing weak passwords. NIST emphasizes the importance of continuous security awareness training and technical guardrails such as Data Loss Prevention (DLP) systems to reduce negligent insider risk. NIST SP 800-50 provides a framework for building and maintaining IT security awareness and training programs.

A **compromised insider** occurs when an external attacker gains control of a legitimate user's credentials, effectively masquerading as that trusted user. This often occurs through phishing, credential stuffing (exploiting reused passwords), or malware such as keyloggers. Because the attacker uses valid authentication tokens and behaves within expected system boundaries initially, their actions may not trigger traditional anomaly detection systems. Detection requires behavioral baselines and continuous monitoring, capabilities aligned with **NIST SP 800-137** (Continuous Monitoring) and the **User and Entity Behavior Analytics (UEBA)** controls recommended in NIST SP 800-53 SI-4 (System Monitoring).

Organizations must implement a layered defense strategy that includes **privileged access management (PAM)**, separation of duties, regular access reviews (addressed in NIST SP 800-53 AC-2 and ISO/IEC 27001 A.9.2), and continuous monitoring via UEBA platforms. The MITRE ATT&CK framework highlights specific techniques used by insider threats, including *Account Manipulation* (T1098), *Data Staged* (T1074), and *Exfiltration Over Web Service* (T1567), enabling defenders to build targeted detection rules.
:::

%%%

---
unit: Nation-State
code: APT
title: Nation-State Actors & APTs
---
:::callout style=soft
Nation-state actors are government-sponsored entities that conduct cyber operations as part of national strategy. Often categorized as **Advanced Persistent Threats (APTs)**, these groups are characterized by their extensive resources, high level of skill, and long-term operational persistence within targeted networks.
:::

::::columns
::col::
:::list heading="Key Characteristics" style=plain
- State-sponsored with significant financial backing
- Highly trained personnel with advanced technical capabilities
- Operate with strategic intent: espionage, sabotage, influence
- Maintain long-term presence (months to years) within targets
:::
::col::
:::list heading="Common Targets" style=plain
- Government agencies and defense contractors
- Critical infrastructure (power grids, water systems, etc.)
- Telecommunications and financial institutions
- Research and development organizations
:::
::::

:::table
| Attribute              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Funding**            | Government-backed; virtually unlimited budget for tools, training, and time |
| **Skill Level**        | Elite-level expertise in exploit development, social engineering, and evasion |
| **Objective**          | Strategic advantage, not immediate financial gain                           |
| **Persistence**        | Long-term access; dwell time often exceeds 200 days (per Verizon DBIR)     |
| **Tactics**            | Often aligned with MITRE ATT&CK framework for persistent access            |
:::

:::table
| APT Group | Attributed Nation | Notable Operation | Techniques Used |
|---|---|---|---|
| APT28 (Fancy Bear) | Russia (GRU) | 2016 DNC Breach | T1566 Spearphishing, T1078 Valid Accounts |
| APT29 (Cozy Bear) | Russia (SVR) | SolarWinds (2020) | T1195 Supply Chain Compromise |
| APT41 (Winnti) | China (MSS) | Global IP Theft | T1190 Exploit Public App, T1005 Data Collection |
| Lazarus Group | North Korea | Bangladesh Bank Heist | T1486 Data Encrypted for Impact |
| APT33 (Elfin) | Iran (IRGC) | Saudi Aramco Targeting | T1499 Endpoint Denial of Service |
:::

:::image src="images/03_apt_attack_timeline.png" alt="Timeline showing APT attack progression from months-long reconnaissance through dwell time to eventual discovery, with key phases labeled" caption="APT Attack Timeline: Nation-state actors often maintain undetected network access for 200+ days, dwell time represents their greatest advantage over defenders" width=full
:::

:::notes
Nation-state actors represent one of the most formidable categories of threat actors in the cybersecurity landscape. Unlike financially motivated cybercriminals, these groups operate under the direction or sponsorship of national governments and pursue objectives aligned with **geopolitical or strategic interests**. They are commonly referred to as **Advanced Persistent Threats (APTs)**, a term that emphasizes their methodical approach, advanced toolsets, and long-term persistence within compromised environments. The "persistent" aspect is key: where a cybercriminal may spend hours to days in a network, an APT group might maintain undetected access for months or years.

These actors are distinguished by their access to substantial resources, both financial and human. They often employ former military or intelligence personnel, operate dedicated research teams to develop zero-day exploits (vulnerabilities unknown to the vendor and thus unpatched), and invest in custom malware frameworks designed to evade commercial antivirus and EDR products. The **MITRE ATT&CK for Enterprise** framework catalogs hundreds of techniques specifically observed in APT campaigns, organized under tactics such as Persistence, Defense Evasion, and Command and Control.

The **SolarWinds supply chain attack** (2020), attributed to APT29 (Cozy Bear), exemplifies the sophistication of nation-state operations. Attackers compromised the build pipeline of SolarWinds' Orion IT management software, embedding a backdoor (dubbed SUNBURST, tracked as **CVE-2020-10148**) into legitimate software updates distributed to approximately 18,000 customers, including U.S. federal agencies and Fortune 500 companies. The attackers maintained access for over nine months before detection, demonstrating the extraordinary patience and stealth of state-sponsored adversaries.

Other significant APT operations include **Operation Aurora** (2009-2010), where APT10 (Stone Panda) compromised Google and dozens of other corporations to steal intellectual property, and the **NotPetya** destructive wiper attack (2017), attributed to the Russian military unit Sandworm, which caused an estimated $10 billion in global damages while targeting Ukrainian critical infrastructure.

Organizations defending against APTs must implement **layered defenses** aligned with NIST SP 800-53, including privileged access workstations (PAWs), network traffic analysis for command-and-control beacon detection, supply chain risk management per NIST SP 800-161, and threat hunting programs that proactively search for indicators of compromise (IoCs) rather than waiting for automated alerts. The **NIST Cybersecurity Framework Detect** function is particularly critical for shortening adversary dwell time, as early detection dramatically limits the impact of even the most sophisticated intrusions.
:::

%%%

---
unit: Motivations
code: MOT
title: Why Do They Do It? — Motivation Analysis
---

::::columns
::col::
:::table
| Motivation              | Typical Actor           | Example Incident |
|------------------------|-------------------------|-----------------|
| Financial gain         | Cybercriminals          | Colonial Pipeline ransomware ($4.4M) |
| Political/ideological   | Hacktivists             | Anonymous vs. HBGary Federal (2011) |
| Espionage/sabotage     | Nation-state actors     | SolarWinds / SUNBURST (2020) |
| Revenge/personal grudge| Insiders                | ACCC insider data theft cases |
| Curiosity/reputation    | Hackers, script kiddies | Lulzsec PBS breach (2011) |
:::

::col::
:::callout
Understanding threat actor **motivation** is foundational to threat modeling and risk assessment. It allows defenders to anticipate not only *what* might be targeted, but *why*, enabling more effective prioritization of defensive resources and selection of controls.
:::
::::

:::image src="images/03_motivation_threat_mapping.png" alt="Matrix mapping five motivations (financial, ideological, espionage, revenge, curiosity) against threat actor types and likely target sectors" caption="Motivation-to-Target Mapping: understanding why an actor attacks reveals what they are likely to target, critical for sector-specific risk prioritization" width=half
:::

:::notes
In cybersecurity, understanding the **motivations** behind threat actors is essential for effective threat modeling, risk assessment, and defensive planning. Motivation often dictates not only the tactics, techniques, and procedures (TTPs) used by an attacker, but also the nature of the targets they pursue and the outcomes they seek. This concept is emphasized in frameworks such as **MITRE ATT&CK**, which categorizes adversary behaviors based on observed motivations and objectives, and in **NIST SP 800-30**, which highlights the importance of identifying threat sources and characterizing their intent as part of risk analysis.

There are five primary motivational categories:

**Financial gain** drives most cybercriminal activity, including ransomware campaigns, credit card theft, and data exfiltration for resale on the dark web. These actors typically prioritize targets with high-value data, healthcare records (worth $250+ per record on dark web markets, compared to $5-10 for credit cards), financial accounts, and intellectual property. The financial motivation means these attacks follow economic logic: high-value targets with weak defenses are most attractive.

**Political or ideological causes** are the hallmark of **hacktivists**, who seek to disrupt services, deface websites, or leak sensitive data to advance a political or social agenda. Groups like Anonymous have historically targeted government and corporate entities whose actions they oppose, from opposing SOPA legislation to protesting actions by various governments. Their attacks tend to be noisy (DDoS, defacement) and publicly claimed, as their goal is to send a message, not remain hidden.

**Espionage and sabotage** are typically associated with **nation-state actors** or **APT groups**. These actors aim to gather intelligence on foreign government policies, steal defense technology, compromise critical infrastructure, or disrupt adversary operations. Their campaigns are long-term, patient, and carefully targeted. Unlike cybercriminals, they may avoid monetizing their access immediately, instead maintaining persistent access for future use.

**Revenge or personal grievance** often originates from **insider threats**, where individuals with access misuse their privileges to harm their organization following a perceived injustice such as demotion, termination, or disciplinary action. The Carnegie Mellon CERT Insider Threat Center's research database shows that the average time between the triggering event and the malicious act is approximately 32 days, giving organizations a window to detect behavioral changes.

**Curiosity or reputation-seeking** is common among **hackers** and **script kiddies**, who may explore systems for personal learning or to gain recognition within hacking communities. While often non-malicious in intent, their actions can still result in unintended damage or exposure. Understanding this motivation informs appropriate responses, often education and community engagement rather than purely punitive measures.

By analyzing motivation, security professionals can better align defensive strategies with likely threats. This approach aligns with **ISO/IEC 27005**, which emphasizes risk treatment based on threat likelihood and impact, and likelihood is heavily influenced by whether an organization is a realistic target for actors with a given motivation.
:::

%%%

---
unit: ATT&CK
code: TTP
title: Introducing MITRE ATT&CK
---
:::callout style=soft
**MITRE ATT&CK** is a globally adopted, open knowledge base that catalogs real-world adversary behaviors observed across the cyber threat landscape. The acronym ATT&CK stands for **Adversarial Tactics, Techniques, and Common Knowledge**, representing a structured framework for understanding and defending against cyber threats.
:::

:::list heading="Core Purposes for Defenders" style=plain
- Provides a **standardized vocabulary** for threat analysis and incident response
- Documents **real-world attack behaviors**, not hypothetical threat models
- Enables **consistent evaluation** of defensive capabilities and detection gaps
- Facilitates **cross-team and cross-organization communication**
:::

:::table
| Component     | Description                                                                 | Example |
|---------------|-----------------------------------------------------------------------------|---------|
| **Tactics**   | High-level adversarial goals (the "why")  | TA0001 Initial Access |
| **Techniques**| Specific methods used to achieve a tactic (the "how") | T1566 Phishing |
| **Sub-techniques** | Granular variations of techniques | T1566.001 Spearphishing Attachment |
| **Procedures** | Real-world documented instances of technique use | APT28 using spearphishing in DNC breach |
| **Mitigations** | Recommended defenses for each technique | M1049 Antivirus/Antimalware |
| **Detections** | Data sources and methods to identify technique use | Process monitoring, email gateway logs |
:::

:::image src="images/03_mitre_attack_matrix_overview.png" alt="MITRE ATT&CK Enterprise Matrix showing 14 tactic columns with example techniques listed beneath each, color-coded by detection coverage" caption="MITRE ATT&CK Enterprise Matrix: 14 tactical columns spanning Initial Access through Impact, with hundreds of techniques, defenders use this to visualize and close detection gaps" width=full
:::

:::notes
The MITRE ATT&CK framework represents a paradigm shift in cybersecurity from theoretical risk modeling to **behavior-based threat understanding**. Unlike traditional models that focus on vulnerabilities or asset inventories, ATT&CK centers on the **actions of adversaries** during an intrusion, what they do step-by-step after gaining access. This behavioral approach aligns with NIST SP 800-53's emphasis on continuous monitoring and adaptive defense strategies, moving from a "protect everything equally" model to a threat-informed prioritization of defenses.

ATT&CK was developed by MITRE Corporation and initially released in 2013, based on observations of adversary behavior against Microsoft Windows enterprise environments. Since then, it has expanded to cover Linux, macOS, mobile platforms (Android and iOS), cloud environments (AWS, Azure, GCP), containers, and Industrial Control Systems (ICS/OT). This breadth makes it applicable across virtually every modern computing environment.

The framework is structured into three core components:
- **Tactics** represent the strategic goals of the adversary at each phase of the attack, the "why." The 14 Enterprise tactics span from TA0001 (Initial Access) through TA0043 (Reconnaissance) at the beginning to TA0040 (Impact) at the end.
- **Techniques** are the specific methods used to achieve a tactic, the "how." For example, under the Credential Access tactic, T1110 (Brute Force) and T1003 (OS Credential Dumping) are distinct techniques.
- **Sub-techniques** provide further granularity. T1566 (Phishing) breaks down into T1566.001 (Spearphishing Attachment), T1566.002 (Spearphishing Link), and T1566.003 (Spearphishing via Service), enabling more precise detection rule creation.
- **Procedures** are real-world documented instances of technique use by specific threat groups, serving as ground truth for threat intelligence.

ATT&CK supports integration with other standards. Mapping ATT&CK techniques to **CVEs** helps prioritize patch management based on which vulnerabilities are actively exploited by relevant threat actors. Alignment with **ISO/IEC 27001** controls enhances risk assessment by grounding abstract controls in real attacker behaviors. Tools such as the **ATT&CK Navigator** (a free web-based tool) allow teams to create layered views showing which techniques they can detect, which they have mitigations for, and which represent blind spots, enabling data-driven security investment decisions.

Today, ATT&CK is integrated into commercial SIEM platforms, EDR solutions, threat intelligence platforms, and red team tools. It has become the de facto language for adversary simulation, security operations, and threat intelligence sharing across the global cybersecurity community.
:::

%%%

---
unit: ATT&CK
code: TTP
title: The Attack Lifecycle, 14 ATT&CK Tactics
---
:::flow
Reconnaissance (TA0043), Gather intel via OSINT, scanning
Resource Development (TA0042), Acquire infrastructure, malware
Initial Access (TA0001), Phishing, exploit public-facing app
Execution (TA0002), Run malicious code on victim system
Persistence (TA0003), Maintain foothold across reboots
Privilege Escalation (TA0004), Gain higher-level permissions
Defense Evasion (TA0005), Avoid detection, disable logging
Credential Access (TA0006), Steal passwords, tokens, hashes
Discovery (TA0007), Enumerate network, systems, accounts
Lateral Movement (TA0008), Move to adjacent systems
Collection (TA0009), Gather files, keystrokes, screenshots
Command and Control (TA0011), Maintain attacker communication channel
Exfiltration (TA0010), Transfer stolen data out of network
Impact (TA0040), Encrypt, destroy, or manipulate data
:::

:::callout style=line
These are the 14 MITRE ATT&CK Enterprise tactics, the "what" an attacker is trying to accomplish at each stage, regardless of the specific tool used. Defenders map their controls and detection capabilities to each tactic to identify coverage gaps.
:::

:::image src="images/03_attack_lifecycle_killchain.png" alt="Circular attack lifecycle diagram showing all 14 MITRE ATT&CK tactics connected by arrows, with the defender's detection layer shown as an outer ring" caption="The ATT&CK Attack Lifecycle: 14 tactics representing the complete adversary kill chain, defense-in-depth aims to disrupt the chain at multiple points" width=full
:::

:::notes
The attack lifecycle, as conceptualized by the **MITRE ATT&CK framework**, represents the sequential phases that adversaries typically follow during a cyber intrusion. Each phase, or **tactic**, reflects a strategic objective that must be met to progress toward the ultimate goal, whether that is data theft, system disruption, or persistent access. ATT&CK's 14 Enterprise tactics provide a more granular and operationally accurate model than the classic Lockheed Martin Cyber Kill Chain (which uses 7 phases) by including early-stage activities like Reconnaissance and Resource Development that occur before any interaction with the target.

The lifecycle begins with **Reconnaissance (TA0043)** and **Resource Development (TA0042)**, phases that occur entirely outside the target environment. Attackers gather intelligence about the target's technology stack, employee names, email formats, and network topology using passive methods (DNS lookups, LinkedIn, Shodan) and active scanning. They also acquire or develop attack infrastructure: registering lookalike domains, setting up command-and-control servers, and acquiring or developing exploit code. NIST SP 800-204 emphasizes that understanding the threat environment, including how adversaries prepare, is essential to proactive defense.

**Initial Access (TA0001)** involves exploiting a vulnerability or deceiving a user to gain entry. Phishing (T1566) remains dominant due to its high success rate and low technical barrier. Exploitation of public-facing applications using published CVEs is also common, for example, CVE-2021-44228 (Log4Shell) was widely exploited for Initial Access within hours of public disclosure. Once inside, **Execution (TA0002)** deploys malicious code using scripting interpreters (T1059), Windows Management Instrumentation (T1047), or scheduled tasks.

**Persistence (TA0003)** ensures continued access across reboots via registry modifications, scheduled tasks (T1053), or boot/logon autostart entries. **Privilege Escalation (TA0004)** elevates attacker rights using vulnerability exploitation or token manipulation. **Defense Evasion (TA0005)**, often the most diverse tactic with over 40 techniques, helps attackers avoid detection by disabling security tools, obfuscating code, or abusing signed legitimate binaries (T1218, Living-off-the-Land).

With elevated privileges and evasion in place, **Credential Access (TA0006)**, **Discovery (TA0007)**, and **Lateral Movement (TA0008)** enable the attacker to understand and traverse the target network. **Collection (TA0009)** gathers relevant data, **Command and Control (TA0011)** maintains the attacker's communication channel back to their infrastructure, and **Exfiltration (TA0010)** transfers stolen data out via encrypted channels. The final **Impact (TA0040)** tactic includes ransomware encryption (T1486), data destruction (T1485), and service disruption (T1499).

This structured model supports both defensive planning and incident response, enabling precise mapping of threats to controls aligned with ISO/IEC 27001 and NIST SP 800-53.
:::

%%%

---
unit: ATT&CK
code: TTP
title: Walking Through an Attack, Live Example
---
:::steps
Attacker researches the company's employees on LinkedIn and GitHub (Reconnaissance, TA0043, T1591 Gather Victim Org Information)
A crafted spearphishing email with a malicious Office document is sent to a finance employee (Initial Access, TA0001, T1566.001)
The employee opens the document; a macro runs PowerShell that downloads a dropper payload (Execution, TA0002, T1059.001)
The dropper installs a persistent backdoor by adding a registry Run key (Persistence, TA0003, T1547.001)
The attacker exploits an unpatched local privilege escalation CVE to gain SYSTEM rights (Privilege Escalation, TA0004, T1068)
Security tools are disabled and event logs cleared to cover tracks (Defense Evasion, TA0005, T1070.001)
LSASS memory is dumped to extract domain credentials (Credential Access, TA0006, T1003.001)
The attacker maps the internal network and locates the database server (Discovery, TA0007, T1018 Remote System Discovery)
RDP is used with stolen credentials to access the database server (Lateral Movement, TA0008, T1021.001)
Customer PII is collected and staged in an encrypted archive (Collection, TA0009, T1074 Data Staged)
Data exfiltrated over HTTPS to attacker-controlled cloud storage (Exfiltration, TA0010, T1567.002)
:::

:::image src="images/03_attack_walkthrough_annotated.png" alt="Annotated network diagram showing the step-by-step attack path from phishing email through lateral movement to database exfiltration, with ATT&CK technique codes labeled at each step" caption="Annotated Attack Walkthrough: every step maps to a specific MITRE ATT&CK Tactic (TA) and Technique (T), defenders use this mapping to build detection rules targeting each stage" width=full
:::

:::notes
This eleven-step attack sequence exemplifies a canonical enterprise intrusion lifecycle, aligned with the MITRE ATT&CK Enterprise framework. Each step maps to a specific tactic and technique, demonstrating how ATT&CK transforms abstract attack descriptions into actionable, searchable, and detectable behaviors. This mapping is the foundation of **threat-informed defense**, the practice of building security controls around real attacker behaviors rather than hypothetical scenarios.

The attack begins with **Reconnaissance (TA0043)**: the attacker spends days or weeks gathering information about the target organization using open-source intelligence (OSINT). LinkedIn reveals employee names, job titles, and organizational hierarchy. GitHub repositories may expose internal tooling, API keys, or infrastructure configurations inadvertently committed to public repositories. Shodan scans reveal externally exposed services and their software versions. This entirely passive phase occurs outside the target's visibility, underscoring why threat intelligence and attack surface management are proactive defensive priorities.

**Initial Access (TA0001, T1566.001)** exploits the weakest link: human psychology. The attacker crafts a convincing spearphishing email, personalized with the recipient's name, role, and a plausible business context, containing a malicious Microsoft Office document. When the employee opens the document and enables macros (often prompted by a social engineering message within the document), **Execution (TA0002, T1059.001)** occurs: a PowerShell one-liner reaches out to the attacker's staging server and downloads a second-stage payload.

The downloaded dropper establishes **Persistence (TA0003, T1547.001)** by writing a registry Run key that relaunches the implant on every system boot. This ensures access survives reboots and partial remediation attempts. The attacker then exploits a local privilege escalation vulnerability, perhaps an unpatched kernel driver CVE, to gain SYSTEM-level rights (**Privilege Escalation, TA0004, T1068**).

With system-level access, the attacker performs **Defense Evasion (TA0005, T1070.001)**: security event logs are cleared, endpoint detection tools are disabled via registry modifications, and timestamps on malicious files are manipulated to match legitimate system files. LSASS memory is then dumped (**Credential Access, TA0006, T1003.001**) to extract domain credential hashes, a technique famously used in the 2020 SolarWinds breach to move laterally across federated environments.

Network **Discovery (TA0007)** reveals the database server hosting customer PII. **Lateral Movement (TA0008, T1021.001)** via RDP using stolen domain admin credentials grants access to the database. Customer records are collected (TA0009) and staged in an encrypted 7zip archive, then exfiltrated (**TA0010, T1567.002**) via HTTPS to an attacker-controlled cloud storage account, disguised as normal web traffic.

This walkthrough illustrates why **defense-in-depth** is essential: breaking the chain at any single point (email filtering for initial access, MFA for credential use, network segmentation limiting lateral movement, DLP for exfiltration) dramatically reduces the probability of a complete breach. NIST SP 800-53 controls mapped to each stage provide the structured control framework for this layered defense.
:::

%%%

---
unit: Summary
code: SUM
title: Mapping the Adversary, Summary
---
::::columns
::col::
:::callout style=soft
Knowing who is attacking you, and the stage of the lifecycle they're in, turns a vague sense of danger into a specific, defensible problem. Threat actor characterization feeds directly into risk assessment, control selection, and incident response prioritization.
:::
::col::
:::list heading="Core Concepts" style=chips
- Hackers (White/Grey/Black)
- Cybercriminals & RaaS
- Insider Threats
- Nation-State APTs
- Motivations Analysis
- MITRE ATT&CK
- Attack Lifecycle (14 Tactics)
:::
::col::
:::table
| Threat Actor Type     | Motivation                  | Detection Priority                  |
|-----------------------|-----------------------------|-------------------------------------|
| Script Kiddies        | Curiosity, Bragging Rights  | Web application WAF alerts          |
| Cybercriminals        | Financial Gain              | Ransomware IOCs, BEC email patterns |
| Insider Threats       | Disgruntlement, Coercion    | UEBA anomalies, access review logs  |
| Nation-State Actors   | Espionage, Disruption       | Long-dwell-time behavioral analysis |
| Hacktivists           | Ideological                 | DDoS monitoring, web integrity checks |
:::
::::

:::image src="images/03_defender_threat_intelligence_cycle.png" alt="Circular threat intelligence cycle: Identify threat actor, analyze TTPs, map to ATT&CK, build detections, monitor, update intelligence" caption="The Threat-Informed Defense Cycle: characterizing threat actors feeds ATT&CK TTP mapping, which drives detection engineering and continuous monitoring, closing the loop through incident learnings" width=full
:::

:::notes
In cybersecurity, understanding the nature of the adversary is foundational to constructing effective defenses. This process, often referred to as **threat modeling**, involves categorizing adversaries based on capability, intent, and motivation. The **NIST Cybersecurity Framework (CSF) 2.0** emphasizes this in its **Govern (GV)** function, which requires organizations to understand their threat context before making risk management decisions, and in the **Identify (ID)** function, which calls for the characterization of threat actors relevant to the organization's environment.

Threat actors span a spectrum from low-capability, opportunistic script kiddies to elite nation-state operators with virtually unlimited resources and multi-year time horizons. The appropriate defensive response differs dramatically across this spectrum:
- Against **script kiddies** and **hacktivists**, basic hardening, patching known CVEs, rate limiting web services, monitoring public-facing applications, is often sufficient.
- Against **cybercriminals**, organizations must layer controls across email security, endpoint protection, identity verification (MFA), and rapid incident response capabilities, as these actors iterate quickly based on which targets and techniques prove most profitable.
- Against **insiders**, the response must balance security with employee privacy and organizational culture, behavioral monitoring, least-privilege access, and strong offboarding procedures are key, but must be implemented with HR and legal coordination.
- Against **nation-state APTs**, traditional reactive security is insufficient. Organizations must invest in proactive threat hunting, threat intelligence subscriptions, supply chain risk management, and potentially government partnership programs like CISA advisories.

The **MITRE ATT&CK® framework** provides the structured vocabulary that connects threat actor behavior to defensive control selection. By mapping known threat group TTPs to the ATT&CK matrix and overlaying an organization's current detection capabilities (using the ATT&CK Navigator), security teams can produce a **heat map** of coverage gaps, a data-driven basis for security investment decisions.

Ultimately, this structured, threat-informed approach transforms abstract risk into actionable intelligence, enabling security teams to ask not "are we secure?", an unanswerable question, but "are we secure against our most likely and most dangerous adversaries?", a question that can be systematically answered, monitored, and continuously improved.
:::

%%%

---
unit: Threat Actors
code: SKH
title: Script Kiddies & Hacktivists, Low Sophistication, Real Impact
---
:::callout style=soft
Not every attack requires a nation-state budget or criminal syndicate. Script kiddies and hacktivists prove that low-sophistication actors can cause significant, public-facing disruption, especially against unpatched, internet-exposed systems.
:::

::::columns
::col::
:::list heading="Script Kiddies" style=plain
- Use pre-written exploit tools without understanding them
- Motivated by curiosity, peer recognition, or thrill
- Commonly target schools, gaming servers, small businesses
- Rely on known CVEs, patching eliminates most risk
- Example tools: Metasploit modules, LOIC, SQLmap
:::
::col::
:::list heading="Hacktivists" style=plain
- Driven by political, social, or ideological beliefs
- Favor DDoS, website defacement, and document leaks
- Attacks are intentionally public and attributed
- Example groups: Anonymous, LulzSec, Ghostsec
- Targets chosen for symbolic, not monetary, value
:::
::::

:::table
| Attribute | Script Kiddies | Hacktivists |
|---|---|---|
| Motivation | Curiosity / Status | Ideology / Protest |
| Skill Level | Very Low | Low–Medium |
| Targeting | Opportunistic | Deliberate (symbolic) |
| Preferred Attack | Port scanning, SQLi, DoS | DDoS, defacement, leaks |
| Attribution Sought? | Rarely | Usually, makes a statement |
| Typical Dwell Time | Minutes to hours | Hours to days |
:::

:::code language=mermaid caption="Script Kiddies vs. Hacktivists: both operate at lower sophistication levels than APTs, but their visibility and public impact can cause serious reputational and operational harm"
flowchart LR
  SK["<b>Script kiddie</b><br/>Motivation: thrill, bragging rights<br/>Tools: downloaded exploits, booter services<br/>Targets: anything vulnerable<br/>Detection: easy, noisy and unskilled"] ~~~ HA["<b>Hacktivist</b><br/>Motivation: political or social cause<br/>Tools: DDoS, defacement, data leaks<br/>Targets: organizations tied to the cause<br/>Detection: moderate, often announce themselves"]
:::

:::notes
Although script kiddies and hacktivists occupy the lower end of the threat actor sophistication spectrum, they represent a disproportionate volume of cyber incidents and deserve focused treatment. Understanding their behaviors, tools, and motivations enables defenders to prioritize the controls that most effectively neutralize these actors.

**Script kiddies** are individuals who lack deep technical expertise and rely on pre-written exploit frameworks, automated scanning tools, and publicly available proof-of-concept (PoC) code to conduct attacks. The term originated in hacker culture as a pejorative for someone who executes others' code without understanding how it works. Common tools include **Metasploit** (an open-source penetration testing framework), **SQLmap** (an automated SQL injection tool), **LOIC (Low Orbit Ion Cannon)** for DDoS attacks, and **Shodan** for identifying exposed services.

Despite their low skill level, script kiddies can cause real harm. When a high-profile CVE is published, for example, CVE-2021-44228 (Log4Shell) or CVE-2022-22965 (Spring4Shell), automated scanner tools within hours incorporate PoC exploit code, enabling even novice attackers to compromise unpatched systems at scale. The **CISA Known Exploited Vulnerabilities (KEV) Catalog** tracks which vulnerabilities are actively exploited, many of them by opportunistic, low-skill actors. Organizations that lag in patching become easy targets for this category.

Most of the best-known breaches began with an unpatched, publicly known CVE. Attacks that use known vulnerabilities, the typical method of low-skill attackers, are therefore the most preventable class of attack.

**Hacktivists** combine hacking techniques with activism, using cyber operations as a form of protest or political expression. Their objective is visibility and impact on a symbolic target rather than financial gain. The **Anonymous** collective is the most recognizable hacktivist group, known for targeting government agencies, corporations, and controversial organizations. Their 2011 operation against HBGary Federal, where CEO Aaron Barr claimed to have identified Anonymous members, resulted in the public release of 71,000 company emails and the destruction of company backups, causing significant reputational damage.

Hacktivist attacks follow a predictable pattern: public announcement of intent on social media or platforms like Pastebin, coordinated DDoS using voluntary botnets (LOIC), website defacement to spread messaging, and data dumps of leaked internal documents through WikiLeaks or similar platforms. Because attribution is actively sought by hacktivists, their operations are often noisier and more publicly documented than other threat actor categories, making them easier to track via open-source intelligence (OSINT).

From a defensive standpoint, organizations that may become hacktivist targets, those engaged in controversial industries, government operations, or public disputes, should prioritize **DDoS mitigation services** (e.g., Cloudflare, Akamai), **web application firewall (WAF)** deployment, and **incident response communications plans** to manage reputational fallout. NIST SP 800-61 (Computer Security Incident Handling Guide) recommends pre-establishing public communication templates for exactly these scenarios.

The MITRE ATT&CK framework documents techniques commonly used by hacktivists, including T1498 (Network Denial of Service), T1491 (Defacement), and T1213 (Data from Information Repositories for document leaks).
:::

%%%

---
unit: Case Study
code: CS1
title: Case Study, Anonymous vs. HBGary Federal (2011)
---
:::callout style=soft
In February 2011, the hacktivist collective Anonymous breached cybersecurity firm HBGary Federal after its CEO claimed to have infiltrated their organization. The incident demonstrated that cybersecurity firms are not immune, and that social engineering can bypass technical defenses.
:::

:::steps
HBGary Federal CEO Aaron Barr publicly claims he has identified Anonymous leadership and plans to sell the intelligence to the FBI
Anonymous discovers this through public statements and begins targeting HBGary Federal and its sister company HBGary
Attackers use SQL injection to compromise the HBGary Federal website's content management system
Credentials extracted from the CMS database are reused to access the company's email server (credential reuse / T1078 Valid Accounts)
Using email access, attackers social-engineer a system administrator to reset root credentials
Full access obtained, 71,000+ internal emails exfiltrated and published on WikiLeaks
Aaron Barr resigns; HBGary Federal's reputation is destroyed; the incident exposes planned disinformation campaigns targeting journalists
:::

::::columns
::col::
:::list heading="Attack Techniques (ATT&CK)" style=plain
- T1190, Exploit Public-Facing Application (SQLi on CMS)
- T1078, Valid Accounts (credential reuse across systems)
- T1566, Phishing / Social Engineering (admin reset)
- T1567, Exfiltration Over Web Service (WikiLeaks upload)
:::
::col::
:::list heading="Defensive Lessons" style=plain
- Never reuse passwords across systems, enforce unique credentials
- Privileged actions (password reset) must require multi-factor verification
- Web applications require SQL injection protection (parameterized queries, WAF)
- Insider communications may be subject to leak, assume breach posture
:::
::::

:::code language=mermaid caption="HBGary Federal Attack Chain (2011): a cascade of preventable failures, SQL injection, password reuse, and social engineering combined to compromise a cybersecurity firm's entire email archive"
flowchart LR
  A["SQL injection in<br/>custom CMS"] --> B["Unsalted MD5 password<br/>hashes cracked"]
  B --> C["Same passwords reused<br/>for email and servers"]
  C --> D["Social engineering of an<br/>admin to open SSH access"]
  D --> E["Tens of thousands of<br/>emails exfiltrated and leaked"]
:::

:::notes
The 2011 Anonymous breach of HBGary Federal is a landmark case study in cybersecurity education because it illustrates how a cascade of individually preventable failures can produce a catastrophic outcome, and because the victim was a professional cybersecurity firm, making the lessons particularly sobering.

The incident began when HBGary Federal CEO Aaron Barr, seeking media attention and a lucrative intelligence sale, publicly announced that he had identified key members of Anonymous through social network analysis. This provocation gave Anonymous both motivation and a high-profile target. Their response was swift and methodical.

The initial compromise leveraged **SQL injection (T1190)** against the HBGary Federal website, which was running a content management system with an unparameterized database query. SQL injection, documented as part of the **OWASP Top 10** and mapped to MITRE ATT&CK T1190, remains one of the most common and oldest web application attack vectors, first formally documented in 1998. The attack extracted the website's user database, including password hashes.

The hashes were quickly cracked (many were unsalted MD5, considered cryptographically weak per NIST SP 800-63B guidance published years earlier), revealing passwords. Here is where the second critical failure occurred: the same passwords were reused across multiple systems, including the corporate email server. This **credential reuse** (T1078 Valid Accounts) gave attackers immediate access to email without exploiting any additional vulnerabilities, they simply logged in.

With email access, attackers performed **social engineering** against a system administrator, impersonating an executive to request a root password reset for the Google Apps environment. This step required no technical skill, only persuasion and the appearance of authority. It maps to the **social engineering** techniques documented in MITRE ATT&CK TA0001 and underscores NIST's emphasis in SP 800-50 that human factors training is as critical as technical controls.

The 71,000+ exfiltrated emails revealed not only company communications but also proposed disinformation campaigns targeting WikiLeaks, journalists, and activist groups, amplifying the reputational damage. The incident raises the ethical, legal and reputational risks of aggressive offensive intelligence work. It also motivates the "assume breach" posture: sensitive communications should be written as though they may one day be public.

Key controls that would have prevented or limited this breach: parameterized database queries (preventing SQL injection), unique salted password hashing (preventing hash cracking), multi-factor authentication on privileged accounts (preventing credential reuse exploitation), and a rigorous identity verification procedure for privileged action requests (preventing social engineering success). These controls map to NIST SP 800-53 controls IA-5 (Authenticator Management), AC-3 (Access Enforcement), and SC-28 (Protection of Information at Rest).
:::

%%%

---
unit: Case Study
code: CS2
title: Case Study, Colonial Pipeline Ransomware (2021)
---
:::callout style=soft
In May 2021, the DarkSide ransomware group shut down the largest fuel pipeline in the United States using a single compromised VPN credential. The attack caused fuel shortages across the East Coast and resulted in a $4.4 million ransom payment, illustrating that critical infrastructure is a prime target for financially motivated cybercriminals.
:::

:::flow
Attackers obtain a single legacy VPN account credential (no MFA), likely purchased from a dark web marketplace
DarkSide affiliates log into Colonial's VPN using the valid credential (T1078, Valid Accounts)
Lateral movement across the network to locate OT/IT systems and backup infrastructure
Approximately 100 GB of data exfiltrated as leverage for double extortion
DarkSide ransomware deployed, encrypts billing and IT systems (T1486, Data Encrypted for Impact)
Colonial Pipeline shuts down 5,500 miles of pipeline proactively to prevent OT system spread
Colonial pays $4.4 million in Bitcoin; FBI later recovers $2.3 million
CISA and FBI release joint advisory on DarkSide TTPs; executive order EO 14028 on cybersecurity issued
:::

:::table
| Incident Detail | Value |
|---|---|
| Attack Vector | Compromised VPN credential (no MFA) |
| Threat Actor | DarkSide (RaaS affiliate model) |
| Ransom Paid | $4.4 million in Bitcoin |
| Amount Recovered by FBI | ~$2.3 million |
| Pipeline Downtime | 6 days |
| Data Exfiltrated | ~100 GB (double extortion) |
| U.S. States Impacted | 17 states + Washington D.C. (fuel shortages) |
| MITRE ATT&CK Techniques | T1078, T1486, T1567, T1490 |
:::

:::code language=mermaid caption="Colonial Pipeline Attack Timeline (May 2021): a single VPN credential with no MFA led to 6 days of pipeline downtime affecting fuel supply for 17 states, the case for MFA on all remote access systems"
flowchart TB
  A["April 29, 2021<br/>Login to a legacy VPN account: leaked password, no MFA"] --> B["May 7<br/>Ransomware deployed on IT systems"]
  B --> C["May 7<br/>Pipeline shut down as a precaution"]
  C --> D["May 8<br/>About $4.4 million ransom paid in bitcoin"]
  D --> E["June 7<br/>FBI recovers 63.7 bitcoin"]
:::

:::notes
The Colonial Pipeline ransomware attack of May 2021 stands as one of the most consequential cybersecurity incidents in U.S. history, not because of its technical sophistication, it was not particularly advanced, but because of its cascading impact on critical infrastructure and the public response it triggered. It remains a definitive case study in the intersection of financially motivated cybercrime, critical infrastructure vulnerability, and incident response decision-making under pressure.

The attack was carried out by the **DarkSide** ransomware group, operating under the Ransomware-as-a-Service (RaaS) model. DarkSide developed and maintained the ransomware platform while leasing access to affiliates who conducted the actual intrusions. The group had a self-imposed code of conduct, they claimed to avoid hospitals, schools, and non-profit organizations, but critical infrastructure was fair game.

The entry point was strikingly simple: a **single compromised VPN account** that lacked multi-factor authentication (MFA). The credentials were likely obtained from a dark web credential marketplace, where login pairs from previous data breaches are sold in bulk. This technique maps to **T1078 (Valid Accounts)** in MITRE ATT&CK and represents the most common initial access vector used by ransomware affiliates according to the **Verizon DBIR 2022**.

Once inside, the affiliates conducted reconnaissance and lateral movement over several days, exfiltrating approximately 100 GB of data for use in **double extortion**, a tactic where attackers threaten to publish stolen data if the ransom is not paid, even if the victim restores from backups. Double extortion is documented in MITRE ATT&CK T1567 (Exfiltration Over Web Service) and T1657 (Financial Theft).

On May 7, 2021, DarkSide ransomware was deployed, encrypting critical billing and IT systems. Colonial Pipeline made the difficult decision to **proactively shut down the pipeline**, a decision made to prevent the malware from spreading to operational technology (OT) systems that directly controlled physical pipeline operations. This is a critical point for discussion: the shutdown was not caused directly by the ransomware encrypting OT systems, but by Colonial's own risk-averse decision to isolate the pipeline during remediation.

The impact was severe: fuel shortages across 17 states, panic buying, price spikes, and disruption to aviation. Colonial paid the $4.4 million ransom within hours of the attack to receive the decryption key. The FBI subsequently tracked the Bitcoin wallet and recovered approximately $2.3 million of the ransom by seizing the private key, a notable law enforcement achievement demonstrating that cryptocurrency is not as anonymous as threat actors assume.

The attack directly prompted **Executive Order 14028 on Improving the Nation's Cybersecurity** (May 2021), which mandated MFA, zero-trust architecture adoption, and supply chain security standards across federal agencies and contractors. CISA issued emergency directives requiring MFA on all remote access systems in critical infrastructure sectors.

A single cyber incident can reshape national policy. The ransom decision is contested: paying can speed recovery, but it funds criminal operations and sets a precedent. CISA discourages ransom payments while acknowledging that some organizations face no viable alternative.

Key controls: MFA on all VPN and remote access systems (NIST SP 800-63B), network segmentation between IT and OT environments (NIST SP 800-82), offline backups tested regularly (NIST SP 800-53 CP-9), and an incident response plan that pre-defines shutdown criteria.
:::

%%%

---
unit: Case Study
code: CS3
title: Case Study, SolarWinds Supply Chain Attack (2020)
---
:::callout style=soft
The 2020 SolarWinds SUNBURST attack, attributed to Russian APT29, compromised the software build pipeline of a widely-used IT management platform and delivered a backdoor to approximately 18,000 organizations, including U.S. federal agencies, through a trusted software update.
:::

:::steps
APT29 compromises SolarWinds' internal software development environment
Attackers inject the SUNBURST backdoor into the Orion software build pipeline (T1195.002, Compromise Software Supply Chain)
Trojanized Orion updates (versions 2019.4 through 2020.2.1) are digitally signed with SolarWinds' legitimate certificate and distributed to ~18,000 customers
SUNBURST lies dormant for 12–14 days post-installation, mimicking legitimate Orion behavior to evade sandbox detection
Backdoor activates, beaconing to actor-controlled C2 infrastructure disguised as legitimate Orion API traffic
Attackers use SUNBURST to deploy secondary payloads (TEARDROP, Cobalt Strike) for hands-on intrusion into high-value targets
Among confirmed victims: U.S. Treasury, State Department, DHS, Microsoft, FireEye
FireEye (now Mandiant) detects the breach in December 2020 during an investigation of their own incident
:::

::::columns
::col::
:::list heading="Why This Attack Was Exceptional" style=plain
- Compromised the software supply chain, not the victim directly
- Legitimate code signing bypassed all signature-based defenses
- 12–14 day dormancy defeated sandbox and behavioral detection
- Exploited trusted vendor relationships at scale
- Dwell time estimated at 9+ months before detection
:::
::col::
:::list heading="ATT&CK Techniques" style=plain
- T1195.002, Supply Chain Compromise (Software)
- T1036, Masquerading (mimicking legitimate traffic)
- T1071, Application Layer Protocol C2
- T1027, Obfuscated Files or Information
- T1078, Valid Accounts (using legitimate credentials post-access)
:::
::::

:::code language=mermaid caption="SolarWinds SUNBURST Supply Chain Attack: the attackers never needed to breach victim networks individually, by compromising the supplier, they gained simultaneous access to thousands of organizations through a trusted update mechanism"
flowchart LR
  A["APT29 inside SolarWinds<br/>build pipeline"] --> B["SUNBURST compiled<br/>into Orion"]
  B --> C["Signed, trusted<br/>update"]
  C --> D["About 18,000<br/>customers install it"]
  D --> E["Hand-picked victims get<br/>second-stage tools"]
:::

:::notes
The SolarWinds SUNBURST attack, publicly disclosed in December 2020, represents a watershed moment in cybersecurity, a textbook Advanced Persistent Threat (APT) operation that redefined assumptions about supply chain security, trusted software, and the limits of perimeter-based defense. The attack was attributed by the U.S. government to APT29 (Cozy Bear), a threat group associated with the Russian Foreign Intelligence Service (SVR).

The attack's genius, and its defining characteristic, was that **APT29 never needed to breach victim organizations individually**. Instead, they compromised the software build pipeline of SolarWinds, a Texas-based IT management software company whose Orion platform is used by tens of thousands of organizations worldwide, including U.S. federal agencies, defense contractors, and Fortune 500 companies. By injecting malicious code into the legitimate Orion software package, attackers piggybacked on the trust relationship between SolarWinds and its customers.

The SUNBURST backdoor (tracked as **CVE-2020-10148**) was embedded in a single .dll file within the Orion update package. The code was written to blend in with existing legitimate code, it mimicked naming conventions, avoided suspicious function calls, and was compiled with the same toolchain as the rest of the application. Critically, it was **digitally signed with SolarWinds' own code-signing certificate**, meaning all signature-based security controls, antivirus, endpoint protection, and software integrity checks, treated it as a legitimate, trusted file.

Once deployed on victim systems, SUNBURST entered a **dormancy period of 12 to 14 days** before activating. This delay was deliberate: most automated sandbox analysis tools run malware for only minutes to hours. By waiting, SUNBURST bypassed automated behavioral detection entirely. When it activated, it communicated with attacker-controlled command-and-control (C2) infrastructure using **domain-generated algorithm (DGA)** subdomains of avsvmcloud[.]com, disguised as legitimate Orion telemetry traffic to evade network-based detection.

For high-value targets, APT29 deployed secondary payloads including **TEARDROP** (a custom memory-only dropper) and **Cobalt Strike** beacons for hands-on intrusion. They used stolen SAML tokens to authenticate to cloud services (including Microsoft 365 and Azure AD) as legitimate users, a technique now specifically addressed in NIST SP 800-63 and Microsoft's identity security guidance.

The breach was discovered not by any government agency or SolarWinds, but by **FireEye** (now Mandiant), who noticed a suspicious new multi-factor authentication device registration associated with one of their own employee accounts and began investigating, ultimately uncovering the full scope of the supply chain compromise.

**Key lessons for defenders:**
- Supply chain risk management (NIST SP 800-161) must include vendor software security assessments, not just hardware and personnel vetting
- Software Bill of Materials (SBOM), a machine-readable inventory of software components, can help detect unauthorized changes, and is now mandated by EO 14028 for federal software procurement
- Zero Trust principles (NIST SP 800-207), never trust, always verify, should apply even to signed software updates from trusted vendors
- Behavioral anomaly detection for cloud identity (detecting unusual SAML token use, new MFA device registrations) is critical and maps to MITRE ATT&CK T1606 (Forge Web Credentials)

SolarWinds poses the trusted-vendor problem: if a digitally signed update from a known vendor cannot be trusted, trust must come from somewhere else. Software supply chain security, code-signing ceremonies and reproducible builds address it, and NIST's Secure Software Development Framework (SSDF, SP 800-218) defines the controls on the developer side.
:::

%%%

---
unit: Threat Actors
code: FAQ
title: Common Misconceptions, Threat Actor Edition
---
:::callout style=soft
Misconceptions about threat actors lead to misallocated defenses. Challenging these assumptions is essential to building a realistic, threat-informed security posture.
:::

:::table
| Misconception | Reality |
|---|---|
| "We're too small to be targeted" | Opportunistic attackers use automated scanning, size is irrelevant; unpatched systems are targets |
| "Hackers are lone geniuses in hoodies" | Most serious attacks are conducted by organized teams with defined roles and business-like operations |
| "Nation-states only target governments" | APT groups routinely target universities, hospitals, law firms, and contractors for IP and lateral access |
| "Strong antivirus is enough protection" | Nation-state actors use custom, signed malware specifically built to evade AV signatures |
| "Insiders are easy to spot" | Malicious insiders often behave normally for weeks or months before acting, behavioral baselines take time |
| "Ransomware just encrypts files, pay and it's over" | Modern double-extortion ransomware exfiltrates data first; paying doesn't guarantee deletion |
| "MFA makes you immune to credential attacks" | MFA can be bypassed via MFA fatigue attacks, SIM swapping, or session token theft (T1539) |
| "The dark web is where all attacks are planned" | Most initial access vectors (phishing, unpatched CVEs) require no dark web involvement at all |
:::

:::notes
One of the most important, and often overlooked, aspects of cybersecurity education is the correction of deeply held misconceptions that, if left unchallenged, lead to fatally flawed security strategies. These misconceptions exist at every level of organizations, from executive boards making budget decisions to individual employees choosing whether to click a suspicious link. This slide addresses the most common and dangerous myths about threat actors.

**"We're too small to be targeted"** is perhaps the most dangerous misconception in small-to-medium business (SMB) cybersecurity. Opportunistic attackers, including script kiddies and ransomware affiliates, use automated scanning tools like Shodan, Masscan, and Censys to continuously scan the entire IPv4 address space for exposed, unpatched services. Being small does not make an organization invisible, it makes it a faster compromise with less resistance. The 2021 Verizon DBIR found that 46% of breaches involved organizations with fewer than 1,000 employees.

**"Hackers are lone geniuses"**, the Hollywood stereotype, is contradicted by the reality of modern cybercrime. Groups like LockBit, Cl0p, and ALPHV operate as structured organizations with leadership, developers, negotiators, and customer service teams (yes, ransomware groups often provide "technical support" to help victims decrypt files after payment). This business model reality has important implications: law enforcement disruption of one layer of the organization (e.g., arresting affiliates) does not eliminate the threat.

**"Nation-states only target governments"** is disproved by decades of APT targeting data. The APT10 "Cloud Hopper" campaign (2016–2018) targeted managed service providers (MSPs) as a vector to access their downstream corporate clients. APT41 has simultaneously conducted espionage against defense targets and financial fraud against gaming companies. Universities are targeted for academic research on defense, biotech, and AI. Any organization with valuable intellectual property or privileged access to a more interesting target is a potential APT target.

**"MFA makes you immune"** deserves special attention. While MFA dramatically reduces credential-based attack success rates, Microsoft estimates MFA blocks 99.9% of automated credential attacks, sophisticated adversaries have developed countermeasures. **MFA fatigue attacks** (also called MFA bombing or push spam) overwhelm users with rapid-fire push notifications until they approve one accidentally, as demonstrated in the 2022 Uber breach. **Session token theft (T1539)** allows adversaries to bypass MFA entirely by stealing authenticated browser session tokens using infostealers like Raccoon or Redline. **SIM swapping** can redirect SMS MFA codes to attacker-controlled phones.

MFA fatigue attacks exploit ordinary behavior: a user who receives dozens of push notifications in the night may approve one simply to make them stop. FIDO2/WebAuthn hardware security keys are phishing-resistant and immune to this bypass, and NIST SP 800-63B requires them at AAL3.

The **double extortion** misconception about ransomware is increasingly important. Prior to 2019, ransomware operators encrypted data and demanded payment for decryption. Starting with the Maze group in late 2019, ransomware operators began exfiltrating data *before* encryption and publishing it on "leak sites" if payment was refused. This means organizations cannot rely on backups alone, the breach component must also be addressed. The data published may include personal data triggering GDPR, HIPAA, or state breach notification requirements regardless of whether the encryption is reversed.
:::

%%%

---
unit: Insiders
code: CS4
title: Case Study, The Edward Snowden Insider Incident (2013)
---
:::callout style=soft
The 2013 disclosure of classified NSA surveillance programs by contractor Edward Snowden remains the most consequential insider threat incident in U.S. intelligence history, and a definitive example of how technical controls alone cannot prevent a determined, privileged insider.
:::

::::columns
::col::
:::list heading="Key Facts" style=plain
- Edward Snowden: NSA contractor (Booz Allen Hamilton)
- Role: Infrastructure analyst with broad system administration access
- Access Level: Top Secret / SCI (Sensitive Compartmented Information)
- Data Exfiltrated: ~1.5 million classified documents
- Method: USB drives, sysadmin credential abuse
- Destination: Journalists Glenn Greenwald and Laura Poitras
- Impact: Global diplomatic fallout; NSA reform legislation
:::
::col::
:::list heading="MITRE ATT&CK Techniques Used" style=plain
- T1078, Valid Accounts (used legitimate credentials)
- T1074, Data Staged (aggregated files before exfiltration)
- T1052, Exfiltration Over Physical Medium (USB drives)
- T1003, OS Credential Dumping (obtained others' credentials)
- T1213, Data from Information Repositories
:::
::::

:::table
| Control That Failed | Why It Failed | NIST Control Mapping |
|---|---|---|
| Need-to-know access | Snowden had broader access than his role required | AC-6 Least Privilege |
| Removable media controls | USB ports were not disabled on sensitive systems | MP-7 Media Use |
| Insider threat monitoring | Unusual bulk downloads not detected in time | SI-4 System Monitoring, AU-12 Audit Generation |
| Credential sharing controls | Snowden obtained credentials from colleagues | IA-5 Authenticator Management |
| Contractor access review | Insufficient oversight of contractor privileges | AC-2 Account Management |
:::

:::code language=mermaid caption="Snowden Incident, Control Failure Mapping: each step in the insider exfiltration chain maps to a NIST SP 800-53 control that was absent or ineffective, a textbook insider threat prevention gap analysis"
flowchart LR
  F1["Systems administrator with very broad access"] -->|"should have had"| C1["AC-6 Least Privilege"]
  F2["Coworkers' credentials borrowed and reused"] --> C2["IA-2 MFA, AC-2 Account Management"]
  F3["Bulk downloads went unnoticed"] --> C3["AU-6 Audit Review, SI-4 Monitoring"]
  F4["Data carried out on removable media"] --> C4["MP-7 Media Use"]
  F5["No second person checking sensitive actions"] --> C5["AC-5 Separation of Duties"]
:::

:::notes
The Edward Snowden case is one of the most studied insider threat incidents in history, and for good reason: it combined extraordinary scale, public impact, and a comprehensive illustration of how an insider with legitimate access can bypass or defeat nearly every technical control an organization deploys. It is also a nuanced case ethically, Snowden is regarded by some as a whistleblower and by others as a traitor, but from a security professional's perspective, the technical and procedural failures are instructive regardless of one's moral assessment.

Edward Snowden was a contractor for Booz Allen Hamilton, working on behalf of the NSA at a facility in Hawaii. His role as a **system administrator** granted him elevated, broad access to classified systems, significantly beyond what a principle of least privilege would warrant for his operational responsibilities. This is the first critical failure: **AC-6 (Least Privilege)** under NIST SP 800-53 requires that users be granted only the minimum access necessary for their job function. System administrators, by the nature of their role, often receive access far exceeding this principle, a structural vulnerability that requires compensating controls.

Snowden used his administrative access to access and aggregate documents far outside his operational scope. He reportedly persuaded colleagues to share their login credentials by claiming to need them for work-related tasks, a social engineering technique that maps to **T1078 (Valid Accounts)**. The NSA subsequently identified that at least 25 colleagues provided passwords to Snowden. This failure maps to **IA-5 (Authenticator Management)**, which prohibits credential sharing and requires individuals to be held accountable for their own authentication activities.

The exfiltration mechanism was remarkably low-tech: **USB drives**. Despite operating in one of the world's highest-classified intelligence environments, the systems Snowden accessed did not uniformly enforce removable media controls (**MP-7 Media Use** in NIST SP 800-53). In many high-security environments, USB ports are physically disabled, filled with epoxy, or controlled by endpoint DLP software that blocks unauthorized removable storage. The absence of this control at the relevant facility allowed Snowden to walk out with approximately 1.5 million classified documents.

Behavioral monitoring failures are equally instructive. Snowden's bulk download activity, accessing far more documents than his role required, should have triggered anomaly alerts in a properly configured **User and Entity Behavior Analytics (UEBA)** system. **AU-12 (Audit Record Generation)** and **SI-4 (System Monitoring)** in NIST SP 800-53 together mandate that privileged user activity be logged and monitored. The NSA has acknowledged that monitoring of insider activity at the relevant facility was insufficient.

The Snowden case illustrates the insider-threat paradox: the people with the most access, such as system administrators, security staff and executives, are the hardest to monitor, because they can often read or alter the audit logs themselves. Separation of duties (NIST control AC-5) and privileged access workstations that log tamper-evidently to immutable storage address this.

The post-Snowden landscape changed significantly. Executive Order 13587 (2011, expanded post-Snowden) established requirements for insider threat detection programs across federal agencies. The **National Insider Threat Policy** mandates continuous evaluation of personnel with security clearances. NIST SP 800-53 was updated to include the **Insider Threat (IT)** control family. The intelligence community invested heavily in UEBA tools and user activity monitoring platforms specifically designed to detect Snowden-style bulk access anomalies.

From ISO/IEC 27001 perspective, this incident maps to controls in Annex A domains A.7 (Human Resource Security), A.9 (Access Control), and A.12 (Operations Security), all of which require that the people who maintain and operate security systems are themselves subject to appropriate oversight and control.
:::

%%%

---
unit: ATT&CK
code: PHI
title: "Deep-Dive, Phishing (T1566): The Most Used Initial Access Technique"
---
:::callout style=soft
Phishing is the single most common initial access technique across all threat actor categories, from script kiddies to nation-state APTs. Understanding its variants, mechanics, and defenses is foundational to both offensive simulation and defensive strategy.
:::

:::table
| Sub-Technique | Code | Description | Example |
|---|---|---|---|
| Spearphishing Attachment | T1566.001 | Malicious file attached to targeted email | Office macro dropper sent to finance team |
| Spearphishing Link | T1566.002 | URL leading to malicious site or credential harvester | Fake M365 login page via shortened URL |
| Spearphishing via Service | T1566.003 | Phishing via LinkedIn, Teams, SMS, or other platforms | Fake recruiter LinkedIn message with malware link |
| Voice Phishing (Vishing) | T1566.004 | Phone call impersonating IT support or authority | Caller impersonating IT helpdesk to reset MFA |

:::

::::columns
::col::
:::list heading="Why Phishing Works" style=plain
- Exploits human cognitive biases (urgency, authority, fear)
- Bypasses most technical perimeter controls
- Low cost and high scalability for attackers
- Targets the weakest link, human decision-making under pressure
- Personalization via LinkedIn/OSINT increases success rates dramatically
:::
::col::
:::list heading="Defensive Controls" style=plain
- Email gateway filtering with sandboxing (NIST SP 800-177)
- DMARC, DKIM, SPF email authentication
- Security awareness training with simulated phishing
- MFA resistant to credential harvest (FIDO2/WebAuthn)
- URL rewriting and time-of-click scanning
- Reporting culture, "see something, say something"
:::
::::

:::code language=mermaid caption="Phishing T1566 Sub-Techniques: four delivery channels, one goal, deceiving a human into taking an action that creates initial access for the attacker"
mindmap
  root((Phishing T1566))
    Attachment .001
      Invoice.docm with macro
      Lever: routine work
    Link .002
      Fake password-reset page
      Lever: urgency
    Via service .003
      LinkedIn or Teams message
      Lever: trust in the platform
    Voice .004
      Call from fake help desk
      Lever: authority
:::

:::notes
Phishing is the undisputed king of initial access techniques, appearing in more data breaches than any other vector year after year. The **2023 Verizon DBIR** reports that 36% of breaches involved phishing, and across all social engineering incidents, human error was the primary enabler. MITRE ATT&CK catalogues phishing as technique T1566, with four documented sub-techniques reflecting the evolution of delivery channels from email attachments to voice calls to third-party messaging platforms.

**Why does phishing work despite decades of awareness?** The answer lies in cognitive psychology, not technical failure. Phishing exploits well-documented cognitive biases: **authority bias** (a message appearing to come from the CEO or IT department triggers compliance), **urgency bias** (a message claiming "your account will be suspended in 24 hours" short-circuits careful evaluation), **fear bias** (a message claiming "unusual activity detected on your account" triggers anxiety-driven action), and **social proof** (a message referencing a real colleague's name increases credibility). These biases are inherent to human decision-making and cannot be fully eliminated through training, only reduced in impact.

**Spearphishing (T1566.001 and .002)** is the targeted variant, where the attacker personalizes the message using information gathered during reconnaissance (TA0043). A convincing spearphishing email might reference the recipient's boss by name, mention a real project the recipient works on, and use the organization's email template styling, all information available via LinkedIn and public company documents. The 2016 DNC breach began with a spearphishing email to campaign chairman John Podesta, mimicking a legitimate Google security alert. His IT consultant mistakenly called the email "legitimate" instead of the intended word "illegitimate," and Podesta entered his credentials on the fake Google login page.

**Spearphishing via Service (T1566.003)** is a rapidly growing variant as organizations tighten email gateway controls. Attackers pivot to platforms with less filtering: LinkedIn messages from fake recruiters, WhatsApp or Teams messages from impersonated colleagues, and SMS messages (smishing) delivering malicious links. These channels often lack the sandboxing and DMARC/DKIM/SPF protections that mature email gateways provide.

**Voice phishing (vishing, T1566.004)** gained widespread attention during the 2020 Twitter hack, where attackers called Twitter employees and impersonated IT support staff, convincing them to provide VPN credentials. The 2022 Uber breach similarly used vishing to get an employee to approve an MFA push notification after being told by an attacker posing as IT security that it was a verification step.

Defensive controls must operate at multiple layers. Technical controls, email gateways with sandbox analysis, URL rewriting, DMARC enforcement, reduce the volume of phishing that reaches users. But because some phishing will inevitably reach users, **security awareness training** with realistic simulated phishing campaigns (using tools like KnowBe4, Proofpoint Security Awareness, or open-source GoPhish) is essential. NIST SP 800-50 and SP 800-177 provide guidance on both email security controls and awareness program development.

Critically, organizations should build a **reporting culture** where employees feel safe and rewarded for reporting suspected phishing, even if they clicked the link. Fear of punishment discourages reporting and delays incident response. NIST SP 800-61 recommends establishing clear, friction-free reporting channels and recognizing employees who report phishing attempts.

Proofpoint's 2023 State of the Phish report found that one user in three clicked a link in simulated phishing campaigns and one in eight submitted credentials. Human error persists even with awareness training, which is why MFA and response controls cannot be replaced by training alone.
:::

%%%

---
unit: ATT&CK
code: DEF
title: "Deep-Dive, Defense Evasion (TA0005): How Attackers Stay Hidden"
---
:::callout style=soft
Defense Evasion is the most diverse tactic in MITRE ATT&CK Enterprise, with over 40 techniques and 100+ sub-techniques. It represents attackers' methods for avoiding detection after gaining access, and understanding it reveals the gaps in signature-based security tools.
:::

:::list heading="Key Defense Evasion Techniques" style=plain
- **T1070.001**, Indicator Removal: Clear Windows Event Logs to erase evidence of activity
- **T1036**, Masquerading: Rename malware to match legitimate Windows processes (e.g., svchost.exe, explorer.exe)
- **T1218**, System Binary Proxy Execution: Use trusted Windows binaries (Living off the Land) to execute malicious code
- **T1027**, Obfuscated Files or Information: Base64-encode or encrypt payloads to bypass signature detection
- **T1562.001**, Impair Defenses: Disable or tamper with antivirus, EDR, or logging services
- **T1055**, Process Injection: Inject malicious code into a legitimate process to inherit its trust level
:::

:::table
| Evasion Category | Technique | Why It Works | Detection Method |
|---|---|---|---|
| Log Tampering | T1070, Indicator Removal | Removes forensic evidence from SIEM | Forward logs to immutable remote syslog immediately |
| LOLBins | T1218, System Binary Proxy Execution | Trusted signed binaries bypass allowlisting | Monitor command-line arguments of signed binaries |
| Fileless Malware | T1059.001, PowerShell in memory | No file on disk to scan | Script Block Logging, AMSI, memory scanning |
| Process Hollowing | T1055.012, Process Hollowing | Malicious code runs inside a trusted process | Behavioral EDR monitoring process memory integrity |
| Timestomping | T1070.006, Timestomping | Alters file timestamps to hide creation time | Hash-based integrity monitoring, not timestamp-based |
:::

:::code language=mermaid caption="Defense Evasion TA0005: the most technique-rich ATT&CK tactic, attackers invest heavily in evasion because persistence without detection is the foundation of all advanced attacks"
mindmap
  root((Defense Evasion))
    Log tampering
      Clear event logs
      Detect: log forwarding gaps
    LOLBins
      certutil, rundll32, mshta
      Detect: unusual parent processes
    Obfuscation
      Encoded scripts, packing
      Detect: script block logging
    Process injection
      Code run inside trusted processes
      Detect: EDR memory scanning
    Disabling defenses
      Stop antivirus or EDR
      Detect: tamper alerts
:::

:::notes
Defense Evasion (TA0005) is the broadest and most technically nuanced tactic in the MITRE ATT&CK Enterprise framework. With over 40 techniques and more than 100 sub-techniques as of ATT&CK v14, it reflects a fundamental reality of modern intrusions: **gaining access is only half the challenge, staying undetected is the other half**. Nation-state actors and professional ransomware groups invest extraordinary resources in evasion techniques specifically designed to defeat commercial security products, because detection means expulsion and the loss of all investment in the intrusion.

**Living off the Land (LotL)** is arguably the most impactful defense evasion category. Rather than deploying custom or known-malicious tools, attackers leverage legitimate, pre-installed Windows utilities, called **LOLBins (Living off the Land Binaries)**, to execute their objectives. Examples include using `certutil.exe` to download files (since it's a trusted Windows certificate tool), `mshta.exe` to execute remote HTML applications, `wmic.exe` for lateral movement commands, and `regsvr32.exe` to execute arbitrary code via the Squiblydoo technique. Because these are signed Microsoft binaries, they bypass application allowlisting, are trusted by antivirus solutions, and may not trigger SIEM rules designed to detect known malicious tools. The [LOLBAS Project](https://lolbas-project.github.io) catalogues hundreds of such binaries with their documented abuse cases.

**Fileless malware** represents another evasion evolution. By loading malicious code entirely in memory, typically through PowerShell scripts or reflective DLL injection, attackers leave no file on disk for antivirus scanners to analyze. Detection requires **Script Block Logging** (capturing the full decoded content of PowerShell scripts before execution), the **Antimalware Scan Interface (AMSI)** (which allows security tools to inspect in-memory scripts), and **memory scanning capabilities** in EDR platforms. NIST SP 800-92 recommends that PowerShell Script Block Logging be enabled across all enterprise endpoints as a baseline detection capability.

**Process injection (T1055)** is a family of techniques where malicious code is injected into the memory space of a legitimate, trusted process, such as `explorer.exe`, `lsass.exe`, or a browser process. The injected code inherits the legitimate process's security context, network connections, and trust level. Variants include Process Hollowing (T1055.012), where a legitimate process is launched, its code is replaced with malicious code, and execution resumes; DLL Injection (T1055.001); and Thread Execution Hijacking (T1055.003). Detection requires behavioral monitoring by EDR solutions that can inspect process memory integrity and detect unexpected cross-process memory write operations.

**Log tampering (T1070)** is a common late-stage evasion technique where attackers clear Windows Event Logs, Security logs, and application logs to remove forensic evidence of their activities. The countermeasure is **immediate, immutable log forwarding**: sending log entries to a remote SIEM or immutable log store (S3 with Object Lock, for example) the moment they are generated, so that clearing local logs does not destroy the audit trail. NIST SP 800-92 (Guide to Computer Security Log Management) mandates this architectural approach for enterprise logging.

**AV/EDR disabling (T1562.001)** involves attackers with administrative privileges modifying registry keys, stopping security services, or using driver exploits (BYOVD, Bring Your Own Vulnerable Driver) to disable endpoint protection before deploying noisy payloads like ransomware. Detection involves monitoring for unexpected termination of security processes and logging Tamper Protection events from EDR solutions.

No single control detects every technique; the uncovered techniques form the detection gap. Mapping an organization's detection capabilities onto the ATT&CK matrix shows which techniques it cannot see and gives a data-driven basis for security investment, in line with the NIST CSF Detect (DE) function.
:::

%%%

---
unit: Tools
code: NAV
title: Tool Spotlight, MITRE ATT&CK Navigator
---
:::callout style=soft
ATT&CK Navigator is a free, browser-based tool that lets security teams visualize, annotate, and compare technique coverage across the ATT&CK matrix. It is the primary tool for threat-informed defense gap analysis and adversary emulation planning.
:::

::::columns
::col::
:::list heading="What You Can Do with Navigator" style=plain
- Color-code techniques by detection status (detected / not detected / mitigated)
- Import threat group profiles to see exactly which techniques specific APT groups use
- Layer multiple matrices to compare your coverage against relevant threat groups
- Export annotated matrices for reporting to leadership or compliance auditors
- Create adversary emulation plans for red team exercises
:::
::col::
:::list heading="Key Use Cases" style=plain
- Detection gap analysis, which techniques have no detection rule?
- Purple team planning, map red team objectives to coverage gaps
- Threat intelligence, overlay APT group TTPs against your controls
- SIEM rule validation, confirm alert coverage against known techniques
- Board reporting, visual heat map of defense posture
:::
::::

:::steps
Open ATT&CK Navigator at https://mitre-attack.github.io/attack-navigator/
Select "Enterprise ATT&CK" layer (or Cloud, Mobile, ICS as appropriate)
Click "Load Layer from URL" to import a specific APT group profile (e.g., APT29 from MITRE CTI GitHub)
Create a second layer showing your current detection coverage (color techniques green = detected, yellow = partial, red = no coverage)
Use "Expand Sub-techniques" to see granular coverage at the sub-technique level
Export combined layer as SVG or Excel for gap analysis reporting
:::

:::notes
The **MITRE ATT&CK Navigator** is one of the most practically valuable free tools in the cybersecurity defender's toolkit. It transforms the abstract ATT&CK matrix into an interactive, customizable workspace for threat analysis, detection engineering, and security posture communication. Understanding how to use Navigator effectively is a core professional skill for security operations center (SOC) analysts, threat intelligence analysts, and security architects.

Navigator operates on a **layer-based model**: each layer is a JSON file describing an annotation on the ATT&CK matrix, which techniques are colored, labeled, scored, or linked. Layers can be created manually, imported from MITRE's publicly available Cyber Threat Intelligence (CTI) repository on GitHub (which contains pre-built layers for hundreds of documented threat groups), or exported from commercial threat intelligence platforms like Recorded Future, Mandiant Advantage, or CrowdStrike Falcon Intelligence.

**Threat group profiling** is one of Navigator's most powerful use cases. The MITRE CTI repository contains JSON profiles for known APT groups including APT28, APT29, Lazarus Group, APT41, and dozens more. By importing the APT29 layer, for example, a security team can immediately see every technique documented in MITRE ATT&CK as having been used by APT29 in observed real-world campaigns. This provides a prioritized list of techniques to focus detection and mitigation efforts on, based on the organization's threat landscape.

**Detection gap analysis** works by creating a coverage layer that maps the security team's current alert rules and monitoring capabilities to specific ATT&CK techniques. Techniques with confirmed detection rules are colored green; partial coverage is yellow (e.g., detected in some environments but not all); no coverage is red. When the threat group layer is overlaid, the most critical gaps, techniques used by your relevant adversaries that you currently cannot detect, immediately stand out as high-priority remediation targets. This visual representation is extraordinarily effective for communicating security gaps to leadership and making a data-driven case for budget allocation.

**Purple team exercises** use Navigator to coordinate between red teams (offensive testers simulating specific adversary TTPs) and blue teams (defenders), ensuring that the techniques tested in an exercise are selected based on actual gaps rather than arbitrary attacker preferences. This aligns with NIST SP 800-53A assessment procedures and supports continuous improvement cycles mandated by ISO/IEC 27001's Plan-Do-Check-Act model.

Navigator's **scoring capability** allows analysts to assign numerical scores to techniques, enabling heat-map visualizations where techniques are shaded by confidence, frequency, or priority. This is useful for aggregating threat intelligence from multiple sources (e.g., combining scores from industry ISAC reports, CISA advisories, and internal incident data) into a single risk-weighted view.

A gap analysis against a specific actor starts by loading that actor's profile, for example APT29, into ATT&CK Navigator and comparing it with current detection coverage. For a U.S. federal agency, a realistic APT29 target, the techniques with no coverage are the priorities.

The tool is freely available at https://mitre-attack.github.io/attack-navigator/ and requires no installation, account registration, or licensing, a key advantage for security teams of any size and budget.
:::

%%%

---
unit: ATT&CK
code: CMP
title: Comparison, Cyber Kill Chain vs. MITRE ATT&CK
---
:::callout style=soft
Both the Lockheed Martin Cyber Kill Chain and MITRE ATT&CK model attacker behavior, but they differ in granularity, scope, and practical application. Understanding both frameworks and knowing when to use each is important for security practitioners.
:::

:::table
| Dimension | Cyber Kill Chain (2011) | MITRE ATT&CK (2013–present) |
|---|---|---|
| Origin | Lockheed Martin (military "kill chain" concept) | MITRE Corporation (derived from observed APT activity) |
| Phases / Tactics | 7 phases (linear) | 14 tactics (non-linear, can skip/repeat) |
| Granularity | High-level phase descriptions | Specific techniques and sub-techniques with CVE/tool references |
| Real-World Grounding | Conceptual model | Based on observed real adversary behavior |
| Post-Compromise Coverage | Limited (stops at "Actions on Objectives") | Extensive, Persistence, Lateral Movement, C2, Exfiltration, Impact |
| Tool Integration | Limited | Integrated into SIEM, EDR, TI platforms, ATT&CK Navigator |
| Adversary Profiles | Not included | Hundreds of APT/criminal group profiles documented |
| Cloud / Mobile / ICS | Not covered | Dedicated matrices for each platform |
| Use Case | High-level strategic planning, executive communication | Detection engineering, threat hunting, adversary emulation |
:::

::::columns
::col::
:::list heading="When to Use Kill Chain" style=plain
- Briefing executives or board on attack lifecycle
- High-level incident communication during a breach
- Initial security program planning (what phases to defend)
- Training non-technical stakeholders
:::
::col::
:::list heading="When to Use ATT&CK" style=plain
- Writing SIEM detection rules for specific techniques
- Threat hunting for specific adversary behaviors
- Purple team exercise planning
- Gap analysis of detection coverage
- Mapping specific incident evidence to adversary activity
:::
::::

:::code language=mermaid caption="Cyber Kill Chain vs. MITRE ATT&CK: the Kill Chain provides intuitive phase-by-phase communication; ATT&CK provides operational depth, most mature security programs use both together"
flowchart LR
  K1["Reconnaissance, Weaponization"] --> A1["Reconnaissance, Resource Development"]
  K3["Delivery"] --> A2["Initial Access"]
  K4["Exploitation"] --> A3["Execution"]
  K5["Installation"] --> A4["Persistence, Privilege Escalation, Defense Evasion"]
  K6["Command and Control"] --> A5["Command and Control"]
  K7["Actions on Objectives"] --> A6["Credential Access, Discovery, Lateral Movement,<br/>Collection, Exfiltration, Impact"]
:::

:::notes
When security practitioners encounter both the **Lockheed Martin Cyber Kill Chain** and the **MITRE ATT&CK framework**, a common question emerges: which one should we use? The answer is nuanced, both have distinct strengths and optimal use cases, and mature security programs typically leverage both frameworks in complementary ways.

The **Cyber Kill Chain** was introduced by Lockheed Martin in 2011, derived from the military concept of a "kill chain", a structured sequence of steps required to achieve a military objective. The cyber model identifies seven sequential phases: Reconnaissance, Weaponization, Delivery, Exploitation, Installation, Command and Control, and Actions on Objectives. The model's key insight was that **every phase must succeed for an attack to achieve its goal**, defenders who interrupt any single phase prevent the attack from completing. This "break the chain" philosophy was highly influential in shifting security thinking from pure detection-after-breach to proactive disruption at earlier phases.

However, the Kill Chain has significant limitations. Its linear, 7-phase structure does not reflect the reality of modern intrusions, where attackers may skip phases, repeat them, or operate multiple phases simultaneously. It provides no mechanism for describing the specific techniques used within each phase, making it insufficient for operational detection and response work. Its coverage ends at "Actions on Objectives" without distinguishing between the significantly different behaviors of lateral movement, credential theft, data collection, and ransomware deployment, all of which ATT&CK treats as distinct, separately detectable activities.

**MITRE ATT&CK** addresses these gaps by providing operationally granular, behaviorally grounded descriptions of adversary techniques based on real-world observations. Where the Kill Chain says "Exploitation," ATT&CK specifies whether the exploitation used T1190 (Exploit Public-Facing Application), T1203 (Exploitation for Client Execution), or T1068 (Exploitation for Privilege Escalation), three very different behaviors requiring different detection approaches. This granularity enables defenders to write specific SIEM rules, configure EDR behavioral policies, and conduct precise threat hunting.

The mapping relationship between the frameworks is not one-to-one: each Kill Chain phase maps to multiple ATT&CK tactics. For example, Kill Chain "Installation" maps roughly to ATT&CK Persistence (TA0003) and Execution (TA0002). Kill Chain "Actions on Objectives" encompasses ATT&CK's Collection (TA0009), Exfiltration (TA0010), and Impact (TA0040), three distinct tactical phases with entirely different detection signatures.

In practice, security programs use the **Kill Chain for strategic communication**, explaining the attack lifecycle to executives, board members, and non-technical stakeholders in a clear, intuitive 7-step narrative, and **ATT&CK for operational work**, detection engineering, threat hunting, incident analysis, and adversary emulation. NIST SP 800-53 control CA-8 (Penetration Testing) and CA-2 (Control Assessments) implicitly align with ATT&CK by requiring that assessments reflect real adversary techniques rather than generic testing methodologies.

ATT&CK did not replace the Lockheed Martin Kill Chain; it elaborated it. Each of the seven Kill Chain stages expands into one or more of ATT&CK's 14 tactics, adding operational detail to the same sequence.
:::

%%%

---
unit: Threat Actors
code: MID1
title: Mid-Lecture Checkpoint, Threat Actors & Motivations
---
:::callout style=soft
Let's pause and solidify understanding of threat actor categories and motivations before we move into deeper ATT&CK framework content.
:::

:::list heading="Check Your Understanding" style=plain
- Can you name all five major threat actor categories and their primary motivations?
- What distinguishes a malicious insider from a compromised insider?
- Why is a nation-state APT more dangerous than a cybercriminal group, even if both steal data?
- What does "double extortion" mean in the context of ransomware, and why does it matter even if you have backups?
- Which threat actor category is most likely targeting a small dental practice? A defense contractor? A news organization?
:::

:::table
| Scenario | Most Likely Threat Actor | Primary Motivation | Key Control |
|---|---|---|---|
| Small retailer gets encrypted by ransomware | Cybercriminal (RaaS affiliate) | Financial | MFA, backups, patching |
| University research stolen over 18 months | Nation-State APT | Espionage / IP theft | Network segmentation, threat hunting |
| Voting website defaced during election | Hacktivist | Ideological | WAF, DDoS protection, integrity monitoring |
| Employee downloads customer list before quitting | Malicious Insider | Personal gain / revenge | DLP, UEBA, access reviews |
| Teenager crashes school network with DoS tool | Script Kiddie | Curiosity / disruption | Patching, rate limiting, network monitoring |
:::

:::notes
Mid-lecture checkpoints serve an essential pedagogical function: they consolidate learning before new material is introduced and surface misconceptions before they compound. This checkpoint focuses on the first half of today's content, threat actor categories and motivations, which form the foundation for all subsequent ATT&CK framework discussion.

The **five threat actor categories**, script kiddies, hacktivists, cybercriminals, insiders, and nation-state actors, form a spectrum of capability and intent. Students should be able to place any described attacker or incident on this spectrum based on observable characteristics: tool sophistication, targeting logic, operational patience, and the nature of the damage sought.

The **malicious vs. compromised insider distinction** is frequently confused. A malicious insider is a legitimate user who intentionally exploits their own access. A compromised insider is a legitimate user whose account has been taken over by an external attacker, the external attacker is the threat actor, but they operate with the insider's credentials and trust level. The practical implication: detecting a compromised insider requires behavioral baseline analysis (this account is doing things inconsistent with its history), while detecting a malicious insider requires behavioral *pattern* analysis (this user is doing things consistent with their role but at unusual times, volumes, or targets).

The **APT vs. cybercriminal distinction** around data theft is important: both steal data, but their objectives, methods, and impacts differ fundamentally. A cybercriminal steals data for immediate monetization (sale on dark web, ransomware leverage). A nation-state APT steals data for intelligence value, competitive advantage, or future operational use, and may maintain access for years without monetizing, preserving their foothold for future operations. The defense implication: cybercriminal intrusions tend to be noisy and quick; APTs are patient and quiet. Detection strategies must account for both profiles.

Threat-actor likelihood depends on context. The same technical vulnerability faces an entirely different adversary profile at a defense contractor, where nation-state actors are likely, than at a dental practice, where opportunistic criminals are.

The **backup vs. double extortion** point is critical and worth spending time on. Many organizations assume that ransomware risk is fully mitigated by having good backups. This assumption was valid for early ransomware (Cryptolocker-era, 2013–2018), but modern ransomware groups universally employ double or triple extortion. Triple extortion adds threatening to DDoS the victim's public services to the encryption + data leak threats, creating three simultaneous leverage vectors. NIST SP 800-34 (Contingency Planning Guide) and SP 800-83 (Guide to Malware Incident Prevention) both address backup strategy, but must now be read alongside an understanding that backup restoration may not prevent breach notification obligations or reputational damage from a data leak.
:::

%%%

---
unit: Threat Actors
code: DRK
title: The Dark Web, Criminal Infrastructure for Threat Actors
---
:::callout style=soft
The dark web is not a single place but a collection of overlay networks, most prominently Tor, that enable anonymous communication and commerce. For cybersecurity professionals, understanding dark web criminal infrastructure explains how threat actors acquire tools, sell stolen data, and coordinate operations.
:::

::::columns
::col::
:::list heading="What's Available on Dark Web Markets" style=plain
- Stolen credentials and database dumps (by sector/country)
- Ransomware-as-a-Service affiliate portals
- Exploit kits and zero-day vulnerabilities
- Hacking tools and botnets for rent
- Tutorials and "crime-as-a-service" services
- Counterfeit documents and financial fraud tools
:::
::col::
:::list heading="Key Dark Web Concepts for Defenders" style=plain
- Monitoring for your organization's data on paste sites and markets
- Threat intelligence feeds that surface dark web mentions of your brand
- Initial Access Brokers (IABs), criminals who sell network access
- "Combo lists", compiled credential databases from multiple breaches
- Cryptocurrency use for pseudonymous payments (Bitcoin, Monero)
:::
::::

:::table
| Dark Web Actor | Role in Criminal Ecosystem | Defense Implication |
|---|---|---|
| Initial Access Broker (IAB) | Sells VPN, RDP, or email access to victim networks | Monitor for your domains/IPs on dark web intel feeds |
| Data Broker | Sells stolen PII, credentials, health records | Have I Been Pwned, breach monitoring for your domains |
| Malware Developer | Creates and leases ransomware, RATs, infostealers | Threat intel signatures in EDR/SIEM |
| Money Launderer | Converts crypto proceeds to fiat currency | Irrelevant for most defenders, law enforcement concern |
| Forum Administrator | Runs criminal marketplace or forum | Platform takedowns coordinated with FBI/Europol |
:::

:::code language=mermaid caption="Dark Web Criminal Ecosystem: a mature marketplace where specialized criminal roles interact, defenders who monitor this ecosystem gain early warning of attacks before they materialize"
flowchart TB
  DEV["Ransomware developers<br/>run affiliate programs"] -->|"kit, revenue share"| RD["Ransomware affiliates"]
  IAB["Initial access brokers<br/>sell network logins"] --> RD
  RD -->|attack| V["Victim organizations"]
  V -->|"stolen records"| DB["Data brokers"]
  DB --> M["Dark web marketplace"]
  IAB -.-> M
  V -->|"ransom in cryptocurrency"| MIX["Mixers and exchanges"]
  MIX -->|"laundered payouts"| RD
:::

:::notes
The "dark web" is a term that generates significant confusion in mainstream media, where it is often depicted as a mysterious, monolithic criminal underworld. For cybersecurity professionals, a more precise understanding is essential: the dark web refers to content and services accessible only through overlay networks that anonymize traffic, most prominently the **Tor (The Onion Router) network**. While Tor itself has many legitimate uses, journalists in authoritarian countries, whistleblowers, privacy advocates, a portion of Tor-accessible services are criminal markets and forums.

**Initial Access Brokers (IABs)** represent one of the most practically important dark web phenomena for security defenders. IABs are specialized cybercriminals who compromise corporate networks, often via phishing, credential stuffing, or exploiting VPN vulnerabilities, and then sell that access rather than exploiting it themselves. A listing might read: "Fortune 500 manufacturing company, domain admin access, 5,000 endpoints, asking $25,000." Ransomware affiliates then purchase this access to deploy ransomware without having to perform the time-consuming initial compromise themselves. This specialization has dramatically accelerated the ransomware attack cycle.

Intelligence firms like **Recorded Future, Intel 471, Digital Shadows (now ReliaQuest), and Cybersixgill** monitor dark web markets, forums, and paste sites on behalf of enterprise clients, providing early warning when their organization's credentials, internal documents, or network access appears for sale. This intelligence enables proactive response, forcing password resets before credentials are weaponized, or patching systems before an IAB's access listing is purchased by a ransomware affiliate.

**Combo lists**, massive compiled databases of username/password pairs aggregated from multiple historical breaches, are freely shared or sold on dark web forums and Telegram channels. These lists fuel **credential stuffing** attacks (T1110.004 in MITRE ATT&CK) at massive scale. Services like **Have I Been Pwned (HIBP)**, created by security researcher Troy Hunt, allow individuals and organizations to check whether their email addresses or passwords appear in known breach databases. NIST SP 800-63B now recommends that organizations check user-chosen passwords against known breached password lists at the time of creation or change, a control directly motivated by the existence of combo lists.

**Zero-day vulnerability markets** represent the highest tier of dark web commerce. Government-affiliated brokers like Zerodium publicly advertise purchasing prices for unpatched vulnerabilities: $2.5 million for an iOS full chain exploit, $1.5 million for a Chrome browser sandbox escape. While these transactions often occur through legitimate or semi-legitimate channels (not always dark web), they illustrate the financial incentives for discovering and withholding vulnerability disclosures, a problem that coordinated vulnerability disclosure (CVD) programs, mandated in NIST SP 800-40 and championed by CISA, attempt to counterbalance.

Tor Browser, the main tool for reaching dark web markets, is legal to download and use in most countries, but buying from criminal markets is illegal, and visiting some markets can attract law-enforcement attention. Threat intelligence analysts work from isolated virtual machines with documented research justification, and defenders use dark web intelligence passively, watching for their own organization's data, never taking part in transactions.
:::

%%%

---
unit: ATT&CK
code: SCA
title: Supply Chain Attacks, Compromising Trust at Scale
---
:::callout style=soft
Supply chain attacks target software vendors, managed service providers, or hardware suppliers to compromise their downstream customers at scale. A single successful supply chain compromise can simultaneously grant access to thousands of organizations, making this one of the highest-impact attack vectors.
:::

:::table
| Supply Chain Attack Type | Description | Notable Example |
|---|---|---|
| Software Build Compromise | Malicious code injected into software before distribution | SolarWinds SUNBURST (2020) |
| Dependency Confusion | Malicious package published to override internal package names | Alex Birsan research (2021, 35+ companies affected) |
| Typosquatting | Malicious packages with names similar to popular libraries | `colourama` vs `colorama` on PyPI |
| MSP Compromise | Attack managed service providers to access their customer networks | Kaseya VSA attack (2021, REvil ransomware) |
| Hardware Implant | Malicious components inserted during manufacturing | Alleged Supermicro supply chain concern |
| Open Source Contribution | Malicious contributor inserts backdoor into open source project | XZ Utils backdoor (CVE-2024-3094) |
:::

::::columns
::col::
:::list heading="Why Supply Chain Attacks Are Effective" style=plain
- Exploit trusted relationships and code signing
- Single compromise cascades to thousands of victims
- Detection is extremely difficult, legitimate signed binaries
- Traditional perimeter controls are irrelevant (you invited the attacker in)
- Dwell time before activation can span months
:::
::col::
:::list heading="Defensive Controls" style=plain
- Software Bill of Materials (SBOM), track all components
- Verify package integrity (checksums, signatures)
- Vendor security assessment programs (NIST SP 800-161)
- Zero Trust, verify even trusted software behavior
- Dependency scanning in CI/CD pipelines (Dependabot, Snyk)
- Monitor vendor update traffic for behavioral anomalies
:::
::::

:::code language=mermaid caption="Supply Chain Attack Vectors: six pathways where attackers can insert malicious code or access into the software and service delivery chain, each one exploits a trust relationship between supplier and customer"
flowchart LR
  B["Build pipeline"] --> V
  D["Dependency repository<br/>(npm, PyPI)"] --> V
  H["Hardware and firmware"] --> V
  M["Managed service provider"] --> V
  O["Open-source contribution"] --> V
  U["Update mechanism"] --> V
  V["Trusted product or service"] --> X["Many downstream victims at once"]
:::

:::notes
Supply chain attacks represent a category of cyber threat that is growing rapidly in both frequency and impact. The defining characteristic is **indirect attack**: rather than targeting the victim organization directly, the attacker compromises a trusted third party, a software vendor, managed service provider, hardware supplier, or open source library, and uses that compromise as a stepping stone to reach the true target. This approach offers attackers extraordinary efficiency: a single supply chain compromise can simultaneously grant access to thousands of downstream organizations, each of which has explicitly trusted the compromised supplier.

The **SolarWinds SUNBURST attack** (covered in detail in an earlier slide) demonstrated the devastating potential of build pipeline compromise. However, it was not an isolated incident. The **Kaseya VSA ransomware attack** (July 2021) used a zero-day vulnerability (CVE-2021-30116) in Kaseya's VSA remote monitoring and management software, used by managed service providers, to deploy REvil ransomware to approximately 1,500 businesses through their MSPs. The attack cascaded from Kaseya to MSPs to end-customer organizations in hours, with the attacker demanding a $70 million ransom for a universal decryptor.

**Dependency confusion** (also called namespace confusion) was demonstrated by security researcher Alex Birsan in 2021. He discovered that major companies including Microsoft, Apple, PayPal, and Tesla were using internal package names in their build pipelines. By publishing packages with those exact internal names to public package repositories (npm, PyPI, RubyGems), which take precedence over internal repositories by default in many build tool configurations, he caused development machines at 35+ companies to automatically download and execute his test packages. He collected $130,000+ in bug bounty awards. The attack required no traditional hacking, just understanding how package resolution priority works.

The **XZ Utils backdoor** (CVE-2024-3094, disclosed March 2024) is a chilling example of a long-term social engineering attack on open source infrastructure. An attacker using the identity "Jia Tan" spent approximately two years contributing legitimate, helpful code to the XZ Utils data compression library, building trust with the maintainer, before inserting a sophisticated backdoor targeting systemd-linked SSH authentication on Linux systems. The backdoor was discovered by Microsoft developer Andres Freund only by chance, after noticing unexpected CPU usage. The attacker's patience, two years of legitimate contribution as cover, exemplifies nation-state-level operational security.

**Software Bill of Materials (SBOM)** is now the primary defensive response to dependency and supply chain risks. An SBOM is a machine-readable inventory of all software components in an application, including third-party libraries and their versions. **Executive Order 14028** mandates SBOMs for all software sold to the U.S. federal government, and **NIST SP 800-218** (Secure Software Development Framework) recommends SBOM generation as part of secure build practices. With an SBOM, organizations can rapidly determine whether a newly announced vulnerable component (e.g., Log4j's Log4Shell) exists in any of their applications, dramatically reducing response time.

The XZ Utils backdoor shows that supply chain attacks are not limited to commercial software. Open-source libraries that run critical infrastructure can be compromised by socially engineering volunteer maintainers, who often have no security team, no budget and heavy time pressure.

**NIST SP 800-161** (Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations) provides the comprehensive framework for organizational supply chain risk management, including vendor assessment criteria, contractual security requirements, and ongoing monitoring obligations.
:::

%%%

---
unit: Threat Actors
code: BBP
title: Bug Bounty Programs, Turning Hackers into Allies
---
:::callout style=soft
Bug bounty programs create formal, legal channels for security researchers, including grey and white hat hackers, to report vulnerabilities to organizations in exchange for recognition or financial reward. They transform a potential adversarial relationship into a collaborative security asset.
:::

::::columns
::col::
:::list heading="How Bug Bounty Programs Work" style=plain
- Organization publishes a scope defining which systems/applications are in-scope for testing
- Researchers (worldwide) independently probe in-scope targets for vulnerabilities
- Discovered vulnerabilities reported through a coordinated disclosure platform (HackerOne, Bugcrowd, Intigriti)
- Organization triages, validates, and patches the vulnerability
- Researcher receives bounty payment based on severity (CVSS score) and impact
- CVE may be published after patch release (responsible disclosure)
:::
::col::
:::list heading="Notable Bug Bounty Programs" style=plain
- Google: $31M+ paid since 2010, up to $151,515 for Chrome RCE
- Microsoft: Up to $250,000 for Hyper-V remote code execution
- Apple: Up to $1,000,000 for zero-click kernel exploits
- U.S. Department of Defense: "Hack the Pentagon" program (first federal BBP)
- Facebook: $1.5M+ annually through Meta's program
:::
::::

:::table
| Metric | Value |
|---|---|
| HackerOne platform researchers | 1,000,000+ registered |
| Total bounties paid across all programs | $300M+ (as of 2023) |
| Average critical vulnerability bounty | $3,000–$10,000+ |
| Average time to fix after report | 30–70 days depending on platform/program |
| Percentage of HackerOne bugs that are critical/high | ~15% |
:::

:::code language=mermaid caption="Bug Bounty Vulnerability Lifecycle: coordinated disclosure turns vulnerability discovery from a liability into a controlled security improvement, defenders gain early warning before malicious actors can exploit the same vulnerability"
flowchart LR
  A["Researcher finds<br/>a vulnerability"] --> B["Reports via HackerOne,<br/>Bugcrowd or VDP"]
  B --> C["Organization triages<br/>and patches"]
  C --> D["CVE assigned"]
  D --> E["Public disclosure<br/>after the fix"]
  E --> F["Researcher receives<br/>bounty and credit"]
:::

:::notes
Bug bounty programs represent one of the most effective, and arguably one of the most underutilized, security tools available to organizations of all sizes. The concept builds on a simple insight: the community of skilled security researchers worldwide vastly outnumbers any organization's internal security team, and many of those researchers will probe your systems regardless of whether you have a formal program. A bug bounty program channels that activity into a legal, controlled, productive relationship, replacing the potential for unauthorized testing (grey hat activity) with authorized, rewarded research.

The legal foundation for bug bounty programs is typically a **Vulnerability Disclosure Policy (VDP)** or a more comprehensive **Bug Bounty Policy**, both of which explicitly authorize specific testing activities on defined scope assets. Without this authorization, security researchers probing systems, even with good intentions, risk criminal liability under laws like the **Computer Fraud and Abuse Act (CFAA)** in the United States, the **Computer Misuse Act** in the United Kingdom, or equivalent statutes worldwide. The VDP creates a legal safe harbor for researchers acting in good faith within defined scope.

**CISA** now mandates that all U.S. federal civilian agencies maintain a public VDP under Binding Operational Directive (BOD) 20-01, recognizing the security value of coordinated vulnerability disclosure for government systems. The "Hack the Pentagon" program, launched in 2016, was the first federal bug bounty program, it ran for 24 days, engaged 1,400 researchers, and resulted in 138 valid vulnerabilities reported for a cost far lower than equivalent internal testing would have required.

**Platforms** like HackerOne, Bugcrowd, and Intigriti serve as intermediaries: they provide the infrastructure for report submission, triage workflow management, bounty payment processing, and program reputation management. They also allow organizations to expand programs from private (invitation-only, typically used for initial program launch) to public (open to all researchers) as their triage capacity and program maturity increase.

The **economics of bug bounties** are compelling. A critical vulnerability discovered internally might cost $50,000–$200,000 in security assessment hours. A researcher discovering and reporting the same vulnerability via a bug bounty program might receive $3,000–$15,000, a fraction of the cost, and the organization benefits from hundreds of researchers looking simultaneously. When Google paid $10 million to a researcher who discovered a critical Chrome Remote Code Execution vulnerability, that payment was cost-effective compared to the breach costs that could have resulted if a malicious actor found it first.

Bug bounties sit in tension with the vulnerability market. A researcher who reports a flaw to the vendor for a $5,000 bounty may be giving up a far larger sum from a zero-day broker. Responsible disclosure depends on incentives such as fair bounties, legal safe harbor and professional reputation.

For organizations considering starting a bug bounty program, **NIST SP 800-53 RA-5** (Vulnerability Scanning) and **CA-8** (Penetration Testing) provide the control framework context, while CISA's **VDP Platform** provides a free government-hosted platform for federal agencies to manage their disclosure programs. The **ISO/IEC 30111** standard and **ISO/IEC 29147** provide international frameworks for vulnerability handling and disclosure processes.
:::

%%%

---
unit: ATT&CK
code: OSI
title: OSINT & Reconnaissance, Seeing Through the Attacker's Eyes
---
:::callout style=soft
Reconnaissance (TA0043) is the first ATT&CK tactic and the phase where defenders are most blind. Understanding how attackers gather intelligence about targets from public sources enables organizations to reduce their attack surface before any intrusion attempt begins.
:::

:::list heading="Common OSINT Sources Attackers Use" style=plain
- **LinkedIn**, employee names, org chart, technologies used (job postings reveal tech stack)
- **Shodan / Censys / FOFA**, internet-exposed services, banners, versions, certificates
- **GitHub / GitLab**, accidentally committed credentials, API keys, infrastructure configs
- **WHOIS / DNS records**, domain registrants, mail servers, subdomains (passive DNS)
- **Google Dorks**, advanced search operators to find exposed files, login pages, cameras
- **wayback Machine**, historical web content revealing old/hidden functionality
- **Pastebin / GitHub Gists**, leaked internal data, credentials posted publicly
- **Certificate Transparency Logs**, enumerate subdomains from SSL certificate records
:::

:::steps
Identify the target organization and its internet-facing assets (domain, IP ranges, subsidiaries)
Use Shodan to find exposed services: VPN gateways, email servers, admin panels, IoT devices
Search LinkedIn for IT staff job titles to infer the technology stack (e.g., "Cisco ASA Administrator" = Cisco VPN in use)
Run theHarvester or Amass to enumerate subdomains and email addresses via DNS and certificate transparency
Search GitHub for the company name, domain, and employee usernames to find accidentally exposed credentials
Correlate collected data to identify the most vulnerable initial access point (outdated VPN, unpatched web app, exposed RDP)
:::

:::code language=mermaid caption="OSINT Reconnaissance Sources: the information an attacker assembles before touching a single target system, organizations can audit their own exposure using the same tools and techniques"
mindmap
  root((Target organization))
    LinkedIn
      Staff names, roles, tech skills
    Shodan
      Exposed devices and open ports
    GitHub
      Leaked keys, internal hostnames
    DNS
      Subdomains, mail servers
    Google dorks
      Indexed documents and login pages
    Certificate transparency
      New and forgotten hostnames
    Paste sites
      Leaked credentials
:::

:::notes
Reconnaissance (TA0043) is the ATT&CK tactic that occurs entirely *before* any interaction with the target's systems, meaning traditional perimeter security controls, network-based intrusion detection, and endpoint protection are all irrelevant during this phase. The attacker operates purely on publicly available information, and the organization has no direct ability to prevent or detect reconnaissance activity against them. This asymmetry makes reconnaissance reduction, minimizing publicly available information about your organization's technology, personnel, and infrastructure, a proactive and valuable security practice.

**OSINT (Open-Source Intelligence)** is the practice of collecting information from publicly available sources. Every legitimate OSINT technique an attacker uses is also available to defenders conducting their own attack surface analysis. Organizations that regularly perform OSINT audits on themselves, searching for accidentally exposed credentials on GitHub, overly detailed job postings that reveal their exact technology stack, or internet-exposed services they didn't know were public, gain the same intelligence advantage as their adversaries.

**Shodan and Censys** are internet search engines that index metadata about internet-connected devices and services. A Shodan search for a company's IP ranges reveals exposed services, their software versions, and sometimes their banner strings (which often include exact version numbers and configuration details). Security teams should regularly audit their Shodan and Censys presence, any internet-exposed service that does not need to be public should be restricted, and all public services should be running current, patched versions. NIST SP 800-40 (Guide to Enterprise Patch Management) emphasizes this continuous asset visibility requirement.

**GitHub credential exposure** is a pervasive problem. Developers frequently accidentally commit API keys, database connection strings, AWS credentials, and private cryptographic keys to public repositories. Tools like **truffleHog**, **GitLeaks**, and **GitHub's own secret scanning feature** automatically detect common credential patterns in repository commits. Organizations should enable GitHub secret scanning on all repositories, configure pre-commit hooks to prevent credential commits, and implement automated rotation for any credentials that might have been exposed. AWS, for example, automatically revokes and notifies about IAM credentials detected in public GitHub repositories, a service-level compensating control for this common mistake.

**LinkedIn as an attack surface** is underappreciated. A company's LinkedIn page and employee profiles collectively reveal: the names and roles of security personnel (who to impersonate or target with spearphishing), the technology stack (through job postings requiring specific product experience), the organizational hierarchy (who reports to whom, useful for BEC targeting), and recent hiring patterns (suggesting organizational changes and potential knowledge gaps). Security-aware organizations scrub excessive technology specificity from job postings, "experience with enterprise security platforms" rather than "experience with Palo Alto Prisma CASB version 4.x."

**Certificate Transparency (CT) logs** are public databases of all TLS/SSL certificates issued by publicly trusted certificate authorities, required by the CA/Browser Forum to enable detection of misissued certificates. Security researchers repurposed CT logs as an OSINT tool: every subdomain for which a certificate has been issued appears in CT logs, enabling enumeration of subdomains far beyond what DNS zone enumeration can achieve. Tools like **Cert.sh**, **Amass**, and **Subfinder** automate CT log querying for subdomain enumeration.

OSINT can assemble a detailed picture of a large organization from public sources alone: Shodan for exposed services, LinkedIn for staff and technologies, and certificate transparency logs for hostnames. The volume of information available without any intrusion is the point.

The MITRE ATT&CK sub-techniques under TA0043 include T1589 (Gather Victim Identity Information), T1590 (Gather Victim Network Information), T1591 (Gather Victim Org Information), T1592 (Gather Victim Host Information), and T1593 (Search Open Websites/Domains), together providing a comprehensive taxonomy of reconnaissance activities that defenders can use to structure their own attack surface audits.
:::

%%%

---
unit: ATT&CK
code: WRK
title: Worked Example, Building a Threat Profile for a Hospital
---
:::callout style=soft
Threat profiles connect threat actor categories, motivations, and ATT&CK TTPs to a specific organizational context. This worked example builds a threat profile for a regional hospital system, applying everything from this lecture to a realistic sector.
:::

::::columns
::col::
:::list heading="Hospital System Profile" style=plain
- 2,000 employees; 3 locations
- Electronic Health Records (EHR) on Epic platform
- Connected medical devices (IoT, infusion pumps, imaging)
- HIPAA-regulated; breach notification mandated
- Internet-facing patient portal and telemedicine platform
- Staff: physicians, nurses, IT generalists (not security specialists)
:::
::col::
:::list heading="Step 1: Identify Relevant Threat Actors" style=plain
- Cybercriminals (ransomware), HIGH likelihood; healthcare is top target
- Nation-state actors, MEDIUM likelihood; medical research data, COVID IP
- Malicious insiders, MEDIUM likelihood; patient record snooping, data theft
- Hacktivists, LOW likelihood unless politically controversial procedures offered
- Script kiddies, LOW impact; patching eliminates most opportunistic risk
:::
::::

:::table
| Threat Actor | Most Likely ATT&CK Techniques | Priority Controls (NIST SP 800-53) |
|---|---|---|
| Ransomware Affiliate | T1566.001 Phishing, T1078 Valid Accounts, T1486 Data Encrypted | MFA (IA-5), Offline Backups (CP-9), Email Sandbox |
| Nation-State APT | T1195 Supply Chain, T1036 Masquerading, T1071 C2 over HTTPS | Network Segmentation (SC-7), Threat Hunting, EDR |
| Malicious Insider | T1074 Data Staged, T1052 USB Exfil, T1213 EHR Data Access | UEBA (SI-4), Least Privilege (AC-6), DLP (SI-12) |
| Compromised Insider | T1078 Valid Accounts, T1539 Session Token Theft | Behavioral Baseline, Anomaly Alerts, SIEM |
:::

:::code language=mermaid caption="Hospital Threat Profile: the output of threat actor analysis applied to a specific sector, this document drives control prioritization, investment decisions, and incident response pre-planning"
flowchart TB
  subgraph R["Ransomware gangs: likelihood High"]
    R1["T1566 Phishing, T1133 External Remote Services, T1486 Data Encrypted for Impact"]
    R2["Controls: offline backups, MFA, EDR"]
  end
  subgraph N["Nation-states: likelihood Medium"]
    N1["T1190 Exploit Public-Facing App, T1078 Valid Accounts, T1041 Exfiltration over C2"]
    N2["Controls: patching, network monitoring"]
  end
  subgraph I["Insiders: likelihood Medium"]
    I1["T1078 Valid Accounts, T1005 Data from Local System, T1052 Exfiltration over USB"]
    I2["Controls: access reviews, DLP, audit logs"]
  end
  subgraph H["Hacktivists: likelihood Low"]
    H1["T1498 Network DoS, T1491 Defacement, T1595 Active Scanning"]
    H2["Controls: DDoS protection, web hardening"]
  end
  R ~~~ N
  I ~~~ H
:::

:::notes
Building a **threat profile** is the practical output of threat actor analysis, the document or structured assessment that translates abstract threat landscape knowledge into actionable, organization-specific guidance. This is the core deliverable of the **NIST Cybersecurity Framework Govern (GV.RM)** function, which requires organizations to understand their threat context as the foundation of all subsequent risk management decisions.

The healthcare sector provides an excellent worked example because it faces a uniquely complex threat landscape: it is simultaneously one of the most targeted sectors by ransomware groups (due to the operational criticality of systems and the value of patient data), a target of nation-state espionage (medical research, particularly vaccine and pharmaceutical research, has significant geopolitical value), a sector with significant insider threat exposure (patient records are regularly accessed by staff, creating abundant opportunity for unauthorized access), and an environment with significant legacy and IoT device challenges (medical devices running unsupported operating systems cannot always be patched).

**Why healthcare is the top ransomware target:** Patient data is valued at $250–$500 per record on dark web markets, compared to $5–10 for credit card data. More critically, hospitals cannot tolerate system downtime, patients die if EHR access is lost, imaging systems fail, or medication dispensing systems are unavailable. This operational criticality gives ransomware operators extraordinary leverage, often compelling payment even when the organization has backups, because restoration time alone could cost lives. The **2020 Düsseldorf University Hospital** ransomware attack, where a patient was diverted to another hospital and died during transport, potentially linked to the system outage, illustrates this life-safety dimension.

**Building the threat actor likelihood assessment** involves analyzing: sector-specific incident data (DBIR healthcare sector statistics, HHS HIPAA breach portal data, CISA healthcare advisories), the organization's specific characteristics (research hospital vs. community hospital, academic medical center with research IP vs. regional clinic), and the organization's existing security posture (prior breaches, audit findings, known vulnerabilities from assessment).

For the hypothetical regional hospital in this example, the **ransomware affiliate threat is high priority** because regional hospitals typically lack the security budgets, dedicated security teams, and technical controls of large academic medical centers, making them attractive targets for affiliates using automated attack toolkits who prioritize ease of compromise over target prestige.

The **nation-state threat** would be elevated to HIGH if the hospital conducted vaccine research, military medicine research, or had affiliations with government health agencies, but for a standard regional hospital, it remains medium.

**Priority controls from the threat profile:** The analysis identifies MFA on all email and remote access systems as the highest-priority single control, it directly counters the most common initial access vector (credential-based attacks and phishing for valid accounts) used by the highest-priority threat actor (ransomware affiliates). Offline backups tested quarterly address the ransomware impact phase. Network segmentation isolating medical devices from business systems limits lateral movement from a compromised workstation to life-safety systems. UEBA baseline monitoring of EHR access patterns detects both malicious and compromised insider activity.

This prioritization approach, driven by threat actor analysis rather than compliance checkbox completion, aligns with the **NIST CSF 2.0 Govern function** and represents the difference between a security program that systematically reduces the most likely and impactful risks versus one that spends equal resources on all possible risks regardless of probability.

A threat profile names the two most likely threat actors for an organization, the ATT&CK techniques they would most likely use and the defensive controls that matter most. Profiles for a university, a local government, a retail bank and a law firm differ completely, and so do the optimal security investments.
:::

%%%

---
unit: ATT&CK
code: MID2
title: Mid-Lecture Checkpoint, MITRE ATT&CK Framework
---
:::callout style=soft
Let's consolidate ATT&CK framework knowledge before we close the lecture. These questions target the operational application of ATT&CK, the skills you'll use in a SOC, red team, or security architecture role.
:::

:::list heading="Check Your Understanding" style=plain
- What is the difference between a Tactic, a Technique, and a Sub-technique in ATT&CK?
- Which ATT&CK tactic has the most techniques? Why does that make sense from an attacker's perspective?
- A SIEM alert fires on "PowerShell Encoded Command." Which ATT&CK technique does this map to? Which tactic?
- Why might an attacker skip the Exfiltration tactic entirely but still achieve their primary objective?
- How would you use ATT&CK Navigator to justify a security budget increase to your CISO?
- What is the key operational difference between the Cyber Kill Chain and MITRE ATT&CK?
:::

:::table
| ATT&CK Question | Answer |
|---|---|
| What does TA0043 represent? | Reconnaissance, the first tactic in ATT&CK Enterprise |
| What technique is "credential dumping from LSASS"? | T1003.001, OS Credential Dumping: LSASS Memory |
| What tactic covers "clearing Windows Event Logs"? | Defense Evasion (TA0005), T1070.001 |
| What does "T1566.002" describe? | Spearphishing Link, a sub-technique of Phishing (T1566) |
| Which tactic is "moving from one system to another using stolen credentials"? | Lateral Movement (TA0008) |
| What ATT&CK component provides real-world examples of technique use? | Procedures, documented instances of specific threat groups using specific techniques |
:::

:::notes
This second mid-lecture checkpoint shifts focus from threat actor characterization (the first checkpoint) to operational ATT&CK framework application. The questions here target the practical skills that differentiate a security professional who has read about ATT&CK from one who can apply it in a SOC, red team operation, or security architecture review.

The **Tactic/Technique/Sub-technique hierarchy** is fundamental and worth reviewing. A **Tactic** (identified by TA numbers like TA0043) is the adversary's strategic objective, what they are trying to accomplish. A **Technique** (identified by T numbers like T1566) is how they accomplish that objective. A **Sub-technique** (identified by T numbers with a decimal suffix like T1566.001) is a specific variant of the technique, different enough in behavior and detection approach to warrant its own entry. Understanding this hierarchy is essential for writing detection rules: a rule targeting T1566 (all phishing) will fire on different signals than one targeting T1566.001 (specifically malicious email attachments) versus T1566.002 (malicious links).

**Defense Evasion (TA0005) as the most technique-rich tactic** reflects an important attacker logic: once inside a network, an attacker's primary challenge shifts from gaining access to maintaining it without being detected and expelled. The investment in evasion is proportional to the investment already made in achieving access, sophisticated attackers who spend weeks on reconnaissance and initial access cannot afford to lose their foothold to an antivirus detection after 10 minutes. This creates an arms race between attacker evasion innovation and defender detection capability expansion.

The **PowerShell Encoded Command** scenario maps to **T1059.001** (Command and Scripting Interpreter: PowerShell) under the **Execution (TA0002)** tactic, but the encoding component specifically also maps to **T1027** (Obfuscated Files or Information) under **Defense Evasion (TA0005)**. A single malicious action can simultaneously manifest multiple ATT&CK techniques, reinforcing that ATT&CK is not a linear checklist but a multi-dimensional behavior taxonomy.

The **"skip Exfiltration" scenario** typically applies to ransomware operators and destructive attacks (Impact-focused campaigns). If the attacker's goal is to encrypt files and demand payment, they never need to exfiltrate data, they simply deploy the ransomware directly. Early ransomware (pre-2019) operated this way. This underscores that ATT&CK is not a required-linear sequence, adversaries pursue only the tactics relevant to their objective.

**ATT&CK Navigator for CISO briefing** involves creating a heat map showing: (a) the techniques used by your organization's most likely threat actors, colored in one layer; (b) your current detection coverage, colored in a second layer; (c) the gaps where high-priority techniques have no detection coverage. This visual immediately communicates: "here are the attacks we face, here's what we can currently detect, and here's what we need to invest in to close these gaps." This transforms a budget conversation from "we need money for security" to "here are the specific gaps we need to close and here is what each gap costs to address."

:::

%%%

---
unit: Summary
code: ZTA
title: Zero Trust Architecture, Defense Against All Threat Actors
---
:::callout style=soft
Zero Trust is a security architecture principle that eliminates implicit trust from network design. Rather than trusting users because they are "inside the perimeter," Zero Trust requires continuous verification of every access request, from both inside and outside the network, against defined policy. It is directly motivated by the threat actor landscape we've studied today.
:::

:::table
| Traditional Security Assumption | Zero Trust Replacement |
|---|---|
| "Inside the network = trusted" | No implicit trust based on network location |
| "Users authenticate once at login" | Continuous authentication and authorization for every resource access |
| "Perimeter firewall keeps attackers out" | Assume breach, attackers may already be inside |
| "Lateral movement is hard for outsiders" | Microsegmentation limits movement even for insiders and compromised accounts |
| "VPN grants access to the network" | VPN replaced by identity-aware proxies granting per-application access |
:::

::::columns
::col::
:::list heading="Zero Trust Core Principles (NIST SP 800-207)" style=plain
- Verify explicitly, authenticate and authorize every request
- Use least privileged access, minimum access for minimum time
- Assume breach, design as if the attacker is already inside
- Inspect and log all traffic, encrypted or not
- Apply policy dynamically based on user, device, and context
:::
::col::
:::list heading="How ZTA Addresses Each Threat Actor" style=plain
- Script kiddies: no exploitable trusted zone to pivot from
- Cybercriminals: stolen credentials alone don't grant broad access
- Insiders: least privilege limits blast radius of any single account
- Nation-state APTs: microsegmentation limits lateral movement
- Compromised accounts: behavioral anomaly triggers re-verification
:::
::::

:::code language=mermaid caption="Zero Trust Architecture: every threat actor category benefits from the elimination of implicit trust, ZTA directly counters the TTPs that enable lateral movement, insider exploitation, and credential-based attacks"
flowchart LR
  U["User and device"] --> IV{"Identity verified?<br/>MFA"}
  IV -->|yes| DH{"Device healthy?<br/>patched, managed"}
  DH -->|yes| PP{"Policy allows this<br/>resource now?"}
  PP -->|yes| RS["Single resource,<br/>least privilege"]
  IV -->|no| X1["Blocked"]
  DH -->|no| X2["Blocked"]
  PP -->|no| X3["Blocked"]
  A["Attacker with stolen password"] -.-> IV
:::

:::notes
Zero Trust Architecture (ZTA) is the most significant architectural shift in enterprise security in the past decade, and its emergence is directly driven by the threat actor landscape we have studied throughout this lecture. Traditional perimeter-based security rested on a fundamentally flawed assumption: that users and systems inside the corporate network could be trusted, and threats came primarily from outside the perimeter. This assumption is invalidated by nearly every threat actor category we have discussed.

**Insider threats** (malicious, negligent, and compromised) demonstrate that internal network position cannot imply trust. **Nation-state APTs** with dwell times exceeding 200 days demonstrate that perimeters are regularly breached without detection, and that an attacker inside the network with implicit trust can traverse freely. **Supply chain attacks** deliver malware through trusted software update mechanisms that perimeter controls explicitly permit. **Credential attacks** give attackers valid credentials that perimeter authentication accepts without question. Together, these threat actors collectively prove that the perimeter-trust model is architecturally insufficient.

**NIST SP 800-207** (Zero Trust Architecture), published in August 2020, provides the authoritative federal guidance on ZTA principles and implementation. It defines three core tenets: **verify explicitly** (never assume trust based on network location; authenticate and authorize every request), **use least privileged access** (grant minimum permissions for minimum time, using just-in-time and just-enough-access approaches), and **assume breach** (design as if the adversary is already inside the network, monitor all traffic, minimize blast radius, log everything).

**How ZTA addresses specific ATT&CK tactics:**
- **Lateral Movement (TA0008)**: microsegmentation restricts east-west traffic between workloads, limiting an attacker's ability to move from a compromised workstation to a database server. Even with valid credentials, policy enforcement points require contextual re-authorization for each new resource.
- **Credential Access (TA0006)**: even if an attacker obtains a user's password via T1003 (credential dumping), Zero Trust's continuous verification evaluates device health, location, behavior baseline, and access time before granting resource access, potentially blocking the stolen credential's use.
- **Persistence (TA0003)**: regular re-verification cycles and device health checks can detect implants that cause device posture degradation, triggering re-authentication or access revocation.
- **Defense Evasion (TA0005)**: Zero Trust's comprehensive logging of all traffic, including encrypted traffic via TLS inspection where policy permits, reduces the effectiveness of evasion techniques that rely on blending with normal traffic.

**Implementation reality:** Zero Trust is a journey, not a product. No single product makes an organization "Zero Trust." Implementation requires identity consolidation (moving to a single IdP with strong MFA), device management (ensuring all devices are enrolled, healthy, and policy-compliant), application access modernization (replacing broad VPN network access with per-application, identity-aware proxies like Zscaler or Cloudflare Access), and network microsegmentation (deploying software-defined perimeters that enforce policy between workloads). **CISA's Zero Trust Maturity Model** (2023) provides a five-pillar framework (Identity, Devices, Networks, Applications & Workloads, Data) with maturity levels from Traditional through Optimal, useful for planning incremental implementation.

Zero Trust is often dismissed as marketing or as too disruptive to deploy. Both objections have some basis: vendors market ZTA heavily, and full implementation is complex. Its principles, verify explicitly, use least privilege and assume breach, are nonetheless sound, follow directly from the threat landscape and can be adopted incrementally.

**Executive Order 14028** (May 2021) mandated Zero Trust Architecture adoption across all U.S. federal agencies, with specific milestones established by CISA and OMB Memorandum M-22-09 (Moving the U.S. Government Toward Zero Trust Cybersecurity Principles, January 2022), which set concrete requirements for MFA, device trust, and network segmentation across federal civilian agencies by end of fiscal year 2024.
:::

%%%

---
unit: Summary
code: TII
title: Threat Intelligence, Turning Data into Actionable Defense
---
:::callout style=soft
Threat intelligence transforms raw data about threat actors, campaigns, and techniques into actionable information that improves security decisions. Understanding the types, sources, and application of threat intelligence closes the loop between threat actor analysis and operational defense.
:::

:::table
| Intelligence Type | Description | Consumer | Example |
|---|---|---|---|
| Strategic | High-level trends, threat actor motivations, geopolitical context | CISO, Board, Risk Committee | "Nation-state APT activity targeting energy sector increased 40% this quarter" |
| Operational | Specific campaigns, actor behaviors, planned operations | SOC Manager, Incident Response Team | "APT29 is targeting EU diplomatic organizations via spearphishing this month" |
| Tactical | Specific TTPs, malware behaviors, attack patterns | Security Engineers, Detection Engineers | "SUNBURST uses DGA domains resolving to avsvmcloud[.]com for C2" |
| Technical | Specific IoCs: IPs, domains, file hashes, YARA rules | SIEM, EDR, Firewall, IDS | SHA256: [SUNBURST malware hash], IP: 13.59.205.99 (C2 server) |
:::

::::columns
::col::
:::list heading="Threat Intelligence Sources" style=plain
- CISA Advisories and Known Exploited Vulnerabilities (KEV) catalog
- MITRE ATT&CK threat group profiles
- Industry ISACs (Information Sharing and Analysis Centers)
- Commercial TI platforms (Recorded Future, CrowdStrike, Mandiant)
- Open-source feeds (AlienVault OTX, abuse.ch, Threat Fox)
- Government partnerships (MS-ISAC, FBI InfraGard)
:::
::col::
:::list heading="Intelligence Cycle Steps" style=plain
- Direction: define intelligence requirements based on organizational context
- Collection: gather data from relevant sources
- Processing: normalize, de-duplicate, and enrich raw data
- Analysis: apply analytical techniques to produce finished intelligence
- Dissemination: share with appropriate stakeholders in right format
- Feedback: assess utility and refine requirements
:::
::::

:::code language=mermaid caption="The Threat Intelligence Cycle: a continuous six-phase process that converts raw threat data into actionable security decisions, aligning threat actor analysis with real-time operational defense"
flowchart LR
  D["Direction<br/>which actors matter to us?"] --> C["Collection<br/>feeds, logs, reports"]
  C --> P["Processing<br/>normalize, deduplicate"]
  P --> A["Analysis<br/>TTPs, intent, capability"]
  A --> DS["Dissemination<br/>briefings, detection rules"]
  DS --> F["Feedback<br/>was it useful?"]
  F --> D
:::

:::notes
Threat intelligence is the discipline that bridges threat actor analysis, the theoretical framework we've built throughout this lecture, with operational security defense. Without intelligence, defenders operate reactively, responding to incidents after they occur. With quality threat intelligence, defenders can anticipate adversary behavior, pre-configure detections for relevant techniques, and make proactive decisions about control priorities before an attack begins.

The **four intelligence types** form a hierarchy from strategic to technical, serving different consumer audiences with different decision-making timescales:

**Strategic intelligence** informs multi-year security investment decisions and risk appetite discussions at the executive and board level. "The healthcare sector is experiencing a 75% increase in ransomware incidents this year" (source: Verizon DBIR, HHS HIPAA Breach Portal) is strategic intelligence that informs a hospital board's decision to allocate additional security budget or purchase cyber insurance.

**Operational intelligence** informs the security operations center's priorities this week or this month. "APT29 is currently conducting a spearphishing campaign targeting European Union diplomatic personnel using COVID-19 research themes" (source: CISA joint advisory) tells the SOC to increase phishing detection sensitivity and alert the relevant workforce immediately.

**Tactical intelligence** informs detection engineering, the creation of specific SIEM rules, EDR behavioral policies, and network signatures. "SunBurst malware uses domain-generated algorithm subdomains of avsvmcloud[.]com for C2 beacon traffic with specific HTTP header patterns" enables a Snort rule or SIEM query to detect that specific behavior.

**Technical intelligence** (Indicators of Compromise, IoCs) is the most granular form: specific IP addresses, domain names, file hashes, email subjects, YARA rules for malware identification. These feed directly into technical security controls, firewall block lists, EDR hash blocking, SIEM alerting. However, technical IoCs have the shortest useful lifespan: attackers rotate IPs, domains, and recompile malware (changing hashes) regularly. TTP-level intelligence (tactical) persists longer because adversaries cannot easily change their underlying techniques.

**ISACs (Information Sharing and Analysis Centers)** are sector-specific organizations that facilitate threat intelligence sharing among organizations in the same industry. The **FS-ISAC** (Financial Services), **H-ISAC** (Health), **E-ISAC** (Electricity), and **MS-ISAC** (Multi-State, for state and local government) aggregate threat intelligence from member organizations and government sources, enriching it through collective analysis and distributing it to members, often including IoCs, TTPs, and defensive guidance faster than any single organization could produce independently. NIST SP 800-150 provides guidance on cyber threat information sharing practices and the establishment of information sharing relationships.

The **CISA Known Exploited Vulnerabilities (KEV) Catalog** is a particularly valuable free threat intelligence resource: a curated, authoritative list of CVEs that CISA has confirmed are being actively exploited in the wild. Unlike the full CVE database (200,000+ entries), the KEV catalog (1,000+ entries as of 2024) represents the vulnerabilities that security teams should prioritize patching *first*, because they are confirmed to be under active exploitation, not merely theoretical risks. Binding Operational Directive (BOD) 22-01 mandates federal agencies patch KEV entries within 2–3 weeks of catalog publication.

Threat intelligence can overwhelm. Commercial feeds produce thousands of indicators of compromise a day, more than any team can act on. Effective programs filter them by relevance (does the actor target this sector?), confidence (do several sources confirm it?) and actionability (is there a control that can act on it?). Quality matters far more than quantity.
:::

%%%

---
unit: Summary
code: FIN
title: Bringing It All Together, Threat-Informed Defense Strategy
---
:::callout style=soft
Threat-informed defense connects everything from this lecture into a unified operational model: who is attacking you, why, what they'll do, and what you can do about it, at every level from executive strategy to SOC analyst detection rules.
:::

:::flow
Identify your organization's relevant threat actors (based on sector, size, data, and public profile)
Characterize each actor's motivation, capability, and likely initial access vectors
Map relevant ATT&CK techniques for each prioritized threat actor (use ATT&CK Navigator)
Assess current detection and mitigation coverage against those techniques (create coverage heat map)
Identify gaps, techniques used by high-priority actors with no detection coverage
Prioritize controls based on gap analysis and implement (MFA, segmentation, logging, awareness)
Validate with purple team exercises and threat hunting
Feed incident learnings back into threat actor profiles and detection rules
Repeat continuously, the threat landscape evolves; defense must too
:::

::::columns
::col::
:::list heading="Standards That Support This Model" style=plain
- NIST CSF 2.0, Govern, Identify, Detect, Respond, Recover
- NIST SP 800-53, Control selection based on threat assessment
- ISO/IEC 27001, Risk treatment based on threat likelihood and impact
- MITRE ATT&CK, Adversary behavior taxonomy for detection and simulation
- NIST SP 800-207, Zero Trust Architecture as structural defense
- CISA KEV Catalog, Priority vulnerability remediation
:::
::col::
:::list heading="Key Takeaways from This Lecture" style=plain
- Threat actors range from script kiddies to nation-states, each requires different defenses
- Motivation analysis reveals what attackers want and who they'll target
- MITRE ATT&CK provides the operational vocabulary connecting threat behavior to defensive action
- The 14-tactic lifecycle models the complete adversary journey from reconnaissance to impact
- Threat profiling applies the framework to your specific organizational context
- Zero Trust and layered defense together address the full threat actor spectrum
:::
::::

:::code language=mermaid caption="Threat-Informed Defense: the complete operational model, from threat actor characterization through ATT&CK mapping to gap analysis and control implementation, closing the loop through continuous validation and intelligence feedback"
flowchart LR
  A["Characterize threat actors<br/>(CTI reports)"] --> B["Map their TTPs<br/>(MITRE ATT&CK)"]
  B --> C["Find detection gaps<br/>(ATT&CK Navigator)"]
  C --> D["Implement controls<br/>(SP 800-53, CIS Controls)"]
  D --> E["Validate with emulation<br/>(purple team, Atomic Red Team)"]
  E --> A
:::

:::notes
The concept of **threat-informed defense** represents the synthesis of everything covered in this lecture and provides the philosophical foundation for modern, effective cybersecurity programs. It is explicitly endorsed by NIST, CISA, and the global cybersecurity community as the correct approach to security decision-making, and it stands in contrast to the compliance-driven, checkbox-completion approach that characterized much of the industry in the pre-ATT&CK era.

The core insight of threat-informed defense is that **security resources are finite and threats are not equal**. An organization that allocates equal resources to defending against every possible threat actor and technique will inevitably under-invest in the defenses that matter most and over-invest in defending against threats that are irrelevant to their specific context. A healthcare organization spending significant resources defending against ICS (Industrial Control Systems) attacks targeting manufacturing equipment, while leaving their email system without anti-phishing controls, has inverted its priorities completely. Threat-informed defense prevents this by ensuring that control selection and resource allocation flow from a systematic understanding of relevant threat actors and their specific techniques.

The **nine-step model** presented in this slide represents the operational implementation cycle:

Steps 1-2 (Identify and characterize actors) correspond to the **NIST CSF Govern (GV.RM)** and **Identify (ID.RA)** functions, building the organizational risk context. This is where the threat actor knowledge from this lecture is directly applied.

Steps 3-4 (Map ATT&CK techniques and assess coverage) are the core gap analysis activities supported by the ATT&CK Navigator tool. They correspond to NIST CSF **Detect (DE.CM)**, ensuring detection processes are calibrated to the relevant threat landscape.

Steps 5-6 (Identify gaps and implement controls) are the risk treatment phase, corresponding to NIST CSF **Protect (PR)** and aligned with ISO/IEC 27001's Plan-Do-Check-Act cycle for control implementation.

Steps 7-8 (Validate and feed back learnings) correspond to NIST CSF **Respond** and **Recover**, but also to the continuous improvement requirements of both NIST and ISO/IEC 27001. Purple team exercises, where red team operators simulate specific threat actor TTPs and blue team defenders attempt to detect and respond, are the most rigorous validation mechanism, providing direct evidence of whether implemented controls work against real adversary behaviors.

Step 9 (Repeat) reflects the dynamic nature of the threat landscape. Threat actors evolve their techniques, new vulnerabilities emerge, new APT groups are identified, and organizational environments change through mergers, acquisitions, new technologies, and new business processes. Threat-informed defense is not a project that completes, it is a continuous operational discipline.

**For students entering the cybersecurity field**, this model provides a career-long framework. Whether you work as a SOC analyst (applying TTPs to detection rules), a penetration tester (simulating specific threat actor techniques), a security architect (designing controls around the threat landscape), a risk analyst (quantifying likelihood and impact based on threat actor analysis), or a CISO (communicating risk in business terms to executives), the threat-informed defense cycle is your operating model.

The lecture has covered the full arc from "who is attacking you" (threat actor categories and motivations) through "what they do" (MITRE ATT&CK tactics and techniques) to "how to defend against them" (threat-informed control prioritization, Zero Trust architecture, and threat intelligence). These concepts are not academic abstractions, they are the daily working vocabulary of every effective security operations team in the world today.

Threat-actor knowledge translates into immediate personal protections: enabling MFA on personal accounts, auditing code repositories for committed credentials, and checking an organization's exposure on Shodan.
:::

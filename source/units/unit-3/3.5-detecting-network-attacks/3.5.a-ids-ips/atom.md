# 3.5.a, Intrusion detection and prevention systems (IDS/IPS)

> **Unit 3 · 3.5 Detecting Network Attacks**
> **AP Learning Objective(s):** 3.5.A
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Distinguish between intrusion detection systems (IDS) and intrusion prevention systems (IPS), explain how signature-based and anomaly-based detection work, and identify which alert type (true positive, false positive, true negative, false negative) a given scenario represents.

## Lesson
A firewall decides what traffic is allowed in and out. An intrusion detection or prevention system watches traffic that has already been permitted and asks a harder question: does this allowed traffic actually look like an attack? The difference matters because many attacks travel over ports and protocols that firewalls must leave open, HTTP on port 80, DNS on port 53, encrypted traffic on port 443. A system that only checks "is this port allowed?" will never catch a web-application exploit or a beaconing piece of malware calling home over HTTPS.

**IDS vs. IPS, detection vs. action.** An Intrusion Detection System (IDS) is a passive sensor. It inspects a copy of traffic (via a network tap or port mirror), compares what it sees to known attack patterns, and raises an alert. The traffic itself is not interrupted; the IDS only observes and reports. An Intrusion Prevention System (IPS) is an inline device, traffic must flow through it. When the IPS sees a match, it can drop the packet, reset the connection, or block the source IP in real time, before the payload reaches the target. IDS = watch and tell. IPS = watch and stop.

Both names appear together because most modern appliances operate in either mode, and many organizations run the same sensor as IDS on a high-value segment (to avoid false-positive outages) and as IPS on a perimeter segment (to get automatic blocking). The AP framework asks you to know the difference in principle.

**Signature-based detection.** The most common detection method works by matching traffic against a database of known attack patterns called signatures. A signature for a specific SQL injection string, a known malware file hash, or a particular shellcode sequence will fire whenever that exact pattern appears. Signature detection is fast, precise, and produces few false alarms for patterns that are already known. Its limitation is equally clear: it only catches attacks whose signatures exist in the database. A brand-new exploit, a zero-day, has no signature. Signatures must be updated constantly; a sensor running a database that is weeks old is blind to recently discovered threats.

**Anomaly-based detection.** Anomaly detection builds a behavioral baseline of what "normal" looks like on the network: typical connection rates, usual protocols per host, normal data volumes, expected working-hour activity. It then flags deviations from that baseline, regardless of whether the deviation matches any known signature. This approach can catch novel attacks, a never-before-seen worm spreading laterally will generate unusual port-scan patterns that anomaly detection can recognize even without a matching signature. The cost is a higher false-positive rate: legitimate but unusual behavior (a developer running a mass database query for the first time, a backup job kicking off at 2 AM) can trigger alerts, and analysts must tune the baseline continuously.

In the the simulation for this skill, you play the role of a junior analyst reviewing an IDS alert queue. For each alert you must classify it as a true positive (TP), false positive (FP), true negative (TN), or false negative (FN) given the traffic description and sensor verdict.

**Alert classification.** Four outcomes are possible when any detection system evaluates an event:

| | Sensor says: attack | Sensor says: benign |
|---|---|---|
| Actually is an attack | True Positive (TP) | False Negative (FN) |
| Actually is benign | False Positive (FP) | True Negative (TN) |

True positives are the goal, the sensor caught a real attack. False positives are the analyst's daily burden: a real alert that turns out to be benign traffic, wasting time and potentially desensitizing responders (alert fatigue). False negatives are the dangerous outcome: an attack passed through undetected. True negatives are the quiet wins, benign traffic correctly ignored.

An IDS/IPS that is too sensitive produces so many false positives that analysts start ignoring alerts, allowing real attacks to slip past. A system tuned too loosely produces false negatives, missed detections. This tuning tension is at the heart of real-world IDS/IPS management.

**HIDS vs. NIDS.** Sensors can live at the network level (NIDS, Network IDS) or on individual hosts (HIDS, Host IDS). A NIDS sits at a choke point and inspects traffic flowing past; it can see attacks before they reach any host but cannot inspect encrypted payloads unless it performs SSL/TLS inspection. A HIDS runs as an agent on the endpoint and watches system calls, file changes, and process creation; it sees what actually executed on the machine. Enterprise deployments typically combine both.

The coding problem in `problem/` asks you to apply a set of IDS signatures to a synthetic packet-log and return which log entries match, similar to how a real rule engine like Snort processes rules against a pcap file.

## Key terms
- **IDS (Intrusion Detection System)**, a passive sensor that copies and analyzes traffic, generating alerts without blocking.
- **IPS (Intrusion Prevention System)**, an inline sensor that can drop or block malicious traffic in real time.
- **Signature-based detection**, matching traffic against a database of known attack patterns; fast but blind to zero-days.
- **Anomaly-based detection**, flagging deviations from a learned behavioral baseline; catches novel attacks but produces more false positives.
- **True positive (TP)**, the sensor correctly identified an actual attack.
- **False positive (FP)**, the sensor flagged benign traffic as an attack (wasted analyst effort, alert fatigue).
- **False negative (FN)**, the sensor missed a real attack (most dangerous outcome).
- **NIDS / HIDS**, network-level vs. host-level placement of the sensor.

## Common misconceptions
- "IDS and IPS are the same thing." → IDS only alerts; IPS actively blocks. A misconfigured IPS with a high false-positive rate will drop legitimate traffic and cause outages.
- "Signature-based IDS catches all attacks." → Only attacks with existing signatures are caught. Zero-days and novel variants pass through undetected unless anomaly or behavioral detection is also in place.
- "More alerts = better security." → Alert fatigue from excessive false positives degrades security by causing analysts to stop investigating alerts. Tuning and prioritization matter as much as detection capability.

## Try it
- **Simulation:** Classify 6 IDS alert scenarios as TP, FP, FN, or TN, score at least 5 of 6 correctly to meet the objective.
- **Coding problem:** Apply a set of IDS signatures (keyword/port rules) to a synthetic traffic log and return the list of matching log-entry IDs.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (IDS/IPS concepts and rule engines), rebuilt as original prose above; see `vendor/web/opensecuritytraining/` notes.
- Reference: NIST SP 800-94 "Guide to Intrusion Detection and Prevention Systems", key definitions rebuilt from primary text.
- Practice: Cybrary IDS/IPS micro-challenges, rebuilt locally as the simulation alert-classification exercise.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.

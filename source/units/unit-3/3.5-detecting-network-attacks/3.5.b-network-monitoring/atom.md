# 3.5.b, Network monitoring and traffic analysis

> **Unit 3 · 3.5 Detecting Network Attacks**
> **AP Learning Objective(s):** 3.5.B
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Explain how baseline traffic profiles support anomaly detection,
read basic flow-record and packet-capture data, and identify network-monitoring indicators of
compromise such as beaconing, unusual port usage, and abnormal data-volume spikes.

## Lesson
An IDS signature engine (3.5.a) catches attacks it already knows about. Network monitoring is the
broader discipline of continuously watching traffic itself, volumes, ports, destinations, timing, so that an analyst can notice when something looks wrong even without a matching signature. It
is the practice of knowing what "normal" looks like well enough to recognize "not normal."

**Two views of traffic: full capture and flow records.** The most detailed view is a packet
capture (pcap), every byte of every packet, gathered by a sniffer such as a network tap or a tool
like tcpdump. Full capture is precise but expensive to store and slow to search at scale. The more
common operational view is a flow record (commonly called NetFlow, after Cisco's original
implementation). A flow record summarizes a conversation between two endpoints, source IP,
destination IP, source port, destination port, protocol, byte count, packet count, and duration, without keeping the payload. Flow data is far cheaper to store and query, which is why most
enterprise monitoring pipelines run on flow records and reserve full packet capture for a smaller
set of high-value segments or triggered deep-dive investigations.

**Baselining.** Before you can call something abnormal, you need to know what normal looks like.
Baselining is the process of recording typical traffic patterns over time: which hosts talk to
which other hosts, on which ports, at what volume, and during what hours. A file server at
Meridian High School might normally see 200-400 MB of outbound traffic per school day, almost
entirely on port 445 (SMB) to on-campus clients, concentrated between 7 AM and 4 PM. That profile
is the baseline. Anomaly-based monitoring, the same underlying idea introduced in 3.5.a for IDS, compares current traffic against this baseline and flags deviations.

**Common monitoring indicators.** Several traffic patterns recur across real incidents:
- **Unusual port usage.** A host suddenly making outbound connections on a port it has never used
  (e.g., a printer talking on TCP 4444) is worth investigating regardless of whether any signature
  matches, the port itself is the anomaly.
- **Beaconing.** Malware that "phones home" to a command-and-control server often does so at
  regular, machine-precise intervals (every 60 seconds, every 5 minutes) rather than the irregular
  bursts typical of human-driven traffic. A host contacting the same external IP at suspiciously
  regular intervals, even in small amounts, is a classic beaconing signature that traffic analysis, not payload inspection, is well suited to catch.
- **Data-volume spikes (possible exfiltration).** A host that normally uploads a few megabytes a
  day suddenly uploading several gigabytes to an external destination, especially outside business
  hours, is a strong indicator of data exfiltration in progress. Volume-based detection does not
  need to know what the data *is*, the volume and direction alone are the signal.
- **Off-baseline timing.** Traffic that is otherwise unremarkable but occurs at a time no legitimate
  process runs (e.g., large database queries at 3 AM from a workstation account) raises suspicion
  even when every individual packet looks benign.

**Tools, conceptually.** A packet sniffer (e.g., Wireshark, tcpdump) captures and displays raw
packets for deep inspection. A flow collector aggregates NetFlow/IPFIX-style records for
volume-and-pattern analysis at scale. A SIEM (Security Information and Event Management platform)
ingests logs and flow data from many sources, correlates them, and gives analysts a single place to
query "show me all hosts that exceeded 1 GB outbound today." The AP framework does not require
operating a specific product, it requires understanding what each layer of tooling is for and
what kind of anomaly each is positioned to catch.

**Why this complements the firewall and the IDS.** A firewall enforces which conversations are
allowed to start. An IDS matches traffic against known bad patterns. Network monitoring catches
what neither can: attacks that use entirely permitted ports and protocols, and that have no
matching signature, but whose volume, timing, or destination pattern deviates from what the network
normally does. This is why mature security operations run all three together rather than relying on
any single layer.

**Simulation.** The simulation gives you a baseline table of normal per-host traffic
and a window of observed traffic; you decide which hosts show a genuine anomaly (unusual port,
volume spike, or beaconing pattern) versus which are within normal variation.

**Coding problem.** The `problem/` directory implements a simplified traffic-anomaly detector:
given a baseline of normal per-host volume and allowed ports, and a window of observed flow
records, flag every host that exceeds its baseline volume threshold or uses a port outside its
baseline set.

## Key terms
- **Packet capture (pcap)**, full-fidelity recording of every packet, including payload; precise
  but storage- and search-expensive at scale.
- **Flow record (NetFlow)**, a summarized record of a single conversation (endpoints, ports,
  protocol, byte/packet counts, duration) without payload; the common basis for large-scale
  monitoring.
- **Baseline**, the recorded profile of "normal" traffic (volume, ports, timing, destinations)
  that current traffic is compared against.
- **Beaconing**, regular, machine-timed outbound connections characteristic of malware
  command-and-control check-ins.
- **Data exfiltration (volume-based indicator)**, an abnormal spike in outbound data volume,
  often the clearest sign that data is actively leaving the network.
- **SIEM (Security Information and Event Management)**, a platform that aggregates and correlates
  logs and flow data from many sources for centralized analyst query and alerting.

## Common misconceptions
- "You need full packet capture to detect an attack." → Most anomalies (volume spikes, beaconing,
  unusual ports) are visible in flow records alone, without ever inspecting payload content.
- "A baseline is set once and never changes." → Legitimate traffic patterns shift (new
  applications, seasonal usage, staff changes); baselines must be re-established periodically or
  monitoring drifts into constant false positives.
- "Any traffic on an unusual port is malicious." → Unusual-port traffic is a prompt for
  investigation, not automatic proof of compromise, new legitimate software can also introduce new
  ports. Volume, destination, and timing context matter together.

## Try it
- **Simulation:** Given a baseline and an observed traffic
  window, correctly flag every host showing a genuine anomaly and clear every host within normal
  variation.
- **Coding problem:** Implement a traffic-anomaly detector: given a per-host baseline
  (volume threshold, allowed ports) and observed flow records, return the hosts that exceed the
  volume threshold or use a port outside the baseline.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (network traffic analysis fundamentals), rebuilt as original prose
  above; see `vendor/web/opensecuritytraining/` notes.
- Reference: NIST SP 800-94 (Guide to Intrusion Detection and Prevention Systems) and NIST SP
  800-61 network-monitoring guidance, key concepts rebuilt from primary text.
- Practice: Cybrary traffic-analysis micro-challenges, rebuilt locally as the simulation baseline
  exercise.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.

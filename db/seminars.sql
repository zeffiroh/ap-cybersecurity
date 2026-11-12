insert into seminars (id, sort, title, summary, description, level, minutes, tickets, topics, domains, published) values
(1, 1, 'Evidence, notes and handoffs',
 'Write the three things every security job runs on: a triage note, an escalation and a shift handover.',
$d$Most security work is passed from one person to the next. In this free seminar you rewrite a poor ticket into a triage note someone else can act on, write an escalation that says what you know, what you do not know and what you need, and hand over a shift so nothing is lost overnight.

Hands-on: the report builder and the alert queue's handover, on a real case from the course.

Hand-in: a triage note, an escalation and a shift handover.$d$,
 'Foundation', 120, 0, 'Triage notes · Escalation · Shift handover · Writing for the next analyst',
 '["Security Operations", "Incident Response"]', false),
(2, 2, 'Reading evidence: packets, Linux, Windows and network sensors',
 'Read the four kinds of evidence every analyst meets and turn each into a short finding.',
$d$Packets: DNS, HTTP and TLS, display filters, follow-stream and "who talked to whom". Linux: auth logs, processes and permissions from the command line, separating noise from compromise. Windows: logons, process creation and PowerShell logs. Network sensors: Zeek logs and IDS rules run past a capture.

Hands-on: the packet viewer and a tshark simulator, the browser Linux, event logs, IDS rules and captured Zeek output.

Hand-in: a host triage note and a one-page network finding, with the commands and filters you used.$d$,
 'Foundation', 360, 12, 'Packets · tshark · Linux logs · Windows event logs · Sysmon · Zeek · IDS rules',
 '["Security Operations", "Incident Response", "Network Security"]', false),
(3, 3, 'Log search and detection as code',
 'Hunt in SPL and KQL, then turn the hunt into a tested, tuned Sigma rule.',
$d$Run the same hunt in two search languages side by side: filters, stats, time charts and pivots. Then write a Sigma rule, test it for hits and false positives, tune it, and convert it to a SIEM query.

Hands-on: an SPL and KQL simulator (a teaching subset of each language, over real-format logs), SQL over logs, the Sigma tool with real pySigma conversion, and the log parser.

Hand-in: a saved hunt pack in SPL and KQL, and a Sigma rule pack with tests and tuning notes.$d$,
 'Practitioner', 300, 10, 'SPL · KQL · SQL · Sigma · pySigma · Detection testing · Tuning',
 '["Security Operations", "Detection Engineering"]', false),
(4, 4, 'SOC triage: alerts, phishing, threat intel and AI verdicts',
 'Work a real alert queue: close, escalate or "cannot determine", and back every call with evidence.',
$d$Work a queue of alerts on messy evidence. Triage reported emails from headers to URLs to the lure, write and tune a YARA rule on harmless samples, enrich indicators and map them to ATT&CK, and check an AI assistant's verdicts, including one alert carrying injected text.

Hands-on: the alert queue, email triage, real YARA-X, CyberChef, indicators and the ATT&CK heatmap, and a scripted AI assistant.

Hand-in: ten dispositions with one escalation, a phishing report with a tested YARA rule, an intel note, and an AI-verdict review log.$d$,
 'Practitioner', 360, 12, 'Alert triage · Phishing · YARA-X · Threat intel · ATT&CK · Reviewing AI output',
 '["Security Operations", "Threat Intelligence"]', false),
(5, 5, 'Capstone A: the night shift',
 'Run a night shift alone: an unlabelled, noisy queue, and a report for the morning team.',
$d$You are the only analyst on shift. The queue is unlabelled, the data is noisy, some alerts are false leads, and "benign" is a valid answer. Hints are available but cost points.

Hands-on: the whole SOC kit from seminars 2 and 3.

Hand-in: a shift report, one escalation and one new detection.$d$,
 'Advanced', 270, 9, 'Capstone · Alert queue · Escalation · Detection · Shift report',
 '["Security Operations"]', false),
(6, 6, 'Incident response: ransomware, lateral movement and memory',
 'Take a ransomware incident from first alert to executive summary.',
$d$Triage, scope, contain and decide under pressure. Reconstruct lateral movement from Windows timelines, read saved memory-forensics output, and keep a chain of custody for every file you touch.

Hands-on: the merged timeline, process tree, hex, strings and hashes with chain of custody, a tabletop exercise, and captured Velociraptor, Hayabusa and Volatility output.

Hand-in: an executive summary, a technical annex and a lateral-movement timeline mapped to ATT&CK.$d$,
 'Practitioner', 360, 12, 'Ransomware · Scoping · Containment · Timelines · Lateral movement · Memory forensics',
 '["Incident Response", "Digital Forensics"]', false),
(7, 7, 'Breach clocks: CERT-In 6 hours, DPDP, RBI and GDPR',
 'File a CERT-In report within six hours with partial facts, then build the full notification pack.',
$d$Start the clock, choose the CERT-In category, and file with what you know to a simulated inbox while injects arrive. Then work out which other clocks apply (DPDP, RBI, GDPR and others), decide the order, and write the DPDP notification pack: the Board note, the plain-language notice to people affected, and the 72-hour report.

Hands-on: a CERT-In filing form and simulated inbox, a tabletop with injects, and a notification-clock matrix.

Hand-in: a filed CERT-In report and update, a DPDP notification pack, and a one-page notification order.$d$,
 'Practitioner', 300, 10, 'CERT-In · DPDP Act · RBI · GDPR · Breach notification · Tabletop',
 '["Incident Response", "Governance, Risk and Compliance"]', false),
(8, 8, 'Identity from both sides: AD, Entra and cloud IAM',
 'Find the path from an ordinary account to admin, then cut it and detect anyone who tries.',
$d$Trace group memberships and permissions to an admin path, read the protocol traces an attacker leaves, cut access to least privilege, harden sign-in and MFA, and write the detection.

Hands-on: the identity and access tool (review and attack paths), the cloud IAM simulator, and captured Kerberos and NTLM traces.

Hand-in: an attack path, a policy diff, a detection and the fix.$d$,
 'Practitioner', 300, 10, 'Active Directory · Entra ID · Cloud IAM · Attack paths · Least privilege · MFA',
 '["Identity and Access Management", "Cloud Security"]', false),
(9, 9, 'Cloud and DevSecOps: posture, pipelines, secrets and automation',
 'Investigate a cloud account, fix what matters first, and gate the pipeline so it does not come back.',
$d$Investigate cloud audit logs, rank posture findings, find secrets in code, review infrastructure-as-code and Kubernetes manifests, build an SBOM, check log coverage and retention, and automate the boring parts with Python and a SOAR playbook.

Hands-on: the code and config scanner, the cloud IAM replay, the SOAR playbook, the Python notebook, and captured Trivy, Checkov and Prowler output.

Hand-in: a ranked findings register, a pipeline gate policy and a tested Python script.$d$,
 'Practitioner', 360, 12, 'Cloud audit logs · Posture · Secrets · Terraform · Kubernetes · SBOM · Python · SOAR',
 '["Cloud Security", "Security Engineering"]', false),
(10, 10, 'Authorised testing: web, APIs and findings that get fixed',
 'Test our own shop with permission, from scope to report, and write findings a developer will actually fix.',
$d$Agree the rules of engagement, scan and map, then test server-side (SQL injection, access control, authentication) and client-side and APIs (XSS, CSRF, JWT). Score each finding, map it to CWE, plan the retest and brief the board. Every attack is watched from the defender's side too.

Hands-on: Hack the shop, the SQL injection lab, an intercept proxy simulator, the JWT inspector, the CSRF mission, an nmap simulator, and CVSS and patch priority.

Hand-in: a scope document, three findings with reproduction and fix, and a board note.$d$,
 'Practitioner', 360, 12, 'Rules of engagement · Web testing · SQL injection · XSS · CSRF · JWT · CVSS · Reporting',
 '["Security Testing", "Application Security"]', false),
(11, 11, 'Design, risk and audit',
 'Threat-model a system, run the risk register, and pass an audit with evidence.',
$d$Threat-model a system with STRIDE and an attack tree and write the design review. Assess, score and treat risks and justify control choices in a Statement of Applicability. Sample audit evidence for ISO 27001 and SOC 2 and write an exception. Score a vendor and mark up a data processing agreement.

Hands-on: the threat model, the risk register, the compliance gap check (ISO 27001, SOC 2, PCI DSS, DPDP Act, CERT-In) and the report builder.

Hand-in: a design review memo, a risk register with Statement of Applicability, an audit exception and a vendor file.$d$,
 'Practitioner', 360, 12, 'Threat modelling · Risk register · ISO 27001 · SOC 2 · Audit evidence · Vendor risk',
 '["Governance, Risk and Compliance", "Security Architecture"]', false),
(12, 12, 'AI security: attacking and governing LLM apps',
 'Break a support bot, a document search and an agent, then write the policy that stops it happening again.',
$d$Try prompt injection and prompt leaks on a support bot, poison a small document search (RAG), and stop an agent from acting without approval. Then write an AI policy and an AI risk register mapped to MITRE ATLAS.

Hands-on: the AI security simulator (scripted assistant, toy RAG and an agent with an approval gate) and ATLAS data.

Hand-in: an LLM test report with fixes, an AI policy and an AI risk register.$d$,
 'Advanced', 270, 9, 'Prompt injection · RAG poisoning · Agents · MITRE ATLAS · AI policy · AI risk',
 '["AI Security", "Governance, Risk and Compliance"]', false),
(13, 13, 'Capstone B: a breach across teams',
 'One breach, cloud, Windows and network evidence, no hints: investigate, report and notify.',
$d$A breach that crosses every team. Work cloud, Windows and network evidence with no topic hints, reach a conclusion you can defend, brief executives, and file what the regulators need.

Hands-on: everything from the other seminars.

Hand-in: an executive briefing, a technical report, a notification pack and a new detection.$d$,
 'Advanced', 480, 16, 'Capstone · Investigation · Reporting · Notification · Detection',
 '["Incident Response", "Security Operations", "Governance, Risk and Compliance"]', false)
on conflict (id) do nothing;

select setval(pg_get_serial_sequence('seminars', 'id'), greatest((select max(id) from seminars), 1));

do $$
declare
  clash text;
begin
  select string_agg(id || ' (' || title || ')', ', ' order by id) into clash from seminars
   where id between 1 and 13 and title not in ('Evidence, notes and handoffs', 'Reading evidence: packets, Linux, Windows and network sensors',
     'Log search and detection as code', 'SOC triage: alerts, phishing, threat intel and AI verdicts', 'Capstone A: the night shift',
     'Incident response: ransomware, lateral movement and memory', 'Breach clocks: CERT-In 6 hours, DPDP, RBI and GDPR',
     'Identity from both sides: AD, Entra and cloud IAM', 'Cloud and DevSecOps: posture, pipelines, secrets and automation',
     'Authorised testing: web, APIs and findings that get fixed', 'Design, risk and audit', 'AI security: attacking and governing LLM apps',
     'Capstone B: a breach across teams');
  if clash is not null then
    raise warning 'These seminar IDs were already used, so the new seminar was not added there: %. The labs expect IDs 1 to 13.', clash;
  end if;
end $$;

from kit import REPLAY, after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

PATHS = '''import csv
import sys

start, goal = sys.argv[1], sys.argv[2]
edges = []
for r in csv.DictReader(open("identity/ad_edges.csv")):
    if r["relation"] == "HasSessionOn":
        edges.append((r["target"], "takes saved password of", r["source"]))
    else:
        edges.append((r["source"], r["relation"], r["target"]))


def walk(node, path):
    if node == goal:
        yield path
        return
    for a, rel, b in edges:
        if a == node and b not in [p[2] for p in path] and b != start:
            yield from walk(b, path + [(a, rel, b)])


best = min(walk(start, []), key=len)
for a, rel, b in best:
    print(f"{a:12} --{rel}-->  {b}")
on = {(a, b) for a, _, b in best}
with open("graph.dot", "w") as f:
    f.write("digraph AD {\\n rankdir=LR; node [shape=box, style=rounded, fontname=\\"DejaVu Sans\\", fontsize=16];\\n")
    for a, rel, b in edges:
        hot = (a, b) in on
        f.write(f' "{a}" -> "{b}" [label="{rel}", fontsize=12, color="{"red" if hot else "gray60"}", penwidth={3 if hot else 1}];\\n')
    f.write("}\\n")
'''


KERB_RULE = """title: Kerberos service ticket with RC4 for a user account (possible kerberoasting)
id: 3b7a2f10-6c1d-4e2a-8f00-7e1d00000001
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4769
    TicketEncryptionType: '0x17'
  filter_computers:
    ServiceName|endswith: '$'
  condition: selection and not filter_computers
falsepositives:
  - Old applications that only speak RC4 (list them and fix them)
level: high
tags:
  - attack.credential-access
  - attack.t1558.003
"""

DCSYNC_RULE = """title: Directory replication by an account that is not a domain controller (DCSync)
id: 3b7a2f10-6c1d-4e2a-8f00-7e1d00000002
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4662
    Properties|contains:
      - '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2'
      - '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'
  filter_dcs:
    SubjectUserName|endswith: '$'
  condition: selection and not filter_dcs
falsepositives:
  - Azure AD Connect or similar sync accounts (exclude by name)
level: critical
tags:
  - attack.credential-access
  - attack.t1003.006
"""

FIX = """FIX, HOP BY HOP   Nimbus Analytics   10 Nov 2026 (UTC)
CONTAIN NOW
  1. Disable the cloud user ops-backup and delete its key; revoke key NKIA1141977357.
  2. Reset h.verma, svc-sql and adm.k.nair; remove the remote control tool from hd-pc04.
REBUILD TRUST (after a DCSync, assume every domain password is known)
  3. Reset krbtgt twice, 10 hours apart; reset every privileged and service account.
ROOT CAUSES, one per link
  phished password            -> MFA for every account, starting with helpdesk
  Helpdesk can reset svc-sql  -> remove the inherited ForceChangePassword on OU=Service Accounts
  RC4 tickets, weak password  -> AES only; 25+ character service passwords or gMSA
  admin task with saved pwd   -> run Nightly KPI export as a gMSA, not adm.k.nair
  key in a script, Allow *    -> PutObject on nimbus-reports only (replay: 0 and 0)
DETECTIONS: kerberoast-rc4.yml, dcsync.yml (tested on dc01: 6 and 2 hits, 0 on normal)
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Identity from both sides. Almost every serious breach goes through an account: a password, a group, a saved login, a cloud key. Nimbus Analytics, a data firm in Hyderabad, has a Windows domain for its office and a cloud account for client data. On Monday the ninth of November, Harsh Verma, a helpdesk analyst, typed his password into a phishing page."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("On Tuesday someone used it from the helpdesk PC. In about three hours they had every password in the domain, four files of client data from the cloud, and a cloud user of their own. We look at Nimbus twice: as the auditor, reviewing who has what, and as the attacker, walking the same directory. Real tools only: the terminal, Python, Graphviz, Zeek's Kerberos log, Sigma and Zircolite."),
 close("files"),
 term,

 chapter("1. Who's who"),
 say("Step one: who's who. An attacker who gets into a network doesn't start with exploits. They start by reading the directory. So we read it first. users.csv is every account."),
 cmd("column -t -s, identity/users.csv | cut -c1-170", 4),
 after("Twelve accounts. Notice the pairs and the leftovers: Kavya Nair has a normal account and an admin account. Pooja Das left in September and is disabled. Tanvi Mehta is a contractor leaving at the end of December. Who has no MFA?"),
 cmd("awk -F, '$7==\"no\" {print $1, \"-\", $4}' identity/users.csv", 2.5),
 after("And ad_edges.csv is the relationship graph: each line is one thing one account or group can do to another."),
 cmd("column -t -s, identity/ad_edges.csv | cut -c1-150", 4),
 clear,

 chapter("2. Review access like an auditor"),
 say("Step two: review access like an auditor. Three questions for every account. Does this person still need it? Does it have more than it needs? Is it protected well enough for what it can do? The edges answer the second one. Look at line two: Helpdesk can force a password change on svc-sql, inherited since 2023. And adm.k.nair has a session on app02, because a scheduled task runs as her, with a saved password. On the course site the access review tab flags these; here the decisions go in our notes: reduce Helpdesk, replace the task's account, and confirm the contractor's end date."),
 clear,

 chapter("3. Walk it like an attacker"),
 say("Step three: walk it like an attacker. Defenders think in lists. Attackers think in graphs: from where I am, what can I reach? This short Python script follows the edges from h.verma, the phished account, to Domain-Admins, and writes the whole graph for Graphviz to draw."),
 edit("paths.py", "code", (200, 60, 1500, 950)),
 wait(4),
 after("A saved password on a machine you control counts as an edge, because an administrator can take it from memory or the registry."),
 close("code"),
 cmd("python3 paths.py h.verma Domain-Admins", 3),
 cmd("dot -Tpng graph.dot -o graph.png && echo drawn", 3),
 {"open": ["firefox-esr", "--new-window", "file:///case/graph.png"], "window": "graph.png", "as": "img", "geometry": [60, 50, 1800, 960], "timeout": 60, "settle": 2},
 wait(4),
 after("The red path: h.verma is in Helpdesk, Helpdesk can reset svc-sql's password, svc-sql is a Server-Admin, Server-Admins are admins on app02, adm.k.nair's password is saved on app02, and adm.k.nair is a Domain Admin. Five hops, and no exploit anywhere. Every arrow is a setting someone chose."),
 close("img"),
 clear,

 chapter("4. The kerberoast in the logs"),
 say("Step four: the twist. The attacker didn't need the password reset at all. In Kerberos, any domain user can ask for a service ticket for any account that has a service name. Part of that ticket is encrypted with a key made from the service account's password. If it uses the old RC4 cipher, the attacker can guess passwords against it offline, and the domain never sees a failed login. That's kerberoasting. Zeek's Kerberos log, by cipher:"),
 cmd("grep -v '^#' captured/zeek-kerberos.log | awk -F'\\t' '{print $8}' | sort | uniq -c", 2.5),
 cmd("grep rc4 captured/zeek-kerberos.log | awk -F'\\t' '{print $2, $5, $6}'", 3),
 after("Twenty-seven normal AES tickets, and six RC4 tickets, all asked for by h.verma from 10.60.2.31, the helpdesk PC, for six service accounts in a row. The domain controller saw the same thing as event 4769 with encryption type 0x17."),
 cmd("jq -r 'select(.EventID==4769 and .Data.TicketEncryptionType==\"0x17\") | [.TimeCreated[11:19], .Data.TargetUserName, .Data.ServiceName] | @tsv' eventlogs/dc01-Security.jsonl", 3),
 clear,

 chapter("5. From a service account to the domain"),
 say("Step five: at 10:05, svc-sql starts doing things on app02. dc01's log has no 4724, the event for a password reset, so the likelier answer is the cracked ticket: svc-sql's password was weak enough to guess."),
 cmd("jq -r '[.TimeCreated[11:19], .EventID, .Data.TargetUserName // .Data.SubjectUserName, .Data.IpAddress // \"\", .Data.CommandLine // \"\"] | @tsv' eventlogs/app02-Security.jsonl", 3.5),
 after("A network logon as svc-sql from the helpdesk PC, special privileges, then reg save of the SECURITY and SYSTEM hives: together they hold the saved passwords of scheduled tasks, including adm.k.nair's. Then findstr searches every PowerShell script for AccessKey. Now the domain controller, event 4662 with the replication rights."),
 cmd("jq -r 'select(.EventID==4662 or (.EventID==4624 and .Data.TargetUserName==\"adm.k.nair\")) | [.TimeCreated[11:19], .EventID, .Data.SubjectUserName // .Data.TargetUserName, .Data.IpAddress // \"\", .Data.Properties // \"\"] | @tsv' eventlogs/dc01-Security.jsonl", 3.5),
 after("Every two hours DC02, the other domain controller, replicates: that's normal, and its name ends in a dollar sign because it's a computer. At 11:41, adm.k.nair, a person, logged on from app02 and asked for the same replication rights. That's DCSync: pretending to be a domain controller to copy every password hash in the domain."),
 clear,

 chapter("6. The cloud side, one key in a script"),
 say("Step six: the cloud side. The findstr found what it was looking for."),
 cmd("cat captured/app02-sync-ps1.txt", 2.5),
 after("An access key written straight into the script, so the nightly job can upload the KPI file. Now the cloud audit trail: every call, who made it, from where, and whether it worked."),
 cmd("jq -r '.[] | [.time[5:16], .identity, .action, .resource // \"\", .result, .source_ip] | @tsv' cloud/audit.json | column -t -s $'\\t'", 4),
 after("From the office address, 203.0.113.60, reporting-sync does what it always does: PutObject, one KPI file a night. From 198.51.100.200, the same key asks who am I, lists every bucket, downloads four client files, then creates a user called ops-backup, gives it a policy and a key. ops-backup tries to stop the audit log and is denied by an organisation guardrail. That guardrail is why we can still read this."),
 clear,

 chapter("7. Least privilege, the policy diff"),
 say("Step seven: least privilege. The audit trail tells us exactly what reporting-sync needs: PutObject into nimbus-reports. It had Allow star on star. This script replays every logged call against a set of policies and gives two numbers: attacker actions still allowed, and normal actions broken."),
 cmd("python3 replay.py cloud/policies.json 198.51.100.200", 3),
 say("Now we write the reduced policy with jq, changing only reporting-sync, and replay again."),
 cmd("jq '(.identities[] | select(.name==\"reporting-sync\") | .policies) = [{\"name\":\"kpi-upload\",\"statements\":[{\"effect\":\"Allow\",\"actions\":[\"PutObject\"],\"resources\":[\"bucket/nimbus-reports/*\"]}]}]' cloud/policies.json > policies-new.json && python3 replay.py policies-new.json 198.51.100.200", 3.5),
 after("Zero and zero. The attacker's calls would all have failed, and the nightly upload still works. A policy that stops the attacker but breaks the upload isn't a fix, it's an outage."),
 clear,

 chapter("8. Detections for next time"),
 say("Step eight: detections for next time. Two Sigma rules. The first: a service ticket with RC4 for an account that isn't a computer."),
 cmd("sed -n '6,16p' rules/kerberoast-rc4.yml", 2.5),
 cmd("zircolite -e eventlogs/dc01-Security.jsonl -r rules/kerberoast-rc4.yml 2>&1 | grep -E 'Matched|Detections'", 6),
 after("Six, the six roasted accounts, and none of the twenty-seven normal tickets. The second: replication rights asked for by anything that isn't a computer account."),
 cmd("sed -n '6,17p' rules/dcsync.yml", 2.5),
 cmd("zircolite -e eventlogs/dc01-Security.jsonl -r rules/dcsync.yml 2>&1 | grep -E 'Matched|Detections'", 6),
 after("Two hits, both adm.k.nair at 11:41, and DC02's regular replication stays quiet. A rule isn't finished when it matches the attack. It's finished when it also stays quiet on a normal day."),
 clear,

 chapter("9. The fix, hop by hop"),
 say("Step nine: the fix, in the order that matters. Containment first, so the attacker can't use what they have. Then rebuild trust in the domain, because after a DCSync you assume they have every password. Then the root causes, one for each link in the chain."),
 edit("fix.txt"),
 write(FIX, cps=44),
 save_note(),
 close("note"),
 clear,

 chapter("10. Hand in"),
 say("Step ten: hand in. The course notebook carries the review decisions, the attack path, the log findings, the policy replay at zero and zero, both rules, and the report."),
 cmd("ls -l *.txt *.png *.json rules/", 2),
 chapter("Wrap-up"),
 say("That's identity from both sides. As the auditor you found an inherited reset right, a saved admin password and a key with Allow star. As the attacker you walked them: a phished helpdesk password, six roasted tickets, a service account, the saved password, DCSync, and a cloud key in a script. Every link was a setting someone chose, and every link has a fix. Next, in Cloud and DevSecOps, we find those keys before they ship. Thank you for watching."),
 wait(2),
]

build("s07-identity", scenes, host="nimbus-soc",
      files={"paths.py": PATHS, "replay.py": REPLAY, "rules/kerberoast-rc4.yml": KERB_RULE, "rules/dcsync.yml": DCSYNC_RULE},
      setup=["echo \"alias zircolite='python3 /opt/zircolite/zircolite.py -j --no-event-filter --flatten-backend python -l /tmp/zircolite.log -o /tmp/detected.json'\" >> ~/.bashrc"])

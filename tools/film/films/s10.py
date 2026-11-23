from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

TM = '''from pytm import TM, Actor, Boundary, Dataflow, Datastore, ExternalEntity, Process

tm = TM("Banyan Parent Pay")
tm.description = "Parents pay school fees in the app and get an SMS receipt. Design v0.9, 13 Nov 2026."
tm.isOrdered = True

internet = Boundary("Internet")
cloud = Boundary("Banyan cloud")
partners = Boundary("Partners")

parent = Actor("Parent (app)")
parent.inBoundary = internet
staff = Actor("Office staff")
staff.inBoundary = internet
paygate = ExternalEntity("PayGate")
paygate.inBoundary = partners
sms = ExternalEntity("TextBridge SMS")
sms.inBoundary = partners

api = Process("Fees API")
api.inBoundary = cloud
api.validatesInput = False
api.authenticatesSource = False
admin = Process("Admin console")
admin.inBoundary = cloud
db = Datastore("Student records DB")
db.inBoundary = cloud
db.isEncrypted = False

Dataflow(parent, api, "fees, start payment (amount from the app)").protocol = "HTTPS"
Dataflow(api, paygate, "redirect with order and amount").protocol = "HTTPS"
hook = Dataflow(paygate, api, "webhook /fees/paid (unsigned)")
hook.protocol = "HTTPS"
Dataflow(api, db, "read fees, mark paid")
Dataflow(api, sms, "mobile number and receipt").protocol = "HTTPS"
Dataflow(staff, admin, "mark paid, refund").protocol = "HTTPS"
Dataflow(admin, db, "updates and refunds")

if __name__ == "__main__":
    tm.process()
'''

TREE = '''import re
import sys

cut = [c.lower() for c in sys.argv[1:]]
lines = [l.rstrip() for l in open("threat-model/attack-tree.txt") if l.strip()]


def parse(i, depth):
    text = lines[i].strip()
    kind, _, name = text.partition(" ") if text.split()[0] in ("OR", "AND") else ("LEAF", "", text)
    node = {"kind": kind, "name": name if kind != "LEAF" else re.sub(r"\\s+cost=\\d+", "", text), "kids": []}
    m = re.search(r"cost=(\\d+)", text)
    node["cost"] = int(m.group(1)) if m else None
    j = i + 1
    while j < len(lines) and (len(lines[j]) - len(lines[j].lstrip())) > depth:
        kid, j = parse(j, len(lines[j]) - len(lines[j].lstrip()))
        node["kids"].append(kid)
    return node, j


def cost(n):
    if n["kind"] == "LEAF":
        return 999 if any(c in n["name"].lower() for c in cut) else n["cost"]
    costs = [cost(k) for k in n["kids"]]
    return min(costs) if n["kind"] == "OR" else min(999, sum(costs))


def show(n, depth=0):
    c = cost(n)
    print("  " * depth + f"{n['kind']:4} {n['name'][:52]:52} cost {'cut' if c >= 999 else c}")
    for k in n["kids"]:
        show(k, depth + 1)


root, _ = parse(0, 0)
show(root)
best = min(root["kids"], key=cost)
print("\\ncheapest way in:", best["name"], "(cost", cost(best), ")")
'''

CHECK = """.mode box
SELECT asset, left(threat, 34) AS threat, likelihood * impact AS score, coalesce(treatment, '-') AS treatment,
  concat_ws('; ',
    CASE WHEN treatment IS NULL THEN 'no treatment' END,
    CASE WHEN owner IS NULL THEN 'no owner' END,
    CASE WHEN due IS NULL THEN 'no due date' END,
    CASE WHEN treatment = 'mitigate' AND control IS NULL THEN 'mitigate with no control' END,
    CASE WHEN treatment = 'accept' AND likelihood * impact >= 15 THEN 'high risk accepted without sign-off' END) AS problems
FROM 'risk-register-banyan.csv' ORDER BY score DESC;
"""

MEMO = """DESIGN REVIEW MEMO  Parent Pay v0.9   to Kunal Desai (Product), Sana Pillai (Engineering)
Verdict: GO for 4 December only if the three conditions below are met.

CONDITIONS FOR GO-LIVE
  1. Sign and verify the PayGate webhook (HMAC + order ID + amount); confirm with PayGate's
     status API before marking paid. Today anyone can send /fees/paid. Cheapest attack, cost 1.
  2. The server looks up the fee amount; the app never sends it. (Attack cost 2.)
  3. MFA for office staff, and a second person approves refunds over Rs 5,000.
FIX WITHIN 30 DAYS
  4. Stop logging full request bodies; keep 30 days, mask mobile numbers.
  5. Remove the child's name and class from SMS receipts (vendor gets less).
GOOD
  Payments go through PayGate, so Banyan never sees card numbers.
"""

EXCEPTION = """EXCEPTION to ISO 27001 A.8.8 for IA-2026-07     Expires 15 Jan 2027
Not met: VM-311, VM-318, VM-322 open past the 15-day target (41, 38, 33 days).
Why: the framework upgrade breaks the refund screen; the VPN patch needs downtime.
Risk meanwhile: remote code execution on the reporting server; admin console takeover.
Compensating controls (each checkable):
  VM-318 reporting server reachable only from the office VPN range; WAF rule for the exploit path.
  VM-311 admin console behind SSO with MFA; refunds need a second approver.
  VM-322 VPN admin interface closed to the internet; daily check of VPN logins.
Owners: VM-311/318 Sana Pillai; VM-322 IT lead. Patch dates: VM-322 window 28 Nov; others by 10 Jan.
Approved: CISO ______  Risk owner ______   Review at expiry, not renewed automatically.
"""

VENDOR = """VENDOR REVIEW  TextBridge Messaging (SMS receipts)        Decision: APPROVE WITH CONDITIONS
Before signing:
  1. Current ISO 27001 certificate (the June 2026 one has expired), or approval stops.
  2. Name every sub-processor; no "others as needed". Notice before adding one.
  3. Incident notice within 24 hours of discovery, not 7 working days after confirmation:
     our own CERT-In and DPDP clocks are shorter than theirs.
  4. MFA for all staff who can see message logs; logs kept 90 days, not 2 years.
  5. Backups in Singapore: confirm the transfer is allowed and in the contract.
On our side: send only the receipt number and amount; no child name or class.
Price is 22% lower: these conditions cost them little and we have leverage before signing.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Design, risk and audit. The cheapest security bug is the one that never ships. Banyan Learning, a school fees and learning app company in Pune, wants to launch a new feature called Parent Pay on Friday the fourth of December. Parents see the fees due for their child, pay, and get a receipt by SMS."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("Today you're the security reviewer. We read the design, threat-model it with pytm, the open-source threat modelling tool, find the cheapest attack in an attack tree, check the risk register with DuckDB, and write the memo, the audit exception and the vendor decision. Real software, on a real Linux machine."),
 close("files"),
 term,

 chapter("1. Read the design like a reviewer"),
 say("Step one: read the design like a reviewer. For every part, ask three things. What data does it hold or carry? Who can reach it? And what has the team already decided? The decisions taken are where most of the risk hides."),
 cmd("cat design.md", 5),
 after("Read the decisions taken. The app sends the amount. PayGate tells us a payment succeeded by calling a webhook, and the webhook isn't signed yet. Office staff can mark a fee paid or refund it with one click. Each of those is a door."),
 clear,

 chapter("2. Threat-model it with STRIDE"),
 say("Step two: threat-model it. We describe the system as elements and the flows between them, with the trust boundaries, where data passes from one owner to another. In pytm that description is a short Python file."),
 edit("tm.py", "code", (200, 40, 1500, 1000)),
 wait(5),
 after("Four outside parties, two processes, one database, three boundaries, and seven flows, copied from dataflow.txt. pytm draws the data flow diagram for Graphviz, and checks every element and flow against its library of threats."),
 close("code"),
 cmd("python3 tm.py --dfd | dot -Tpng -o dfd.png && echo drawn", 4),
 {"open": ["firefox-esr", "--new-window", "file:///case/dfd.png"], "window": "dfd.png", "as": "img", "geometry": [60, 50, 1800, 960], "timeout": 60, "settle": 2},
 wait(4),
 after("Each dashed box is a trust boundary. The flow that crosses from the partners into Banyan's cloud, the PayGate webhook, is the one the whole feature trusts most and checks least. STRIDE names six kinds of threat: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service and Elevation of privilege."),
 close("img"),
 cmd("python3 tm.py --json tm.json && jq -r '.findings[] | [.target, .threat_id, .description] | @tsv' tm.json | sort | uniq | head -n 18 | cut -c1-150", 5),
 after("pytm's list is long and generic: a starting point, not a verdict. Our job is to pick the ones that matter for Parent Pay. Spoofing the webhook. Tampering with the amount. Repudiation of a refund nobody approved. Information disclosure in the SMS and the logs."),
 clear,

 chapter("3. The attack tree, the cheapest way in"),
 say("Step three: STRIDE gives a list. An attack tree gives an order: what's the cheapest way to reach the goal? The goal: get a fee marked paid without paying. OR means any one child will do. AND means every child is needed, so the costs add up. This script works out the cost of every branch."),
 cmd("python3 atree.py", 3),
 after("The cheapest way in is a fake webhook, cost one. Now we cut it, as if the webhook were signed, and see what's next."),
 cmd("python3 atree.py 'fake webhook'", 3),
 after("Changing the amount in the app, cost two. Cut that too, by having the server look up the amount."),
 cmd("python3 atree.py 'fake webhook' 'change the amount'", 3),
 after("Now the cheapest way in costs five: stealing a staff login and issuing refunds. That's what MFA and a second approver are for. Each cut raises the attacker's price."),
 clear,

 chapter("4. Write the design review memo"),
 say("Step four: the model is for us. The memo is for the people who decide: ranked, short, with conditions for go-live, things to fix soon, and what's good."),
 edit("memo.txt"),
 write(MEMO, cps=42),
 save_note(),
 close("note"),
 clear,

 chapter("5. Build the risk register"),
 say("Step five: a risk register records each risk, how likely and how bad, what we'll do, who owns it and by when. The product team's first try is a CSV. This DuckDB query checks every row: a treatment, an owner, a due date, a control if the treatment is mitigate, and no high risk accepted without sign-off."),
 cmd("cat check-register.sql | head -n 3", 2),
 cmd("duckdb < check-register.sql", 4),
 after("The worst risk, the fake payment confirmation, scores twenty-five and has nothing at all: no treatment, no owner, no date. Refund fraud scores fifteen and was simply accepted, with no sign-off. Personal data in logs is marked mitigate with no control and no owner. Only one row of four is complete."),
 clear,

 chapter("6. The Statement of Applicability"),
 say("Step six: an ISO 27001 auditor asks which controls apply, which are in place, and where's the evidence. The rule: met without evidence is not met. Here's what Banyan can show today."),
 cmd("cat controls-evidence.txt | cut -c1-160", 4),
 after("On the course site, the compliance tool takes each control and marks it met, partly, gap or not applicable, with this evidence beside it."),
 clear,

 chapter("7. Write the audit exception"),
 say("Step seven: internal audit raised finding IA-2026-07."),
 cmd("cat audit-finding.txt", 3),
 after("Three critical vulnerabilities past the fifteen-day target, and fixing all three today isn't possible. An exception is how a company says not yet, honestly: what isn't met, why, the risk in the meantime, compensating controls, an owner, an expiry and who approved it."),
 edit("exception-IA-2026-07.txt"),
 write(EXCEPTION, cps=42),
 save_note(),
 close("note"),
 clear,

 chapter("8. The vendor file"),
 say("Step eight: TextBridge is the cheapest SMS vendor, and the contract isn't signed yet. That's the moment you have leverage. Their questionnaire answers:"),
 cmd("cat vendor-textbridge.txt", 4),
 after("An expired certificate, unnamed sub-processors, MFA for most staff, logs kept two years, and incident notice in seven working days. The review must end in a decision."),
 edit("vendor-review.txt"),
 write(VENDOR, cps=42),
 save_note(),
 close("note"),
 clear,

 chapter("9. Hand in"),
 say("Step nine: hand in. The course notebook carries the threat model, the attack tree, the memo, the risk register, the Statement of Applicability, the exception and the vendor file."),
 cmd("ls -l *.txt *.png", 2),
 chapter("Wrap-up"),
 say("That's security before launch. You read the design for decisions already taken, modelled it with pytm, found the cheapest attack and priced it up step by step, turned it into a go-live memo, fixed a register where the biggest risk had no owner, wrote an honest exception, and used the moment before signing to get a vendor to do better. Next, in AI security, we attack and govern an LLM assistant. Thank you for watching."),
 wait(2),
]

build("s10-design-risk-audit", scenes, host="banyan-review", files={"tm.py": TM, "atree.py": TREE, "check-register.sql": CHECK})

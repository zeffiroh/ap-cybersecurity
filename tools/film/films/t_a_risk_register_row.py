from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

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

FIXED = """asset,threat,weakness,likelihood,impact,treatment,control,owner,due
Fees API,Fake payment confirmation,Webhook isn't signed,5,5,mitigate,Verify the gateway signature and confirm with the gateway,Sana Pillai,2026-12-01
Fees API,Fee amount changed by the parent,Amount comes from the app,4,4,mitigate,Server looks up the amount,Sana Pillai,2026-12-01
Admin console,Refund fraud by a stolen staff login,No MFA; one-click refunds,3,5,mitigate,MFA and a second approver for refunds,Kunal Desai,2026-12-01
Web framework,Exploit of the outdated web framework,Framework is two versions behind,3,5,mitigate,Upgrade and turn on automatic updates,Sana Pillai,2026-12-03
App logs,Personal data in logs,Full request bodies kept 90 days,4,3,mitigate,Mask personal data and keep logs 30 days,Sana Pillai,2026-12-03
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. Security teams find far more problems than any company can fix at once. A risk register is how leadership decides what to fix first, what to accept, and who is responsible. Today you'll fix a weak register and see what makes each row useful."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Banyan Learning in Pune, which runs a school fees and learning app. Its new payment feature, Parent Pay, launches on the fourth of December 2026, and we're doing the security review before launch. The case folder has the product team's first risk register and the threat model."),
 close("files"),
 term,

 chapter("1. The first register has holes"),
 say("The product team's first register is a simple table. Each row needs: the asset, the threat, the weakness, a likelihood and an impact from one to five, a treatment, a control, an owner and a date."),
 cmd("column -t -s, risk-register-banyan.csv | cut -c1-170", 4),
 after("Some rows have no owner, some have no treatment, and one high risk is accepted with nobody's name on it. Likelihood times impact gives the score, and fifteen or more is high. This DuckDB query checks every row and flags any high risk that's accepted without sign-off."),
 {"use": "term", "at": [0.5, 0.45], "keys": ["ctrl+u"], "type": "duckdb < check-register.sql", "wait": 4, "cps": 16},
 after("The worst risk, the fake payment confirmation, scores twenty-five and has nothing at all: no treatment, no owner, no date. Refund fraud scores fifteen and was simply accepted, with no sign-off. Personal data in logs is marked mitigate with no control and no owner."),
 clear,

 chapter("2. Build the fixed register"),
 say("Now fix it. Every row gets a treatment, a control, a named owner and a date. The webhook is the worst risk, so the treatment is mitigate, by verifying the payment gateway's signature, owned by Sana Pillai, due the first of December, before launch. Refund fraud is mitigated with multi-factor sign-in and a second approver. And the outdated web framework gets its own row."),
 edit("risk-register-fixed.csv"),
 write(FIXED, cps=60),
 save_note(),
 close("note"),
 say("Now run the same check on the fixed file."),
 cmd("sed 's/risk-register-banyan/risk-register-fixed/' check-register.sql | duckdb", 4),
 after("No problems left. Fake payment confirmation, twenty-five. Fee amount changed by the parent, sixteen. Then two at fifteen: refund fraud through a stolen staff login, and an exploit of the outdated web framework. Four high risks. Notice every row now has a named person and a date. And look at treatment. Accept is a real choice, but it belongs to someone senior enough to pay for the consequence."),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 10, Design, risk and audit. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. Every risk needs a score, a treatment, a control, an owner and a date. Score it as likelihood times impact. Mitigate what you can before launch, and when you accept a risk, get the right person's name on it. A register like this turns a list of worries into decisions. Thank you for watching."),
 wait(2),
]

build("t-a-risk-register-row", scenes, host="banyan-review", files={"check-register.sql": CHECK})

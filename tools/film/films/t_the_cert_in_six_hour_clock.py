from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

CERTIN = """CERT-In incident report (draft)            EXERCISE
Organisation: Kaveri Microfinance Ltd, Bengaluru (NBFC, regulated by RBI)
Contact: Meenal Rao, CISO
Incident type: Data breach; unauthorised access of data
Occurred: 2027-06-08 03:10 UTC (08:40 IST) to 04:18 UTC (09:48 IST)
Noticed: 2027-06-08 04:50 UTC (10:20 IST), WAF digest review
Filed: 2027-06-08 06:30 UTC

Systems affected: loan app API, api.kaveri.example, path /v2/customers/{id}/kyc
What happened: one client with a valid token for customer 118842 asked for
  other customers' records in order (100001 to 102060). The API did not check
  ownership and returned each full KYC record. WAF rule 9021 was in log-only mode.
Extent: 2,060 customer records: name, mobile, loan amount, Aadhaar last 4, address.
Indicators: 198.51.100.66, user agent python-requests/2.31.0
Done so far: 198.51.100.66 blocked at the WAF; rule 9021 switched to block;
  developers fixing the ownership check; logs preserved.
Not known yet: when the flaw was introduced; whether other clients used it.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. In India, many cyber incidents must be reported to CERT-In, the national computer emergency response team, within six hours. Six hours from when, though? That one question decides whether a company files on time. Today you'll start the clock correctly and file the report."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting, and it's marked EXERCISE, because this is a rehearsal. Kaveri Microfinance, a non-banking finance company in Bengaluru, regulated by the Reserve Bank of India. Tuesday the eighth of June 2027, after the Digital Personal Data Protection Rules' breach duties have started. All times are UTC unless marked IST, and IST is UTC plus five thirty. Before any real incident, always check the current text of each rule, because rules change."),
 close("files"),
 term,

 chapter("1. Start the clock"),
 say("Every breach clock starts at the moment you noticed. Not when the attack began, and not when you finished investigating. Read the analyst's note and the WAF alert, and write down three times: when the attack started, when Kaveri noticed, and when the six-hour report is due."),
 cmd("cat waf_alert.txt", 3),
 after("The analyst's note says rule 9021, one client reading many different customers' records, fired two thousand and sixty times for one address, between 08:40 and 09:48 IST. The rule was in log-only mode, so nothing was blocked. So the attack started at 08:40 IST, which is 03:10 UTC. But Kaveri noticed when the analyst reviewed the digest, at 10:20 IST, which is 04:50 UTC. That's the time that starts the clock. The date command can do the deadline arithmetic, so nobody adds hours in their head."),
 cmd("for h in 6 72; do date -u -d \"2027-06-08 04:50 UTC + $h hours\" \"+$h hours: %a %d %b %H:%M UTC\"; done", 3),
 after("Six hours from 04:50 is 10:50 UTC, or 16:20 IST. Seventy-two hours is 04:50 UTC on Friday the eleventh."),
 clear,

 chapter("2. File with CERT-In inside six hours"),
 say("Now file the CERT-In report with what you know. You won't know everything yet, and that's expected: file on time with partial facts, and say what you don't know. We draft the content first."),
 edit("certin-filing.txt"),
 write(CERTIN, cps=40),
 save_note(),
 after("The reporter is the CISO, Meenal Rao. The incident type is data breach, because personal data was taken by someone who shouldn't have it. Every time has a zone, and the detected time, 04:50 UTC, matches the evidence. The extent is a number from the logs, not a guess. The indicators are the address and the user agent. And the last line says what we don't know yet. Filed before 10:50 UTC. When the facts change, you send an update. And remember, CERT-In is only one clock. The DPDP Board and the RBI have their own, and the seminar covers all of them."),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 6, Breach clocks: CERT-In 6 hours, DPDP, RBI and GDPR. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. The clock starts when you noticed, not when the attack began. Write every time in UTC and in IST. File on time with partial facts, say what you don't know, and update when the facts change. Thank you for watching."),
 wait(2),
]

build("t-the-cert-in-six-hour-clock", scenes, host="kaveri-soc")

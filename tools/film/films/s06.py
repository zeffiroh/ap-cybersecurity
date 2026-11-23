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

ORDER = """clock,due (UTC),owner,status
CERT-In,Tue 08 Jun 10:50,CISO,filed 06:30
RBI,Tue 08 Jun 10:50,Head of compliance,due
Data Protection Board (intimation),without delay,DPO,due
Each affected person (2060),without delay,DPO,notice drafted
Data Protection Board (detailed report),Fri 11 Jun 04:50,DPO,due
EU authority (GDPR; 64 DE and IE),Fri 11 Jun 04:50,DPO with legal,check if it applies
"""

NOTICE = """Subject: Your Kaveri loan details were seen by someone else

On 8 June 2027, between 8:40 and 9:48 in the morning, a fault in the Kaveri app let one
person read other customers' details. Yours were among 2,060 records they saw: your name,
mobile number, loan amount, the last 4 digits of your Aadhaar, and your address.
They could not see your full Aadhaar, bank account, password or OTPs, and no money moved.

What we have done: fixed the fault, blocked the person, and told CERT-In, the RBI and
the Data Protection Board.

What you can do: be careful of calls or messages that use your loan details. Kaveri will
never ask for your OTP or PIN. Report anything strange to us.

Questions: Arvind Shetty, Data Protection Officer, dpo@kaveri.example, 1800 000 0000.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Breach clocks. When personal data leaks, the technical work is only half the job. The other half is telling the right people, in the right order, before each deadline runs out. In India the first clock is CERT-In's six hours. Then there's the Reserve Bank for regulated lenders, the Data Protection Board and every affected person under the DPDP Rules, and, if some customers live in Europe, GDPR's 72 hours."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("This is an exercise at Kaveri Microfinance, a lender in Bengaluru, on Tuesday the eighth of June 2027. It's marked as an exercise because it's set after the DPDP breach duties begin, and the first rule of this work is: before any real incident, check the current text of every rule. We use the terminal and a text editor, and the CERT-In tool on the course site for the filing and the tabletop."),
 close("files"),
 term,

 chapter("1. Start the clock"),
 say("Step one: start the clock. Every breach clock starts at the moment you noticed. Not when the attack began, and not when you finished investigating. So the first job is to find that moment in the evidence: the SOC analyst's note."),
 cmd("cat waf_alert.txt", 3),
 after("Reviewed at 10:20 IST, which the analyst has helpfully written as 04:50 UTC. IST is UTC plus five and a half hours. That's the moment Kaveri noticed, so every clock starts at 04:50 UTC. The date command can do the deadline arithmetic for us, so nobody adds hours in their head at five in the morning."),
 cmd("for h in 6 72; do date -u -d \"2027-06-08 04:50 UTC + $h hours\" \"+$h hours: %a %d %b %H:%M UTC\"; done", 3),
 after("Six hours from 04:50 is 10:50 UTC on Tuesday. Seventy-two hours is 04:50 UTC on Friday the eleventh."),
 clear,

 chapter("2. Scope it from the logs"),
 say("Step two: scope it from the logs. Regulators ask three questions first: what happened, how much, and to whom. The API log answers the first two. First, how many requests came from the scraper's address."),
 cmd("grep -c 198.51.100.66 api_access.log", 2),
 cmd("grep 198.51.100.66 api_access.log | sed -n '1p;2p;$p'", 3),
 after("Two thousand and sixty requests. The first at 08:40 IST for customer 100001, the next for 100002, and the last at 09:48 IST for 102060. The user agent is python-requests, a script, not the Kaveri app. Did they all succeed, and how many different customers?"),
 cmd("grep 198.51.100.66 api_access.log | awk '{print $9}' | sort | uniq -c", 2.5),
 cmd("grep 198.51.100.66 api_access.log | awk '{print $7}' | sort -u | wc -l", 2.5),
 after("Every one returned 200, OK, and every one was a different customer. For comparison, normal app users."),
 cmd("grep -vc 198.51.100.66 api_access.log; grep -v 198.51.100.66 api_access.log | awk '{print $1}' | sort -u | wc -l; grep -v 198.51.100.66 api_access.log | awk -F'\"' '{print $2, \"|\", $6}' | head -n 4", 3.5),
 after("320 normal requests that morning, from 320 different phones, each asking for its own customer's loans, repayments or offers, through the Kaveri app. One address asking for two thousand customers, in order, with a script, is not a customer. Now the times in UTC, because the log is in IST and our report isn't. date converts them."),
 cmd("date -u -d '2027-06-08 08:40:00 +0530' +%H:%M; date -u -d '2027-06-08 09:48:38 +0530' +%H:%M", 2.5),
 after("The scraping ran from 03:10 to 04:18 UTC. It started more than an hour and a half before anyone noticed, but the clock still starts at 04:50."),
 clear,

 chapter("3. Who is affected"),
 say("Step three: to whom. The API's own response log lists every record the scraper received, with the customer's country of residence and the fields that went out. The countries decide which clocks apply."),
 cmd("head -n 3 affected_customers.csv", 2),
 cmd("tail -n +2 affected_customers.csv | cut -d, -f2 | sort | uniq -c | sort -rn", 2.5),
 after("Two thousand and sixty records. 1,932 live in India, 64 in the UAE, 41 in Germany and 23 in Ireland. Everyone is covered by India's rules. The 64 in Germany and Ireland are residents of the European Union, so GDPR may apply as well. Which fields?"),
 cmd("tail -n +2 affected_customers.csv | cut -d, -f3 | sort | uniq -c", 2.5),
 after("The same five for every record: name, mobile number, loan amount, the last four digits of Aadhaar, and address. Enough to make a very convincing fraud call."),
 clear,

 chapter("4. File with CERT-In inside six hours"),
 say("Step four: file with CERT-In inside six hours. CERT-In is the national computer emergency response team, and its directions ask for many kinds of incident to be reported within six hours of noticing. You won't know everything yet, and that's expected. File on time with what you know, say what you don't know yet, and update when the facts change. We draft the content first."),
 edit("certin-filing.txt"),
 write(CERTIN, cps=36),
 save_note(),
 after("Every time has a zone. The extent is a number from the logs, not a guess. The indicators are the address and the user agent. And the last line says what we don't know yet. On the course site, the CERT-In tool checks these times against the evidence, and after you file, the inbox brings new facts. One of them: the flaw was released on the twenty-first of May, so the filing needs an update."),
 close("note"),
 clear,

 chapter("5. Every clock, in order"),
 say("Step five: every clock, in order. CERT-In is only the first. The Reserve Bank wants regulated lenders to report cyber incidents within six hours too. The DPDP Rules say tell the Data Protection Board without delay, then send a detailed report within 72 hours, and tell each affected person without delay. And GDPR's 72 hours, if it applies. We write them as one table, with one owner each."),
 edit("notification-order.csv"),
 write(ORDER, cps=36),
 save_note(),
 close("note"),
 cmd("column -t -s, notification-order.csv", 3),
 after("One page, in time order, one name against each clock. When the CEO asks are we on time, this is the answer."),
 clear,

 chapter("6. Decide with four regulators watching"),
 say("Step six: decide with four regulators watching. On the course site, the tabletop puts you in the CISO's chair. A CEO who wants to wait until everything is known, a DPO who wants a plan, and a journalist who says she already has a sample of customer records. Here's the shape of the decisions."),
 cmd("jq -r '.nodes[] | \"\(.title)  \(.text)\"' tabletop-kaveri-clocks.json | cut -c1-150", 3.5),
 after("Play it once as the CISO, then again as the CEO, and notice which decision feels hardest from that chair. Waiting until everything is known feels safe, and it is exactly how companies miss the six hours."),
 clear,

 chapter("7. The notice to customers"),
 say("Step seven: two more readers. The Board needs to decide; the customers need to know what happened to them and what to do. The notice must be short and plain, in the language the customer uses with Kaveri, and say five things: what happened, with its nature, extent and timing; the likely consequences; what Kaveri has done; what the person can do; and who to contact."),
 edit("customer-notice.txt"),
 write(NOTICE, cps=36),
 save_note(),
 after("Read it aloud. It says what was seen and what wasn't, warns about the most likely harm, fraud calls, and gives a real person to contact. A customer can understand it in a minute."),
 close("note"),
 clear,

 chapter("8. Hand in"),
 say("Step eight: hand in. On the course site the notebook carries your answers, the CERT-In filing, the notification order, the tabletop, the Board note and the customer notice."),
 cmd("ls -l *.txt *.csv", 2.5),
 chapter("Wrap-up"),
 say("That's a breach from the regulator's side. The clock starts when you noticed, at 04:50 UTC, not when the scraping began at 03:10. You scoped it from the logs: 2,060 records, 64 of them in Germany and Ireland. You drafted CERT-In inside six hours with what you knew, ordered every other clock with one owner each, and wrote a notice a customer can understand in a minute. And remember the exercise label: rules change, so check the current text of every one before a real incident. Next, in Identity from both sides, we look at how attackers move through accounts and permissions. Thank you for watching."),
 wait(2),
]

build("s06-breach-clocks", scenes, host="kaveri-soc")

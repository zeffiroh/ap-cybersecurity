from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

RULES = {
 "rules/domain-only.yar": """rule llh_phishing_domain
{
  meta:
    description = "Anything that mentions the phishing domain"
  strings:
    $d = "login-verify.example"
  condition:
    $d
}
""",
 "rules/guest-complaint-lure.yar": """rule llh_guest_complaint_lure
{
  meta:
    description = "The fake guest-complaint email aimed at hotel reservations teams"
    author = "SOC"
    reference = "AL-4101, message 7C1A20F11"
  strings:
    $subject = "Subject: Guest complaint BKG-"
    $link = "login-verify.example/complaints/"
    $press = "hidden from search results"
  condition:
    all of them
}
""",
 "rules/bp-grab-stealer.yar": """rule bp_grab_stealer_strings
{
  meta:
    description = "Strings from Boarding_Pass.pdf.exe, a password stealer left on guest USB sticks"
  strings:
    $mutex = "Global\\\\bp-grab-7731"
    $chrome = "\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data"
    $flag = "--grab-all"
    $exfil = "telegram-relay.example/bot"
  condition:
    3 of them
}
""",
}

MISSES = """What each rule would miss
domain-only.yar         nothing about this domain, but it also fires on our own alerts, intel and logs (5 files).
guest-complaint-lure.yar a new email with a different subject, link path or threat; tighter means fewer false alarms and more misses.
bp-grab-stealer.yar     a rebuilt version that changes more than one of the four strings; 3 of 4 gives some room.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. YARA is a pattern-matching tool that security teams use to find files: malware, phishing emails, anything with a recognisable fingerprint. Today you'll write a YARA rule that catches this morning's phishing lure and nothing else. The hard part isn't catching the bad file. It's not catching the good ones."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Lotus Lake Hotels, three lake-side hotels in Udaipur, Wednesday the eleventh of November 2026, the start of the wedding season. This morning the reservations team reported a fake guest complaint: an email pretending to come from a booking website, with a link to a fake sign-in page on login-verify.example. The mail gateway can scan every incoming email with a YARA rule, so a good rule stops the next one."),
 close("files"),
 term,

 chapter("1. A YARA rule for the lure"),
 say("A YARA rule has three parts. meta, which describes the rule. strings, the text or bytes to look for. And condition, which says how many of those strings must be found. The first rule is the obvious one: match anything that mentions the phishing domain."),
 cmd("cat ~/rules/domain-only.yar", 2),
 say("We test it on every file in the case, not just the email, because that's how you find out what else it catches."),
 cmd("yara -r ~/rules/domain-only.yar . | sort", 3),
 after("Five files match. Only one of them is an email. The others are the alert queue, the threat-intel feed, the hotel association's block list and the proxy log. They all mention the domain because they're about the attack. In a file scanner or across an analyst's notes this rule would fire all day, and analysts stop trusting rules that cry wolf."),
 say("Now the tuned rule. It needs three things together that only the lure email has: a subject starting Guest complaint BKG, a link to login-verify.example slash complaints, and the threat in the body, hidden from search results. The condition says all of them."),
 cmd("cat ~/rules/guest-complaint-lure.yar", 2.5),
 cmd("yara -r -s ~/rules/guest-complaint-lure.yar .", 3),
 after("It matches one file: guest-complaint.eml, and minus s shows the three strings it found. That's the rule you'd ship. The third rule shows how YARA is usually used: on malware. The antivirus quarantined Boarding_Pass.pdf.exe at the front desk, a password stealer left on a guest's USB stick. The rule describes it by four strings from inside the program, and the condition says three of them, so one changed string doesn't let a new version slip past."),
 cmd("yara -r -s ~/rules/bp-grab-stealer.yar .", 3),
 after("One match."),
 clear,

 chapter("2. What each rule would miss"),
 say("Finally, write one line for each rule on what it would miss. For the tuned rule: a new email with a different subject or domain. That's the trade-off: tighter rules make fewer false alarms but miss more variations."),
 edit("rule-notes.txt"),
 write(MISSES, cps=46),
 save_note(),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 3, SOC triage: alerts, phishing, threat intel and AI verdicts. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. A YARA rule is meta, strings and a condition. Always test on every file you have, not just the bad one. Pick strings that only the bad thing has, and say what the rule would miss. That's how a rule earns the team's trust. Thank you for watching."),
 wait(2),
]

build("t-a-yara-rule-for-a-lure", scenes, host="lotuslake-soc", files=RULES,
      setup=["mkdir -p ~/rules && mv rules/* ~/rules/ && rmdir rules"])

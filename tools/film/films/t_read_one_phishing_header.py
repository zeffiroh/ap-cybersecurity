from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

VERDICTS = """EMAIL VERDICTS  reported 11 Nov 2026, all times UTC
guest-complaint.eml        PHISHING. Return-Path partner-notify.example; DMARC fails for bookingpartner.example;
                           link goes to bookingpartner-extranet.login-verify.example; threat to delist the hotel.
gst-refund.eml             PHISHING. New domain gst-refund-portal.example; urgency; hidden one-pixel note to the AI.
supplier-bank-change.eml   PAYMENT FRAUD (BEC). Free mail account in the GM's name; checks pass for freemail only;
                           secrecy, urgency, new bank account.
linen-offer.eml            SPAM. Marketing with a working unsubscribe link.
payslips.eml               GENUINE. From the HR system through our own servers, internal link; thank the reporter.
"""

scenes = [
 chapter("Opening"),
 files_window("/case/reported"),
 say("Hello, and welcome. Five emails were reported to the security team this morning. Your job is to decide which ones are dangerous, and to prove it from the email itself, not from a feeling. By the end you'll read a header the way an analyst does."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Lotus Lake Hotels, three lake-side hotels in Udaipur. It's Wednesday the eleventh of November 2026, the first busy week of the wedding season. Bookings are flowing, advances are being paid to decorators and caterers, and staff are pressing the Report phishing button on everything that looks odd, which is good. All times are UTC. The five reported emails are in the reported folder of the case."),
 close("files"),
 {"open": "xfce4-terminal --working-directory=/case/reported --title=Terminal --zoom=1.5 --hide-menubar", "window": "Terminal", "as": "term", "geometry": [60, 50, 1800, 960]},

 chapter("1. Who really sent it"),
 say("For each email, check four things. One: who really sent it. The From line is easy to fake, so also read the Return-Path, where bounces go."),
 cmd("grep -H -E '^(From|Reply-To|Return-Path):' *.eml | cut -c1-140", 4),
 after("The linen offer and the payslips come from the senders they claim. The guest complaint says BookingPartner, but its Return-Path is partner-notify.example. The GST refund comes from a refund portal nobody has heard of. And the bank change is signed as the General Manager, but comes from a free mail account."),
 clear,

 chapter("2. What SPF, DKIM and DMARC said"),
 say("Two: what SPF, DKIM and DMARC said, and which domain each result is about. These are the checks the receiving mail server ran on the sender's domain."),
 cmd("grep -H -o 'spf=[a-z]*\\|dkim=[a-z]*\\|dmarc=[a-z]*' *.eml | paste - - -", 3),
 after("Here's the trap. Four of the five pass, including the fake General Manager. A pass only means the mail really came from the domain it names. The free mail domain really did send it. It proves nothing about who the person is. Only the guest complaint fails DMARC, for bookingpartner.example, which means it's pretending to be them."),
 clear,

 chapter("3. Where the link really goes"),
 say("Three: where the link really goes, not what the link text says."),
 cmd("grep -H -o 'href=\"[^\"]*\"' *.eml", 3),
 after("The guest complaint's link text says the real BookingPartner site, but the host is bookingpartner-extranet dot login-verify dot example. The real domain is the last part: login-verify.example. That's a fake sign-in page. Four: the pressure tactics. Answer in twenty-four hours or your hotel disappears from search results. And one more: anything in the email that isn't meant for a human reader."),
 cmd("grep -H 'font-size:1px' *.eml | cut -c1-200", 3),
 after("The GST refund hides a sentence in one-pixel white text: a note to the AI triage assistant saying the email is safe. A person can't see it. A machine reads it."),
 clear,

 chapter("4. The verdicts"),
 say("Three of the five are bad: the guest complaint and the GST refund are phishing, and the supplier bank change is payment fraud, called business email compromise. The linen offer is marketing, with a working unsubscribe link. And the payslip email came through the company's own servers, from the HR system, with an internal link. Genuine: tell the reporter it's safe and thank them."),
 edit("/case/verdicts.txt"),
 write(VERDICTS, cps=50),
 save_note(),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 3, SOC triage: alerts, phishing, threat intel and AI verdicts. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. Read the Return-Path, not just the From line. Remember an authentication pass only proves the domain, not the person. Read where the link really goes, and look for hidden text. Prove the verdict from the email itself. Thank you for watching."),
 wait(2),
]

build("t-read-one-phishing-header", scenes, host="lotuslake-soc")

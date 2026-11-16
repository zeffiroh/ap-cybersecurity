HACKER ROOM TRIAL: Lantern Cafe, Saturday 14 November 2026 (times UTC)

The cafe's Wi-Fi portal (portal01, 10.9.0.10) showed a strange welcome message this morning.
Look around with the programs on the desktop. Everything here is a lab copy: nothing reaches the internet.

  auth.log                    the portal server's login log
  capture.pcap                a few minutes of network traffic (open it in the Packet viewer)
  eventlogs/Security.jsonl    the till PC's Windows Security log (open it in the Event viewer)
  alerts-trial.json           three alerts (open them in the Alert queue)
  intel.json                  what threat intel says about the addresses
  mail/prize.eml              an email a barista reported
  process.csv                 programs that ran on the till PC
  risk-trial.csv              the cafe's risk list (open it in the Risk register)
  certin-trial.json           the incident report clock (open it in CERT-In)
  ai-trial.json               the cafe's booking chatbot (open it in AI security)

Try in a terminal:  grep "Failed password" auth.log | wc -l     then    grep Accepted auth.log

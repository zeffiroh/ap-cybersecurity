Wattle & Finch Accountants, Brisbane: a 14-person accounting practice and a client of our managed SOC.
Thursday 12 November 2026. All times are UTC. Brisbane is UTC+10 (00:00 UTC is 10:00 in Brisbane; it is 05:30 in India).
You are on the night shift; the client's working day runs while you are on.

acc-lt03       10.40.0.23   laptop of j.walsh, the practice manager
reception-pc01 10.40.0.11   reception; sends files to clients through cloud storage
acc-lt01, 02, 04, 05        the accountants' laptops (10.40.0.21, .22, .24, .25)
fs01           10.40.0.5    file server; S:\Clients holds every client's tax files
10.40.0.2                   the client's DNS server
edge-fw01                   the client's internet firewall. There is no web proxy: laptops go straight out through the firewall.

The queue has twelve alerts and no severities. One real intrusion is hiding in it.

What you have:
  alerts-night.json       the twelve alerts
  eventlogs/Sysmon.jsonl, Security.jsonl, System.jsonl   Windows logs from acc-lt03
  process.csv             EDR process list from acc-lt03
  fw_sessions.csv         the firewall's session log for every laptop
  dns.log                 the DNS server's query log
  capture.pcap            a short packet capture of acc-lt03's internet traffic
  intel.json              threat-intel indicators and the client's allow list

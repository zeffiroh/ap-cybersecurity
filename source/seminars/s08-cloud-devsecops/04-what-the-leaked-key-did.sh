cd ~/case/cloud
grep -o '"source_ip": "[^"]*"' audit.json | sort | uniq -c
echo ---
grep -c RunInstances audit.json
grep -o '"action": "[A-Za-z]*"' audit.json | sort | uniq -c

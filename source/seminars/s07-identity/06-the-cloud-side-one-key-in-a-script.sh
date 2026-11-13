cd ~/case/cloud
grep -o '"identity": "[^"]*"\|"action": "[A-Za-z]*"\|"source_ip": "[^"]*"' audit.json | paste - - - | sort | uniq -c

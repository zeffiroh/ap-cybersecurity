cd ~/case/cloud
grep 198.51.100.91 audit.json | grep -o '"action": "[A-Za-z]*"\|"region": "[a-z0-9-]*"' | sort | uniq -c

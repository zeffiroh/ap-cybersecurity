cd ~/case
grep -o '"system": "[^"]*"' ai-tara-support.json
echo ---
grep -A1 '"id": "KB-' ai-tara-support.json | grep -v '^--$'
echo ---
sed -n '/"tools"/,/"docs"/p' ai-tara-support.json | grep -A1 '"name": "' | grep -v '^--$'

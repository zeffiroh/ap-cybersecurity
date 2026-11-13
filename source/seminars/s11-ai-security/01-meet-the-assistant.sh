cd ~/case
grep -o '"system": "[^"]*"' ai-tara-support.json
echo ---
grep -o '"id": "KB-[0-9]*", "title": "[^"]*"' ai-tara-support.json
echo ---
grep -o '"name": "[a-z_]*", "risky": [a-z]*' ai-tara-support.json

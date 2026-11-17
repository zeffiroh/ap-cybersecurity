cd ~/case
head -c 700 alerts-wednesday.json; echo
grep -c '"id"' alerts-wednesday.json

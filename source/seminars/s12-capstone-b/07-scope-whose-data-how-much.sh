cd ~/case
cat clients.csv
awk -F, 'NR>1 {s+=$2} END {print s, "people"}' clients.csv

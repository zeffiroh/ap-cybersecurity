cd ~/case/identity
cat users.csv
echo ---
grep -c . users.csv
awk -F, '$7=="no" {print $1, $4}' users.csv
echo ---
cat ad_edges.csv

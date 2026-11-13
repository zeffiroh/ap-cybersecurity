cd ~/case
tail -n +2 affected_customers.csv | cut -d, -f2 | sort | uniq -c | sort -rn
echo ---
head -2 affected_customers.csv

cd ~/case/zeek
grep -v '^#' conn.log | awk -F'\t' '{print $3, "->", $5":"$6, $8}' | sort | uniq -c | sort -rn
echo ---
grep -v '^#' conn.log | awk -F'\t' '$5=="10.30.2.33" {print $1, $3, $6, $12, $11}'

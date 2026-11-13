cd ~/case/captured
grep -v '^#' zeek-kerberos.log | awk -F'\t' '{print $8}' | sort | uniq -c
echo ---
grep rc4 zeek-kerberos.log | awk -F'\t' '{print $2, $5, $6}'

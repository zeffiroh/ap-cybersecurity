cd ~/case/zeek
grep -v '^#' conn.log | awk -F'\t' '$3=="10.80.9.33" && $6=="445" {print $5, $12}' | sort -u | awk '{print $2}' | sort | uniq -c
echo ---
grep -v '^#' smb_files.log | awk -F'\t' '{print $5, $6, $7}'

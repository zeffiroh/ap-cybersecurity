cd ~/case
grep 7C3E90B14 mail.log
echo ---
grep -E 'report|blocklist' mail.log
echo ---
grep -E 'AWB-77120|upd.dat|files-cdn-sync' proxy.log

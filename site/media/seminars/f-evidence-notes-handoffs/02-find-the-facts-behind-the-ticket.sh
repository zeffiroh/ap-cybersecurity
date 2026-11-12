cd ~/case
grep 4A1F21C02 mail.log
echo ---
grep -E 'report|blocklist' mail.log
echo ---
grep -E 'docm|s2.bin' proxy.log

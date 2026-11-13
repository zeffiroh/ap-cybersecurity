cd ~/case
grep -c '^198.51.100.66 ' api_access.log
grep '^198.51.100.66 ' api_access.log | grep -o '/customers/[0-9]*' | sort -u | wc -l
echo ---
grep '^198.51.100.66 ' api_access.log | head -1
grep '^198.51.100.66 ' api_access.log | tail -1
echo ---
grep -v '^198.51.100.66 ' api_access.log | head -3

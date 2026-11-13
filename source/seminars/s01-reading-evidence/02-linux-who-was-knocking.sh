cd ~/case
grep -c 'Failed password' auth.log
echo ---
grep 'Failed password' auth.log | grep -o 'from [0-9.]*' | sort | uniq -c | sort -rn
echo ---
grep 'Failed password' auth.log | grep -o 'for [a-z ]*from' | sort | uniq -c | sort -rn

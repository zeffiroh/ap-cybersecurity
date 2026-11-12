cd ~/case
wc -l auth.log access.log
grep -c 'Failed password' auth.log
grep 'Failed password' auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

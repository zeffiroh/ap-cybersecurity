cd ~/case
grep 'Accepted' auth.log
echo ---
grep 'sudo' auth.log | grep COMMAND
echo ---
cat recovered/m.sh
echo ---
cat crontab.txt
echo ---
grep -E 'sysmon|\.m\.sh' ps.txt

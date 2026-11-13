cd ~/case/captured
grep -E '^(724|6630|6711|6790) ' volatility-eng-ws14.txt
echo ---
grep -A4 'windows.cmdline' volatility-eng-ws14.txt
echo ---
grep -A4 'windows.sessions' volatility-eng-ws14.txt

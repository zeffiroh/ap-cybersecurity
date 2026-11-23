cd ~/case/reported
grep -H -E '^(From|Reply-To|Return-Path):' *.eml
echo ---
grep -H -o 'spf=[a-z]*\|dkim=[a-z]*\|dmarc=[a-z]*' *.eml
echo ---
grep -H -o 'href="[^"]*"' *.eml
echo ---
grep -H 'font-size:1px' *.eml

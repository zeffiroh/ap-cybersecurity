cd ~/case
grep logistlcs proxy.log
echo ---
grep logistlcs proxy.log | while read t ms ip code size method url rest; do echo "$(date -u -d @${t%.*} '+%F %T') $ip $code $url"; done

cd ~/case
grep -c 'kestrel-locked' share_listing.txt
grep 'Directory of' share_listing.txt
echo ---
sha256sum alerts.json mail.log proxy.log process.csv share_listing.txt invoice.eml

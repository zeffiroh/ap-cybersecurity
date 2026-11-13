cd ~/case
find . -type f | sort
echo ---
find . -type f -exec sha256sum {} + | sort -k2
echo ---
cat cloud/egress-alert.txt

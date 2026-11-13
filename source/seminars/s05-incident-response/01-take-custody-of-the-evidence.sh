cd ~/case
find . -type f | sort
echo ---
find . -type f -exec sha256sum {} + | sort -k2

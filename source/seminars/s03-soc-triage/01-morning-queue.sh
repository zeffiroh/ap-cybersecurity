cd ~/case
sha256sum *.* reported/* suspect/*
echo ---
grep -E '"(id|rule|host)"' alerts-tuesday.json

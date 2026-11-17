cd ~/case
sha256sum *.* eventlogs/*
echo ---
grep -c '"id"' alerts-night.json
grep -E '"(id|host|rule)"' alerts-night.json

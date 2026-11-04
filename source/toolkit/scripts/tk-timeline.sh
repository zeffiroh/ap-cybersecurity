d=${1:-.}
find "$d" -type f ! -name "*.pcap" | sort | while IFS= read -r p; do
    grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}[ T][0-9]{2}:[0-9]{2}' "$p" 2>/dev/null | sed "s|\$|   [$(basename "$p")]|"
done | sort | head -n "${2:-60}"

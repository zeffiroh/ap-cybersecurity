[ -n "$1" ] || { echo 'Give a file, for example: tk-top-ips auth.log'; exit 2; }
f="$1"
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' "$f" | sort | uniq -c | sort -rn | head -n "${2:-10}"

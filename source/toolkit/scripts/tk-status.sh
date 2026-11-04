[ -n "$1" ] || { echo 'Give a web or proxy log, for example: tk-status access.log'; exit 2; }
grep -oE '" [1-5][0-9]{2} |/[1-5][0-9]{2} ' "$1" | grep -oE '[1-5][0-9]{2}' | sort | uniq -c | sort -rn

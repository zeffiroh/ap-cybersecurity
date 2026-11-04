[ -n "$1" ] || { echo 'Give a folder, for example: tk-check-bad suspect known_bad.txt'; exit 2; }
d="$1"
[ -n "$2" ] || { echo 'Give the list of bad hashes, for example known_bad.txt'; exit 2; }
l="$2"
find "$d" -type f | sort | while IFS= read -r p; do
    h=$(sha256sum "$p" | cut -d" " -f1)
    if grep -q "$h" "$l"; then echo "KNOWN BAD   $p"; else echo "not listed  $p"; fi
done

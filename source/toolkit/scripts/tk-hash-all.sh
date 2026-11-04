d=${1:-.}
o=${2:-/tmp/evidence.sha256}
find "$d" -type f | sort | while IFS= read -r p; do sha256sum "$p"; done > "$o"
echo "$(wc -l < "$o") files hashed into $o"
head -n 5 "$o"

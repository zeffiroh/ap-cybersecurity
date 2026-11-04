[ -n "$1" ] || { echo 'Give a file, for example: tk-failed auth.log'; exit 2; }
f="$1"
t=/tmp/.tk-failed
grep -iE 'fail|invalid|denied|unauthori|TCP_DENIED|" 40[13] |/40[13] ' "$f" > "$t"
echo "$(wc -l < "$t") failure lines in $f"
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' "$t" | sort | uniq -c | sort -rn | head -n 10
rm -f "$t"

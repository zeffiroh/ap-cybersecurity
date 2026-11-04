[ -n "$1" ] || { echo 'Give some text, for example: tk-decode aGVsbG8='; exit 2; }
s="$1"
echo "base64: $(printf %s "$s" | base64 -d 2>/dev/null)"
echo "hex:    $(printf %s "$s" | xxd -r -p 2>/dev/null)"
echo "rot13:  $(printf %s "$s" | tr 'A-Za-z' 'N-ZA-Mn-za-m')"

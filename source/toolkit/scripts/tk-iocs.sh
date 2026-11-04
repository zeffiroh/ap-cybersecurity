d=${1:-.}
show() { echo "== $1"; grep -rhoE "$2" "$d" 2>/dev/null | sort -u | head -n 40; }
show Addresses '([0-9]{1,3}\.){3}[0-9]{1,3}'
show Links 'https?://[^ "<>]+'
show Domains '[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.(com|net|org|io|xyz|ru|cn|top|info|biz|co|in|edu|lan|local)\b'
show Hashes '\b[a-f0-9]{64}\b'
show Emails '[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+'

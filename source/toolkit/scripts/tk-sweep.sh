[ -n "$1" ] || { echo 'Give a range, for example: tk-sweep 10.20.0.0/24'; exit 2; }
r="$1"
nmap -sn "$r"

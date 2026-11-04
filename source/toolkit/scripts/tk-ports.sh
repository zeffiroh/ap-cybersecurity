[ -n "$1" ] || { echo 'Give a host, for example: tk-ports 10.20.0.5'; exit 2; }
h="$1"
nmap -sV "$h"

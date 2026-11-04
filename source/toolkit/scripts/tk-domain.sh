[ -n "$1" ] || { echo 'Give a domain, for example: tk-domain example.com'; exit 2; }
n="$1"
echo "== Address"
dig +short "$n"
echo "== Registration"
whois "$n"

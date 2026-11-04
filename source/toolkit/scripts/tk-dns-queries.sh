f=${1:-capture.pcap}
tshark -r "$f" -Y dns -T fields -e dns.qry.name | sort | uniq -c | sort -rn | head -n 30

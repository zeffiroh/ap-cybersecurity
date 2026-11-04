f=${1:-capture.pcap}
tshark -r "$f" -q -z conv,ip

f=${1:-capture.pcap}
tshark -r "$f" -Y http.request -T fields -e ip.src -e http.host -e http.request.method -e http.request.uri | head -n 40

cd ~/case
tshark -r capture.pcap -Y 'http.request' -T fields -e ip.src -e http.host -e http.request.uri -e http.user_agent

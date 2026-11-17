nmap -sV 10.40.0.0/24
echo ---
cd ~/case
grep 10.40.0.99 dhcp-leases.txt switch-ports.txt

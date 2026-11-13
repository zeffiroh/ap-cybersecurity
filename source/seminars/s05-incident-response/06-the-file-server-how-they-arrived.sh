cd ~/case/captured
cut -d, -f1-3 hayabusa-fs02.csv
echo ---
grep -i 'crit' hayabusa-fs02.csv | cut -d, -f2,8
echo ---
grep -i winupd velociraptor-fs02-services.csv

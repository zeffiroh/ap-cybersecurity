cd ~/case/captured
grep -E 'HIGH|CRITICAL|Total' trivy-cart-api.txt
echo ---
grep FAILED checkov-main-tf.txt | cut -c1-80
echo ---
grep ^FAIL prowler-monsoon-prod.csv | cut -d, -f2,4,5

cd ~/case/cloud
grep -i 'bucket/monsoon-invoices\|CreateAccessKey' audit.json | cut -c1-200

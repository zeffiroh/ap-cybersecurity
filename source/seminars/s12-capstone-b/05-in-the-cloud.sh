cd ~/case/cloud
grep -c GetObject audit.json
grep -o 'payroll-exports/[a-z-]*/' audit.json | sort | uniq -c

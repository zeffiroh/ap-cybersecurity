from kit import after, build, chapter, clear, close, cmd, files_window, say, term, wait

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. Tonight's question is a classic one: who got in overnight? You'll use three small Linux commands, grep, sort and uniq, to find a password-guessing attack in a server's login log, and then follow the attacker to what they left behind."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Tamarind Health, a clinic chain. The night of the fifth to the sixth of November 2026. All times are UTC, and India is five and a half hours ahead. The server is appt01, the appointments server, and its SSH port, 22, is open to the internet. The evidence is in the case folder."),
 close("files"),
 term,

 chapter("1. Linux: who was knocking"),
 say("auth.log records every SSH login, good or bad. The plan has three parts. First, count the failures with grep minus c."),
 cmd("grep -c 'Failed password' auth.log", 2),
 say("Second, count them by source address. grep minus o keeps only the from-address part of each line, sort puts the same addresses together, uniq minus c counts each one, and sort minus r n ranks them, biggest first."),
 cmd("grep 'Failed password' auth.log | grep -o 'from [0-9.]*' | sort | uniq -c | sort -rn", 2.5),
 after("Fifty failed passwords in total, and one address, 198.51.100.23, made forty-six of them. One address, dozens of guesses in a short time: that's a brute force. Third, the same trick for the user names it tried."),
 cmd("grep 'Failed password' auth.log | grep -o 'for [a-z ]*from' | sort | uniq -c | sort -rn", 2.5),
 after("Root, and names that don't exist here, like admin, test, ubnt, postgres and oracle, marked invalid user. And one name that does exist, vendor, tried sixteen times. Attackers try lists of usual names, and they only need one real account with a weak password."),
 clear,

 chapter("2. Linux: the login and what came next"),
 say("A brute force only matters if it worked. So now find the Accepted line."),
 cmd("grep Accepted auth.log", 2.5),
 after("Two Accepted lines. One is deploy, logging in with a key from the IT admin PC, as it does every night. That's normal. The other is the account vendor, from 198.51.100.23, with a password, at 01:19:44. That's our attacker. Now read everything that account did afterwards. sudo lines show each command run as root."),
 cmd("grep sudo auth.log | grep -o 'COMMAND=.*'", 2.5),
 after("The vendor account used wget to download a script into tmp, then ran it as root. And look at the last sudo line: smbclient, connecting to a file share called Scans on another machine. The attacker was already looking further into the network. Now read the script the IT contractor recovered."),
 cmd("cat recovered/m.sh", 3),
 after("It uses curl to download a program and saves it as /usr/local/bin/.sysmon-agent, with a dot at the start so a normal listing hides it, and adds a cron line that runs it every ten minutes. Now the two places an attacker hides to come back later: a scheduled job, called cron, and a running process."),
 cmd("cat crontab.txt; grep -E 'sysmon|\\.m\\.sh' ps.txt", 3),
 after("The backup job is old and normal. The .sysmon-agent line is new, and the process list shows it running since 01:21. That's persistence: even if you reset the password, the program keeps coming back."),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 1, Reading evidence: packets, Linux, Windows and network sensors. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. grep, sort and uniq turn a thousand log lines into a ranked list. One address, many failures, is a brute force. Then find the Accepted line, read what that account did, and check cron and the process list for what was left behind. Thank you for watching."),
 wait(2),
]

build("t-who-got-in-overnight", scenes, host="tamarind-soc")

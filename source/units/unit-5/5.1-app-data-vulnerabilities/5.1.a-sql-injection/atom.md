# 5.1.a, SQL Injection

> **Unit 5 · 5.1 Application and Data Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 5.1.A, 5.1.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)

Identify SQL injection attack patterns in web application input, explain how unsanitized queries expose database contents, and apply detection logic to flag malicious parameter strings.

## Lesson

### What is SQL Injection?

Web applications that store data almost always use a relational database behind the scenes. When a user logs in, searches for a product, or retrieves a record, the application typically builds a SQL query using whatever the user typed. SQL injection (SQLi) happens when an attacker types SQL syntax instead of ordinary data, and the application blindly pastes it into the query without checking. The database then executes the attacker's SQL as if it were the application's own code.

This is not a niche or exotic attack. The Open Web Application Security Project (OWASP) has listed injection as one of the top web risks for over a decade. Real breaches attributed to SQLi include the 2008 Heartland Payment Systems compromise, where attackers stole over 130 million card numbers by injecting a database command through a web form.

### How Queries Get Built

Consider a login form. When you type your username and password, many applications build a query that looks like this:

```
SELECT * FROM users WHERE username = 'alice' AND password = 'secret';
```

The application fills in `alice` and `secret` from whatever the user typed. If the developer does this with simple string concatenation rather than parameterized queries, the query is built like:

```python
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "';"
```

Now picture an attacker who types `admin'--` as the username. The resulting query becomes:

```
SELECT * FROM users WHERE username = 'admin'--' AND password = 'anything';
```

In SQL, `--` is a comment character. Everything after it is ignored. The password check disappears. The attacker is logged in as `admin` without knowing the password.

### Common Payload Patterns

Attackers have catalogued dozens of payload patterns over the years. The major families are:

**Authentication bypass**, uses `OR` logic to make the WHERE clause always true. A classic example: typing `' OR '1'='1` as a password transforms the WHERE clause into one that is always satisfied, returning the first user in the database (often an administrator).

**Comment truncation**, using `--` or `/*` to comment out the rest of the query. `admin'--` is the textbook example. The `/*...*/ ` block-comment form is used when line comments are filtered.

**UNION-based extraction**, the `UNION SELECT` construct appends an attacker's own SELECT to the original query. If the original returns two columns, an attacker can write `UNION SELECT username, password FROM users` to dump credentials alongside normal results.

**Stacked queries and stored procedure abuse**, some database drivers allow multiple statements separated by semicolons. `'; DROP TABLE users--` attempts to delete a table. On Microsoft SQL Server, `EXEC(` and `xp_` (extended stored procedures like `xp_cmdshell`) can execute operating-system commands.

**Time-based blind injection**, when the application gives no visible output, attackers use `SLEEP(5)` or `WAITFOR DELAY` to infer data one bit at a time by watching whether a response is slow.

### Why It Still Works

SQL injection survives because it is easy to introduce and easy to miss in code review. A developer under deadline pressure writes one concatenated query. A legacy codebase mixes safe and unsafe patterns. Automated scanners catch obvious cases but miss logical-context variations. Once a single injection point exists, the attacker's leverage is enormous: they can read, modify, or delete any data the application account can touch.

### Detecting and Preventing SQLi

Detection at the network or application layer scans incoming query parameters for known payload strings: quotes followed by SQL keywords, comment sequences, UNION, DROP, EXEC, and so on. This is what the coding problem in this skill asks you to implement.

Prevention requires fixing the root cause: parameterized queries (also called prepared statements). Instead of concatenating user input into a SQL string, the developer passes the SQL template and the data values separately. The database driver handles quoting and escaping, making it structurally impossible for user data to be interpreted as SQL syntax. Web Application Firewalls (WAFs) can block known payloads in transit but are not a substitute for parameterized queries.

### AP Connection

LO 5.1.A asks you to explain how attackers can exploit weaknesses in applications that handle data. SQL injection is the defining example: the weakness is trusting user input, the exploit is inserting SQL logic, and the impact ranges from data theft to complete database destruction. LO 5.1.B asks you to describe defenses; parameterized queries and input validation are the standard technical controls, with least-privilege database accounts as a depth-of-defense measure.

The simulation (the simulation) lets you try three payload types against a fake login form and see the raw SQL the server would execute. The coding problem asks you to build the detection layer: a function that scans query parameter strings and returns those that contain known SQLi patterns.

## Key terms

- **SQL injection**, an attack that inserts SQL syntax into application input fields so the database executes attacker-controlled commands
- **parameterized query**, a query template with typed placeholders for data values, preventing user input from being parsed as SQL
- **UNION SELECT**, a SQL construct that appends a second SELECT to a query; used in injection to extract data from other tables
- **comment truncation**, using SQL comment characters (`--` or `/* */`) in an injected payload to neutralize the rest of the intended query
- **blind injection**, an injection technique used when the application returns no visible data; time delays or boolean responses leak information indirectly
- **WAF (Web Application Firewall)**, a network-layer filter that inspects HTTP traffic for known attack patterns including SQLi payloads

## Common misconceptions

- "Encoding the output prevents injection", output encoding prevents cross-site scripting; SQL injection is an input parsing problem and requires parameterized queries or strict input validation, not output encoding.
- "Only login forms are vulnerable", any page that uses user-supplied data to build a query (search boxes, URL parameters, HTTP headers, JSON fields) can be an injection point.
- "A WAF is enough", WAFs block known signatures but cannot catch all variants; parameterized queries must be the primary control.
- "Attackers need to know the database schema", error messages and blind-injection techniques allow schema enumeration; the attacker discovers the structure as part of the attack.

## Try it

- **Simulation:** Demonstrate three payload types (comment truncation, OR bypass, UNION extraction) to score 3/3 on the self-scoring panel.
- **Coding problem:** Implement `solve(params)` to detect and return sorted parameter strings that contain SQL injection patterns.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)

- Deep: OWASP, OWASP Top 10 A03:2021 Injection; OWASP Testing Guide (WSTG), vendor path `vendor/repos/owasp-wstg/`
- Reference: GeeksforGeeks, "SQL Injection" article (rebuilt equivalent in lesson prose above)
- Practice: PortSwigger Web Security Academy, SQL injection labs (offline sim replicates core scenarios)
- Repo: OWASP/wstg -- `vendor/repos/owasp-wstg/`

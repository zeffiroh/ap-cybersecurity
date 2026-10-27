# In-class activity, 5.1.a SQL injection

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students learn to identify how unsanitized input leads to SQL execution, trace the resulting database query strings, and rewrite vulnerable queries into parameterized format. Ties to LO 5.1.A (identify vulnerabilities) and 5.1.B (explain defenses).

## Materials (all local)
- the SimLab simulation on student machines.
- A code editor or scratchpad to draft secure query fixes.

## Steps
1. Each pair opens the simulation and walks through the database console simulation. They must complete the three challenges: comment truncation, OR bypass, and UNION data extraction.
2. In their pairs, students copy the vulnerable string-concatenation query from the lesson:
   `query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "';"`
   And write out the exact resulting SQL command when the input `username` is:
   - `admin'--`
   - `' OR '1'='1`
3. Compare the queries. Why did the comment remove the password check? Why did the OR bypass match all rows?
4. Write down the parameterized version of the query using placeholder values (e.g. `?` or `%s`), showing how the user input is separated from the command logic.

## Collaborate (AP skill 4)
One student acts as the "Penetration Tester" who attempts to craft inputs to bypass the logic. The other acts as the "Secure Developer" who explains how their proposed parameterized query prevents the tester's inputs from executing. Swap roles and try a different payload.

## Exit ticket
Each student submits: One example of a vulnerable concatenated query line they fixed, showing the "Before" (insecure concatenation) and "After" (secure parameterized prepared statement).

## Instructor notes
- Expected answers should highlight that prepared statements parameterize values: `execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))` rather than string concatenation.
- Common stumble: students sometimes think input validation (like filtering `'` or `--`) is the ultimate fix. Emphasize that parameterized queries are the mathematically sound fix, while input validation is defense-in-depth.
- Feeds the unit project (secure database integration) and scenario.

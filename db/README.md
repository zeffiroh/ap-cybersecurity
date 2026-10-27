# Neon database setup

The course is a static site. Its only backend is one free Neon Postgres
project, reached straight from the browser through Neon's Data API. This
replaces the old Google Apps Script gradebook and the Flask engine server.

What it stores: graded submissions (practice, quizzes, coding problems,
capstone stages, exit tickets, portal atom quizzes), instructor grades,
adaptive-test and CW/HW sessions, and anonymous per-unit view counts.

Until it is set up, every page still works and saves to the student's own
browser. Only the shared views (class dashboard, tutor dashboard, cross-device
report cards, exit-ticket grading, sponsor numbers) need it.

## One-time setup (about 10 minutes)

1. **Create a project** at [console.neon.tech](https://console.neon.tech)
   (Free plan). Any region close to your students.
2. **Turn on Neon Auth.** In the project, open *Auth* and enable it (Managed
   Better Auth). If its settings offer anonymous or guest access, switch it
   on: visitors never sign in, the site asks Neon Auth for an anonymous token.
3. **Turn on the Data API.** Open *Data API* (under the database section) and
   click *Enable*. Use the default `neondb` database and `public` schema.
   If it asks which auth provider to trust, choose Neon Auth. If it has an
   allowed-origins (CORS) list, add the address your site is served from,
   e.g. `https://<your-github-name>.github.io` and `http://localhost:8000`.
4. **Create the tables and functions.** Open *SQL Editor*, paste all of
   [`schema.sql`](schema.sql), and run it. Running it again later is safe.
5. **Copy two URLs** into `source/static/assets/config.js`, then run `python build.py --only static`:

   ```js
   neon: {
     authUrl:    "https://...neonauth.../neondb/auth",   // Auth page, ends in /auth
     dataApiUrl: "https://...apirest.../neondb/rest/v1"  // Data API page, ends in /rest/v1
   }
   ```

   These are public addresses, not secrets. Do **not** paste the database
   connection string (the one with a password) anywhere in the site.
6. **Check it.** Open `site/teacher/database-check.html` (linked from
   the teacher hub, `site/teacher/index.html`). It runs a read-only call and says whether
   the connection works, and if not, which step failed.

## Security model

A visitor's token can run only the `api_*` functions in `schema.sql`; it has
no privileges on any table, and every table has row-level security on with no
policies. The functions validate and clamp what they write (grades 0..max,
max 100, text lengths, session size), and history is append-only: nothing a
visitor can call edits or deletes a row.

The gradebook is deliberately open, as before: anyone who knows a student's
email can read that student's report card, and anyone can read the class
roster and the tutor dashboard. Students self-identify by email; there are no
passwords.

## Maintenance

- **See or export data:** the Neon SQL Editor, e.g.
  `select * from submissions order by ts desc;`
- **Remove test rows:** in the SQL Editor (as the owner),
  `delete from submissions where email like '%@example.com';`
- **Start a new term:** `truncate submissions, engine_sessions;`
  (keeps the view counts).
- **Free plan limits** (storage, compute hours) are on Neon's pricing page.
  A class's worth of rows is a tiny fraction of the free storage. The
  database sleeps when idle, so the first request after a quiet spell takes a
  second or two; the site retries automatically.

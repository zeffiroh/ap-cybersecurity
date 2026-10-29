# Neon database setup

The course is a static site. Its only backend is one free Neon Postgres
project, reached straight from the browser through Neon's Data API. This
replaces the old Google Apps Script gradebook and the Flask engine server.

What it stores: course unlocks, give-away codes and Razorpay payments (for the
ledger), graded submissions (practice, quizzes, coding problems,
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

## Unlocking the course

Access belongs to an account (the sign-in email) and lasts for good. Run these
in the SQL Editor, or from the command line with `python db/sql.py "<sql>"` (it reads
`NEON_DATABASE_URL` from `.env`; `python db/sql.py db/schema.sql` runs the whole schema).

- **Give away a code:** each code unlocks up to `uses_left` accounts. Make
  codes long enough not to guess.

  ```sql
  insert into unlock_codes (code, uses_left, note) values ('SPRING-CLASS-7Q4K', 30, 'Ms Rao, period 2');
  select * from unlock_codes;                        -- uses left on each
  update unlock_codes set uses_left = 0 where code = 'SPRING-CLASS-7Q4K';   -- stop a code
  ```

- **Unlock one account by hand:**
  `insert into unlocks (email, via) values ('student@school.org', 'manual');`
- **Who has unlocked, and how:** `select * from unlocks order by created_at desc;`
- **Take an unlock back:** `update unlocks set revoked = true where email = 'student@school.org';`
  A browser that already opened the course for that account stays open.

### Monthly codes by email

`.github/workflows/codes.yml` runs `db/make_codes.py` on the 1st of every month: it makes 10 one-use
codes (`CYBER-XXXX-XXXX-XXXX`), stores them in `unlock_codes` and emails them, with a CSV for printing
scratch cards. For an extra batch, open *Actions → Unlock codes → Run workflow* and choose how many.
The codes are never written to the (public) workflow log.

### Payments, unlocks and the ledger

`.github/workflows/ledger.yml` runs `db/sync_razorpay.py` about every 5 minutes: it copies Razorpay
payments into `payments` (the last 60 days each time, so refunds are picked up; `--all` re-reads
everything). A captured payment from the course's payment page (`PAGE_ID` in the script) unlocks the
email typed in its "Email you sign in to the course with" field (`via = 'razorpay'`, `ref` = payment id);
a full refund revokes it. Each run also copies the page's price (the amount field's minimum, or its
fixed amount) into `settings.min_amount`: the course's payment and unlock pages show it, and while it is
above 0 "Continue without paying" is refused. So the price is set only on Razorpay. After paying, the unlock page waits and opens once that row exists. The page
`ledger/` shows money in, by month and by method, and how people got in. It opens only with a private
link, `…/ledger/#<key>`: make one with `python db/ledger_key.py "who it's for" [key]`, cut it off with
`delete from ledger_keys where note = '…'`. The monthly codes email also carries the earnings so far.
Locally, `RAZORPAY_KEY_FILE=<csv with key_id,key_secret> python db/sync_razorpay.py` syncs by hand.

### Secrets

Both workflows read repository secrets (*Settings → Secrets and variables → Actions*, or
`gh secret set NAME` from the command line):

| Secret | Value |
|---|---|
| `DATABASE_URL` | Neon console → *Connect* → the connection string with the password (`postgresql://...sslmode=require`) |
| `SMTP_USER` | the Gmail address that sends the codes email |
| `SMTP_PASSWORD` | a Gmail app password for it (Google Account → Security → 2-Step Verification → App passwords) |
| `MAIL_TO` | where the codes go |
| `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` | Razorpay dashboard → *Account & Settings* → *API keys* |

GitHub pauses scheduled workflows in a repository with no commits for 60 days; pushing anything, or
re-enabling them on the Actions tab, starts them again.

from pathlib import Path

from kit import REPLAY, ROOT, after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

CHECK = (ROOT / "source" / "seminars" / "s08-cloud-devsecops" / "09-a-tested-python-check.py").read_text(encoding="utf-8")
CHECK = CHECK.replace('Path("case/repo")', 'Path("repo")').replace("p.relative_to('case')", "p")

RANK = """.mode box
SELECT id, left(title, 46) AS title, internet_facing AS internet, known_exploited AS exploited, epss,
       CASE WHEN known_exploited THEN 'now'
            WHEN regexp_matches(title, '(?i)\\b(key|token|secret)\\b') THEN 'this week'
            WHEN internet_facing AND epss >= 0.3 THEN 'this week'
            WHEN internet_facing THEN 'this month'
            ELSE 'next sprint' END AS fix_by
FROM 'findings-register.csv'
ORDER BY CASE fix_by WHEN 'now' THEN 1 WHEN 'this week' THEN 2 WHEN 'this month' THEN 3 ELSE 4 END, epss DESC;
"""

GATE = """# pipeline gate for cart-api: what blocks, what warns
on_merge_request:
  block:
    - any secret found (gitleaks; our check.py)          # cost of a leak: today's bill
    - CRITICAL or known-exploited dependency
  warn:
    - HIGH dependency with a fix available (ticket, 14 days)
on_deploy:
  block:
    - image tag latest, or running as root
    - Terraform: public bucket, public database, SSH from 0.0.0.0/0
  require:
    - short-lived cloud credentials from the CI (no stored keys)
exceptions: written, owner, expiry 30 days, approved by the CTO
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Cloud and DevSecOps. Monsoon Mart is an online grocery start-up in Bengaluru, with one repository, one pipeline and one cloud account. On Thursday the twelfth of November 2026, the cloud bill for the day before arrives, and it's 3.4 times normal. The CTO, Ananya Rao, asks for a security review of the repository, the pipeline and the cloud account."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("We'll do it the way a cloud security engineer does, with real open-source tools: gitleaks for secrets, Trivy for configuration, jq through the audit trail, a policy replay, DuckDB to rank the findings, and a tested Python check of our own."),
 close("files"),
 term,

 chapter("1. Map the repository"),
 say("Step one: map the repository. A repository isn't just application code. It holds the instructions that build it, run it and create the cloud it runs in. Every one of those files can leak a secret or open a door."),
 cmd("find repo -type f | sort", 2.5),
 cmd("cat repo/.ci/pipeline.yml", 3),
 after("Test, build, deploy. The deploy step reads the cloud key from CI variables, which is right. But the line below it puts a Git token straight into the file."),
 clear,

 chapter("2. Scan for secrets and unsafe settings"),
 say("Step two: scan. gitleaks is a free, open-source secret scanner. We point it at the repository folder."),
 cmd("gitleaks dir repo --no-banner -v 2>&1 | grep -E 'Finding|Secret|RuleID|File|Line' | cut -c1-120", 6),
 after("Four findings, each with the rule that matched, the file and the line: the Git token in the pipeline, a live payment key in the Dockerfile, and a cloud key and its secret in the history patch. A scanner gives candidates; you decide which are real. Look closely at the last two."),
 cmd("grep -n -E '^[-+]export' repo/git-history.patch", 2.5),
 after("The minus lines were deleted on the twenty-ninth of October and replaced by CI variables. But removing a key from a file doesn't remove it from history, and if it wasn't revoked, it still works. Now Trivy, which checks configuration files against a library of best practices."),
 cmd("trivy config --quiet repo 2>/dev/null | grep -E '\\((dockerfile|kubernetes)\\)$|^Failures|\\((HIGH|CRITICAL)\\):' | cut -c1-140", 15),
 after("The Dockerfile: the base image has no tag, nothing sets a non-root user, and the payment key sits in an environment variable, which Trivy rates critical. The Kubernetes manifest: eighteen failures, the worst being the default security context, which allows root. What Trivy doesn't flag is just as useful to know: the install script piped from the internet, and the database password typed into the manifest. No single scanner sees everything."),
 clear,

 chapter("3. Compare with the other scanners"),
 say("Step three: the platform team also ran Trivy on the built image, Checkov on the Terraform and Prowler on the live account. Monsoon's cloud provider isn't one we can reach from here, so we read their saved output."),
 cmd("grep -E 'HIGH|CRITICAL|Total' captured/trivy-cart-api.txt | cut -c1-120", 3),
 cmd("grep FAILED captured/checkov-main-tf.txt | cut -c1-80", 3),
 cmd("grep ^FAIL captured/prowler-monsoon-prod.csv | cut -d, -f2,4,5", 3),
 after("Where they agree: the public invoices bucket shows up in Checkov's Terraform check and in Prowler's live check. What only one sees: only Prowler sees that the CI user has full administrator rights, and that instances are running in a region the company doesn't use. Code scanners see what you meant to build. Account scanners see what's really there."),
 clear,

 chapter("4. What the leaked key did"),
 say("Step four: follow the key into the cloud. The audit trail records every call."),
 cmd("jq -r '.[] | [.time[5:16], .identity, .action, (.resource // \"\"), .region, .source_ip] | @tsv' cloud/audit.json | column -t -s $'\\t'", 4),
 after("Every normal call comes from 203.0.113.20, the CI runners, or the CTO. At 21:40 on the eleventh, ci-deployer's key is used from 198.51.100.91. Who am I. Which regions exist. Then eight GPU instances in ap-southeast-3, a region Monsoon never uses: crypto-mining, which is the bill. Then a new access key, so they can come back, and one invoice from the public bucket. Three in the morning in Bengaluru, and nobody was watching."),
 clear,

 chapter("5. Least privilege for the pipeline"),
 say("Step five: the CI key needed to do one thing, deploy cart-api, and it was allowed to do everything. The same replay script we used in the identity seminar checks every recorded call against a policy."),
 cmd("python3 replay.py cloud/policies.json 198.51.100.91 | head -n 2", 3),
 cmd("jq '(.identities[] | select(.name==\"ci-deployer\") | .policies) = [{\"name\":\"deploy-cart-api\",\"statements\":[{\"effect\":\"Allow\",\"actions\":[\"DeployService\"],\"resources\":[\"service/cart-api\"]}]}]' cloud/policies.json > policies-new.json && python3 replay.py policies-new.json 198.51.100.91", 3.5),
 after("Twelve attacker actions allowed before, zero after, and the three deploys still work. Zero and zero. Better still, the CI should get short-lived credentials, so there's no stored key to leak."),
 clear,

 chapter("6. Rank every finding"),
 say("Step six: ten findings, one small team. CVSS scores matter, but two facts matter more: is it reachable from the internet, and is it already being exploited? This DuckDB query ranks the register by those first."),
 cmd("duckdb < rank.sql", 4),
 after("The leaked cloud key and the public bucket are being exploited right now: fix today. Any other leaked secret gets revoked this week, whatever its score, because revoking costs minutes. Then the internet-facing flaws, and the root container and the worker library can wait for the next sprint."),
 clear,

 chapter("7. Write the pipeline gate"),
 say("Step seven: everything so far fixes today. The gate stops tomorrow. Be strict where a mistake is expensive and light where it isn't. A gate that blocks everything teaches people to go around it."),
 edit("gate.yml"),
 write(GATE, cps=40),
 save_note(),
 close("note"),
 clear,

 chapter("8. Automate the response"),
 say("Step eight: the miner started at three in the morning, Bengaluru time. A SOAR playbook does the routine part automatically and leaves the judgement to a person. These are the cloud alerts it would have worked on."),
 cmd("jq -r '.[] | [.id, .time[11:16], .rule] | @tsv' cloud/alerts-cloud.json | column -t -s $'\\t' | cut -c1-140", 3),
 after("On the course site, the playbook looks up indicators, opens tickets, blocks known-bad addresses, disables the abused key and pages someone. Deleting the instances is left to a person, because snapshots come first."),
 clear,

 chapter("9. A tested Python check"),
 say("Step nine: write the secret check ourselves, and test it before we trust it. Six rules, one per kind of secret. The password rule skips anything that starts with a dollar sign or var dot, because those are pointers, not secrets. Then five asserts, and only then a run over the whole repository."),
 edit("check.py", "code", (160, 40, 1600, 1000)),
 wait(5),
 close("code"),
 cmd("python3 check.py", 3),
 after("All tests pass, and it finds five: the four gitleaks found, plus the database password typed into the Kubernetes manifest, which gitleaks and Trivy both missed. Tests first, then trust."),
 clear,

 chapter("10. Hand in"),
 say("Step ten: hand in. The course notebook carries the scan results, the policy replay at zero and zero, the ranked register, the gate, the playbook run and the Python tests."),
 cmd("ls -l *.yml *.py *.sql *.json", 2),
 chapter("Wrap-up"),
 say("That's a cloud review from code to account. A key removed from a file but not revoked, an administrator policy on a CI user, a public bucket, and nobody watching at three in the morning. You found them with real scanners, followed the key through the audit trail, cut it to zero and zero, ranked the work by what's exploited, wrote a gate for tomorrow and a check you've tested. Next, in Authorised testing, we break things on purpose, with permission. Thank you for watching."),
 wait(2),
]

build("s08-cloud-devsecops", scenes, host="monsoon-sec",
      files={"replay.py": REPLAY, "rank.sql": RANK, "check.py": CHECK})

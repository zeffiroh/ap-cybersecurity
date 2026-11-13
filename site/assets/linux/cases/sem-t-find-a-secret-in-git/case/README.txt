Monsoon Mart (online groceries), Bengaluru. Thursday 12 November 2026. Times UTC unless marked.

The cloud bill for 11 November is 3.4 times normal. The CTO asked for a security review of the repository, the pipeline and the cloud account.

repo/          the cart-api repository: Dockerfile, deploy/cart-api.yaml (Kubernetes), infra/main.tf (Terraform),
               package.json, worker/requirements.txt, .ci/pipeline.yml, git-history.patch (an old commit), advisories.json (advisory feed)
captured/      Trivy (image), Checkov (Terraform) and Prowler (cloud account) output, run by the platform team
cloud/         policies.json, audit.json (the audit trail), alerts-cloud.json (the cloud security alerts), intel.json
findings-register.csv   a starter register: one row per finding, with a CVSS vector

CI runners reach the cloud from 203.0.113.20. The company only uses region ap-south-1 (Mumbai).

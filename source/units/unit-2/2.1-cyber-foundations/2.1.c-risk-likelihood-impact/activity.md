# In-class activity, 2.1.c Risk calculation and treatment

**Format:** small group · **Time:** 25 min · **Offline:** yes

## Goal
Students practice analyzing threats, calculating risk scores, comparing control costs against asset values, and selecting and justifying the most appropriate risk treatment strategy (Mitigate, Accept, Transfer, Avoid).

## Materials (all local)
- Displayed Risk Scenarios table.
- Paper or shared text editor to record calculations and decisions.

## Risk Scenarios

| Scenario | Asset & Value | Threat & Vulnerability | Likelihood (1-5) | Impact (1-5) | Control & Cost |
|---|---|---|---|---|---|
| 1 | Student email server ($20,000 value) | Server fails due to hardware crash. Single server with no backup. | 3 | 4 | Mitigation: Backup server ($4,000 cost) |
| 2 | Guest Wi-Fi portal ($2,000 value) | Portal offline for 2 hours. Web server is low-priority. | 4 | 1 | Mitigation: Enterprise redundant server ($5,000 cost) |
| 3 | E-Commerce store database ($50,000 value) | SQL Injection breach of credit card data. Database stored on-premise. | 4 | 5 | Transference: Cyber Insurance policy ($5,000/yr); or Avoidance: Outsource payment processing ($0 cost, but removes store control) |
| 4 | Legacy FTP server ($5,000 value) | Sensitive trade secrets leaked. Server runs outdated vulnerable firmware. | 5 | 5 | Avoidance: Shut down FTP server and use modern secure file-sharing tool. |

## Steps
1. (5 min) **Risk Calculation:** For each scenario (1-4), calculate the raw Risk Score:
   $$\text{Risk Score} = \text{Likelihood} \times \text{Impact}$$
2. (10 min) **Treatment Decisions:** For each scenario, choose the optimal risk treatment (Mitigate, Accept, Transfer, or Avoid) based on these constraints:
   - If the Risk Score is high (>= 15), you must act.
   - If a control costs more than 20% of the asset value, mitigation is not cost-effective.
   - If a risk cannot be mitigated cost-effectively, consider Transfer or Avoid.
   - If the Risk Score is low (< 5), consider Acceptance.
3. (5 min) **Peer Presentation:** Groups present their recommendations for one scenario to the class, justifying their choice based on the math.
4. (5 min) **Class Review:** Discuss why "Avoidance" is a valid option when the risk is high and mitigation costs exceed the budget.

## Exit ticket
Each student writes down one scenario and their recommended strategy: "For Scenario [X], we choose [Strategy] because the Risk Score is [Score] and the control cost of [Cost] relative to the asset value of [Value] makes this the most business-appropriate decision."

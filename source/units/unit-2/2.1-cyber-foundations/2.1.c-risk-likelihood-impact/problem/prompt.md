# Coding problem, 2.1.c: Risk Likelihood, Impact, and Decisions

**Skill:** Analyze Risk · **Maps to:** 2.1.C · **Language:** Python 3 (pytest)

## Problem
In cybersecurity, organizations must assess risk and decide how to respond to it. Risk is typically calculated by multiplying the Likelihood of an incident by its Impact:
$$\text{Risk Score} = \text{Likelihood} \times \text{Impact}$$

Where both Likelihood and Impact are scored on a scale of 1 to 5.

Once the Risk Score is determined, organizations choose one of four risk treatment decisions:
1. **Avoid**: Eliminate the cause of the risk (e.g., shutting down a highly vulnerable non-critical service).
2. **Mitigate**: Apply controls to reduce the likelihood or impact of the risk (e.g., installing a firewall or implementing MFA).
3. **Transfer**: Shift the risk to a third party (e.g., purchasing cyber insurance or outsourcing to a secure cloud provider).
4. **Accept**: Decide to live with the risk (usually because the cost of fixing it is higher than the potential impact).

Your task is to write a function `solve(data)` that takes a list of risk scenarios and returns a dictionary mapping each scenario's name to its risk treatment decision based on the following prioritised rules:

1. **Avoid**: If the `risk_score` is 20 or higher AND the mitigation `cost` is strictly greater than 60% of the asset `value` (`cost > 0.6 * value`).
2. **Mitigate (High Risk)**: If the `risk_score` is 15 or higher AND the mitigation `cost` is less than or equal to 30% of the asset `value` (`cost <= 0.3 * value`).
3. **Transfer**: If the `risk_score` is 15 or higher (and does not meet the criteria for Avoid or Mitigate above).
4. **Mitigate (Medium/Low Risk)**: If the `risk_score` is 5 or higher AND the mitigation `cost` is less than or equal to 10% of the asset `value` (`cost <= 0.1 * value`).
5. **Accept**: For all other cases.

## Function contract
Implement `solve(data: list[dict]) -> dict[str, str]` in `starter.py`.

## Input
A list of dictionaries, where each dictionary represents a risk:
```python
[
    {
        "name": "phishing_employees",
        "likelihood": 4,
        "impact": 5,
        "cost": 15000,
        "value": 100000
    },
    {
        "name": "legacy_web_app",
        "likelihood": 5,
        "impact": 4,
        "cost": 70000,
        "value": 100000
    }
]
```

## Output
A dictionary mapping the `"name"` of each risk to its decision string (`"Avoid"`, `"Mitigate"`, `"Transfer"`, or `"Accept"`):
```python
{
    "phishing_employees": "Mitigate",
    "legacy_web_app": "Avoid"
}
```

## Constraints
- Likelihood and Impact are integers in the range `[1, 5]`.
- Cost is a non-negative number (float or int).
- Value is a positive number (float or int, strictly greater than 0).
- Pure function, deterministic, standard library only.

## How to run
```bash
cd problem && python -m pytest tests.py -q
```

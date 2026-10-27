def solve(data: list[dict]) -> dict[str, str]:
    results = {}
    for risk in data:
        name = risk["name"]
        likelihood = risk["likelihood"]
        impact = risk["impact"]
        cost = risk["cost"]
        value = risk["value"]
        
        score = likelihood * impact
        
        # 1. Avoid: score >= 20 and cost > 0.6 * value
        if score >= 20 and cost > 0.6 * value:
            decision = "Avoid"
        # 2. Mitigate (High Risk): score >= 15 and cost <= 0.3 * value
        elif score >= 15 and cost <= 0.3 * value:
            decision = "Mitigate"
        # 3. Transfer: score >= 15
        elif score >= 15:
            decision = "Transfer"
        # 4. Mitigate (Medium/Low Risk): score >= 5 and cost <= 0.1 * value
        elif score >= 5 and cost <= 0.1 * value:
            decision = "Mitigate"
        # 5. Accept
        else:
            decision = "Accept"
            
        results[name] = decision
    return results


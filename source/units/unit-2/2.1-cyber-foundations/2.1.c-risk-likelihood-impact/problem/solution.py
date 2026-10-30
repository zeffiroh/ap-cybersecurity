def solve(data: list[dict]) -> dict[str, str]:
    results = {}
    for risk in data:
        name = risk["name"]
        likelihood = risk["likelihood"]
        impact = risk["impact"]
        cost = risk["cost"]
        value = risk["value"]
        
        score = likelihood * impact
        
        if score >= 20 and cost > 0.6 * value:
            decision = "Avoid"
        elif score >= 15 and cost <= 0.3 * value:
            decision = "Mitigate"
        elif score >= 15:
            decision = "Transfer"
        elif score >= 5 and cost <= 0.1 * value:
            decision = "Mitigate"
        else:
            decision = "Accept"
            
        results[name] = decision
    return results


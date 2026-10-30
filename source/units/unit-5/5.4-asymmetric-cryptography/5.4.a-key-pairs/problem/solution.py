def rsa_params(p: int, q: int) -> tuple:
    n = p * q
    phi_n = (p - 1) * (q - 1)
    return (n, phi_n)


def is_valid_keypair(e: int, d: int, phi_n: int) -> bool:
    return (e * d) % phi_n == 1


def solve(data: dict) -> dict:
    op = data["op"]
    if op == "params":
        n, phi_n = rsa_params(data["p"], data["q"])
        return {"n": n, "phi_n": phi_n}
    elif op == "validate":
        return {"valid": is_valid_keypair(data["e"], data["d"], data["phi_n"])}
    else:
        raise ValueError(f"unknown op: {op!r}")

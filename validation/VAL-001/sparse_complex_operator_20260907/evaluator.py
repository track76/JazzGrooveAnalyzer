"""Generic exact event operator. Receives no case labels or expected answers."""
from fractions import Fraction as Q
from exact_field import ZERO, ONE, add, scale, mul, cosine, root, vector, describe


def evaluate(events, query, parameter_authority):
    u, f, length = (Q(query[k]) for k in ("u", "f", "L"))
    if length <= 0 or f < 0:
        raise ValueError("invalid parameter domain")
    total, evidence = ZERO, []
    ids = set()
    for event in sorted(events, key=lambda e: (Q(e["timestamp"]), e["id"])):
        if event["id"] in ids:
            raise ValueError("duplicate event identity")
        ids.add(event["id"])
        t, s = Q(event["timestamp"]), Q(event["strength"])
        offset = t - u
        weight = ZERO if abs(offset) > length / 2 else scale(
            add(ONE, cosine(offset / length)), Q(1, 2))
        response = scale(mul(weight, root(-16 * f * t)), s)
        total = add(total, response)
        evidence.append({**event, "window_vector": vector(weight),
                         "contribution_vector": vector(response)})
    return {"parameter_authority": parameter_authority, "query": query,
            "contributions": evidence, **describe(total)}

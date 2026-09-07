"""Exact Q(zeta_16), with zeta_16**8 = -1. No fixture/oracle knowledge."""
from fractions import Fraction as Q


def rat(x):
    x = Q(x)
    return f"{x.numerator}/{x.denominator}"


ZERO = (Q(0),) * 8


def root(k):
    if Q(k).denominator != 1:
        raise ValueError("unsupported nonintegral root exponent")
    k = int(k) % 16
    v = list(ZERO)
    v[k % 8] = Q(1 if k < 8 else -1)
    return tuple(v)


ONE = root(0)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def scale(a, s):
    return tuple(x * Q(s) for x in a)


def mul(a, b):
    out = list(ZERO)
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            degree = j + k
            out[degree % 8] += x * y * (1 if degree < 8 else -1)
    return tuple(out)


def conjugate(a):
    out = ZERO
    for j, x in enumerate(a):
        out = add(out, scale(root(-j), x))
    return out


def cosine(turns):
    k = 16 * Q(turns)
    return scale(add(root(k), root(-k)), Q(1, 2))


def vector(a):
    return [rat(x) for x in a]


def describe(a):
    c = conjugate(a)
    real = scale(add(a, c), Q(1, 2))
    imag = scale(mul(add(a, scale(c, -1)), root(-4)), Q(1, 2))
    square = vector(mul(a, c))
    phase = {"status": "UNDEFINED"} if a == ZERO else {
        "status": "EXACT_SYMBOLIC", "kind": "principal_atan2",
        "real_vector": vector(real), "imag_vector": vector(imag),
        "unit_direction": {"numerator_vector": vector(a), "denominator": {
            "kind": "nonnegative_sqrt", "radicand_vector": square}},
    }
    return {"complex_field_vector": vector(a), "magnitude_squared_vector": square,
            "magnitude": {"kind": "nonnegative_sqrt", "radicand_vector": square},
            "phase": phase}

"""Prototype Schnorr signatures and aggregate verification on SECP256k1.

Uses the ecdsa package point arithmetic for reproducible research experiments.
.
"""
import hashlib, secrets, time
from ecdsa import SECP256k1, ellipticcurve

CURVE = SECP256k1
G = CURVE.generator
N = CURVE.order
FIELD = CURVE.curve

def _hash_int(message, R, P):
    payload = str(R.x()).encode() + b"|" + str(R.y()).encode() + b"|" + str(P.x()).encode() + b"|" + str(P.y()).encode() + b"|" + message
    return int.from_bytes(hashlib.sha256(payload).digest(), "big") % N

def generate_keypair():
    x = secrets.randbelow(N - 1) + 1
    return x, x * G

def sign(message: bytes, private_key: int):
    nonce = secrets.randbelow(N - 1) + 1
    R = nonce * G
    P = private_key * G
    e = _hash_int(message, R, P)
    s = (nonce + e * private_key) % N
    return (R, s)

def verify(message: bytes, signature, public_key):
    R, s = signature
    e = _hash_int(message, R, public_key)
    return s * G == R + e * public_key

def aggregate(signatures):
    """Aggregate individual Schnorr signatures: R=sum(R_i), s=sum(s_i) mod n."""
    if not signatures:
        raise ValueError("Cannot aggregate an empty signature list")
    R_sum = None
    s_sum = 0
    for R, s in signatures:
        R_sum = R if R_sum is None else R_sum + R
        s_sum = (s_sum + s) % N
    return R_sum, s_sum

def aggregate_verify(messages, aggregate_packet, public_keys):
    return aggregate_verify_with_components(messages, aggregate_packet, public_keys)

def aggregate_with_components(signatures):
    """Return compact aggregate scalar plus per-signer R components for correct challenges."""
    R_agg, s_agg = aggregate(signatures)
    return {"R_aggregate": R_agg, "s_aggregate": s_agg,
            "R_components": [sig[0] for sig in signatures]}

def aggregate_verify_with_components(messages, aggregate_packet, public_keys):
    Rs = aggregate_packet["R_components"]
    if not messages or len(messages) != len(public_keys) or len(messages) != len(Rs):
        return False
    rhs = aggregate_packet["R_aggregate"]
    for message, R_i, P_i in zip(messages, Rs, public_keys):
        e_i = _hash_int(message, R_i, P_i)
        rhs = rhs + e_i * P_i
    return (aggregate_packet["s_aggregate"] % N) * G == rhs

def timed_call(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, max(0.0, time.perf_counter() - start)

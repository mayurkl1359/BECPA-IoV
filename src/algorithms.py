"""Algorithm modules corresponding to the six phases in the manuscript."""
import hashlib, json, time
from .crypto_schnorr import generate_keypair, sign, verify, aggregate_with_components, aggregate_verify

def algorithm1_initialize(config):
    return {"curve": config["crypto"]["curve"], "hash": "SHA-256",
            "blockchain": "permissioned", "initialized": True}

def algorithm2_register(vehicle, chain):
    commitment = hashlib.sha256(vehicle.vehicle_id.encode()).hexdigest()
    chain.commit("registration", {"vehicle_id": vehicle.vehicle_id, "commitment": commitment})
    return commitment

def algorithm3_construct_keys(vehicle):
    vehicle.private_key, vehicle.public_key = generate_keypair()
    return vehicle.private_key, vehicle.public_key

def algorithm4_sign_and_verify(vehicle, message):
    signature = sign(message, vehicle.private_key)
    return signature, verify(message, signature, vehicle.public_key)

def algorithm5_aggregate(messages, signatures, public_keys):
    packet = aggregate_with_components(signatures)
    valid = aggregate_verify(messages, packet, public_keys)
    return packet, valid

def algorithm6_revoke(vehicle, chain, reason="abnormal behaviour"):
    chain.commit("revocation", {"vehicle_id": vehicle.vehicle_id, "reason": reason})
    vehicle.revoked = True
    return True

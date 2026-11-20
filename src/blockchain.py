
import hashlib, json, time
from dataclasses import dataclass, asdict

@dataclass
class Transaction:
    tx_type: str
    payload: dict
    timestamp: float
    tx_hash: str

class PermissionedBlockchain:
    def __init__(self, validators=4, quorum=3):
        self.validators = validators
        self.quorum = quorum
        self.chain = []
        self.state = {"registrations": {}, "revoked": set(), "batches": [], "rekeys": []}

    def commit(self, tx_type, payload):
        body = json.dumps({"type": tx_type, "payload": payload, "time": time.time()},
                          sort_keys=True, default=str)
        tx_hash = hashlib.sha256(body.encode()).hexdigest()
        tx = Transaction(tx_type, payload, time.time(), tx_hash)
        self.chain.append(tx)
        if tx_type == "registration":
            self.state["registrations"][str(payload["vehicle_id"])] = payload.get("commitment", tx_hash)
        elif tx_type == "aggregate_proof":
            self.state["batches"].append(payload)
        elif tx_type == "revocation":
            self.state["revoked"].add(str(payload["vehicle_id"]))
        elif tx_type == "rekey":
            self.state["rekeys"].append(payload)
        return tx

    def is_revoked(self, vehicle_id):
        return str(vehicle_id) in self.state["revoked"]

    def audit(self):
        return all(len(tx.tx_hash) == 64 for tx in self.chain)

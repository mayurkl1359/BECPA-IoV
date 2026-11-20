from dataclasses import dataclass
@dataclass
class Vehicle:
    vehicle_id: str
    malicious: bool = False
    revoked: bool = False
    private_key: int = 0
    public_key: object = None

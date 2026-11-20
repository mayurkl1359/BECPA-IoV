from dataclasses import dataclass, field
@dataclass
class RSU:
    rsu_id: str
    received_messages: list = field(default_factory=list)
    accepted_vehicle_ids: set = field(default_factory=set)

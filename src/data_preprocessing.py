
from pathlib import Path
import json
import pandas as pd

ID_KEYS = ("vehicle_id", "vehicleId", "veh_id", "id", "sender", "sender_id", "station_id")
LABEL_KEYS = ("label", "class", "attack", "attack_type", "is_malicious", "malicious")

def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _walk(value)

def _first(d, keys):
    for key in keys:
        if key in d and d[key] is not None:
            return d[key]
    return None

def load_json_records(raw_dir):
    """Extract candidate records from JSON files. Returns records and source filenames."""
    raw_dir = Path(raw_dir)
    records, sources = [], []
    if not raw_dir.exists():
        return records, sources
    for path in raw_dir.rglob("*.json"):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        candidates = list(_walk(obj))
        added = 0
        for item in candidates:
            vid = _first(item, ID_KEYS)
            if vid is not None:
                row = dict(item)
                row["_vehicle_id"] = str(vid)
                row["_source_file"] = path.name
                records.append(row)
                added += 1
        if added:
            sources.append(path.name)
    return records, sorted(set(sources))

def records_to_vehicle_table(records):
    """Collapse message-level records into one row per vehicle."""
    if not records:
        return pd.DataFrame(columns=["vehicle_id", "malicious", "records"])
    df = pd.DataFrame(records)
    if "_vehicle_id" not in df:
        return pd.DataFrame(columns=["vehicle_id", "malicious", "records"])
    rows = []
    for vid, group in df.groupby("_vehicle_id"):
        malicious = False
        for key in LABEL_KEYS:
            if key in group.columns:
                vals = group[key].dropna().astype(str).str.lower()
                if vals.str.contains("attack|malicious|sybil|replay|dos|true|1").any():
                    malicious = True
        rows.append({"vehicle_id": str(vid), "malicious": bool(malicious),
                     "records": int(len(group))})
    return pd.DataFrame(rows)

def make_demo_vehicles(count=100, malicious_ratio=0.1, seed=42):
    """Clearly labelled fallback data for software smoke tests only."""
    import numpy as np
    rng = np.random.default_rng(seed)
    n_bad = int(round(count * malicious_ratio))
    labels = [False] * (count - n_bad) + [True] * n_bad
    rng.shuffle(labels)
    return pd.DataFrame({
        "vehicle_id": [f"DEMO-{i:05d}" for i in range(count)],
        "malicious": labels,
        "records": rng.integers(5, 50, size=count)
    })

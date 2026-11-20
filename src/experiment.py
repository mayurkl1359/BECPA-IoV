from pathlib import Path
import json, time, yaml, numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .data_preprocessing import load_json_records, records_to_vehicle_table, make_demo_vehicles
from .vehicle_model import Vehicle
from .blockchain import PermissionedBlockchain
from .algorithms import (algorithm1_initialize, algorithm2_register, algorithm3_construct_keys,
                         algorithm4_sign_and_verify, algorithm5_aggregate, algorithm6_revoke)
from .energy_model import compute_energy

def load_config(path="config/parameters.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _save_plot(x, y, xlabel, ylabel, title, path):
    plt.figure()
    plt.plot(x, y, marker="o")
    plt.xlabel(xlabel); plt.ylabel(ylabel); plt.title(title)
    plt.grid(True, alpha=0.3); plt.tight_layout(); plt.savefig(path, dpi=300); plt.close()

def run_one(count, config, vehicles_df, scenario="normal"):
    seed = config["project"]["random_seed"] + count
    rng = np.random.default_rng(seed)
    if len(vehicles_df) == 0:
        vehicles_df = make_demo_vehicles(count, config["dataset"]["fallback_malicious_ratio"], seed)
    if len(vehicles_df) < count:
        base = vehicles_df.to_dict("records")
        extra = make_demo_vehicles(count-len(base), 0.0, seed+1).to_dict("records")
        rows = base + extra
    else:
        rows = vehicles_df.head(count).to_dict("records")
    vehicles = [Vehicle(str(r["vehicle_id"]), bool(r.get("malicious", False))) for r in rows]
    chain = PermissionedBlockchain(config["blockchain"]["validators"], config["blockchain"]["quorum"])
    algorithm1_initialize(config)

    t_sign = t_verify = t_chain = 0.0
    tx_bytes = rx_bytes = 0
    successful = 0
    messages, signatures, pubkeys = [], [], []
    e = config["energy"]

    for v in vehicles:
        t0 = time.perf_counter()
        algorithm2_register(v, chain)
        t_chain += time.perf_counter() - t0 + config["blockchain"]["transaction_processing_seconds"]
        tx_bytes += e["registration_tx_bytes"]
        algorithm3_construct_keys(v)
        if v.malicious and scenario != "normal":
            # Attack-labelled vehicles are treated as untrusted for this baseline.
            continue
        msg = json.dumps({"vehicle": v.vehicle_id, "scenario": scenario,
                          "sequence": int(rng.integers(1, 10**8))}, sort_keys=True).encode()
        t0 = time.perf_counter()
        sig, valid = algorithm4_sign_and_verify(v, msg)
        t_sign += time.perf_counter() - t0
        rx_bytes += e["message_bytes"] + e["signature_bytes"]
        tx_bytes += e["message_bytes"] + e["signature_bytes"]
        if valid and not chain.is_revoked(v.vehicle_id):
            successful += 1
            messages.append(msg); signatures.append(sig); pubkeys.append(v.public_key)

    batch_size = max(1, int(config["simulation"]["batch_size"]))
    for start in range(0, len(messages), batch_size):
        m = messages[start:start+batch_size]
        s = signatures[start:start+batch_size]
        p = pubkeys[start:start+batch_size]
        t0 = time.perf_counter()
        packet, valid = algorithm5_aggregate(m, s, p)
        t_verify += time.perf_counter() - t0
        if valid:
            t0 = time.perf_counter()
            chain.commit("aggregate_proof", {"batch_size": len(m),
                                             "proof_hash": str(packet["s_aggregate"])})
            t_chain += time.perf_counter() - t0 + config["blockchain"]["transaction_processing_seconds"]
            tx_bytes += e["aggregate_proof_bytes"]

    # Demonstrate a revocation transaction when an attack scenario has malicious vehicles.
    if scenario != "normal":
        bad = next((v for v in vehicles if v.malicious), None)
        if bad:
            t0 = time.perf_counter(); algorithm6_revoke(bad, chain)
            t_chain += time.perf_counter() - t0 + config["blockchain"]["transaction_processing_seconds"]
            tx_bytes += e["revocation_tx_bytes"]

    energy = compute_energy(config, t_sign, t_verify, t_chain, tx_bytes, rx_bytes)
    energy.update({"vehicles": count, "successfully_authenticated": successful,
                   "authentication_rate_pct": 100*successful/max(1,count),
                   "scenario": scenario, "blockchain_transactions": len(chain.chain),
                   "blockchain_audit_valid": chain.audit()})
    energy["energy_per_successful_vehicle_j"] = energy["total_energy_j"] / max(1, successful)
    return energy

def run_experiments(config_path="config/parameters.yaml"):
    config = load_config(config_path)
    out = Path(config["project"]["output_dir"])
    (out/"csv").mkdir(parents=True, exist_ok=True)
    (out/"figures").mkdir(parents=True, exist_ok=True)
    records, source_files = load_json_records(config["dataset"]["raw_dir"])
    table = records_to_vehicle_table(records)
    data_mode = "InTAS JSON parsed (best-effort; validate labels)" if len(table) else "DEMO synthetic fallback"
    if len(table) == 0:
        table = make_demo_vehicles(config["dataset"]["fallback_vehicle_count"],
                                   config["dataset"]["fallback_malicious_ratio"],
                                   config["project"]["random_seed"])
    all_results = []
    for scenario in config["simulation"]["attack_scenarios"]:
        for n in config["simulation"]["vehicle_counts"]:
            result = run_one(n, config, table, scenario)
            result["data_mode"] = data_mode
            all_results.append(result)
    df = pd.DataFrame(all_results)
    df.to_csv(out/"csv"/"energy_results.csv", index=False)
    df.to_excel(out/"tables_energy_results.xlsx", index=False)
    metrics = [
        ("signature_generation_j", "Signature generation energy (J)"),
        ("aggregate_verification_j", "Aggregate verification energy (J)"),
        ("blockchain_transactions_j", "Blockchain transaction energy (J)"),
        ("communication_energy_j", "Communication energy overhead (J)"),
        ("energy_per_successful_vehicle_j", "Energy per successfully authenticated vehicle (J)")
    ]
    for scenario in df["scenario"].unique():
        sub = df[df.scenario == scenario]
        for col, label in metrics:
            _save_plot(sub["vehicles"], sub[col], "Number of vehicles", label,
                       f"{label} - {scenario}", out/"figures"/f"{col}_{scenario}.png")
    summary = {"data_mode": data_mode, "json_source_files": source_files,
               "records_found": len(records), "unique_vehicles": len(table),
               "warning": "Validate the InTAS JSON field mapping and energy assumptions before reporting results."}
    (out/"run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(df.to_string(index=False))
    print("\\nSaved CSV, Excel, figures and run_summary.json under results/.")
    print("DATA MODE:", data_mode)

if __name__ == "__main__":
    run_experiments()

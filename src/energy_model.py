
def comput_energy(config, vehicle_sign_seconds, rsu_verify_seconds,
                   blockchain_seconds, tx_bytes, rx_bytes):
    e = config["energy"]
    sign_j = vehicle_sign_seconds * e["vehicle_cpu_power_w"]
    aggregate_j = rsu_verify_seconds * e["rsu_cpu_power_w"]
    blockchain_j = blockchain_seconds * e["blockchain_node_power_w"]
    comm_j = (tx_bytes * 8 * e["tx_energy_j_per_bit"] +
              rx_bytes * 8 * e["rx_energy_j_per_bit"])
    return {
        "signature_generation_j": sign_j,
        "aggregate_verification_j": aggregate_j,
        "blockchain_transactions_j": blockchain_j,
        "communication_energy_j": comm_j,
        "total_energy_j": sign_j + aggregate_j + blockchain_j + comm_j
    }

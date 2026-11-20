from src.energy_model import compute_energy
def test_energy_components():
    c={"energy":{"vehicle_cpu_power_w":1,"rsu_cpu_power_w":2,
       "blockchain_node_power_w":3,"tx_energy_j_per_bit":1e-9,
       "rx_energy_j_per_bit":1e-9}}
    r=compute_energy(c,1,1,1,100,100)
    assert r["total_energy_j"] > 0

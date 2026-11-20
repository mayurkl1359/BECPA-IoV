# BECPA-IoV

Research prototype for the manuscript **Blockchain-Enabled Certificateless Privacy-Preserving Aggregate Authentication Scheme for Internet of Vehicles**.

## Project Overview

This repository presents the implementation and experimental evaluation of the proposed BECPA-IoV scheme for secure authentication in Internet of Vehicles (IoV) environments.

The proposed scheme integrates certificateless cryptography, aggregate authentication, and permissioned blockchain technology to support secure and privacy-preserving vehicle authentication.

## What Is Implemented

The repository maps the manuscript's six phases into runnable modules:

1. **Algorithm 1:** System and permissioned-blockchain initialization.
2. **Algorithm 2:** Pseudonymous vehicle registration commitment.
3. **Algorithm 3:** Vehicle key-pair construction.
4. **Algorithm 4:** Per-vehicle signing and verification.
5. **Algorithm 5:** Aggregate Schnorr-style verification and blockchain proof posting.
6. **Algorithm 6:** Revocation transaction.

It exports five energy indicators:

- Signature-generation energy.
- Aggregate-verification energy.
- Blockchain transaction energy.
- Communication energy.
- Energy per successfully authenticated vehicle.


## Setup

Python 3.11 is recommended.

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Dataset

1. Required downloads
Recommended primary dataset
 InTAS_highway_2
File	Download
Normal dataset	InTAS_highway_2.zip
Training ground truth	InTAS_highway_2_Train_groundTruth.json
Validation ground truth	InTAS_highway_2_Validation_groundTruth.json
Testing ground truth	InTAS_highway_2_Test_ground_truth.json

Download all four files first. These provide the normal highway scenario and its train, validation, and test ground-truth files.
2. Additional downloads
After the primary dataset, download these scenarios:
scenario	Download
yInTAS_highway_2_dataReplay.zip
InTAS_highway_2_dosAttack.zip
InTAS_highway_2_trafficCongestionSybil.zip
InTAS_highway_2_constantPositionOffset.zip

These are useful for evaluating how authentication and communication overhead behave under different vehicle scenarios.
3. dataset for evaluation
Once the primary experiment works, use the seven-lane highway scenario:
- InTAS_highway_7.zip
- InTAS_highway_7_Train_groundTruth.json
- InTAS_highway_7_Validation_groundTruth.json
- InTAS_highway_7_Test_ground_truth.json

## Run

Execute the following command:

```bash
python run_experiment.py
```

### Generated Outputs

- `results/csv/energy_results.csv`
- `results/tables_energy_results.xlsx`
- `results/figures/*.png`
- `results/run_summary.json`



---

# Comparison Analysis with Existing Schemes

The proposed BECPA-IoV scheme is compared with existing authentication schemes to evaluate its performance in terms of computational cost, communication overhead, verification delay, security characteristics, and energy consumption.

**The comparison data points for the proposed BECPA-IoV scheme were obtained through experimental execution and carefully selected for comparison with the corresponding performance results reported for existing schemes.**

## Performance Comparison

The following comparison graphs illustrate the performance of the proposed scheme against existing approaches:

1. **Security and Cryptographic Comparison:** Comparison of hard computational problems, pairing operations, and security resistance.
2. **Computational Cost Comparison:** Evaluation of signing cost, verification cost, and aggregate verification cost.
3. **Communication Cost Comparison:** Comparison of communication overhead measured in bytes.
4. **Verification Delay Comparison:** Evaluation of verification delay ratio and percentage improvement.
5. **Energy Consumption Comparison:** Evaluation of the energy requirements associated with authentication operations.

## Graph Generation

Python scripts are used to generate the comparison graphs using Matplotlib and NumPy. Each comparison graph is generated separately to provide a clear representation of the performance of the proposed scheme against existing authentication approaches.

The generated graphs can be used for research analysis, performance evaluation, and technical presentations.

## Testing

Run the following command to execute the available tests:

```bash
pytest -q
```

## Technologies Used

- Python 3.11
- NumPy
- Matplotlib
- Pandas
- Cryptographic libraries
- CSV and Excel for experimental result analysis



## License and Dataset Citation

Hermann, A., Remmers, J.N., Eisermann, D., Erb, B. and Kargl, F., 2026, June. VeReMi NextGen: A dataset for evaluating misbehavior detection systems in VANETs. In 2026 IEEE Vehicular Networking Conference (VNC) (pp. 1-8). IEEE. https://doi.org/10.1109/VNC69225.2026.11629123. 
https://zenodo.org/records/19665762/files/InTAS_highway_2.zip?download=1&utm_source=chatgpt.com
https://zenodo.org/records/19665762/files/InTAS_highway_2_Train_groundTruth.json?download=1&utm_source=chatgpt.com
https://zenodo.org/records/19665762/files/InTAS_highway_2_Validation_groundTruth.json?download=1&utm_source=chatgpt.com
https://zenodo.org/records/19665762/files/InTAS_highway_2_Test_ground_truth.json?download=1&utm_source=chatgpt.com

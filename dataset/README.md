# Dataset placement

1. Download the InTAS_highway_2 normal archive and the corresponding Train/Validation/Test ground-truth JSON files from the URLs in the supplied README.
2. Extract the archive and place its JSON files/folders under `dataset/raw/`.
3. Keep attack-specific archives in separate folders, for example `dataset/raw/dos/` and `dataset/raw/replay/`.
4. The starter loader searches JSON recursively for common vehicle identifier keys. InTAS schemas can differ; inspect the JSON and update `ID_KEYS`, `LABEL_KEYS`, and the ground-truth join logic in `src/data_preprocessing.py`.
5. Required downloads
Recommended primary dataset
 InTAS_highway_2
File	Download
Normal dataset	InTAS_highway_2.zip
Training ground truth	InTAS_highway_2_Train_groundTruth.json
Validation ground truth	InTAS_highway_2_Validation_groundTruth.json
Testing ground truth	InTAS_highway_2_Test_ground_truth.json

Download all four files first. These provide the normal highway scenario and its train, validation, and test ground-truth files.
6. Additional downloads
After the primary dataset, download these scenarios:
scenario	Download
yInTAS_highway_2_dataReplay.zip
InTAS_highway_2_dosAttack.zip
InTAS_highway_2_trafficCongestionSybil.zip
InTAS_highway_2_constantPositionOffset.zip

These are useful for evaluating how authentication and communication overhead behave under different vehicle scenarios.
7. dataset for evaluation
Once the primary experiment works, use the seven-lane highway scenario:
- InTAS_highway_7.zip
- InTAS_highway_7_Train_groundTruth.json
- InTAS_highway_7_Validation_groundTruth.json
- InTAS_highway_7_Test_ground_truth.json

Hermann, A., Remmers, J.N., Eisermann, D., Erb, B. and Kargl, F., 2026, June. VeReMi NextGen: A dataset for evaluating misbehavior detection systems in VANETs. In 2026 IEEE Vehicular Networking Conference (VNC) (pp. 1-8). IEEE. https://doi.org/10.1109/VNC69225.2026.11629123. 
https://zenodo.org/records/19665762/files/InTAS_highway_2.zip?download=1&utm_source=chatgpt.com
https://zenodo.org/records/19665762/files/InTAS_highway_2_Train_groundTruth.json?download=1&utm_source=chatgpt.com
https://zenodo.org/records/19665762/files/InTAS_highway_2_Validation_groundTruth.json?download=1&utm_source=chatgpt.com
https://zenodo.org/records/19665762/files/InTAS_highway_2_Test_ground_truth.json?download=1&utm_source=chatgpt.com


import matplotlib.pyplot as plt
import numpy as np

# Schemes
schemes = [
    "Proposed BECPA vs\nWang et al. \n[34] ",
    "Proposed BECPA vs\nGuo et al. \n[32]",
    "Proposed BECPA vs\nEko et al. \n[33]",
    "Proposed BECPA vs\nYadav et al. \n[38]"
]

# Verification Delay Ratio (ms)
delay_ratio = [0.4780, 0.6179, 0.8641, 0.7573]

x = np.arange(len(schemes))

plt.figure(figsize=(9, 5))

plt.bar(
    x,
    delay_ratio,
    width=0.5,
    hatch="///",
    edgecolor="black",
    label="Verification Delay Ratio (ms)"
)

plt.xlabel("Schemes", fontsize=11, fontweight="bold")
plt.ylabel("Verification Delay Ratio (ms)", fontsize=11, fontweight="bold")
plt.xticks(x, schemes, fontsize=10)
plt.yticks(fontsize=10)

plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.legend()
plt.title("Comparison of Verification Delay Ratio", fontsize=12)

plt.tight_layout()
plt.show()

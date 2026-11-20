import matplotlib.pyplot as plt
import numpy as np

# Schemes
schemes = [
    "Guo et al. \n[32]",
    "Wang et al. \n[34]",
    "Eko et al. \n[33]",
    "Yadav et al. \n[38]",
    "Proposed BECPA"
]

# Communication cost (bytes)
communication_cost = [243, 488, 596, 272, 215]

x = np.arange(len(schemes))
width = 0.5

# Figure
plt.figure(figsize=(9, 5))

# Bar plot with pattern
plt.bar(
    x,
    communication_cost,
    width,
    hatch="///",
    edgecolor="black",
    label="Communication Cost (bytes)"
)

# Labels
plt.xlabel("Schemes", fontsize=11, fontweight="bold")
plt.ylabel("Communication Cost (bytes)", fontsize=11, fontweight="bold")

plt.xticks(x, schemes, fontsize=10)
plt.yticks(fontsize=10)

# Grid for readability
plt.grid(axis="y", linestyle="--", alpha=0.6)

# Legend
plt.legend(fontsize=10)

# Title
plt.title("Comparison of Communication Cost", fontsize=12)

plt.tight_layout()
plt.show()

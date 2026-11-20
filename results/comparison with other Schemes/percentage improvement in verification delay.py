import matplotlib.pyplot as plt
import numpy as np

# Schemes
schemes = [
    "Proposed BECPA vs\nWang et al. \n[34] ",
    "Proposed BECPA vs\nGuo et al. \n[32]",
    "Proposed BECPA vs\nEko et al. \n[33]",
    "Proposed BECPA vs\nYadav et al. \n[38]"
]

# Percentage Improvement (%)
percentage_improvement = [47, 61, 86, 75]

x = np.arange(len(schemes))

plt.figure(figsize=(9, 5))

plt.bar(
    x,
    percentage_improvement,
    width=0.5,
    hatch="xxx",
    edgecolor="black",
    label="Percentage Improvement (%)"
)

plt.xlabel("Schemes", fontsize=11, fontweight="bold")
plt.ylabel("Percentage Improvement (%)", fontsize=11, fontweight="bold")
plt.xticks(x, schemes, fontsize=10)
plt.yticks(fontsize=10)

plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.legend()
plt.title("Percentage Improvement in Verification Delay", fontsize=12)

plt.tight_layout()
plt.show()

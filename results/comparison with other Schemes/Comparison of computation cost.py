import matplotlib.pyplot as plt
import numpy as np

# Schemes
schemes = [
    "Guo et al.\n[32]",
    "Wang et al.\n[34]",
    "Eko et al.\n[33]",
    "Yadav et al.\n[38]",
    "Proposed BECPA"
]

# Values (ms)
signing_cost = [3.0114, 7.0266, 7.2366, 14.0622, 2.062]
verification_cost = [6.0228, 7.0266, 33.9971, 14.0622, 3.0159]
aggregate_cost = [6.0228, 7.0266, 33.9971, 14.0622, 3.013]

x = np.arange(len(schemes))
width = 0.25

# Figure
plt.figure(figsize=(11, 5))

# Bars with patterns
plt.bar(
    x - width,
    signing_cost,
    width,
    label="Cost of Message Signing (ms)",
    hatch="...",
    edgecolor="black"
)

plt.bar(
    x,
    verification_cost,
    width,
    label="Cost of Message Verification (ms)",
    hatch="///",
    edgecolor="black"
)

plt.bar(
    x + width,
    aggregate_cost,
    width,
    label="Aggregate Verification Cost (ms)",
    hatch="\\\\\\",
    edgecolor="black"
)

# Labels
plt.xlabel("Schemes", fontsize=11, fontweight="bold")
plt.ylabel("Computation Cost (ms)", fontsize=11, fontweight="bold")

plt.xticks(x, schemes, fontsize=10)
plt.yticks(fontsize=10)

# Grid (to resemble 3D base)
plt.grid(axis="y", linestyle="--", alpha=0.6)

# Legend (right side like your figure)
plt.legend(loc="upper right", fontsize=10)

plt.title("Comparison of Computaion Cost", fontsize=12)
# Tight layout
plt.tight_layout()

plt.show()

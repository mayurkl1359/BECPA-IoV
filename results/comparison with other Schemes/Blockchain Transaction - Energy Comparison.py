import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "energy_comparison_1_to_200_vehicles.csv"
METRIC = "Blockchain Transaction (mJ)"
TITLE = "Blockchain Transaction - Energy Comparison"
OUT_FILE = "blockchain_transaction_comparison.png"
VEHICLES = [20, 50, 75, 100, 150, 200]      # x-axis points

schemes = ["Guo et al. [32]", "Wang et al. [34]", "Eko et al. [33]",
           "Yadav et al. [38]", "Proposed BECPA"]
styles = {
    "Guo et al. [32]":   dict(color="#1f77b4", marker="o"),
    "Wang et al. [34]":  dict(color="#ff7f0e", marker="s"),
    "Eko et al. [33]":   dict(color="#2ca02c", marker="^"),
    "Yadav et al. [38]": dict(color="#9467bd", marker="D"),
    "Proposed BECPA":    dict(color="#d62728", marker="*", lw=2.8, ms=10),
}

df = pd.read_csv(CSV_FILE)
df = df[df["Vehicles"].isin(VEHICLES)]

fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
for s in schemes:
    d = df[df["Scheme"] == s].sort_values("Vehicles")
    st = dict(styles[s])
    ax.plot(d["Vehicles"], d[METRIC], label=s,
            lw=st.pop("lw", 2), ms=st.pop("ms", 7),
            markerfacecolor="white", markeredgewidth=1.8, **st)

ax.set_xticks(VEHICLES)                      # x-axis shows only these values
ax.set_xlabel("Number of Vehicles")
ax.set_ylabel("Energy Consumption (mJ)")
ax.set_title(TITLE)
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(OUT_FILE)
plt.show()
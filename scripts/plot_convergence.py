import os
import matplotlib.pyplot as plt

# setting output folder
os.makedirs("results", exist_ok=True)

# -----------------------------
# k-point convergence data
# -----------------------------
k_labels = ["12x12x1", "18x18x1", "24x24x1", "48x48x1"]
k_values = [12, 18, 24, 48]
k_energies = [-36.88676178, -36.88704571, -36.88710481, -36.88711522]

# shifting energies for better readability
k_ref = min(k_energies)
k_delta_mev = [(e - k_ref) * 13.605693 * 1000 for e in k_energies]

plt.figure(figsize=(8, 5))
plt.plot(k_values, k_delta_mev, marker="o")
plt.xticks(k_values, k_labels)
plt.xlabel("K-point mesh")
plt.ylabel("Relative total energy (meV)")
plt.title("Graphene k-point convergence")

# annotating each point
for x, y, raw_e in zip(k_values, k_delta_mev, k_energies):
    plt.annotate(
        f"{raw_e:.8f} Ry",
        (x, y),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8
    )

plt.grid(True)
plt.tight_layout()
plt.savefig("results/graphene_kpoint_convergence.png", dpi=300)
plt.close()

# -----------------------------
# cutoff convergence data
# -----------------------------
ecut_values = [40, 50, 60, 70, 80, 90]
ecut_energies = [-36.88637258, -36.88710481, -36.88748843,
                 -36.88782147, -36.88795788, -36.88799252]

ecut_ref = min(ecut_energies)
ecut_delta_mev = [(e - ecut_ref) * 13.605693 * 1000 for e in ecut_energies]

plt.figure(figsize=(8, 5))
plt.plot(ecut_values, ecut_delta_mev, marker="o")
plt.xlabel("ecutwfc (Ry)")
plt.ylabel("Relative total energy (meV)")
plt.title("Graphene cutoff convergence")

# annotating each point
for x, y, raw_e in zip(ecut_values, ecut_delta_mev, ecut_energies):
    plt.annotate(
        f"{raw_e:.8f} Ry",
        (x, y),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8
    )

# marking chosen production cutoff
plt.axvline(80, linestyle="--", linewidth=1)
plt.annotate(
    "Chosen baseline: 80 Ry",
    (80, ecut_delta_mev[4]),
    textcoords="offset points",
    xytext=(8, -18),
    fontsize=9
)

plt.grid(True)
plt.tight_layout()
plt.savefig("results/graphene_cutoff_convergence.png", dpi=300)
plt.close()

print("Saved:")
print(" - results/graphene_kpoint_convergence.png")
print(" - results/graphene_cutoff_convergence.png")

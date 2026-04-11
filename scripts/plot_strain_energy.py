import os
import matplotlib.pyplot as plt

# setting output folder
os.makedirs("results", exist_ok=True)

# storing strain data
strain_percent = [0, 2, 4]
energies_ry = [-36.88794316, -36.88662125, -36.88175957]

# shifting relative to unstrained case
e0 = energies_ry[0]
delta_mev = [(e - e0) * 13.605693 * 1000 for e in energies_ry]

plt.figure(figsize=(8, 5))
plt.plot(strain_percent, delta_mev, marker="o")
plt.xlabel("Uniaxial strain (%)")
plt.ylabel("Relative total energy (meV)")
plt.title("Graphene strain-energy trend")

for x, y, raw_e in zip(strain_percent, delta_mev, energies_ry):
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
plt.savefig("results/graphene_strain_energy.png", dpi=300)
plt.close()

print("Saved: results/graphene_strain_energy.png")

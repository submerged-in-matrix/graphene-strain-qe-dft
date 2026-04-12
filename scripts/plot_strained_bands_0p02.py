"""
Band Structure Plot: Graphene under 2% Uniaxial Strain
------------------------------------------------------
Reads the .bands.dat.gnu file from bands.x post-processing
and plots E(k) along Gamma -> M -> K -> Gamma with annotations.

Band identification (from data inspection):
  Band 3 = π  (valence,    p_z)  — touches E_F from below at K
  Band 4 = π* (conduction, p_z)  — touches E_F from above at K
  Bands 0-2, 5-7 = σ/σ* (sp² in-plane)

Usage:
    python plot_bands_strain_0p02.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

# ── Configuration ──────────────────────────────────────────────
gnu_file = "graphene_strain_0p02.bands.dat.gnu"
E_fermi = -1.8001  # eV, from relax output
y_min, y_max = -22, 18
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)

# ── Read data ──────────────────────────────────────────────────
raw = open(gnu_file).read().strip()
blocks = raw.split("\n\n")
bands = []
for block in blocks:
    data = np.loadtxt(block.splitlines())
    if data.ndim == 2:
        bands.append(data)

k = bands[0][:, 0]

# ── High-symmetry positions ───────────────────────────────────
# 40 points per segment: Γ(0) → M(40) → K(80) → Γ(120)
K_pos = k[80]
M_pos = k[40]
G1_pos = k[0]
G2_pos = k[120]
hsp_positions = [G1_pos, M_pos, K_pos, G2_pos]
hsp_labels = [r"$\Gamma$", r"$M$", r"$K$", r"$\Gamma$"]

# Band 3 = π, Band 4 = π*
pi_indices = {3, 4}

# ── Plot ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))

for i, band in enumerate(bands):
    energy = band[:, 1] - E_fermi
    if i in pi_indices:
        ax.plot(band[:, 0], energy, color="#D32F2F", linewidth=2.0, zorder=5)
    else:
        ax.plot(band[:, 0], energy, color="#1565C0", linewidth=1.2, zorder=3)

# Fermi level
ax.axhline(0, color="#888888", linestyle="--", linewidth=0.8, zorder=2)
ax.text(G2_pos * 1.01, 0.3, r"$E_F$", fontsize=11, color="#888888", va="bottom")

# High-symmetry vertical lines
for pos in hsp_positions:
    ax.axvline(pos, color="#CCCCCC", linestyle="-", linewidth=0.6, zorder=1)

# ── Annotations ───────────────────────────────────────────────

# 1. Dirac cone — yellow highlight around K, arrow to touching point
cone_dk = (G2_pos - G1_pos) * 0.055
ax.axvspan(K_pos - cone_dk, K_pos + cone_dk,
           color="#FFEB3B", alpha=0.25, zorder=0)
ax.annotate("Dirac cone\n(survives at 2%)",
            xy=(K_pos, 0.0),
            xytext=(K_pos - 0.32, 5.0),
            fontsize=10, fontweight="bold", color="#D32F2F",
            arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.5),
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#D32F2F", alpha=0.9))

# 2. π (valence) — arrow to band 3 near Γ
ax.annotate(r"$\pi$ (valence)",
            xy=(k[12], bands[3][12, 1] - E_fermi),
            xytext=(k[12] + 0.12, -8.0),
            fontsize=10, color="#D32F2F",
            arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.2),
            ha="center")

# 3. π* (conduction) — arrow to band 4 near Γ
ax.annotate(r"$\pi^*$ (conduction)",
            xy=(k[12], bands[4][12, 1] - E_fermi),
            xytext=(k[12] + 0.12, 9.0),
            fontsize=10, color="#D32F2F",
            arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.2),
            ha="center")

# 4. σ bands — arrow to deepest band (band 0) in Γ-M region
ax.annotate(r"$\sigma$ bands (sp² bonding)",
            xy=(k[25], bands[0][25, 1] - E_fermi),
            xytext=(k[25] + 0.28, -16.0),
            fontsize=10, color="#1565C0",
            arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.2),
            ha="center")

# 5. Van Hove singularity — saddle point of π at M
ax.annotate("van Hove\nsingularity",
            xy=(M_pos, bands[3][40, 1] - E_fermi),
            xytext=(M_pos + 0.18, -5.8),
            fontsize=9, fontstyle="italic", color="#555555",
            arrowprops=dict(arrowstyle="->", color="#555555", lw=1.0),
            ha="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#AAAAAA", alpha=0.8))

# ── Axes, labels, legend ──────────────────────────────────────
ax.set_xticks(hsp_positions)
ax.set_xticklabels(hsp_labels, fontsize=14)
ax.set_xlim(k[0], k[-1])
ax.set_ylim(y_min, y_max)
ax.set_ylabel(r"$E - E_F$ (eV)", fontsize=13)
ax.set_title("Graphene Band Structure — 2% Uniaxial Strain (zigzag)", fontsize=14)

legend_elements = [
    Line2D([0], [0], color="#D32F2F", lw=2.0, label=r"$\pi / \pi^*$ bands (p$_z$)"),
    Line2D([0], [0], color="#1565C0", lw=1.2, label=r"$\sigma / \sigma^*$ bands (sp²)"),
    Line2D([0], [0], color="#888888", lw=0.8, ls="--", label=r"$E_F$"),
]
ax.legend(handles=legend_elements, fontsize=10, loc="upper right",
          framealpha=0.9, edgecolor="#CCCCCC")

plt.tight_layout()
save_path = os.path.join(save_dir, "bands_strain_0p02.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Saved: {save_path}")
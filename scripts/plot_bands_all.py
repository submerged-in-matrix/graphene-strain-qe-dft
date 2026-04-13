"""
Band Structure Plots: Graphene under Uniaxial Strain (0%, 2%, 4%)
-----------------------------------------------------------------
Reads .bands.dat.gnu files from bands.x post-processing and generates:
  1. Three individual annotated band structure plots
  2. One comparison panel showing Dirac cone evolution

Band identification (consistent across all strains):
  Band 3 = π  (valence,    p_z)
  Band 4 = π* (conduction, p_z)
  Bands 0-2, 5-7 = σ/σ* (sp² in-plane)

Usage:
    python plot_bands_all.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

# ── Configuration ──────────────────────────────────────────────
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)

strain_data = {
    "0%":  ("dft_data/graphene_strain_0p00.bands.dat.gnu", -1.6591),
    "2%":  ("dft_data/graphene_strain_0p02.bands.dat.gnu", -1.8001),
    "4%":  ("dft_data/graphene_strain_0p04.bands.dat.gnu", -2.0146),
    "20%": ("dft_data/graphene_strain_0p20.bands.dat.gnu", -2.5756),
}

pi_indices = {3, 4}

# ── Load all data ─────────────────────────────────────────────
data = {}
for label, (fname, ef) in strain_data.items():
    raw = open(fname).read().strip()
    blocks = raw.split("\n\n")
    bands = []
    for block in blocks:
        d = np.loadtxt(block.splitlines())
        if d.ndim == 2:
            bands.append(d)
    data[label] = (bands, ef)


# ══════════════════════════════════════════════════════════════
# INDIVIDUAL ANNOTATED PLOTS
# ══════════════════════════════════════════════════════════════
for label, (bands, ef) in data.items():
    k = bands[0][:, 0]
    K_pos, M_pos, G1, G2 = k[80], k[40], k[0], k[-1]
    hsp = [G1, M_pos, K_pos, G2]

    e3K = bands[3][80, 1] - ef
    e4K = bands[4][80, 1] - ef
    gap_meV = abs(e4K - e3K) * 1000

    fig, ax = plt.subplots(figsize=(10, 7))

    for i, band in enumerate(bands):
        energy = band[:, 1] - ef
        if i in pi_indices:
            ax.plot(band[:, 0], energy, color="#D32F2F", linewidth=2.0, zorder=5)
        else:
            ax.plot(band[:, 0], energy, color="#1565C0", linewidth=1.2, zorder=3)

    ax.axhline(0, color="#888888", linestyle="--", linewidth=0.8, zorder=2)
    ax.text(G2 * 1.01, 0.3, r"$E_F$", fontsize=11, color="#888888", va="bottom")

    for pos in hsp:
        ax.axvline(pos, color="#CCCCCC", linestyle="-", linewidth=0.6, zorder=1)

    # Dirac cone highlight
    cone_dk = (G2 - G1) * 0.055
    ax.axvspan(K_pos - cone_dk, K_pos + cone_dk, color="#FFEB3B", alpha=0.25, zorder=0)

    if gap_meV < 1:
        cone_text = "Dirac cone\n(intact, 0 meV gap)"
        highlight_color = "#FFEB3B"
        highlight_alpha = 0.25
    elif gap_meV < 1000:
        cone_text = f"Dirac cone\n(gap ≈ {gap_meV:.0f} meV)"
        highlight_color = "#FFEB3B"
        highlight_alpha = 0.25
    else:
        cone_text = f"Gap ≈ {gap_meV/1000:.2f} eV\nDirac cone destroyed"
        highlight_color = "#FFCDD2"
        highlight_alpha = 0.35

    ax.annotate(cone_text,
                xy=(K_pos, (e3K + e4K) / 2),
                xytext=(K_pos - 0.32, 5.0),
                fontsize=10, fontweight="bold", color="#D32F2F",
                arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.5),
                ha="center", va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#D32F2F", alpha=0.9))

    # π / π* labels
    ax.annotate(r"$\pi$ (valence)",
                xy=(k[12], bands[3][12, 1] - ef),
                xytext=(k[12] + 0.12, -8.0),
                fontsize=10, color="#D32F2F",
                arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.2), ha="center")

    ax.annotate(r"$\pi^*$ (conduction)",
                xy=(k[12], bands[4][12, 1] - ef),
                xytext=(k[12] + 0.12, 9.0),
                fontsize=10, color="#D32F2F",
                arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.2), ha="center")

    # σ bands
    ax.annotate(r"$\sigma$ bands (sp² bonding)",
                xy=(k[25], bands[0][25, 1] - ef),
                xytext=(k[25] + 0.28, -16.0),
                fontsize=10, color="#1565C0",
                arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.2), ha="center")

    # van Hove singularity
    ax.annotate("van Hove\nsingularity",
                xy=(M_pos, bands[3][40, 1] - ef),
                xytext=(M_pos + 0.18, -5.8),
                fontsize=9, fontstyle="italic", color="#555555",
                arrowprops=dict(arrowstyle="->", color="#555555", lw=1.0), ha="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#AAAAAA", alpha=0.8))

    ax.set_xticks(hsp)
    ax.set_xticklabels([r"$\Gamma$", r"$M$", r"$K$", r"$\Gamma$"], fontsize=14)
    ax.set_xlim(k[0], k[-1])
    ax.set_ylim(-22, 18)
    ax.set_ylabel(r"$E - E_F$ (eV)", fontsize=13)
    ax.set_title(f"Graphene Band Structure — {label} Uniaxial Strain (zigzag)", fontsize=14)

    legend_elements = [
        Line2D([0], [0], color="#D32F2F", lw=2.0, label=r"$\pi / \pi^*$ bands (p$_z$)"),
        Line2D([0], [0], color="#1565C0", lw=1.2, label=r"$\sigma / \sigma^*$ bands (sp²)"),
        Line2D([0], [0], color="#888888", lw=0.8, ls="--", label=r"$E_F$"),
    ]
    ax.legend(handles=legend_elements, fontsize=10, loc="upper right",
              framealpha=0.9, edgecolor="#CCCCCC")

    plt.tight_layout()
    strain_tag = label.replace("%", "")
    save_path = os.path.join(save_dir, f"bands_strain_0p0{strain_tag}.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {save_path}")


# ══════════════════════════════════════════════════════════════
# COMPARISON PANEL
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(14, 12), sharey=True, sharex=False)
axes = axes.flatten()

colors_pi = ["#2E7D32", "#D32F2F", "#1565C0", "#B71C1C"]
colors_sigma = ["#81C784", "#EF9A9A", "#90CAF9", "#FFCDD2"]

for idx, (label, (bands, ef)) in enumerate(data.items()):
    ax = axes[idx]
    k = bands[0][:, 0]
    K_pos, M_pos, G1, G2 = k[80], k[40], k[0], k[-1]
    hsp = [G1, M_pos, K_pos, G2]

    e3K = bands[3][80, 1] - ef
    e4K = bands[4][80, 1] - ef
    gap_meV = abs(e4K - e3K) * 1000

    for i, band in enumerate(bands):
        energy = band[:, 1] - ef
        if i in pi_indices:
            ax.plot(band[:, 0], energy, color=colors_pi[idx], linewidth=2.0, zorder=5)
        else:
            ax.plot(band[:, 0], energy, color=colors_sigma[idx], linewidth=1.0, zorder=3)

    ax.axhline(0, color="#888888", linestyle="--", linewidth=0.8, zorder=2)
    for pos in hsp:
        ax.axvline(pos, color="#CCCCCC", linestyle="-", linewidth=0.6, zorder=1)

    cone_dk = (G2 - G1) * 0.05
    if gap_meV > 1000:
        ax.axvspan(K_pos - cone_dk, K_pos + cone_dk, color="#FFCDD2", alpha=0.35, zorder=0)
        gap_text = f"Gap: {gap_meV/1000:.2f} eV\n(cone destroyed)"
    else:
        ax.axvspan(K_pos - cone_dk, K_pos + cone_dk, color="#FFEB3B", alpha=0.25, zorder=0)
        gap_text = "Gap: 0 meV" if gap_meV < 1 else f"Gap: {gap_meV:.0f} meV"

    ax.annotate(gap_text,
                xy=(K_pos, (e3K + e4K) / 2),
                xytext=(K_pos + 0.15, 4.0),
                fontsize=10, fontweight="bold", color=colors_pi[idx],
                arrowprops=dict(arrowstyle="->", color=colors_pi[idx], lw=1.5),
                ha="left",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=colors_pi[idx], alpha=0.9))

    ax.set_xticks(hsp)
    ax.set_xticklabels([r"$\Gamma$", r"$M$", r"$K$", r"$\Gamma$"], fontsize=13)
    ax.set_xlim(k[0], k[-1])
    ax.set_title(f"{label} strain", fontsize=14, fontweight="bold")

    if idx in [0, 2]:
        ax.set_ylabel(r"$E - E_F$ (eV)", fontsize=13)

axes[0].set_ylim(-22, 18)

fig.suptitle("Graphene Band Structure — Dirac Cone Under Uniaxial Strain (zigzag)",
             fontsize=15, fontweight="bold")
plt.tight_layout()
save_path = os.path.join(save_dir, "bands_comparison.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {save_path}")

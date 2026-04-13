"""
Gap vs Strain with Fermi Velocity Diagnostic
---------------------------------------------
Top panel:  Band gap at K vs strain (0–20%)
Bottom panel: Fermi velocity from M→K and K→Γ sides — divergence
              indicates transition from shifted cone to true gap.

Usage:
    python scripts/plot_gap_vs_strain.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
import re

# ── Configuration ──────────────────────────────────────────────
dft_data_dir = "dft_data"
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)

fermi_energies = {
    0:  -1.6591,
    2:  -1.8001,
    4:  -2.0146,
    6:  -2.1195,
    8:  -2.0971,
    10: -2.1519,
    12: -2.3267,
    14: -2.4219,
    16: -2.3893,
    18: -2.4297,
    20: -2.5756,
}

# ── Load all data ─────────────────────────────────────────────
results = []

for fname in sorted(os.listdir(dft_data_dir)):
    if not fname.endswith(".bands.dat.gnu"):
        continue

    match = re.search(r'0p(\d+)', fname)
    if not match:
        continue
    strain_pct = int(match.group(1))

    if strain_pct not in fermi_energies:
        print(f"  Warning: no Fermi energy for {strain_pct}% — skipping {fname}")
        continue

    ef = fermi_energies[strain_pct]

    filepath = os.path.join(dft_data_dir, fname)
    raw = open(filepath).read().strip()
    blocks = raw.split("\n\n")
    bands = []
    for block in blocks:
        data = np.loadtxt(block.splitlines())
        if data.ndim == 2:
            bands.append(data)

    if len(bands) < 5:
        print(f"  Warning: only {len(bands)} bands in {fname} — skipping")
        continue

    k = bands[0][:, 0]
    b3 = bands[3][:, 1] - ef
    b4 = bands[4][:, 1] - ef

    # Gap at K
    gap = b4[80] - b3[80]

    # Fermi velocity from M→K side (indices 76–80) and K→Γ side (80–84)
    dk_MK = k[80] - k[76]
    dk_KG = k[84] - k[80]

    v_MK = (abs((b3[80] - b3[76]) / dk_MK) + abs((b4[80] - b4[76]) / dk_MK)) / 2
    v_KG = (abs((b3[84] - b3[80]) / dk_KG) + abs((b4[84] - b4[80]) / dk_KG)) / 2

    results.append((strain_pct, gap, v_MK, v_KG))
    print(f"  {strain_pct:2d}%: gap = {gap:.4f} eV  v_MK = {v_MK:.2f}  v_KG = {v_KG:.2f}")

results.sort(key=lambda x: x[0])
strains = np.array([r[0] for r in results])
gaps = np.array([r[1] for r in results])
v_MKs = np.array([r[2] for r in results])
v_KGs = np.array([r[3] for r in results])

print(f"\nFound {len(results)} strain levels.")

# ── Plot ───────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 10),
                                gridspec_kw={'height_ratios': [3, 2], 'hspace': 0.08})

# ── Top panel: Gap vs Strain ──────────────────────────────────
ax1.plot(strains, gaps, 'o-', color="#D32F2F", linewidth=2.0, markersize=8,
         markerfacecolor="white", markeredgewidth=2.0, markeredgecolor="#D32F2F", zorder=5)

for s, g in zip(strains, gaps):
    if g < 1.0:
        ax1.annotate(f"{g*1000:.0f} meV", (s, g), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=8, color="#555555")
    else:
        ax1.annotate(f"{g:.2f} eV", (s, g), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=8, color="#555555")

ax1.set_ylabel("Band Gap at K (eV)", fontsize=13)
ax1.set_title("Dirac Cone Gap vs. Uniaxial Strain — Graphene (zigzag)", fontsize=14)
ax1.set_ylim(-0.1, max(gaps) + 0.5)
ax1.axhline(0, color="#888888", linestyle="--", linewidth=0.5)
ax1.tick_params(labelbottom=False)

# ── Bottom panel: Fermi velocity ──────────────────────────────
ax2.plot(strains, v_MKs, 's-', color="#1565C0", linewidth=1.8, markersize=7,
         markerfacecolor="white", markeredgewidth=1.8, label=r"$v_F$ (M→K side)")
ax2.plot(strains, v_KGs, 'D-', color="#E65100", linewidth=1.8, markersize=7,
         markerfacecolor="white", markeredgewidth=1.8, label=r"$v_F$ (K→Γ side)")

ax2.set_xlabel("Uniaxial Strain (%)", fontsize=13)
ax2.set_ylabel("Fermi Velocity (eV / k-unit)", fontsize=13)
ax2.set_xlim(-1, max(strains) + 1)
ax2.set_xticks(strains)
ax2.legend(fontsize=10, loc="center right")

# ── Shared shading for transition regions ─────────────────────
for ax in [ax1, ax2]:
    ax.axvspan(-1, 6, color="#E8F5E9", alpha=0.3, zorder=0)
    ax.axvspan(6, 10, color="#FFF9C4", alpha=0.3, zorder=0)
    ax.axvspan(10, 21, color="#FFEBEE", alpha=0.3, zorder=0)

# Region labels (top panel)
ax1.text(2.5, max(gaps) * 0.92, "Cone survives\n(shifted)", fontsize=10,
         color="#2E7D32", ha="center", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#2E7D32", alpha=0.8))

ax1.text(8, max(gaps) * 0.92, "Transition", fontsize=10,
         color="#F57F17", ha="center", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#F57F17", alpha=0.8))

ax1.text(15, max(gaps) * 0.92, "Cone destroyed\n(true gap)", fontsize=10,
         color="#B71C1C", ha="center", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#B71C1C", alpha=0.8))

# Velocity divergence annotation (bottom panel)
ax2.annotate("Velocities diverge →\ncone deforming",
             xy=(8, v_KGs[4]), xytext=(12, v_KGs[4] + 3),
             fontsize=9, color="#555555",
             arrowprops=dict(arrowstyle="->", color="#555555", lw=1.0),
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#AAAAAA", alpha=0.8))

plt.savefig(os.path.join(save_dir, "gap_vs_strain.png"), dpi=300, bbox_inches="tight")
plt.show()
print(f"\nSaved: {os.path.join(save_dir, 'gap_vs_strain.png')}")

# ── Save numerical data ──────────────────────────────────────
data_path = os.path.join(dft_data_dir, "gap_vs_strain.dat")
with open(data_path, "w") as f:
    f.write("# strain(%)  gap_at_K(eV)  v_F_MK(eV/k)  v_F_KG(eV/k)  v_ratio\n")
    for s, g, vmk, vkg in zip(strains, gaps, v_MKs, v_KGs):
        f.write(f"{s:4.0f}  {g:10.6f}  {vmk:10.4f}  {vkg:10.4f}  {vmk/vkg:8.4f}\n")
print(f"Saved: {data_path}")

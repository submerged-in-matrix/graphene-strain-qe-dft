"""
2D k-scan Gap Map: Graphene under Strain
-----------------------------------------
Reads .bands.dat files from 2D k-scans around K and plots
the band gap as a color map in k-space.

Usage:
    python scripts/plot_2d_kscan.py
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ── Configuration ──────────────────────────────────────────────
dft_data_dir = "dft_data"
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)

scans = {
    "4%":  ("graphene_strain_0p04_2dscan.bands.dat", -2.0146, 479),
    "10%": ("graphene_strain_0p10_2dscan.bands.dat", -2.1519, 1268),
}

nk = 21  # grid dimension

# ── Read and parse ────────────────────────────────────────────
def read_bands_dat(filepath):
    lines = open(filepath).readlines()
    kpoints = []
    eigenvalues = []
    i = 1  # skip header
    while i < len(lines):
        kline = lines[i].split()
        kx, ky = float(kline[0]), float(kline[1])
        i += 1
        eline = lines[i].split()
        eigs = [float(e) for e in eline]
        i += 1
        kpoints.append((kx, ky))
        eigenvalues.append(eigs)
    return np.array(kpoints), np.array(eigenvalues)

def reshape_to_grid(kpoints, gaps, nk):
    kx_unique = np.unique(np.round(kpoints[:, 0], 6))
    KX = np.zeros((nk, nk))
    KY = np.zeros((nk, nk))
    GAP = np.zeros((nk, nk))
    for ix, kx_val in enumerate(kx_unique):
        mask = np.abs(kpoints[:, 0] - kx_val) < 1e-4
        ky_vals = kpoints[mask, 1]
        gap_vals = gaps[mask]
        sort_idx = np.argsort(ky_vals)
        KX[ix, :] = kx_val
        KY[ix, :] = ky_vals[sort_idx]
        GAP[ix, :] = gap_vals[sort_idx]
    return KX, KY, GAP

# ── Plot ───────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

for ax, (label, (fname, ef, gap_1d)) in zip(axes, scans.items()):
    filepath = os.path.join(dft_data_dir, fname)
    kpoints, eigenvalues = read_bands_dat(filepath)
    gaps = eigenvalues[:, 4] - eigenvalues[:, 3]

    KX, KY, GAP = reshape_to_grid(kpoints, gaps, nk)

    min_idx = np.unravel_index(GAP.argmin(), GAP.shape)
    min_kx = KX[min_idx]
    min_ky = KY[min_idx]
    min_gap = GAP[min_idx]

    # Color map
    pcm = ax.pcolormesh(KX, KY, GAP, cmap="RdYlGn_r", shading="gouraud",
                         vmin=0, vmax=1.5)

    # Contour lines
    contours = ax.contour(KX, KY, GAP, levels=[0.05, 0.1, 0.2, 0.5, 1.0],
                           colors="black", linewidths=0.6, alpha=0.5)
    ax.clabel(contours, fmt="%.2f eV", fontsize=7)

    # Mark minimum gap (actual Dirac point)
    ax.plot(min_kx, min_ky, 'k*', markersize=15, zorder=10)
    ax.annotate(f"Min gap: {min_gap*1000:.0f} meV\n(1D path: {gap_1d} meV)",
                xy=(min_kx, min_ky),
                xytext=(min_kx + 0.015, min_ky + 0.02),
                fontsize=10, fontweight="bold", color="black",
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.9))

    # Mark nominal K (center of grid)
    k_center_x = (KX.min() + KX.max()) / 2
    k_center_y = (KY.min() + KY.max()) / 2
    ax.plot(k_center_x, k_center_y, 'w+', markersize=12, markeredgewidth=2, zorder=10)
    ax.annotate("nominal K",
                xy=(k_center_x, k_center_y),
                xytext=(k_center_x - 0.02, k_center_y - 0.03),
                fontsize=9, color="white",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2))

    ax.set_xlabel(r"$k_x$ (reciprocal Å$^{-1}$)", fontsize=12)
    ax.set_ylabel(r"$k_y$ (reciprocal Å$^{-1}$)", fontsize=12)
    ax.set_title(f"{label} strain", fontsize=14, fontweight="bold")
    ax.set_aspect('equal')

    cbar = plt.colorbar(pcm, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label("Gap (eV)", fontsize=11)

fig.suptitle("2D k-scan: Band Gap Around K Point — Graphene Under Strain",
             fontsize=15, fontweight="bold")
plt.tight_layout()
save_path = os.path.join(save_dir, "2d_kscan_gap_map.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()
print(f"Saved: {save_path}")

# ── Summary ───────────────────────────────────────────────────
print("\n=== 2D k-scan Summary ===")
for label, (fname, ef, gap_1d) in scans.items():
    filepath = os.path.join(dft_data_dir, fname)
    kpoints, eigenvalues = read_bands_dat(filepath)
    gaps = eigenvalues[:, 4] - eigenvalues[:, 3]
    min_i = gaps.argmin()
    print(f"\n{label}:")
    print(f"  1D path gap at K:  {gap_1d} meV")
    print(f"  2D scan min gap:   {gaps[min_i]*1000:.0f} meV")
    print(f"  Dirac point at:    kx={kpoints[min_i,0]:.6f}, ky={kpoints[min_i,1]:.6f}")
    print(f"  Reduction factor:  {gap_1d / (gaps[min_i]*1000):.1f}×")

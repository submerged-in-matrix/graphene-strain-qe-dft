"""
Generate 2D k-scan input files for Quantum ESPRESSO
----------------------------------------------------
Creates a grid of k-points around K = (1/3, 1/3, 0) in crystal coordinates
and writes pw.x bands input files for specified strain levels.

Usage:
    python scripts/gen_2d_kscan.py
"""

import numpy as np
import os

# ── Configuration ──────────────────────────────────────────────
# Grid: 21×21 points centered on K = (1/3, 1/3, 0)
# Window: ±0.05 in crystal coordinates (small patch around K)
nk = 21
dk = 0.05
k_center = np.array([1/3, 1/3, 0.0])

# Strain levels to scan
scans = {
    4: {
        "prefix": "graphene_0p04_2dscan",
        "a1x": "2.558400",
        "C1": "-0.0012527510  -0.0014530200   0.0000000000",
        "C2": " 0.3345857510   0.6681200200   0.0000000000",
    },
    10: {
        "prefix": "graphene_0p10_2dscan",
        "a1x": "2.706000",
        "C1": " 0.0004880748  -0.0011654227   0.0000000000",
        "C2": " 0.3328449252   0.6678324227   0.0000000000",
    },
}

a2x = "-1.230000"
a2y = "2.130422"

os.makedirs("inputs", exist_ok=True)

# ── Generate k-grid ───────────────────────────────────────────
k1_vals = np.linspace(k_center[0] - dk, k_center[0] + dk, nk)
k2_vals = np.linspace(k_center[1] - dk, k_center[1] + dk, nk)

nk_total = nk * nk
print(f"Grid: {nk}×{nk} = {nk_total} k-points")
print(f"Window: K ± {dk} in crystal coordinates")
print(f"k1 range: {k1_vals[0]:.6f} to {k1_vals[-1]:.6f}")
print(f"k2 range: {k2_vals[0]:.6f} to {k2_vals[-1]:.6f}")

# Build k-point list
kpoints_block = f"K_POINTS crystal\n{nk_total}\n"
for k1 in k1_vals:
    for k2 in k2_vals:
        kpoints_block += f"  {k1:.8f}  {k2:.8f}  0.00000000  1.0\n"

# ── Write input files ─────────────────────────────────────────
for strain, params in scans.items():
    tag = f"0p{strain:02d}"

    input_text = f"""&CONTROL
    calculation = 'bands',
    prefix = '{params["prefix"]}',
    pseudo_dir = './pseudo/',
    outdir = './tmp/'
/
&SYSTEM
    ibrav = 0,
    nat = 2,
    ntyp = 1,
    ecutwfc = 80.0,
    ecutrho = 640.0,
    occupations = 'smearing',
    smearing = 'mv',
    degauss = 0.02,
    nbnd = 8
/
&ELECTRONS
    conv_thr = 1.0d-8
/
ATOMIC_SPECIES
C 12.011 C.pbe-n-kjpaw_psl.1.0.0.UPF
CELL_PARAMETERS angstrom
{params["a1x"]}   0.000000   0.000000
{a2x}  {a2y}   0.000000
0.000000   0.000000  15.000000
ATOMIC_POSITIONS crystal
C  {params["C1"]}
C  {params["C2"]}
{kpoints_block}"""

    fname = f"inputs/graphene_strain_{tag}_2dscan.bands.in"
    with open(fname, "w") as f:
        f.write(input_text)
    print(f"Written: {fname}")

    # Post-processing input
    pp_text = f"""&BANDS
    prefix = '{params["prefix"]}',
    outdir = './tmp/',
    filband = 'graphene_strain_{tag}_2dscan.bands.dat',
    lsym = .false.
/
"""
    pp_fname = f"inputs/graphene_strain_{tag}_2dscan.bands_pp.in"
    with open(pp_fname, "w") as f:
        f.write(pp_text)
    print(f"Written: {pp_fname}")

print(f"\nDone. Run with:")
for strain in scans:
    tag = f"0p{strain:02d}"
    print(f"  ~/q-e/bin/pw.x < inputs/graphene_strain_{tag}_2dscan.bands.in "
          f"> outputs/graphene_strain_{tag}_2dscan.bands.out 2>&1")
    print(f"  ~/q-e/bin/bands.x < inputs/graphene_strain_{tag}_2dscan.bands_pp.in "
          f"> outputs/graphene_strain_{tag}_2dscan.bands_pp.out 2>&1")

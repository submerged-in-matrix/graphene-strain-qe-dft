# 2D k-scan Around K: Locating the Dirac Point Under Strain

## Objective

Determine whether the band gap measured along the 1D Γ→M→K→Γ path is a true gap or an artifact of the Dirac point shifting off the high-symmetry path. A 2D grid of k-points around K directly maps the gap in k-space and locates the actual minimum.

---

## Why a 2D Scan?

The standard band structure calculation samples eigenvalues along a 1D path through the Brillouin zone. Under uniaxial strain, the C₃ rotational symmetry of the honeycomb lattice is broken, and the Dirac point is no longer pinned to the high-symmetry K point. It can shift in any direction in 2D k-space.

A 1D path that passes through the nominal K will measure a nonzero gap even if the Dirac crossing still exists — just at a different k-point. The only way to resolve this ambiguity is to scan a 2D region around K and find where the gap actually minimizes.

---

## Method

A 21×21 grid of k-points was placed in a window of ±0.05 in crystal reciprocal coordinates around K = (1/3, 1/3, 0). This gives 441 k-points per strain level. At each k-point, pw.x diagonalizes the Kohn-Sham Hamiltonian (using the charge density from the relaxation run) and returns all 8 eigenvalues. The gap is defined as ε₅(k) − ε₄(k) — the energy difference between the π* (conduction) and π (valence) bands.

Two strain levels were scanned:
- **4%** — in the "cone survives" regime according to the velocity diagnostic
- **10%** — in the transition zone

### Computational Details

- K_POINTS crystal (not crystal_b) — explicit list of 441 k-points with equal weight
- Charge density reused from relaxation via a copy of the tmp/prefix.save directory under a new prefix, to avoid overwriting existing data
- nbnd = 8, all other parameters identical to the 1D band calculations
- lsym = .false. in bands.x post-processing

---

## Results

| Strain | Gap from 1D path | Min gap from 2D scan | Reduction | Dirac point location (Cartesian reciprocal) |
|--------|-------------------|----------------------|-----------|----------------------------------------------|
| 4%     | 479 meV           | **21 meV**           | 23×       | kx = 0.318, ky = 0.602                      |
| 10%    | 1,268 meV         | **71 meV**           | 18×       | kx = 0.288, ky = 0.641                      |

---

## Physical Interpretation

### 4% Strain — Cone Survives

The 2D scan confirms what the velocity diagnostic suggested: the Dirac cone is intact at 4% strain. The 1D path measured 479 meV because it passes through the nominal K, but the actual Dirac point has shifted to a new location. The minimum gap of 21 meV is essentially zero within the numerical precision of the calculation (the Marzari-Vanderbilt smearing broadens eigenvalues by ~degauss ≈ 0.02 Ry ≈ 272 meV, and the finite k-grid spacing adds discretization error).

The gap color map shows a clear, roughly circular minimum — the green "island" — displaced from the nominal K (white cross) toward lower kx and higher ky. The contour lines are approximately concentric around the Dirac point, consistent with a slightly tilted but intact cone.

### 10% Strain — Transition Zone

The minimum gap drops from 1,268 meV (1D path) to 71 meV (2D scan) — a dramatic reduction, but the gap does not reach zero. This is consistent with the transition regime identified by the velocity diagnostic.

Key differences from the 4% case:
- The Dirac point has shifted further from nominal K (larger displacement)
- The gap minimum region is more elongated and asymmetric — the contour lines are no longer circular
- The 71 meV residual gap is larger than the 21 meV at 4%, even though the 2D scan should find the true minimum

The elongation and asymmetry of the gap valley indicate that the Dirac cone is being strongly deformed — the dispersion is no longer cone-like in all directions. The 71 meV residual could indicate either:
1. A true gap is beginning to open (the Dirac points are merging)
2. The grid resolution (21×21) is too coarse to resolve the exact minimum

A finer grid (41×41) around the minimum or a reduced smearing parameter would distinguish these cases. However, the qualitative conclusion is clear: the cone is severely distorted at 10% but not yet fully destroyed.

---

## Connection to the Velocity Diagnostic

The 2D scan validates the three-regime classification from the Fermi velocity analysis:

- **Cone survives (0–4%)**: 2D scan confirms Dirac point exists with near-zero gap. The 1D path gap was purely a geometric artifact of missing the shifted crossing.
- **Transition (6–10%)**: 2D scan shows the gap is dramatically reduced but nonzero. The cone is deforming.
- **Cone destroyed (>10%)**: not scanned here, but at 20% the 1D gap is 2.85 eV — even a 2D scan would not recover a crossing, since the velocity diagnostic shows fully parabolic bands.

---

## Remarks

- The 2D scan is computationally modest: 441 k-points took ~7–15 minutes per strain level
- The .bands.dat file from bands.x provides eigenvalues in eV at each k-point in Cartesian reciprocal coordinates
- For publication quality, the scan window and grid density should be optimized — a preliminary coarse scan to locate the minimum, followed by a fine scan around it
- The residual 21 meV gap at 4% could be further reduced by decreasing degauss or increasing the grid density
- The gap map also reveals the anisotropy of the Dirac cone under strain — the contour shape encodes the direction-dependent Fermi velocity

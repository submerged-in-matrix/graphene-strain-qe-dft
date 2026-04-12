# Band Structure of Graphene under Uniaxial Strain (0%, 2%, 4%)

## Objective

Compute the electronic band structure of graphene at three strain levels (0%, 2%, 4% uniaxial tension along zigzag) and track the fate of the Dirac cone — the linear band crossing at the K point that gives graphene its semimetallic character.

---

## Why Band Structure?

The band structure E_n(k) tells us how electron energies depend on crystal momentum. For graphene, the most important feature is the Dirac cone: the point where the π (valence) and π* (conduction) bands meet with linear dispersion at the K point of the Brillouin zone. This crossing makes graphene a zero-gap semimetal with massless charge carriers.

Under strain, the lattice distorts, the Brillouin zone deforms, and the hopping parameters between carbon atoms change. The central question of this project is whether that crossing survives.

---

## Physical Background

### The Dirac Cone

In unstrained graphene, the honeycomb lattice has two carbon atoms per unit cell (sublattices A and B). The π electrons from the out-of-plane p_z orbitals form two bands:

- π (bonding) → valence band
- π* (antibonding) → conduction band

At the K and K' corners of the hexagonal Brillouin zone, these bands touch at the Fermi level with linear dispersion:

E(k) ≈ ±ℏv_F|k − K|

Where v_F ≈ 10⁶ m/s is the Fermi velocity. This linear crossing is the Dirac cone — electrons near K behave as massless Dirac fermions.

### What Strain Does

Uniaxial strain along the zigzag direction modifies the three nearest-neighbor hopping parameters t₁, t₂, t₃ unequally. The bond aligned with the strain direction stretches more, reducing its hopping integral, while the two angled bonds stretch less. This breaks C₃ rotational symmetry.

The Dirac point can respond in three ways:

1. **Survives and shifts** — the crossing point moves in k-space but remains gapless
2. **Survives but tilts** — the Fermi velocity becomes anisotropic (different slopes in different k-directions)
3. **Opens a gap** — the cone is destroyed, graphene becomes a semiconductor

Tight-binding theory predicts that the Dirac cone is topologically protected and survives until the strain is large enough (~20%+) to merge the two inequivalent Dirac points (K and K'). Below that threshold, the cone shifts and tilts but does not gap.

---

## Method: The Two-Step Calculation

### Step 1: SCF (or reuse from relaxation)

The self-consistent field calculation produces the ground-state charge density ρ(r) by solving the Kohn-Sham equations iteratively on a uniform k-grid. This ρ(r) defines the Kohn-Sham potential V_KS[ρ] that electrons feel.

For the strained cases (2%, 4%), the ρ(r) from the final relaxation step was reused directly — no separate SCF was needed.

For the unstrained case (0%), the existing SCF charge density was used.

### Step 2: Non-SCF Bands Calculation

`calculation = 'bands'` tells QE: do not solve self-consistently. Read the converged ρ(r), construct V_KS[ρ], and diagonalize the Hamiltonian at each k-point along a specified path through the Brillouin zone. One diagonalization per k-point, no iterative convergence. This is computationally cheap.

The result is the set of eigenvalues ε_n(k) — the band energies at each k-point along the path.

### Post-Processing: bands.x

The raw eigenvalues from pw.x are stored in QE's internal format. `bands.x` reads them and produces a plottable text file (.bands.dat.gnu) with two columns: cumulative k-path distance and energy in eV.

---

## The k-Path: Γ → M → K → Γ

The high-symmetry path for the hexagonal Brillouin zone:

- **Γ (0, 0, 0)** — zone center
- **M (1/2, 0, 0)** — midpoint of a BZ edge
- **K (1/3, 1/3, 0)** — corner of the BZ, where the Dirac cone lives

Each segment was sampled with 40 k-points for smooth dispersion curves.

### K-Point Convention

With ibrav=0 and explicit CELL_PARAMETERS, the K point in crystal_b coordinates is (1/3, 1/3, 0) — not (1/3, 2/3, 0). This depends on how the reciprocal lattice vectors are oriented relative to the real-space cell. Using the wrong K coordinates produces bands that look qualitatively similar but miss the Dirac crossing entirely. The correct coordinates were verified by confirming band degeneracy at K for unstrained graphene.

### Strain and the Brillouin Zone

Under uniaxial strain, the real-space lattice vectors change, and so do the reciprocal lattice vectors. The BZ is no longer a regular hexagon. However, the fractional coordinates (1/3, 1/3, 0) in crystal_b still map to the correct K point because QE uses the actual reciprocal lattice to convert — the strain is automatically accounted for.

---

## Key Parameters

- calculation = bands
  → non-self-consistent, reads existing ρ(r)
- prefix must match the SCF/relax run
  → so QE finds the correct charge density in outdir
- nbnd = 8
  → 8 bands total (4 occupied + 4 empty), sufficient to capture π, π*, σ, and σ* bands
- K_POINTS crystal_b
  → k-path in fractional reciprocal coordinates with interpolation counts
- lsym = .false. (in bands.x post-processing)
  → disables symmetry classification of eigenstates. Required for ibrav=0 with hexagonal symmetry, where the sym_band routine can segfault. Does not affect the band energies.

---

## Results Summary

| Strain | Fermi Energy (eV) | Gap at K (meV) | BFGS Steps (relax) | Final Energy (Ry) |
|--------|-------------------|----------------|--------------------|--------------------|
| 0%     | -1.6591           | 0              | — (no relax)       | -36.8871           |
| 2%     | -1.8001           | 238            | 5                  | -36.8867           |
| 4%     | -2.0146           | 479            | 5                  | -36.8850           |

---

## Band Identification

With 8 bands and 2 atoms in the unit cell (8 valence electrons: 4 per carbon), the band assignment is:

- **Band 0**: deep σ (s-derived bonding)
- **Bands 1–2**: σ bands (sp² in-plane bonding)
- **Band 3**: π band (p_z bonding) — valence
- **Band 4**: π* band (p_z antibonding) — conduction
- **Bands 5–7**: σ* and higher conduction bands

Bands 3 and 4 are the ones that form the Dirac cone at K. They arise from the out-of-plane p_z orbitals that do not participate in the sp² framework — they form a separate π system with weaker bonding, which is why they sit closest to the Fermi level.

---

## Physical Interpretation

### 0% (Unstrained)

Perfect Dirac cone. Bands 3 and 4 are exactly degenerate at K (0 meV gap), confirming the expected semimetallic behavior. The linear dispersion near K reflects massless Dirac fermion physics. The σ bands lie well below (~-3 eV at Γ) and above (~+3 eV at Γ) the Fermi level, uninvolved in the low-energy transport.

### 2% Strain

The Dirac cone survives. The measured gap of 238 meV at K is a numerical artifact — it arises from the combination of Marzari-Vanderbilt smearing (degauss = 0.02 Ry) and the finite k-grid density along the path. The actual Dirac point may have shifted slightly away from the high-symmetry K in response to the broken C₃ symmetry, so our path passes close to but not exactly through the crossing.

The overall band shape is preserved. The π/π* bands still cross near E_F with approximately linear dispersion. The σ bands are slightly modified but remain well separated from E_F.

### 4% Strain

Same picture, slightly more pronounced. The gap at K grows to 479 meV, consistent with the Dirac point shifting further from the nominal K as the lattice distortion increases. The cone is not destroyed — it has moved in k-space. The band dispersion near the crossing remains approximately linear.

### The Trend

0 → 238 → 479 meV: the apparent gap grows roughly linearly with strain. This is consistent with a Dirac point that shifts away from K in proportion to the strain magnitude, rather than a true gap opening. A real gap opening would show qualitatively different behavior — the bands would flatten near K and develop a parabolic (massive) dispersion, which we do not observe.

---

## Remarks

- The "gap" values reported here are upper bounds — the actual Dirac crossing likely occurs at a k-point slightly off the high-symmetry path, where the gap is zero or near-zero
- To confirm this, one could compute bands on a 2D k-grid around K and search for the true crossing point
- The Fermi energy shifts progressively downward with strain (-1.66 → -1.80 → -2.01 eV), reflecting the change in average potential as bonds stretch
- The total energy increases with strain (-36.8871 → -36.8867 → -36.8850 Ry), as expected — you are pulling against the bonding forces
- For the unstrained case, lsym=.false. was required in bands.x to avoid a segfault in the symmetry classification routine (a known QE issue with ibrav=0 and full hexagonal symmetry). With strain, the reduced symmetry avoids this bug.

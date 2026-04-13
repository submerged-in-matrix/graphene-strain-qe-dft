# Gap vs Strain Analysis: Identifying Dirac Cone Destruction

## Objective

Determine at what strain level the Dirac cone in graphene transitions from "shifted but intact" to "truly gapped and destroyed", using a physics-based diagnostic rather than an arbitrary gap threshold.

---

## The Problem

When we compute band structures along the fixed Γ→M→K→Γ path, any measured "gap" at K could mean two things:

1. **The cone has shifted** — the crossing still exists at zero gap, but at a k-point slightly off our 1D path. The measured gap is an artifact of sampling.
2. **The cone is destroyed** — the bands genuinely separate, and no crossing exists anywhere in k-space.

A single gap value cannot distinguish these cases. We need a structural diagnostic of the band dispersion itself.

---

## The Diagnostic: Fermi Velocity Asymmetry

The key observable is the **Fermi velocity** — the slope of the π and π* bands approaching K from the M→K direction vs the K→Γ direction.

v_F(M→K) = |dE/dk| measured from the M side approaching K
v_F(K→Γ) = |dE/dk| measured from the K side departing toward Γ

For a true Dirac cone (even a tilted one), both velocities are comparable — the cone is a V-shape that may lean but retains steep slopes on both sides.

When the cone is destroyed, the bands develop **parabolic** curvature near K. The dispersion flattens, and because the strain breaks C₃ symmetry, the flattening is direction-dependent. The velocity from one direction drops significantly while the other holds — the two velocities diverge.

---

## Results

| Strain | Gap at K (eV) | v_F M→K | v_F K→Γ | Ratio (M→K / K→Γ) |
|--------|---------------|---------|---------|-------------------|
| 0%     | 0.000         | 13.2    | 15.4    | 0.86              |
| 2%     | 0.238         | 12.2    | 13.2    | 0.93              |
| 4%     | 0.479         | 11.5    | 11.2    | 1.02              |
| 6%     | 0.732         | 10.9    | 9.5     | 1.14              |
| 8%     | 0.992         | 10.3    | 8.1     | 1.28              |
| 10%    | 1.268         | 9.9     | 6.9     | 1.43              |
| 12%    | 1.555         | 9.6     | 6.1     | 1.58              |
| 14%    | 1.859         | 9.4     | 5.5     | 1.71              |
| 16%    | 2.174         | 9.2     | 5.1     | 1.82              |
| 18%    | 2.508         | 9.2     | 4.8     | 1.89              |
| 20%    | 2.853         | 9.2     | 4.8     | 1.92              |

---

## Three Regimes

### 1. Cone Survives (0–4%)

The velocity ratio stays near 1.0 (range: 0.86–1.02). Both sides of the dispersion have comparable slopes. The measured gap (0–479 meV) arises from the Dirac point shifting away from the nominal K on our 1D path, not from a true gap opening. The dispersion remains approximately linear (V-shaped) on both sides.

At 0%, the ratio is slightly below 1 (0.86) because of the natural anisotropy of the hexagonal BZ — the M→K and K→Γ directions have different lengths in reciprocal space.

### 2. Transition (6–10%)

The velocity ratio climbs from 1.14 to 1.43. The K→Γ velocity drops sharply (15.4 → 6.9 eV/k-unit) while the M→K velocity decreases only gently (13.2 → 9.9). The dispersion is becoming asymmetric — the bands are flattening on the K→Γ side, developing parabolic character. The cone is being deformed, not just shifted.

This is the crossover region. There is no sharp phase transition — the destruction is gradual.

### 3. Cone Destroyed (10–20%)

The velocity ratio exceeds 1.4 and saturates near 1.9. The K→Γ velocity has collapsed to ~5 eV/k-unit (one third of its unstrained value) while the M→K velocity has stabilized at ~9 eV/k-unit. The dispersion near K is now genuinely parabolic — the electrons have acquired mass. The gap is real and grows linearly with further strain.

The saturation of the velocity ratio above ~14% confirms that the band structure has settled into a new, qualitatively different regime.

---

## Why ~6–10%?

The transition occurs in this range because of the competition between two effects:

1. **Hopping parameter asymmetry** — uniaxial strain makes the three nearest-neighbor hoppings (t₁, t₂, t₃) increasingly unequal. The bond along the strain direction weakens, while the two angled bonds weaken less.

2. **Dirac point merging** — in tight-binding theory, the two inequivalent Dirac points (K and K') move toward each other under uniaxial strain. When the hopping asymmetry reaches a critical value (one hopping equals the sum of the other two: t₁ = t₂ + t₃), the Dirac points merge and annihilate, opening a true gap.

For zigzag strain, this merging condition is approached gradually. The 6–10% range is where the Dirac points are close enough that their mutual influence begins to deform the local band structure, even before full merging occurs.

---

## Physical Interpretation

The gap-vs-strain curve is approximately linear across the full range (0–20%), which might suggest a simple, uniform mechanism. But the velocity diagnostic reveals that the underlying physics changes qualitatively:

- At low strain: the gap is a **geometric artifact** of our k-path
- At high strain: the gap is a **physical reality** of a gapped band structure

The Fermi velocity plot makes this transition visible. It is the recommended diagnostic for any study that needs to distinguish "shifted Dirac cone" from "destroyed Dirac cone" without performing a computationally expensive 2D k-scan.

---

## Remarks

- The velocity ratio is a more robust diagnostic than the gap value, which depends on the specific k-path chosen
- The transition is a crossover, not a sharp phase transition — there is no single "critical strain"
- A 2D k-scan around K at 6–10% strain would directly confirm whether the crossing persists off-path or has genuinely vanished
- The velocity values reported here are in units of eV per k-path unit, not SI units — they reflect the band slope in the QE output coordinate system
- PBE may slightly over- or underestimate the critical strain for merging — GW corrections could shift the transition range

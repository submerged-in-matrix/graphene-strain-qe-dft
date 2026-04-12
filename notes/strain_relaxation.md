# Fixed-Cell Relaxation (relax) for Graphene under 2% Uniaxial Strain

## Objective

Determine the internal atomic equilibrium of graphene when the lattice is deformed by 2% uniaxial tensile strain along the zigzag direction, while keeping the strained cell fixed.

---

## Why Relax under Strain?

When we apply uniaxial strain by manually stretching the lattice vectors, we change the cell but leave the atoms at their unstrained fractional coordinates. Those positions are no longer equilibrium positions — the atoms feel residual forces because the bond angles and lengths have been disrupted by the asymmetric deformation. Relaxation lets the atoms find their new equilibrium within the deformed cell.

This is different from the silicon vc-relax case: there, both atoms and cell were free. Here, the cell is deliberately frozen at the strained geometry — we are imposing a mechanical constraint and asking only how the atoms rearrange internally.

---

## Physical Model

For fixed-cell relaxation, we minimize:

E = E({R_i}) at fixed cell

The equilibrium condition is:

F_i = -∂E/∂R_i = 0

Where:
- R_i: atomic positions (in crystal coordinates)
- F_i: Hellmann–Feynman force on atom i

The stress tensor σ is not required to vanish — it reflects the mechanical response of the material to the imposed strain, which is exactly what we want to preserve.

---

## Method

The relax calculation performs:

1. SCF → solve electronic structure at current geometry
2. Compute Hellmann–Feynman forces on each atom
3. Update atomic positions using BFGS
4. Repeat until forces fall below threshold

Optimization algorithm:
- BFGS (Broyden–Fletcher–Goldfarb–Shanno)
  - Same quasi-Newton method as the silicon vc-relax, but here it only updates atomic positions, not the cell.
  - Builds an approximate inverse Hessian from force history to accelerate convergence beyond simple steepest descent.

---

## Key Parameters

- calculation = relax
  → relax atomic positions only, cell is frozen
- ion_dynamics = bfgs
  → BFGS optimizer for atomic positions
- forc_conv_thr = 1.0×10⁻⁴ Ry/Bohr
  → force convergence threshold (tighter than the silicon case, appropriate for 2D systems where small force residuals matter)
- ibrav = 0 with explicit CELL_PARAMETERS
  → required because uniaxial strain breaks the hexagonal symmetry that ibrav=4 assumes

No &CELL block is needed — the cell is not being optimized.

---

## How the Strain Was Applied

Unstrained graphene (ibrav=4):
- a = 4.65 Bohr ≈ 2.46 Å
- Hexagonal symmetry: a₁ = a(1, 0, 0), a₂ = a(-1/2, √3/2, 0)

2% uniaxial strain along x (zigzag direction):
- a₁x stretched: 2.46 × 1.02 = 2.5092 Å
- a₂ adjusted to maintain its y-component but reflect the x-strain
- c-axis (vacuum) unchanged at 15.0 Å

This breaks the C₃ rotational symmetry of the honeycomb → the two sublattice sites are no longer related by the same symmetry operations → internal relaxation becomes necessary.

---

## Results Summary

- BFGS steps: 5
- Final total energy: -36.8867 Ry
- Final total force: 0.000011 Ry/Bohr (well below threshold)

Relaxed atomic positions (crystal coordinates):
- C₁: (-0.000806, -0.000853, 0.0000)
- C₂: ( 0.334139,  0.667520, 0.0000)

---

## Physical Interpretation

Unstrained positions were (0, 0, 0) and (1/3, 2/3, 0). After relaxation:

- Both atoms shifted slightly from their ideal fractional coordinates
- The shifts are small (~0.001 in crystal units) — graphene's sp² bonding is stiff
- The displacement pattern reflects the broken symmetry: uniaxial strain along zigzag makes the three C–C bonds inequivalent (one bond aligned with strain, two at angles), and the atoms adjust to partially equalize bond lengths
- Atoms remain in-plane (z = 0) — graphene stays flat under in-plane strain, as expected for a 2D sp² network

The fact that relaxation changed the positions at all confirms that simply stretching the cell without relaxing would introduce a systematic error in the band structure. These relaxed coordinates are what we feed into the next step.

---

## Remarks

- The initial forces (~0.012 Ry/Bohr) were small, confirming that 2% strain is a mild perturbation for graphene
- Convergence in 5 steps is typical for such small distortions
- For larger strains (e.g., 10%+), more BFGS steps would be needed and the sublattice shifts would grow
- The relaxed positions from this calculation will be used directly in the subsequent band structure calculation to check whether the Dirac cone survives under strain

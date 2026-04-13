#!/bin/bash
# ══════════════════════════════════════════════════════════════
# Graphene Strain Grid: Automated SCF → Relax → Bands Pipeline
# Generates and runs input files for 6%, 8%, 10%, 12%, 14%, 16%, 18%
# ══════════════════════════════════════════════════════════════
#
# Usage: 
#   cd ~/dft_projects/graphene-strain-qe-dft
#   bash scripts/run_strain_grid.sh
#
# Prerequisites:
#   - pseudo/C.pbe-n-kjpaw_psl.1.0.0.UPF exists
#   - ~/q-e/bin/pw.x and ~/q-e/bin/bands.x are compiled
#   - inputs/, outputs/, dft_data/ directories exist

set -e  # exit on error

PW=~/q-e/bin/pw.x
BANDS=~/q-e/bin/bands.x

# Unstrained lattice parameter (Angstrom)
A0=2.460000

# a2 components (unchanged across all strains)
A2X=-1.230000
A2Y=2.130422

# Strain levels to compute (percent)
STRAINS=(6 8 10 12 14 16 18)

mkdir -p inputs outputs dft_data

for STRAIN in "${STRAINS[@]}"; do

    # ── Compute strained a1x ──────────────────────────────────
    FACTOR=$(echo "1 + $STRAIN / 100" | bc -l)
    A1X=$(echo "$A0 * $FACTOR" | bc -l | xargs printf "%.6f")
    
    # Naming: 0p06, 0p08, ..., 0p18
    TAG=$(printf "0p%02d" $STRAIN)
    
    echo ""
    echo "══════════════════════════════════════════════════════"
    echo "  STRAIN: ${STRAIN}%  |  a1x = ${A1X} Å  |  tag = ${TAG}"
    echo "══════════════════════════════════════════════════════"

    # ── 1. SCF ────────────────────────────────────────────────
    cat > inputs/graphene_strain_${TAG}_scf.in << EOF
&CONTROL
    calculation = 'scf',
    prefix = 'graphene_${TAG}',
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
    degauss = 0.02
/
&ELECTRONS
    conv_thr = 1.0d-8
/
ATOMIC_SPECIES
C 12.011 C.pbe-n-kjpaw_psl.1.0.0.UPF
CELL_PARAMETERS angstrom
${A1X}   0.000000   0.000000
${A2X}  ${A2Y}   0.000000
0.000000   0.000000  15.000000
ATOMIC_POSITIONS crystal
C 0.000000  0.000000  0.000000
C 0.333333  0.666667  0.000000
K_POINTS automatic
24 24 1 0 0 0
EOF

    echo "[${TAG}] Running SCF..."
    $PW < inputs/graphene_strain_${TAG}_scf.in > outputs/graphene_strain_${TAG}_scf.out 2>&1
    
    if grep -q "convergence has been achieved" outputs/graphene_strain_${TAG}_scf.out; then
        echo "[${TAG}] SCF converged."
    else
        echo "[${TAG}] *** SCF FAILED TO CONVERGE *** — skipping this strain."
        continue
    fi

    # ── 2. RELAX ──────────────────────────────────────────────
    cat > inputs/graphene_strain_${TAG}.relax.in << EOF
&CONTROL
    calculation = 'relax',
    prefix = 'graphene_${TAG}_relax',
    pseudo_dir = './pseudo/',
    outdir = './tmp/',
    forc_conv_thr = 1.0d-4
/
&SYSTEM
    ibrav = 0,
    nat = 2,
    ntyp = 1,
    ecutwfc = 80.0,
    ecutrho = 640.0,
    occupations = 'smearing',
    smearing = 'mv',
    degauss = 0.02
/
&ELECTRONS
    conv_thr = 1.0d-8
/
&IONS
    ion_dynamics = 'bfgs'
/
ATOMIC_SPECIES
C 12.011 C.pbe-n-kjpaw_psl.1.0.0.UPF
CELL_PARAMETERS angstrom
${A1X}   0.000000   0.000000
${A2X}  ${A2Y}   0.000000
0.000000   0.000000  15.000000
ATOMIC_POSITIONS crystal
C 0.000000  0.000000  0.000000
C 0.333333  0.666667  0.000000
K_POINTS automatic
24 24 1 0 0 0
EOF

    echo "[${TAG}] Running RELAX..."
    $PW < inputs/graphene_strain_${TAG}.relax.in > outputs/graphene_strain_${TAG}.relax.out 2>&1
    
    if grep -q "bfgs converged" outputs/graphene_strain_${TAG}.relax.out; then
        echo "[${TAG}] Relaxation converged."
    else
        echo "[${TAG}] *** RELAX FAILED *** — skipping bands."
        continue
    fi

    # Extract relaxed positions
    C1=$(grep -A 2 "ATOMIC_POSITIONS" outputs/graphene_strain_${TAG}.relax.out | tail -2 | head -1 | awk '{print $2, $3}')
    C2=$(grep -A 2 "ATOMIC_POSITIONS" outputs/graphene_strain_${TAG}.relax.out | tail -1 | awk '{print $2, $3}')
    C1X=$(echo $C1 | awk '{print $1}')
    C1Y=$(echo $C1 | awk '{print $2}')
    C2X=$(echo $C2 | awk '{print $1}')
    C2Y=$(echo $C2 | awk '{print $2}')
    
    # Extract Fermi energy
    EF=$(grep "the Fermi energy" outputs/graphene_strain_${TAG}.relax.out | tail -1 | awk '{print $5}')
    
    echo "[${TAG}] Relaxed positions: C1=(${C1X}, ${C1Y}), C2=(${C2X}, ${C2Y})"
    echo "[${TAG}] Fermi energy: ${EF} eV"
    
    # Save metadata for plotting later
    TOTAL_E=$(grep "Final energy" outputs/graphene_strain_${TAG}.relax.out | awk '{print $4}')
    echo "${STRAIN} ${EF} ${TOTAL_E} ${C1X} ${C1Y} ${C2X} ${C2Y}" >> dft_data/strain_grid_summary.dat

    # ── 3. BANDS ──────────────────────────────────────────────
    cat > inputs/graphene_strain_${TAG}.bands.in << EOF
&CONTROL
    calculation = 'bands',
    prefix = 'graphene_${TAG}_relax',
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
${A1X}   0.000000   0.000000
${A2X}  ${A2Y}   0.000000
0.000000   0.000000  15.000000
ATOMIC_POSITIONS crystal
C  ${C1X}  ${C1Y}  0.0000000000
C  ${C2X}  ${C2Y}  0.0000000000
K_POINTS crystal_b
4
0.0000  0.0000  0.0000  40  ! Gamma
0.5000  0.0000  0.0000  40  ! M
0.3333  0.3333  0.0000  40  ! K
0.0000  0.0000  0.0000   0  ! Gamma
EOF

    echo "[${TAG}] Running BANDS..."
    $PW < inputs/graphene_strain_${TAG}.bands.in > outputs/graphene_strain_${TAG}.bands.out 2>&1

    # ── 4. BANDS POST-PROCESSING ──────────────────────────────
    cat > inputs/graphene_strain_${TAG}.bands_pp.in << EOF
&BANDS
    prefix = 'graphene_${TAG}_relax',
    outdir = './tmp/',
    filband = 'graphene_strain_${TAG}.bands.dat',
    lsym = .false.
/
EOF

    echo "[${TAG}] Running BANDS post-processing..."
    $BANDS < inputs/graphene_strain_${TAG}.bands_pp.in > outputs/graphene_strain_${TAG}.bands_pp.out 2>&1
    
    # Move the .gnu file to dft_data
    if [ -f "graphene_strain_${TAG}.bands.dat.gnu" ]; then
        mv graphene_strain_${TAG}.bands.dat.gnu dft_data/
        mv graphene_strain_${TAG}.bands.dat dft_data/ 2>/dev/null || true
        echo "[${TAG}] ✓ Complete — .gnu file saved to dft_data/"
    else
        echo "[${TAG}] *** bands.x did not produce .gnu file ***"
    fi

done

echo ""
echo "══════════════════════════════════════════════════════"
echo "  ALL DONE. Summary saved to dft_data/strain_grid_summary.dat"
echo "══════════════════════════════════════════════════════"
echo ""
echo "Strain grid summary:"
echo "strain(%)  E_F(eV)  E_total(Ry)  C1x  C1y  C2x  C2y"
cat dft_data/strain_grid_summary.dat

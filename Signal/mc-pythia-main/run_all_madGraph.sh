#!/usr/bin/env bash

set -euo pipefail

# ============================================================
# Configuration
# ============================================================

# SAFETY:
#   true  = only show what would be changed
#   false = actually modify the files
DRY_RUN=false

# Number of generated events
NEVENTS=100000

# Gravitino mass in GeV
GRAVITINO_MASS=1e-13

# Lifetime calculation script
LIFETIME_SCRIPT="./lifetime.py"

# MadGraph configuration
MG5="./bin/mg5_aMC"

MG5_MODEL="./GldGrv_UFO"

MG5_GENERATE_CARD="mg5_generate.txt"
MG5_LAUNCH_CARD="mg5_launch.txt"

# ============================================================
# Folders to process
# ============================================================

FOLDERS=(
    # "FCCee_100_stau_0.2m_ctau_ecm_240"
    # "FCCee_105_stau_0.2m_ctau_ecm_240"
    # "FCCee_110_stau_0.2m_ctau_ecm_240"
    # "FCCee_115_stau_0.2m_ctau_ecm_240"
    # "FCCee_118_stau_0.2m_ctau_ecm_240"
    # "FCCee_119_stau_0.2m_ctau_ecm_240"

    # "FCCee_100_stau_0.5m_ctau_ecm_240"
    # "FCCee_105_stau_0.5m_ctau_ecm_240"
    # "FCCee_110_stau_0.5m_ctau_ecm_240"
    # "FCCee_115_stau_0.5m_ctau_ecm_240"
    # "FCCee_118_stau_0.5m_ctau_ecm_240"
    # "FCCee_119_stau_0.5m_ctau_ecm_240"

    # "FCCee_100_stau_1m_ctau_ecm_240"
    # "FCCee_105_stau_1m_ctau_ecm_240"
    # "FCCee_110_stau_1m_ctau_ecm_240"
    # "FCCee_115_stau_1m_ctau_ecm_240"
    # "FCCee_118_stau_1m_ctau_ecm_240"
    # "FCCee_119_stau_1m_ctau_ecm_240"

    "FCCee_100_stau_5m_ctau_ecm_240"
    "FCCee_105_stau_5m_ctau_ecm_240"
    "FCCee_110_stau_5m_ctau_ecm_240"
    "FCCee_115_stau_5m_ctau_ecm_240"
    "FCCee_118_stau_5m_ctau_ecm_240"
    "FCCee_119_stau_5m_ctau_ecm_240"

    # "FCCee_100_stau_6m_ctau_ecm_240"
    # "FCCee_105_stau_6m_ctau_ecm_240"
    # "FCCee_110_stau_6m_ctau_ecm_240"
    # "FCCee_115_stau_6m_ctau_ecm_240"
    # "FCCee_118_stau_6m_ctau_ecm_240"
    # "FCCee_119_stau_6m_ctau_ecm_240"

    # "FCCee_100_stau_10m_ctau_ecm_240"
    # "FCCee_105_stau_10m_ctau_ecm_240"
    # "FCCee_110_stau_10m_ctau_ecm_240"
    # "FCCee_115_stau_10m_ctau_ecm_240"
    # "FCCee_118_stau_10m_ctau_ecm_240"
    # "FCCee_119_stau_10m_ctau_ecm_240"

    # "FCCee_100_stau_20m_ctau_ecm_240"
    # "FCCee_105_stau_20m_ctau_ecm_240"
    # "FCCee_110_stau_20m_ctau_ecm_240"
    # "FCCee_115_stau_20m_ctau_ecm_240"
    # "FCCee_118_stau_20m_ctau_ecm_240"
    # "FCCee_119_stau_20m_ctau_ecm_240"

    "FCCee_100_stau_50m_ctau_ecm_240"
    "FCCee_105_stau_50m_ctau_ecm_240"
    "FCCee_110_stau_50m_ctau_ecm_240"
    "FCCee_115_stau_50m_ctau_ecm_240"
    "FCCee_118_stau_50m_ctau_ecm_240"
    "FCCee_119_stau_50m_ctau_ecm_240"

    # "FCCee_120_stau_5m_ctau_ecm_365"
    # "FCCee_130_stau_5m_ctau_ecm_365"
    # "FCCee_140_stau_5m_ctau_ecm_365"
    # "FCCee_150_stau_5m_ctau_ecm_365"
    # "FCCee_160_stau_5m_ctau_ecm_365"
    # "FCCee_170_stau_5m_ctau_ecm_365"
    # "FCCee_180_stau_5m_ctau_ecm_365"

    # "FCCee_120_stau_10m_ctau_ecm_365"
    # "FCCee_130_stau_10m_ctau_ecm_365"
    # "FCCee_140_stau_10m_ctau_ecm_365"
    # "FCCee_150_stau_10m_ctau_ecm_365"
    # "FCCee_160_stau_10m_ctau_ecm_365"
    # "FCCee_170_stau_10m_ctau_ecm_365"
    # "FCCee_180_stau_10m_ctau_ecm_365"

    # "FCCee_120_stau_20m_ctau_ecm_365"
    # "FCCee_130_stau_20m_ctau_ecm_365"
    # "FCCee_140_stau_20m_ctau_ecm_365"
    # "FCCee_150_stau_20m_ctau_ecm_365"
    # "FCCee_160_stau_20m_ctau_ecm_365"
    # "FCCee_170_stau_20m_ctau_ecm_365"
    # "FCCee_180_stau_20m_ctau_ecm_365"

    # "FCCee_120_stau_50m_ctau_ecm_365"
    # "FCCee_130_stau_50m_ctau_ecm_365"
    # "FCCee_140_stau_50m_ctau_ecm_365"
    # "FCCee_150_stau_50m_ctau_ecm_365"
    # "FCCee_160_stau_50m_ctau_ecm_365"
    # "FCCee_170_stau_50m_ctau_ecm_365"
    # "FCCee_180_stau_50m_ctau_ecm_365"
)

# ============================================================
# Initial information
# ============================================================

echo "============================================================"
echo "Configuration"
echo "============================================================"
echo "DRY_RUN:          ${DRY_RUN}"
echo "Events:           ${NEVENTS}"
echo "Gravitino mass:   ${GRAVITINO_MASS} GeV"
echo "Lifetime script:  ${LIFETIME_SCRIPT}"
echo "============================================================"
echo

if [[ "$DRY_RUN" == true ]]; then
    echo "*** DRY RUN: no files will be modified ***"
else
    echo "*** LIVE RUN: files WILL be modified ***"
fi

echo

# ============================================================
# Check lifetime.py
# ============================================================

if [[ ! -f "$LIFETIME_SCRIPT" ]]; then
    echo "ERROR: lifetime script not found:"
    echo "       ${LIFETIME_SCRIPT}"
    exit 1
fi

# ============================================================
# Process selected folders only
# ============================================================

for DIR_NAME in "${FOLDERS[@]}"; do

    # ========================================================
    # Generate MadGraph process for this folder
    # ========================================================

    if [[ ! -d "${DIR_NAME}" ]]; then

        echo "Generating MadGraph process: ${DIR_NAME}"

        cat > "${MG5_GENERATE_CARD}" <<EOF
import model ${MG5_MODEL}
generate e+ e- > ta1- ta1+
output ${DIR_NAME}
exit
EOF

        ${MG5} "${MG5_GENERATE_CARD}"

        rm -f "${MG5_GENERATE_CARD}"

    else
        echo "MadGraph directory already exists:"
        echo "  ${DIR_NAME}"
    fi

    DIR="${DIR_NAME}/"

    # ========================================================
    # Checks and pre-calculations
    # ========================================================

    # --------------------------------------------------------
    # Check directory
    # --------------------------------------------------------

    if [[ ! -d "$DIR" ]]; then
        echo "WARNING: directory not found: ${DIR_NAME}"
        exit 1
    fi

    # --------------------------------------------------------
    # Extract parameters from folder name
    #
    # Expected:
    #
    # FCCee_<mass>_stau_<ctau>m_ctau_ecm_<energy>
    # --------------------------------------------------------

    if [[ "$DIR_NAME" =~ ^FCCee_([0-9]+([.][0-9]+)?)_stau_([0-9]+([.][0-9]+)?)m_ctau_ecm_([0-9]+([.][0-9]+)?)$ ]]; then

        STAU_MASS="${BASH_REMATCH[1]}"
        CTAU_M="${BASH_REMATCH[3]}"
        ECM="${BASH_REMATCH[5]}"

    else
        echo "ERROR: invalid folder name:"
        echo "       ${DIR_NAME}"
        exit 1
    fi

    # --------------------------------------------------------
    # Calculate derived quantities
    # --------------------------------------------------------

    EBEAM=$(python3 -c "print(${ECM} / 2)")
    CTAU_MM=$(python3 -c "print(${CTAU_M} * 1000)")

    # --------------------------------------------------------
    # Calculate decay width
    # --------------------------------------------------------

    WIDTH=$(python3 "$LIFETIME_SCRIPT" --ctau "$CTAU_M")

    # --------------------------------------------------------
    # Card paths
    # --------------------------------------------------------

    CARDS="${DIR}/Cards"

    RUN_CARD="${CARDS}/run_card.dat"
    PARAM_CARD="${CARDS}/param_card.dat"

    PYTHIA_DEFAULT="${CARDS}/pythia8_card_default.dat"
    PYTHIA_CARD="${CARDS}/pythia8_card.dat"

    # --------------------------------------------------------
    # Check required files
    # --------------------------------------------------------

    if [[ ! -f "$RUN_CARD" ]]; then
        echo "ERROR: missing card:"
        echo "       ${RUN_CARD}"
        exit 1
    fi

    if [[ ! -f "$PARAM_CARD" ]]; then
        echo "ERROR: missing card:"
        echo "       ${PARAM_CARD}"
        exit 1
    fi

    if [[ ! -f "$PYTHIA_DEFAULT" ]]; then
        echo "ERROR: missing default Pythia8 card:"
        echo "       ${PYTHIA_DEFAULT}"
        exit 1
    fi

    # ========================================================
    # Display configuration
    # ========================================================

    echo
    echo "============================================================"
    echo "Folder: ${DIR_NAME}"
    echo "============================================================"
    echo "Stau mass:       ${STAU_MASS} GeV"
    echo "cτ:              ${CTAU_M} m"
    echo "ECM:             ${ECM} GeV"
    echo "Beam 1:          ${EBEAM} GeV"
    echo "Beam 2:          ${EBEAM} GeV"
    echo "Pythia8 tau0:    ${CTAU_MM} mm"
    echo "Decay width:     ${WIDTH}"
    echo "Events:          ${NEVENTS}"
    echo

    # ========================================================
    # run_card.dat
    # ========================================================

    if [[ "$DRY_RUN" == true ]]; then

        echo "[DRY RUN] Would modify ${RUN_CARD}:"
        echo "  ebeam1        -> ${EBEAM} GeV"
        echo "  ebeam2        -> ${EBEAM} GeV"
        echo "  nevents       -> ${NEVENTS}"
        echo "  time_of_flight -> 1.0 mm"

    else

        # Beam 1 energy
        sed -i -E \
            "s/^[[:space:]]*[^[:space:]]+[[:space:]]*=[[:space:]]*ebeam1([[:space:]]*!.*)?$/     ${EBEAM}     = ebeam1\1/" \
            "$RUN_CARD"

        # Beam 2 energy
        sed -i -E \
            "s/^[[:space:]]*[^[:space:]]+[[:space:]]*=[[:space:]]*ebeam2([[:space:]]*!.*)?$/     ${EBEAM}     = ebeam2\1/" \
            "$RUN_CARD"

        # Number of events
        sed -i -E \
            "s/^[[:space:]]*[^[:space:]]+[[:space:]]*=[[:space:]]*nevents([[:space:]]*!.*)?$/     ${NEVENTS}     = nevents\1/" \
            "$RUN_CARD"

        # Time of flight threshold
        sed -i -E \
            "s/^[[:space:]]*[^[:space:]]+[[:space:]]*=[[:space:]]*time_of_flight([[:space:]]*!.*)?$/     1.0     = time_of_flight\1/" \
            "$RUN_CARD"

    fi

    # ========================================================
    # param_card.dat
    # ========================================================

    if [[ "$DRY_RUN" == true ]]; then

        echo "[DRY RUN] Would modify ${PARAM_CARD}:"
        echo "  Stau mass       -> ${STAU_MASS} GeV"
        echo "  Gravitino mass  -> ${GRAVITINO_MASS} GeV"
        echo "  Stau width      -> ${WIDTH}"
        echo "  Stau decay      -> 1000015 -> 15 + 1000049"

    else

        python3 - "$PARAM_CARD" "$STAU_MASS" "$GRAVITINO_MASS" "$WIDTH" <<'PY'
import sys
import re

filename = sys.argv[1]
stau_mass = float(sys.argv[2])
gravitino_mass = float(sys.argv[3])
width = sys.argv[4]

with open(filename, "r") as f:
    lines = f.readlines()

output = []

in_mass_block = False
skip_stau_decay = False
stau_decay_found = False

for line in lines:

    # ----------------------------------------------------
    # Detect blocks
    # ----------------------------------------------------

    if re.match(r'^\s*Block\s+mass\b', line, re.IGNORECASE):
        in_mass_block = True
        output.append(line)
        continue

    if re.match(r'^\s*Block\s+', line, re.IGNORECASE):
        in_mass_block = False

    # ----------------------------------------------------
    # MASS block
    # ----------------------------------------------------

    if in_mass_block:

        # Stau mass: PDG 1000015
        if re.match(r'^\s*1000015\s+', line):
            output.append(
                f"  1000015 {stau_mass:.6e} # Msl3\n"
            )
            continue

        # Gravitino mass: PDG 1000049
        if re.match(r'^\s*1000049\s+', line):
            output.append(
                f"  1000049 {gravitino_mass:.6e} # Mgrv\n"
            )
            continue

    # ----------------------------------------------------
    # Stau decay replacement
    # ----------------------------------------------------

    if re.match(r'^\s*DECAY\s+1000015\b', line):

        output.append(
            f"DECAY 1000015 {width} # ~tau^-_1\n"
        )

        output.append(
            "    1.000000e+00 2 15 1000049  # ~tau^-_1 -> tau^- grv\n"
        )

        stau_decay_found = True
        skip_stau_decay = True
        continue

    # ----------------------------------------------------
    # Remove old stau decay channels
    # ----------------------------------------------------

    if skip_stau_decay:

        # End of stau decay block
        if re.match(r'^\s*DECAY\s+', line):
            skip_stau_decay = False
            output.append(line)
            continue

        # Skip old decay channels
        if re.match(
            r'^\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\s+\d+\s+',
            line
        ):
            continue

        output.append(line)
        continue

    output.append(line)

if not stau_decay_found:
    raise RuntimeError("Could not find DECAY 1000015 in param_card.dat")

with open(filename, "w") as f:
    f.writelines(output)

PY

    fi

    # ========================================================
    # pythia8_card.dat
    # ========================================================

    # --------------------------------------------------------
    # Remove existing pythia8_card.dat if it exists
    # --------------------------------------------------------

    if [[ -f "$PYTHIA_CARD" ]]; then

        if [[ "$DRY_RUN" == true ]]; then
            echo "[DRY RUN] Would rm ${PYTHIA_CARD}:"
        else
            echo "WARNING: ${PYTHIA_CARD} already exists."
            echo "         Removing it before recreating."

            rm -f "$PYTHIA_CARD"
        fi
    fi

    # --------------------------------------------------------
    # Modify existing pythia8_card.dat
    # --------------------------------------------------------
    
    if [[ "$DRY_RUN" == true ]]; then

        echo "[DRY RUN] Would create:"
        echo "  ${PYTHIA_CARD}"
        echo "  by copying ${PYTHIA_DEFAULT}"
        echo
        echo "[DRY RUN] Would modify output type from hepmc.gz to hepmc"
        echo
        echo "[DRY RUN] Would append to ${PYTHIA_CARD}:"
        echo "  PartonLevel:ISR = on"
        echo "  PartonLevel:FSR = on"
        echo
        echo "  SUSY:all = on"
        echo
        echo "  1000015:tau0 = ${CTAU_MM}   # stau cτ in mm (${CTAU_M} m)"
        echo "  1000015:mayDecay = on"

    else

        # Copy default card
        cp "$PYTHIA_DEFAULT" "$PYTHIA_CARD"

        # Change HepMC output filename
        sed -i -E \
            "s|^[[:space:]]*HEPMCoutput:file[[:space:]]*=.*|HEPMCoutput:file         = hepmc|" \
            "$PYTHIA_CARD"

        # Append Pythia8 configuration
        cat >> "$PYTHIA_CARD" <<EOF

PartonLevel:ISR = on
PartonLevel:FSR = on

SUSY:all = on

1000015:tau0 = ${CTAU_MM}   # stau cτ in mm (${CTAU_M} m)
1000015:mayDecay = on
EOF

    fi

    # ========================================================
    # Launch MadGraph
    # ========================================================

    if [[ "$DRY_RUN" == true ]]; then

        echo "[DRY RUN] Would launch:"
        echo "  ${DIR_NAME}"

    else

        echo "Launching ${DIR_NAME}"

        cat > "${MG5_LAUNCH_CARD}" <<EOF
launch ${DIR_NAME}
set shower Pythia8
EOF

        ${MG5} "${MG5_LAUNCH_CARD}"

        rm -f "${MG5_LAUNCH_CARD}"

    fi

    echo "Done: ${DIR_NAME}"

done

echo
echo "============================================================"

if [[ "$DRY_RUN" == true ]]; then
    echo "DRY RUN complete."
    echo "No files were modified or created."
    echo
    echo "To perform the modifications, set:"
    echo "    DRY_RUN=false"
else
    echo "All selected folders have been processed."
fi

echo "============================================================"
#!/bin/bash

# BEFORE RUNNING: source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh

# === Environment ===
export MAIN_PATH=/data/dust/user/creusett/SummerSchool
export USER_PATH=$MAIN_PATH/Signal

DELPHES_PATH=$USER_PATH/delphes
K4_INSTALL=$USER_PATH/k4simdelphes/install

export PATH=$K4_INSTALL/bin:$DELPHES_PATH/bin:$PATH
export LD_LIBRARY_PATH=$K4_INSTALL/lib64:$K4_INSTALL/lib:$DELPHES_PATH/lib:$LD_LIBRARY_PATH

# === Delphes cards ===
CARD_TCL=$DELPHES_PATH/cards/IDEA/card_IDEA.tcl
EDM4HEP_TCL=$DELPHES_PATH/cards/IDEA/edm4hep_IDEA.tcl

# === Output directory ===
OUTPUT_DIR=$MAIN_PATH/Data/k4SD
mkdir -p $OUTPUT_DIR

# === List of samples ===
SAMPLES=(
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

    # "FCCee_100_stau_6m_ctau_ecm_240"
    # "FCCee_105_stau_6m_ctau_ecm_240"
    # "FCCee_110_stau_6m_ctau_ecm_240"
    # "FCCee_115_stau_6m_ctau_ecm_240"
    # "FCCee_118_stau_6m_ctau_ecm_240"
    # "FCCee_119_stau_6m_ctau_ecm_240"

    "FCCee_100_stau_5m_ctau_ecm_240"
    "FCCee_105_stau_5m_ctau_ecm_240"
    "FCCee_110_stau_5m_ctau_ecm_240"
    "FCCee_115_stau_5m_ctau_ecm_240"
    "FCCee_118_stau_5m_ctau_ecm_240"
    "FCCee_119_stau_5m_ctau_ecm_240"

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


# === Loop over all samples ===
for SAMPLE in "${SAMPLES[@]}"; do

    INPUT_HEPMC=$USER_PATH/mc-pythia-main/${SAMPLE}/Events/run_01/tag_1_pythia8_events.hepmc
    OUTPUT_ROOT=$OUTPUT_DIR/${SAMPLE}.root
    
    if [ -f "$OUTPUT_ROOT" ]; then
        echo "Output already exists, skipping $SAMPLE"
        continue
    fi

    echo "----------------------------------------------------"
    echo "Running Delphes for sample: $SAMPLE"
    echo "INPUT: $INPUT_HEPMC"
    echo "OUTPUT: $OUTPUT_ROOT"
    echo "----------------------------------------------------"

    $K4_INSTALL/bin/DelphesHepMC_EDM4HEP $CARD_TCL $EDM4HEP_TCL $OUTPUT_ROOT $INPUT_HEPMC || true

done

echo "All samples processed!"

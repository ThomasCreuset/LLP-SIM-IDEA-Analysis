#!/bin/bash

# BEFORE RUNNING: source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh

export USER_PATH=/data/dust/user/creusett/SummerSchool
export DELPHES_PATH=$USER_PATH/delphes
export PATH=$DELPHES_PATH/bin:$PATH
export LD_LIBRARY_PATH=$DELPHES_PATH/lib:$LD_LIBRARY_PATH

echo "USER_PATH=$USER_PATH"
echo "DELPHES_PATH=$DELPHES_PATH"

## modify the paths :

K4SIMDELPHES_DIR=$USER_PATH/k4simdelphes
BUILD_DIR=$USER_PATH/k4_build
INSTALL_DIR=$USER_PATH/k4stuff/install

echo "Cleaning previous build/install..."
rm -rf $BUILD_DIR $INSTALL_DIR
mkdir -p $BUILD_DIR $INSTALL_DIR
cd $BUILD_DIR

echo "Configuring k4SimDelphes with local Delphes..."
cmake $K4SIMDELPHES_DIR \
  -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR \
  -DCMAKE_PREFIX_PATH="$CMAKE_PREFIX_PATH;$DELPHES_PATH" \
  -DDELPHES_DIR=$DELPHES_PATH \
  -DCMAKE_CXX_FLAGS="-I$DELPHES_PATH/external"
  
#echo "Building k4SimDelphes..."
make -j8
make install

export LD_LIBRARY_PATH=$INSTALL_DIR/lib64:$INSTALL_DIR/lib:$LD_LIBRARY_PATH
export PATH=$INSTALL_DIR/bin:$PATH

#echo "Checking linked Delphes library..."
ldd $INSTALL_DIR/bin/DelphesHepMC_EDM4HEP | grep libDelphes

# Run DelphesHepMC_EDM4HEP with the IDEA CARD + IDEA_EDM4HEP_CONVERSION_CARD + OUTPUT_DIRECTORY + INPUT DIRECTORY OF HEPMC FILE
#echo "Running DelphesHepMC_EDM4HEP..."
#DelphesHepMC_EDM4HEP  $DELPHES_PATH/cards/IDEA/card_IDEA.tcl \
#                      $DELPHES_PATH/cards/IDEA/edm4hep_IDEA.tcl \
#                      $K4SIMDELPHES_DIR/FCCee_mass_stau_lifetime_ctau_ecm_com.root \
#                      $USER_PATH/mc-pythia-main/FCCee_mass_stau_lifetime_ctau_ecm_com/Events/run_03/tag_1_pythia8_events.hepmc
#echo "Done!" #Output written to $OUTPUT_ROOT"

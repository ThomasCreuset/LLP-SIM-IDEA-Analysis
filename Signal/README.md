# How to use the Signal Folder

! TO DO !

## Setup

- Start a new shell
- Go to `FCCAnalysis/`
- Use `source setup.sh`
- Run `compileDelphes`
- Run `confk4SD`
- Run `compilek4SD`
- Run `confFCC`
- Run `compileFCC`

## Running

### mc-pythia

Optional:
- Start a new shell
- Go to `FCCAnalysis/`
- Use `source setup.sh`

Needed:
- Go to `mc-pythia-main`
- Modify the list of processes in `run_all_madGraph.sh`
- Run `bash run_all_madGraph.sh`

### k4simdelphes

*Run mc-pythia first.*

- Start a new shell
- Go to `FCCAnalysis/`
- Use `source setup.sh`
- Go to `k4simdelphes/`
- Modify the list of processes and the `MAIN_PATH` variable in `run_delphes_all.sh`
- Run `bash run_delphes_all.sh`

### Stage1

*Run k4simdelphes first.*

- Start a new shell
- Go to `FCCAnalysis/`
- Use `source setup.sh`
- Go to `FCCAnalyses/examples/FCCee/bsm/LLPs/Stau`
- Modify the list of processes and paths in `analysis_stage1.py`
- Run `fccanalysis run analysis_stage1.py`

If you want to run on Condor:
- Start a new shell
- Go to `FCCAnalysis/`
- Use `source setup.sh`
- Go to `FCCAnalyses/examples/FCCee/bsm/LLPs/Stau`
- Modify the paths in `analysis_stage1.py`
- Modify the list of process in `MySampleList.txt`
- Run `condor_submit signalOnCondor.sub`

### Final

*Run stage1 for Signal and stage_pre1 for Background first.*

- Start a new shell
- Go to `FCCAnalysis/`
- Use `source setup.sh`
- Go to `FCCAnalyses/examples/FCCee/bsm/LLPs/Stau`
- Modify the list of processes, the luminosity and paths in `analysis_final.py` (if you still have the madGraphs files, you can put fake values for cross sections and use the command `bash updateFinal.sh` to automatically update them)
- Run `fccanalysis final analysis_final.py -o OUTPUT_DIR_NAME`, where `OUTPUT_DIR_NAME` correspond to the name of the subfolder in `Data/FCCAna/Final/`

### Plots

*Run final first.*

- Start a new shell
- Go to `FCCAnalysis/`
- Use `source setup.sh`
- Go to `FCCAnalyses_pre/examples/FCCee/bsm/LLPs/Stau`
- Modify the list of processes and paths in `analysis_plots.py` and make the luminosity match the one of `analysis_final.py`
- Run `fccanalysis plots  analysis_plots.py -i INPUT_DIR -o OUTPUT_DIR_NAME`, where `INPUT_DIR` and `OUTPUT_DIR_NAME` corespond to the name of the subfolder in `Data/FCCAna/Final/` (if none specify it will output directly in `Final`, which is fine if you do not do multiple selections)

## In case of modifications of the code

### Of Delphes

- Start a new shell
- Go to `FCCAnalysis_pre/`
- Use `source setup.sh`
- Run `compileDelphes`
- Run `confFCC`
- Run `compileFCC`

### Of FCCAnalysis

- Start a new shell
- Go to `FCCAnalysis_pre/`
- Use `source setup.sh`
- (Run `confFCC`)
- Run `compileFCC`

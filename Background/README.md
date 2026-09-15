# How to use the Background Folder

## Setup

- Start a new shell
- Go to `FCCAnalysis_pre/`
- Use `source setup.sh`
- Run `compileDelphes`
- Run `confFCC`
- Run `compileFCC`

## Running the background

- Start a new shell
- Go to `FCCAnalysis_pre/`
- Use `source setup.sh`
- Go to `FCCAnalyses_pre/examples/FCCee/bsm/LLPs/Stau`
- Modify the list of processes and paths in `analysis_stage_pre_1.py`
- Run `fccanalysis run analysis_stage_pre1.py`

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

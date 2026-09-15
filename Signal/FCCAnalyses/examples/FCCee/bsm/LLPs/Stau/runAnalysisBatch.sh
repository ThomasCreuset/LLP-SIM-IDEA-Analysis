#!/bin/bash

theSample=$1

source /data/dust/user/creusett/SummerSchool/Signal/FCCAnalyses/setup.sh

fccanalysis run analysis_stage1.py -- --sample $theSample
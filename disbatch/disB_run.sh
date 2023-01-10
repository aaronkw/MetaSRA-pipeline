#!/bin/bash
 
id=$1
shift

SRC_DIR=~/projects/MetaSRA-pipeline/           # the directory of run_pipeline.py
LOG_DIR=$SRC_DIR/disbatch/log                  # the directory of log files
VENV_DIR=$SRC_DIR/env_python38/                # the directory of virtual environment. We use python virtual environment here.
                                               # you can use a different virutal environment and should change directory and command accordingly
mkdir -p "$LOG_DIR"

module purge
module load python3

#activate the python virtual environment created beforehand
source $VENV_DIR/bin/activate

#run the command
echo "python $SRC_DIR/run_pipeline.py $@ > $LOG_DIR/${id}.out 2> $LOG_DIR/${id}.log"
#python $SRC_DIR/run_pipeline.py $@ > $LOG_DIR/${id}.out 2> $LOG_DIR/${id}.log

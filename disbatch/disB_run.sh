#!/bin/bash
 
id=$1
shift

module purge
module load python3

DIR_LOG=./log
mkdir -p "$DIR_LOG"

#go to the project source directory 
cd ~/projects/MetaSRA-pipeline/
#activate a python virtual environment we have created 
#if you use a differnt virutal environment, you should change command accordingly
source ./env_python38/bin/activate

python run_pipeline.py $@ > $DIR_LOG/${id}.out 2> $DIR_LOG/${id}.log

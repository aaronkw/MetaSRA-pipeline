#!/bin/bash
 
id=$1
shift

module purge
module load python3

DIR_LOG=./log
mkdir -p "$DIR_LOG"

cd /mnt/home/yliu/projects/MetaSRA-pipeline/
source ./env_python38/bin/activate

python run_pipeline.py $@ > $DIR_LOG/${id}.out 2> $DIR_LOG/${id}.log

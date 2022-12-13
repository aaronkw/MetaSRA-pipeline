#!/bin/bash
 
id=$1
shift
module purge
module load python3

cd /mnt/home/yliu/projects/MetaSRA-pipeline/
source ./env_python38/bin/activate

python run_pipeline.py $@ > ./ceph_yliu_data/results/${id}.out 2> ./ceph_yliu_data/log/${id}.log

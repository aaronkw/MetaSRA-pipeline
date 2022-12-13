module load disBatch/beta
mkdir ./ceph_yliu_data/log
mkdir ./ceph_yliu_data/results
sbatch -p scc -N 3 -c 1 --mincpus=100 disBatch -p ./ceph_yliu_data/log disB_tasks_all
#./ceph_yliu_data/log/disB_tasks_disBatch_220922145716_553_dbUtil.sh --mon


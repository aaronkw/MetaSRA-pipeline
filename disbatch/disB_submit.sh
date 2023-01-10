module load disBatch/beta

DISB_FILE=disB_tasks_all
DIR_LOG=./log
mkdir -p $DIR_LOG

sbatch -p scc -N 3 -c 1 --mincpus=100 disBatch -p $DIR_LOG $DISB_FILE
#use the following commands to start monitoring interface
#replace [ids] with real ones
#./log/disB_tasks_disBatch_[ids]_dbUtil.sh --mon


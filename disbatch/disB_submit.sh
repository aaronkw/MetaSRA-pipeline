module load disBatch/beta

if [[ $# == 0 ]] 
then
   DISB_FILE='./disB_tasks_all'
else
   DISB_FILE=$1
fi
DISB_LOG=./log
mkdir -p $DISB_LOG

echo "sbatch -p scc -N 3 -c 1 --mincpus=100 disBatch -p $DISB_LOG $DISB_FILE"
sbatch -p scc -N 3 -c 1 --mincpus=100 disBatch -p $DISB_LOG $DISB_FILE
#use the following commands to start monitoring interface
#replace [ids] with real ones
#./log/disB_tasks_disBatch_[ids]_dbUtil.sh --mon


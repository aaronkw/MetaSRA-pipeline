This directory includes the tools that enable users to use [disbatch](https://github.com/flatironinstitute/disBatch), which is designed to submit a large number of tasks to slurm.

First, we generate a disBatch taskfile by executing

`python createDisBTasks.py`

You may modify `INPUT_DIR` and `TASKOUT_DIR` inside `createDisBTasks.py`and make them the correct input and output directories of python program `run_pipeline.py` in your environment.  

The taskfile `disB_tasks_all` is generated under the current directory. 
Each line in the file is corresponding to a slurm task. 
We have a task for each non-empty data file under directory `INPUT_DIR`.
Each line is a command executing `disB_run.sh` such as,

`./disB_run.sh SRP058038 -o ~/ceph/projects/MetaSRA-pipeline/data/ /mnt/ceph/users/humanbase/data/meta/datasets/SRP058038.json`,

where `SRP058038` is the task id used by disBatch and the remained parameters are passed to the python program `run_pipeline.py`. 

The shell script `disB_run.sh` sets up the execution environment and run the python program `run_pipeline.py`.
We use module and python virtual environment here. You may need to change the script according to your environment.

Finally, you can execute

`. ./disB_submit.sh"`

to  submit the disBatch job to Slurm. 

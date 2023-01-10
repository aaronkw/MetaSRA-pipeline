This directory includes the tools that enable users to use [disBatch](https://github.com/flatironinstitute/disBatch), which is designed to submit a large number of tasks to Slurm. In this case, we need to run `run_pipeline.py` for each input file. 

## First, generate a disBatch taskfile 

Execute

`python createDisBTasks.py`

to generate disBatch taskfile `disB_tasks_all` under the current directory.

Inside 'createDisBTasks.py`, you may need to modify `INPUT_DIR` and `TASKOUT_DIR` to point to the correct input and output directories of `run_pipeline.py` in your environment.  

In taskfile `disB_tasks_all`,
each line is corresponding to a [Slurm](https://slurm.schedmd.com/documentation.html) task. 
We have a line for each non-empty data file under directory `INPUT_DIR`.
Each line is a command executing `disB_run.sh` such as,

`./disB_run.sh SRP058038 -o ~/ceph/projects/MetaSRA-pipeline/data/ /mnt/ceph/users/humanbase/data/meta/datasets/SRP058038.json`,

where `SRP058038` is the task id used by disBatch and the remained parameters are passed to the program `run_pipeline.py`. In specific, `~/ceph/projects/MetaSRA-pipeline/data/` is the output directory (defined by `TASKOUT_DIR` in `createDisBTasks.py`) and `/mnt/ceph/users/humanbase/data/meta/datasets/SRP058038.json` is the input file (`/mnt/ceph/users/humanbase/data/meta/datasets/` defined by `INPUT_DIR` in `createDisBTasks.py`). 

The shell script `disB_run.sh` sets up the execution environment and run the python program `run_pipeline.py`.
We use module and python virtual environment here. You may need to change the script according to your environment.

## Then, submit the disBatch job to Slurm

Execute

`. ./disB_submit.sh`

to  submit the disBatch job to Slurm. 

You may need to change the script to ask for a different set of Slurm resources and/or use different disBatch taskfile other than 'disB_tasks_all`.

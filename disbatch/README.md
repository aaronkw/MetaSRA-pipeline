This directory includes that enable users to use [disbatch](https://github.com/flatironinstitute/disBatch), which is designed to submit a large number of tasks to slurm.

First, we generate a disBatch taskfile by executing

`python createDisBTasks.py`

The taskfile `disB_tasks_all` is generated under the current directory. 
Each line in the file is corresponding to a slurm task. 
We have a task for each non-empty data file under directory `INPUT_DIR`, which is defined and can be modified inside createDisBTasks.py. 
Each line in `disB_tasks_all` is a command executing `disB_run.sh` such as,

`./disB_run.sh SRP058038 -o ~/ceph/projects/MetaSRA-pipeline/data/ /mnt/ceph/users/humanbase/data/meta/datasets/SRP058038.json`,

where `SRP058038` is the task id used by disBatch and the remained parameters are passed to a python program `run_pipeline.py`. 
Parameters `-o ~/ceph/projects/MetaSRA-pipeline/data/` define the output directory of `run_pipeline.py`.
This value is defined as `TASKOUT_DIR` and can be changed inside `createDisBTasks.py`.

Finally, you can execute 

`. ./disB_submit.sh"`

to  submit the disBatch job to Slurm. 

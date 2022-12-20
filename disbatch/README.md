This directory include the tools that enable the user to use disbatch [a link](https://github.com/flatironinstitute/disBatch), which is designed to submit a large number of tasks to slurm.

First, we generate a disBatch taskfile by 
`python createDisBTasks.py`

The generated taskfile "disB_tasks_all" is under the current directory. 
Each line in this taskfile is corresponding to a slurm task. 
We have a task for each non-empty data file under "INPUT_DIR" directory, which is defined and can be modified inside createDisBTasks.py. 

If you check the content of "disB_tasks_all", you will see each line is a command executing "disB_run.sh" such as,
`./disB_run.sh SRP058038 -o ~/ceph/projects/MetaSRA-pipeline/data/ /mnt/ceph/users/humanbase/data/meta/datasets/SRP058038.json`,
where "SRP058038" is an id used by disBatch and the remained parameters are passed to the python program "run_pipeline.py" inside "disB_run.sh". 
"-o ~/ceph/projects/MetaSRA-pipeline/data/" defines the output directory of "run_pipeline.py".
This value is defined as "TASKOUT_DIR" and can be changed inside "createDisBTasks.py".

Finally, you can execute 
`. ./disB_submit.sh"`
to  submit the disBatch job to Slurm. 

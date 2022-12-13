This directory include the tools that make use of disBatch.

"python createDisBTasks.py" will generate a disBatch taskfile "disB_tasks_all" that includes all the input files under /mnt/ceph/users/humanbase/data/meta/datasets/.

Inside disBatch taskfile, "disB_run.sh" is used to run with an input file. In turn, "disB_run.sh" sets up environment and calls "python run_pipeline.py" with parameters.

". ./disB_submit.sh" will finally submit the disBatch job to Slurm.

The results are saved under /mnt/ceph/users/yliu/projects/MetaSRA-pipeline/data/

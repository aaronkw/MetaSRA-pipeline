This directory includes the tools that enable users to use [disBatch](https://github.com/flatironinstitute/disBatch), 
which is designed to submit a large number of tasks to Slurm. 
In this case, we shall run `run_pipeline.py` for each input file under a input directory. 

## First, generate a disBatch taskfile 

Execute program `createDisBTasks.py' to generate a disBatch taskfile.

```
Usage: createDisBTasks.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir=INPUT_DIR
                        The directory to get input files for run_pipeline.py
  -o OUTPUT_DIR, --output_dir=OUTPUT_DIR
                        The directory to store output files for run_pipeline.py
  -t TASKFILE, --taskfile=TASKFILE
                        The file name of disBatch taskfile
```

If you do not provide argument values in the command line, the default value of each parameter will be used. For example, the default value of TASKFILE is `./disB_tasks_all`.

In the generated taskfile,
each line is corresponding to a [Slurm](https://slurm.schedmd.com/documentation.html) task. 
We have a line for each non-empty data file under directory defined by INPUT_DIR.
Each line is a command executing a shell script `disB_run.sh` such as,

`./disB_run.sh SRP058038 -o ~/ceph/projects/MetaSRA-pipeline/data/ /mnt/ceph/users/humanbase/data/meta/datasets/SRP058038.json`

where `SRP058038` is the task id used by disBatch and the remained parameters are passed to the program `run_pipeline.py`. In specific, `~/ceph/projects/MetaSRA-pipeline/data/` is the output directory and `/mnt/ceph/users/humanbase/data/meta/datasets/SRP058038.json` is the input file. 

The shell script `disB_run.sh` sets up the execution environment and run the python program `run_pipeline.py`.
We use module and python virtual environment here. You may need to change the script according to your environment.

## Then, submit the disBatch job to Slurm

Execute

`. ./disB_submit.sh [TASKFILE]`

to submit the disBatch job defined in a taskfile to Slurm. If TASKFILE is not provided, the default taskfile is `./disB_tasks_all`.

You may need to change the script to request a different set of Slurm resources to run the disBatch job.

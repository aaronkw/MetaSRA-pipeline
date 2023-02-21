from optparse import OptionParser
import glob, json, os, os.path, sys

DEF_INPUT_DIR  = '/mnt/ceph/users/humanbase/data/meta/datasets/'                #default input directory for run_pipeline.py
DEF_OUTPUT_DIR = '~/ceph/projects/MetaSRA-pipeline/data/'                       #default output directory for run_pipeline.py
DEF_TASKFILE   = './disB_tasks_all'                                                #default disBatch taskfile name

BIG_FILE_SIZE  = 300000           #when divide_big is set True, we will divide the files bigger than this size
SAMPLE_COUNT   = 2000             #                             each resulting file will have this number of samples

#create disbatch taskfile task_fname that include all the tasks for the input files under input_dir
#if divide_big is set to True, then the big input file will be divided into smaller ones
def createAllTask (input_dir=DEF_INPUT_DIR, output_dir=DEF_OUTPUT_DIR, task_fname=DEF_TASKFILE, divide_big=False):
    task_file = open(task_fname, 'w')
    big_files  = {}
    for file_name in glob.glob('{}/*.json'.format(input_dir)):
        checkFile (file_name, task_file, divide_big, output_dir)

    task_file.close()

#generate one task for a input file_name
def checkFile (file_name, task_file, divide_big, output_dir):
    head, tail = os.path.split(file_name)
    e, ext     = os.path.splitext(tail)
    size       = os.path.getsize(file_name)
    f_lst      = []
    if size==0:
       print("Ignore empty data file {}".format(file_name))
    elif (divide_big and size>BIG_FILE_SIZE):
       print("Divide big data file {} (size {})".format(file_name, size))
       lst   = []
       with open(file_name, "r") as f:
            lst = json.load(f)
       # SAMPLE_COUNT samples in a file
       for idx in range(0, len(lst), SAMPLE_COUNT):
           outf_name = "{}/{}_{}{}".format(output_dir, e, idx, ext)
           print("\t{}".format(outf_name))
           with open(outf_name, "w") as out_f:
               json.dump(lst[idx:idx+SAMPLE_COUNT], out_f)
               print("./disB_run.sh {}_{} -o {} {}".format(e, idx, output_dir, outf_name), file=task_file)
           f_lst.append(outf_name)
    else:
       print("./disB_run.sh {} -o {} {}".format(e, output_dir, file_name), file=task_file)
    return f_lst

#create disbatch taskfile "disB_tasks_failed" that include the task for the input files under input_dir
#which does not have a result file under output_dir
def createFailedTask (input_dir=DEF_INPUT_DIR, output_dir=DEF_OUTPUT_DIR, task_fname='disB_tasks_failed', divide_big=False):
    task_file = open(task_fname, 'w')
    big_files  = {}
    for file_name in glob.glob('{}/*.json'.format(input_dir)):
        head, tail = os.path.split(file_name)
        e, ext     = os.path.splitext(tail)
        out_file   = '{}/{}_meta.json'.format(output_dir, e)
        if not os.path.exists(out_file):
           print("Missing {}".format(out_file))
           f_lst      = checkFile(file_name, task_file, divide_big, output_dir)
           big_files[file_name] = f_lst
    task_file.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--input_dir",  default=DEF_INPUT_DIR,  help="The directory to get input files for run_pipeline.py")
    parser.add_option("-o", "--output_dir", default=DEF_OUTPUT_DIR, help="The directory to store output files for run_pipeline.py")
    parser.add_option("-t", "--taskfile",   default=DEF_TASKFILE,   help="The file name of disBatch taskfile")
    (options, args) = parser.parse_args()

    if not os.path.exists(options.input_dir):
        print ("INPUT DIRECTORY {} DOES NOT EXIST!".format(options.input_dir))
        sys.exit(1)
    if not os.path.exists(options.output_dir):
        print("Create output directory {}".format(options.output_dir))
        os.makedirs(options.output_dir)
    createAllTask(options.input_dir, options.output_dir, options.taskfile)
    #createFailedTask()

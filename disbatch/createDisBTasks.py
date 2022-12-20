import glob, json, os, os.path, sys

#You need need to modify INPUT_DIR, TASKOUT_DIR to point to the right directory
INPUT_DIR   = '/mnt/ceph/users/humanbase/data/meta/datasets/'
TASKOUT_DIR = '~/ceph/projects/MetaSRA-pipeline/data/'
BIG_FILE_SIZE = 300000           #when divide_big is set True, we will divide the files bigger than this size
SAMPLE_COUNT  = 2000             #                             each resulting file will have this number of samples

#create disbatch taskfile "disB_tasks_all" that include all the tasks for the input files under INPUT_DIR
#if divide_big is set to True, then the big input file will be divided into smaller ones
def createAllTask (task_fname='disB_tasks_all', divide_big=False):
    task_file = open(task_fname, 'w')
    big_files  = {}
    for file_name in glob.glob('{}/*.json'.format(INPUT_DIR)):
        checkFile (file_name, task_file, divide_big)

    #merge the result of big file
    #print("#DISBATCH BARRIER", file=task_file)
    #print("./disB_combine.sh {} -o {} {}".format("check_combine", TASKOUT_DIR, big_files), file=task_file)
    task_file.close()

#generate one task for a input file_name
def checkFile (file_name, task_file, divide_big):
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
           outf_name = "{}/{}_{}{}".format(TASKOUT_DIR, e, idx, ext)
           print("\t{}".format(outf_name))
           with open(outf_name, "w") as out_f:
               json.dump(lst[idx:idx+SAMPLE_COUNT], out_f)
               print("./disB_run.sh {}_{} -o {} {}".format(e, idx, TASKOUT_DIR, outf_name), file=task_file)
           f_lst.append(outf_name)
    else:
       print("./disB_run.sh {} -o {} {}".format(e, TASKOUT_DIR, file_name), file=task_file)
    return f_lst

#create disbatch taskfile "disB_tasks_failed" that include the task for the input files under INPUT_DIR
#which does not have a result file under TASKOUT_DIR
def createFailedTask (task_fname='disB_tasks_failed'):
    task_file = open(task_fname, 'w')
    big_files  = {}
    for file_name in glob.glob('{}/*.json'.format(INPUT_DIR)):
        head, tail = os.path.split(file_name)
        e, ext     = os.path.splitext(tail)
        out_file   = '{}/{}_meta.json'.format(TASKOUT_DIR, e)
        if not os.path.exists(out_file):
           print("Missing {}".format(out_file))
           f_lst      = checkFile(file_name, task_file)
           big_files[file_name] = f_lst
    task_file.close()

if __name__ == "__main__":
    if not os.path.exists(INPUT_DIR):
        print ("INPUT DIRECTORY {} DOES NOT EXIST!".format(INPUT_DIR))
        sys.exit(1)
    if not os.path.exists(TASKOUT_DIR):
        print("Create output directory {}".format(TASKOUT_DIR))
        os.makedirs(TASKOUT_DIR)
    createAllTask()
    #createFailedTask()

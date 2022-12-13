import glob, json, os.path, pandas, sys

INPUT_DIR  = '/mnt/ceph/users/humanbase/data/meta/datasets/'
TASKOUT_DIR = '/mnt/ceph/users/yliu/projects/MetaSRA-pipeline/data/'

def createAnnoTask ():
    task_file = open('disB_tasks_anno', 'w')
    df        = pandas.read_csv("./manual_annotations_ursa.csv", sep='\t', index_col='GSMID')
    exps      = set()
    for e in set(df['GSEID']):
        if ',' in e:
           exps.update([x.strip() for x in e.split(',')])
        else:
           exps.add(e)

    for e in exps:
        file_name = "{}/{}.json".format(INPUT_DIR,e)
        if os.path.exists(file_name):
           print("./disB_run.sh {} -o {} {}".format(e, TASKOUT_DIR, file_name), file=task_file)
        else:
           print ("{}: file not exists".format(file_name))
    task_file.close()

def checkFile (file_name, task_file, divide_big):
    head, tail = os.path.split(file_name)
    e, ext     = os.path.splitext(tail)
    size       = os.path.getsize(file_name)
    f_lst      = []
    if size==0:
       print("Ignore empty data file {}".format(file_name))
    elif (divide_big and size>300000):
       print("Divide big data file {} (size {})".format(file_name, size))
       lst   = []
       with open(file_name, "r") as f:
            lst = json.load(f)
       # 2000 samples in a file
       for idx in range(0, len(lst), 2000):
           outf_name = "{}/{}_{}{}".format(TASKOUT_DIR, e, idx, ext)
           print("\t{}".format(outf_name))
           with open(outf_name, "w") as out_f:
               json.dump(lst[idx:idx+2000], out_f)
               print("./disB_run.sh {}_{} -o {} {}".format(e, idx, TASKOUT_DIR, outf_name), file=task_file)
           f_lst.append(outf_name)
    else:
       print("./disB_run.sh {} -o {} {}".format(e, TASKOUT_DIR, file_name), file=task_file)
    return f_lst

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
    createAllTask()
    #createFailedTask()

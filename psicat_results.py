# test each psi type separately and in combination

from fileinfo import FileList
import pickle
import os.path
import os
import ast
from mclearn import *

# Initialize Directory and File Paths
dir_dataset = "/home/cloud/Documents/dataset_paper/dataset1"
dir_results = os.path.join(os.getcwd(), "psicat_results")
if not os.path.exists(dir_results):
    os.mkdir(dir_results)
objfile_benign = os.path.join(dir_results, 'db_benign.pkl')
objfile_malware = os.path.join(dir_results, 'db_malware.pkl')
objfile_dataset = os.path.join(dir_results, 'db_dataset.pkl')

fil_fv = os.path.join(dir_results, 'dataset1_feature_vector.csv')
fil_fl = os.path.join(dir_results, 'dataset1_feature_list.txt')

# Read the directories containing sample executable files
if not os.path.exists(objfile_benign):
    benign_dir = os.path.join(dir_dataset, "benign")
    print(benign_dir)
    fl_benign_dir = FileList(benign_dir)
    print(fl_benign_dir)
    fl_benign_dir.set_Class(1)
    fl_benign_dir.set_category('none')
    with open(objfile_benign, 'wb') as output:
        pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)
else:
    print("Reading benign dataset from pickle")
    with open(objfile_benign,'rb') as inputfile:
        fl_benign_dir = pickle.load(inputfile)

if not os.path.exists(objfile_malware):
    malware_dir = os.path.join(dir_dataset, "malware")
    print(malware_dir)
    fl_malware_dir = FileList(malware_dir)
    print(fl_malware_dir)
    fl_malware_dir.set_Class(1)
    fl_malware_dir.set_category('none')
    with open(objfile_malware, 'wb') as output:
        pickle.dump(fl_malware_dir, output, pickle.HIGHEST_PROTOCOL)
else:
    print("Reading malware dataset from pickle")
    with open(objfile_malware, 'rb') as inputfile:
        fl_malware_dir = pickle.load(inputfile)


fil_cat_fl = os.path.join(dir_results, 'fl_results_350.json')

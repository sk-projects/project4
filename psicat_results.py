# test each psi type separately and in combination

from fileinfo import FileList
import pickle
import os.path
import os
import ast
from mclearn import *

# Initialize Directory and File Paths
dir_dataset = "/home/cloud/Documents/dataset_paper/dataset1cv"
dir_results = os.path.join(os.getcwd(), "psicat_results")
if not os.path.exists(dir_results):
    os.mkdir(dir_results)
objfile_benign = os.path.join(dir_results, 'db_benign.pkl')
objfile_malware = os.path.join(dir_results, 'db_malware.pkl')
objfile_dataset = os.path.join(dir_results, 'db_dataset.pkl')
var_ApplyMachineLearning = True


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
    fl_malware_dir.set_Class(0)
    fl_malware_dir.set_category('none')
    with open(objfile_malware, 'wb') as output:
        pickle.dump(fl_malware_dir, output, pickle.HIGHEST_PROTOCOL)
else:
    print("Reading malware dataset from pickle")
    with open(objfile_malware, 'rb') as inputfile:
        fl_malware_dir = pickle.load(inputfile)

fl_dataset = fl_benign_dir + fl_malware_dir

fil_cat_fl = os.path.join(dir_results, 'fl_results_350.json')
dct_cat_fl = ast.literal_eval(open(fil_cat_fl, 'r').read())
if not os.path.exists(os.path.join(dir_results, '350')):
    os.mkdir(os.path.join(dir_results, '350'))

numfeatures = len(dct_cat_fl[350][0])
fl_dataset.feature_list = dct_cat_fl[350][0]
fl_dataset.generate_feature_vector(numfeatures, 4)
fil_fv = os.path.join(dir_results, '350', 'fv_350_func.csv')
fl_dataset.save_feature_vector(fil_fv)

# Generate results for machine learning algorithms
if var_ApplyMachineLearning:
    print('Reading Feature Vector Dataset')

    # Read Dataset 1
    dataset = read_dataset(fil_fv)

    # Initialize to 7 machine learning models defined in mclearn [LR, KNN, DT, NB, MNB, SVM, RF]
    models = initialize_models()

    # Intialize file names
    json_ds1_cv_results = os.path.join(dir_results, '350', "func_cv_results.json")
    png_ds1_cv_graph = os.path.join(dir_results, '350', "func_cv_graph.png")

    # Cross Validation Results
    print('running machine learning algorithms')
    save_cv_results(dataset, models, 5, numfeatures+1, numfeatures-5, json_ds1_cv_results)

    # Plot Graph
    plot_graph('Cross Validation Results for Dataset1', 'Number of Features', 'Accuracy', json_ds1_cv_results,
               png_ds1_cv_graph)

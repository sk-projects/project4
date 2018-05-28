"""
MALWARE DETECTION COMPONENT

DATASET 1 : Trojan = 1576,   Virus = 2566,   Worm = 1234
            Benign    =   1169
            Total     =   6545

Steps in this Component
1. Extract Printable String Information from Binary Executable Files.
2. Generate global list of strings
3. Create unique list of strings
4. Generate Binary Feature Vector
    * Filter out strings less than length 4
    * Sort the strings in descending order according to frequency count
    * Select top 1000 strings
5. Save Feature List for new Malware detection

"""
from fileinfo import FileList
import pickle
import os.path
import os
from mclearn import *

# Initialize Directory and File Paths
dataset1_dir = "/home/cloud/Documents/dataset_paper/dataset1"
ds1_results_path = os.path.join(os.getcwd(),"dataset1_results")
if not os.path.exists(ds1_results_path):
    os.mkdir(ds1_results_path)
objfile_benign = os.path.join(ds1_results_path, 'benign_dataset1.pkl')
objfile_malware = os.path.join(ds1_results_path, 'malware_dataset1.pkl')
objfile_dataset1 = os.path.join(ds1_results_path, 'dataset1.pkl')
csv_dataset1_fv = os.path.join(ds1_results_path, 'dataset1_feature_vector.csv')
file_fl_dataset1 = os.path.join(ds1_results_path, 'dataset1_feature_list.txt')
var_ApplyMachineLearning = False

# Read the directories containing sample executable files
if not os.path.exists(objfile_benign):
    benign_dir = os.path.join(dataset1_dir, "benign")
    print(benign_dir)
    fl_benign_dir = FileList(benign_dir)
    print(fl_benign_dir)
    fl_benign_dir.set_Class('Benign')
    fl_benign_dir.set_category('none')
    with open(objfile_benign, 'wb') as output:
        pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)
else:
    print("Reading benign dataset from pickle")
    with open(objfile_benign,'rb') as inputfile:
        fl_benign_dir = pickle.load(inputfile)

if not os.path.exists(objfile_malware):
    trojan_dir = os.path.join(dataset1_dir, "malware", "trojan")
    print(trojan_dir)
    fl_trojan_dir = FileList(trojan_dir)
    print(fl_trojan_dir)
    fl_trojan_dir.set_Class('Malware')
    fl_trojan_dir.set_category('trojan')

    worm_dir = os.path.join(dataset1_dir, "malware", "worm")
    print(worm_dir)
    fl_worm_dir = FileList(worm_dir)
    print(fl_worm_dir)
    fl_worm_dir.set_Class('Malware')
    fl_worm_dir.set_category('worm')

    virus_dir = os.path.join(dataset1_dir, "malware", "virus")
    print(virus_dir)
    fl_virus_dir = FileList(virus_dir)
    print(fl_virus_dir)
    fl_virus_dir.set_Class('Malware')
    fl_virus_dir.set_category('virus')

    fl_malware_dir = fl_trojan_dir + fl_worm_dir + fl_virus_dir
    with open(objfile_malware, 'wb') as output:
        pickle.dump(fl_malware_dir, output, pickle.HIGHEST_PROTOCOL)
    print(fl_malware_dir)
else:
    print("Reading malware dataset from pickle")
    with open(objfile_malware,'rb') as inputfile:
        fl_malware_dir =  pickle.load(inputfile)


# Generate Global list of Unique Strings with frequency count
dataset1 = fl_benign_dir + fl_malware_dir
dataset1.generate_global_list()
dataset1.calculate_unique_strings()

# Generate Binary Feature Vector
dataset1.generate_feature_vector(1000, 4)

# Save top 1000 features into a list
dataset1.save_feature_list(1000, 4, file_fl_dataset1)

# Save feature vector
if not os.path.exists(csv_dataset1_fv):
    dataset1.save_feature_vector(csv_dataset1_fv)

# Save dataset
if not os.path.exists(objfile_dataset1):
    print("Write dataset to pickle")
    with open(objfile_dataset1, 'wb') as output:
        pickle.dump(dataset1, output, pickle.HIGHEST_PROTOCOL)


# Generate results for machine learning algorithms
if var_ApplyMachineLearning:
    print('Reading Feature Vector Dataset')

    # Read Dataset 1
    dataset = read_dataset(csv_dataset1_fv)

    # Initialize to 7 machine learning models defined in mclearn [LR, KNN, DT, NB, MNB, SVM, RF]
    models = initialize_models()

    # Intialize file names
    json_ds1_cv_results = os.path.join(ds1_results_path, "dataset1_cv_results.json")
    png_ds1_cv_graph = os.path.join(ds1_results_path, "dataset1_cv_graph.png")

    # Cross Validation Results
    print('running machine learning algorithms')
    save_cv_results(dataset, models, 50, 1000, 50, json_ds1_cv_results)

    # Plot Graph
    plot_graph('Cross Validation Results for Dataset1', 'Number of Features', 'Accuracy', json_ds1_cv_results,
               png_ds1_cv_graph)

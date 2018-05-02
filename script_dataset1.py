"""
Script to generate feature vector for dataset1

"""
from fileinfo import FileList
import pickle
import os.path
from mclearn import *

dataset1_dir = "/home/cloud/Documents/dataset_paper/dataset1"
ds1_results_path = os.path.join(os.getcwd(),"dataset1_results")
if not os.path.exists(ds1_results_path):
    os.mkdir(ds1_results_path)
objfile_benign = os.path.join(ds1_results_path, 'benign_dataset1.pkl')
objfile_malware = os.path.join(ds1_results_path, 'malware_dataset1.pkl')
objfile_dataset1 = os.path.join(ds1_results_path, 'dataset1.pkl')
csv_dataset1_fv = os.path.join(ds1_results_path, 'dataset1_feature_vector.csv')
file_fl_dataset1 = os.path.join(ds1_results_path, 'dataset1_feature_list.txt')

if not os.path.exists(objfile_benign):
    benign_dir = os.path.join(dataset1_dir, "benign")
    print(benign_dir)
    fl_benign_dir = FileList(benign_dir)
    print(fl_benign_dir)
    fl_benign_dir.set_Class('Benign')
    with open(objfile_benign, 'wb') as output:
        pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)
else:
    print("reading benign dataset from pickle")
    with open(objfile_benign,'rb') as inputfile:
        fl_benign_dir = pickle.load(inputfile)

if not os.path.exists(objfile_malware):
    trojan_dir = os.path.join(dataset1_dir, "malware", "trojan")
    print(trojan_dir)
    fl_trojan_dir = FileList(trojan_dir)
    print(fl_trojan_dir)
    fl_trojan_dir.set_Class('Malware')

    worm_dir = os.path.join(dataset1_dir, "malware", "worm")
    print(worm_dir)
    fl_worm_dir = FileList(worm_dir)
    print(fl_worm_dir)
    fl_worm_dir.set_Class('Malware')

    virus_dir = os.path.join(dataset1_dir, "malware", "virus")
    print(virus_dir)
    fl_virus_dir = FileList(virus_dir)
    print(fl_virus_dir)
    fl_virus_dir.set_Class('Malware')

    fl_malware_dir = fl_trojan_dir + fl_worm_dir + fl_virus_dir
    with open(objfile_malware, 'wb') as output:
        pickle.dump(fl_malware_dir, output, pickle.HIGHEST_PROTOCOL)
    print(fl_malware_dir)
else:
    print("reading malware dataset from pickle")
    with open(objfile_malware,'rb') as inputfile:
        fl_malware_dir =  pickle.load(inputfile)


dataset1 = fl_benign_dir + fl_malware_dir
dataset1.generate_global_list()
dataset1.generate_feature_vector(1000, 4)
dataset1.save_feature_list(1000, 4, file_fl_dataset1)

if not os.path.exists(csv_dataset1_fv):
    dataset1.save_feature_vector(csv_dataset1_fv)

if not os.path.exists(objfile_dataset1):
    print("write dataset to pickle")
    with open(objfile_dataset1, 'wb') as output:
        pickle.dump(dataset1, output, pickle.HIGHEST_PROTOCOL)


# generate results for machine learning algorithms
if 1 == 2:
    print('reading feature vector dataset')
    dataset = read_dataset(csv_dataset1_fv)
    models = initialize_models()
    json_ds1_cv_results = os.path.join(ds1_results_path, "dataset1_cv_results.json")
    png_ds1_cv_graph = os.path.join(ds1_results_path, "dataset1_cv_graph.png")
    print('running machine learning algorithms')
    save_cv_results(dataset, models, 50, 1000, 50, json_ds1_cv_results)
    plot_graph('Cross Validation Results for Dataset1', 'Number of Features', 'Accuracy', json_ds1_cv_results,
               png_ds1_cv_graph)

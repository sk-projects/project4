from fileinfo import FileList
import pickle
import ast
import os.path
import os

# Generate test dataset

# directories
src_test_directory = "/home/cloud/Documents/dataset_paper/test_dataset"
result_test_directory = os.path.join(os.getcwd(), 'test_dataset1_results')

#ds1_results_path = os.path.join(os.getcwd(),"dataset1_test_results")
csv_test_dataset1_fv = os.path.join(result_test_directory, 'test_dataset1_feature_vector.csv')
pkl_benign_test_dataset = os.path.join(result_test_directory, 'benign_test_dataset.pkl')
pkl_malware_test_dataset = os.path.join(result_test_directory, 'malware_test_dataset.pkl')
json_dataset1_test_results = os.path.join(result_test_directory, 'dataset1_test_result.json')
png_dataset1_test_results = os.path.join(result_test_directory, 'dataset1_test_result.png')

ds1_results_path = os.path.join(os.getcwd(),"dataset1_results")
dataset1_feature_list = ast.literal_eval(open(os.path.join(ds1_results_path, 'dataset1_feature_list.txt'),'r').read())

test_dataset_dir = src_test_directory
# ----------------------- benign

if not os.path.exists(pkl_benign_test_dataset):
    benign_dir = os.path.join(test_dataset_dir, "benign")
    print(benign_dir)
    fl_benign_dir = FileList(benign_dir)
    print(fl_benign_dir)
    fl_benign_dir.set_Class('Benign')
    with open(pkl_benign_test_dataset, 'wb') as output:
        pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)
else:
    print("reading benign dataset from pickle")
    with open(pkl_benign_test_dataset,'rb') as inputfile:
        fl_benign_dir = pickle.load(inputfile)


# ------------------------ malware

if not os.path.exists(pkl_malware_test_dataset):
    trojan_dir = os.path.join(test_dataset_dir, "malware", "trojan")
    print(trojan_dir)
    fl_trojan_dir = FileList(trojan_dir)
    print(fl_trojan_dir)
    fl_trojan_dir.set_Class('Malware')

    worm_dir = os.path.join(test_dataset_dir, "malware", "worm")
    print(worm_dir)
    fl_worm_dir = FileList(worm_dir)
    print(fl_worm_dir)
    fl_worm_dir.set_Class('Malware')

    virus_dir = os.path.join(test_dataset_dir, "malware", "virus")
    print(virus_dir)
    fl_virus_dir = FileList(virus_dir)
    print(fl_virus_dir)
    fl_virus_dir.set_Class('Malware')

    fl_malware_dir = fl_trojan_dir + fl_worm_dir + fl_virus_dir
    with open(pkl_malware_test_dataset, 'wb') as output:
        pickle.dump(fl_malware_dir, output, pickle.HIGHEST_PROTOCOL)
    print(fl_malware_dir)
else:
    print("reading malware dataset from pickle")
    with open(pkl_malware_test_dataset,'rb') as inputfile:
        fl_malware_dir =  pickle.load(inputfile)


# -------------------  combine benign and malware and generate test dataset feature vector


print("generate test feature vector based on dataset1 feature list")
test_dataset1 = fl_benign_dir + fl_malware_dir
test_dataset1.feature_list = dataset1_feature_list
test_dataset1.generate_feature_vector(1000, 4)
test_dataset1.save_feature_vector(csv_test_dataset1_fv)

# ------------------ test

from mclearn import *

# train dataset
print("reading train dataset")
ds1_results_path = os.path.join(os.getcwd(),"dataset1_results")
csv_dataset1_fv = os.path.join(ds1_results_path, 'dataset1_feature_vector.csv')
train_dataset = read_dataset(csv_dataset1_fv)

# test dataset
print("reading test dataset")
test_dataset = read_dataset(csv_test_dataset1_fv)

print("Testing performance on unseen data")
models = initialize_models()
save_test_results(train_dataset, test_dataset, models, 50, 1001, 50, json_dataset1_test_results)
plot_graph('Test Results for Unseen Dataset', 'Number of Features', 'Accuracy', json_dataset1_test_results, png_dataset1_test_results)

from FormatResult import *
write_cv_results_to_excel(json_dataset1_test_results, os.path.join(result_test_directory,'dataset1_test_result.xlsx'))

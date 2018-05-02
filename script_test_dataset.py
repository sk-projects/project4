
from fileinfo import FileList
import pickle
import os.path

# Generate test dataset

test_dataset_dir = "/home/cloud/Documents/dataset_paper/test_dataset"

benign_dir = os.path.join(test_dataset_dir, "benign")
print(benign_dir)
fl_benign_dir = FileList(benign_dir)
print(fl_benign_dir)
fl_benign_dir.set_Class('Benign')
with open('benign_test_dataset.pkl', 'wb') as output:
    pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)

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
with open('malware_test_dataset.pkl', 'wb') as output:
    pickle.dump(fl_malware_dir, output, pickle.HIGHEST_PROTOCOL)
print(fl_malware_dir)

test_dataset = fl_benign_dir + fl_malware_dir
test_dataset.generate_global_list()
test_dataset.generate_feature_vector(1000, 5)
test_dataset.save_feature_vector('test_dataset_feature_vector.csv')
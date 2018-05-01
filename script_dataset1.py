"""
Script to generate feature vector for dataset1

"""
from fileinfo import FileList
import pickle
import os.path

dataset1_dir = "/home/cloud/Documents/dataset_paper/dataset1"

benign_dir = os.path.join(dataset1_dir, "benign")
print(benign_dir)
fl_benign_dir = FileList(benign_dir)
print(fl_benign_dir)
fl_benign_dir.setClass('Benign')
with open('benign_dataset1.pkl', 'wb') as output:
    pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)

trojan_dir = os.path.join(dataset1_dir, "malware", "trojan")
print(trojan_dir)
fl_trojan_dir = FileList(trojan_dir)
print(fl_trojan_dir)
fl_trojan_dir.setClass('Malware')

worm_dir = os.path.join(dataset1_dir, "malware", "worm")
print(worm_dir)
fl_worm_dir = FileList(worm_dir)
print(fl_worm_dir)
fl_worm_dir.setClass('Malware')

virus_dir = os.path.join(dataset1_dir, "malware", "virus")
print(virus_dir)
fl_virus_dir = FileList(virus_dir)
print(fl_virus_dir)
fl_virus_dir.setClass('Malware')

fl_malware_dir = fl_trojan_dir + fl_worm_dir + fl_virus_dir
with open('malware_dataset1.pkl', 'wb') as output:
    pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)
print(fl_malware_dir)

# newdir.generate_global_list()
# newdir.generate_feature_vector(1000, 5)
# newdir.save_feature_vector('featurevector2.txt')


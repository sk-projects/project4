"""
Script to generate feature vector for dataset1

"""
from fileinfo import FileList
import pickle
import os.path

dataset1_dir = "/home/xena/Documents/dataset_paper/dataset2"

benign_dir = os.path.join(dataset1_dir, "benign")
print(benign_dir)
fl_benign_dir_win7 = FileList(benign_dir)
print(fl_benign_dir_win7)
fl_benign_dir_win7.setClass('Benign')

benign_dir_win10 = os.path.join(dataset1_dir, "benign_win10")
print(benign_dir_win10)
fl_benign_dir_win10 = FileList(benign_dir_win10)
print(fl_benign_dir_win10)
fl_benign_dir_win10.setClass('Benign')

fl_benign_dir = fl_benign_dir_win7 +  fl_benign_dir_win10
print(fl_benign_dir)
with open('benign_dataset2.pkl', 'wb') as output:
    pickle.dump(fl_benign_dir, output, pickle.HIGHEST_PROTOCOL)

del fl_benign_dir_win7
del fl_benign_dir_win10

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
with open('malware_dataset2.pkl', 'wb') as output:
    pickle.dump(fl_malware_dir, output, pickle.HIGHEST_PROTOCOL)
print(fl_malware_dir)

del fl_trojan_dir
del fl_worm_dir
del fl_virus_dir

dataset1 = fl_benign_dir + fl_malware_dir
dataset1.generate_global_list()
dataset1.generate_feature_vector(1000, 5)
dataset1.save_feature_vector('dataset2_feature_vector.csv')


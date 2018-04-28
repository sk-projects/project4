
#from fileinfo import SampleFile
from fileinfo import FileList

import pickle

print("main.py is being run")
import os.path
# path='/home/cloud/Desktop/win10exe/system'
# path=r'C:\Users\Rose\Desktop\win10exe\system'
path = os.path.join(os.path.join(os.getcwd(), 'win10exe'), 'system')
#path = '/media/cloud/aceshub1/dt/repo/benign/ds01b'
path = '/media/cloud/aceshub1/dt/psi/detection/dataset2/benign_samples'
print(path)
dir1 = FileList(path)
print(dir1)
dir1.setClass('Benign')
#dir1.generate_global_list()
#dir1.generate_feature_vector(1000, 5)

with open('benign_data2.pkl', 'wb') as output:
    pickle.dump(dir1, output, pickle.HIGHEST_PROTOCOL)


# path=r'C:\Users\Rose\Desktop\win10exe\system2'
path = os.path.join(os.path.join(os.getcwd(), 'win10exe'), 'system2')
#path = '/media/cloud/aceshub1/dt/repo/malware/ds01m'
path = '/media/cloud/aceshub1/dt/psi/detection/dataset2/malware_samples'
dir2 = FileList(path)
print(dir2)
dir2.setClass('Malware')
#dir2.generate_global_list()
#dir2.generate_feature_vector(1000, 5)

with open('malware_data2.pkl', 'wb') as output:
    pickle.dump(dir1, output, pickle.HIGHEST_PROTOCOL)

newdir = dir1 + dir2
del dir1
del dir2
print(newdir)
newdir.generate_global_list()
newdir.generate_feature_vector(1000, 5)
newdir.save_feature_vector('featurevector2.txt')


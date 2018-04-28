
#from fileinfo import SampleFile
from fileinfo import FileList

print("fileinfo.py is being run directly")
import os.path
# path='/home/cloud/Desktop/win10exe/system'
# path=r'C:\Users\Rose\Desktop\win10exe\system'
path = os.path.join(os.path.join(os.getcwd(), 'win10exe'), 'system')
#path = '/media/cloud/aceshub1/dt/repo/benign/ds01b'
print(path)
dir1 = FileList(path)
print(dir1)
dir1.setClass('Benign')
dir1.generate_global_list()
#    dir1.find_urls()
dir1.generate_feature_vector(1000, 5)
dir1.save_feature_vector("fv20180417-1.txt")

# path=r'C:\Users\Rose\Desktop\win10exe\system2'
path = os.path.join(os.path.join(os.getcwd(), 'win10exe'), 'system2')
#path = '/media/cloud/aceshub1/dt/repo/malware/ds01m'
dir2 = FileList(path)
dir2.setClass('Malware')
dir2.generate_global_list()
#    dir1.find_urls()
dir2.generate_feature_vector(1000, 5)
dir2.save_feature_vector("fv20180417-2.txt")

newdir = dir1 + dir2
newdir.generate_global_list()
newdir.generate_feature_vector(1000, 5)
newdir.save_feature_vector('fv20180417-3.txt')


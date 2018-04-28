#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:55:41 2018

@author: sk cloud

Class SampleFile and Class FileList
"""

import hashlib
import subprocess
import numpy as np


class SampleFile:
#    sha256=''
#    filename=''
#    dct_freq_count={}
#    psi_count=0
#    urls=[]
#    Class=''
#    feature_vector=[]
    
    def __init__(self,filename):
        self.filename=filename
        self.calculate_sha256()
    
    def calculate_sha256(self):
        BLOCKSIZE = 65536
        hasher = hashlib.sha256()
        with open(self.filename, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        self.sha256 = hasher.hexdigest()
        
    def extract_strings(self):
        result=subprocess.run(['strings',self.filename],stdout=subprocess.PIPE)
        psi=result.stdout.splitlines()
#        open(self.filename + '.txt','w').write('\n'.join(map(bytes.decode,psi)))
        self.psi_count=len(psi)
        psistr=list(map(bytes.decode,psi))
        self.psi_freq_count(psistr)
    
    def psi_freq_count(self,psi):
        self.dct_freq_count={}
        for string in psi:
            if string not in self.dct_freq_count.keys():
                self.dct_freq_count[string] = 1
            else:
                self.dct_freq_count[string] += 1
#        open(self.filename + '.txt1','w').write(str(self.dct_freq_count))

    def find_urls(self):
        lst=[]
        for string in self.dct_freq_count.keys():
            lst.append(string)
        strlst = list(map(bytes.decode,lst))
        import re
        regex=re.compile("^.*http:.*")
        self.urls=[m.group(0) for l in strlst for m in [regex.search(l)] if m]
#        print(self.urls)
        
    def set_Class(self,Class):
        self.Class=Class
 
    def create_feature_vector(self,feature_list):
        file_strings = self.dct_freq_count.keys()
        self.feature_vector=[]
        for feature in feature_list:
            if feature in file_strings:
                self.feature_vector.append(1)
            else:
                self.feature_vector.append(0)
        self.feature_vector.append(self.Class)
    
    def save_feature_vector(self,file_featurevector):
        if self.feature_vector == []:
            print("Feature vector Empty")
        else:
            open(file_featurevector,"w").write(self.feature_vector)
            
    def __str__(self):
        return 'sha256: %s \nFileName: %s\nClass: %s' % (self.sha256, self.filename, self.Class)

class FileList:
#    dct_fileinfo={}
#    dirname = ''
    alldir_list = []
#    global_list=[]
#    filtered_global_list=[]
#    feature_list=[]
        
    def __init__(self,dirname=''):
        self.dct_fileinfo = {}
        self.feature_list = []
        self.filtered_global_list = []
        self.feature_vector = []
        if dirname != '':            
            self.dirnames = [dirname]
            if dirname not in self.alldir_list:
                self.alldir_list.append(dirname)
            self.extract_strings_from_files(dirname)            

    def __str__(self):
        #total_files = 
        return 'Dir Name: %s \nTotal Files: %d' % (self.dirnames, len(self.dct_fileinfo.keys()))
    
    def __add__(self, other):
        dirnames = self.dirnames + other.dirnames
        dct_fileinfo={}
        dct_fileinfo = self.dct_fileinfo.copy()
        dct_fileinfo.update(other.dct_fileinfo)
        newdir = FileList()
        newdir.dct_fileinfo = dct_fileinfo
        newdir.dirnames = dirnames
        return newdir
         
    def extract_strings_from_files(self,path):
        files=os.listdir(path)
        for file in files:
            f = SampleFile(os.path.join(path,file))
            if f.sha256 not in self.dct_fileinfo.keys():
                f.extract_strings()
                self.dct_fileinfo[f.sha256]=f  

    def generate_global_list(self):
        from operator import itemgetter
        dct_global_list={}
        for file in self.dct_fileinfo.values():
#            print(file.filename)
            for psi in file.dct_freq_count.keys():
                if psi not in dct_global_list.keys():
#                    dct_global_list[psi] = file.dct_freq_count[psi]
                    dct_global_list[psi] = 1
                else:
#                    dct_global_list[psi] += file.dct_freq_count[psi]
                    dct_global_list[psi] += 1
        self.global_list = []
        for stringkey in dct_global_list.keys():
            self.global_list.append((stringkey, dct_global_list[stringkey]))
        self.global_list = sorted(self.global_list, key=itemgetter(1), reverse=True)
    
    def filter_global_list_len(self,minlen):
        self.filtered_global_list=list(filter(lambda x:len(x[0])>=minlen, dir1.global_list))
        
    def create_feature_list(self,threshold,strlen):
        if self.filtered_global_list == []:
            self.filter_global_list_len(strlen)
        self.feature_list=[x[0] for x in self.filtered_global_list[0:threshold]]
        
    def find_urls(self):
        lst=[]
        for x in self.global_list:
            lst.append(x[0])
        #strlst = list(map(bytes.decode,lst))
        import re
        regex=re.compile("^.*http:.*")
        result=[m.group(0) for l in lst for m in [regex.search(l)] if m]
        return result
#        print(result)
    
    def setClass(self,Class):
        for file in self.dct_fileinfo.values():
            file.Class = Class
    
    def generate_feature_vector(self,threshold,strlen):
        if self.feature_list == []:
            self.create_feature_list(threshold,strlen)
        for file in self.dct_fileinfo.values():
            file.create_feature_vector(self.feature_list)
            
    def save_feature_vector(self,file_featurevector):
        all_feature_vectors=''
        files = list(self.dct_fileinfo.values())
        for file in files:
            if file.feature_vector == []:
                print("Feature vector Empty")
            else:
                if all_feature_vectors == '':
                    all_feature_vectors = ','.join(list(map(str,file.feature_vector))) 
                else:
                    all_feature_vectors = all_feature_vectors + '\n' + ','.join(list(map(str,file.feature_vector))) 
        open(file_featurevector,"w").write(all_feature_vectors)
        self.feature_vector = all_feature_vectors

    def save_global_list(self,file_globallist):
        open(file_globallist,"w").write('\n'.join(list(map(str,self.global_list))))
        
    def save_fileinfo(self,file_info):
        import os
        os.remove(file_info)
        for file in self.dct_fileinfo.values():
            fninfo = file.filename + '\n' #+ str(file.dct_freq_count) + '\n'
            open(file_info,"a+").write(fninfo)
    
    def show_file_list(self):
        for file in self.dct_fileinfo.values():
            print(file.filename)
    
if __name__ == "__main__":
    print("fileinfo.py is being run directly")
    import os
    from os.path import join
    #path='/home/cloud/Desktop/win10exe/system'
    #path=r'C:\Users\Rose\Desktop\win10exe\system'
    path = join(join(os.getcwd(),'win10exe'),'system')
    path = '/media/cloud/aceshub1/dt/repo/benign/ds01b'
    
    dir1 = FileList(path)
    dir1.setClass('Benign')
    dir1.generate_global_list()
#    dir1.find_urls()
    dir1.generate_feature_vector(1000,5)
    dir1.save_feature_vector("fv20180417-1.txt")
    
    #path=r'C:\Users\Rose\Desktop\win10exe\system2'
    path = join(join(os.getcwd(),'win10exe'),'system2')
    path = '/media/cloud/aceshub1/dt/repo/malware/ds01m'
    dir2 = FileList(path)
    dir2.setClass('Malware')
    dir2.generate_global_list()
#    dir1.find_urls()
    dir2.generate_feature_vector(1000,5)
    dir2.save_feature_vector("fv20180417-2.txt")    
    
    newdir = dir1 + dir2
    newdir.generate_global_list()
    newdir.generate_feature_vector(1000,5)
    newdir.save_feature_vector('fv20180417-3.txt')
else:
    print("fileinfo.py is being imported into another module")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:55:41 2018

@author: sk cloud

Class SampleFile and Class FileList
"""

import hashlib
import subprocess
from typing import Dict, Any, List

import numpy as np
import os


class SampleFile:

    word_list_func = []
    word_list_msg = []

    def __init__(self,filename):
        self.filename = filename
        self.calculate_sha256()
        self.psi_count = 0
        self.dct_freq_count = {}

        # string category
        self.urls = []
        self.dlls = []
        self.other_files = {} # is a dictionary with key as extension and values as list of files with that extension
        self.func_names = []
        self.messages = []
        self.symbolic = []
        self.other_files_list = []
        self.symbolic_count = 0

    
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
        result=subprocess.run(['strings', self.filename],stdout=subprocess.PIPE)
        psi=result.stdout.splitlines()
#        open(self.filename + '.txt','w').write('\n'.join(map(bytes.decode,psi)))
        self.psi_count = len(psi)
        psistr=list(map(bytes.decode,psi))
        self.psi_freq_count(psistr)

        # if self.word_list_func == []:
        #     self.generate_word_list_func()
        # if self.word_list_msg == []:
        #     self.generate_word_list_msg()
        # self.find_urls()
        # self.find_dll_files()
        # self.find_other_files()
        # self.find_api_calls(word_list1=self.word_list_func)
        # #self.find_messages()
        # #self.find_symbolic()
        # self.find_messages_symbolic(word_list1=self.word_list_msg)
        # self.write_count()

    
    def psi_freq_count(self,psi):
        self.dct_freq_count={}
        for string in psi:
            if string not in self.dct_freq_count.keys():
                self.dct_freq_count[string] = 1
            else:
                self.dct_freq_count[string] += 1
#        open(self.filename + '.txt1','w').write(str(self.dct_freq_count))


    def generate_word_list_func(self):
        if self.word_list_func == []:
            from nltk.corpus import words
            word_list = words.words()
            word_list1 = [x for x in word_list if 9 > len(x) > 2]
            word_list1 = sorted(word_list1, key=len)
            self.word_list_func = word_list1


    def generate_word_list_msg(self):
        if self.word_list_msg == []:
            from nltk.corpus import words
            word_list = words.words()
            word_list1 = [x for x in word_list if len(x) > 3]
            word_list1 = sorted(word_list1, key=len)
            self.word_list_msg = word_list1

    def categorize_strings(self):
        if self.word_list_func == []:
            self.generate_word_list_func()
        if self.word_list_msg == []:
            self.generate_word_list_msg()

        self.find_urls()
        self.find_dll_files()
        self.find_other_files()
        self.find_api_calls(word_list1=self.word_list_func)
        self.find_messages()
        self.find_symbolic()


    def find_urls(self):
        if self.urls != []:
            self.urls = []
        #for string in self.dct_freq_count.keys():
        #    lst.append(string)
        strlst = list(self.dct_freq_count.keys())
        #strlst = list(map(bytes.decode,lst))
        import re
        pattern = re.compile(r'(?:(?:http|HTTP|https|HTTPS|ftp|FTP|smtp|SMTP|irc|IRC)?:\/\/)?[\w-]{2,}\.[\w-]{2,}\.[\w-]{2,6}[\/\w.-]*\??[\w.=\-]*')
        for string in strlst:
            if len(string) > 100 or len(string) < 5:
                continue
           # print(string)
            matches = pattern.findall(string)
            for match in matches:
                if(len(match) > 2):
                    self.urls.append(match)
                   # print(self.urls)

    def print_urls(self):
        print(self.urls)

    def find_dll_files(self):
        if self.dlls != []:
            self.dlls = []
        strlst = list(self.dct_freq_count.keys())
        import re
        pattern = re.compile(r'[a-zA-Z0-9-]+\.dll')
        for string in strlst:
            if len(string) > 15 or len(string) < 5:
                continue
          #  print(string)
            for match in pattern.findall(string):
                if(len(match) > 2):
                    self.dlls.append(match)
        #print(self.dlls)

    def print_dlls(self):
        print(self.dlls)

    def find_other_files(self):
        # is a dictionary with key as extension and values as list of files with that extension
        self.other_files = {}
        self.other_files_list = []
        strlst = list(self.dct_freq_count.keys())
        import re
        pattern = re.compile('([^:#&<>?|~%]+\.(exe|vbs|msi|jpg|pdf|cfg))$', re.IGNORECASE)
        for string in strlst:
            if len(string) > 50 or len(string) < 2:
                continue
            for match in pattern.findall(string):
                try:
                    self.other_files[str(match[1]).lower()].append(match[0])
                except KeyError:
                    self.other_files[str(match[1]).lower()] = [match[0]]
                self.other_files_list.append(match[0])

            #print(self.other_files)


    def print_other_files(self):
        print(self.other_files)


    def find_api_calls(self, word_list1=None):
        self.func_names = []
        strlst = list(self.dct_freq_count.keys())
        import re
        pattern = re.compile(r'^([A-Z]([a-z]+[A-Z]*){,6}(32|64)?)')
        for string in strlst:
            if(len(string) > 30):
                continue
            matches = pattern.fullmatch(string)
            if matches:
                #        print(matches[0])
                self.func_names.append(matches[0])

        garb = []
        pat1 = re.compile(r'[A-Z]([a-zA-Z])\1+')
        for string in self.func_names:
            matches = pat1.fullmatch(string)
            if matches:
                garb.append(matches[0])

        sfunc = []
        for x in self.func_names:
            if len(x) < 6:
                sfunc.append(x)

        small_func = ['sleep','exit','_exit','sqrt']
        msgstrings = [sm for sm in sfunc if sm.lower() not in small_func]
        fnf = list(set(self.func_names) - set(msgstrings))
        self.func_names = fnf

        if not word_list1:
            from nltk.corpus import words
            word_list = words.words()
            word_list1 = [x for x in word_list if 9 > len(x) > 2]
            word_list1 = sorted(word_list1, key=len)

        func_strings = []
        for string in self.func_names:
            for word in word_list1:
                if string.lower().find(word.lower()) != -1:
                    func_strings.append(string)
                    break
        self.func_names = func_strings

        #print(self.func_names)

#----------------------------------------------------------------------------------------------------------------
    def find_messages(self, word_list1=None):

        strlst = list(self.dct_freq_count.keys())
        strings = strlst

        if self.dlls == []:
            self.find_dll_files()
        if self.func_names == []:
            self.find_api_calls()
        if self.other_files_list == []:
            self.find_other_files()
        if self.urls == []:
            self.find_urls()
        strings = [string for string in strings if string not in self.dlls]
        strings = [string for string in strings if string not in self.func_names]
        strings = [string for string in strings if string not in self.other_files_list]
        strings = [string for string in strings if string not in self.urls]
        #print(len(strings))

        if not word_list1:
            from nltk.corpus import words
            word_list = words.words()
            word_list1 = [x for x in word_list if len(x) > 3]
            word_list1 = sorted(word_list1, key=len)

        msg_strings = []
        for string in strings:
            for word in word_list1:
                if string.lower().find(word.lower()) != -1:
                    msg_strings.append(string)
                    break

        self.messages = msg_strings


    def find_symbolic(self):

        strlst = list(self.dct_freq_count.keys())
        strings = strlst

        if self.dlls == []:
            self.find_dll_files()
        if self.func_names == []:
            self.find_api_calls()
        if self.other_files_list == []:
            self.find_other_files()
        if self.urls == []:
            self.find_urls()
        if self.messages == []:
            self.find_messages()

        msgstrings = self.messages
        strings = [string for string in strings if string not in self.dlls]
        strings = [string for string in strings if string not in self.func_names]
        strings = [string for string in strings if string not in self.other_files_list]
        strings = [string for string in strings if string not in self.urls]

        symstrings = [string for string in list(map(lambda x:x.lower(), strings)) if string not in list(map(lambda x:x.lower(), msgstrings))]

        self.symbolic = symstrings
        return symstrings


    def find_messages_symbolic(self,word_list1=None):
        strlst = list(self.dct_freq_count.keys())
        strings = strlst

        if self.dlls == []:
            self.find_dll_files()
        if self.func_names == []:
            self.find_api_calls()
        if self.other_files_list == []:
            self.find_other_files()
        if self.urls == []:
            self.find_urls()

        #strings = [string for string in strings if string not in self.dlls]
        #strings = [string for string in strings if string not in self.func_names]
        #strings = [string for string in strings if string not in self.other_files_list]
        #strings = [string for string in strings if string not in self.urls]

        strings = list(set(strings) - set(self.dlls) - set(self.func_names) - set(self.other_files_list) - set(self.urls))

        #print(len(strings))

        if not word_list1:
            from nltk.corpus import words
            word_list = words.words()
            word_list1 = [x for x in word_list if len(x) > 3]
            word_list1 = sorted(word_list1, key=len)

        msg_strings = []
        for string in strings:
            for word in word_list1:
                if string.lower().find(word.lower()) != -1:
                    msg_strings.append(string)
                    break

        self.messages = msg_strings

        #symstrings = [string for string in list(map(lambda x:x.lower(), strings)) if string not in list(map(lambda x:x.lower(), msg_strings))]

        #self.symbolic = symstrings
        self.symbolic_count = len(strings) - len(self.messages)

        #return symstrings

    def write_count(self):
        content = os.path.basename(self.filename) + " : " + "func = " + str(len(self.func_names)) + "|"
        content = content + " dlls = " + str(len(self.dlls)) + "|"
        content += " urls = " + str(len(self.urls)) + "|"
        content += " other files = " + str(len(self.other_files_list)) + "|"
        content += " message = " + str(len(self.messages)) + "|"
        content += " symbolic = " + str(self.symbolic_count) + "\n"

        open("psi_count_worm.txt","a").write(content)

#-----------------------------------------------------------------------------------------------------------------------

    def set_Class(self, Class):
        self.Class = Class

    def set_category(self, category):
        self.category = category

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

    alldir_list = []

    def __init__(self,dirname=''):
        self.dct_fileinfo = {}
        self.feature_list = []
        self.filtered_global_list = []
        self.feature_vector = []
        self.global_list = []
        self.total_strings = 0
        self.unique_strings = 0
        self.Class = []
        self.name = dirname
        self.dll_global_freq_count = {}
        if dirname != '':            
            self.dirnames = [dirname]
            if dirname not in self.alldir_list:
                self.alldir_list.append(dirname)
            self.extract_strings_from_files(dirname)
            self.total_files=0
            for dirname in self.dirnames:
                self.total_files += len(os.listdir(dirname))
            self.calculate_total_strings()


    def __str__(self):
        return 'Dir Name: %s \nTotal Files: %d \n listfile = %d' % (self.dirnames, len(self.dct_fileinfo.keys()), self.total_files)

    def __add__(self, other):
        dirnames = self.dirnames + other.dirnames
        dct_fileinfo={}
        dct_fileinfo = self.dct_fileinfo.copy()
        dct_fileinfo.update(other.dct_fileinfo)
        newdir = FileList()
        newdir.dct_fileinfo = dct_fileinfo
        newdir.dirnames = dirnames
        newdir.total_files = self.total_files + other.total_files
        newdir.total_strings = self.total_strings + other.total_strings
        newdir.Class = self.Class + other.Class
        return newdir

    def extract_strings_from_files(self,path):
        import os
        files = os.listdir(path)
        print("Total files in directory = ", len(files))
        counter = 0
        for file in files:
            f = SampleFile(os.path.join(path,file))
            print("processing file %s " % (f.filename))
            if f.sha256 not in self.dct_fileinfo.keys():
                f.extract_strings()
                self.dct_fileinfo[f.sha256] = f
                counter += 1
                print("processed %s " % (f.filename))
                if counter % 200 == 0:
                    print("Processed %d files" % (counter))

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

    def filter_global_list_len(self, minlen):
        self.filtered_global_list=list(filter(lambda x: len(x[0]) >= minlen, self.global_list))

    def filter_global_list_occ(self, occurance):
        self.filtered_global_list = list(filter(lambda x: x[1] >= occurance, self.global_list))

    def create_feature_list(self, threshold, strlen):
        if self.filtered_global_list == []:
            self.filter_global_list_len(strlen)
        self.feature_list = [x[0] for x in self.filtered_global_list[0:threshold]]

    def save_feature_list(self, threshold, strlen, filename):
        if self.feature_list == []:
            self.create_feature_list(threshold, strlen)
        open(filename,"w").write(str(self.feature_list))

    def read_feature_list_file(self, filename):
        import ast
        self.feature_list = ast.literal_eval(open(filename,'r').read())
    
    def generate_feature_vector(self, threshold, strlen):
        if self.feature_list == []:
            self.create_feature_list(threshold, strlen)
        for file in self.dct_fileinfo.values():
            file.create_feature_vector(self.feature_list)
            
    def save_feature_vector(self, file_featurevector):
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
        open(file_globallist, "w").write('\n'.join(list(map(str,self.global_list))))
        
    def save_fileinfo(self,file_info):
        import os
        os.remove(file_info)
        for file in self.dct_fileinfo.values():
            fninfo = file.filename + '\n' #+ str(file.dct_freq_count) + '\n'
            open(file_info,"a+").write(fninfo)



    def set_Class(self, Class):
        for file in self.dct_fileinfo.values():
            file.Class = Class
        self.Class = [Class]


    def set_category(self, category=''):
        for file in self.dct_fileinfo.values():
            file.category = category

    def show_file_list(self):
        for file in self.dct_fileinfo.values():
            print(file.filename)

    def calculate_total_strings(self):
        total_strings = 0
        for file in self.dct_fileinfo.values():
            total_strings += file.psi_count
        self.total_strings = total_strings

    def calculate_unique_strings(self):
        self.unique_strings = len(self.global_list)

    def print_average_strings_per_file(self):
        print("Total Strings = ", self.total_strings)
        print("Total Files = ", len(self.dct_fileinfo))
        print("Average number of strings per file = ", self.total_strings / len(self.dct_fileinfo))

    def save_global_list(self, outFile):
        content = ''
        
# =============================================================================
#         for item in self.global_list:
#             if content == '':
#                 content = str(item)
#             else:
#                 content = content + '\n' + str(item)
#                 
# =============================================================================
        content = '\n'.join(list(map(str,self.global_list)))
        open(outFile, 'w').write(content)

    def print_urls(self):
        for file in list(self.dct_fileinfo.values()):
            print(file.filename)
            file.print_urls()

    def print_dlls(self):
        for file in list(self.dct_fileinfo.values()):

            print(file.filename)
            file.print_dlls()

    def print_other_files(self):
        for file in list(self.dct_fileinfo.values()):
            print(file.filename)
            file.print_other_files()


    def generate_feature_vector_from_dlls(self, fil_dll_feature_vector):
        from operator import itemgetter
        files = list(self.dct_fileinfo.values())
        self.dll_global_freq_count = {}
        dll_global_list = []
        for file in files:
            dlls = list(map(lambda x: x.lower(),file.dlls))
            dll_global_list = dll_global_list + dlls
        from collections import Counter
        self.dll_global_freq_count = dict(Counter(dll_global_list))
        print(self.dll_global_freq_count)

        global_list = []
        for stringkey in self.dll_global_freq_count.keys():
            global_list.append((stringkey, self.dll_global_freq_count[stringkey]))
        revlst = sorted(global_list, key=itemgetter(1), reverse=True)
        print(revlst)
        dll_feature_list = [x[0] for x in revlst]
        dll_names = list(self.dll_global_freq_count.keys())
        self.dll_feature_vector = []

        for file in files:
            file_feature_vector=[]
            for feature in dll_feature_list:
                if feature in file.dlls:
                    file_feature_vector.append(file.dlls.count(feature))
                else:
                    file_feature_vector.append(0)
            file_feature_vector.append(file.Class)
            self.dll_feature_vector.append(file_feature_vector)

        content = ''
        for item in self.dll_feature_vector:
            if content == '':
                content = ','.join(list(map(str,item)))
            else:
                content = content + '\n' + ','.join(list(map(str,item)))
        print(content)
        print('Total Files = %d' % (len(self.dll_feature_vector)))
        open(fil_dll_feature_vector,'w').write(content)

    def write_psi_freq_count(self, output):
        files = list(self.dct_fileinfo.values())
        dct_psi = {}
        for file in files:
            dct_psi[os.path.basename(file.filename)] = file.dct_freq_count
        open(output,'w').write(str(dct_psi))


if __name__ == "__main__":
    print("fileinfo.py is being run directly")
    import os
    from os.path import join
    #path='/home/cloud/Desktop/win10exe/system'
    #path=r'C:\Users\Rose\Desktop\win10exe\system'
    path = join(join(os.getcwd(),'win10exe'),'system')
    path = '/media/cloud/aceshub1/dt/repo/benign/ds01b'
    
    dir1 = FileList(path)
    dir1.set_Class('Benign')
    dir1.generate_global_list()
#    dir1.find_urls()
    dir1.generate_feature_vector(1000, 5)
    dir1.save_feature_vector("fv20180417-1.txt")
    
    #path=r'C:\Users\Rose\Desktop\win10exe\system2'
    path = join(join(os.getcwd(),'win10exe'),'system2')
    path = '/media/cloud/aceshub1/dt/repo/malware/ds01m'
    dir2 = FileList(path)
    dir2.set_Class('Malware')
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
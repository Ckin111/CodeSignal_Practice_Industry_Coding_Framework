import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict

import numpy
import sortedcontainers

class Server:
    def __init__(self):
        self.files = []
    
    def is_server_empty(self):
        if not self.files:
            return True
        else: 
            return False

    def exists(self,file):
        if self.is_server_empty() == False:
            for item in self.files:
                if item[0] == file[0]:
                    return True   
        return False

    def upload(self,file):
        # file is file_name, size
        if self.exists(file) == False:
            self.files.append(file)
        else:
            raise RuntimeError("File already exists")

    def get(self,file):
        # file is file_name
        if self.exists(file) == False:
            for item in self.files:
                if item[0] == file[0]:
                    return item[1]

    def copy(self,file):
        # file is source, dest
        dest= None
        src = None
        if self.exists(file) == True:
            for item in self.files:
                if item[0] == file[1]:
                    dest = item
                if item[0] == file[0]:
                    src = item
            
            if src is None:
                raise RuntimeError("File doesn't exist")
            else:
                src[0] = file[1]
                if dest is not None:
                    self.files.remove(dest)
        else:
            raise RuntimeError("File doesn't exist")
    
    def search(self,file):
        # file is prefix ["Ba"]
        # Find top 10 files starting with the provided prefix. 
        # Order results by their size in descending order
        # in case of a tie by file name.

        prefix = file[0]
        prefix_length = len(prefix)
        matches = []
        if self.is_server_empty() == True:
            return []
        
        # search
        for item in self.files:
            if len(matches)==10:
                break
            elif prefix_length < len(item[0]):
                if item[0][:prefix_length] == prefix:
                    matches.append(item)
        
        # sort results filesize descending
        sorted_files = sorted(matches, key=lambda x: (-int(x[1][:-2]), x[0]))

        # make results in the right format
        for i in range(len(matches)):
            matches[i] = matches[i][0]
            
        return matches

def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    server = Server()
    result_list = []
    for item in list_of_lists:
        match item.pop(0):
            case "FILE_UPLOAD":
                server.upload(item)
                result_list.append("uploaded " + item[0])
            case "FILE_GET":
                server.get(item)
                result_list.append("got " + item[0])
            case "FILE_COPY":
                server.copy(item)
                result_list.append("copied " + item[0] + " to " + item[1])
            case "FILE_SEARCH":
                ans = server.search(item)
                print(ans)
                result_list.append("found " + str(ans).replace("'", ""))
        print(server.files)
    print(result_list)
    return result_list
            

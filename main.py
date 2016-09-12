import os
import re
import pandas as pd
# \{(([^\n,{}]+)[,]?)+\},(.)+

TARGET_DIR = r'D:\download\1'
re_grp = re.compile(r't_ast([A-Z]{3})grp')
re_params = re.compile(r'\{(([^\n,{}]+)[,]?)+\},(.)+', re.MULTILINE or re.DOTALL)

def read_grp(line):
    #re.match 는 문장 처음부터 찾는다. 중간거는 못찾음  
    matchObj = re_grp.search(line)
    if( matchObj ) :
        return matchObj.group(1)
    return None 

def read_params(line):
    matchObj = re_params.search(line)
    if( matchObj ) :
        return matchObj.groups()
    return None

def test():
    for root, directories, filenames in os.walk(TARGET_DIR):
        print(root, directories, filenames)
        
        for filename in filenames:
            filePath = root + os.sep + filename
            # print(filePath)
            if(filename == 'KpdPara_Table.c'):
                with open(filePath, 'r', encoding= 'utf8') as f:
                    for line in f.readlines():
                        grpName = read_grp(line)
                        params = read_params(line)
                        if( params ) :
                            print(params)
                     


               
            # pass
            # pass
    pass 
if __name__ == '__main__':
    test() 
    print('hello world')

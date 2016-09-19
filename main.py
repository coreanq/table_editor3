import os
import re
import pandas as pd
# \{(([^\n,{}]+)[,]?)+\},(.)+

TARGET_DIR = r'D:\download\1'
re_check_grp = re.compile(r't_ast([A-Z]{2:3})grp')
re_check_params = re.compile(r'\{([^\n,{}]+[,]?)+\}', re.DOTALL)
re_parse_params = re.compile(r'(\([^,\n{}]+\))?([^\n,{}]+)', re.DOTALL)
def read_grp(line):
    #re.match 는 문장 처음부터 찾는다. 중간거는 못찾음  
    matchObj = re_check_grp.search(line)
    if( matchObj ) :
        return matchObj.group(1)
    return None 

def read_params(line):
    # 처음엔 파라미터 형식에 맞는 라인을 찾는다. 
    lineMatchObj = re_check_params.search(line)
    params = None
    params = None
    if(lineMatchObj):
        params = re_parse_params.findall(line) 
        return params
    else: return None

def test():
    for root, directories, filenames in os.walk(TARGET_DIR):
        print(root, directories, filenames)
        
        for filename in filenames:
            filePath = root + os.sep + filename
            grpName = ""
            # print(filePath)
            if(filename == 'KpdPara_Table.c'):
                with open(filePath, 'r', encoding= 'utf8') as f:
                    for line in f.readlines():
                        result  = read_grp(line)
                        if( result ):
                            grpName = result
                        params = read_params(line) 
                        if( params ):
                            print(grpName, params)

               
if __name__ == '__main__':
    test() 
    print('hello world')

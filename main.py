import os
import re
import io
# import pandas as pd
# \{(([^\n,{}]+)[,]?)+\},(.)+

TARGET_DIR = r'D:\download\1'
KPD_BASIC_TITLE_SRC_FILE='kpd_tbl_msg_eng.c'
KPD_ADD_TITLE_SRC_FILE = 'addtitle_eng.c'
KPD_ADD_TITLE_HEADER_FILE = 'addtitle_eng.h'
KPD_TITLE_ENUM_HEADER_FILE = 'kpd_title_enum.h'
KPD_PARA_TABLE_SRC_FILE = 'kpdpara_table.c'
KPD_PARA_VARI_SRC_FILE = 'kpdpara_vari.c'
KPD_PARA_VARI_HEADER_FILE = 'kpdpara_vari.h'


re_check_grp = re.compile(r'(static const S_TABLE_X_TYPE t_ast([A-Z]{2,3})grp[^;]+\}\;)') # 한개의 그룹 뽑아냄 
re_check_params = re.compile(r'\{([^\n,{}]+[,]?)+\}', re.DOTALL)
re_parse_params = re.compile(r'(\([^,\n{}]+\))?([^\n,{}]+)', re.DOTALL)

# check 의 경우 input 의 값이 원하는 형식인지 파악 parse 의 경우 input 에서 param 리스트를 뽑아냄  
re_check_basic_title = re.compile(r'({([^{},]+[,]?)+}[^\n]+)', re.DOTALL)
re_parse_basic_title = re.compile(r'([^{},]+)[,]?', re.DOTALL)



def read_basic_title(line):
    findList =  []
    searchObj = re_check_basic_title.search(line)
    if( searchObj ):
        findList = re_parse_basic_title.findall(line)
        return findList 
    else: 
        return None
    pass

def read_grp(contents):
    #re.match 는 문장 처음부터 찾는다. 중간거는 못찾음  
    searchObj = re_check_grp.search(contents)

    if( searchObj ):
        buf = io.StringIO(contents)
        for line in buf.readline():
            read_params(line)

    if( searchObj ) :
        return searchObj.group(1)
    return None 

def read_params(line):
    # 처음엔 파라미터 형식에 맞는 라인을 찾는다. 
    lineMatchObj = re_check_params.search(line)
    params = None
    if(lineMatchObj):
        params = re_parse_params.findall(line) 
        return params
    else: 
        return None


def test():
    for root, directories, filenames in os.walk(TARGET_DIR):
        print(root, directories, filenames)
        
        for filename in filenames:
            filePath = root + os.sep + filename
            grpName = ""
            # print(filePath)
            if(filename.lower() == KPD_PARA_TABLE_SRC_FILE ):
                with open(filePath, 'r', encoding= 'utf8') as f:
                    contents = f.read()
                    read_grp(contents)
                    # print(contents) 
            elif ( filename.lower() == KPD_BASIC_TITLE_SRC_FILE):
                with open(filePath, 'r', encoding= 'utf8') as f:
                    for line in f.readlines():
                        ret = read_basic_title(line)
                        if(ret):
                            print(ret)
                pass
                    # for line in f.readlines():
                    #     result  = read_grp(line)
                    #     if( result ):
                    #         grpName = result
                    #     params = read_params(line) 
                    #     if( params ):
                    #         print(grpName, params)

               
if __name__ == '__main__':
    test() 
    print('hello world')

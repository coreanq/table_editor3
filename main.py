import os
import re
import io
# parsing 방법
# 전체 파일을 한번에 읽음
# 파일 명에 상관없이 변수 명을 통해 그 파싱 내용이 어느 부분 데이터 인지 파악함
# 각 인자들 파싱 

TARGET_DIR = r'D:\download\1'

KPD_BASIC_TITLE_SRC_FILE='kpd_tbl_msg_eng.c'
KPD_ADD_TITLE_SRC_FILE = 'addtitle_eng.c'
KPD_ADD_TITLE_HEADER_FILE = 'addtitle_eng.h'
KPD_ENUM_TITLE_HEADER_FILE = 'kpd_title_enum.h'
KPD_PARA_TABLE_SRC_FILE = 'kpdpara_table.c'
KPD_PARA_VARI_HEADER_FILE = 'kpdpara_vari.h'

parsing_file_list = [KPD_BASIC_TITLE_SRC_FILE, KPD_ADD_TITLE_SRC_FILE,
                    KPD_ADD_TITLE_HEADER_FILE, KPD_ENUM_TITLE_HEADER_FILE, 
                    KPD_PARA_TABLE_SRC_FILE, KPD_PARA_VARI_HEADER_FILE]


re_check_grp = re.compile(r'(S_TABLE_X_TYPE t_ast([A-Z]{2,3})grp[^;]+\}\;)') # 한개의 그룹 뽑아냄 
re_check_params = re.compile(r'\{([^\n,{}]+[,]?)+\}', re.DOTALL)
re_parse_params = re.compile(r'(\([^,\n{}]+\))?([^\n,{}]+)', re.DOTALL)

# check 의 경우 input 의 값이 원하는 형식인지 파악 parse 의 경우 input 에서 param 리스트를 뽑아냄  
re_extract_basic_title_vari = re.compile(r'BYTE kpdParaTitleEng[^;]+};')
re_extract_add_title_vari = re.compile(r'WORD g_awAddTitleEng[^;]+};')
re_check_title = re.compile(r'{([^{},]+[,]?)+}[^\n]+', re.DOTALL)
re_parse_title = re.compile(r'{([^{}]+)}(\/\/[^\n]+(T_[^\n]+))')

re_extract_enum_title = re.compile(r'enum{\s*([,]?T_[^\n]+\s+)+};')
re_check_enum_title = re.compile(r'(T_[^\n\s]+)[^\n]+')
re_parse_enum_title = re.compile(r'(T_[^\n\s]+)[^\n]+(\/\/[^\n]+)')

re_parse_kpd_declaration = re.compile(r'extern ([A-Z_a-z0-9]+)\s+\/\/')
re_parse_kpd_vari_define = re.compile(r'#define K_(K_[A-Z_0-9]+)\s+([0-9]+)')
re_parse_kpd_vari = re.compile(r'[,]?(k_[a-zA-Z_0-9]+)(\[([a-zA-Z_0-9]+)\])?\s*(\/\/[^\n]*)?')


def read_kpd_para_vari(contents):
    vari_type = "WORD"
    defines_dict = {}
    buf = io.StringIO(contents) 
    for line in buf.readlines():

        find_list = re_parse_kpd_declaration.findall(line)
        if( len(find_list) ):
            # extern WORD ...
            vari_type = find_list[0]
            continue

        find_list  = re_parse_kpd_vari_define.findall(line)
        if( len(find_list) ):
            # [('K_AWAOCONST', '2')]
            defines_dict[find_list[0][0]] = int(find_list[0][1])
            continue
        find_list = re_parse_kpd_vari.findall(line)
        if( len(find_list) ):
            # example
            #,k_awMotNoloadCurr[K_AWMOTNOLOADCURR]              //PJW 2005/02/22
            # (group0         )(group1(group2)   )              (group3       )
            try: 
                array_footer = '['+ str(defines_dict[find_list[0][2]]) + ']'
            except KeyError:
                array_footer = ""  
            # {'k_wUnlmtCarrFreqSel': ['WORD', '//변수설명']}
            yield {find_list[0][0] + array_footer: [vari_type, find_list[0][3]] }
            continue
    pass

def read_enum_title(contents):
    find_list =  []
    search_file_obj = re_extract_enum_title.search(contents)
    if( search_file_obj ):
        search_string = search_file_obj.string[search_file_obj.start(0):]
        # print(search_string )
        buf = io.StringIO(search_string) 
        for line in buf.readlines():
            search_line_obj = re_check_enum_title.search(line)
            if(search_line_obj):
                searched_line =  search_line_obj.string[search_line_obj.start(0):]
                # print(searched_line)
                # example
                #,T_LangBankEmpty               //94
                # (group0        )              (group1)
                find_list = re_parse_enum_title.findall(searched_line)
                if( len(find_list) ):
                    # {'T_nnn5kW4': '//1065'}
                    yield {find_list[0][0]: find_list[0][1] } 
    else: 
        yield None
    pass



def read_basic_title(contents):
    yield None
    find_list =  []
    search_file_obj = re_extract_basic_title_vari.search(contents)
    if( search_file_obj ):
        search_string = search_file_obj.string[search_file_obj.start(0):]
        # print(search_string )
        buf = io.StringIO(search_string) 
        for line in buf.readlines():
            search_line_obj = re_check_title.search(line)
            if(search_line_obj):
                searched_line =  search_line_obj.string[search_line_obj.start(0):]
                # print(searched_line)
                find_list = re_parse_title.findall(searched_line)
                # example
                #  {0x45,0x6E,0x67,0x6C,0x69,0x73,0x68,0x20,0x20,0x20,0x20,0x20,0x20,0x20}//0    "English        "T_Language
                #   (group0                                                              )(group1                 (group2  ))
                if( len(find_list) ):
                    temp_string = find_list[0][0].replace('0x', '')
                    temp_string = temp_string.replace(',', '')
                    # {'T_UMarrMCn': ['55264D094D434020202020202020', '//726  "U&M\tMC@        "T_UMarrMCn']}
                    yield {find_list[0][2]:[temp_string, find_list[0][1]]} 
    else: 
        yield None
    pass

def read_add_title(contents):
    find_list =  []
    search_file_obj = re_extract_add_title_vari.search(contents)
    if( search_file_obj ):
        search_string = search_file_obj.string[search_file_obj.start(0):]
        # print(search_string )
        buf = io.StringIO(search_string) 
        for line in buf.readlines():
            search_line_obj = re_check_title.search(line)
            if(search_line_obj):
                searched_line =  search_line_obj.string[search_line_obj.start(0):]
                # print(searched_line)
                find_list = re_parse_title.findall(searched_line)
                #  {0x45,0x6E,0x67,0x6C,0x69,0x73,0x68,0x20,0x20,0x20,0x20,0x20,0x20,0x20}//0    "English        "T_Language
                #   (group0                                                              )(group1                 (group2  ))
                if( len(find_list) ):
                    temp_string = find_list[0][0].replace('0x', '')
                    temp_string = temp_string.replace(',', '')
                    # {'T_RegenAvdIgain': ['526567656E41766420496761696E', '//1005 "RegenAvd Igain      "T_RegenAvdIgain']}
                    yield {find_list[0][2]:[temp_string, find_list[0][1]]} 
    else: 
        yield None
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

# 파일 이름 별로 파싱 루틴을 다르게 적용하지만 실제로 파일에 관계 없이 동작하도록 해야함. 
def test():
    for root, directories, filenames in os.walk(TARGET_DIR):
        print(root, directories, filenames)
        
        for filename in filenames:
            if( filename.lower() not in parsing_file_list ): 
                continue
            contents = ""
            filePath = root + os.sep + filename
            grpName = ""
            with open(filePath, 'r', encoding='utf8') as f:
                contents = f.read()
    
            # print(filePath)
            if(filename.lower() == KPD_PARA_TABLE_SRC_FILE ):
                read_grp(contents)
            elif ( filename.lower() == KPD_BASIC_TITLE_SRC_FILE):
                for item in read_basic_title(contents):
                    # print(item)
                    pass
            elif( filename.lower() == KPD_ADD_TITLE_SRC_FILE):
                for item in read_add_title(contents):
                    # print(item)
                    pass
            elif( filename.lower() == KPD_ENUM_TITLE_HEADER_FILE):
                for item in read_enum_title(contents):
                    # print(item)
                    pass
            elif ( filename.lower() == KPD_PARA_VARI_HEADER_FILE):
                for item in read_kpd_para_vari(contents):
                    print(item)
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
    print('finished')

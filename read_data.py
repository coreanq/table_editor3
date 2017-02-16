import os
import re
import io
# parsing 방법
# 전체 파일을 한번에 읽음
# 파일 명에 상관없이 변수 명을 통해 그 파싱 내용이 어느 부분 데이터 인지 파악함
# 각 인자들 파싱 

KPD_ADD_TITLE_SRC_FILE = 'AddTitle_Eng.c'
KPD_ADD_TITLE_HEADER_FILE = 'AddTitle_Eng.H'
KPD_FUNC_HEAD_HEADER_FILE = 'KFunc_Head.H'
KPD_BASIC_TITLE_SRC_FILE='KPD_TBL_MSG_ENG.c'
KPD_ENUM_TITLE_HEADER_FILE = 'KPD_Title_Enum.H'
KPD_GRP_INDEX_HEADER_FILE = 'KpdPara_GrpIdx.H'

KPD_PARA_MSG_SRC_FILE =  'KpdPara_Msg.c'
KPD_PARA_MSG_HEADER_FILE = 'KpdPara_Msg.h'
KPD_PARA_STRUCT_UNIT_HEADER_FILE = 'KpdPara_StructUnit.h'
KPD_PARA_TABLE_SRC_FILE = 'KpdPara_Table.c'
KPD_PARA_TABLE_HEADER_FILE = 'KpdPara_Table.h'

KPD_PARA_VAR_SRC_FILE = 'KpdPara_Vari.c'
KPD_PARA_VAR_HEADER_FILE = 'KpdPara_Vari.H'

# neweraplatform kpd_index 파일
DRVPARA_DATASTORAGE_SRC_AUTO = 'DrvPara_DataStorage_Auto.c'
DRVPARA_DATASTORAGE_HEADER_AUTO = 'DrvPara_DataStorage_Auto.h'

# write 에 사용하는 파일 리스트 정의
make_files = (
    KPD_ADD_TITLE_SRC_FILE,
    KPD_ADD_TITLE_HEADER_FILE,
    KPD_FUNC_HEAD_HEADER_FILE,
    KPD_BASIC_TITLE_SRC_FILE,
    KPD_ENUM_TITLE_HEADER_FILE,
    KPD_GRP_INDEX_HEADER_FILE,
    KPD_PARA_MSG_SRC_FILE,
    KPD_PARA_MSG_HEADER_FILE,
    KPD_PARA_STRUCT_UNIT_HEADER_FILE,
    KPD_PARA_TABLE_SRC_FILE,
    KPD_PARA_TABLE_HEADER_FILE,
    KPD_PARA_VAR_SRC_FILE,
    KPD_PARA_VAR_HEADER_FILE,
    DRVPARA_DATASTORAGE_SRC_AUTO,
    DRVPARA_DATASTORAGE_HEADER_AUTO
)

# read 에 사용하는 파싱 파일 리스트 정의 
parsing_files = (   
    KPD_BASIC_TITLE_SRC_FILE,
    KPD_ADD_TITLE_SRC_FILE,
    KPD_PARA_MSG_SRC_FILE,
    KPD_PARA_STRUCT_UNIT_HEADER_FILE,
    KPD_PARA_TABLE_SRC_FILE
)               




re_extract_kpd_para_unit = re.compile(r'(?P<para_unit>{[^{}]*(U_[^,=]+[,]?)+[^{}]*})')
re_parse_kpd_para_unit_params = re.compile(r'(U_[^,= ]+)')

re_extract_grp = re.compile(r'(?P<group_data>S_TABLE_X_TYPE t_ast(?P<group_name>[A-Z0-9]{2,3})grp[^;]+\}\;)') # 한개의 그룹 뽑아냄 
re_check_params = re.compile(r'{(?P<parameters>[^\n]+)}.?(?P<comment>[^\n]+)')
re_parse_params = re.compile(r'(\([A-Z*]+\))?&?([^,{}\n;]+)')
re_parse_comment = re.compile(r'"([^\n]+)"((\[EDS :([-0-9]*)[,]?([-0-9 ]*)\])?\/\/([^\n]*))*')

re_extract_grp_info = re.compile(r'(?P<group_info_data>S_GROUP_X_TYPE t_astGrpInfo[^;]+\}\;)') # 한개의 그룹 정보 뽑아냄 
re_check_grp_info = re.compile(r'{(?P<grp_info>[^\n]+)}[,]?')
re_parse_grp_info = re.compile(r'(\([A-Z*]+\))?&?([^,{}\n;]+)')

re_extract_msg = re.compile(r'(?P<msg_data>S_MSG_TYPE t_ast(?P<msg_name>[A-Z-a-z_0-9]+)[^\n]+\/\/(?P<msg_info>[^\n]+)\/\/(?P<msg_info_comment>[^\n]*)[^;]+\;)') # 한개의 그룹 뽑아냄 
re_check_msg_info = re.compile(r'S_MSG_TYPE t_ast[A-Z-a-z_0-9]+[^\n]+\/\/([^\n]+)\/\/([^\n]+)')
re_check_msg_params = re.compile(r'{(?P<parameters>[^\n]+)}.?(?P<comment>[^\n]+)')
re_parse_msg_params = re.compile(r'([^,{}\n;]+)')
re_parse_msg_comment = re.compile(r'\/\/"([^\n]+)"')

# table editor 파일의 버전정보 추출 
re_extract_version_info = re.compile(r'Table Edit[a-z]{0,2} (?P<table_editor_number>[0-9]) V(?P<table_editor_version>[0-9](.[0-9]+){0,3})', re.I)
# check 의 경우 input 의 값이 원하는 형식인지 파악 parse 의 경우 input 에서 param 리스트를 뽑아냄  
re_extract_basic_title_var = re.compile(r'BYTE kpdParaTitleEng[^;]+};')
re_extract_add_title_var = re.compile(r'const WORD g_awAddTitleEng[^;]+};')
re_check_title = re.compile(r'{(?P<parameters>[^\n]+)}(?P<comment>\/\/[^\n]+)')
re_parse_title_params = re.compile(r'([^,{}\n;]+)')
re_parse_title_comment = re.compile(r'\/\/([0-9]+)[^\n\"]+\"([^\n]+)\"(T_[^\n]+)')

re_parse_kpd_declaration = re.compile(r'extern ([A-Z_a-z0-9]+)\s+\/\/')
re_parse_kpd_var_define = re.compile(r'#define (K_[A-Z_0-9]+)\s+([0-9]+)')
re_parse_kpd_var = re.compile(r'(k_[a]?w[a-zA-Z_0-9]+)(\[([a-zA-Z_0-9]+)\])?s*\/\/([^\n]*)?')
re_parse_kpd_var_only = re.compile(r'k_[a]?w([a-zA-Z_0-9]+)(\[([a-zA-Z_0-9]+)\])?', re.I)

# re_extract_enum_title = re.compile(r'enum{\s*([,]?T_[^\n]+\s+)+};')
# re_check_enum_title = re.compile(r'(T_[^\n\s]+)[^\n]+')
# re_parse_enum_title = re.compile(r'(T_[^\n\s]+)[^\n]+(\/\/[^\n]+)')

def read_kpd_para_struct_unit(contents):
    search_obj = re_extract_kpd_para_unit.search(contents)
    if( search_obj ):
        data_part = search_obj.group('para_unit')
        find_list = re_parse_kpd_para_unit_params.findall(data_part)
        yield find_list 
    pass
        
def read_para_table_version(contents):
    search_obj  = re_extract_version_info.search(contents)
    table_editor_number = ''
    table_editor_version = '' 
    if( search_obj ):
         table_editor_number = search_obj.group('table_editor_number')
         table_editor_version = search_obj.group('table_editor_version')
    return table_editor_number, table_editor_version 
    
def read_para_table(contents):
    find_list = []
    search_grp_iter = re_extract_grp.finditer(contents)
    for match in search_grp_iter:
        # all contents, groupname
        group_name = match.group('group_name')
        group_data = match.group('group_data')
        buf = io.StringIO(group_data) 
        for line in buf.readlines():
            search_line_obj = re_check_params.search(line)
            if(search_line_obj):
                data_part =  search_line_obj.group('parameters')
                comment_part = search_line_obj.group('comment')
                find_list = re_parse_params.findall(data_part)
                # // "Cmd Frequency "[EDS :60000,]//20110519 whko modified MISRA 0-3635
                #     (group1)       group(2)(group(3)group(4))    group(5)
                comment_list = re_parse_comment.findall(comment_part)
                # 검색 결과는 하나만 나옴 
                # eds_max, eds_min, comment
                comment_list = comment_list[0][3], comment_list[0][4], comment_list[0][5]
                # print(comment_list)
                # (WORD)blahblah
                # item[0] item[1]
                yield (group_name, *[item[1].strip() for item in find_list], *comment_list )

def read_para_msg(contents):
    find_list = []
    search_grp_iter = re_extract_msg.finditer(contents)
    for match in search_grp_iter:
        # all contents, groupname
        msg_name = match.group('msg_name')
        msg_data = match.group('msg_data')
        msg_info = match.group('msg_info')
        msg_info_comment = match.group('msg_info_comment') 
        buf = io.StringIO(msg_data) 
        for line in buf.readlines():
            search_line_obj = re_check_msg_params.search(line)
            if( search_line_obj ):
                data_part =  search_line_obj.group('parameters')
                comment_part = search_line_obj.group('comment')
                find_list = re_parse_msg_params.findall(data_part)
                # {T_nndnkW            ,2     }                           //" 0.2 kW       " 
                comment = ""
                comment_search_obj = re_parse_msg_comment.search(comment_part)
                if( comment_search_obj ):
                    comment = comment_search_obj.group(1)
                # para msg col info 에 맞춰서 형식을 만들어 줌 
                yield (msg_name, msg_info_comment,  find_list[0].strip() , "", find_list[1].strip())
    pass               
    
def read_grp_info(contents):
    match = re_extract_grp_info.search(contents)
    if( match ):
        group_info_data = match.group('group_info_data') 
        buf = io.StringIO(group_info_data) 
        for line in buf.readlines():
            search_line_obj = re_check_grp_info.search(line)
            if(search_line_obj):
                data_part =  search_line_obj.group('grp_info')
                find_list = re_parse_grp_info.findall(data_part)
                result = []
                for item in find_list:
                    result.append(item[1])
                # {dummy_key, T_MAK     ,GRP_MAK_CODE_TOTAL  ,(WORD*)&g_wMakGrpShow    ,0x01      },
                yield '', result[0].replace('T_', '').strip(), result[2].strip(), result[3].strip()
    


def read_kpd_para_var(contents):
    var_type = "WORD"
    defines_dict = {}
    buf = io.StringIO(contents) 
    for line in buf.readlines():
        find_list = re_parse_kpd_declaration.findall(line)
        if( len(find_list) ):
            # extern WORD ...
            var_type = find_list[0]
            continue
        find_list  = re_parse_kpd_var_define.findall(line)
        if( len(find_list) ):
            # [('K_AWAOCONST', '2')]
            defines_dict[find_list[0][0]] = find_list[0][1]
            continue
        find_list = re_parse_kpd_var.findall(line)
        if( len(find_list) ):
            # example
            #,k_awMotNoloadCurr[K_AWMOTNOLOADCURR]              //PJW 2005/02/22
            # (group0         )(group1(group2)   )              (group3       )
            try: 
                array_footer = '['+ str(defines_dict[find_list[0][2]]) + ']'
            except KeyError:
                array_footer = ""  
            # ('dummy_key', 'k_wUnlmtCarrFreqSel': ['WORD', '//변수설명'] )
            yield ('', find_list[0][0] + array_footer, var_type, find_list[0][3]) 
            continue
    pass


def read_basic_title(contents):
    find_list =  []
    search_file_obj = re_extract_basic_title_var.search(contents)
    if( search_file_obj ):
        search_string = search_file_obj.string[search_file_obj.start(0):]
        # print(search_string )
        buf = io.StringIO(search_string) 
        for line in buf.readlines():
            search_line_obj = re_check_title.search(line)
            if(search_line_obj):
                data_part = search_line_obj.group('parameters')
                comment_part = search_line_obj.group('comment')
                find_list = re_parse_title_params.findall(data_part)
                #  {0x45,0x6E,0x67,0x6C,0x69,0x73,0x68,0x20,0x20,0x20,0x20,0x20,0x20,0x20}//0    "English        "T_Language
                comment_search_obj = re_parse_title_comment.search(comment_part)
                comment_list = []
                # //0    "English        "T_Language
                # group1  group2           group3
                if( comment_search_obj ):
                    comment_list = comment_search_obj.group(2), comment_search_obj.group(3), comment_search_obj.group(1)

                data_string = ''.join(find_list)
                data_string= data_string.replace('0x', '')
                yield ('', *comment_list, data_string) 
    pass

def read_add_title(contents):
    find_list =  []
    search_file_obj = re_extract_add_title_var.search(contents)
    if( search_file_obj ):
        search_string = search_file_obj.string[search_file_obj.start(0):]
        # print(search_string )
        buf = io.StringIO(search_string) 
        for line in buf.readlines():
            search_line_obj = re_check_title.search(line)
            if(search_line_obj):
                data_part = search_line_obj.group('parameters')
                comment_part = search_line_obj.group('comment')
                find_list = re_parse_title_params.findall(data_part)
                #  {0x45,0x6E,0x67,0x6C,0x69,0x73,0x68,0x20,0x20,0x20,0x20,0x20,0x20,0x20}//0    "English        "T_Language
                comment_search_obj = re_parse_title_comment.search(comment_part)
                comment_list = []
                # //0    "English        "T_Language
                # group1  group2           group3
                if( comment_search_obj ):
                    comment_list =  comment_search_obj.group(2).strip(),\
                                    comment_search_obj.group(3).strip(),\
                                    comment_search_obj.group(1).strip()

                data_string = ''.join(find_list)
                data_string= data_string.replace('0x', '')
                yield ('', *comment_list, data_string) 
    pass


# 파일 이름 별로 파싱 루틴을 다르게 적용하지만 실제로 파일에 관계 없이 동작하도록 해야함. 
def test_read():
    TARGET_DIR = r'D:\download\1'
    for root, directories, filenames in os.walk(TARGET_DIR):
        # print(root, directories, filenames)
        for filename in filenames:
            if( filename.lower() in parsing_files):
                contents = ""
                filePath = root + os.sep + filename
                with open(filePath, 'r', encoding='utf8') as f:
                    contents = f.read()
                if(filename.lower() == KPD_PARA_TABLE_SRC_FILE ):
                    for item in read_para_table(contents):
                        # print(item)
                        pass
                    for item in read_grp_info(contents):
                        # print(item)
                        pass
                    pass
                elif( filename.lower() == KPD_PARA_MSG_SRC_FILE):
                    for item in read_para_msg(contents):
                        # print(item)
                        pass
                elif( filename.lower() == KPD_BASIC_TITLE_SRC_FILE):
                    for item in read_basic_title(contents):
                        pass 
                        # print(item)
                elif( filename.lower() == KPD_ADD_TITLE_SRC_FILE ):
                    for item in read_add_title(contents):
                        # print(item)
                        pass
                    pass
                elif( filename.lower() == KPD_PARA_VAR_HEADER_FILE):
                    for item in read_kpd_para_var(contents):
                        # print(item)
                        pass
                elif( filename.lower() == KPD_PARA_STRUCT_UNIT_HEADER_FILE ):
                    for item in read_kpd_para_struct_unit(contents):
                        print(item) 
                        pass
                pass

def test_write():
    from PyQt5.QtCore import QFile, QIODevice
    TARGET_DIR  = r'd:\download\result' 
    # qrc 내에 있는 파일에 접근할 수 있는 것은 QFile 만 가능함 
    file = QFile(r':/base/' + KPD_ADD_TITLE_SRC_FILE)
    print(file.open(QIODevice.ReadOnly))
    contents = bytearray(file.readAll()).decode('utf8')

    for item in read_add_title(contents):
        print(item)
    
    # with open(r':/base/'+ KPD_ADD_TITLE_SRC_FILE, 'r', encoding='utf8') as f:
    #     contents = f.read()
    #     print(contents)

   
if __name__ == '__main__':
    # test_read() 
    test_write()
    print('finished')

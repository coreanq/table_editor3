import sys, os, re
import column_info as ci
import read_data as rd
'''
re_kpd_var:
아래 같은 형태의 keypad 변수가 파싱 가능함 
k_w1234
k_w123kd = 
k_w123kd= 
&k_w123kd= 
k_wAutoTuneMode == 0
k_wAutoTuneMode==0

re_kpd_var_array:
k_aw1234[123]
k_aw1234[ 1234]
k_aw1234[Num]
k_aw1243[Adk - 1 ]
k_aw1243[Adk - 1 ] = 
k_aw1243[Adk - 1 ] ==
k_aw1243[Adk - 1 ]==
k_aw1243[Adk - 1 ]=
&k_aw1243[Adk - 1 ]

FIXME: 한줄에 키패드 변수 2개 이상 나오는 경우 
k_wLoopMaxTime = k_wLoopMeanTime  --> 오류남 
'''

# re group info: [0]: all [?]: &a-z [1]: 123kd [2]: = or ==
re_kpd_var = re.compile(r'[^\w\&](k_w[\w]+)\s*([\=]*)')
# re group info: [0]: all [1]: & [2]: 123kd [3]: abc -1  [4]: = or ==
re_kpd_var_array  = re.compile(r'(\&)?k_aw([\w]+)\[([\w -]+)\]\s*([\=]*)')

re_grp_and_code = re.compile(r'([A-Z0-9]{2,3}_[0-9]{3})')


def chage_kpd_vari(parameter_model, target_dir):
    target_file_list = []
    # file list gathering
    for (dirpath, dirnames, filenames) in os.walk(target_dir):
        for name in filenames:
            extension_name = os.path.splitext(name)[1].lower() 
            if( extension_name == '.c' ):
                if( 'stm32' not in name.lower()):
                    target_file_list.append(dirpath + os.path.sep + name)
    # print('\n'.join(target_file_list))

    # open file and read line by line and print keypad variable 
    for file_path in target_file_list:
        pre_contents = [] # 변환되기전 파일에서 읽은 데이터 
        contents = []
        with open(file_path, 'r', encoding='utf8') as f:
            pre_contents = f.readlines()
        
        isSearch = False
        for count, line in enumerate(pre_contents):
            find_objs = re_kpd_var.finditer(line)

            # finding keypad variable  대입문은 찾지 않는다.
            for match_obj in find_objs:
                if( match_obj.group(2) != '=' ):
                    keypad_vari_name = match_obj.group(1)
                    name = ''

                    items = parameter_model.findItems(keypad_vari_name, column = ci.para_col_info_for_view().index('ParaVar'))
                    # 한개만 찾아짐 
                    for item in items:
                        row = item.row()
                        name = parameter_model.item(row, ci.para_col_info_for_view().index('Name')).text()
                        break

                    ret = line.replace(keypad_vari_name, 
                                r'DriveParaReadData( {0}, {1} )'.format(
                                     name, 
                                    'SENDER_SYSTEM'
                                ), 
                            )
                    print(line + '->' + ret )
                    line = ret
                    isSearch = True
            contents.append(line)

        if( isSearch ) : 
            with open(file_path , 'w', encoding= 'utf8') as f:
                f.writelines(contents)
            print(file_path)

        isSearch = False
        contents.clear()

def addExternC(target_dir):
    re_header_guard_start = re.compile(r'#define[\s]+([A-Z_]+_H_)')
    exception_list = ['CarrierFreqByTemp.h', 'rtwtypes.h']
    target_file_list = []
    for (dirpath, dirnames, filenames) in os.walk(target_dir):
        for name in filenames:
            extension_name = os.path.splitext(name)[1].lower() 
            if( extension_name == '.h' ):
                if( 'stm32' not in name.lower()):
                    if( name not in exception_list ):
                        target_file_list.append(dirpath + os.path.sep + name)
    # print('\n'.join(target_file_list))

    header_start = '''
#if defined(__cplusplus)
extern "C" {
#endif
'''
    header_end = '''\n#if defined(__cplusplus)
}
#endif\n
'''
    # open file and read line by line and print keypad variable 
    for file_path in target_file_list:
        pre_contents = [] # 변환되기전 파일에서 읽은 데이터 
        contents = []
        with open(file_path, 'r', encoding='utf8') as f:
            pre_contents = f.readlines()
        
        isSearch = False
        header_start_pos = -1 
        header_end_pos = -1

        for count, line in enumerate(pre_contents):
            find_obj = re_header_guard_start.search(line)
            if(find_obj):
                header_start_pos = count; 
                break
        
        isSearch = False
        if( header_start_pos != -1):
            isSearch = True
            pre_contents.insert( header_start_pos +1,  header_start )
        
        if( isSearch ) : 
            for count, line in enumerate(pre_contents[::-1]):
                if( '#endif' in line ):
                    pre_contents.insert(len(pre_contents) - count -1,  header_end )
                    break
                pass

            with open(file_path , 'w', encoding= 'utf8') as f:
                f.writelines(pre_contents)

            print(''.join(pre_contents))
            print('------------------------------------------------------------------')

    pass

if __name__ == '__main__' :
    addExternC(r'd:\\download\\3_work\\Drive_SW_Platform\\src\\trunk\\NewEraPlatform\\Source\\Inverter')
    pass
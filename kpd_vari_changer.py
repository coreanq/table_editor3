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


target_dir = 'd:\\download\\3_work\\Drive_SW_Platform\\src\\branches\\NewEraPlatform_kpd_index\\Source\\Inverter\\'


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


        # for count, line in enumerate(pre_contents):
        #     # kpd func 의 mak_000 형태의 변수 변환 
        #     find_objs = re_grp_and_code.finditer(line)

        #     for match_obj in find_objs:
        #         grp_and_code = match_obj.group(1).strip()
        #         src_grp_name = grp_and_code.split('_')[0]
        #         src_code_name = grp_and_code.split('_')[1]

        #         items = parameter_model.findItems(src_grp_name, column = ci.para_col_info_for_view().index('Group'))
        #         for item in items:
        #             row = item.row()
        #             searched_code_name = parameter_model.item(row, column = ci.para_col_info_for_view().index('Code#')).text()

        #             if( src_code_name == '{0:>03}'.format(searched_code_name) ):
        #                 para_vari_name = parameter_model.item(row, column =ci.para_col_info_for_view().index('ParaVar')).text()
        #                 name = rd.changeParaName2Enum(para_vari_name)

        #                 ret = line.replace(grp_and_code,  name , )
        #                 print(line + '->' + ret )
        #                 line = ret
        #                 isSearch = True 


        #     contents.append(line)
        # if( isSearch ) : 
        #     with open(file_path , 'w', encoding= 'utf8') as f:
        #         f.writelines(contents)
        #     print(file_path)

            # finding keypad_array varialbe
            # find_objs = re_kpd_var_array.finditer(line)
            # for match_obj in find_objs:
            #     if( match_obj.group(1) == None and match_obj.group(4) != '=' ):
            #         index_str = ''
            #         if( match_obj.group(3) == '0'):
            #             index_str = ''
            #         else:
            #             index_str  = '+ ' + match_obj.group(3)

            #         finded_word = match_obj.group(0)
            #         ret  = line.replace(finded_word,
            #                     r'DrvParaGetWordData(E_DATA_CMD_{0}_00 {1} ) {2}'.format(
            #                         match_obj.group(2).upper(),
            #                         index_str,
            #                         match_obj.group(4)
            #                     ),
            #                     1 # 같은 줄에 같은 이름의 k_wAsrSLPGain, k_wAsrSLPGain2 변수가 있는 경우 문제 생기므로 하나만 변경 
            #                 ) 
            #         # print(line + '\t\t\t  ----> ' + ret )
            #         line = ret
        #     #         isSearch = True
        # if( isSearch ) : 
        #     with open(file_path , 'w', encoding= 'utf8') as f:
        #         f.writelines(contents)
        #     print(file_path)
        # isSearch = False


if __name__ == '__main__' :
    pass
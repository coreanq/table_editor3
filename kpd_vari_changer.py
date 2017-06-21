import sys, os, re
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

# re group info: [0]: all [1]:& [2]:123kd [3] =  or ==
re_kpd_var = re.compile(r'(\&)?k_w([\w]+)\s*([\=]*)')
# re group info: [0]: all [1]: & [2]: 123kd [3]: abc -1  [4]: = or ==
re_kpd_var_array  = re.compile(r'(\&)?k_aw([\w]+)\[([\w -]+)\]\s*([\=]*)')


target_dir = 'd:\\download\\3_work\\Drive_SW_Platform\\src\\branches\\NewEraPlatform_kpd_index\\Source\\Inverter\\'

if __name__ == '__main__' :
    target_file_list = []
    # file list gathering
    for (dirpath, dirnames, filenames) in os.walk(target_dir):

        for name in filenames:
            extension_name = os.path.splitext(name)[1].lower() 
            if( extension_name == '.c' or extension_name =='.h' ):
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

            # finding key_pad variable
            for match_obj in find_objs:
                if( match_obj.group(1) == None and match_obj.group(3) != '=' ):
                    finded_word = match_obj.group(0)
                    ret = line.replace(finded_word, 
                                r'DrvParaGetWordData(E_DATA_CMD_{0}) {1}'.format(
                                    match_obj.group(2).upper(),
                                    match_obj.group(3)
                                ), 
                                1 # 같은 줄에 같은 이름의 k_wAsrSLPGain, k_wAsrSLPGain2 변수가 있는 경우 문제 생기므로 하나만 변경 
                            )
                    # print(line + '\t\t\t  ----> ' + ret )
                    line = ret
                    isSearch = True
                
            # finding key_pad_array varialbe
            find_objs = re_kpd_var_array.finditer(line)
            for match_obj in find_objs:
                if( match_obj.group(1) == None and match_obj.group(4) != '=' ):
                    index_str = ''
                    if( match_obj.group(3) == '0'):
                        index_str = ''
                    else:
                        index_str  = '+ ' + match_obj.group(3)

                    finded_word = match_obj.group(0)
                    ret  = line.replace(finded_word,
                                r'DrvParaGetWordData(E_DATA_CMD_{0}_00 {1} ) {2}'.format(
                                    match_obj.group(2).upper(),
                                    index_str,
                                    match_obj.group(4)
                                ),
                                1 # 같은 줄에 같은 이름의 k_wAsrSLPGain, k_wAsrSLPGain2 변수가 있는 경우 문제 생기므로 하나만 변경 
                            ) 
                    # print(line + '\t\t\t  ----> ' + ret )
                    line = ret
                    isSearch = True

            contents.append(line)

        if( isSearch ) : 
            with open(file_path , 'w', encoding= 'utf8') as f:
                f.writelines(contents)
            print(file_path)
            isSearch = False




import os, sys, re, datetime
import column_info as ci

import read_data as rd
import version

ATTR_BYTE = 0x0001  # byte 단위 사용 안함 
ATTR_UP = 0x0002
ATTR_LP = 0x0004
ATTR_READ_ONLY = 0x0008
ATTR_NO_CHANGE_ON_RUN =  0x0010
ATTR_ZERO_INPUT = 0x0020
ATTR_NO_COMM =0x0040
ATTR_ENT = 0x0080
ATTR_HIDDEN_CON = 0x0700
ATTR_ADD  = 0x1000

banner = '''\
//------------------------------------------------------------------------------
//      Auto generated from TABLE EDITOR {0} V{1}    {2}
//------------------------------------------------------------------------------
'''.format(
    version.TABLE_EDITOR_NUMBER, 
    version.VERSION_INFO,
    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

def makeHiddenCondition(attribute):
    hidden_condition = '' 
    val = (attribute & ATTR_HIDDEN_CON) >> 8
    if( val == 0 ):
        hidden_condition = '=='
    elif ( val == 1 ):
        hidden_condition = '>'
    elif ( val == 2 ):
        hidden_condition = '<'
    elif( val  == 3 ) :
        hidden_condition = '!='
    return hidden_condition

def hiddenConditionToValue(hidden_condition ):
    value = 0
    if( hidden_condition == '=='):
        value = 0
    elif ( hidden_condition == '>'):
        value = 1
    elif( hidden_condition == '<'):
        value = 2
    elif( hidden_condition == '!='):
        value = 3
    return value

def make_title_with_at_value(title, at_value, padding = ''):
    # padding  이 있는 이유는 parameter 랑 msg 의 at value 생성 방식이 다르기 때문이다. 
    # title 내 at value 설정 
    at_count = 0
    result = title
    if( at_value.lower() == '0xff'):
        title.replace('@', '0')
        result = title
    else:
        if( title.count('#') == 0 ):
            at_count = title.count('@')
            at_value = '{value:{padding}>{count}}'.format(value = at_value, count = at_count, padding = padding)

            for value in at_value:
                result = result.replace('@', value, 1)
        else:
            at_value = at_value.replace('\'', '')
            result = result.replace('#', at_value)

    return result

def make_add_title_eng(source_path, title_model):
    col_info = ci.title_col_info()
    model = title_model 
    row = model.rowCount()
    col = model.columnCount()

    rows = []
    total_add_title = 0
    add_title_size = 0
    enum_list = []

    for row_index in range(row):
        row_items = []
        for col_index in range(col):
            item = model.item(row_index, col_index)
            row_items.append(item.text()) 

        title = row_items[col_info.index('Title')]
        enum_name = row_items[col_info.index('Enum 이름')]
        title_index = row_items[col_info.index('Title Index')]
        data = row_items[col_info.index('Data')]

        if( title_index == ''):
            title_index_num = 0
        else:
            title_index_num = int(title_index)

        # enum_list 생성용  for kpd_title_enum.h
        if( title_index_num == 1000):
            enum_list.append('T_TotalDefaultTitleSize')
            enum_list.append(r'{0:<32} = START_ADD_TITLE_INDEX//{1}'.format(enum_name, title_index))
        else:
            enum_list.append(r'{0:<32}//{1}'.format(enum_name, title_index))

        if( title_index_num < 1000):
            continue

        total_add_title = total_add_title + 1   
        # hex data 4개씩 짜름 
        re_split = re.compile(r'[a-z0-9A-Z]{4,4}')
        find_list = re_split.findall(data)
        add_title_size = len(find_list)
        find_merge = ','.join('0x'+item for item in find_list )
        rows.append(r'{{{0}}}//{1:<5}"{2:<20}"{3}'.format(find_merge, title_index, title, enum_name))
    # print('\n'.join(rows))

    
    src_template= \
'''{0}
#include "BaseDefine.H"
#include "AddTitle_Eng.H"\n\n\n
const WORD g_awAddTitleEng[TOTAL_ADD_TITLE][ADD_TITLE_SIZE] = {{ 
 {1}
}};
'''
    file_contents = src_template.format(
        banner, 
        '\n,'.join(rows)
        )

    with open(source_path + os.path.sep + rd.KPD_ADD_TITLE_SRC_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

    header_template= \
'''{0}
#ifndef ADD_TITLE_ENG_H
#define ADD_TITLE_ENG_H\n\n
#define TOTAL_ADD_TITLE       {1} 
#define ADD_TITLE_SIZE        {2} 
extern const WORD g_awAddTitleEng[TOTAL_ADD_TITLE][ADD_TITLE_SIZE];\n
#endif   //ADD_TITLE_ENG_H 
'''

    file_contents = header_template.format(
        banner, 
        total_add_title, 
        add_title_size
        )
    with open(source_path + os.path.sep + rd.KPD_ADD_TITLE_HEADER_FILE, 'w') as f:
        f.write(file_contents)
    pass


    kpd_title_enum_header_template= \
'''{0}
#ifndef KPD_TITLE_ENUM_H
#define KPD_TITLE_ENUM_H

#define START_ADD_TITLE_INDEX 1000

enum{{ 
  {1}
}};
{2}
#endif
'''
    enum_list.append('T_TotalAddTitleSize')
    if( total_add_title ):
        have_add_title = '#define HAVE_ADD_TITLE	//Add Title이 존재할때만 Define 된다.'
    else:
        have_add_title = ''

    file_contents = kpd_title_enum_header_template.format(
        banner, 
        '\n ,'.join(enum_list), 
        have_add_title
        )
    with open(source_path + os.path.sep + rd.KPD_ENUM_TITLE_HEADER_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

# def make_kpdpara_var(source_path, variable_model):
#     col_info = ci.variable_col_info()
#     model = variable_model 
#     row = model.rowCount()
#     col = model.columnCount()

#     define_list = []
#     var_list = []
#     var_type = ''

#     for row_index in range(row):
#         row_items = []
#         for col_index in range(col):
#             item = model.item(row_index, col_index)
#             row_items.append(item.text()) 

#         variable = row_items[col_info.index('Variable')]
#         var_type = row_items[col_info.index('Type')]
#         description = row_items[col_info.index('Description')]

#         re_split = re.compile(r'(k_[a-z0-9A-Z]+)(\[([0-9_A-Z]+)\])?')
#         find_list = re_split.findall(variable)
#         for var_name, dummy, var_arr_cnt in find_list:
#             if( len(var_arr_cnt) ):
#                 define_list.append(r'#define {0:<32}{1}'.format(var_name.upper(), var_arr_cnt ))
#                 variable = re.sub(r'\[([0-9]+)\]', '[' + var_name.upper() + ']', variable )
#             var_list.append('{0:<62}//{1}'.format(variable, description))


#     header_template= \
# '''
# {0}
# #ifndef KPD_PARA_VARI_H
# #define KPD_PARA_VARI_H\n
# {1}\n\n\n
# extern {2}                          //{2} TYPE의 변수들
# {3}
# ;    
# \n\n\n
# #endif    //KPD_PARA_VARI_H
# '''

#     file_contents = header_template.format(
#         banner, 
#         '\n'.join(define_list), 
#         var_type, 
#         '\n,'.join(var_list)
#     ) 
#     # print(var_list)
#     # print(define_list)
#     # print(file_contents)
#     with open(source_path + os.path.sep + rd.KPD_PARA_VAR_HEADER_FILE, 'w', encoding='utf8') as f:
#         f.write(file_contents)
#     pass


#     source_template = \
# '''
# {0}

# #include "BaseDefine.H"
# #include "KpdPara_Vari.H"
# {1}                          //{1} TYPE의 변수들 
# {2}
# ;
# '''
#     file_contents = source_template.format(
#         banner, 
#         var_type, 
#         '\n,'.join(var_list)
#         ) 
#     with open(source_path + os.path.sep + rd.KPD_PARA_VAR_SRC_FILE , 'w', encoding='utf8') as f:
#         f.write(file_contents)
#     pass


def make_kpdpara_msg(source_path, msg_info_model, msg_values_model ):
    col_info = ci.msg_values_col_info()
    key_col_info = ci.msg_info_col_info()
    key_model = msg_info_model  
    model = msg_values_model 

    key_row = key_model.rowCount()
    key_col = key_model.columnCount()

    msg_name_count_list  = []
    msg_vars = [] 
    lines = []
    msg_var_template = \
'''{0:<90}//MSG_{1:<20}//{2}
\t {3}
}};
'''
    msg_name_count = 0 # 각 msg name 에 몇개의 인자가 있는지 나타냄 yesno msg 의 경우 2개 
    msg_name, msg_comment, title_name, at_value  = '', '', '', ''
    # key model 에서 key 값을 추출하여 key_value 모델에서 find 함 
    for row_index in range(key_row):
        key_msg_name = key_model.item(row_index, key_col_info.index('MsgName')).text() 
        msg_name = key_msg_name
        find_items = model.findItems(key_msg_name, column = col_info.index('MsgName'))
        msg_name_count = 0 # 각 msg name 에 몇개의 인자가 있는지 나타냄 yesno msg 의 경우 2개 
        lines = []
        enum_name = ''

        for find_item in find_items:
            find_row_index = find_item.row()

            msg_name = model.item(find_row_index, col_info.index('MsgName')).text()
            msg_comment = model.item(find_row_index, col_info.index('MsgComment')).text()
            title_name = model.item(find_row_index, col_info.index('Title')).text()
            at_value = model.item(find_row_index, col_info.index('AtValue')).text()
            enum_name = model.item(find_row_index, col_info.index('Title Index')).text()
            title_name = make_title_with_at_value(title_name, at_value)

            lines.append('{{{0:<20},{1:<5}}}                       //"{2}"'.format(enum_name, at_value, title_name))
            msg_name_count =msg_name_count + 1


        
        msg_var_banner = 'static const S_MSG_TYPE t_ast{0}[MSG_COUNT_{1}] = {{'\
            .format(msg_name, 
                    msg_name.upper() 
            )
        
        msg_vars.append(
            msg_var_template.format(
                msg_var_banner,
                msg_name, 
                msg_comment, 
                '\n\t,'.join(lines))
        )
        lines.clear()
        msg_name_count_list.append([msg_name, msg_name_count])
        


    source_template = \
'''// PRQA S 502, 4130, 4131, 750, 759, 1514, 3218, 1504, 1505, 1503, 2860, 2895 EOF
{0}        
        
#include "BaseDefine.H"
#include "KPD_Title_Enum.H"
#include "KpdPara_Msg.H"
\n\n
static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], WORD wMsgNum);
\n\n
{1}\n
static const S_MSG_TYPE * t_pastMsgDataTbl[MSG_TOTAL] = {{
\t {2}
}};
static const WORD t_awMsgDataSize[MSG_TOTAL] = {{
\t {3}
}};\n
static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], WORD wMsgNum)
{{
return astMsgType[wMsgNum];
}}
S_MSG_TYPE KpdParaGetMsgData(WORD wMsgIdx, WORD wMsgNum)
{{
return KpdParaGetMsg(t_pastMsgDataTbl[wMsgIdx], wMsgNum);
}}
WORD KpdParaGetMsgSize(WORD wMsgIdx)
{{
return t_awMsgDataSize[wMsgIdx];
}}

'''
    msg_data_tbl_lines = []
    msg_data_size_lines = []
    msg_data_enum_lines = []
    msg_enum_count = 0

    for msg_name, msg_name_count in msg_name_count_list:
        msg_data_tbl_lines.append('t_ast{0}'.format(msg_name))
        msg_data_size_lines.append('MSG_COUNT_{0}'.format(msg_name.upper()))
        msg_data_enum_lines.append('MSG_{0:<36}//{1:0>3}'.format(msg_name, msg_enum_count))
        msg_enum_count = msg_enum_count + 1

    file_contents = source_template.format(  
        banner,
        '\n'.join(msg_vars),
        '\n\t,'.join(msg_data_tbl_lines),
        '\n\t,'.join(msg_data_size_lines) 
        )
    with open(source_path + os.path.sep + rd.KPD_PARA_MSG_SRC_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

    header_template =  \
'''{0}
#ifndef KEYPAD_MESSAG_H
#define KEYPAD_MESSAG_H
    
#include "KpdPara_StructUnit.H"
    
enum{{  //MSG들의 Index 값
\t\t {1}
}};
\n
{2}
\n\n
S_MSG_TYPE KpdParaGetMsgData(WORD wMsgIdx, WORD wMsgNum);
WORD KpdParaGetMsgSize(WORD wMsgIdx);
#endif  //KEYPAD_MESSAG_H

'''
    # 한라인 추가 되므로  msg_total 
    msg_data_enum_lines.append('MSG_{0:<36}//{1:0>3}'.format('TOTAL', msg_enum_count))
    msg_define_lines = []
    for msg_name, msg_name_count in msg_name_count_list:
        msg_define_lines.append('#define MSG_COUNT_{0:<30}{1}'.format(msg_name.upper(), msg_name_count))

    file_contents = header_template.format(  
        banner,
        '\n\t\t,'.join(msg_data_enum_lines),
        '\n'.join(msg_define_lines) 
        )
    with open(source_path + os.path.sep + rd.KPD_PARA_MSG_HEADER_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

def make_kpdpara_table(source_path, parameters_model, group_model):
    col_info = ci.para_col_info_for_view()
    model = parameters_model
    key_col_info = ci.group_col_info()
    key_model = group_model  

    key_row = key_model.rowCount()

    # 소스용 variable template
    para_vars = [] 
    para_vars_lines = []
    para_vars_template = \
'''static const S_TABLE_X_TYPE t_ast{0}grp[GRP_{1}_CODE_TOTAL] = {{
{2}
}};
'''
    # 소스내 group info 용 template 
    group_info_lines  = []
    group_info_template ='{{T_{0:<10},{1:<20},{2:<25},{3:<10}}}'

    table_addr_lines = [] 
    table_addr_template = \
'''\tcase GROUP_{0}:
\t\tpstTable = &t_ast{0}grp[wTableIdx];
\t\tbreak;
'''

    # 헤더용 define template
    defines_lines = []
    defines_template = '#define GRP_{0}_CODE_TOTAL\t{1}'

    # group index 용 
    group_index_lines = []

    # key model 에서 key 값을 추출하여 key_value 모델에서 find 함 
    for row_index in range(key_row):
        # 그룹 정보 추출 
        key_group_name = key_model.item(row_index, key_col_info.index('Group')).text() 
        key_group_hidden_var = key_model.item(row_index, key_col_info.index('Hidden Var')).text()
        key_group_hidden_val = key_model.item(row_index, key_col_info.index('Hidden Val')).text()
        if( 'g_' in key_group_hidden_var or 'k_' in key_group_hidden_val ):
            key_group_hidden_var = '(WORD*)&' + key_group_hidden_var

        group_info_lines.append( 
            group_info_template.format(
                key_group_name.upper(), 'GRP_' + key_group_name.upper() + '_CODE_TOTAL', 
                key_group_hidden_var, key_group_hidden_val
            )
        )

        table_addr_lines.append( 
            table_addr_template.format(
                key_group_name.upper()
            )
        )

        # 해당 하는 그룹의 아이템 정보를 얻음 
        find_items = model.findItems(key_group_name, column = col_info.index('Group'))
        per_group_item_count = len(find_items)

        defines_lines.append( 
            defines_template.format(
                key_group_name.upper(),
                per_group_item_count
            )
        )

        group_index_lines.append( 
            'GROUP_{0}'.format( key_group_name.upper() )
        )

        for find_item in find_items:
            find_row_index = find_item.row()

            group_name = model.item(find_row_index, col_info.index('Group')).text()
            code_num = model.item(find_row_index, col_info.index('Code#')).text()
            title_name = model.item(find_row_index, col_info.index('Code TITLE')).text()
            title_enum_name =  model.item(find_row_index, col_info.index('Title Index')).text()
            
            at_value = model.item(find_row_index, col_info.index('AtValue')).text()
            title_name = make_title_with_at_value(title_name, at_value) # at value 적용 
            para_var= model.item(find_row_index, col_info.index('Para Index')).text()
            para_var = 'E_DATA_CMD_' + para_var
            para_word_scale = model.item(find_row_index, col_info.index('KpdWordScale')).text()
            para_float_scale = model.item(find_row_index, col_info.index('KpdFloatScale')).text()
            kpd_func = model.item(find_row_index, col_info.index('KPD 함수')).text()
            default_val =  model.item(find_row_index, col_info.index('공장설정값')).text()
            max_val = model.item(find_row_index, col_info.index('최대값')).text()
            min_val = model.item(find_row_index, col_info.index('최소값')).text()
            show_var  =  model.item(find_row_index, col_info.index('보임변수')).text()

            # max, min show var 의 key_pad index 인 경우 처리 
            re_val = re.compile('[A-Z][A-Z_0-9]+')
            if( re_val.search(max_val) ):
                max_val = 'E_DATA_CMD_' + max_val
            if( re_val.search(min_val) ):
                max_val = 'E_DATA_CMD_' + max_val
            if( re_val.search(show_var) ):
                max_val = 'E_DATA_CMD_' + max_val

            form_msg = model.item(find_row_index, col_info.index('폼메시지')).text()
            unit = model.item(find_row_index, col_info.index('단위')).text()

            hidden_condition =  model.item(find_row_index, col_info.index('Hidden Con')).text()
            kpd_type = model.item(find_row_index, col_info.index('KPD 타입')).text()
            no_comm = model.item(find_row_index, col_info.index('통신쓰기금지')).text()
            read_only = model.item(find_row_index, col_info.index('읽기전용')).text()
            no_change_on_run =  model.item(find_row_index, col_info.index('운전중변경불가')).text()
            zero_input = model.item(find_row_index, col_info.index('0 입력가능')).text()
            '''
            no_comm, read_only, no_change_on_run, zero_input = False, False, False, False
            if( attribute & ATTR_NO_COMM ):
                no_comm = True 
            if( attribute & ATTR_READ_ONLY ):
                read_only = True
            if( attribute & ATTR_NO_CHANGE_ON_RUN ):
                no_change_on_run = True 
            if( attribute & ATTR_ZERO_INPUT ):
                zero_input = True 
            '''
            attribute = 0x0000
            if( no_comm == 'True'):
                attribute |= ATTR_NO_COMM
            if( read_only == 'True'):
                attribute |= ATTR_READ_ONLY
            if( no_change_on_run == 'True'):
                attribute |= ATTR_NO_CHANGE_ON_RUN
            if( zero_input == 'True'):
                attribute |= ATTR_ZERO_INPUT
            if( 'k_' in max_val ):
                attribute |= ATTR_UP
            if( 'k_' in min_val ):
                attribute |= ATTR_LP
            if( kpd_type == 'AfterEnter' ):
                attribute |= ATTR_ENT
            hidden_val = hiddenConditionToValue(hidden_condition)
            attribute |= (hidden_val << 8)

            show_value = model.item(find_row_index, col_info.index('보임값')).text()
            eep_addr = model.item(find_row_index, col_info.index('EEP 주소')).text()
            comm_addr = model.item(find_row_index, col_info.index('통신주소')).text()
            max_eds = model.item(find_row_index, col_info.index('최대 EDS')).text()
            min_eds = model.item(find_row_index, col_info.index('최소 EDS')).text()
            comment = model.item(find_row_index, col_info.index('설명')).text()

            default_val ='(WORD)' + default_val
            if( 'k_' in max_val ) :
                max_val = '(LONG)&' + max_val
            else:
                max_val = '(WORD)' + max_val

            if( 'k_' in min_val ) :
                min_val = '(LONG)&' + min_val
            else:
                min_val = '(WORD)' + min_val
                
            if( 'DATAMSG' in unit ):
                form_msg = 'MSG_' + form_msg
            
            eds_val = ''
            if( max_eds or min_eds):
                eds_val ='[EDS :{0},{1}]'.format(max_eds, min_eds)

            attribute_str = '0x{0:0>4}'.format(hex(attribute)[2:].upper())

            if( 'k_' in show_var or 'g_' in show_var ):
                show_var = '(WORD*)&' + show_var

            format_str = ( '{{{0:<5},{1:<5},{2:<30},{3:<40},{4:<20},'
                            '{5:<20},{6:<40},{7:<30},{8:<30},{9:<30},'
                            '{10:<30},{11:<30},{12:<10},{13:<30},{14:<5}}},'
                            '//"{15:<14}"{16}//{17}' )
            if( find_item == find_items[-1]):
                format_str = ( '{{{0:<5},{1:<5},{2:<30},{3:<40},{4:<20},'
                                    '{5:<20},{6:<40},{7:<30},{8:<30},{9:<30},'
                                    '{10:<30},{11:<30},{12:<10},{13:<30},{14:<5}}}'
                                    '//"{15:<14}"{16}//{17}' )
            para_vars_lines.append(
                format_str.format(\
                        code_num,              at_value, title_enum_name,  para_var, para_word_scale, 
                        para_float_scale,      kpd_func, default_val,      max_val,  min_val,
                        form_msg,              unit,     attribute_str,    show_var, show_value, 
                        title_name,            eds_val,  comment\
                )
            )
        
        para_vars.append(
            para_vars_template.format(group_name,
                                        group_name,
                                    '\n'.join(para_vars_lines))
        )
        para_vars_lines.clear()


    source_template = \
'''// PRQA S 502, 4130, 4131, 750, 759, 1514, 3218, 1504, 1505, 1503, 2860, 2895 EOF

{0}
#include "BaseDefine.H"
#include "KPD_Title_Enum.H"
#include "KpdPara_GrpIdx.H"
#include "KpdPara_Msg.H"
#include "KpdPara_ShowParaVari.H"
#include "KFunc_Head.H"
#include "KpdPara_Table.H"
#include "DrvPara_DataStorage.h"
{1}
\n\n
static const S_GROUP_X_TYPE t_astGrpInfo[GROUP_TOTAL] = {{ 
{2}
}};\n\n
const S_GROUP_X_TYPE* KpdParaTableGetGrpAddr(WORD wGrpIdx)
{{
return &t_astGrpInfo[wGrpIdx];
}}

const S_TABLE_X_TYPE* KpdParaTableGetTableAddr(WORD wGrpIdx, WORD wTableIdx)
{{
const S_TABLE_X_TYPE* pstTable;

switch(wGrpIdx)
{{
{3}
default:
    pstTable = NULL;
    break;
}}
return pstTable;
}}
'''
    file_contents = source_template.format( 
        banner,
        '\n'.join(para_vars),
        ',\n'.join(group_info_lines),
        ''.join(table_addr_lines)

    )
    with open(source_path + os.path.sep + rd.KPD_PARA_TABLE_SRC_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass


    header_template = \
'''{0}
#ifndef _KPD_TABLE_H
#define _KPD_TABLE_H
#include "KpdPara_StructUnit.H"
\n\n
{1}\n\n
const S_GROUP_X_TYPE* KpdParaTableGetGrpAddr(WORD wGrpIdx);
const S_TABLE_X_TYPE* KpdParaTableGetTableAddr(WORD wGrpIdx, WORD wTableIdx);
\n\n
#endif   //_KPD_TABLE_H
'''
    file_contents = header_template.format(
        banner,
        '\n'.join(defines_lines)
    )
    with open(source_path + os.path.sep + rd.KPD_PARA_TABLE_HEADER_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass


    group_index_template = \
'''{0}
#ifndef KPDPARA_GRP_INDEX_H
#define KPDPARA_GRP_INDEX_H
\n
enum eGrpIndex{{
\t {1}
\t,GROUP_TOTAL
}};
\n
#endif   //KPDPARA_GRP_INDEX_H
'''

    file_contents = group_index_template.format(
        banner,
        '\n\t,'.join(group_index_lines)
    )
    with open(source_path + os.path.sep + rd.KPD_GRP_INDEX_HEADER_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

def make_kfunc_head(source_path, parameters_model, group_model):
    col_info = ci.para_col_info_for_view()
    model = parameters_model
    key_col_info = ci.group_col_info()
    key_model = group_model

    key_row = key_model.rowCount()

    cmd_key_func_lines = []
    after_enter_key_func_lines = []

    # key model 에서 key 값을 추출하여 key_value 모델에서 find 함 
    key_func_list = [] # 중복 제거를 위해 사용 
    for row_index in range(key_row):
        # 그룹 정보 추출 
        key_group_name = key_model.item(row_index, key_col_info.index('Group')).text() 

        # 해당 하는 그룹의 아이템 정보를 얻음 
        find_items = model.findItems(key_group_name, column = col_info.index('Group'))

        for find_item in find_items:
            find_row_index = find_item.row()

            key_func = model.item(find_row_index, col_info.index('KPD 함수')).text()
            code_num = model.item(find_row_index, col_info.index('Code#')).text()
            kpd_type = model.item(find_row_index, col_info.index('KPD 타입')).text()

            if('NULL' not in key_func):
                if( key_func not in key_func_list ):
                    key_func_list.append(key_func)
                    arg = '{0:<40}//({1},{2:>2})'.format(key_func, key_group_name, code_num)
                    if(kpd_type == 'AfterEnter'):
                        after_enter_key_func_lines.append(arg)
                    else:
                        cmd_key_func_lines.append(arg)

    header_template = \
'''{0}
#ifndef KFUNC_INDEX_H
#define KFUNC_INDEX_H
\n
enum eKpdFuncIndex{{
     KFUNC_NULL
\t,{1}
\t,KFUNC_START_AFTER_ENT_FUNC = 1000
\t,{2}

}};
\n
#define TOTAL_KFUNC_CMD_ENT                  {3} 
#define TOTAL_KFUNC_AFTER_ENT                {4} 
\n
#endif   //KFUNC_INDEX_H
'''

    file_contents = header_template.format(
        banner, 
        '\n\t,'.join(cmd_key_func_lines),
        '\n\t,'.join(after_enter_key_func_lines),
        len(cmd_key_func_lines),
        len(after_enter_key_func_lines)
    )
    with open(source_path + os.path.sep + rd.KPD_FUNC_HEAD_HEADER_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

def make_drv_para_data_storage(source_path, parameters_model):
    col_info = ci.para_col_info_for_view()
    model = parameters_model
    para_index = col_info.index('Para Index') 
    para_word_scale_index = col_info.index('KpdWordScale')
    para_float_scale_index = col_info.index('KpdFloatScale')
    para_title_index = col_info.index('Code TITLE')
    para_group_index = col_info.index('Group')
    para_code_index = col_info.index('Code#')

    para_indexes = [] # duplication 제거를 위한 para_index 저장 
    para_indexes_lines  = [] # generation 을 위한 line 
    para_scale_info = [] # [float, word , comment ]

    for index in range(model.rowCount() ):

        float_scale = model.item(index, para_float_scale_index).text()
        word_scale  = model.item(index, para_word_scale_index).text()
        group = model.item(index, para_group_index).text()
        code = model.item(index, para_code_index).text()
        title = model.item(index, para_title_index ).text()
        comment = '\t//{0:>5} {1:>4} {2:>20}'.format(group, code, title)
        para_index_str = model.item(index, para_index).text()

        if( para_index_str not in para_indexes ):
            #duplication 제거 
            para_indexes.append(para_index_str) 
            para_index_str_line = 'E_DATA_CMD_{0:<30}{1}'.format(para_index_str, comment)
            para_indexes_lines.append(para_index_str_line)
            para_scale_info.append('{{{0:>20}, {1:>20}}}{2}'.format(float_scale, word_scale, comment) )
        else:
            # 중복 발생시 comment 추가 
            duplication_index = para_indexes.index(para_index_str)
            para_indexes_lines[duplication_index] = '{0}\t{1}'.format(para_indexes_lines[duplication_index] , comment)
            para_scale_info[duplication_index] = '{0}\t{1}'.format(para_scale_info[duplication_index] , comment)

    header_template = \
'''{0}
#ifndef DRIVE_PARA_DATA_STORAGE_AUTO_H_
#define DRIVE_PARA_DATA_STORAGE_AUTO_H_

typedef enum eDrvParaDataDiv
{{
	E_DATA_DIV_1,
	E_DATA_DIV_10,
	E_DATA_DIV_100,
	E_DATA_DIV_1K,
	E_DATA_DIV_10K,
	E_DATA_DIV_100K,

	TOTAL_DATA_DIV

}}E_DRV_PARA_DATA_DIV;

typedef enum eDrvParaSetErr
{{
	E_DRV_PARA_ERR_NONE,
	E_DRV_PARA_WRONG_INDEX,
	E_DRV_PARA_RANGE_OVER,
	E_DRV_PARA_TRANS_LIMITED
}}E_DRV_PARA_SET_ERR;

typedef enum eDrvParaDataVariIdx	//Drive Parameter Variable Index Enumeration 0 ~ 9999사이에는 Floating Point Type의 변수, Fixed Point Type의 변수
{{
\t {1}
\t,E_DATA_VARI_END
}}E_DRV_PARA_DATA_VARI_IDX;

typedef enum eDrvParaMsgVariIdx	   //Drive Parameter Message Variable Index Enumeration
{{
\t {2}
\t,E_MSG_VARI_END

}}E_DRV_PARA_MSG_VARI_IDX;

#endif 
'''

    file_contents = header_template.format(
        banner,
        '\n\t,'.join(para_indexes_lines),
        '\n\t,'.join('TES')
    )
    with open(source_path + os.path.sep + rd.DRVPARA_DATASTORAGE_HEADER_AUTO, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass



    src_template = \
'''{0}
#include "BaseDefine.H"
#include "DrvPara_DataStorage_Auto.h"

typedef struct sDrvParaDataScaleType	//소수점 표현하는 Data
{{
	E_DRV_PARA_DATA_DIV eFloatScale;		//Floating 변수로 전환할때의 소수점 자리값
	E_DRV_PARA_DATA_DIV eWordScale;			//WORD Type으로 Data를 변화할때 잘라낼 자리값
}}S_DRV_PARA_DATA_SCALE;

static const S_DRV_PARA_DATA_SCALE t_astDrvParaDataScale[E_DATA_VARI_END] =	
{{
\t {1}
}};
'''
    file_contents = src_template.format(
        banner,
        '\n\t,'.join(para_scale_info)
    )
    with open(source_path + os.path.sep + rd.DRVPARA_DATASTORAGE_SRC_AUTO, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass
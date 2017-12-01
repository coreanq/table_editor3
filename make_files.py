import os, sys, re, datetime
import column_info as ci

import read_data as rd
import version

ATTR_BYTE = 0x0001  # byte 단위 현재 사용 안함 
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
//      Auto generated from TABLE EDITOR {0} Ver:{1}    {2}
//      Do not modify this source file
//------------------------------------------------------------------------------
'''.format(
    version.TABLE_EDITOR_NUMBER, 
    version.VERSION_INFO,
    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

PARA_START_ADDR	        =    0x1000
GRP_OFFSET_MUL		    =    0x100


def makeCodeAddr(grp, code):
    return PARA_START_ADDR + ((grp * GRP_OFFSET_MUL) + code)


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

def make_kpd_title(source_path, title_model):
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
        title_index = row_items[col_info.index('TitleIndex')]
        data = row_items[col_info.index('Data')]

        if( title_index == ''):
            title_index_num = 0
        else:
            title_index_num = int(title_index)

        comma = ','
        if( row_index == row ):
            comma = ' '
    
        # enum_list 생성용  for kpd_title_enum.h
        if( title_index_num == 1000):
            enum_list.append('T_TotalDefaultTitleSize,')
            enum_list.append('{0:<32} = START_ADD_TITLE_INDEX, //{1}'.format(enum_name, title_index))
        else:
            enum_list.append('{0:<32}{1}//{2}'.format(enum_name, comma,  title_index))

        if( title_index_num < 1000):
            continue

        total_add_title = total_add_title + 1   
        # hex data 4개씩 짜름 
        re_split = re.compile(r'[a-z0-9A-Z]{4,4}')
        find_list = re_split.findall(data)
        add_title_size = len(find_list)
        find_merge = ','.join('0x'+item for item in find_list )
        comma = ','
        if( row_index == row - 1 ):
            comma = ' '
        rows.append('\t{{{0}}}{1}\t//{2:<5}"{3:<20}"{4}'.format(
                find_merge, 
                comma, 
                title_index, 
                title, 
                enum_name
            )
        )
    # print('\n'.join(rows))

    
    src_template= \
'''{0}
#include "BaseDefine.H"
#include "AddTitle_Eng.H"\n\n\n
const uint16_t g_awAddTitleEng[TOTAL_ADD_TITLE][ADD_TITLE_SIZE] = {{ 
{1}
}};
'''
    file_contents = src_template.format(
        banner, 
        '\t\n'.join(rows)
        )

    with open(source_path + os.path.sep + rd.KPD_ADD_TITLE_SRC_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

    header_template= \
'''{0}
#ifndef ADD_TITLE_ENG_H_
#define ADD_TITLE_ENG_H_\n

#if defined(__cplusplus)
extern "C" {{
#endif

#define TOTAL_ADD_TITLE       {1} 
#define ADD_TITLE_SIZE        {2} 
extern const uint16_t g_awAddTitleEng[TOTAL_ADD_TITLE][ADD_TITLE_SIZE];\n

#if defined(__cplusplus)
}}
#endif

#endif   //ADD_TITLE_ENG_H_
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
#ifndef KPD_TITLE_ENUM_H_
#define KPD_TITLE_ENUM_H_

#if defined(__cplusplus)
extern "C" {{
#endif

#define START_ADD_TITLE_INDEX 1000

enum{{ 
\t{1}
}};
{2}

#if defined(__cplusplus)
}}
#endif

#endif
'''
    enum_list.append('T_TotalAddTitleSize')
    if( total_add_title ):
        have_add_title = '#define HAVE_ADD_TITLE	//Add Title이 존재할때만 Define 된다.'
    else:
        have_add_title = ''

    file_contents = kpd_title_enum_header_template.format(
        banner, 
        '\n\t'.join(enum_list), 
        have_add_title
        )
    with open(source_path + os.path.sep + rd.KPD_ENUM_TITLE_HEADER_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass


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
\t{3}
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
            enum_name = model.item(find_row_index, col_info.index('TitleIndex')).text()
            title_name = make_title_with_at_value(title_name, at_value)
            title_name = '{:<15}'.format(title_name)
            comma = ','

            if( find_items[-1] == find_item ):
                comma = ' ' 
            lines.append('{{{0:<20},{1:<5}}}{2}           //"{3}"'.format(
                enum_name, 
                at_value, 
                comma, 
                title_name)
                )
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
                '\n\t'.join(lines))
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
static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], uint16_t wMsgNum);
\n\n
{1}\n
static const S_MSG_TYPE * t_pastMsgDataTbl[MSG_TOTAL] = {{
\t{2}
}};
static const uint16_t t_awMsgDataSize[MSG_TOTAL] = {{
\t{3}
}};\n
static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], uint16_t wMsgNum)
{{
return astMsgType[wMsgNum];
}}
S_MSG_TYPE KpdParaGetMsgData(uint16_t wMsgIdx, uint16_t wMsgNum)
{{
return KpdParaGetMsg(t_pastMsgDataTbl[wMsgIdx], wMsgNum);
}}
uint16_t KpdParaGetMsgSize(uint16_t wMsgIdx)
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
        msg_data_enum_lines.append('MSG_{0:<30},//{1:0>3}'.format(msg_name, msg_enum_count))
        msg_enum_count = msg_enum_count + 1

    # 한라인 추가 되므로  msg_total 
    msg_data_enum_lines.append('MSG_{0:<30} //{1:0>3}'.format('TOTAL', msg_enum_count))

    file_contents = source_template.format(  
        banner,
        '\n'.join(msg_vars),
        ',\n\t'.join(msg_data_tbl_lines),
        ',\n\t'.join(msg_data_size_lines) 
        )
    with open(source_path + os.path.sep + rd.KPD_PARA_MSG_SRC_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

    header_template =  \
'''{0}
#ifndef KEYPAD_MESSAGE_H_
#define KEYPAD_MESSAGE_H_

#if defined(__cplusplus)
extern "C" {{
#endif
    
#include "KpdPara_StructUnit.H"
    
enum{{  //MSG들의 Index 값
\t{1}
}};
\n
{2}
\n\n
S_MSG_TYPE KpdParaGetMsgData(uint16_t wMsgIdx, uint16_t wMsgNum);
uint16_t KpdParaGetMsgSize(uint16_t wMsgIdx);

#if defined(__cplusplus)
}}
#endif

#endif  //KEYPAD_MESSAGE_H_

'''
    msg_define_lines = []
    for msg_name, msg_name_count in msg_name_count_list:
        msg_define_lines.append('#define MSG_COUNT_{0:<30}{1}'.format(msg_name.upper(), msg_name_count))

    file_contents = header_template.format(  
        banner,
        '\n\t'.join(msg_data_enum_lines),
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

    # table.c 소스내 group info 용 template 
    group_info_lines  = []
    group_info_template ='{{  T_{0:<7},{1:>30}, {2:>30}}}'

    # table.c 소스내 index 를 통해 group table address 접근 하기 위한 소스 파일 
    table_addr_lines = [] 
    table_addr_template = \
'''\tcase GROUP_{0}:
\t\tpstTable = &t_ast{0}grp[wTableIdx];
\t\tbreak;
'''

    group_index_lines = []   # group index 정의용 #define GROUP_MAK ...
    header_name_enum_lines = []   # unique name enum 을 만들기 위함 
    header_grp_size_define_lines = [] # grp total count 정보 용  #define GRP_MAK_CODE_TOTAL 24
    header_grp_size_define_template = '#define GRP_{0}_CODE_TOTAL\t{1}'
    header_grp_start_index_define_lines = []
    header_grp_start_index_define_template = '#define GRP_{0}_START_INDEX\t{1}'

    total_code_count = 0
    # key model(grp info) 에서 group 값을 추출하여 para table 모델에서 find 함 
    for grp_row_index in range(key_row):
        # 그룹 정보 추출 
        key_group_name = key_model.item(grp_row_index, key_col_info.index('Group')).text() 

        group_info_lines.append( 
            group_info_template.format(
                key_group_name.upper(), 
                'GRP_' + key_group_name.upper() + '_START_INDEX',
                'GRP_' + key_group_name.upper() + '_CODE_TOTAL'
            )
        )

        table_addr_lines.append( 
            table_addr_template.format(
                key_group_name.upper()
            )
        )

        ##########################################################################################################
        # group index 정의용 #define GROUP_MAK ...
        group_index_lines.append( 
            'GROUP_{0}'.format( key_group_name.upper() )
        )


        ##########################################################################################################
        # table 헤더의 group count 생성  
        # 해당 하는 그룹의 아이템 정보를 얻음 
        find_items = model.findItems(key_group_name, column = col_info.index('Group'))
        per_group_item_count = len(find_items)
        total_code_count += per_group_item_count

        header_grp_size_define_lines.append( 
            header_grp_size_define_template.format(
                key_group_name.upper(),
                per_group_item_count
            )
        )

        # group info 를 정보를 토대로 해당하는 그룹에 맞는 아이템만 찾아냄 
        for count, find_item in enumerate(find_items):
            find_row_index = find_item.row()

            if( count == 0 ):
                header_grp_start_index_define_lines.append( 
                    header_grp_start_index_define_template.format(
                        key_group_name.upper(), 
                        find_row_index
                    )
                )

            name = model.item(find_row_index, col_info.index('Name')).text()
            group_name = model.item(find_row_index, col_info.index('Group')).text()
            code_num = model.item(find_row_index, col_info.index('Code#')).text()
            grp_and_code = '{0}_{1:>02}'.format( group_name.upper() , code_num )

            title_name = model.item(find_row_index, col_info.index('Title')).text()
            title_enum_name =  model.item(find_row_index, col_info.index('TitleIndex')).text()
            
            at_value = model.item(find_row_index, col_info.index('AtValue')).text()
            title_name = make_title_with_at_value(title_name, at_value) # at value 적용 
            # kpd_vari = model.item(find_row_index, col_info.index('ParaVar')).text()
            # kpd_func_name  = model.item(find_row_index, col_info.index('KpdFunc')).text()

            para_word_scale = model.item(find_row_index, col_info.index('KpdWordScale')).text()
            para_float_scale = model.item(find_row_index, col_info.index('KpdFloatScale')).text()

            data_func_run = model.item(find_row_index, col_info.index('DataFunc실행여부')).text()
            default_val =  model.item(find_row_index, col_info.index('공장설정값')).text()
            max_val = model.item(find_row_index, col_info.index('최대값')).text()
            min_val = model.item(find_row_index, col_info.index('최소값')).text()

            read_only = model.item(find_row_index, col_info.index('읽기전용')).text()
            no_change_on_run = model.item(find_row_index, col_info.index('운전중변경불가')).text()
            zero_input = model.item(find_row_index, col_info.index('0입력가능')).text()
            no_comm = model.item(find_row_index, col_info.index('통신쓰기금지')).text()
 
            form_msg = model.item(find_row_index, col_info.index('폼메시지')).text()
            unit = model.item(find_row_index, col_info.index('단위')).text()

            comm_addr = hex(makeCodeAddr(grp_row_index, int(code_num)))

            # table 헤더의 enum MAK_000 define 생성 title_name 도 추가해서 알아 보기 쉽게 함  
            header_name_enum_lines.append(
                    "#define {0:<30} {1:<10}//{2:<10}{3:<20}{4:>10}".format(
                            name, 
                            comm_addr, 
                            grp_and_code,
                            title_name, 
                            '' 
                            # kpd_vari,
                            # kpd_func_name

                    ) 
                )

            comment = model.item(find_row_index, col_info.index('설명')).text()

            if( 'DATAMSG' in unit ):
                form_msg = 'MSG_' + form_msg
            
            format_str = ( '/* {0:>8} */ {{{1:<30},{2:>20},{3:>5},{4:>6},{5:>8},'
                            '{6:>8},{7:>8},{8:>6},{9:>6},{10:>6},'
                            '{11:>6},{12:>25},{13:>25},{14:>10}}}{15} //"{16:<30}"'
                            '//{17}' )

            if( find_item == find_items[-1] ):
                comment = comment + '\n\n'

            para_vars_lines.append(
                format_str.format(\
                        grp_and_code,       name,               title_enum_name,    at_value,           data_func_run,      default_val,        
                        max_val,            min_val,            read_only,          no_change_on_run,   zero_input,
                        no_comm,            form_msg,           unit,               comm_addr,          ',',                title_name,         
                        comment
                )
            )
        
        para_vars.append(
            '\n'.join(para_vars_lines)
        )
        para_vars_lines.clear()


    source_template = \
'''// PRQA S 502, 4130, 4131, 750, 759, 1514, 3218, 1504, 1505, 1503, 2860, 2895 EOF

{0}
#include "BaseDefine.H"
#include "KpdPara_Table.H"
#include "KPD_Title_Enum.H"
#include "KpdPara_Msg.H"
#include "DrvPara_DataStorage.H"

static const S_TABLE_X_TYPE t_astAllGrp[ALL_GRP_CODE_TOTAL] = {{
{1}
}};
\n\n
static const S_GROUP_X_TYPE t_astGrpInfo[GROUP_TOTAL] = {{ 
{2}
}};\n\n

const S_GROUP_X_TYPE* KpdParaTableGetGrpAddr(uint8_t bGrpIdx)
{{
    return &t_astGrpInfo[bGrpIdx];
}}

static bool KpdParaAddrBinarySearch(uint16_t wInputAddr, uint16_t* pwIndex)
{{
	uint16_t wMidIndex = 0;
	uint16_t wLeftIndex = 0;
	uint16_t wRightIndex = 0;
    uint16_t wSrcAddr = 0;
	bool blSearchData = false;
	
	wRightIndex = ( sizeof(t_astAllGrp) / sizeof(t_astAllGrp[0]) ) - 1;
	
	while( wLeftIndex <= wRightIndex )
	{{
		wMidIndex = wLeftIndex + (wRightIndex - wLeftIndex)/2 ;
		wSrcAddr = t_astAllGrp[wMidIndex].wCommAddr;
		// 찾으려는 값이 중앙값보다 작으면  right index 를 mid - 1로 둔다. 
		if( wSrcAddr > wInputAddr )
			wRightIndex = wMidIndex - 1;
		// 찾으려는 값이 중앙값보다 크면  left index 를 mid + 1 로 둔다. 
		else if( wSrcAddr < wInputAddr ) 
			wLeftIndex = wMidIndex + 1;
		// 찾은 경우 값 대입 후  return
		else
		{{
			blSearchData = true;
			*pwIndex = wMidIndex;
			break;
		}}
	}}
	return blSearchData;
}}

const S_TABLE_X_TYPE* KpdParaTableGetTableAddrFromGrpAndCode(uint8_t bGrp, uint8_t bCodeNum, int16_t iOffset)
{{
	const S_TABLE_X_TYPE* pstTable = NULL;
    uint16_t wCommAddr = KpdParaTableGetTableAddr(bGrp, bCodeNum);
	pstTable = KpdParaTableGetTableAddrFromCommAddr(wCommAddr, iOffset);
	return pstTable;
}}
const S_TABLE_X_TYPE* KpdParaTableGetTableAddrFromCommAddr(uint16_t wCommAddr, int16_t iOffset)
{{
	uint8_t bGrp = KpdParaUtilGetGrp(wCommAddr);
    const S_TABLE_X_TYPE* pstTable = NULL;
    
	if( bGrp < GROUP_TOTAL )
	{{
        uint16_t wSearchedIndex = 0;
		uint16_t wGrpSize = t_astGrpInfo[bGrp].bGrpSize;
		uint16_t wStartIndex = t_astGrpInfo[bGrp].wStartIndex;
		if( KpdParaAddrBinarySearch( wCommAddr, &wSearchedIndex)  == true )
		{{
			uint32_t ulOffsetIndex = ((int32_t)(wSearchedIndex - wStartIndex + iOffset)) % wGrpSize;
			uint32_t ulFindedIndex = wStartIndex + ulOffsetIndex;
			pstTable = &t_astAllGrp[ulFindedIndex];
		}}
		else
		{{
            MSG_ERR("%08x search Error\\n", wCommAddr);
			pstTable = NULL;
		}}
	}}
	else
	{{
		MSG_ERR("GrpSize overflow\\n");
	}}

	return pstTable;
}}

const S_TABLE_X_TYPE* KpdParaTableGetTableAddrFromCodeIndex(uint8_t bGrp, uint8_t bPosition)
{{
    const S_TABLE_X_TYPE * pstTable = NULL;
    uint16_t wStartIndex = 0;
    if( bGrp < GROUP_TOTAL ) 
    {{
        if( bPosition < t_astGrpInfo[bGrp].bGrpSize )
        {{
            wStartIndex = t_astGrpInfo[bGrp].wStartIndex;
            pstTable = &t_astAllGrp[wStartIndex + bPosition];
        }}
        else
        {{
			pstTable = NULL;
            MSG_ERR("bPosition %d\\n", bPosition);
        }}
    }}
    else
    {{
		pstTable = NULL;
        MSG_ERR("GrpSize overflow\\n");
    }}
    return pstTable;
}}

// 지정 그룹부터의 bPosition 만큼 배열 index 를 증가한 CommAddr 값을 리턴함 
uint16_t KpdParaTableGetCommAddrFromCodeIndex(uint8_t bGrp, uint8_t bPosition )
{{
	uint16_t wCommAddr = 0;
	uint16_t wStartIndex = 0;
    if( bGrp < GROUP_TOTAL ) 
    {{
        if( bPosition < t_astGrpInfo[bGrp].bGrpSize )
        {{
            wStartIndex = t_astGrpInfo[bGrp].wStartIndex;
            wCommAddr = t_astAllGrp[wStartIndex + bPosition].wCommAddr;
        }}
        else
        {{
			wCommAddr = 0;
            MSG_ERR("bPosition %d\\n", bPosition);
        }}
    }}
    else
    {{
		wCommAddr = 0;
        MSG_ERR("GROUP TOTAL\\n");
    }}
	return wCommAddr;
}}
uint16_t KpdParaTableGetTableAddr(uint8_t bGrp, uint8_t bCode)
{{
	// to pass MISRAC rule: dont use define constant for calculating ( relative: implicitly conversion )
	uint16_t wParaStartAddr = PARA_START_ADDR;
	uint16_t wGrpOffsetMul = GRP_OFFSET_MUL;
	uint16_t wRet = wParaStartAddr + (bGrp  << wGrpOffsetMul) + bCode;
	return wRet;
}}
uint8_t KpdParaUtilGetGrp(uint16_t wCommAddr)
{{
    uint8_t bGrpCode;
    
    bGrpCode = ((((wCommAddr) & 0x0f00) >> 8)  & 0xff);
    return bGrpCode;
}}
uint8_t KpdParaUtilGetCodeId(uint16_t wCommAddr)
{{
    uint8_t bCodeId;
    
    bCodeId = (wCommAddr & 0xff);
    return bCodeId;
}}
'''
    # 맨 마지막 콤마 삭제 
    last_str = para_vars[-1]
    modified_str = last_str.rsplit('},', 1)
    modified_str = '} '.join(modified_str)
    para_vars[-1] = modified_str

    file_contents = source_template.format( 
        banner,
        '\n'.join(para_vars),
        ',\n'.join(group_info_lines)
    )
    with open(source_path + os.path.sep + rd.KPD_PARA_TABLE_SRC_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

    group_index_template = \
'''
\n
enum eGrpIndex{{
\t{0},
\tGROUP_TOTAL
}};
\n
'''
    group_indexes = group_index_template.format(
        ',\n\t'.join(group_index_lines)
    )


    header_template = \
'''{0}
#ifndef KPD_TABLE_H_
#define KPD_TABLE_H_

#if defined(__cplusplus)
extern "C" {{
#endif

#include "KpdPara_StructUnit.H"

#define PARA_START_ADDR	                    (uint16_t)0x1000
#define GRP_OFFSET_MUL			           	8 
\n
uint16_t KpdParaTableGetTableAddr(uint8_t bGrp, uint8_t bCode);
const S_GROUP_X_TYPE* KpdParaTableGetGrpAddr(uint8_t bGrp);
// wCommAddr 을 기준으로 해당 그룹 내에서 offset 위치만큼의 Table Addr 을 리턴함 0 인 경우 input 어드레스의 Table Addr 리턴  
const S_TABLE_X_TYPE* KpdParaTableGetTableAddrFromCommAddr(uint16_t wCommAddr, int16_t iOffset);
const S_TABLE_X_TYPE* KpdParaTableGetTableAddrFromGrpAndCode(uint8_t bGrp, uint8_t bCodeNum, int16_t iOffset);
const S_TABLE_X_TYPE* KpdParaTableGetTableAddrFromCodeIndex(uint8_t bGrp, uint8_t bPosition);
uint16_t KpdParaTableGetCommAddrFromCodeIndex(uint8_t bGrp, uint8_t bPosition );
uint8_t KpdParaUtilGetGrp(uint16_t wCommAddr);
uint8_t KpdParaUtilGetCodeId(uint16_t wCommAddr);
{1}
{2}
\n
{3}
\n
{4}
\n
\n
#if defined(__cplusplus)
}}
#endif
#endif   //KPD_TABLE_H_
'''
    # 하나의 테이블이므로 전체 크기를 define 으로 추가함 
    header_grp_size_define_lines.append('#define ALL_GRP_CODE_TOTAL\t{0}'.format(total_code_count))
    file_contents = header_template.format(
        banner,
        group_indexes, 
        '\n'.join(header_grp_size_define_lines),
        '\n'.join(header_grp_start_index_define_lines),
        '\n'.join(header_name_enum_lines)
    )
    with open(source_path + os.path.sep + rd.KPD_PARA_TABLE_HEADER_FILE, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

def make_drv_para_data_storage(source_path, parameters_model):
    col_info = ci.para_col_info_for_view()
    model = parameters_model
    para_word_scale_index = col_info.index('KpdWordScale')
    para_float_scale_index = col_info.index('KpdFloatScale')
    para_name_index = col_info.index('Name')

    scale_line_template = '{{ {0:<30}, {1:>20}, {2:>20} }}'
    scale_lines = []
    data_lines = []

    for index in range(model.rowCount() ):
        float_scale = model.item(index, para_float_scale_index).text()
        word_scale  = model.item(index, para_word_scale_index).text()
        grp_code = model.item(index, para_name_index).text()
        scale_lines.append(
            scale_line_template.format( 
                grp_code, 
                float_scale, 
                word_scale
            )
        )

    for index in range(model.rowCount() ):
        grp_code = model.item(index, para_name_index).text()
        data_lines.append(
               '{{ {0:<30}, 0 }}'.format(
                grp_code 
            )
        )

    src_template = \
'''{0}
#include "BaseDefine.h"
#include "DrvPara_DataStorage.h"
#include "KpdPara_Table.h"

static const int32_t t_alDrvParaDivSlongData[TOTAL_DATA_DIV] =	//int32_t Type의 Scale Data
{{
	1,			//E_DATA_DIV_1
	10,			//E_DATA_DIV_10
	100,		//E_DATA_DIV_100
	1000,		//E_DATA_DIV_1K
	10000,		//E_DATA_DIV_10K
	100000		//E_DATA_DIV_100K
}};

static const float t_afDrvParaDivFloatData[TOTAL_DATA_DIV] =	//float Type의 Scale Data
{{
	1.0,			//E_DATA_DIV_1
	10.0,			//E_DATA_DIV_10
	100.0,			//E_DATA_DIV_100
	1000.0,			//E_DATA_DIV_1K
	10000.0,		//E_DATA_DIV_10K
	100000.0		//E_DATA_DIV_100K
}};

//Drive Parameter Data값이 저장되어 있는 변수
static S_DRV_PARA_DATA t_astDrvParaData[ALL_GRP_CODE_TOTAL] = 
{{
\t{1}
}};

//Drive Parameter Scale 값이 저장되어 있는 변수 
static const S_DRV_PARA_SCALE t_astDrvParaScale[ALL_GRP_CODE_TOTAL] = 
{{
\t{2}
}};
'''
    file_contents = src_template.format(
        banner,
        ',\n\t'.join(data_lines),
        ',\n\t'.join(scale_lines)
    )
    with open(source_path + os.path.sep + rd.DRVPARA_DATASTORAGE_SRC_AUTO, 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass



def make_drv_para_data_from_array(source_path, parameters_model):
    col_info = ci.para_col_info_for_view()
    model = parameters_model
    para_name_index = col_info.index('Name')

    define_size_list = []
    read_case_list = []
    write_case_list = []

    re_grp_and_code_array = re.compile(r'(?P<para_name>[\w]+)_[0-9]{2,2}')

    grp_code_array_dict = {} 
    for index in range(model.rowCount() ):
        grp_code = model.item(index, para_name_index).text()
        match = re_grp_and_code_array.search(grp_code)
        if( match ):
            para_name = match.group('para_name')

            if( para_name not in grp_code_array_dict):
                grp_code_array_dict[para_name] = []
            grp_code_array_dict[para_name].append(grp_code)

    read_para_case_template = '''
    case {}_00: 
    {{
        uint16_t wAddrList[{}_ARRAY_SIZE] = {{
            {}
        }};
        wValue = DriveParaReadData( wAddrList[bPosition], SENDER_SYSTEM );
    }}
    break;
'''

    write_para_case_template = '''
    case {}_00: 
    {{
        uint16_t wAddrList[{}_ARRAY_SIZE] = {{
            {}
        }};
        DriveParaWriteData( wAddrList[bPosition], wData, SENDER_SYSTEM );
    }}
    break;
'''

    for key, array_value in grp_code_array_dict.items():
        define_size_str = '#define {:<40}\t\t{}'.format( key + "_ARRAY_SIZE", len(array_value) )
        define_size_list.append(define_size_str) 

        read_case_list.append (
            read_para_case_template.format( 
                key, key, ',\n\t\t\t'.join(array_value) 
            )
        ) 

        write_case_list.append (
            write_para_case_template.format( 
                key, key, ',\n\t\t\t'.join(array_value) 
            )
        ) 

    

    para_template = '''
{}


uint16_t DriveParaReadFromArrayData(uint16_t wStartIndex, uint8_t bPosition)
{{
    uint16_t wValue = 0;
    switch(wStartIndex)
    {{
    {}
    default:
        wValue = 0;
        MSG_ERR("wStartIndex\\n");
    break;
    }}
    return wValue;
}}

void DriveParaWriteToArrayData(uint16_t wStartIndex, uint8_t bPosition, uint16_t wData)
{{
    switch(wStartIndex)
    {{
    {}
    default:
        MSG_ERR("wStartIndex\\n");
    break;
    }}
}}
'''
    file_contents = para_template.format(
        '\n'.join(define_size_list),
        '\t\t'.join(read_case_list),
        '\t\t'.join(write_case_list)
    )

    with open(source_path + os.path.sep + "DrivePara_IO_expand.c", 'w', encoding='utf8') as f:
        f.write(file_contents)
    pass

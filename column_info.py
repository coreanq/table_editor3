import os
import sys
from PyQt5.QtCore import QStringListModel
# file 을 읽고 파싱 후  올라오는 column 정보 
_parameters_file_columns_info_old = [ 
    'Group', # key column
    'Code#' , 
    'AtValue',
    'TitleIndex', 
    'ParaVar', 
    'KpdFunc',
    '공장설정값',
    '최대값', 
    '최소값', 
    '폼메시지',
    '단위', 
    'Attribute', 
    'ShowVar',
    'ShowVal',
    'MaxEDS', 
    'MinEDS',
    '설명' 
]
# version 4 이상 file 을 파싱후 올라오는 column  정보 
_parameters_file_columns_info = [
    'Group', # key column  단순 all 값만 옴 
    'GrpAndCode', 
    'AtValue',
    'TitleIndex',
    'DataFunc실행여부', 
    '공장설정값',
    '최대값', 
    '최소값', 
    '읽기전용',
    '운전중변경불가', 
    '0입력가능', 
    '통신쓰기금지', 
    '폼메시지', 
    '단위', 
    '설명'
]
# table view 에서 보여지는 column 의 정보 
_parameters_view_columns_info = [
    'Group', # 숨김 컬럼 key column 왼쪽 컬럼 클릭시 사용하기 위한 용도 
    'GrpAndCode', 
    'TitleIndex', # 숨김 컬럼 
    'CodeTITLE',
    'AtValue',
    'ParaVar', # 사용안함 이전 버전 상위버전 변환시 필요함 
    'KpdFunc', # 사용안함 이전 버전 상위버전 변환시 필요함 
    'KpdFloatScale',  
    'KpdWordScale',   
    'DataFunc실행여부', 
    '공장설정값',
    '최대값', 
    '최소값', 
    '읽기전용',
    '운전중변경불가', 
    '0입력가능', 
    '통신쓰기금지', 
    '폼메시지', 
    '단위', 
    '최대 EDS', # 사용안함 이전 버전 상위버전 변환시 필요함 
    '최소 EDS', # 사용안함 이전 버전 상위버전 변환시 필요함 
    '설명'
]
# table editor version 4
_group_columns_info = [
    'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 사용함수가 공용이므로 dummy 만듬
    'Group'
    # 'GroupSize'
]
# table editor version 2, 3
_group_columns_info_old = [
    'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 사용함수가 공용이므로 dummy 만듬
    'Group', 
    '보임값', 
    '보임비교값'
]

# read_data 시 yield 되는 tuple 의 index 정보를 나타냄  
_title_columns_info = [
   'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 사용함수가 공용이므로 dummy 만듬
   'Title',
   'Enum 이름',
   'TitleIndex',
   'Data'
]
_variable_columns_info = [
    'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 사용함수가 공용이므로 dummy 만듬
    'Variable',
    'Type',
    'Description'
]
_msg_values_columns_info = [
    'MsgName',
    'MsgComment',
    'TitleIndex',
    'Title', 
    'AtValue' 
]
_msg_info_columns_info = [
    'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 사용함수가 공용이므로 dummy 만듬
    'MsgName',
    'MsgComment'
]


# unit 에 따른 msg 리스트 정의 
_unit_with_msg = {
    'U_HZ_RPM': QStringListModel(['F_NOT_TITLE_CHANGE', 'F_TITLE_CHANGE', 'F_NOT_TITLE_CHANGE_SIG', 'F_TITLE_CHANGE_SIG']),
    'U_B':QStringListModel([ 'F_BIT'+ str(cnt) for cnt in range(2, 17) ] ),  
    'Other': QStringListModel([ *['F_DEX' + str(cnt) for cnt in range(0, 5)],  
                                *['F_SIG' + str(cnt) for cnt in range(0, 5)],  
                                'F_HEX4', 'F_HEX8', 'F_TIME_MIN', 'F_TWO',   
                                'F_YMDHM', 'F_RYMDHM', 'F_VER'] )
}


def para_col_info_for_file_old():
    return _parameters_file_columns_info_old

def para_col_info_for_file():
    return _parameters_file_columns_info

def para_col_info_for_view():
    return _parameters_view_columns_info
    
def title_col_info():
    return _title_columns_info
    
def variable_col_info():
    return _variable_columns_info

def msg_values_col_info():
    return _msg_values_columns_info 

def msg_info_col_info():
    return _msg_info_columns_info

def group_col_info():
    return _group_columns_info

def group_col_info_old():
    return _group_columns_info_old

def unit_with_msg():
    return _unit_with_msg
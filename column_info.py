import os
import sys
from PyQt5.QtCore import QStringListModel
# file 을 읽고 파싱 후  올라오는 column 정보 
_parameters_file_columns_info = [ 
    'Group',
    'Code#' , 
    'AtValue',
    'TitleIndex', 
    'ParaVar', 
    'KpdFunc',
    'DefaultVal',
    'MaxVal', 
    'MinVal', 
    'Msg',
    'Unit', 
    'Attribute', 
    'ShowVar',
    'ShowVal',
    'MaxEDS', 
    'MinEDS',
    'Comment' 
]
# table view 에서 보여지는 column 의 정보 
_parameters_view_columns_info = [
    'Group', 
    'Code#',
    'Code TITLE',
    'AtValue',
    'Para 변수',
    'KPD 함수',
    '공장설정값',
    '최대값', 
    '최소값', 
    '폼메시지', 
    '단위', 
    'Hidden Con', # 0,1,2,3
    'KPD 타입', # AfterEnter, Cmd
    '통신쓰기금지', 
    '읽기전용', 
    '운전중변경불가', 
    '0 입력가능',
    '보임변수',
    '보임값',
    'EEP 주소',
    '통신주소',
    '최대 EDS',
    '최소 EDS',
    '설명'
]
_group_columns_info = [
    'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 func 가 공용이므로 dummy 만듬
    'Group', 
    'Hidden Var', 
    'Hidden Val'
]

# read_data 시 yield 되는 tuple 의 index 정보를 나타냄  
_title_columns_info = [
   'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 func 가 공용이므로 dummy 만듬
   'Title',
   'Enum 이름',
   'Title Index',
   'Data'
]
_variable_columns_info = [
    'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 func 가 공용이므로 dummy 만듬
    'Variable',
    'Type',
    'Description'
]
_msg_values_columns_info = [
    'MsgName',
    'MsgInfo',
    'Title', 
    'AtValue' 
]
_msg_info_columns_info = [
    'Dummy Key',  # parameter 처럼 filtering 기능을 사용하지 않지만 func 가 공용이므로 dummy 만듬
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

def unit_with_msg():
    return _unit_with_msg
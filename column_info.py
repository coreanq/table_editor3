import os
import sys
# file 을 읽고 파싱 후  올라오는 column 정보 
_parameters_file_columns_info = [ 
    'Group',
    'Code#' , 
    'AtValue',
    'TitleIndex', 
    'ParaVari', 
    'KpdFunc',
    'DefaultVal',
    'MaxVal', 
    'MinVal', 
    'Msg',
    'Unit', 
    'Attribute', 
    'ShowVari',
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
# combobox 등에 사용되기 위해서는 0번째 컬럼이 무조건 keycolumn 이여야함  
_title_columns_info = [
   'Title',
   'Enum 이름',
   'Title Index',
   'Data'
]
_variable_columns_info = [
    'Variable',
    'Type',
    'Description'
]

def para_col_info_for_file():
    return _parameters_file_columns_info
    
def para_col_info_for_view():
    return _parameters_view_columns_info
    
def title_col_info():
    return _title_columns_info
    
def variable_col_info():
    return _variable_columns_info

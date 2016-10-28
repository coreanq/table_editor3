#ifndef _KPD_TABLE_H
#define _KPD_TABLE_H
/***********************************************
//  TABLE EDITOR 3  인버터 Keypad Table
//  Edit시 Table Edit 3 V1.00을 사용하세요      
***********************************************/
#include "KpdPara_StructUnit.H"



#define GRP_MAK_CODE_TOTAL    68
#define GRP_DRV_CODE_TOTAL    23
#define GRP_BAS_CODE_TOTAL    54
#define GRP_ADV_CODE_TOTAL    57
#define GRP_CON_CODE_TOTAL    61
#define GRP_IN_CODE_TOTAL     41
#define GRP_OUT_CODE_TOTAL    32
#define GRP_COM_CODE_TOTAL    23
#define GRP_PID_CODE_TOTAL    68
#define GRP_PRT_CODE_TOTAL    59
#define GRP_ENC_CODE_TOTAL    20
#define GRP_M2_CODE_TOTAL     26


const S_GROUP_X_TYPE* KpdParaTableGetGrpAddr(WORD wGrpIdx);
const S_TABLE_X_TYPE* KpdParaTableGetTableAddr(WORD wGrpIdx, WORD wTableIdx);



#endif   //_KPD_TABLE_H

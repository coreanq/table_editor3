//========================================= 
// TABLE EDITOR 3 : 인버터 Message들 저장   
//========================================= 
#ifndef KEYPAD_MESSAG_H
#define KEYPAD_MESSAG_H
      
#include "KpdPara_StructUnit.H"
      
enum{  //MSG들의 Index 값
	 MSG_YesNO                          //000
	,MSG_TimeScale                      //001
	,MSG_InitGrp                        //002
	,MSG_RunCmdSrc                      //003
	,MSG_FreqRefSrc2                    //004
	,MSG_TorqueSrc                      //005
	,MSG_FreqRefSrc1                    //006
	,MSG_XcelCurve                      //007
	,MSG_StartMode                      //008
	,MSG_XcelFreqMode                   //009
	,MSG_BoostMode                      //010
	,MSG_VfMode                         //011
	,MSG_Int485BRate                    //012
	,MSG_MotCooling                     //013
	,MSG_InvCap                         //014
	,MSG_CtrlMode                       //015
	,MSG_AoMode                         //016
	,MSG_DiMode                         //017
	,MSG_DoMode                         //018
	,MSG_MotCap                         //019
	,MSG_DnOutInst                      //020
	,MSG_DnInInst                       //021
	,MSG_RunPrevent                     //022
	,MSG_LostAiChkLvl                   //023
	,MSG_modbusMsg_X                    //024
	,MSG_AppMode                        //025
	,MSG_AutoTuneMode                   //026
	,MSG_StopMode                       //027
	,MSG_FanCtrlMode                    //028
	,MSG_LoadDutyMsg_X                  //029
	,MSG_MotSpdUnit                     //030
	,MSG_Int485CharForm                 //031
	,MSG_AnalogInSrc                    //032
	,MSG_LoHiSel                        //033
	,MSG_OptName                        //034
	,MSG_AdcAdjustInLv                  //035
	,MSG_TermiAIType                    //036
	,MSG_AuxCalcType                    //037
	,MSG_MonitorPara                    //038
	,MSG_EsaveMsg_X                     //039
	,MSG_MacroType                      //040
	,MSG_InvStateType                   //041
	,MSG_InVoltFreq                     //042
	,MSG_TripName                       //043
	,MSG_RunEnableType                  //044
	,MSG_RunDisStopMode                 //045
	,MSG_WarningName                    //046
	,MSG_AutoTuneSeq                    //047
	,MSG_PIDUnitScale                   //048
	,MSG_FeedbackSrc                    //049
	,MSG_PIDOutputMode                  //050
	,MSG_PIDUnit                        //051
	,MSG_ProcPIDCtrlMode                //052
	,MSG_FuncRunMode                    //053
	,MSG_ReferenceSrc                   //054
	,MSG_LoadSpdScale                   //055
	,MSG_LoadSpdUnit                    //056
	,MSG_InvIpType                      //057
	,MSG_PwmModeType                    //058
	,MSG_FBusBRate                      //059
	,MSG_SsModeType                     //060
	,MSG_StallSrcMsg_X                  //061
	,MSG_TripStop1Mode                  //062
	,MSG_TripStop2Mode                  //063
	,MSG_TripMode                       //064
	,MSG_AdcInputType                   //065
	,MSG_RotaryEncInLineType            //066
	,MSG_RotaryEncInputType             //067
	,MSG_TOTAL                     //068
};


#define MSG_COUNT_YESNO                 	2
#define MSG_COUNT_TIMESCALE             	3
#define MSG_COUNT_INITGRP               	13
#define MSG_COUNT_RUNCMDSRC             	7
#define MSG_COUNT_FREQREFSRC2           	7
#define MSG_COUNT_TORQUESRC             	8
#define MSG_COUNT_FREQREFSRC1           	10
#define MSG_COUNT_XCELCURVE             	5
#define MSG_COUNT_STARTMODE             	3
#define MSG_COUNT_XCELFREQMODE          	2
#define MSG_COUNT_BOOSTMODE             	2
#define MSG_COUNT_VFMODE                	4
#define MSG_COUNT_INT485BRATE           	8
#define MSG_COUNT_MOTCOOLING            	2
#define MSG_COUNT_INVCAP                	39
#define MSG_COUNT_CTRLMODE              	6
#define MSG_COUNT_AOMODE                	16
#define MSG_COUNT_DIMODE                	44
#define MSG_COUNT_DOMODE                	32
#define MSG_COUNT_MOTCAP                	28
#define MSG_COUNT_DNOUTINST             	8
#define MSG_COUNT_DNININST              	8
#define MSG_COUNT_RUNPREVENT            	3
#define MSG_COUNT_LOSTAICHKLVL          	2
#define MSG_COUNT_MODBUSMSG_X           	2
#define MSG_COUNT_APPMODE               	7
#define MSG_COUNT_AUTOTUNEMODE          	7
#define MSG_COUNT_STOPMODE              	5
#define MSG_COUNT_FANCTRLMODE           	3
#define MSG_COUNT_LOADDUTYMSG_X         	2
#define MSG_COUNT_MOTSPDUNIT            	2
#define MSG_COUNT_INT485CHARFORM        	4
#define MSG_COUNT_ANALOGINSRC           	3
#define MSG_COUNT_LOHISEL               	2
#define MSG_COUNT_OPTNAME               	25
#define MSG_COUNT_ADCADJUSTINLV         	3
#define MSG_COUNT_TERMIAITYPE           	3
#define MSG_COUNT_AUXCALCTYPE           	14
#define MSG_COUNT_MONITORPARA           	25
#define MSG_COUNT_ESAVEMSG_X            	3
#define MSG_COUNT_MACROTYPE             	3
#define MSG_COUNT_INVSTATETYPE          	4
#define MSG_COUNT_INVOLTFREQ            	2
#define MSG_COUNT_TRIPNAME              	41
#define MSG_COUNT_RUNENABLETYPE         	2
#define MSG_COUNT_RUNDISSTOPMODE        	3
#define MSG_COUNT_WARNINGNAME           	13
#define MSG_COUNT_AUTOTUNESEQ           	10
#define MSG_COUNT_PIDUNITSCALE          	5
#define MSG_COUNT_FEEDBACKSRC           	7
#define MSG_COUNT_PIDOUTPUTMODE         	5
#define MSG_COUNT_PIDUNIT               	7
#define MSG_COUNT_PROCPIDCTRLMODE       	4
#define MSG_COUNT_FUNCRUNMODE           	3
#define MSG_COUNT_REFERENCESRC          	7
#define MSG_COUNT_LOADSPDSCALE          	5
#define MSG_COUNT_LOADSPDUNIT           	2
#define MSG_COUNT_INVIPTYPE             	2
#define MSG_COUNT_PWMMODETYPE           	2
#define MSG_COUNT_FBUSBRATE             	16
#define MSG_COUNT_SSMODETYPE            	2
#define MSG_COUNT_STALLSRCMSG_X         	4
#define MSG_COUNT_TRIPSTOP1MODE         	5
#define MSG_COUNT_TRIPSTOP2MODE         	6
#define MSG_COUNT_TRIPMODE              	3
#define MSG_COUNT_ADCINPUTTYPE          	2
#define MSG_COUNT_ROTARYENCINLINETYPE   	3
#define MSG_COUNT_ROTARYENCINPUTTYPE    	3



S_MSG_TYPE KpdParaGetMsgData(WORD wMsgIdx, WORD wMsgNum);
WORD KpdParaGetMsgSize(WORD wMsgIdx);
#endif  //KEYPAD_MESSAG_H 


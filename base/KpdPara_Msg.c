// PRQA S 502, 4130, 4131, 750, 759, 1514, 3218, 1504, 1505, 1503, 2860, 2895 EOF


//========================================= 
// TABLE EDITOR 3 : 인버터 Message들 저장   
//=========================================/ 
          
          
#include "BaseDefine.H"
#include "KPD_Title_Enum.H"
#include "KpdPara_Msg.H"


static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], WORD wMsgNum);



static const S_MSG_TYPE t_astYesNO[MSG_COUNT_YESNO] = {                       //MSG_YesNO           //
	 {T_No                ,0xFF  }                           //"----- No -----"
	,{T_Yes               ,0xFF  }                           //"----- Yes ----"
};


static const S_MSG_TYPE t_astTimeScale[MSG_COUNT_TIMESCALE] = {               //MSG_TimeScale       //
	 {T_00nsec            ,1     }                           //"0.01 sec      "
	,{T_0nsec             ,1     }                           //"0.1 sec       "
	,{T_nsec              ,1     }                           //"1 sec         "
};


static const S_MSG_TYPE t_astInitGrp[MSG_COUNT_INITGRP] = {                   //MSG_InitGrp         //
	 {T_No                ,0xFF  }                           //"----- No -----"
	,{T_AllGroup          ,0xFF  }                           //"All Grp       "
	,{T_DRV               ,0xFF  }                           //"DRV Grp       "
	,{T_BAS               ,0xFF  }                           //"BAS Grp       "
	,{T_ADV               ,0xFF  }                           //"ADV Grp       "
	,{T_CON               ,0xFF  }                           //"CON Grp       "
	,{T_IN                ,0xFF  }                           //"IN Grp        "
	,{T_OUT               ,0xFF  }                           //"OUT Grp       "
	,{T_COM               ,0xFF  }                           //"COM Grp       "
	,{T_PID               ,0xFF  }                           //"PID Grp       "
	,{T_PRT               ,0xFF  }                           //"PRT Grp       "
	,{T_ENC               ,0xFF  }                           //"ENC Grp       "
	,{T_M2                ,0xFF  }                           //"M2 Grp        "
};


static const S_MSG_TYPE t_astRunCmdSrc[MSG_COUNT_RUNCMDSRC] = {               //MSG_RunCmdSrc       //
	 {T_Keypad            ,0xFF  }                           //"Keypad        "
	,{T_FxRxn             ,1     }                           //"Fx/Rx-1       "
	,{T_FxRxn             ,2     }                           //"Fx/Rx-2       "
	,{T_3Wire             ,0xFF  }                           //"3-Wire        "
	,{T_Int485            ,0xFF  }                           //"Int 485       "
	,{T_FieldBus          ,0xFF  }                           //"FieldBus      "
	,{T_PLC               ,0xFF  }                           //"PLC           "
};


static const S_MSG_TYPE t_astFreqRefSrc2[MSG_COUNT_FREQREFSRC2] = {           //MSG_FreqRefSrc2     //2009/04/22 LBK EXTIO2 추가 타이틀
	 {T_Keypadn           ,1     }                           //"Keypad-1      "
	,{T_Keypadn           ,2     }                           //"Keypad-2      "
	,{T_AnalogInnn        ,1     }                           //"Analog In 1   "
	,{T_AnalogInnn        ,2     }                           //"Analog In 2   "
	,{T_Int485            ,0xFF  }                           //"Int 485       "
	,{T_FieldBus          ,0xFF  }                           //"FieldBus      "
	,{T_PLC               ,0xFF  }                           //"PLC           "
};


static const S_MSG_TYPE t_astTorqueSrc[MSG_COUNT_TORQUESRC] = {               //MSG_TorqueSrc       //2009/04/22 LBK EXTIO2 추가 타이틀
	 {T_Keypad            ,0xFF  }                           //"Keypad        "
	,{T_AnalogInnn        ,1     }                           //"Analog In 1   "
	,{T_AnalogInnn        ,2     }                           //"Analog In 2   "
	,{T_Int485            ,0xFF  }                           //"Int 485       "
	,{T_FieldBus          ,0xFF  }                           //"FieldBus      "
	,{T_PLC               ,0xFF  }                           //"PLC           "
	,{T_Synchro           ,0xFF  }                           //"Synchro       "
	,{T_UpDownDrive       ,0xFF  }                           //"Up Down Drive "
};


static const S_MSG_TYPE t_astFreqRefSrc1[MSG_COUNT_FREQREFSRC1] = {           //MSG_FreqRefSrc1     //2009/04/22 LBK EXTIO2 추가 타이틀
	 {T_Keypadn           ,1     }                           //"Keypad-1      "
	,{T_Keypadn           ,2     }                           //"Keypad-2      "
	,{T_AnalogInnn        ,1     }                           //"Analog In 1   "
	,{T_AnalogInnn        ,2     }                           //"Analog In 2   "
	,{T_Int485            ,0xFF  }                           //"Int 485       "
	,{T_Encoder           ,0xFF  }                           //"Encoder       "
	,{T_FieldBus          ,0xFF  }                           //"FieldBus      "
	,{T_PLC               ,0xFF  }                           //"PLC           "
	,{T_Synchro           ,0xFF  }                           //"Synchro       "
	,{T_UpDownDrive       ,0xFF  }                           //"Up Down Drive "
};


static const S_MSG_TYPE t_astXcelCurve[MSG_COUNT_XCELCURVE] = {               //MSG_XcelCurve       //
	 {T_Linear            ,0xFF  }                           //"Linear        "
	,{T_Scurve            ,0xFF  }                           //"S-curve       "
	,{T_Ucurve            ,0xFF  }                           //"U-curve       "
	,{T_Minimum           ,0xFF  }                           //"Minimum       "
	,{T_Optimum           ,0xFF  }                           //"Optimum       "
};


static const S_MSG_TYPE t_astStartMode[MSG_COUNT_STARTMODE] = {               //MSG_StartMode       //
	 {T_Accel             ,0xFF  }                           //"Acc           "
	,{T_DcStart           ,0xFF  }                           //"Dc-Start      "
	,{T_FlyingStart       ,0xFF  }                           //"Flying-Start  "
};


static const S_MSG_TYPE t_astXcelFreqMode[MSG_COUNT_XCELFREQMODE] = {         //MSG_XcelFreqMode    //
	 {T_MaxFreq           ,0xFF  }                           //"Max Freq      "
	,{T_deltafreq         ,0xFF  }                           //"Delta Freq    "
};


static const S_MSG_TYPE t_astBoostMode[MSG_COUNT_BOOSTMODE] = {               //MSG_BoostMode       //
	 {T_Manual            ,0xFF  }                           //"Manual        "
	,{T_Auto              ,0xFF  }                           //"Auto          "
};


static const S_MSG_TYPE t_astVfMode[MSG_COUNT_VFMODE] = {                     //MSG_VfMode          //
	 {T_Linear            ,0xFF  }                           //"Linear        "
	,{T_Square            ,0xFF  }                           //"Square        "
	,{T_UserVF            ,0xFF  }                           //"User V/F      "
	,{T_Squaren           ,2     }                           //"Square 2      "
};


static const S_MSG_TYPE t_astInt485BRate[MSG_COUNT_INT485BRATE] = {           //MSG_Int485BRate     //
	 {T_nnn00bps          ,12    }                           //" 1200 bps     "
	,{T_nnn00bps          ,24    }                           //" 2400 bps     "
	,{T_nnn00bps          ,48    }                           //" 4800 bps     "
	,{T_nnn00bps          ,96    }                           //" 9600 bps     "
	,{T_nnn00bps          ,192   }                           //"19200 bps     "
	,{T_38400bps          ,0xFF  }                           //"38400 bps     "
	,{T_nnnKbps           ,56    }                           //" 56 Kbps      "
	,{T_nnnKbps           ,112   }                           //"112 Kbps      "
};


static const S_MSG_TYPE t_astMotCooling[MSG_COUNT_MOTCOOLING] = {             //MSG_MotCooling      //
	 {T_Selfcool          ,0xFF  }                           //"Self-cool     "
	,{T_Forcedcool        ,0xFF  }                           //"Forced-cool   "
};


static const S_MSG_TYPE t_astInvCap[MSG_COUNT_INVCAP] = {                     //MSG_InvCap          //
	 {T_ndnnkW2           ,75    }                           //"0.75kW-2      "
	,{T_nndnkW2           ,15    }                           //" 1.5 kW-2     "
	,{T_nndnkW2           ,22    }                           //" 2.2 kW-2     "
	,{T_nndnkW2           ,37    }                           //" 3.7 kW-2     "
	,{T_nndnkW2           ,55    }                           //" 5.5 kW-2     "
	,{T_nndnkW2           ,75    }                           //" 7.5 kW-2     "
	,{T_nnnd0kW2          ,11    }                           //" 11.0 kW-2    "
	,{T_nnnd0kW2          ,15    }                           //" 15.0 kW-2    "
	,{T_nnnd5kW2          ,18    }                           //" 18.5 kW-2    "
	,{T_nnnd0kW2          ,22    }                           //" 22.0 kW-2    "
	,{T_nnnd0kW2          ,30    }                           //" 30.0 kW-2    "
	,{T_nnnd0kW2          ,37    }                           //" 37.0 kW-2    "
	,{T_nnnd0kW2          ,45    }                           //" 45.0 kW-2    "
	,{T_nnnd0kW2          ,55    }                           //" 55.0 kW-2    "
	,{T_ndnnkW4           ,75    }                           //"0.75kW-4      "
	,{T_nndnkW4           ,15    }                           //" 1.5 kW-4     "
	,{T_nndnkW4           ,22    }                           //" 2.2 kW-4     "
	,{T_nndnkW4           ,37    }                           //" 3.7 kW-4     "
	,{T_nndnkW4           ,55    }                           //" 5.5 kW-4     "
	,{T_nndnkW4           ,75    }                           //" 7.5 kW-4     "
	,{T_nnnd0kW4          ,11    }                           //" 11.0 kW-4    "
	,{T_nnnd0kW4          ,15    }                           //" 15.0 kW-4    "
	,{T_nnnd5kW4          ,18    }                           //" 18.5 kW-4    "
	,{T_nnnd0kW4          ,22    }                           //" 22.0 kW-4    "
	,{T_nnnd0kW4          ,30    }                           //" 30.0 kW-4    "
	,{T_nnnd0kW4          ,37    }                           //" 37.0 kW-4    "
	,{T_nnnd0kW4          ,45    }                           //" 45.0 kW-4    "
	,{T_nnnd0kW4          ,55    }                           //" 55.0 kW-4    "
	,{T_nnnd0kW4          ,75    }                           //" 75.0 kW-4    "
	,{T_nnnd0kW4          ,90    }                           //" 90.0 kW-4    "
	,{T_nnnd0kW4          ,110   }                           //"110.0 kW-4    "
	,{T_nnnd0kW4          ,132   }                           //"132.0 kW-4    "
	,{T_nnnd0kW4          ,160   }                           //"160.0 kW-4    "
	,{T_nnnd0kW4          ,185   }                           //"185.0 kW-4    "
	,{T_nnn00kW4          ,22    }                           //" 220.0 kW-4   "
	,{T_nnn00kW4          ,28    }                           //" 280.0 kW-4   "
	,{T_nnn5kW4           ,31    }                           //"315 kW-4      "
	,{T_nnn5kW4           ,37    }                           //"375 kW-4      "
	,{T_nnn00kW4          ,45    }                           //" 450.0 kW-4   "
};


static const S_MSG_TYPE t_astCtrlMode[MSG_COUNT_CTRLMODE] = {                 //MSG_CtrlMode        //
	 {T_VF                ,0xFF  }                           //"V/F           "
	,{T_VFPG              ,0xFF  }                           //"V/F PG        "
	,{T_Slipcompen        ,0xFF  }                           //"Slip Compen   "
	,{T_Sensorlessn       ,1     }                           //"Sensorless-1  "
	,{T_Sensorlessn       ,2     }                           //"Sensorless-2  "
	,{T_Vector            ,0xFF  }                           //"Vector        "
};


static const S_MSG_TYPE t_astAoMode[MSG_COUNT_AOMODE] = {                     //MSG_AoMode          //2009/04/22 LBK EXTIO2 Web추가
	 {T_Frequency         ,0xFF  }                           //"Frequency     "
	,{T_OutputCurrent     ,0xFF  }                           //"Output Current"
	,{T_OutputVoltage     ,0xFF  }                           //"Output Voltage"
	,{T_DCLinkVoltage     ,0xFF  }                           //"DCLink Voltage"
	,{T_Torque            ,0xFF  }                           //"Torque        "
	,{T_OutputPower       ,0xFF  }                           //"Output Power  "
	,{T_Idse              ,0xFF  }                           //"Idse          "
	,{T_Iqse              ,0xFF  }                           //"Iqse          "
	,{T_TargetFreq        ,0xFF  }                           //"Target Freq   "
	,{T_RampFreq          ,0xFF  }                           //"Ramp Freq     "
	,{T_SpeedFdb          ,0xFF  }                           //"Speed Fdb     "
	,{T_SpeedDev          ,0xFF  }                           //"Speed Dev     "
	,{T_PIDRefValue       ,0xFF  }                           //"PID Ref Value "
	,{T_PIDFdbValue       ,0xFF  }                           //"PID Fdb Value "
	,{T_PIDOutput         ,0xFF  }                           //"PID Output    "
	,{T_Constant          ,0xFF  }                           //"Constant      "
};


static const S_MSG_TYPE t_astDiMode[MSG_COUNT_DIMODE] = {                     //MSG_DiMode          //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_FX                ,0xFF  }                           //"FX            "
	,{T_RX                ,0xFF  }                           //"RX            "
	,{T_RST               ,0xFF  }                           //"RST           "
	,{T_ExternalTrip      ,0xFF  }                           //"External Trip "
	,{T_BX                ,0xFF  }                           //"BX            "
	,{T_JOG               ,0xFF  }                           //"JOG           "
	,{T_SpeedL            ,0xFF  }                           //"Speed-L       "
	,{T_SpeedM            ,0xFF  }                           //"Speed-M       "
	,{T_SpeedH            ,0xFF  }                           //"Speed-H       "
	,{T_SpeedX            ,0xFF  }                           //"Speed-X       "
	,{T_XCELL             ,0xFF  }                           //"XCEL-L        "
	,{T_XCELM             ,0xFF  }                           //"XCEL-M        "
	,{T_XCELH             ,0xFF  }                           //"XCEL-H        "
	,{T_XCELStop          ,0xFF  }                           //"XCEL Stop     "
	,{T_RUNEnable         ,0xFF  }                           //"RUN Enable    "
	,{T_3Wire             ,0xFF  }                           //"3-Wire        "
	,{T_2ndSource         ,0xFF  }                           //"2nd Source    "
	,{T_Exchange          ,0xFF  }                           //"Exchange      "
	,{T_Up                ,0xFF  }                           //"Up            "
	,{T_Down              ,0xFF  }                           //"Down          "
	,{T_UDClear           ,0xFF  }                           //"U/D Clear     "
	,{T_AnalogHold        ,0xFF  }                           //"Analog Hold   "
	,{T_2ndMotor          ,0xFF  }                           //"2nd Motor     "
	,{T_PreExcite         ,0xFF  }                           //"Pre Excite    "
	,{T_SpeedTorque       ,0xFF  }                           //"Speed/Torque  "
	,{T_AsrGainn          ,2     }                           //"Asr Gain 2    "
	,{T_ASRPPI            ,0xFF  }                           //"ASR P/PI      "
	,{T_TimerIn           ,0xFF  }                           //"Timer In      "
	,{T_ThermalIn         ,0xFF  }                           //"Thermal In    "
	,{T_disAuxRef         ,0xFF  }                           //"dis Aux Ref   "
	,{T_FWDJOG            ,0xFF  }                           //"FWD JOG       "
	,{T_REVJOG            ,0xFF  }                           //"REV JOG       "
	,{T_PIDRun            ,0xFF  }                           //"PID Run       "
	,{T_PIDOpenLoop       ,0xFF  }                           //"PID Open Loop "
	,{T_PIDRefChange      ,0xFF  }                           //"PID Ref Change"
	,{T_PIDGainChange     ,0xFF  }                           //"PID GainChange"
	,{T_ITermClear        ,0xFF  }                           //"I-Term Clear  "
	,{T_PIDOutHold        ,0xFF  }                           //"PID Out Hold  "
	,{T_PIDSleepON        ,0xFF  }                           //"PID Sleep ON  "
	,{T_PIDSleepChg       ,0xFF  }                           //"PID Sleep Chg "
	,{T_PIDStepRefL       ,0xFF  }                           //"PID Step Ref-L"
	,{T_PIDStepRefM       ,0xFF  }                           //"PID Step Ref-M"
	,{T_PIDStepRefH       ,0xFF  }                           //"PID Step Ref-H"
};


static const S_MSG_TYPE t_astDoMode[MSG_COUNT_DOMODE] = {                     //MSG_DoMode          //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_FDTn              ,1     }                           //"FDT-1         "
	,{T_FDTn              ,2     }                           //"FDT-2         "
	,{T_FDTn              ,3     }                           //"FDT-3         "
	,{T_FDTn              ,4     }                           //"FDT-4         "
	,{T_OverLoad          ,0xFF  }                           //"Over Load     "
	,{T_IOL               ,0xFF  }                           //"IOL           "
	,{T_UnderLoad         ,0xFF  }                           //"Under Load    "
	,{T_FanWarning        ,0xFF  }                           //"Fan Warning   "
	,{T_Stall             ,0xFF  }                           //"Stall         "
	,{T_OverVoltage       ,0xFF  }                           //"Over Voltage  "
	,{T_LowVoltage        ,0xFF  }                           //"Low Voltage   "
	,{T_OverHeat          ,0xFF  }                           //"Over Heat     "
	,{T_LostIntComm       ,0xFF  }                           //"Lost Int Comm "
	,{T_Run               ,0xFF  }                           //"Run           "
	,{T_Stop              ,0xFF  }                           //"Stop          "
	,{T_Steady            ,0xFF  }                           //"Steady        "
	,{T_InverterLine      ,0xFF  }                           //"Inverter Line "
	,{T_CommLine          ,0xFF  }                           //"Comm Line     "
	,{T_SpeedSearch       ,0xFF  }                           //"Speed Search  "
	,{T_Ready             ,0xFF  }                           //"Ready         "
	,{T_ZspdDect          ,0xFF  }                           //"Zspd Dect     "
	,{T_TorqueDect        ,0xFF  }                           //"Torque Dect   "
	,{T_TimerOut          ,0xFF  }                           //"Timer Out     "
	,{T_Trip              ,0xFF  }                           //"Trip          "
	,{T_LostKeypad        ,0xFF  }                           //"Lost Keypad   "
	,{T_DBWarnED          ,0xFF  }                           //"DB Warn %ED   "
	,{T_ENCTune           ,0xFF  }                           //"ENC Tune      "
	,{T_ENCDir            ,0xFF  }                           //"ENC Dir       "
	,{T_OnOffControl      ,0xFF  }                           //"On/Off Control"
	,{T_BRControl         ,0xFF  }                           //"BR Control    "
	,{T_CommOutput        ,0xFF  }                           //"Comm Output   "
};


static const S_MSG_TYPE t_astMotCap[MSG_COUNT_MOTCAP] = {                     //MSG_MotCap          //모터를 선택하는 메세지 이다.
	 {T_nndnkW            ,2     }                           //" 0.2 kW       "
	,{T_nndnkW            ,4     }                           //" 0.4 kW       "
	,{T_ndnnkW            ,75    }                           //"0.75kW        "
	,{T_nndnkW            ,15    }                           //" 1.5 kW       "
	,{T_nndnkW            ,22    }                           //" 2.2 kW       "
	,{T_nndnkW            ,37    }                           //" 3.7 kW       "
	,{T_nndnkW            ,55    }                           //" 5.5 kW       "
	,{T_nndnkW            ,75    }                           //" 7.5 kW       "
	,{T_nnnd0kW           ,11    }                           //" 11.0 kW      "
	,{T_nnnd0kW           ,15    }                           //" 15.0 kW      "
	,{T_nnnd5kW           ,18    }                           //" 18.5 kW      "
	,{T_nnnd0kW           ,22    }                           //" 22.0 kW      "
	,{T_nnnd0kW           ,30    }                           //" 30.0 kW      "
	,{T_nnnd0kW           ,37    }                           //" 37.0 kW      "
	,{T_nnnd0kW           ,45    }                           //" 45.0 kW      "
	,{T_nnnd0kW           ,55    }                           //" 55.0 kW      "
	,{T_nnnd0kW           ,75    }                           //" 75.0 kW      "
	,{T_nnnd0kW           ,90    }                           //" 90.0 kW      "
	,{T_nnnd0kW           ,110   }                           //"110.0 kW      "
	,{T_nnnd0kW           ,132   }                           //"132.0 kW      "
	,{T_nnnd0kW           ,160   }                           //"160.0 kW      "
	,{T_nnnd0kW           ,185   }                           //"185.0 kW      "
	,{T_nnnd0kW           ,200   }                           //"200.0 kW      "
	,{T_nnnd0kW           ,220   }                           //"220.0 kW      "
	,{T_nnn0kW            ,28    }                           //" 280 kW       "
	,{T_nnn5kW            ,31    }                           //"315 kW        "
	,{T_nnn5kW            ,37    }                           //"375 kW        "
	,{T_nnn0kW            ,45    }                           //" 450 kW       "
};


static const S_MSG_TYPE t_astDnOutInst[MSG_COUNT_DNOUTINST] = {               //MSG_DnOutInst       //2006.07.24 LBK Instance 추가
	 {T_nnn               ,20    }                           //" 20           "
	,{T_nnn               ,21    }                           //" 21           "
	,{T_nnn               ,100   }                           //"100           "
	,{T_nnn               ,101   }                           //"101           "
	,{T_nnn               ,121   }                           //"121           "
	,{T_nnn               ,122   }                           //"122           "
	,{T_nnn               ,123   }                           //"123           "
	,{T_nnn               ,124   }                           //"124           "
};


static const S_MSG_TYPE t_astDnInInst[MSG_COUNT_DNININST] = {                 //MSG_DnInInst        //2006.07.24 LBK 인스턴스 추가
	 {T_nnn               ,70    }                           //" 70           "
	,{T_nnn               ,71    }                           //" 71           "
	,{T_nnn               ,110   }                           //"110           "
	,{T_nnn               ,111   }                           //"111           "
	,{T_nnn               ,141   }                           //"141           "
	,{T_nnn               ,142   }                           //"142           "
	,{T_nnn               ,143   }                           //"143           "
	,{T_nnn               ,144   }                           //"144           "
};


static const S_MSG_TYPE t_astRunPrevent[MSG_COUNT_RUNPREVENT] = {             //MSG_RunPrevent      //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_ForwardPrev       ,0xFF  }                           //"Forward Prev  "
	,{T_ReversePrev       ,0xFF  }                           //"Reverse Prev  "
};


static const S_MSG_TYPE t_astLostAiChkLvl[MSG_COUNT_LOSTAICHKLVL] = {         //MSG_LostAiChkLvl    //
	 {T_HalfofLoLmt       ,0xFF  }                           //"Half of Lo Lmt "
	,{T_BelowLoLmt        ,0xFF  }                           //"Below Lo Lmt   "
};


static const S_MSG_TYPE t_astmodbusMsg_X[MSG_COUNT_MODBUSMSG_X] = {           //MSG_modbusMsg_X     //
	 {T_ModBusRTU         ,0xFF  }                           //"ModBus RTU    "
	,{T_LSInv485          ,0xFF  }                           //"LS Inv 485    "
};


static const S_MSG_TYPE t_astAppMode[MSG_COUNT_APPMODE] = {                   //MSG_AppMode         //2009/04/22 LBK EXTIO2
	 {T_None              ,0xFF  }                           //"None          "
	,{T_Traverse          ,0xFF  }                           //"Traverse      "
	,{T_ProcPID           ,0xFF  }                           //"Proc PID      "
	,{T_MMC               ,0xFF  }                           //"MMC           "
	,{T_AutoSequenc       ,0xFF  }                           //"Auto Sequence "
	,{T_TensionCtrl       ,0xFF  }                           //"Tension Ctrl  "
	,{T_ExtPIDCtrl        ,0xFF  }                           //"Ext PID Ctrl  "
};


static const S_MSG_TYPE t_astAutoTuneMode[MSG_COUNT_AUTOTUNEMODE] = {         //MSG_AutoTuneMode    //2007/07/25 KKY 정지형 튜닝 메세지 추가
	 {T_None              ,0xFF  }                           //"None          "
	,{T_All               ,0xFF  }                           //"All           "
	,{T_AllStdstl         ,0xFF  }                           //"All (Stdstl)  "
	,{T_RsLsigma          ,0xFF  }                           //"Rs+Lsigma     "
	,{T_EncTest           ,0xFF  }                           //"Enc Test      "
	,{T_Tr                ,0xFF  }                           //"Tr            "
	,{T_TrStdstl          ,0xFF  }                           //"Tr (Stdstl)   "
};


static const S_MSG_TYPE t_astStopMode[MSG_COUNT_STOPMODE] = {                 //MSG_StopMode        //
	 {T_Dec               ,0xFF  }                           //"Dec           "
	,{T_DCBrake           ,0xFF  }                           //"DC-Brake      "
	,{T_FreeRun           ,0xFF  }                           //"Free-Run      "
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_PowerBraking      ,0xFF  }                           //"Power Braking "
};


static const S_MSG_TYPE t_astFanCtrlMode[MSG_COUNT_FANCTRLMODE] = {           //MSG_FanCtrlMode     //
	 {T_DuringRun         ,0xFF  }                           //"During Run    "
	,{T_AlwaysON          ,0xFF  }                           //"Always ON     "
	,{T_TempControl       ,0xFF  }                           //"Temp Control  "
};


static const S_MSG_TYPE t_astLoadDutyMsg_X[MSG_COUNT_LOADDUTYMSG_X] = {       //MSG_LoadDutyMsg_X   //
	 {T_NormalDuty        ,0xFF  }                           //"Normal Duty   "
	,{T_HeavyDuty         ,0xFF  }                           //"Heavy Duty    "
};


static const S_MSG_TYPE t_astMotSpdUnit[MSG_COUNT_MOTSPDUNIT] = {             //MSG_MotSpdUnit      //
	 {T_HzDisplay         ,0xFF  }                           //"Hz Display    "
	,{T_RpmDisplay        ,0xFF  }                           //"Rpm Display   "
};


static const S_MSG_TYPE t_astInt485CharForm[MSG_COUNT_INT485CHARFORM] = {     //MSG_Int485CharForm  //
	 {T_DnPNSn            ,81    }                           //"  D8 / PN / S1"
	,{T_DnPNSn            ,82    }                           //"  D8 / PN / S2"
	,{T_DnPESn            ,81    }                           //"  D8 / PE / S1"
	,{T_DnPOSn            ,81    }                           //"  D8 / PO / S1"
};


static const S_MSG_TYPE t_astAnalogInSrc[MSG_COUNT_ANALOGINSRC] = {           //MSG_AnalogInSrc     //2009/04/22 LBK EXTIO2
	 {T_None              ,0xFF  }                           //"None          "
	,{T_AnalogInnn        ,1     }                           //"Analog In 1   "
	,{T_AnalogInnn        ,2     }                           //"Analog In 2   "
};


static const S_MSG_TYPE t_astLoHiSel[MSG_COUNT_LOHISEL] = {                   //MSG_LoHiSel         //
	 {T_Low               ,0xFF  }                           //"Low           "
	,{T_High              ,0xFF  }                           //"High          "
};


static const S_MSG_TYPE t_astOptName[MSG_COUNT_OPTNAME] = {                   //MSG_OptName         //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_RS485             ,0xFF  }                           //"RS-485        "
	,{T_DeviceNet         ,0xFF  }                           //"DeviceNet     "
	,{T_ProfiBus          ,0xFF  }                           //"ProfiBus      "
	,{T_FNet              ,0xFF  }                           //"F-Net         "
	,{T_LonWorks          ,0xFF  }                           //"LonWorks      "
	,{T_Ethernet          ,0xFF  }                           //"Ethernet      "
	,{T_RNet              ,0xFF  }                           //"RNet          "
	,{T_BACnet            ,0xFF  }                           //"BACnet        "
	,{T_CANopen           ,0xFF  }                           //"CANopen       "
	,{T_PLC               ,0xFF  }                           //"PLC           "
	,{T_Synchro           ,0xFF  }                           //"Synchro       "
	,{T_CCLink            ,0xFF  }                           //"CC-Link       "
	,{T_CommOptName       ,0xFF  }                           //"CommOptName   "
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_ExtIOn            ,1     }                           //"Ext I/O 1     "
	,{T_ExtIOn            ,2     }                           //"Ext I/O 2     "
	,{T_MMC               ,0xFF  }                           //"MMC           "
	,{T_Encoder           ,0xFF  }                           //"Encoder       "
	,{T_Reservednn        ,24    }                           //"Reserved - 24 "
};


static const S_MSG_TYPE t_astAdcAdjustInLv[MSG_COUNT_ADCADJUSTINLV] = {       //MSG_AdcAdjustInLv   //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_MaxInput          ,0xFF  }                           //"Max Input     "
	,{T_MinInput          ,0xFF  }                           //"Min Input     "
};


static const S_MSG_TYPE t_astTermiAIType[MSG_COUNT_TERMIAITYPE] = {           //MSG_TermiAIType     //
	 {T_Volt_Unipolar     ,0xFF  }                           //"Volt_Unipolar "
	,{T_Volt_Bipolar      ,0xFF  }                           //"Volt_Bipolar  "
	,{T_Current           ,0xFF  }                           //"Current       "
};


static const S_MSG_TYPE t_astAuxCalcType[MSG_COUNT_AUXCALCTYPE] = {           //MSG_AuxCalcType     //2006.08.10 LBK 메세지 수정 %를 없에소 2*를 추가
	 {T_MGA               ,0xFF  }                           //"M + (G * A)   "
	,{T_MGA12             ,0xFF  }                           //"M * (G * A)   "
	,{T_MGA123            ,0xFF  }                           //"M / (G * A)   "
	,{T_MMGA              ,0xFF  }                           //"M+(M*(G*A))   "
	,{T_MG2A50            ,0xFF  }                           //"M+G*2*(A-50)  "
	,{T_MG2A501           ,0xFF  }                           //"M*(G*2*(A-50))"
	,{T_MG2A5012          ,0xFF  }                           //"M/(G*2*(A-50))"
	,{T_MMG2A50           ,0xFF  }                           //"M+M*G*2*(A-50)"
	,{T_MA2               ,0xFF  }                           //"(M-A)^2       "
	,{T_M2A2              ,0xFF  }                           //"M^2 + A^2     "
	,{T_MAXMA             ,0xFF  }                           //"MAX(M,A)      "
	,{T_MINMA             ,0xFF  }                           //"MIN(M,A)      "
	,{T_MA22              ,0xFF  }                           //"(M+A)/2       "
	,{T_RootMA            ,0xFF  }                           //"Root(M+A)     "
};


static const S_MSG_TYPE t_astMonitorPara[MSG_COUNT_MONITORPARA] = {           //MSG_MonitorPara     //모니터 메세지
	 {T_Frequency         ,0xFF  }                           //"Frequency     "
	,{T_Speed             ,0xFF  }                           //"Speed         "
	,{T_OutputCurrent     ,0xFF  }                           //"Output Current"
	,{T_OutputVoltage     ,0xFF  }                           //"Output Voltage"
	,{T_OutputPower       ,0xFF  }                           //"Output Power  "
	,{T_WHourCounter      ,0xFF  }                           //"WHour Counter "
	,{T_DCLinkVoltage     ,0xFF  }                           //"DCLink Voltage"
	,{T_DIStatus          ,0xFF  }                           //"DI Status     "
	,{T_DOStatus          ,0xFF  }                           //"DO Status     "
	,{T_AInMonitor        ,1     }                           //"AI1 Monitor   "
	,{T_AInMonitor1       ,1     }                           //"AI1 Monitor[%]"
	,{T_AInMonitor        ,2     }                           //"AI2 Monitor   "
	,{T_AInMonitor1       ,2     }                           //"AI2 Monitor[%]"
	,{T_Reservednn        ,13    }                           //"Reserved - 13 "
	,{T_Reservednn        ,14    }                           //"Reserved - 14 "
	,{T_Reservednn        ,15    }                           //"Reserved - 15 "
	,{T_Reservednn        ,16    }                           //"Reserved - 16 "
	,{T_PIDOutput         ,0xFF  }                           //"PID Output    "
	,{T_PIDRefValue       ,0xFF  }                           //"PID Ref Value "
	,{T_PIDFdbValue       ,0xFF  }                           //"PID Fdb Value "
	,{T_Torque            ,0xFF  }                           //"Torque        "
	,{T_TorqueLimit       ,0xFF  }                           //"Torque Limit  "
	,{T_TrqBiasRef        ,0xFF  }                           //"Trq Bias Ref  "
	,{T_SpeedLimit        ,0xFF  }                           //"Speed Limit   "
	,{T_LoadSpeed         ,0xFF  }                           //"Load Speed    "
};


static const S_MSG_TYPE t_astEsaveMsg_X[MSG_COUNT_ESAVEMSG_X] = {             //MSG_EsaveMsg_X      //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_Manual            ,0xFF  }                           //"Manual        "
	,{T_Auto              ,0xFF  }                           //"Auto          "
};


static const S_MSG_TYPE t_astMacroType[MSG_COUNT_MACROTYPE] = {               //MSG_MacroType       //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_None              ,0xFF  }                           //"Draw App      "
	,{T_Traverse          ,0xFF  }                           //"Traverse      "
};


static const S_MSG_TYPE t_astInvStateType[MSG_COUNT_INVSTATETYPE] = {         //MSG_InvStateType    //2006.03.13 LBK 트립 발생시 인버터의 상태를 보여주는 메세지
	 {T_Accel             ,0xFF  }                           //"Acc           "
	,{T_Dec               ,0xFF  }                           //"Dec           "
	,{T_Steady            ,0xFF  }                           //"Steady        "
	,{T_Stop              ,0xFF  }                           //"Stop          "
};


static const S_MSG_TYPE t_astInVoltFreq[MSG_COUNT_INVOLTFREQ] = {             //MSG_InVoltFreq      //
	 {T_nnnHz             ,60    }                           //" 60Hz         "
	,{T_nnnHz             ,50    }                           //" 50Hz         "
};


static const S_MSG_TYPE t_astTripName[MSG_COUNT_TRIPNAME] = {                 //MSG_TripName        //PJW 2008/11/21 (Gr3 이하 반영)
	 {T_ADCOffSet         ,0xFF  }                           //"ADC Off Set   "
	,{T_EEPRomError       ,0xFF  }                           //"EEPRom Error  "
	,{T_WatchDogn         ,1     }                           //"Watch Dog-1   "
	,{T_GatePwrLoss       ,0xFF  }                           //"Gate Pwr Loss "
	,{T_MainSysError      ,0xFF  }                           //"Main Sys Error"
	,{T_OverLoad          ,0xFF  }                           //"Over Load     "
	,{T_UnderLoad         ,0xFF  }                           //"Under Load    "
	,{T_InverterOLT       ,0xFF  }                           //"Inverter OLT  "
	,{T_EThermal          ,0xFF  }                           //"E-Thermal     "
	,{T_GroundTrip        ,0xFF  }                           //"Ground Trip   "
	,{T_OutPhaseOpen      ,0xFF  }                           //"Out Phase Open"
	,{T_InPhaseOpen       ,0xFF  }                           //"In Phase Open "
	,{T_OverSpeed         ,0xFF  }                           //"Over Speed    "
	,{T_SpeedDevTrip      ,0xFF  }                           //"Speed Dev Trip"
	,{T_NTCOpen           ,0xFF  }                           //"NTC Open      "
	,{T_OverCurrentn      ,1     }                           //"Over Current1 "
	,{T_OverVoltage       ,0xFF  }                           //"Over Voltage  "
	,{T_ExternalTrip      ,0xFF  }                           //"External Trip "
	,{T_OverCurrentn      ,2     }                           //"Over Current2 "
	,{T_OverHeat          ,0xFF  }                           //"Over Heat     "
	,{T_FuseOpen          ,0xFF  }                           //"Fuse Open     "
	,{T_EncError          ,0xFF  }                           //"Enc Error     "
	,{T_ThermalTrip       ,0xFF  }                           //"Thermal Trip  "
	,{T_FanTrip           ,0xFF  }                           //"Fan Trip      "
	,{T_ParaWriteTrip     ,0xFF  }                           //"ParaWrite Trip"
	,{T_PrePIDFail        ,0xFF  }                           //"Pre-PID Fail  "
	,{T_IOBoardTrip       ,0xFF  }                           //"IO Board Trip "
	,{T_ExtBrake          ,0xFF  }                           //"Ext-Brake     "
	,{T_NoMotorTrip       ,0xFF  }                           //"No Motor Trip "
	,{T_OptionTripn       ,1     }                           //"Option Trip-1 "
	,{T_OptionTripn       ,2     }                           //"Option Trip-2 "
	,{T_OptionTripn       ,3     }                           //"Option Trip-3 "
	,{T_SafetyOptErr      ,0xFF  }                           //"Safety Opt Err"
	,{T_IP54FanTrip       ,0xFF  }                           //"IP54 Fan Trip "
	,{T_BX                ,0xFF  }                           //"BX            "
	,{T_LowVoltage        ,0xFF  }                           //"Low Voltage   "
	,{T_LostAnalogIn      ,0xFF  }                           //"Lost Analog In"
	,{T_LostIntComm       ,0xFF  }                           //"Lost Int Comm "
	,{T_LostFieldbus      ,0xFF  }                           //"Lost Fieldbus "
	,{T_LostKeypad        ,0xFF  }                           //"Lost Keypad   "
	,{T_LostUSB           ,0xFF  }                           //"Lost USB      "
};


static const S_MSG_TYPE t_astRunEnableType[MSG_COUNT_RUNENABLETYPE] = {       //MSG_RunEnableType   //
	 {T_AlwaysEnable      ,0xFF  }                           //"Always Enable "
	,{T_DIDependent       ,0xFF  }                           //"DI Dependent  "
};


static const S_MSG_TYPE t_astRunDisStopMode[MSG_COUNT_RUNDISSTOPMODE] = {     //MSG_RunDisStopMode  //
	 {T_FreeRun           ,0xFF  }                           //"Free-Run      "
	,{T_QStop             ,0xFF  }                           //"Q-Stop        "
	,{T_QStopResume       ,0xFF  }                           //"Q-Stop Resume "
};


static const S_MSG_TYPE t_astWarningName[MSG_COUNT_WARNINGNAME] = {           //MSG_WarningName     //T_RetryTrTune추가 //2006.08.10 LBK Fan Warning  으로 수정
	 {T_OverLoad          ,0xFF  }                           //"Over Load     "
	,{T_UnderLoad         ,0xFF  }                           //"Under Load    "
	,{T_InvOverLoad       ,0xFF  }                           //"Inv Over Load "
	,{T_LostAnalogIn      ,0xFF  }                           //"Lost Analog In"
	,{T_LostIntComm       ,0xFF  }                           //"Lost Int Comm "
	,{T_LostFieldbus      ,0xFF  }                           //"Lost Fieldbus "
	,{T_LostKeypad        ,0xFF  }                           //"Lost Keypad   "
	,{T_LostUSB           ,0xFF  }                           //"Lost USB      "
	,{T_FanWarning        ,0xFF  }                           //"Fan Warning   "
	,{T_DBWarnED          ,0xFF  }                           //"DB Warn %ED   "
	,{T_EncConnCheck      ,0xFF  }                           //"Enc Conn Check"
	,{T_EncDirCheck       ,0xFF  }                           //"Enc Dir Check "
	,{T_RetryTrTune       ,0xFF  }                           //"Retry Tr Tune "
};


static const S_MSG_TYPE t_astAutoTuneSeq[MSG_COUNT_AUTOTUNESEQ] = {           //MSG_AutoTuneSeq     //
	 {T_Blank             ,0xFF  }                           //"              "
	,{T_RsTuning          ,0xFF  }                           //"Rs Tuning     "
	,{T_LsigmaTuning      ,0xFF  }                           //"Lsigma Tuning "
	,{T_LsigmaTuning      ,0xFF  }                           //"Lsigma Tuning "
	,{T_LsTuning          ,0xFF  }                           //"Ls Tuning     "
	,{T_EncTest           ,0xFF  }                           //"Enc Test      "
	,{T_TrTuning          ,0xFF  }                           //"Tr Tuning     "
	,{T_EncConnCheck      ,0xFF  }                           //"Enc Conn Check"
	,{T_EncDirCheck       ,0xFF  }                           //"Enc Dir Check "
	,{T_LsTrTuning        ,0xFF  }                           //"Ls,Tr Tuning  "
};


static const S_MSG_TYPE t_astPIDUnitScale[MSG_COUNT_PIDUNITSCALE] = {         //MSG_PIDUnitScale    //Proc PID 의 100%에 대한 Scale 값
	 {T_xnnn              ,100   }                           //"x 100         "
	,{T_xnnn              ,10    }                           //"x  10         "
	,{T_xnnn              ,1     }                           //"x  1          "
	,{T_x0n               ,1     }                           //"x 0.1         "
	,{T_x00n              ,1     }                           //"x 0.01        "
};


static const S_MSG_TYPE t_astFeedbackSrc[MSG_COUNT_FEEDBACKSRC] = {           //MSG_FeedbackSrc     //Proc PID의 Reference Source
	 {T_AnalogInnn        ,1     }                           //"Analog In 1   "
	,{T_AnalogInnn        ,2     }                           //"Analog In 2   "
	,{T_Int485            ,0xFF  }                           //"Int 485       "
	,{T_FieldBus          ,0xFF  }                           //"FieldBus      "
	,{T_PLC               ,0xFF  }                           //"PLC           "
	,{T_ExtPIDnOut        ,1     }                           //"Ext PID-1 Out  "
	,{T_ExtPIDnFdb        ,1     }                           //"Ext PID-1 Fdb  "
};


static const S_MSG_TYPE t_astPIDOutputMode[MSG_COUNT_PIDOUTPUTMODE] = {       //MSG_PIDOutputMode   //Proc PID의 Reference Source
	 {T_NotUseOutput      ,0xFF  }                           //"Not Use Output"
	,{T_OnlyPIDOut        ,0xFF  }                           //"Only PID Out   "
	,{T_MainFreq          ,0xFF  }                           //"Main Freq      "
	,{T_ExtPIDnOut        ,1     }                           //"Ext PID-1 Out  "
	,{T_MainEPIDn         ,1     }                           //"Main + EPID-1  "
};


static const S_MSG_TYPE t_astPIDUnit[MSG_COUNT_PIDUNIT] = {                   //MSG_PIDUnit         //Proc PID의 Reference Source
	 {T_Hz                ,0xFF  }                           //"Hz            "
	,{T_rpm               ,0xFF  }                           //"rpm            "
	,{T_Per               ,0xFF  }                           //"%              "
	,{T_mbar              ,0xFF  }                           //"mBar          "
	,{T_bar               ,0xFF  }                           //"Bar           "
	,{T_Pa                ,0xFF  }                           //"Pa            "
	,{T_kPa               ,0xFF  }                           //"kPa           "
};


static const S_MSG_TYPE t_astProcPIDCtrlMode[MSG_COUNT_PROCPIDCTRLMODE] = {   //MSG_ProcPIDCtrlMode //Proc PID의 Reference Source
	 {T_None              ,0xFF  }                           //"None          "
	,{T_RunInDrvRunning   ,0xFF  }                           //"Run In Drv Run"
	,{T_AlwaysEnable      ,0xFF  }                           //"Always Enable  "
	,{T_DIDependent       ,0xFF  }                           //"DI Dependent  "
};


static const S_MSG_TYPE t_astFuncRunMode[MSG_COUNT_FUNCRUNMODE] = {           //MSG_FuncRunMode     //Proc PID의 Reference Source
	 {T_None              ,0xFF  }                           //"None          "
	,{T_AlwaysEnable      ,0xFF  }                           //"Always Enable  "
	,{T_DIDependent       ,0xFF  }                           //"DI Dependent   "
};


static const S_MSG_TYPE t_astReferenceSrc[MSG_COUNT_REFERENCESRC] = {         //MSG_ReferenceSrc    //Proc PID의 Reference Source
	 {T_Keypad            ,0xFF  }                           //"Keypad        "
	,{T_AnalogInnn        ,1     }                           //"Analog In 1   "
	,{T_AnalogInnn        ,2     }                           //"Analog In 2   "
	,{T_Int485            ,0xFF  }                           //"Int 485       "
	,{T_FieldBus          ,0xFF  }                           //"FieldBus      "
	,{T_PLC               ,0xFF  }                           //"PLC           "
	,{T_ExtPIDnOut        ,1     }                           //"Ext PID-1 Out  "
};


static const S_MSG_TYPE t_astLoadSpdScale[MSG_COUNT_LOADSPDSCALE] = {         //MSG_LoadSpdScale    //
	 {T_xnnn              ,1     }                           //"x  1          "
	,{T_x0n               ,1     }                           //"x 0.1         "
	,{T_x00n              ,1     }                           //"x 0.01        "
	,{T_x000n             ,1     }                           //"x0.001        "
	,{T_x0000n            ,1     }                           //"x0.0001       "
};


static const S_MSG_TYPE t_astLoadSpdUnit[MSG_COUNT_LOADSPDUNIT] = {           //MSG_LoadSpdUnit     //
	 {T_rpm               ,0xFF  }                           //"rpm           "
	,{T_mpm               ,0xFF  }                           //"mpm           "
};


static const S_MSG_TYPE t_astInvIpType[MSG_COUNT_INVIPTYPE] = {               //MSG_InvIpType       //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_IP54              ,0xFF  }                           //"IP54          "
};


static const S_MSG_TYPE t_astPwmModeType[MSG_COUNT_PWMMODETYPE] = {           //MSG_PwmModeType     //
	 {T_NormalPWM         ,0xFF  }                           //"Normal PWM    "
	,{T_LowLeakagePWM     ,0xFF  }                           //"LowLeakage PWM"
};


static const S_MSG_TYPE t_astFBusBRate[MSG_COUNT_FBUSBRATE] = {               //MSG_FBusBRate       //
	 {T_nnn00bps          ,96    }                           //" 9600 bps     "
	,{T_nnn00bps          ,192   }                           //"19200 bps     "
	,{T_38400bps          ,0xFF  }                           //"38400 bps     "
	,{T_nnnKbps           ,56    }                           //" 56Kbps       "
	,{T_768Kbps           ,0xFF  }                           //"76.8Kbps      "
	,{T_nnnKbps           ,112   }                           //"112Kbps       "
	,{T_nnnKbps           ,125   }                           //"125Kbps       "
	,{T_nnnKbps           ,250   }                           //"250Kbps       "
	,{T_nnn0Kbps          ,50    }                           //" 500Kbps      "
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_nnnMbps           ,1     }                           //"  1Mbps       "
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_nnnMbps           ,5     }                           //"  5Mbps       "
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
	,{T_nnnMbps           ,10    }                           //" 10Mbps       "
	,{T_Reserved          ,0xFF  }                           //"-- Reserved --"
};


static const S_MSG_TYPE t_astSsModeType[MSG_COUNT_SSMODETYPE] = {             //MSG_SsModeType      //
	 {T_FlyingStartn      ,1     }                           //"Flying Start-1"
	,{T_FlyingStartn      ,2     }                           //"Flying Start-2"
};


static const S_MSG_TYPE t_astStallSrcMsg_X[MSG_COUNT_STALLSRCMSG_X] = {       //MSG_StallSrcMsg_X   //
	 {T_Keypad            ,0xFF  }                           //"Keypad        "
	,{T_AnalogInnn        ,1     }                           //"Analog In 1   "
	,{T_AnalogInnn        ,2     }                           //"Analog In 2   "
	,{T_Pulse             ,0xFF  }                           //"Pulse         "
};


static const S_MSG_TYPE t_astTripStop1Mode[MSG_COUNT_TRIPSTOP1MODE] = {       //MSG_TripStop1Mode   //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_FreeRun           ,0xFF  }                           //"Free-Run      "
	,{T_Dec               ,0xFF  }                           //"Dec           "
	,{T_Warning           ,0xFF  }                           //"Warning       "
	,{T_LostPreset        ,0xFF  }                           //"Lost Preset   "
};


static const S_MSG_TYPE t_astTripStop2Mode[MSG_COUNT_TRIPSTOP2MODE] = {       //MSG_TripStop2Mode   //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_FreeRun           ,0xFF  }                           //"Free-Run      "
	,{T_Dec               ,0xFF  }                           //"Dec           "
	,{T_HoldInput         ,0xFF  }                           //"Hold Input    "
	,{T_HoldOutput        ,0xFF  }                           //"Hold Output   "
	,{T_LostPreset        ,0xFF  }                           //"Lost Preset   "
};


static const S_MSG_TYPE t_astTripMode[MSG_COUNT_TRIPMODE] = {                 //MSG_TripMode        //
	 {T_None              ,0xFF  }                           //"None          "
	,{T_Trip              ,0xFF  }                           //"Trip          "
	,{T_Warning           ,0xFF  }                           //"Warning       "
};


static const S_MSG_TYPE t_astAdcInputType[MSG_COUNT_ADCINPUTTYPE] = {         //MSG_AdcInputType    //
	 {T_Unipolar          ,0xFF  }                           //"Unipolar      "
	,{T_Bipolar           ,0xFF  }                           //"Bipolar       "
};


static const S_MSG_TYPE t_astRotaryEncInLineType[MSG_COUNT_ROTARYENCINLINETYPE] = {//MSG_RotaryEncInLineType//
	 {T_AB                ,0xFF  }                           //"(A + B)       "
	,{T_MAB               ,0xFF  }                           //"-(A + B)      "
	,{T_A                 ,0xFF  }                           //"( A )         "
};


static const S_MSG_TYPE t_astRotaryEncInputType[MSG_COUNT_ROTARYENCINPUTTYPE] = {//MSG_RotaryEncInputType//
	 {T_LineDriver        ,0xFF  }                           //"Line Driver   "
	,{T_TotemorCom        ,0xFF  }                           //"Totem or Com  "
	,{T_OpenCollect       ,0xFF  }                           //"Open Collect  "
};
          
static const S_MSG_TYPE * t_pastMsgDataTbl[MSG_TOTAL] = {
	 t_astYesNO
	,t_astTimeScale
	,t_astInitGrp
	,t_astRunCmdSrc
	,t_astFreqRefSrc2
	,t_astTorqueSrc
	,t_astFreqRefSrc1
	,t_astXcelCurve
	,t_astStartMode
	,t_astXcelFreqMode
	,t_astBoostMode
	,t_astVfMode
	,t_astInt485BRate
	,t_astMotCooling
	,t_astInvCap
	,t_astCtrlMode
	,t_astAoMode
	,t_astDiMode
	,t_astDoMode
	,t_astMotCap
	,t_astDnOutInst
	,t_astDnInInst
	,t_astRunPrevent
	,t_astLostAiChkLvl
	,t_astmodbusMsg_X
	,t_astAppMode
	,t_astAutoTuneMode
	,t_astStopMode
	,t_astFanCtrlMode
	,t_astLoadDutyMsg_X
	,t_astMotSpdUnit
	,t_astInt485CharForm
	,t_astAnalogInSrc
	,t_astLoHiSel
	,t_astOptName
	,t_astAdcAdjustInLv
	,t_astTermiAIType
	,t_astAuxCalcType
	,t_astMonitorPara
	,t_astEsaveMsg_X
	,t_astMacroType
	,t_astInvStateType
	,t_astInVoltFreq
	,t_astTripName
	,t_astRunEnableType
	,t_astRunDisStopMode
	,t_astWarningName
	,t_astAutoTuneSeq
	,t_astPIDUnitScale
	,t_astFeedbackSrc
	,t_astPIDOutputMode
	,t_astPIDUnit
	,t_astProcPIDCtrlMode
	,t_astFuncRunMode
	,t_astReferenceSrc
	,t_astLoadSpdScale
	,t_astLoadSpdUnit
	,t_astInvIpType
	,t_astPwmModeType
	,t_astFBusBRate
	,t_astSsModeType
	,t_astStallSrcMsg_X
	,t_astTripStop1Mode
	,t_astTripStop2Mode
	,t_astTripMode
	,t_astAdcInputType
	,t_astRotaryEncInLineType
	,t_astRotaryEncInputType
};


static const WORD t_awMsgDataSize[MSG_TOTAL] = {
	 MSG_COUNT_YESNO
	,MSG_COUNT_TIMESCALE
	,MSG_COUNT_INITGRP
	,MSG_COUNT_RUNCMDSRC
	,MSG_COUNT_FREQREFSRC2
	,MSG_COUNT_TORQUESRC
	,MSG_COUNT_FREQREFSRC1
	,MSG_COUNT_XCELCURVE
	,MSG_COUNT_STARTMODE
	,MSG_COUNT_XCELFREQMODE
	,MSG_COUNT_BOOSTMODE
	,MSG_COUNT_VFMODE
	,MSG_COUNT_INT485BRATE
	,MSG_COUNT_MOTCOOLING
	,MSG_COUNT_INVCAP
	,MSG_COUNT_CTRLMODE
	,MSG_COUNT_AOMODE
	,MSG_COUNT_DIMODE
	,MSG_COUNT_DOMODE
	,MSG_COUNT_MOTCAP
	,MSG_COUNT_DNOUTINST
	,MSG_COUNT_DNININST
	,MSG_COUNT_RUNPREVENT
	,MSG_COUNT_LOSTAICHKLVL
	,MSG_COUNT_MODBUSMSG_X
	,MSG_COUNT_APPMODE
	,MSG_COUNT_AUTOTUNEMODE
	,MSG_COUNT_STOPMODE
	,MSG_COUNT_FANCTRLMODE
	,MSG_COUNT_LOADDUTYMSG_X
	,MSG_COUNT_MOTSPDUNIT
	,MSG_COUNT_INT485CHARFORM
	,MSG_COUNT_ANALOGINSRC
	,MSG_COUNT_LOHISEL
	,MSG_COUNT_OPTNAME
	,MSG_COUNT_ADCADJUSTINLV
	,MSG_COUNT_TERMIAITYPE
	,MSG_COUNT_AUXCALCTYPE
	,MSG_COUNT_MONITORPARA
	,MSG_COUNT_ESAVEMSG_X
	,MSG_COUNT_MACROTYPE
	,MSG_COUNT_INVSTATETYPE
	,MSG_COUNT_INVOLTFREQ
	,MSG_COUNT_TRIPNAME
	,MSG_COUNT_RUNENABLETYPE
	,MSG_COUNT_RUNDISSTOPMODE
	,MSG_COUNT_WARNINGNAME
	,MSG_COUNT_AUTOTUNESEQ
	,MSG_COUNT_PIDUNITSCALE
	,MSG_COUNT_FEEDBACKSRC
	,MSG_COUNT_PIDOUTPUTMODE
	,MSG_COUNT_PIDUNIT
	,MSG_COUNT_PROCPIDCTRLMODE
	,MSG_COUNT_FUNCRUNMODE
	,MSG_COUNT_REFERENCESRC
	,MSG_COUNT_LOADSPDSCALE
	,MSG_COUNT_LOADSPDUNIT
	,MSG_COUNT_INVIPTYPE
	,MSG_COUNT_PWMMODETYPE
	,MSG_COUNT_FBUSBRATE
	,MSG_COUNT_SSMODETYPE
	,MSG_COUNT_STALLSRCMSG_X
	,MSG_COUNT_TRIPSTOP1MODE
	,MSG_COUNT_TRIPSTOP2MODE
	,MSG_COUNT_TRIPMODE
	,MSG_COUNT_ADCINPUTTYPE
	,MSG_COUNT_ROTARYENCINLINETYPE
	,MSG_COUNT_ROTARYENCINPUTTYPE
};

static S_MSG_TYPE KpdParaGetMsg(const S_MSG_TYPE astMsgType[], WORD wMsgNum)
{
	return astMsgType[wMsgNum];
}

S_MSG_TYPE KpdParaGetMsgData(WORD wMsgIdx, WORD wMsgNum)
{
	return KpdParaGetMsg(t_pastMsgDataTbl[wMsgIdx], wMsgNum);
}


WORD KpdParaGetMsgSize(WORD wMsgIdx)
{
	return t_awMsgDataSize[wMsgIdx];
}


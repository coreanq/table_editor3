/***********************************************
// TABLE EDITOR 3 : 인버터 파라메터 변수 선언
***********************************************/
    
    
#ifndef KPD_PARA_VARI_H
#define KPD_PARA_VARI_H
    
#define K_AWACCTIME                     5
#define K_AWADCCALIBRATIONMAX           3
#define K_AWADCCALIBRATIONMIN           3
#define K_AWADCINPUTTYPE                3
#define K_AWAOBIAS                      2
#define K_AWAOCONST                     2
#define K_AWAOGAIN                      2
#define K_AWAOLPFGAIN                   2
#define K_AWAOMODE                      2
#define K_AWAOOUTPERC                   2
#define K_AWBASEFREQ                    2
#define K_AWCMDREFSRC                   2
#define K_AWCOMMCTRLADDR                16
#define K_AWCOMMSTSADDR                 16
#define K_AWCONTROLMETHOD               2
#define K_AWCUTOFFCARRIERFREQ           2
#define K_AWDECTIME                     5
#define K_AWDERATECARRIER               4
#define K_AWDERATETEMPER                3
#define K_AWETH1MINPERC                 2
#define K_AWETHCONTPERC                 2
#define K_AWFREQREFSRC                  2
#define K_AWFWDBOOST                    2
#define K_AWINERTIARATE                 2
#define K_AWJUMPHIFREQ                  3
#define K_AWJUMPID                      17
#define K_AWJUMPLOFREQ                  3
#define K_AWLOADSPDGAIN                 2
#define K_AWLOADSPDSCALE                2
#define K_AWLOADSPDUNIT                 2
#define K_AWMOTCAP                      2
#define K_AWMOTEFFICPERC                2
#define K_AWMOTNOLOADCURR               2
#define K_AWMOTPARALS                   2
#define K_AWMOTPARALSIGMA               2
#define K_AWMOTPARARSOHM                2
#define K_AWMOTPARATR                   2
#define K_AWMOTPOLENUM                  2
#define K_AWMOTVOLT                     2
#define K_AWOPTPARA                     16
#define K_AWPHYTERMIINMODE              16
#define K_AWPHYTERMIOUTMODE             8
#define K_AWPROCPIDDTIME                2
#define K_AWPROCPIDITIME                2
#define K_AWPROCPIDPGAIN                2
#define K_AWPROCPIDREFAUXCALCFUNC       2
#define K_AWPROCPIDREFAUXGAIN           2
#define K_AWPROCPIDREFAUXSRC            2
#define K_AWPROCPIDREFKPDSETPOINT       2
#define K_AWPROCPIDREFSRC               2
#define K_AWPROCPIDSLEEPCHECKLEVEL      2
#define K_AWPROCPIDSLEEPCHECKTIME       2
#define K_AWPROCPIDSTEPREF              7
#define K_AWPROCPIDWAKEUPCHECKLEVEL     2
#define K_AWPROCPIDWAKEUPCHECKTIME      2
#define K_AWRATEDCURR                   2
#define K_AWRATEDSLIPRPM                2
#define K_AWREVBOOST                    2
#define K_AWSTALLFREQ                   4
#define K_AWSTALLPERC                   4
#define K_AWSTEPTARFREQ                 15
#define K_AWTERMIAILPFGAIN              2
#define K_AWTERMIAIMON                  2
#define K_AWTERMIAIMONPERC              2
#define K_AWTERMIAINEGHILMT             2
#define K_AWTERMIAINEGHIPERC            2
#define K_AWTERMIAINEGLOLMT             2
#define K_AWTERMIAINEGLOPERC            2
#define K_AWTERMIAIPORTTYPE             2
#define K_AWTERMIAIPOSHILMT             2
#define K_AWTERMIAIPOSHIPERC            2
#define K_AWTERMIAIPOSLOLMT             2
#define K_AWTERMIAIPOSLOPERC            2
#define K_AWTERMIAIQUANTIZINGUNIT       2
#define K_AWTRQREFSRC                   2
#define K_AWUSERVFFREQ                  4
#define K_AWUSERVFVOLT                  4
#define K_AWVFMODE                      2
#define K_AWVRTTERMIINMODE              16



extern WORD                          //WORD TYPE의 변수들
 k_awAccTime[K_AWACCTIME]                          //
,k_awAdcCalibrationMax[K_AWADCCALIBRATIONMAX]      //
,k_awAdcCalibrationMin[K_AWADCCALIBRATIONMIN]      //
,k_awAdcInputType[K_AWADCINPUTTYPE]                //
,k_awAoBias[K_AWAOBIAS]                            //2009/04/22 LBK EXTIO2
,k_awAoConst[K_AWAOCONST]                          //2009/04/22 LBK EXTIO2
,k_awAoGain[K_AWAOGAIN]                            //2009/04/22 LBK EXTIO2
,k_awAoLpfGain[K_AWAOLPFGAIN]                      //2009/04/22 LBK EXTIO2
,k_awAoMode[K_AWAOMODE]                            //2009/04/22 LBK EXTIO2
,k_awAoOutPerc[K_AWAOOUTPERC]                      //2009/04/22 LBK EXTIO2
,k_awBaseFreq[K_AWBASEFREQ]                        //
,k_awCmdRefSrc[K_AWCMDREFSRC]                      //
,k_awCommCtrlAddr[K_AWCOMMCTRLADDR]                //2005.11.22 LBK 16개로 확장
,k_awCommStsAddr[K_AWCOMMSTSADDR]                  //2005.11.22 LBK 16개로 확장
,k_awControlMethod[K_AWCONTROLMETHOD]              //변수설명
,k_awCutOffCarrierFreq[K_AWCUTOFFCARRIERFREQ]      //변수설명
,k_awDecTime[K_AWDECTIME]                          //
,k_awDerateCarrier[K_AWDERATECARRIER]              //변수설명
,k_awDerateTemper[K_AWDERATETEMPER]                //변수설명
,k_awEth1MinPerc[K_AWETH1MINPERC]                  //
,k_awEthContPerc[K_AWETHCONTPERC]                  //
,k_awFreqRefSrc[K_AWFREQREFSRC]                    //
,k_awFwdBoost[K_AWFWDBOOST]                        //
,k_awInertiaRate[K_AWINERTIARATE]                  //변수설명
,k_awJumpHiFreq[K_AWJUMPHIFREQ]                    //
,k_awJumpId[K_AWJUMPID]                            //2009/04/22 LBK EXTIO2
,k_awJumpLoFreq[K_AWJUMPLOFREQ]                    //
,k_awLoadSpdGain[K_AWLOADSPDGAIN]                  //로드스피드개인..
,k_awLoadSpdScale[K_AWLOADSPDSCALE]                //로드스피드크기
,k_awLoadSpdUnit[K_AWLOADSPDUNIT]                  //로드스피드단위
,k_awMotCap[K_AWMOTCAP]                            //PJW 2005/02/22
,k_awMotEfficPerc[K_AWMOTEFFICPERC]                //변수설명
,k_awMotNoloadCurr[K_AWMOTNOLOADCURR]              //PJW 2005/02/22
,k_awMotParaLs[K_AWMOTPARALS]                      //PJW 2005/02/23
,k_awMotParaLSigma[K_AWMOTPARALSIGMA]              //PJW 2005/02/23
,k_awMotParaRsOhm[K_AWMOTPARARSOHM]                //PJW 2005/02/23
,k_awMotParaTr[K_AWMOTPARATR]                      //PJW 2005/02/23
,k_awMotPoleNum[K_AWMOTPOLENUM]                    //PJW 2005/02/22
,k_awMotVolt[K_AWMOTVOLT]                          //PJW 2005/02/22
,k_awOptPara[K_AWOPTPARA]                          //변수설명
,k_awPhyTermiInMode[K_AWPHYTERMIINMODE]            //변수설명
,k_awPhyTermiOutMode[K_AWPHYTERMIOUTMODE]          //2009/04/22 LBK EXTIO2 Digital 출력 정리
,k_awProcPIDDTime[K_AWPROCPIDDTIME]                //Proc PID의 D Time 값 msec
,k_awProcPIDITime[K_AWPROCPIDITIME]                //Proc PID의 I Time 값 sec
,k_awProcPIDPGain[K_AWPROCPIDPGAIN]                //Proc PID의 Gain값 %
,k_awProcPIDRefAuxCalcFunc[K_AWPROCPIDREFAUXCALCFUNC]//Proc PID의 Reference Aux에서 연산식 선택
,k_awProcPIDRefAuxGain[K_AWPROCPIDREFAUXGAIN]      //Proc PID의 Reference Aux Gain 값
,k_awProcPIDRefAuxSrc[K_AWPROCPIDREFAUXSRC]        //Proc PID의 Reference Aux값 Source
,k_awProcPIDRefKpdSetpoint[K_AWPROCPIDREFKPDSETPOINT]//Proc PID에서 Reference Source가 Keypad인 경우의 Reference 값
,k_awProcPIDRefSrc[K_AWPROCPIDREFSRC]              //Proc PID에서 사용되는 Reference Source
,k_awProcPIDSleepCheckLevel[K_AWPROCPIDSLEEPCHECKLEVEL]//Proc PID에서 Sleep Mode로 들어가기 위한 Check Level, PID 출력을 기준으로 함.
,k_awProcPIDSleepCheckTime[K_AWPROCPIDSLEEPCHECKTIME]//Proc PID에서 Sleep Mode로 들어가기 위한 Check Time
,k_awProcPIDStepRef[K_AWPROCPIDSTEPREF]            //Proc PID Reference에서 Step Reference값
,k_awProcPIDWakeUpCheckLevel[K_AWPROCPIDWAKEUPCHECKLEVEL]//Proc PID에서 WakeUp 하기 위한 Check Level, PID Feedback값을 기준으로 함.
,k_awProcPIDWakeUpCheckTime[K_AWPROCPIDWAKEUPCHECKTIME]//Proc PID에서 Wake Up 하기 위한 Check Level 유지 시간.
,k_awRatedCurr[K_AWRATEDCURR]                      //
,k_awRatedSlipRPM[K_AWRATEDSLIPRPM]                //변수설명
,k_awRevBoost[K_AWREVBOOST]                        //
,k_awStallFreq[K_AWSTALLFREQ]                      //
,k_awStallPerc[K_AWSTALLPERC]                      //
,k_awStepTarFreq[K_AWSTEPTARFREQ]                  //
,k_awTermiAiLpfGain[K_AWTERMIAILPFGAIN]            //
,k_awTermiAiMon[K_AWTERMIAIMON]                    //
,k_awTermiAiMonPerc[K_AWTERMIAIMONPERC]            //
,k_awTermiAiNegHiLmt[K_AWTERMIAINEGHILMT]          //
,k_awTermiAiNegHiPerc[K_AWTERMIAINEGHIPERC]        //
,k_awTermiAiNegLoLmt[K_AWTERMIAINEGLOLMT]          //
,k_awTermiAiNegLoPerc[K_AWTERMIAINEGLOPERC]        //
,k_awTermiAiPortType[K_AWTERMIAIPORTTYPE]          //
,k_awTermiAiPosHiLmt[K_AWTERMIAIPOSHILMT]          //
,k_awTermiAiPosHiPerc[K_AWTERMIAIPOSHIPERC]        //
,k_awTermiAiPosLoLmt[K_AWTERMIAIPOSLOLMT]          //
,k_awTermiAiPosLoPerc[K_AWTERMIAIPOSLOPERC]        //
,k_awTermiAiQuantizingUnit[K_AWTERMIAIQUANTIZINGUNIT]//
,k_awTrqRefSrc[K_AWTRQREFSRC]                      //
,k_awUserVfFreq[K_AWUSERVFFREQ]                    //
,k_awUserVfVolt[K_AWUSERVFVOLT]                    //
,k_awVFMode[K_AWVFMODE]                            //
,k_awVrtTermiInMode[K_AWVRTTERMIINMODE]            //변수설명
,k_w100Perc2Freq                                   //
,k_w100Perc2Trq                                    //
,k_w2ndMotStallPerc                                //
,k_wAccDwellFreq                                   //Dwell 운전 주파수 1
,k_wAccDwellTime                                   //변수설명
,k_wAccMode                                        //
,k_wAcrIGain                                       //
,k_wAcrPGain                                       //
,k_wAdcCalibCalcAdjustSel                          //
,k_wAdcCalibrationAdjustChNo                       //
,k_wAhrIGain                                       //
,k_wAhrLimitPerc                                   //
,k_wAhrPGain                                       //
,k_wAiAdjustCh                                     //
,k_wAILostLevelMode                                //
,k_wAnalogBand                                     //
,k_wAppMode                                        //
,k_wAsrGainSwDelay                                 //
,k_wAsrGainSwFreq                                  //
,k_wAsrIGain                                       //
,k_wAsrIGain2                                      //
,k_wAsrPGain                                       //
,k_wAsrPGain2                                      //sgf
,k_wAsrRefLpfGain                                  //
,k_wAsrSLIGain                                     //
,k_wAsrSLIGain2                                    //
,k_wAsrSLPGain                                     //변수설명
,k_wAsrSLPGain2                                    //변수설명
,k_wAutoTuneMode                                   //
,k_wAuxCalcType                                    //변수설명
,k_wAuxRefGain                                     //변수설명
,k_wAuxRefSrc                                      //
,k_wAvrMode                                        //
,k_wBinaryInputNum                                 //
,k_wBinaryInputType                                //
,k_wBoostMode                                      //
,k_wBoostTensionIn                                 //
,k_wBrkEngageDlyTime                               //
,k_wBrkEngageFreq                                  //변수설명
,k_wBrkRlsCurrPerc                                 //
,k_wBrkRlsDlyTime                                  //
,k_wBrkRlsFwdFreq                                  //
,k_wBrkRlsRevFreq                                  //
,k_wCarrierFreq                                    //
,k_wCommCtrlParaNum                                //변수설명
,k_wCommOptReset                                   //2006.07.24통신RESET
,k_wCommRespDelay                                  //
,k_wCommStsParaNum                                 //변수설명
,k_wContRateAdjust                                 //변수설명
,k_wCurrIGain                                      //
,k_wCurrIGainNewFS                                 //PJW 2009/03/11
,k_wCurrPGain                                      //
,k_wCurrPGainNewFS                                 //PJW 2009/03/11
,k_wCurrSlope                                      //
,k_wDbWarnEDPerc                                   //
,k_wDcBlockTime                                    //
,k_wDcbrFreq                                       //
,k_wDcBrkPerc                                      //
,k_wDcBrkTime                                      //
,k_wDcInjPerc                                      //
,k_wDcStartTime                                    //
,k_wDeadBand                                       //
,k_wDeadVolt                                       //
,k_wDecDwellFreq                                   //㉫?Dwell 주파수
,k_wDecDwellTime                                   //감속 Dwell 시간
,k_wDecMode                                        //
,k_wDecTripTime                                    //
,k_wDerateFreq                                     //
,k_wDerateTime                                     //IOLT derate time
,k_wDICheckTime                                    //
,k_wDigiFwdSpdLmt                                  //
,k_wDigiRevSpdLmt                                  //
,k_wDiNcNoSelBits                                  //
,k_wDiOffDelay                                     //
,k_wDiOnDelay                                      //디지탈 입력 지연
,k_wDioTimerOff                                    //
,k_wDioTimerOn                                     //
,k_wDiStatus                                       //
,k_wDnetInInst                                     //
,k_wDnetOutInst                                    //
,k_wDoNcNoSelBits                                  //
,k_wDoOffDelay                                     //
,k_wDoOnDelay                                      //
,k_wDoStatus                                       //// PJW 2008/07/10
,k_wDoTripModeBit                                  //변수설명
,k_wDoTripOffDly                                   //
,k_wDoTripOnDly                                    //
,k_wDroopPerc                                      //
,k_wDroopStartTrq                                  //
,k_wEepTestAddr                                    //
,k_wEepTestData                                    //변수설명
,k_wEncSpeedMonitor                                //
,k_wEncFreqMonitor                                 //
,k_wRotaryEncWireCheckTime                         //Encoder의 Time Check수행
,k_wEncIGain                                       //
,k_wEncLimitPerc                                   //
,k_wEncMode                                        //Reference와 Feedback 모드 설정
,k_wEncPGain                                       //
,k_wEncFilterGain                                  //Encoder용 LowpassFilter
,k_wEnergySaveMode                                 //
,k_wEThTripMode                                    //
,k_wFanControlMode                                 //
,k_wFanTripMode                                    //변수설명
,k_wFBusBRate                                      //필드버스속도
,k_wFBusOptLedState                                //2005.08.25 LBK 필드버스 Led 점멸 표시
,k_wFdtBandFreq                                    //
,k_wFdtFreq                                        //
,k_wFixCarrierSel                                  //
,k_wFluxForcing                                    //
,k_wFluxOverExPerc                                 //// 2007/02/27 KKY 추가
,k_wFreqLmtHigh                                    //
,k_wFreqLmtLow                                     //
,k_wFwdNegTrqLimit                                 //
,k_wFwdPosTrqLimit                                 //
,k_wGoundTTime                                     //wGftPerc대신 wGftTime으로 변경
,k_wGroundTLv                                      //
,k_wHwOcsTime                                      //
,k_wHzRpmUnit                                      //
,k_wInPhsVoltBand                                  //
,k_wInt485BRate                                    //
,k_wInt485CharForm                                 //
,k_wInt485Protocol                                 //
,k_wInt485StationID                                //
,k_wInvCapIndex                                    //
,k_wInvCodeVer                                     //2005.05.13 LBK 코드버전
,k_wInvDebugVer                                    //인버터 디버그 버전
,k_wInverterType                                   //IP54Type 2005.07.29
,k_wInvTemper                                      //변수설명
,k_wIOLT200Time                                    //IOLT 200%정격 시간
,k_wJogAccTime                                     //변수설명
,k_wJogDecTime                                     //
,k_wJogTarFreq                                     //
,k_wJumpFreqSel                                    //
,k_wKEBGain                                        //
,k_wKebSel                                         //KEB선택변수
,k_wKEBStartLv                                     //
,k_wKEBStopLv                                      //
,k_wKpdTarFreq                                     //
,k_wKpdTarTrq                                      //
,k_wLimitFreqSel                                   //
,k_wLoopMaxTime                                    //
,k_wLoopMeanTime                                   //
,k_wLostAnaInChkMode                               //
,k_wLostAnaInChkPortSel                            //
,k_wLostAnaInChkTime                               //
,k_wLostAnaInTripMode                              //
,k_wLostIntCommChkTime                             //
,k_wLostIntCommTripMode                            //
,k_wLostKpdTripMode                                //Keypad가 떨어 졌을때 취하는 행동들 정의
,k_wLostPresetFreq                                 //
,k_wLvTripDetectDly                                //
,k_wMakTripOffBit                                  //
,k_wMaxDelFreqDec                                  //변수설명
,k_wMaxFreq                                        //
,k_wMaxFreqDrtPerc                                 //변수설명
,k_wMotCoolMode                                    //
,k_wNoMotChkTime                                   //변수설명
,k_wNoMotLv                                        //변수설명
,k_wNoMotTripMode                                  //변수설명
,k_wNotSaveYesNoVari                               //
,k_wObserverGain                                   //
,k_wObserverGain2                                  //변수설명
,k_wObserverGain3                                  //변수설명
,k_wOcsIGain                                       //
,k_wOcsPGain                                       //
,k_wOlLevel                                        //
,k_wOlTime                                         //
,k_wOltLevel                                       //
,k_wOLTripMode                                     //
,k_wOltTime                                        //
,k_wOlWarnMode                                     //
,k_wOnOffCtrlOffLv                                 //
,k_wOnOffCtrlOnLv                                  //
,k_wOnOffCtrlSrc                                   //
,k_wOptCommSwVer                                   //
,k_wOptFBusMacID                                   //
,k_wOptTripMode                                    //옵션 트립모드
,k_wOverloadDuty                                   //
,k_wOverSpdLevel                                   //변수설명
,k_wOverSpdTime                                    //변수설명
,k_wOvmModeSel                                     //over-modulation PWM mode 선택
,k_wOvmPercSL2                                     //// PJW 2008/07/10
,k_wPhsLossTripBit                                 //
,k_wPreExTime                                      //
,k_wProcPIDCtrlMode                                //PID Control mode 설정 변수
,k_wProcPIDCtrlSts                                 //Proc PID의 제어 상태를 나타내는 Bit값
,k_wProcPIDDeadbandDelay                           //Proc PID의 Deadband 지연 시간
,k_wProcPIDDeadbandWidth                           //Proc PID의 Deadband 범위
,k_wProcPIDErrValue                                //Proc PID의 Error값 Unit설정 값으로 표시
,k_wProcPIDFdbAuxCalcFunc                          //Proc PID의 Feedback Aux 연산식 선택
,k_wProcPIDFdbAuxGain                              //Proc PID의 Feedback Aux Gain 값
,k_wProcPIDFdbAuxSrc                               //Proc PID의 Feedback Aux 값 Source
,k_wProcPIDFdbSrc                                  //Proc PID의 Feedback Source
,k_wProcPIDFdbValue                                //Proc PID에 최종 입력되는 Feedback값 Unit설정 값으로 표시
,k_wProcPIDFFGain                                  //Proc PID의 Feed Forward Gain값 %
,k_wProcPIDLimitHi                                 //Proc PID 출력값 상위 리미트
,k_wProcPIDLimitLo                                 //Proc PID 출력값 하위 리미트
,k_wProcPIDOutputInv                               //Proc PID의 Output Error 연산 방법 설정
,k_wProcPIDOutputLpfGain                           //Proc PID의 Output의 Lowpass Filter Gain값
,k_wProcPIDOutputMode                              //Proc PID의 출력값을 주파수화 하는 방법
,k_wProcPIDOutputValue                             //Proc PID의 출력 값 %로 표시
,k_wProcPIDOutScale                                //Proc PID의 Output Scale 값
,k_wProcPIDPrePIDDelayTime                         //Pre PID 출력값 상태에서 일정 속도를 유지하는 시간.
,k_wProcPIDPrePIDOutFreq                           //Pre PID상태에서 PID Mode 출력 값
,k_wProcPIDRefAccTime                              //Proc PID Reference값의 0%에서 100% 증가 시간
,k_wProcPIDRefDecTime                              //Proc PID Reference값의 100%에서 0% 감소 시간
,k_wProcPIDRefValue                                //Proc PID에 최종 입력되는 Reference값 Unit설정 값으로 표시
,k_wProcPIDSleepBoostLevel                         //Proc PID에서 Sleep Boost 상태에서의 PID 출력 양
,k_wProcPIDSleepBoostSetpoint                      //Proc PID에서 Sleep Boost 기준 Feedback 값
,k_wProcPIDSleepBoostTime                          //Proc PID에서 Sleep Boost 동작 시간
,k_wProcPIDSleepMode                               //Proc PID에서 Sleep Mode 설정
,k_wProcPIDSoftFillCheckPoint                      //Proc PID에서 Soft Fill Mode를 탈출 하기 위한 Level.
,k_wProcPIDSoftFillFdbDiff                         //Proc PID Soft Fill Step을 증가 시키기 위한 Feedback Level값
,k_wProcPIDSoftFillStepPoint                       //Proc PID Soft Fill Mode에서 Reference Step 증가 값
,k_wProcPIDSoftFillStepTime                        //Proc PID Soft Fill Step 유지 시간 이시간중에는 탈출 Level Check를 하지 않음.
,k_wProcPIDSoftStartMode                           //Proc PID에서 Soft Start를 사용할지 결정
,k_wProcPIDUnitAt0Perc                             //Proc PID에서 Precent값이 0%일때의 단위 비래값
,k_wProcPIDUnitAt100Perc                           //Proc PID에서 Precent값이 100%일때의 단위 비래값
,k_wProcPIDUnitScale                               //Proc PID에서 Precent값에 대비한 Scale 설정값
,k_wProcPIDUnitSel                                 //Proc PID에서 사용되는 값의 단위
,k_wPtcInputSrc                                    //
,k_wPtcTripArea                                    //
,k_wPtcTripLevel                                   //
,k_wPtcTripMode                                    //
,k_wPulseMonKHz                                    //
,k_wPulseMonPerc                                   //
,k_wPulseNegHiLmt                                  //
,k_wPulseNegLoPerc                                 //
,k_wPulseNegHiPerc                                 //
,k_wPulseNegLoLmt                                  //
,k_wPulsePosHiLmt                                  //
,k_wPulsePosHiPerc                                 //
,k_wPulsePosLoLmt                                  //
,k_wPulsePosLoPerc                                 //
,k_wPulseLowpassFilter                             //Pulse 출력 필터값
,k_wPulseQuantizeUnit                              //
,k_wPwmModeCmdKpd                                  //
,k_wPwrBrkIGain                                    //변수설명
,k_wPwrBrkPGain                                    //변수설명
,k_wPwrOnStartSel                                  //
,k_wQStopDecTime                                   //변수설명
,k_wRegenAvdDCLimit                                //변수설명
,k_wRegenAvdFreqLimit                              //변수설명
,k_wRegenAvdIgain                                  //
,k_wRegenAvdPgain                                  //
,k_wRegenAvdSel                                    //변수설명
,k_wRevNegTrqLimit                                 //
,k_wRevPosTrqLimit                                 //
,k_wRotaryEncABLineType                            //Rotary Encoder의 입력선 연결 상태
,k_wRotaryEncInSignalType                          //Rotary Encoder의 입력 연결 신호선 Type
,k_wRotaryEncPulseNum                              //Rotary Encoder의 Pulse 입력 수
,k_wRunDisDecMode                                  //변수설명
,k_wRunEnableMode                                  //변수설명
,k_wRunOnDelay                                     //
,k_wRunPreventMode                                 //
,k_wSavePerc                                       //
,k_wSCurvePercAccEnd                               //
,k_wSCurvePercAccStart                             //
,k_wSCurvePercDecEnd                               //
,k_wSCurvePercDecStart                             //
,k_wShowSL2Gain                                    //변수설명
,k_wSpdDevBand                                     //
,k_wSpdDevTripEnSel                                //
,k_wSpdEstIGain                                    //
,k_wSpdEstIGain2                                   //변수설명
,k_wSpdEstPGain                                    //
,k_wSpdEstPGain2                                   //변수설명
,k_wSpdSchAlgorithm                                //PJW 2009/01/15
,k_wSpdSchChkBit                                   //
,k_wSpdTrqAccTime                                  //2005/06/30 KKY 추가
,k_wSpdTrqDecTime                                  //2005/06/30 KKY 추가
,k_wSpeedLmtGain                                   //
,k_wSsBlockTime                                    //
,k_wSsIGain                                        //
,k_wSsPGain                                        //
,k_wSsStallPerc                                    //
,k_wStallChkBit                                    //
,k_wStallPercDisp                                  //PJW 2008/06/13
,k_wStallSrc                                       //PJW 2008/06/13
,k_wStartFrqKPD                                    //
,k_wStartMode                                      //
,k_wStopHoldTime                                   //
,k_wStopMode                                       //
,k_wSwOcsSel                                       //
,k_wSystemFreq                                     //PJW 2005/02/18
,k_wTimeSpdDev                                     //
,k_wTorqueDectBand                                 //
,k_wTorqueDectLevel                                //
,k_wTrimPower                                      //
,k_wTripRstRestart                                 //
,k_wTripRstRetryNum                                //
,k_wTripRstRtyDly                                  //
,k_wTrqBiasFFLv                                    //
,k_wTrqBiasLevel                                   //
,k_wTrqBiasSrc                                     //
,k_wTrqCtrlEnSel                                   //
,k_wTrqLmtSrc                                      //
,k_wTrqOutLpfGain                                  //
,k_wTrqSpdLmtSrc                                   //
,k_wULoadBFLv                                      //
,k_wULoadLFLv                                      //
,k_wULoadTripTime                                  //
,k_wULoadWarnMode                                  //
,k_wULoadWarnTime                                  //
,k_wULTripMode                                     //
,k_wUnlmtCarrFreqSel                               //변수설명
,k_wUpDownSaveMode                                 //
,k_wVac                                            //변수설명
,k_wVConHR                                         //
,k_wVConKi                                         //
,k_wVdcFilterGain                                  //// 2005/07/28 KKY	// 2005/11/30 KKY
,k_wVdcLVTFilterGain                               //
,k_wVdcPerc                                        //
,k_wViewAllCodeSel                                 //모두 보여주는 변수
,k_wVirtualDIStatus                                //// PJW 2008/07/10
,k_wVoltPerc                                       //
,k_wXcelChgFreq                                    //
,k_wXcelFreqMode                                   //
,k_wXcelTimeScale                                  //
,k_wZSpdBand                                       //
,k_wZSpdFreq                                       //
;
    
    
#endif    //KPD_PARA_VARI_H
    

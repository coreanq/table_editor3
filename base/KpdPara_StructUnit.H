#ifndef KPD_PARA_STRUCT_UNIT
#define KPD_PARA_STRUCT_UNIT

enum {
	F_NONE,
	F_DEX0, F_DEX1, F_DEX2, F_DEX3, F_DEX4,
	F_SIG0, F_SIG1, F_SIG2, F_SIG3, F_SIG4,
	F_HEX4, F_HEX8, F_TIME_MIN, F_TWO, F_TIME_YMD, F_TIME_MD,

	F_SP = 0x80,
	F_NOT_TITLE_CHANGE = F_SP,
	F_TITLE_CHANGE,
	F_NOT_TITLE_CHANGE_SIG,
	F_TITLE_CHANGE_SIG,
	F_LONGFORM = 0xA0,
	F_BIT2 = F_LONGFORM, F_BIT3, F_BIT4, F_BIT5, F_BIT6, F_BIT7, F_BIT8,
	F_BIT9, F_BIT10, F_BIT11, F_BIT12, F_BIT13, F_BIT14, F_BIT15, F_BIT16, F_YMDHM, F_RYMDHM, F_VER
};


enum {
	U_NONE, U_PERCENT,U_HZ, U_KHZ, U_SEC,U_MV, U_V, U_KV, U_W, U_KW,U_MW,U_WH,U_KWH,U_MWH, U_B, U_MSEC,
	U_HEX, U_KOHM, U_OHM,U_MOHM, U_RPM,U_TEMP_C,U_A, U_MA,	U_USEC, U_MH,U_H, U_CODE,U_TEMP_F,
	U_MIN,U_HOUR,U_YEAR,U_DAY,U_PW, U_BAR, U_MBAR, U_KPA, U_PA, U_HP, U_KGM, U_NM,U_LOCK,U_MPM,
	U_PSI, U_INWC, U_INM, U_CUST, U_FT, 
	U_MPS, U_M3PS, U_M3PM, U_M3PH, U_LPS, U_LPM, U_LPH,
	U_KGPS, U_KGPM, U_KGPH, U_GALPS, U_GALPM, U_GALPH,
	U_FTPS, U_FT3PS, U_FT3PM, U_FT3PH, U_LBPS, U_LBPM, U_LBPH,
	U_PPM, U_PPS, U_WB,

	U_SP = 0x80,
	U_HZ_RPM, U_HZ_RPM_1ST, U_HZ_RPM_2ND, U_VARI_SEC,
	U_MOT_1ST_SPEC_OHM, U_MOT_1ST_SPEC_MMH, U_MOT_1ST_SPEC_MH,
	U_MOT_2ND_SPEC_OHM, U_MOT_2ND_SPEC_MMH, U_MOT_2ND_SPEC_MH,
	U_PID_VAR_UNIT,	U_VARI_B_IN, U_VARI_B_OUT,

	U_RPM_CHG_DATAMSG = 0xFD,
	U_DATAMSG = 0xFF
};







#define KPD_ATTR_READ_ONLY	0x0008u    		// NO Program flag 
#define KPD_ATTR_NO_CHG_RUN	0x0010u    		// NO CHANGE During runing 
#define KPD_ATTR_ZERO 		0x0020u    		// Zero Edit flag 
#define KPD_ATTR_NOCOM 		0x0040u    		// Not Communication Parameter 

#define KEYPAD_ID			0x01u
#define SET_INFO_GRP		0x50u

#define CONFIG_ADDR			0xF00u
#define MSG_DISABLE			100u
#define KPD_TITLE_SIZE		14u
#define MSG_END_LINE		0xFFu
#define KPD_TITLE_AT_NONE	0xFFu
#define KPD_GRP_MAX_CODE	99u

#define KPD_CHAR_INV_STS	4u
#define KPD_CMD_SRC_CHAR	2u
#define KPD_REF_SRC_CHAR	2u





typedef struct 
{

	uint8_t		bGrp;				//GrpIndex

	uint8_t		bCodeNum;			// code number

	uint8_t		bCodeIndex;			//CodeIndex

	uint16_t	wTitleIdx;		// LCD entry data

	uint8_t 	bAtValue;

	int32_t		lDefVal;			// default value of function data

	int32_t		lMaxVal;			// high limit value of function data

	int32_t		lMinVal;			// low limit value of function data

	uint8_t 	bFormMsgType;

	uint8_t 	bUnitType;

	uint16_t	wAttr;           	// attribute of function

	int32_t	    lEditData;			//Parameter의 값

} S_KPD_TYPE;



typedef struct {

	uint16_t	wCommAddr;			// enum 형태로 파일에 써지며 실제로 comm address 값을 가진다.  

	uint16_t	wTitleIdx;			// LCD entry data

	uint8_t		bAtValue;

	uint8_t 	bFloatScale;

	uint8_t 	bUint16Scale;

	int32_t		lDefData;			// default value 

	int32_t		lMaxData;			// high limit value 

	int32_t		lMinData;			// low limit value 

	bool 		blIsReadOnly;

	bool 		blDontChangeWhenRunning;

	bool 		blIsZeroInputPossible;

	bool 		blIsNoCommPara;

	uint8_t		bFormMsgType;		// word float scale 중복 부분 제거 필요 

	uint8_t		bUnitType;

	uint16_t    wHex16btiCommAddr;       // hex 로 표현되는 16bit comm address

	uint16_t    wHex32bitCommAddr;       // hex 로 표현되는 32bit comm address

} S_TABLE_X_TYPE;				



typedef struct
{
	uint16_t	wTitleIdx;
	uint8_t		bAtValue;

}S_MSG_TYPE;       



typedef struct {
	uint16_t	wGrpTitle;
	uint16_t    wStartIndex; // 전체 배열상에서 그룹이 시작하는 시작 index
	uint8_t		bGrpSize;

} S_GROUP_X_TYPE;


#endif		// KPD_PARA_STRUCT_UNIT
















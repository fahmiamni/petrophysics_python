import sys
import datetime
import TechlogDialog as dlg
import TechlogStat as ts

db.objectApplyModeChange(winId,1)

if pythonEditor:
	TechlogDialog.critical('PEP Error','This script should only be run within a workflow')
	exit(0)

def dependency():
	from pep_dependency_b_June2020 import updateParameterDict
	updateParameterDict(parameterDict)

unitsys = db.unitSystem()
w = DEPTH.wellName()
d = DEPTH.datasetName()
u = db.variableUnit(w,d,"DEPTH")
ListIS = db.interactiveSelection(w,d)
frmCnt = len(DEPTH.values())

loopSize = frmCnt
loopRange = range(loopSize)

# Internal Dictionary
pepParameterDict = {}

for paramName in ['POR_AVG', 'R_GRAIN', 'R_EFF', 'M', 'POB', 'PF', 'RSVR_DEPTH', 'GWC_DEPTH', 'GOC_DEPTH', 'OWC_DEPTH', 'GAS_GRAD', 'OIL_GRAD', 'WTR_GRAD',
                  'EXT_RTSHF_LOG', 'EXT_INPUT_LOG_FOR_SWIR', 'EXT_PERM_LOG', 'EXT_RCKTYP_LOG', 'EXT_INDIC_LOG',
                  'SCOSTG', 'SCOSTO', 'BO_CHOO']:
	values = []
	if paramName+'_NUMBER' in locals():
		values = eval(paramName+'_NUMBER'+'.values()')
	elif paramName in locals():
		values = [eval(paramName) for i in range(frmCnt)]
	pepParameterDict[paramName] = values[:]


#if d <> "PEP":
	#text1 = "Use PEP ,instead of "+d+", as default dataset for this workflow !"
	#dlg.critical("PEP Module Error",text1)
	#exit(0)
	

dllName = "pep_utils_2023.dll"

from ctypes import*
from _ctypes import FreeLibrary
#DynaDLL = cdll.LoadLibrary(os.path.join(db.dirTechlog(), "bin64", dllName))
DynaDLL = cdll.LoadLibrary(os.path.join(db.dirCompany(), "External_DLLs", dllName))

DynaDLL.PEP_Module_B.restype = c_int
DynaDLL.PEP_Module_B.argtypes = [c_double, c_int, POINTER(c_double), POINTER(c_double),\
	POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double),\
	c_wchar_p, c_wchar_p,\
	c_double, c_double, c_double,\
	c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double),\
	c_wchar_p, c_wchar_p, c_wchar_p,\
	POINTER(c_double), c_int, c_double, c_double, c_double,\
	c_double, c_double, c_double, c_double,\
	c_wchar_p, c_wchar_p, c_int, POINTER(c_double),\
	c_double, c_double, c_double, c_double, c_double, c_double,\
	c_double, c_double, c_double, c_double, c_double, c_double,\
	c_double, c_double,\
	c_wchar_p, c_int, POINTER(c_double),\
	c_wchar_p, c_wchar_p,\
	POINTER(c_double), POINTER(c_double), POINTER(c_double),\
	POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double),\
	c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double,\
	c_double, c_double, c_double, c_double, c_double, c_double, c_double,\
	c_wchar_p, c_wchar_p,\
	c_wchar_p,\
	POINTER(c_double), c_double,\
	POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double),\
	POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double),\
	POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	
Md = (c_double * loopSize)(*DEPTH.values())
Tvdss = (c_double * loopSize)(*TVDSS.values())
Phit = (c_double * loopSize)(*PHIT.values())
Phie = (c_double * loopSize)(*PHIE.values())
Vclw = (c_double * loopSize)(*VCLW.values())
Vsilt = (c_double * loopSize)(*VSILT.values())
Vsh_dn = (c_double * loopSize)(*VSH_DN.values())
Vshale = (c_double * loopSize)(*VSHALE.values())
Vcoal = (c_double * loopSize)(*VCOAL.values())

pRSVR_DEPTH = (c_double * loopSize)(*(pepParameterDict['RSVR_DEPTH']))
pPOB = (c_double * loopSize)(*(pepParameterDict['POB']))
pPF = (c_double * loopSize)(*(pepParameterDict['PF']))
pPOR_AVG = (c_double * loopSize)(*(pepParameterDict['POR_AVG']))
pR_GRAIN = (c_double * loopSize)(*(pepParameterDict['R_GRAIN']))
pR_EFF = (c_double * loopSize)(*(pepParameterDict['R_EFF']))
pM = (c_double * loopSize)(*(pepParameterDict['M']))

pEXT_INDIC_LOG = (c_double * loopSize)(*(pepParameterDict['EXT_INDIC_LOG']))
pEXT_RCKTYP_LOG = (c_double * loopSize)(*(pepParameterDict['EXT_RCKTYP_LOG']))
pEXT_PERM_LOG = (c_double * loopSize)(*(pepParameterDict['EXT_PERM_LOG']))
pEXT_INPUT_LOG_FOR_SWIR = (c_double * loopSize)(*(pepParameterDict['EXT_INPUT_LOG_FOR_SWIR']))
pEXT_RTSHF_LOG = (c_double * loopSize)(*(pepParameterDict['EXT_RTSHF_LOG']))

pGWC_DEPTH = (c_double * loopSize)(*(pepParameterDict['GWC_DEPTH']))
pGOC_DEPTH = (c_double * loopSize)(*(pepParameterDict['GOC_DEPTH']))
pOWC_DEPTH = (c_double * loopSize)(*(pepParameterDict['OWC_DEPTH']))
pGAS_GRAD = (c_double * loopSize)(*(pepParameterDict['GAS_GRAD']))
pOIL_GRAD = (c_double * loopSize)(*(pepParameterDict['OIL_GRAD']))
pWTR_GRAD = (c_double * loopSize)(*(pepParameterDict['WTR_GRAD']))

pSCOSTG = (c_double * loopSize)(*(pepParameterDict['SCOSTG']))
pSCOSTO = (c_double * loopSize)(*(pepParameterDict['SCOSTO']))
pBO_CHOO = (c_double * loopSize)(*(pepParameterDict['BO_CHOO']))

#outputs
Perm_ch = (c_double * loopSize)(*[MissingValue]*loopSize)
Rocktype = (c_double * loopSize)(*[MissingValue]*loopSize)
Rtc = (c_double * loopSize)(*[MissingValue]*loopSize)
Perm_trfm = (c_double * loopSize)(*[MissingValue]*loopSize)
M_exp = (c_double * loopSize)(*[MissingValue]*loopSize)
Sw_shf = (c_double * loopSize)(*[MissingValue]*loopSize)
Ht = (c_double * loopSize)(*[MissingValue]*loopSize)
Pc = (c_double * loopSize)(*[MissingValue]*loopSize)
Jfn = (c_double * loopSize)(*[MissingValue]*loopSize)
Rqi = (c_double * loopSize)(*[MissingValue]*loopSize)
Fzi = (c_double * loopSize)(*[MissingValue]*loopSize)
Swirr = (c_double * loopSize)(*[MissingValue]*loopSize)
Swirr_pc_max_oil = (c_double * loopSize)(*[MissingValue]*loopSize)
Swirr_pc_max_gas = (c_double * loopSize)(*[MissingValue]*loopSize)

ret_code = DynaDLL.PEP_Module_B(MissingValue, loopSize, Md, Tvdss,\
		Phit, Phie, Vclw, Vsilt, Vsh_dn, Vshale, Vcoal,\
		PERMCRT, PERM_OPTION,\
		CONST_CHOO, EXPO_CHOO, CLAY_CONS,\
		SILT_CONS, pRSVR_DEPTH, pPOB, pPF, pPOR_AVG, pM, pR_GRAIN, pR_EFF,\
		RTCRT, ROCK_TYPING_METHOD, CUT_OFF_ORDER,\
		pEXT_INDIC_LOG, NZN_ROCKTP, NR_CUT_OFF, RT1_CUT_OFF, RT2_CUT_OFF,\
		RT3_CUT_OFF, RT4_CUT_OFF, RT5_CUT_OFF, RT6_CUT_OFF,\
		TRANSCRT, TRANSTYP, NZN_ROCKTPEXT, pEXT_RCKTYP_LOG,\
		TRANS_A1, TRANS_B1, TRANS_A2, TRANS_B2, TRANS_A3, TRANS_B3,\
		TRANS_A4, TRANS_B4, TRANS_A5, TRANS_B5, TRANS_A6, TRANS_B6,\
		TRANS_A7, TRANS_B7,\
		SHFCRT, NZN_RTSHF, pEXT_RTSHF_LOG,\
		SHF_METHOD, PERM_SOURCE,\
		pEXT_PERM_LOG, pSCOSTG, pSCOSTO,\
		pBO_CHOO, pGWC_DEPTH, pOWC_DEPTH, pGOC_DEPTH, pWTR_GRAD, pOIL_GRAD, pGAS_GRAD,\
		ZA, ZB, JA1, JB1, JA2, JB2, JA3, JB3, JA4, JB4,\
		JA5, JB5, JA6, JB6, JA7, JB7, CUTP1,\
		CONTACT_DEPTH_SOURCE, SWIR_EQU,\
		INPUT_LOG_FOR_SWIR,\
		pEXT_INPUT_LOG_FOR_SWIR, MAX_HEIGHT_OF_SWIR_PC,\
		Perm_ch, Rocktype, Rtc, Perm_trfm, M_exp,\
		Sw_shf, Ht, Pc, Jfn, Rqi, Fzi,\
		Swirr, Swirr_pc_max_oil, Swirr_pc_max_gas)
		
if(ret_code == 0):
	dlg.critical('PEP Module', '*** MODULE EXPIRED !! - CONTACT ADMINISTRATOR ***')
	exit(0)

for loopIterator in loopRange:
	PERM_CH.setValue(loopIterator, Perm_ch[loopIterator])
	PERM_TRFM.setValue(loopIterator, Perm_trfm[loopIterator])
	RTC.setValue(loopIterator, Rtc[loopIterator])
	ROCKTYPE.setValue(loopIterator, Rocktype[loopIterator])
	SW_SHF.setValue(loopIterator, Sw_shf[loopIterator])
	HT.setValue(loopIterator, Ht[loopIterator])
	JFN.setValue(loopIterator, Jfn[loopIterator])
	PC.setValue(loopIterator, Pc[loopIterator])
	RQI.setValue(loopIterator, Rqi[loopIterator])
	FZI.setValue(loopIterator, Fzi[loopIterator])
	SWIRR.setValue(loopIterator, Swirr[loopIterator])
	SWIRR_PC_MAX_OIL.setValue(loopIterator, Swirr_pc_max_oil[loopIterator])
	SWIRR_PC_MAX_GAS.setValue(loopIterator, Swirr_pc_max_gas[loopIterator])
	
	if (PERMCRT == 'YES'):
		M_EXP.setValue(loopIterator, pepParameterDict['M'][loopIterator])
	GRAIN_RAD.setValue(loopIterator, pepParameterDict['R_GRAIN'][loopIterator])
	COMP_FAC.setValue(loopIterator, pepParameterDict['POB'][loopIterator])
	BO_CH.setValue(loopIterator, pepParameterDict['BO_CHOO'][loopIterator])
	SCOSTH_O.setValue(loopIterator, pepParameterDict['SCOSTO'][loopIterator])
	SCOSTH_G.setValue(loopIterator, pepParameterDict['SCOSTG'][loopIterator])

PERM_CH.save(True)
PERM_TRFM.save(True)
RTC.save(True)
ROCKTYPE.save(True)
SW_SHF.save(True)
HT.save(True)
JFN.save(True)
PC.save(True)
RQI.save(True)
FZI.save(True)
SWIRR.save(True)
SWIRR_PC_MAX_OIL.save(True)
SWIRR_PC_MAX_GAS.save(True)
M_EXP.save(True)
GRAIN_RAD.save()
COMP_FAC.save()
BO_CH.save()
SCOSTH_O.save()
SCOSTH_G.save()

if (DisplayLayout=='YES'):
	if (UseGraphicalParameterPicking=='YES'):
		if LITHOLOGY_MODEL == 'SSC':
			Lid = plot.logViewGetIdByName("PEP_SSC_Graphical "+w)
			if Lid==-1:
				if db.objectExists("PEP_SSC_Graphical "+w,db.objectTypeList().index("Layout"),'project'):
					Lid = plot.logViewOpen("Project\\PEP_SSC_Graphical "+w+".xml",'project',0)
				elif db.objectExists("PEP_SSC_Graphical "+w,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_SSC_Graphical "+w+".xml",w,False)
					plot.logViewSave(Lid,"PEP_SSC_Graphical "+w,"Project",0)
				else:
					Lid = plot.logViewApplyTemplate("Company\\PEP_SSC_Graphical.xml",w,False)
					plot.logViewSave(Lid,"PEP_SSC_Graphical "+w,"Project",0)
					
				plot.logViewSetName(Lid,"PEP_SSC_Graphical "+w)
				#if u=="FT" or u=="FEET":
				if (u!="M" and u!="m" and u!="METRES" and u!="METERS" and u!="METER" and u!="meter"):
					plot.logViewSetReferenceUnit(Lid,"FEET")
			else:
				plot.logViewSave(Lid,"PEP_SSC_Graphical "+w,"Project",0)

		if LITHOLOGY_MODEL == "CARB":
			Lid = plot.logViewGetIdByName("PEP_CARB_Graphical "+w)
			if Lid==-1:
				if db.objectExists("PEP_CARB_Graphical "+w,db.objectTypeList().index("Layout"),'project'):
					Lid = plot.logViewOpen("Project\\PEP_CARB_Graphical "+w+".xml",'project',0)
				elif db.objectExists("PEP_CARB_Graphical "+w,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_CARB_Graphical "+w+".xml",w,False)
					plot.logViewSave(Lid,"PEP_CARB_Graphical "+w,"Project",0)
				else:
					Lid = plot.logViewApplyTemplate("Company\\PEP_CARB_Graphical.xml",w,False)
					plot.logViewSave(Lid,"PEP_CARB_Graphical "+w,"Project",0)
				
				plot.logViewSetName(Lid,"PEP_CARB_Graphical "+w)
				#if u=="FT" or u=="FEET":
				if (u!="M" and u!="m" and u!="METRES" and u!="METERS" and u!="METER" and u!="meter"):
					plot.logViewSetReferenceUnit(Lid,"FEET")
			else:
				plot.logViewSave(Lid,"PEP_CARB_Graphical "+w,"Project",0)

	else:
		if LITHOLOGY_MODEL == "SSC":
			Lid = plot.logViewGetIdByName("PEP_SSC_Zonation "+w)
			if Lid==-1:
				if db.objectExists("PEP_SSC_Zonation "+w,db.objectTypeList().index("Layout"),'project'):
					Lid = plot.logViewOpen("Project\\PEP_SSC_Zonation "+w+".xml",'project',0)
				elif db.objectExists("PEP_SSC_Zonation "+w,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_SSC_Zonation "+w+".xml",w,False)
					plot.logViewSave(Lid,"PEP_SSC_Zonation "+w,"Project",0)
				else:
					Lid = plot.logViewApplyTemplate("Company\\PEP_SSC_Zonation.xml",w,False)
					plot.logViewSave(Lid,"PEP_SSC_Zonation "+w,"Project",0)
				
				plot.logViewSetName(Lid,"PEP_SSC_Zonation "+w)
				#if u=="FT" or u=="FEET":
				if (u!="M" and u!="m" and u!="METRES" and u!="METERS" and u!="METER" and u!="meter"):
					plot.logViewSetReferenceUnit(Lid,"FEET")
			else:
				plot.logViewSave(Lid,"PEP_SSC_Zonation "+w,"Project",0)

		if LITHOLOGY_MODEL == "CARB":
			Lid = plot.logViewGetIdByName("PEP_CARB_Zonation "+w)
			if Lid==-1:
				if db.objectExists("PEP_CARB_Zonation "+w,db.objectTypeList().index("Layout"),'project'):
					Lid = plot.logViewOpen("Project\\PEP_CARB_Zonation "+w+".xml",'project',0)
				elif db.objectExists("Project\\PEP_CARB_Zonation "+w,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_CARB_Zonation "+w+".xml",w,False)
					plot.logViewSave(Lid,"PEP_CARB_Zonation "+w,"Project",0)
				else:
					Lid = plot.logViewApplyTemplate("Company\\PEP_CARB_Zonation.xml",w,False)
					plot.logViewSave(Lid,"PEP_CARB_Zonation "+w,"Project",0)
				
				plot.logViewSetName(Lid,"PEP_CARB_Zonation "+w)
				#if u=="FT" or u=="FEET":
				if (u!="M" and u!="m" and u!="METRES" and u!="METERS" and u!="METER" and u!="meter"):
					plot.logViewSetReferenceUnit(Lid,"FEET")
			else:
				plot.logViewSave(Lid,"PEP_CARB_Zonation "+w,"Project",0)



db.datasetPropertyChange(w,'PEP','8------------------------------','Permeability Tab  ####')
val1=str(PERMCRT)
db.datasetPropertyChange(w,'PEP','801)  PERMCRT',val1)
val1=str(PERM_OPTION)
db.datasetPropertyChange(w,'PEP','802)  PERM_OPTION',val1)
val1=str(CLAY_CONS)
db.datasetPropertyChange(w,'PEP','803)  CLAY_CONS',val1)
val1=str(SILT_CONS)
db.datasetPropertyChange(w,'PEP','804)  SILT_CONS',val1)
val1=str(CONST_CHOO)
db.datasetPropertyChange(w,'PEP','805)  CONST_CHOO',val1)
val1=str(EXPO_CHOO)
db.datasetPropertyChange(w,'PEP','806)  EXPO_CHOO',val1)
#val1=str(POR_AVG)
#db.datasetPropertyChange(w,'PEP','807)  POR_AVG',val1)
#val1=str(R_GRAIN)
#db.datasetPropertyChange(w,'PEP','808)  R_GRAIN',val1)
#val1=str(R_EFF)
#db.datasetPropertyChange(w,'PEP','809)  R_EFF',val1)
#val1=str(POB)
#db.datasetPropertyChange(w,'PEP','810)  POB',val1)
#val1=str(PF)
#db.datasetPropertyChange(w,'PEP','811)  PF',val1)
#val1=str(PF)
#db.datasetPropertyChange(w,'PEP','812)  PF',val1)

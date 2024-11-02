import sys
import datetime
import TechlogDialog as dlg
import TechlogStat as ts
from timeit import default_timer as timer

db.__disconnectProjectBrowser
db.objectApplyModeChange(winId,1)

if pythonEditor:
	TechlogDialog.critical('PEP Error','This script should only be run within a workflow')
	exit(0)

def dependency():
	from pep_dependency_a_June2020 import updateParameterDict
	updateParameterDict(parameterDict)

unitsys = db.unitSystem()
w = DEPTH.wellName()
d = DEPTH.datasetName()
u = db.variableUnit(w,d,"DEPTH")
ListIS = db.interactiveSelection(w,d)
frmCnt = len(DEPTH.values())

# Internal Dictionary
pepParameterDict = {} 

if d != "PEP":
	text1 = "Use PEP ,instead of "+d+", as default dataset for this workflow !"
	dlg.critical("PEP Module Error",text1)
	exit(0)

#SSC XPlot initialization
RHOBHCPLOT_FLUID=MissingValue
NPHIHCPLOT_FLUID=MissingValue
RHOBHCPLOT_DRYSD=MissingValue
NPHIHCPLOT_DRYSD=MissingValue
RHOBHCPLOT_DRYSLS=MissingValue
NPHIHCPLOT_DRYSLS=MissingValue
RHOBHCPLOT_DRYCLS=MissingValue
NPHIHCPLOT_DRYCLS=MissingValue
RHOBHCPLOT_WETCLS=MissingValue
NPHIHCPLOT_WETCLS=MissingValue
LINE1_INT = MissingValue
LINE1_GRAD = MissingValue
LINE2_INT = MissingValue
LINE2_GRAD = MissingValue





###################### [3] Storing All Parameters & Logs into Memory (S) ##########################
# This step is quite different between LogLan and Python.
# In LogLan, each parameter was defined many time for each interval that has to be filled by the end user
# The idea here is to have only one definition for each parameter, and change this parameter to a curve in the AWI
# The AWI will then do all the interpolation
#-------------- Storing Zonation Parameters & Log 
#
# DN_ZONATION / Output: ZNRHOBCL,ZNNPHICL
# ZNRHOBCL -> RHOB_CLY
# ZNNPHICL -> NPHI_CLY
#
# SILTPNT_ZONATION / Output: RHODRYSL,ZNSLTLINRAT
# RHODRYSL -> RHOB_DRY_SLT
# ZNSLTLINRAT -> SILTLINE_RATIO
#
# GR_ZONATION / Output: ZNGRSD,ZNGRCL
# ZNGRSD -> GR_SD
# ZNGRCL -> GR_CL
#
# VCLGR_CARB_ZONATION / Output: zngrcln,zngrcly
# zngrcln -> GR_CLN
# zngrcly -> GR_CLY
#
# VCLDN_CARB_ZONATION / Output: znrhowcl,znnphwcl
# znrhowcl -> RHOB_WCL
# znnphwcl -> NPHI_WCL
#
# MN_ZONATION / Output: zn_m,zn_n
# ZN_M -> M
# ZN_N -> N
#
# RW_ZONATION / Output: ZNRW,ZNCWBGRAD
# ZNRW -> RW
# ZNCWBGRAD -> CWBGRAD
#
# TEMP_SAL_ZONATION

def GetParamValues(paramName):
	values = []
	if paramName+'_NUMBER' in globals():
		values = eval(paramName+'_NUMBER'+'.values()')
	elif paramName in globals():
		tmpVal = eval(paramName)
		values = [tmpVal for i in range(frmCnt)]	
	return values


TEMPSOURCE_VALUES = GetParamValues('TEMPSOURCE')
DEPTHSOURCE_VALUES = GetParamValues('DEPTHSOURCE')
TD_TVDSS_VALUES = GetParamValues('TD_TVDSS')
TD_MD_VALUES = GetParamValues('TD_MD')
WELLLOC_VALUES = GetParamValues('WELLLOC')
RTKB_DEP_VALUES = GetParamValues('RTKB_DEP')
BHT_TEMP_VALUES = GetParamValues('BHT_TEMP')
SB_TEMP_VALUES = GetParamValues('SB_TEMP')
SB_DEP_VALUES = GetParamValues('SB_DEP')
SURF_TEMP_VALUES = GetParamValues('SURF_TEMP')
GL_DEP_VALUES = GetParamValues('GL_DEP')
SALFLG_VALUES = GetParamValues('SALFLG')
SALW_VALUES = GetParamValues('SALW')
RW_VALUES = GetParamValues('RW')
TEMP_LOG_VALUES = GetParamValues('TEMP_LOG')

# HCF_ZONATION / Output: ZNHCOR
# ZNHCOR -> HCCOR
#
# OGF_ZONATION / Output: ZNOGF 
# ZNOGF -> OGF
#
# BHF_ZONATION / Output: ZNBHCOR
# ZNBHCOR -> BHCTYP
#
# SYNRHOB_ZONATION / Output : ZNSYNRSD,ZNSYNRCL
# ZNSYNRSD -> SYNDENSD
# ZNSYNRCL -> SYNDENCL
#
# COALCUT_ZONATION / Output : ZNCOALCUT
# ZNCOALCUT -> COALCUT
#
# LMSTRKCUT_ZONATION / Output : ZNSTRKCUT 
# ZNSTRKCUT -> STRCUT
#
# PERM_ZONATION / Output : choo_cons,znagen,znaphit,znaclw,znasilt
# Moved to [4] Proceeding to PERM-ROCKTP-SHF Processing
#
# SHF_ZONATION / Output : topman,GWC_DEPTH,GOC_DEPTH,OWC_DEPTH,GAS_GRAD,OIL_GRAD,WTR_GRAD 
# [4] Proceeding to PERM-ROCKTP-SHF Processing
#
#-------------- Storing Zonation Parameters & Log (S)
#

#-------------- Storing Min/Max Values of Logs
for log in ['RHOB', 'NPHI', 'GR']:
	dist = eval(log+'_LOG_DIST')
	values = eval(log+'.values()')
	pepParameterDict[log+'_ar'] = values[:]
	if dist =='Triangular':
		min_val = eval('ER_MIN_'+log)
		max_val = eval('ER_MAX_'+log)
		pepParameterDict[log+'_lo_ar'] = [values[i]-min_val if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[log+'_hi_ar'] = [values[i]+max_val if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
	else:
		pt_err = eval('PT_ERR_'+log)
		pepParameterDict[log+'_lo_ar'] = [values[i]-pt_err if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[log+'_hi_ar'] = [values[i]+pt_err if values[i] != MissingValue else MissingValue for i in range(frmCnt)]

for log in ['RT']:
	dist = eval(log+'_LOG_DIST')
	values = eval(log+'.values()')
	pepParameterDict[log+'_ar'] = values[:]
	if dist =='Triangular':
		min_val = eval('ER_MIN_'+log)
		max_val = eval('ER_MAX_'+log)
		pepParameterDict[log+'_lo_ar'] = [values[i]/(10**(min_val/100)) if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[log+'_hi_ar'] = [values[i]*(10**(max_val/100)) if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
	else:
		pt_err = eval('PT_ERR_'+log)
		pepParameterDict[log+'_lo_ar'] = [values[i]/(10**(pt_err/100)) if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[log+'_hi_ar'] = [values[i]*(10**(pt_err/100)) if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		



##-------------- Storing Hi/Lo Values of Variable Parameters

for vParam in ['RHOB_CL', 'NPHI_CL', 'GR_SD', 'GR_CL']:
	dist = eval(vParam+'_PAR_DIST')
	if (LITHOLOGY_MODEL=='SSC'):
		if vParam == 'RHOB_CL':
			paramName = 'RHOB_CLY'
		elif vParam == 'NPHI_CL':
			paramName = 'NPHI_CLY'
		elif vParam == 'GR_SD':
			paramName = 'GR_SD'
		elif vParam == 'GR_CL':
			paramName = 'GR_CL'
	else: #(Carbonates)
		if vParam == 'RHOB_CL':
			paramName = 'RHOB_WCL'
		elif vParam == 'NPHI_CL':
			paramName = 'NPHI_WCL'
		elif vParam == 'GR_SD':
			paramName = 'GR_CLN'
		elif vParam == 'GR_CL':
			paramName = 'GR_CLY'
	values = []
	if paramName+'_NUMBER' in locals(): # switched parameter
		values = eval(paramName+'_NUMBER'+'.values()')
	else:
		values = [eval(paramName) for i in range(frmCnt)]
	pepParameterDict[vParam+'_ar'] = values[:]
	if dist =='Triangular':
		min_val = eval('ER_MIN_'+vParam)
		max_val = eval('ER_MAX_'+vParam)
		pepParameterDict[vParam+'_min_ar'] = [values[i]-min_val if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[vParam+'_max_ar'] = [values[i]+max_val if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
	else:
		pt_err = eval('PT_ERR_'+vParam)
		pepParameterDict[vParam+'_min_ar'] = [values[i]-pt_err if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[vParam+'_max_ar'] = [values[i]+pt_err if values[i] != MissingValue else MissingValue for i in range(frmCnt)]



vParamDict = {} # Storing parameters in a Dict {identifier:paramName}
vParamDict ['SILTLINE_RATIO'] = 'SILTLINE_RATIO'
vParamDict ['RHODRYSL'] = 'RHOB_DRY_SLT'
vParamDict ['RW'] = 'RW'
vParamDict ['CWBGRAD'] = 'CWBGRAD'
vParamDict ['M'] = 'M'
vParamDict ['N'] = 'N'
vParamDict ['NEUFAC'] = 'NEUFAC'
vParamDict ['SYNDENSD'] = 'SYNDENSD'
vParamDict ['SYNDENCL'] = 'SYNDENCL'

for vParam in vParamDict:
	dist = eval(vParam+'_PAR_DIST')
	values = []
	coef = 1 
	
	paramName = vParamDict[vParam]
	if paramName+'_NUMBER' in locals(): # switched parameter
		values = eval(paramName+'_NUMBER'+'.values()')
	else:
		values = [eval(paramName) for i in range(frmCnt)]	
	pepParameterDict[vParam+'_ar'] = values[:]
	if dist =='Triangular':
		min_val = eval('ER_MIN_'+vParam)
		max_val = eval('ER_MAX_'+vParam)
		pepParameterDict[vParam+'_min_ar'] = [values[i]-min_val/coef if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[vParam+'_max_ar'] = [values[i]+max_val/coef if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
	else:
		pt_err = eval('PT_ERR_'+vParam)
		pepParameterDict[vParam+'_min_ar'] = [values[i]-pt_err/coef if values[i] != MissingValue else MissingValue for i in range(frmCnt)]
		pepParameterDict[vParam+'_max_ar'] = [values[i]+pt_err/coef if values[i] != MissingValue else MissingValue for i in range(frmCnt)]	

##-------------- Storing Hi/Lo Values of Constant Parameters

cParamDict = {} # Storing parameters in a Dict {identifier:paramName}
cParamDict ['RHODRYSD'] = 'RHOB_DRY_SAND'
cParamDict ['NPHI_DRYSD'] = 'NPHI_DRY_SAND'
cParamDict ['RHOB_DRYLM'] = 'RHOB_DRYLM'
cParamDict ['NPHI_DRYLM'] = 'NPHI_DRYLM'
cParamDict ['RHOB_DRYDL'] = 'RHOB_DRYDL'
cParamDict ['NPHI_DRYDL'] = 'NPHI_DRYDL'
cParamDict ['RHOGAS'] = 'RHO_GAS'
cParamDict ['RHOOIL'] = 'RHO_OIL'
cParamDict ['MFRES'] = 'MFRES'
cParamDict ['DEGHCCOR'] = 'DEGHCCOR'

for cParam in cParamDict:
	dist = eval(cParam+'_PAR_DIST')
	values = []
	paramName = cParamDict[cParam]
	if paramName+'_NUMBER' in locals(): # switched parameter
		values = eval(paramName+'_NUMBER'+'.values()')
	else:
		tmpVal = eval(paramName)
		values = [tmpVal for i in range(frmCnt)]
	pepParameterDict[cParam+'_ar'] = values[:]
	if dist =='Triangular':
		min_val = eval('ER_MIN_'+cParam)
		max_val = eval('ER_MAX_'+cParam)
		pepParameterDict[cParam+'_min_ar'] = [values[i]-min_val for i in range(frmCnt)]
		pepParameterDict[cParam+'_max_ar'] = [values[i]+max_val for i in range(frmCnt)]
	else:
		pt_err = eval('PT_ERR_'+vParam)
		pepParameterDict[cParam+'_min_ar'] = [values[i]-pt_err for i in range(frmCnt)]
		pepParameterDict[cParam+'_max_ar'] = [values[i]+pt_err for i in range(frmCnt)]	

###################### [3] Storing All Parameters & Logs into Memory (E) ##########################

###################### [5] Regression Analysis for Auto Adjustment (S) ##############################
for log in ['RHOB', 'NPHI', 'GR', 'RT']:
	pepParameterDict[log+'_lo_reg'] = [MissingValue, MissingValue]
	pepParameterDict[log+'_hi_reg'] = [MissingValue, MissingValue]
	xValues = eval(log+'.values()')
	yValuesLow = pepParameterDict[log+'_lo_ar']
	yValuesHigh = pepParameterDict[log+'_hi_ar']
	res = ts.regression(xValues, yValuesLow, 1, 'y/x')
	if res and len(res) == 2:
		pepParameterDict[log+'_lo_reg'] = res[:]
	res = ts.regression(xValues, yValuesHigh, 1, 'y/x')
	if res and len(res) == 2:
		pepParameterDict[log+'_hi_reg'] = res[:]
###################### [5] Regression Analysis for Auto Adjustment (E) ###############################

###################### [6] Calculating Parameter Offsets for Auto Adjusment (S) ######################

for log in ['RHOB_CL', 'NPHI_CL', 'GR_SD', 'GR_CL']:
	if (LITHOLOGY_MODEL=='SSC'):
		if log == 'RHOB_CL':
			paramName = 'RHOB_CLY'
		elif log == 'NPHI_CL':
			paramName = 'NPHI_CLY'
		elif log == 'GR_CL':
			paramName = 'GR_CL'
		elif log == 'GR_SD':
			paramName = 'GR_SD'
	else: #(Carbonates)
		if log == 'RHOB_CL':
			paramName = 'RHOB_WCL'
		elif log == 'NPHI_CL':
			paramName = 'NPHI_WCL'
		elif log == 'GR_CL':
			paramName = 'GR_CLY'
		elif log == 'GR_SD':
			paramName = 'GR_CLN'
	regName = log.replace('_CL','').replace('_SD','')
	values = []
	if paramName+'_NUMBER' in locals(): # switched parameter
		values = eval(paramName+'_NUMBER'+'.values()')
	else:
		values = [eval(paramName) for i in range(frmCnt)]
	
	for option in ['hi', 'lo']:
		pepParameterDict[log+'_'+option+'_ar'] = [MissingValue for i in range(frmCnt)]
		pepParameterDict[log+'_'+option+'_min_ar'] = [MissingValue for i in range(frmCnt)]
		pepParameterDict[log+'_'+option+'_max_ar'] = [MissingValue for i in range(frmCnt)]
		for i in range(frmCnt):
			pepParameterDict[log+'_'+option+'_ar'][i] = values[i]*pepParameterDict[regName+'_'+option+'_reg'][0]+pepParameterDict[regName+'_'+option+'_reg'][1]
			pepParameterDict[log+'_'+option+'_min_ar'][i] = pepParameterDict[log+'_min_ar'][i]*pepParameterDict[regName+'_'+option+'_reg'][0]+pepParameterDict[regName+'_'+option+'_reg'][1]
			pepParameterDict[log+'_'+option+'_max_ar'][i] = pepParameterDict[log+'_max_ar'][i]*pepParameterDict[regName+'_'+option+'_reg'][0]+pepParameterDict[regName+'_'+option+'_reg'][1]

###################### [6] Calculating Parameter Offsets for Auto Adjusment (E) ######################

###################### [7] Monte-Carlo Preparation (S) ###############################################
MCCNT = 1
if (DO_MC=='NO'):
	ITR_NO = 1
else:
	if (ITR_NO==1):
		ITR_NO = 2
		MCCNT = 2
###################### [7] Monte-Carlo Preparation (E) ###############################################

def create_array(well, dataset, array_name, number_of_columns, family, unit):
	if db.variableExists(well, dataset, array_name):
		arr = Array(well, dataset, array_name)
		arr.columnCountChange(number_of_columns)
		arr.historyAdd('Array update of column number to {}'.format(number_of_columns))
	else:
		arr = Array(well, dataset, array_name, number_of_columns, family, unit)
	return arr

PHIT_D_LIST_COUNT = 100
SWT_D_LIST_COUNT = 100
VCLW_D_LIST_COUNT = 100
VSILT_D_LIST_COUNT = 100
	
if DO_MC == "YES":
	# FIX_ISSUE_POINT 4 - RMeneu July, 2018
	# The four following count were initialized with respectively 500, 100, 100 and 100
	# They represent the number of bins. Let's initialize them with a formula that allows to test on smallest number of iteration
	# --- BEGINNING
	
	# --- END
	
	# FIX_ISSUE_POINT 4 - RMeneu July, 2018
	# The arrays were deleted and recreated, reason why they disappear from the logview.
	# With the create_array function, arrays are just updated to the new column number if they already exist.
	# They thus remain in logviews
	#
	# --- BEGINNING
	PHIT_D = create_array(DEPTH.wellName(), DEPTH.datasetName(), "PHIT_D", PHIT_D_LIST_COUNT, u"Total Porosity", u"V/V")
	SWT_D = create_array(DEPTH.wellName(), DEPTH.datasetName(), "SWT_D", SWT_D_LIST_COUNT, u"Total Water Saturation", u"V/V")
	VCLW_D = create_array(DEPTH.wellName(), DEPTH.datasetName(), "VCLW_D", VCLW_D_LIST_COUNT, u"Clay Volume", u"V/V")
	VSILT_D = create_array(DEPTH.wellName(), DEPTH.datasetName(), "VSILT_D", VSILT_D_LIST_COUNT, u"Silt Volume", u"V/V")
	# --- END
	
db.progressBarShow()
db.progressBarSetValue(0)

# extracting parameter dict before loop for performance issues
pepParameterDict_RHOB_ar = pepParameterDict['RHOB_ar']
pepParameterDict_RHOB_hi_ar = pepParameterDict['RHOB_hi_ar']
pepParameterDict_RHOB_lo_ar = pepParameterDict['RHOB_lo_ar']
pepParameterDict_NPHI_ar = pepParameterDict['NPHI_ar']
pepParameterDict_NPHI_hi_ar = pepParameterDict['NPHI_hi_ar']
pepParameterDict_NPHI_lo_ar = pepParameterDict['NPHI_lo_ar']
pepParameterDict_GR_ar = pepParameterDict['GR_ar']
pepParameterDict_GR_hi_ar = pepParameterDict['GR_hi_ar']
pepParameterDict_GR_lo_ar = pepParameterDict['GR_lo_ar']
pepParameterDict_RT_ar = pepParameterDict['RT_ar']
pepParameterDict_RT_hi_ar = pepParameterDict['RT_hi_ar']
pepParameterDict_RT_lo_ar = pepParameterDict['RT_lo_ar']

pepParameterDict_RHOB_CL_ar = pepParameterDict['RHOB_CL_ar']
pepParameterDict_RHOB_CL_max_ar = pepParameterDict['RHOB_CL_max_ar']
pepParameterDict_RHOB_CL_min_ar = pepParameterDict['RHOB_CL_min_ar']
pepParameterDict_RHOB_CL_hi_ar = pepParameterDict['RHOB_CL_hi_ar']
pepParameterDict_RHOB_CL_lo_ar = pepParameterDict['RHOB_CL_lo_ar']
pepParameterDict_RHOB_CL_hi_max_ar = pepParameterDict['RHOB_CL_hi_max_ar']
pepParameterDict_RHOB_CL_hi_min_ar = pepParameterDict['RHOB_CL_hi_min_ar']
pepParameterDict_RHOB_CL_lo_max_ar = pepParameterDict['RHOB_CL_lo_max_ar']
pepParameterDict_RHOB_CL_lo_min_ar = pepParameterDict['RHOB_CL_lo_min_ar']

pepParameterDict_NPHI_CL_ar = pepParameterDict['NPHI_CL_ar']
pepParameterDict_NPHI_CL_max_ar = pepParameterDict['NPHI_CL_max_ar']
pepParameterDict_NPHI_CL_min_ar = pepParameterDict['NPHI_CL_min_ar']
pepParameterDict_NPHI_CL_hi_ar = pepParameterDict['NPHI_CL_hi_ar']
pepParameterDict_NPHI_CL_lo_ar = pepParameterDict['NPHI_CL_lo_ar']
pepParameterDict_NPHI_CL_hi_max_ar = pepParameterDict['NPHI_CL_hi_max_ar']
pepParameterDict_NPHI_CL_hi_min_ar = pepParameterDict['NPHI_CL_hi_min_ar']
pepParameterDict_NPHI_CL_lo_max_ar = pepParameterDict['NPHI_CL_lo_max_ar']
pepParameterDict_NPHI_CL_lo_min_ar = pepParameterDict['NPHI_CL_lo_min_ar']

pepParameterDict_GR_CL_ar = pepParameterDict['GR_CL_ar']
pepParameterDict_GR_CL_max_ar = pepParameterDict['GR_CL_max_ar']
pepParameterDict_GR_CL_min_ar = pepParameterDict['GR_CL_min_ar']
pepParameterDict_GR_CL_hi_ar = pepParameterDict['GR_CL_hi_ar']
pepParameterDict_GR_CL_lo_ar = pepParameterDict['GR_CL_lo_ar']
pepParameterDict_GR_CL_hi_max_ar = pepParameterDict['GR_CL_hi_max_ar']
pepParameterDict_GR_CL_hi_min_ar = pepParameterDict['GR_CL_hi_min_ar']
pepParameterDict_GR_CL_lo_max_ar = pepParameterDict['GR_CL_lo_max_ar']
pepParameterDict_GR_CL_lo_min_ar = pepParameterDict['GR_CL_lo_min_ar']

pepParameterDict_GR_SD_ar = pepParameterDict['GR_SD_ar']
pepParameterDict_GR_SD_max_ar = pepParameterDict['GR_SD_max_ar']
pepParameterDict_GR_SD_min_ar = pepParameterDict['GR_SD_min_ar']
pepParameterDict_GR_SD_hi_ar = pepParameterDict['GR_SD_hi_ar']
pepParameterDict_GR_SD_lo_ar = pepParameterDict['GR_SD_lo_ar']
pepParameterDict_GR_SD_hi_max_ar = pepParameterDict['GR_SD_hi_max_ar']
pepParameterDict_GR_SD_hi_min_ar = pepParameterDict['GR_SD_hi_min_ar']
pepParameterDict_GR_SD_lo_max_ar = pepParameterDict['GR_SD_lo_max_ar']
pepParameterDict_GR_SD_lo_min_ar = pepParameterDict['GR_SD_lo_min_ar']

pepParameterDict_SILTLINE_RATIO_max_ar = pepParameterDict['SILTLINE_RATIO_max_ar']
pepParameterDict_SILTLINE_RATIO_min_ar = pepParameterDict['SILTLINE_RATIO_min_ar']
pepParameterDict_RHODRYSL_max_ar = pepParameterDict['RHODRYSL_max_ar']
pepParameterDict_RHODRYSL_min_ar = pepParameterDict['RHODRYSL_min_ar']
pepParameterDict_M_max_ar = pepParameterDict['M_max_ar']
pepParameterDict_M_ar = pepParameterDict['M_ar']
pepParameterDict_M_min_ar = pepParameterDict['M_min_ar']
pepParameterDict_N_max_ar = pepParameterDict['N_max_ar']
pepParameterDict_N_ar = pepParameterDict['N_ar']
pepParameterDict_N_min_ar = pepParameterDict['N_min_ar']
pepParameterDict_NEUFAC_max_ar = pepParameterDict['NEUFAC_max_ar']
pepParameterDict_NEUFAC_ar = pepParameterDict['NEUFAC_ar']
pepParameterDict_NEUFAC_min_ar = pepParameterDict['NEUFAC_min_ar']
pepParameterDict_SYNDENSD_max_ar = pepParameterDict['SYNDENSD_max_ar']
pepParameterDict_SYNDENSD_min_ar = pepParameterDict['SYNDENSD_min_ar']
pepParameterDict_SYNDENCL_max_ar = pepParameterDict['SYNDENCL_max_ar']
pepParameterDict_SYNDENCL_min_ar = pepParameterDict['SYNDENCL_min_ar']
pepParameterDict_RHODRYSD_max_ar = pepParameterDict['RHODRYSD_max_ar']
pepParameterDict_RHODRYSD_min_ar = pepParameterDict['RHODRYSD_min_ar']
pepParameterDict_NPHI_DRYSD_max_ar = pepParameterDict['NPHI_DRYSD_max_ar']
pepParameterDict_NPHI_DRYSD_min_ar = pepParameterDict['NPHI_DRYSD_min_ar']
pepParameterDict_DEGHCCOR_max_ar = pepParameterDict['DEGHCCOR_max_ar']
pepParameterDict_DEGHCCOR_min_ar = pepParameterDict['DEGHCCOR_min_ar']
pepParameterDict_RHODRYSL_ar = pepParameterDict['RHODRYSL_ar']
pepParameterDict_SILTLINE_RATIO_ar = pepParameterDict['SILTLINE_RATIO_ar']
pepParameterDict_SYNDENCL_ar = pepParameterDict['SYNDENCL_ar']
pepParameterDict_SYNDENSD_ar = pepParameterDict['SYNDENSD_ar']
pepParameterDict_RHODRYSD_ar = pepParameterDict['RHODRYSD_ar']
pepParameterDict_NPHI_DRYSD_ar = pepParameterDict['NPHI_DRYSD_ar']
pepParameterDict_RHOGAS_ar =  pepParameterDict['RHOGAS_ar']
pepParameterDict_RHOGAS_max_ar = pepParameterDict['RHOGAS_max_ar']
pepParameterDict_RHOGAS_min_ar = pepParameterDict['RHOGAS_min_ar']
pepParameterDict_RHOOIL_ar =  pepParameterDict['RHOOIL_ar']
pepParameterDict_RHOOIL_max_ar = pepParameterDict['RHOOIL_max_ar']
pepParameterDict_RHOOIL_min_ar = pepParameterDict['RHOOIL_min_ar']
pepParameterDict_MFRES_ar =  pepParameterDict['MFRES_ar']
pepParameterDict_MFRES_max_ar = pepParameterDict['MFRES_max_ar']
pepParameterDict_MFRES_min_ar = pepParameterDict['MFRES_min_ar']
pepParameterDict_DEGHCCOR_ar =  pepParameterDict['DEGHCCOR_ar']

HCCOR_VAL = parameterDict['HCCOR'].value('value')
if 'HCCOR_NUMBER' in locals(): # switched parameter
	HCCOR_VAL = HCCOR_NUMBER.values()
else:
	HCCOR_VAL = [parameterDict['HCCOR'].value('value') for i in range(frmCnt)]

EXT_REF_LOG_VAL = parameterDict['EXT_REF_LOG'].value('value')
if 'EXT_REF_LOG_NUMBER' in locals(): # switched parameter
	EXT_REF_LOG_VAL = EXT_REF_LOG_NUMBER.values()
else:
	EXT_REF_LOG_VAL = [parameterDict['EXT_REF_LOG'].value('value') for i in range(frmCnt)]

CORR_RHOB_LOG_VAL = parameterDict['CORR_RHOB_LOG'].value('value')
if 'CORR_RHOB_LOG_NUMBER' in locals(): # switched parameter
	CORR_RHOB_LOG_VAL = CORR_RHOB_LOG_NUMBER.values()
else:
	CORR_RHOB_LOG_VAL = [parameterDict['CORR_RHOB_LOG'].value('value') for i in range(frmCnt)]

BHCTYP_VAL = parameterDict['BHCTYP'].value('value')
if 'BHCTYP_NUMBER' in locals(): # switched parameter
	BHCTYP_VAL = BHCTYP_NUMBER.values()
else:
	BHCTYP_VAL = [parameterDict['BHCTYP'].value('value') for i in range(frmCnt)]
	
COALCUT_VAL = parameterDict['COALCUT'].value('value')
if 'COALCUT_NUMBER' in locals(): # switched parameter
	COALCUT_VAL = COALCUT_NUMBER.values()
else:
	COALCUT_VAL = [parameterDict['COALCUT'].value('value') for i in range(frmCnt)]
	
COALFLG_LOG_VAL = parameterDict['COALFLG_LOG'].value('value')
if 'COALFLG_LOG_NUMBER' in locals(): # switched parameter
	COALFLG_LOG_VAL = COALFLG_LOG_NUMBER.values()
else:
	COALFLG_LOG_VAL = [parameterDict['COALFLG_LOG'].value('value') for i in range(frmCnt)]
	
STRCUT_VAL = parameterDict['STRCUT'].value('value')
if 'STRCUT_NUMBER' in locals(): # switched parameter
	STRCUT_VAL = STRCUT_NUMBER.values()
else:
	STRCUT_VAL = [parameterDict['STRCUT'].value('value') for i in range(frmCnt)]

EXT_PHIT_LOG_VAL = parameterDict['EXT_PHIT_LOG'].value('value')
if 'EXT_PHIT_LOG_NUMBER' in locals(): # switched parameter
	EXT_PHIT_LOG_VAL = EXT_PHIT_LOG_NUMBER.values()
else:
	EXT_PHIT_LOG_VAL = [parameterDict['EXT_PHIT_LOG'].value('value') for i in range(frmCnt)]
	
EXT_PHIE_LOG_VAL = parameterDict['EXT_PHIE_LOG'].value('value')
if 'EXT_PHIE_LOG_NUMBER' in locals(): # switched parameter
	EXT_PHIE_LOG_VAL = EXT_PHIE_LOG_NUMBER.values()
else:
	EXT_PHIE_LOG_VAL = [parameterDict['EXT_PHIE_LOG'].value('value') for i in range(frmCnt)]
	
EXT_VCLD_LOG_VAL = parameterDict['EXT_VCLD_LOG'].value('value')
if 'EXT_VCLD_LOG_NUMBER' in locals(): # switched parameter
	EXT_VCLD_LOG_VAL = EXT_VCLD_LOG_NUMBER.values()
else:
	EXT_VCLD_LOG_VAL = [parameterDict['EXT_VCLD_LOG'].value('value') for i in range(frmCnt)]
	
OTHER_EXT_VCLY_LOG_VAL = parameterDict['OTHER_EXT_VCLY_LOG'].value('value')
if 'OTHER_EXT_VCLY_LOG_NUMBER' in locals(): # switched parameter
	OTHER_EXT_VCLY_LOG_VAL = OTHER_EXT_VCLY_LOG_NUMBER.values()
else:
	OTHER_EXT_VCLY_LOG_VAL = [parameterDict['OTHER_EXT_VCLY_LOG'].value('value') for i in range(frmCnt)]
	
CLAY_VOLUME_FLAG_VAL = parameterDict['CLAY_VOLUME_FLAG'].value('value')
if 'CLAY_VOLUME_FLAG_NUMBER' in locals(): # switched parameter
	CLAY_VOLUME_FLAG_VAL = CLAY_VOLUME_FLAG_NUMBER.values()
else:
	CLAY_VOLUME_FLAG_VAL = [parameterDict['CLAY_VOLUME_FLAG'].value('value') for i in range(frmCnt)]
	
OGF_VAL = parameterDict['OGF'].value('value')
if 'OGF_NUMBER' in locals(): # switched parameter
	OGF_VAL = OGF_NUMBER.values()
else:
	OGF_VAL = [parameterDict['OGF'].value('value') for i in range(frmCnt)]
	
CWBGRAD_VAL = parameterDict['CWBGRAD'].value('value')
if 'CWBGRAD_NUMBER' in locals(): # switched parameter
	CWBGRAD_VAL = CWBGRAD_NUMBER.values()
else:
	CWBGRAD_VAL = [parameterDict['CWBGRAD'].value('value') for i in range(frmCnt)]


#----------------- Initialize all variables ---------------------------------------------------
loopSize = frmCnt
loopRange = range(loopSize)







# callback function for progress bar
def setProgressBar(progress):
	db.progressBarSetValue(progress)

#----------------- Initialize all variables ---------------------------------------------------

from ctypes import*
from _ctypes import FreeLibrary

dllName = "pep_utils_2023.dll"
#DynaDLL = cdll.LoadLibrary(os.path.join(db.dirTechlog(), "bin64", dllName))
DynaDLL = cdll.LoadLibrary(os.path.join(db.dirCompany(), "External_DLLs", dllName))

# set progress bar callback function
c_func = CFUNCTYPE(c_void_p, c_double)
DynaDLL.setProgressHandler.argtypes = [c_func]
DynaDLL.setProgressHandler.restype = None
handler = c_func(setProgressBar)
DynaDLL.setProgressHandler(handler)

# structure used to avoid maximum 250 function parameters limitation, which is claimed to be fixed in Python 3.7
class Input_1D_Data(Structure):
    _fields_ = [("tEMPSOURCE", POINTER(c_wchar_p)),
				("dEPTHSOURCE", POINTER(c_wchar_p)),
				("wELLLOC", POINTER(c_wchar_p)),
				("sALFLG", POINTER(c_wchar_p)),
				("Md", POINTER(c_double)),
				("TD_MD", POINTER(c_double)),
				("Tvdss", POINTER(c_double)),
				("TD_TVDSS", POINTER(c_double)),
				("RTKB_DEP", POINTER(c_double)),
				("GL_DEP", POINTER(c_double)),
				("SURF_TEMP", POINTER(c_double)),
				("SB_DEP", POINTER(c_double)),
				("SB_TEMP", POINTER(c_double)),
				("BHT_TEMP", POINTER(c_double)),		
				("TEMP_LOG", POINTER(c_double)),
				("SALW", POINTER(c_double)),
				("RW", POINTER(c_double)),
				("Zntemp", POINTER(c_double)),
				("Zntempunit", POINTER(c_double)),
				("Znrw77f", POINTER(c_double)),
				("Znsalwtr", POINTER(c_double)),
				("Znrw", POINTER(c_double)),
				("LithmodUpdated", POINTER(c_wchar_p)),
                ("HCCOR_VAL", POINTER(c_double)),
				("EXT_REF_LOG_VAL", POINTER(c_double)),
				("CORR_RHOB_LOG_VAL", POINTER(c_double)),
				("BHCTYP_VAL", POINTER(c_double)),
				("COALCUT_VAL", POINTER(c_double)),
				("COALFLG_LOG_VAL", POINTER(c_double)),
				("STRCUT_VAL", POINTER(c_double)),
				("EXT_PHIT_LOG_VAL", POINTER(c_double)),
				("EXT_PHIE_LOG_VAL", POINTER(c_double)),
				("EXT_VCLD_LOG_VAL", POINTER(c_double)),
				("OTHER_EXT_VCLY_LOG_VAL", POINTER(c_double)),
				("OGF_VAL", POINTER(c_double)),
				("CWBGRAD_VAL", POINTER(c_double)),
				("GR_ar", POINTER(c_double)),
				("GR_lo_ar", POINTER(c_double)),
				("GR_hi_ar", POINTER(c_double)),
				("GR_SD_ar", POINTER(c_double)),
				("GR_SD_lo_ar", POINTER(c_double)),
				("GR_SD_hi_ar", POINTER(c_double)),
				("GR_SD_max_ar", POINTER(c_double)),
				("GR_SD_lo_max_ar", POINTER(c_double)),
				("GR_SD_hi_max_ar", POINTER(c_double)),
				("GR_SD_min_ar", POINTER(c_double)),
				("GR_SD_lo_min_ar", POINTER(c_double)),
				("GR_SD_hi_min_ar", POINTER(c_double)),
				("GR_CL_ar", POINTER(c_double)),
				("GR_CL_lo_ar", POINTER(c_double)),
				("GR_CL_hi_ar", POINTER(c_double)),
				("GR_CL_max_ar", POINTER(c_double)),
				("GR_CL_lo_max_ar", POINTER(c_double)),
				("GR_CL_hi_max_ar", POINTER(c_double)),
				("GR_CL_min_ar", POINTER(c_double)),
				("GR_CL_lo_min_ar", POINTER(c_double)),
				("GR_CL_hi_min_ar", POINTER(c_double)),
				("NPHI_ar", POINTER(c_double)),
				("NPHI_lo_ar", POINTER(c_double)),
				("NPHI_hi_ar", POINTER(c_double)),
				("NPHI_CL_ar", POINTER(c_double)),
				("NPHI_CL_lo_ar", POINTER(c_double)),
				("NPHI_CL_hi_ar", POINTER(c_double)),
				("NPHI_CL_max_ar", POINTER(c_double)),
				("NPHI_CL_lo_max_ar", POINTER(c_double)),
				("NPHI_CL_hi_max_ar", POINTER(c_double)),
				("NPHI_CL_min_ar", POINTER(c_double)),
				("NPHI_CL_lo_min_ar", POINTER(c_double)),
				("NPHI_CL_hi_min_ar", POINTER(c_double)),
				("RHOB_ar", POINTER(c_double)),
				("RHOB_lo_ar", POINTER(c_double)),
				("RHOB_hi_ar", POINTER(c_double)),
				("RHOB_CL_ar", POINTER(c_double)),
				("RHOB_CL_lo_ar", POINTER(c_double)),
				("RHOB_CL_hi_ar", POINTER(c_double)),
				("RHOB_CL_max_ar", POINTER(c_double)),
				("RHOB_CL_lo_max_ar", POINTER(c_double)),
				("RHOB_CL_hi_max_ar", POINTER(c_double)),
				("RHOB_CL_min_ar", POINTER(c_double)),
				("RHOB_CL_lo_min_ar", POINTER(c_double)),
				("RHOB_CL_hi_min_ar", POINTER(c_double)),
				("RT_ar", POINTER(c_double)),
				("RT_lo_ar", POINTER(c_double)),
				("RT_hi_ar", POINTER(c_double)),
				("PEF", POINTER(c_double)),
				("DT", POINTER(c_double)),
				("MFRES_ar", POINTER(c_double)),
				("MFRES_min_ar", POINTER(c_double)),
				("MFRES_max_ar", POINTER(c_double)),
				("M_ar", POINTER(c_double)),
				("M_min_ar", POINTER(c_double)),
				("M_max_ar", POINTER(c_double)),
				("N_ar", POINTER(c_double)),
				("N_min_ar", POINTER(c_double)),
				("N_max_ar", POINTER(c_double)),
				("RHOOIL_ar", POINTER(c_double)),
				("RHOOIL_min_ar", POINTER(c_double)),
				("RHOOIL_max_ar", POINTER(c_double)),
				("RHOGAS_ar", POINTER(c_double)),
				("RHOGAS_min_ar", POINTER(c_double)),
				("RHOGAS_max_ar", POINTER(c_double)),
				("NEUFAC_ar", POINTER(c_double)),
				("NEUFAC_min_ar", POINTER(c_double)),
				("NEUFAC_max_ar", POINTER(c_double)),
				("SYNDENSD_ar", POINTER(c_double)),
				("SYNDENSD_min_ar", POINTER(c_double)),
				("SYNDENSD_max_ar", POINTER(c_double)),
				("SYNDENCL_ar", POINTER(c_double)),
				("SYNDENCL_min_ar", POINTER(c_double)),
				("SYNDENCL_max_ar", POINTER(c_double)),
				("SILTLINE_RATIO_ar", POINTER(c_double)),
				("SILTLINE_RATIO_min_ar", POINTER(c_double)),
				("SILTLINE_RATIO_max_ar", POINTER(c_double)),
				("DEGHCCOR_ar", POINTER(c_double)),
				("DEGHCCOR_min_ar", POINTER(c_double)),
				("DEGHCCOR_max_ar", POINTER(c_double)),
				("RHODRYSL_ar", POINTER(c_double)),
				("RHODRYSL_min_ar", POINTER(c_double)),
				("RHODRYSL_max_ar", POINTER(c_double)),
				("RHODRYSD_ar", POINTER(c_double)),
				("RHODRYSD_min_ar", POINTER(c_double)),
				("RHODRYSD_max_ar", POINTER(c_double)),
				("NPHI_DRYSD_ar", POINTER(c_double)),
				("NPHI_DRYSD_min_ar", POINTER(c_double)),
				("NPHI_DRYSD_max_ar", POINTER(c_double))]
				
DynaDLL.PEP_Module_A_adj.restype = c_int
DynaDLL.PEP_Module_A_adj.argtypes = [c_int, POINTER(c_double), c_double,\
    c_wchar_p,c_wchar_p,\
    c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p,\
    c_wchar_p,c_wchar_p, c_wchar_p,\
    c_wchar_p,POINTER(c_wchar_p),\
    c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p,\
    c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p,\
    c_wchar_p,c_wchar_p,\
	c_double,c_double,c_double,c_double,c_double,c_double,\
	c_double,c_double,c_double,c_double,c_double,c_double,\
	c_double,c_double,c_double,c_double,c_double,c_double,\
	c_double,c_double,c_double,\
	c_double,c_double,c_double,c_double,c_double,c_double,c_int,\
	Input_1D_Data,\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),\
	c_wchar_p,c_int,c_int,c_int,c_int,\
	c_int,c_int,c_int,c_int,\
	c_wchar_p,c_wchar_p, c_wchar_p,\
	c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p,\
	c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p,\
	c_wchar_p,c_wchar_p, c_wchar_p,c_wchar_p,\
	c_wchar_p,c_wchar_p, c_wchar_p,\
	c_wchar_p,c_wchar_p, c_wchar_p,\
	c_wchar_p,c_wchar_p,\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),\
	POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double)]

cLAY_VOLUME_FLAG_VAL = (c_wchar_p * loopSize)(*CLAY_VOLUME_FLAG_VAL)

dEPTH  = (c_double * loopSize)(*DEPTH.values())
pEF = (c_double * loopSize)(*PEF.values())
dT = (c_double * loopSize)(*DT.values())

hCCOR_VAL = (c_double * loopSize)(*HCCOR_VAL)
bHCTYP_VAL = (c_double * loopSize)(*BHCTYP_VAL)
oGF_VAL = (c_double * loopSize)(*OGF_VAL)

tEMPSOURCE = (c_wchar_p * loopSize)(*TEMPSOURCE_VALUES)
dEPTHSOURCE = (c_wchar_p * loopSize)(*DEPTHSOURCE_VALUES)
wELLLOC = (c_wchar_p * loopSize)(*WELLLOC_VALUES)
sALFLG = (c_wchar_p * loopSize)(*SALFLG_VALUES)
Md = (c_double * loopSize)(*DEPTH.values())
tD_MD = (c_double * loopSize)(*TD_MD_VALUES)
Tvdss = (c_double * loopSize)(*TVDSS.values())
tD_TVDSS = (c_double * loopSize)(*TD_TVDSS_VALUES)
rTKB_DEP = (c_double * loopSize)(*RTKB_DEP_VALUES)
gL_DEP = (c_double * loopSize)(*GL_DEP_VALUES)
sURF_TEMP = (c_double * loopSize)(*SURF_TEMP_VALUES)
sB_DEP = (c_double * loopSize)(*SB_DEP_VALUES)
sB_TEMP = (c_double * loopSize)(*SB_TEMP_VALUES)
bHT_TEMP = (c_double * loopSize)(*BHT_TEMP_VALUES)
tEMP_LOG = (c_double * loopSize)(*TEMP_LOG_VALUES)
sALW = (c_double * loopSize)(*SALW_VALUES)
rW = (c_double * loopSize)(*RW_VALUES)
eXT_REF_LOG_VAL = (c_double * loopSize)(*EXT_REF_LOG_VAL)
cORR_RHOB_LOG_VAL = (c_double * loopSize)(*CORR_RHOB_LOG_VAL)
cOALCUT_VAL = (c_double * loopSize)(*COALCUT_VAL)
cOALFLG_LOG_VAL = (c_double * loopSize)(*COALFLG_LOG_VAL)
sTRCUT_VAL = (c_double * loopSize)(*STRCUT_VAL)
eXT_PHIT_LOG_VAL = (c_double * loopSize)(*EXT_PHIT_LOG_VAL)
eXT_PHIE_LOG_VAL = (c_double * loopSize)(*EXT_PHIE_LOG_VAL)
eXT_VCLD_LOG_VAL = (c_double * loopSize)(*EXT_VCLD_LOG_VAL)
oTHER_EXT_VCLY_LOG_VAL = (c_double * loopSize)(*OTHER_EXT_VCLY_LOG_VAL)
cWBGRAD_VAL = (c_double * loopSize)(*CWBGRAD_VAL)
GR_ar = (c_double * loopSize)(*pepParameterDict_GR_ar)
GR_lo_ar = (c_double * loopSize)(*pepParameterDict_GR_lo_ar)
GR_hi_ar = (c_double * loopSize)(*pepParameterDict_GR_hi_ar)
GR_SD_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_ar)
GR_SD_lo_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_lo_ar)
GR_SD_hi_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_hi_ar)
GR_SD_max_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_max_ar)
GR_SD_lo_max_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_lo_max_ar)
GR_SD_hi_max_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_hi_max_ar)
GR_SD_min_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_min_ar)
GR_SD_lo_min_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_lo_min_ar)
GR_SD_hi_min_ar = (c_double * loopSize)(*pepParameterDict_GR_SD_hi_min_ar)
GR_CL_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_ar)
GR_CL_lo_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_lo_ar)
GR_CL_hi_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_hi_ar)
GR_CL_max_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_max_ar)
GR_CL_lo_max_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_lo_max_ar)
GR_CL_hi_max_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_hi_max_ar)
GR_CL_min_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_min_ar)
GR_CL_lo_min_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_lo_min_ar)
GR_CL_hi_min_ar = (c_double * loopSize)(*pepParameterDict_GR_CL_hi_min_ar)
NPHI_ar = (c_double * loopSize)(*pepParameterDict_NPHI_ar)
NPHI_lo_ar = (c_double * loopSize)(*pepParameterDict_NPHI_lo_ar)
NPHI_hi_ar = (c_double * loopSize)(*pepParameterDict_NPHI_hi_ar)
NPHI_CL_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_ar)
NPHI_CL_lo_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_lo_ar)
NPHI_CL_hi_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_hi_ar)
NPHI_CL_max_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_max_ar)
NPHI_CL_lo_max_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_lo_max_ar)
NPHI_CL_hi_max_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_hi_max_ar)
NPHI_CL_min_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_min_ar)
NPHI_CL_lo_min_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_lo_min_ar)
NPHI_CL_hi_min_ar = (c_double * loopSize)(*pepParameterDict_NPHI_CL_hi_min_ar)
RHOB_ar = (c_double * loopSize)(*pepParameterDict_RHOB_ar)
RHOB_lo_ar = (c_double * loopSize)(*pepParameterDict_RHOB_lo_ar)
RHOB_hi_ar = (c_double * loopSize)(*pepParameterDict_RHOB_hi_ar)
RHOB_CL_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_ar)
RHOB_CL_lo_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_lo_ar)
RHOB_CL_hi_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_hi_ar)
RHOB_CL_max_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_max_ar)
RHOB_CL_lo_max_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_lo_max_ar)
RHOB_CL_hi_max_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_hi_max_ar)
RHOB_CL_min_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_min_ar)
RHOB_CL_lo_min_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_lo_min_ar)
RHOB_CL_hi_min_ar = (c_double * loopSize)(*pepParameterDict_RHOB_CL_hi_min_ar)
RT_ar = (c_double * loopSize)(*pepParameterDict_RT_ar)
RT_lo_ar = (c_double * loopSize)(*pepParameterDict_RT_lo_ar)
RT_hi_ar = (c_double * loopSize)(*pepParameterDict_RT_hi_ar)
MFRES_ar = (c_double * loopSize)(*pepParameterDict_MFRES_ar)
MFRES_min_ar = (c_double * loopSize)(*pepParameterDict_MFRES_min_ar)
MFRES_max_ar = (c_double * loopSize)(*pepParameterDict_MFRES_max_ar)
M_ar = (c_double * loopSize)(*pepParameterDict_M_ar)
M_min_ar = (c_double * loopSize)(*pepParameterDict_M_min_ar)
M_max_ar = (c_double * loopSize)(*pepParameterDict_M_max_ar)
N_ar = (c_double * loopSize)(*pepParameterDict_N_ar)
N_min_ar = (c_double * loopSize)(*pepParameterDict_N_min_ar)
N_max_ar = (c_double * loopSize)(*pepParameterDict_N_max_ar)
RHOOIL_ar = (c_double * loopSize)(*pepParameterDict_RHOOIL_ar)
RHOOIL_min_ar = (c_double * loopSize)(*pepParameterDict_RHOOIL_min_ar)
RHOOIL_max_ar = (c_double * loopSize)(*pepParameterDict_RHOOIL_max_ar)
RHOGAS_ar = (c_double * loopSize)(*pepParameterDict_RHOGAS_ar)
RHOGAS_min_ar = (c_double * loopSize)(*pepParameterDict_RHOGAS_min_ar)
RHOGAS_max_ar = (c_double * loopSize)(*pepParameterDict_RHOGAS_max_ar)
NEUFAC_ar = (c_double * loopSize)(*pepParameterDict_NEUFAC_ar)
NEUFAC_min_ar = (c_double * loopSize)(*pepParameterDict_NEUFAC_min_ar)
NEUFAC_max_ar = (c_double * loopSize)(*pepParameterDict_NEUFAC_max_ar)
SYNDENSD_ar = (c_double * loopSize)(*pepParameterDict_SYNDENSD_ar)
SYNDENSD_min_ar = (c_double * loopSize)(*pepParameterDict_SYNDENSD_min_ar)
SYNDENSD_max_ar = (c_double * loopSize)(*pepParameterDict_SYNDENSD_max_ar)
SYNDENCL_ar = (c_double * loopSize)(*pepParameterDict_SYNDENCL_ar)
SYNDENCL_min_ar = (c_double * loopSize)(*pepParameterDict_SYNDENCL_min_ar)
SYNDENCL_max_ar = (c_double * loopSize)(*pepParameterDict_SYNDENCL_max_ar)
SILTLINE_RATIO_ar = (c_double * loopSize)(*pepParameterDict_SILTLINE_RATIO_ar)
SILTLINE_RATIO_min_ar = (c_double * loopSize)(*pepParameterDict_SILTLINE_RATIO_min_ar)
SILTLINE_RATIO_max_ar = (c_double * loopSize)(*pepParameterDict_SILTLINE_RATIO_max_ar)
DEGHCCOR_ar = (c_double * loopSize)(*pepParameterDict_DEGHCCOR_ar)
DEGHCCOR_min_ar = (c_double * loopSize)(*pepParameterDict_DEGHCCOR_min_ar)
DEGHCCOR_max_ar = (c_double * loopSize)(*pepParameterDict_DEGHCCOR_max_ar)
RHODRYSL_ar = (c_double * loopSize)(*pepParameterDict_RHODRYSL_ar)
RHODRYSL_min_ar = (c_double * loopSize)(*pepParameterDict_RHODRYSL_min_ar)
RHODRYSL_max_ar = (c_double * loopSize)(*pepParameterDict_RHODRYSL_max_ar)
RHODRYSD_ar = (c_double * loopSize)(*pepParameterDict_RHODRYSD_ar)
RHODRYSD_min_ar = (c_double * loopSize)(*pepParameterDict_RHODRYSD_min_ar)
RHODRYSD_max_ar = (c_double * loopSize)(*pepParameterDict_RHODRYSD_max_ar)
NPHI_DRYSD_ar = (c_double * loopSize)(*pepParameterDict_NPHI_DRYSD_ar)
NPHI_DRYSD_min_ar = (c_double * loopSize)(*pepParameterDict_NPHI_DRYSD_min_ar)
NPHI_DRYSD_max_ar = (c_double * loopSize)(*pepParameterDict_NPHI_DRYSD_max_ar)

Zntemp = (c_double * loopSize)(*[MissingValue]*loopSize)
Zntempunit = (c_double * loopSize)(*[MissingValue]*loopSize)
Znrw77f = (c_double * loopSize)(*[MissingValue]*loopSize)
Znsalwtr = (c_double * loopSize)(*[MissingValue]*loopSize)
Znrw = (c_double * loopSize)(*[MissingValue]*loopSize)
LithmodUpdated = (c_wchar_p * loopSize)(*['']*loopSize)

pcmatdclln = (c_double * loopSize)(*[MissingValue]*loopSize)
pmmatdclln = (c_double * loopSize)(*[MissingValue]*loopSize)
pmclayln = (c_double * loopSize)(*[MissingValue]*loopSize)
pcclayln = (c_double * loopSize)(*[MissingValue]*loopSize)
pnonphidrysand = (c_double * loopSize)(*[MissingValue]*loopSize)
pnonrhodrysand = (c_double * loopSize)(*[MissingValue]*loopSize)
pcons1 = (c_double * loopSize)(*[MissingValue]*loopSize)
pcons2 = (c_double * loopSize)(*[MissingValue]*loopSize)
pcons3 = (c_double * loopSize)(*[MissingValue]*loopSize)
pcons4 = (c_double * loopSize)(*[MissingValue]*loopSize)

Peflith2frac = (c_double * loopSize)(*[MissingValue]*loopSize)
Pefcalcfrac = (c_double * loopSize)(*[MissingValue]*loopSize)
Pefdolofrac = (c_double * loopSize)(*[MissingValue]*loopSize)
Pefqrtzfrac = (c_double * loopSize)(*[MissingValue]*loopSize)
Pefmin1frac = (c_double * loopSize)(*[MissingValue]*loopSize)
Pdlith2frac = (c_double * loopSize)(*[MissingValue]*loopSize)
Pdcalcfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Pddolofrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Pdqrtzfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Pdmin1frac = (c_double * loopSize)(*[MissingValue]*loopSize)
Dnlith2frac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Dncalcfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Dndolofrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Dnqrtzfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Dnmin1frac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Dnclayfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vshdrydn = (c_double * loopSize)(*[MissingValue]*loopSize)
Mncalcfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Mndolofrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Mnqrtzfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Mnmin1frac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Mnmin2frac = (c_double * loopSize)(*[MissingValue]*loopSize)
Nphicc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Rhobcc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Pefcc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Ucc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Nphdrysl = (c_double * loopSize)(*[MissingValue]*loopSize) 
Nphdrycl = (c_double * loopSize)(*[MissingValue]*loopSize) 
Rhodrycl = (c_double * loopSize)(*[MissingValue]*loopSize)
Sndsltfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Clysltfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Siltfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Sandfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Clayfrac = (c_double * loopSize)(*[MissingValue]*loopSize)
Calcfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Dolofrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Qrtzfrac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Min1frac = (c_double * loopSize)(*[MissingValue]*loopSize) 
Min2frac = (c_double * loopSize)(*[MissingValue]*loopSize)
Vshgr = (c_double * loopSize)(*[MissingValue]*loopSize) 
Phit = (c_double * loopSize)(*[MissingValue]*loopSize) 
Phie = (c_double * loopSize)(*[MissingValue]*loopSize) 
Rhog = (c_double * loopSize)(*[MissingValue]*loopSize)
Vsand = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vsilt = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vshale = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vcld = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vclb = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vclw = (c_double * loopSize)(*[MissingValue]*loopSize)
Vcalc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vdolo = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vqrtz = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vmin1 = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vmin2 = (c_double * loopSize)(*[MissingValue]*loopSize)
Phit85 = (c_double * loopSize)(*[MissingValue]*loopSize) 
Phit21 = (c_double * loopSize)(*[MissingValue]*loopSize) 
Nphihc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Rhobhc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Rhobfc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Rhobbc = (c_double * loopSize)(*[MissingValue]*loopSize)
Mxpoint = (c_double * loopSize)(*[MissingValue]*loopSize) 
Nxpoint = (c_double * loopSize)(*[MissingValue]*loopSize) 
Synrhobgr = (c_double * loopSize)(*[MissingValue]*loopSize) 
Phitcly = (c_double * loopSize)(*[MissingValue]*loopSize) 
Phitgm = (c_double * loopSize)(*[MissingValue]*loopSize) 
Sxohc = (c_double * loopSize)(*[MissingValue]*loopSize)
Swe = (c_double * loopSize)(*[MissingValue]*loopSize) 
Swt = (c_double * loopSize)(*[MissingValue]*loopSize) 
Rwapp = (c_double * loopSize)(*[MissingValue]*loopSize) 
Swt_arc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Swe_arc = (c_double * loopSize)(*[MissingValue]*loopSize) 
Swtu = (c_double * loopSize)(*[MissingValue]*loopSize) 
Cw = (c_double * loopSize)(*[MissingValue]*loopSize) 
Bqv = (c_double * loopSize)(*[MissingValue]*loopSize)
Rocal = (c_double * loopSize)(*[MissingValue]*loopSize) 
Qvsyn = (c_double * loopSize)(*[MissingValue]*loopSize) 
Zn_m = (c_double * loopSize)(*[MissingValue]*loopSize) 
Zn_n = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vcoal = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vcoalinit = (c_double * loopSize)(*[MissingValue]*loopSize) 
Coalind = (c_double * loopSize)(*[MissingValue]*loopSize)
Lmstrkind = (c_double * loopSize)(*[MissingValue]*loopSize)
Vwater = (c_double * loopSize)(*[MissingValue]*loopSize)
Voil = (c_double * loopSize)(*[MissingValue]*loopSize)
Vgas = (c_double * loopSize)(*[MissingValue]*loopSize) 
Bmob = (c_double * loopSize)(*[MissingValue]*loopSize) 
Vclinvpor = (c_double * loopSize)(*[MissingValue]*loopSize) 
Cwapp = (c_double * loopSize)(*[MissingValue]*loopSize)

phitMin = (c_double * loopSize)(*[MissingValue]*loopSize)
phitMax = (c_double * loopSize)(*[MissingValue]*loopSize)
phitMean = (c_double * loopSize)(*[MissingValue]*loopSize)
phitP1 = (c_double * loopSize)(*[MissingValue]*loopSize)
phitP2 = (c_double * loopSize)(*[MissingValue]*loopSize)
phitP3 = (c_double * loopSize)(*[MissingValue]*loopSize)

swtMin = (c_double * loopSize)(*[MissingValue]*loopSize)
swtMax = (c_double * loopSize)(*[MissingValue]*loopSize)
swtMean = (c_double * loopSize)(*[MissingValue]*loopSize)
swtP1 = (c_double * loopSize)(*[MissingValue]*loopSize)
swtP2 = (c_double * loopSize)(*[MissingValue]*loopSize)
swtP3 = (c_double * loopSize)(*[MissingValue]*loopSize)

vclwMin = (c_double * loopSize)(*[MissingValue]*loopSize)
vclwMax = (c_double * loopSize)(*[MissingValue]*loopSize)
vclwMean = (c_double * loopSize)(*[MissingValue]*loopSize)
vclwP1 = (c_double * loopSize)(*[MissingValue]*loopSize)
vclwP2 = (c_double * loopSize)(*[MissingValue]*loopSize)
vclwP3 = (c_double * loopSize)(*[MissingValue]*loopSize)

vsiltMin = (c_double * loopSize)(*[MissingValue]*loopSize)
vsiltMax = (c_double * loopSize)(*[MissingValue]*loopSize)
vsiltMean = (c_double * loopSize)(*[MissingValue]*loopSize)
vsiltP1 = (c_double * loopSize)(*[MissingValue]*loopSize)
vsiltP2 = (c_double * loopSize)(*[MissingValue]*loopSize)
vsiltP3 = (c_double * loopSize)(*[MissingValue]*loopSize)

if(DO_MC == 'YES'):
	phitD_List = (c_double * (PHIT_D_LIST_COUNT*loopSize))(*[MissingValue]*(PHIT_D_LIST_COUNT*loopSize))
	swtD_List = (c_double * (SWT_D_LIST_COUNT*loopSize))(*[MissingValue]*(SWT_D_LIST_COUNT*loopSize))
	vclwD_List = (c_double * (VCLW_D_LIST_COUNT*loopSize))(*[MissingValue]*(VCLW_D_LIST_COUNT*loopSize))
	vsiltD_List = (c_double * (VSILT_D_LIST_COUNT*loopSize))(*[MissingValue]*(VSILT_D_LIST_COUNT*loopSize))
else:
	phitD_List = (c_double * 1)(*[MissingValue]*1)
	swtD_List = (c_double * 1)(*[MissingValue]*1)
	vclwD_List = (c_double * 1)(*[MissingValue]*1)
	vsiltD_List = (c_double * 1)(*[MissingValue]*1)

M_LIME = c_double()
N_LIME = c_double()
M_DOLO = c_double()
N_DOLO = c_double()
M_SAND = c_double()
N_SAND = c_double()
N_MIN1 = c_double()
M_MIN1 = c_double()
N_MIN2 = c_double()
M_MIN2 = c_double()
NPHIFLC = c_double()
NPHITOOLDL = c_double()
NPHITOOLQZ = c_double()
PEFFLLM = c_double()
PEFFLDL = c_double()
PEFFLQZ = c_double()
PEFFLMIN1 = c_double()

dataRw = Input_1D_Data()

dataRw.tEMPSOURCE = tEMPSOURCE
dataRw.dEPTHSOURCE = dEPTHSOURCE
dataRw.wELLLOC = wELLLOC
dataRw.sALFLG = sALFLG
dataRw.Md = Md
dataRw.TD_MD = tD_MD
dataRw.Tvdss = Tvdss
dataRw.TD_TVDSS = tD_TVDSS
dataRw.RTKB_DEP = rTKB_DEP
dataRw.GL_DEP = gL_DEP
dataRw.SURF_TEMP = sURF_TEMP
dataRw.SB_DEP = sB_DEP
dataRw.SB_TEMP = sB_TEMP
dataRw.BHT_TEMP = bHT_TEMP		
dataRw.TEMP_LOG = tEMP_LOG
dataRw.SALW = sALW
dataRw.RW = rW
dataRw.Zntemp = Zntemp
dataRw.Zntempunit = Zntempunit
dataRw.Znrw77f = Znrw77f
dataRw.Znsalwtr = Znsalwtr
dataRw.Znrw = Znrw
dataRw.LithmodUpdated = LithmodUpdated
dataRw.HCCOR_VAL = hCCOR_VAL
dataRw.EXT_REF_LOG_VAL = eXT_REF_LOG_VAL
dataRw.CORR_RHOB_LOG_VAL = cORR_RHOB_LOG_VAL
dataRw.BHCTYP_VAL = bHCTYP_VAL
dataRw.COALCUT_VAL = cOALCUT_VAL
dataRw.COALFLG_LOG_VAL = cOALFLG_LOG_VAL
dataRw.STRCUT_VAL = sTRCUT_VAL
dataRw.EXT_PHIT_LOG_VAL = eXT_PHIT_LOG_VAL
dataRw.EXT_PHIE_LOG_VAL = eXT_PHIE_LOG_VAL
dataRw.EXT_VCLD_LOG_VAL = eXT_VCLD_LOG_VAL
dataRw.OTHER_EXT_VCLY_LOG_VAL = oTHER_EXT_VCLY_LOG_VAL
dataRw.OGF_VAL = oGF_VAL
dataRw.CWBGRAD_VAL = cWBGRAD_VAL
dataRw.GR_ar = GR_ar
dataRw.GR_lo_ar = GR_lo_ar
dataRw.GR_hi_ar = GR_hi_ar
dataRw.GR_SD_ar = GR_SD_ar
dataRw.GR_SD_lo_ar = GR_SD_lo_ar
dataRw.GR_SD_hi_ar = GR_SD_hi_ar
dataRw.GR_SD_max_ar = GR_SD_max_ar
dataRw.GR_SD_lo_max_ar = GR_SD_lo_max_ar
dataRw.GR_SD_hi_max_ar = GR_SD_hi_max_ar
dataRw.GR_SD_min_ar = GR_SD_min_ar
dataRw.GR_SD_lo_min_ar = GR_SD_lo_min_ar
dataRw.GR_SD_hi_min_ar = GR_SD_hi_min_ar
dataRw.GR_CL_ar = GR_CL_ar
dataRw.GR_CL_lo_ar = GR_CL_lo_ar
dataRw.GR_CL_hi_ar = GR_CL_hi_ar
dataRw.GR_CL_max_ar = GR_CL_max_ar
dataRw.GR_CL_lo_max_ar = GR_CL_lo_max_ar
dataRw.GR_CL_hi_max_ar = GR_CL_hi_max_ar
dataRw.GR_CL_min_ar = GR_CL_min_ar
dataRw.GR_CL_lo_min_ar = GR_CL_lo_min_ar
dataRw.GR_CL_hi_min_ar = GR_CL_hi_min_ar
dataRw.NPHI_ar = NPHI_ar
dataRw.NPHI_lo_ar = NPHI_lo_ar
dataRw.NPHI_hi_ar = NPHI_hi_ar
dataRw.NPHI_CL_ar = NPHI_CL_ar
dataRw.NPHI_CL_lo_ar = NPHI_CL_lo_ar
dataRw.NPHI_CL_hi_ar = NPHI_CL_hi_ar
dataRw.NPHI_CL_max_ar = NPHI_CL_max_ar
dataRw.NPHI_CL_lo_max_ar = NPHI_CL_lo_max_ar
dataRw.NPHI_CL_hi_max_ar = NPHI_CL_hi_max_ar
dataRw.NPHI_CL_min_ar = NPHI_CL_min_ar
dataRw.NPHI_CL_lo_min_ar = NPHI_CL_lo_min_ar
dataRw.NPHI_CL_hi_min_ar = NPHI_CL_hi_min_ar
dataRw.RHOB_ar = RHOB_ar
dataRw.RHOB_lo_ar = RHOB_lo_ar
dataRw.RHOB_hi_ar = RHOB_hi_ar
dataRw.RHOB_CL_ar = RHOB_CL_ar
dataRw.RHOB_CL_lo_ar = RHOB_CL_lo_ar
dataRw.RHOB_CL_hi_ar = RHOB_CL_hi_ar
dataRw.RHOB_CL_max_ar = RHOB_CL_max_ar
dataRw.RHOB_CL_lo_max_ar = RHOB_CL_lo_max_ar
dataRw.RHOB_CL_hi_max_ar = RHOB_CL_hi_max_ar
dataRw.RHOB_CL_min_ar = RHOB_CL_min_ar
dataRw.RHOB_CL_lo_min_ar = RHOB_CL_lo_min_ar
dataRw.RHOB_CL_hi_min_ar = RHOB_CL_hi_min_ar
dataRw.RT_ar = RT_ar
dataRw.RT_lo_ar = RT_lo_ar
dataRw.RT_hi_ar = RT_hi_ar
dataRw.PEF = pEF
dataRw.DT = dT
dataRw.MFRES_ar = MFRES_ar
dataRw.MFRES_min_ar = MFRES_min_ar
dataRw.MFRES_max_ar = MFRES_max_ar
dataRw.M_ar = M_ar
dataRw.M_min_ar = M_min_ar
dataRw.M_max_ar = M_max_ar
dataRw.N_ar = N_ar
dataRw.N_min_ar = N_min_ar
dataRw.N_max_ar = N_max_ar
dataRw.RHOOIL_ar = RHOOIL_ar
dataRw.RHOOIL_min_ar = RHOOIL_min_ar
dataRw.RHOOIL_max_ar = RHOOIL_max_ar
dataRw.RHOGAS_ar = RHOGAS_ar
dataRw.RHOGAS_min_ar = RHOGAS_min_ar
dataRw.RHOGAS_max_ar = RHOGAS_max_ar
dataRw.NEUFAC_ar = NEUFAC_ar
dataRw.NEUFAC_min_ar = NEUFAC_min_ar
dataRw.NEUFAC_max_ar = NEUFAC_max_ar
dataRw.SYNDENSD_ar = SYNDENSD_ar
dataRw.SYNDENSD_min_ar = SYNDENSD_min_ar
dataRw.SYNDENSD_max_ar = SYNDENSD_max_ar
dataRw.SYNDENCL_ar = SYNDENCL_ar
dataRw.SYNDENCL_min_ar = SYNDENCL_min_ar
dataRw.SYNDENCL_max_ar = SYNDENCL_max_ar
dataRw.SILTLINE_RATIO_ar = SILTLINE_RATIO_ar
dataRw.SILTLINE_RATIO_min_ar = SILTLINE_RATIO_min_ar
dataRw.SILTLINE_RATIO_max_ar = SILTLINE_RATIO_max_ar
dataRw.DEGHCCOR_ar = DEGHCCOR_ar
dataRw.DEGHCCOR_min_ar = DEGHCCOR_min_ar
dataRw.DEGHCCOR_max_ar = DEGHCCOR_max_ar
dataRw.RHODRYSL_ar = RHODRYSL_ar
dataRw.RHODRYSL_min_ar = RHODRYSL_min_ar
dataRw.RHODRYSL_max_ar = RHODRYSL_max_ar
dataRw.RHODRYSD_ar = RHODRYSD_ar
dataRw.RHODRYSD_min_ar = RHODRYSD_min_ar
dataRw.RHODRYSD_max_ar = RHODRYSD_max_ar
dataRw.NPHI_DRYSD_ar = NPHI_DRYSD_ar
dataRw.NPHI_DRYSD_min_ar = NPHI_DRYSD_min_ar
dataRw.NPHI_DRYSD_max_ar = NPHI_DRYSD_max_ar

ret_code = DynaDLL.PEP_Module_A_adj(loopSize, dEPTH, MissingValue,\
		LITHOLOGY_MODEL, DNXPLOTSAND,\
		LITHTYPE, NEUTOOL, GR_CALC, LITH2FLG,\
		HCREF, COR_METHOD, SOURCE_SYN_LOG,\
		SWT_METHOD, cLAY_VOLUME_FLAG_VAL,\
		CLAYFLG, BH_CORR, EXTRHOBFLG, USE_SILT_ANGLE, SWT_FLAG, BYPASS_LITHO_PORO_CALCULATION,\
		QVFLAG, CALCULATED_MSTAR, COALFL, EXTCOAL, CARSTFL, EXTSTREAK, HCC_APP, HCTYPE_FLAG,\
		PEF_DRYLM, PEF_DRYDL, PEF_DRYQZ, PEF_DRYMIN1, PEF_DRYMIN2, PEF_DRYCLY,\
		NPHI_DRYLM, NPHI_DRYDL, NPHI_DRYQZ, NPHI_DRYMIN1, NPHI_DRYMIN2, NPHI_FLUID,\
		RHOB_DRYLM, RHOB_DRYDL, RHOB_DRYQZ, RHOB_DRYMIN1, RHOB_DRYMIN2, RHOB_DRYCLY,\
		RHOB_FLUID, RHOB_FLC, NPHI_OFFSET,\
		NEU_OFFSET, PEF_OFFSET, MFTEMP, DEGFLSLT, QV_LOG, LMSTRKFLG_LOG, COALFLAG_EXPANSION,\
		dataRw,\
		pcmatdclln, pmmatdclln, pmclayln, pcclayln, pnonphidrysand, pnonrhodrysand,\
		pcons1, pcons2, pcons3, pcons4,\
		Peflith2frac, Pefcalcfrac, Pefdolofrac, Pefqrtzfrac, Pefmin1frac,\
		Pdlith2frac, Pdcalcfrac, Pddolofrac, Pdqrtzfrac, Pdmin1frac,\
		Dnlith2frac, Dncalcfrac, Dndolofrac, Dnqrtzfrac, Dnmin1frac, Dnclayfrac, Vshdrydn,\
		Mncalcfrac, Mndolofrac, Mnqrtzfrac, Mnmin1frac, Mnmin2frac,\
		Nphicc, Rhobcc, Pefcc, Ucc, Nphdrysl, Nphdrycl, Rhodrycl,\
		Sndsltfrac, Clysltfrac, Siltfrac, Sandfrac, Clayfrac,\
		Calcfrac, Dolofrac, Qrtzfrac, Min1frac, Min2frac,\
		Vshgr, Phit, Phie, Rhog,\
		Vsand, Vsilt, Vshale, Vcld, Vclb, Vclw,\
		Vcalc, Vdolo, Vqrtz, Vmin1, Vmin2,\
		Phit85, Phit21, Nphihc, Rhobhc, Rhobfc, Rhobbc,\
		Mxpoint, Nxpoint, Synrhobgr, Phitcly, Phitgm, Sxohc,\
		Swe, Swt, Rwapp, Swt_arc, Swe_arc, Swtu, Cw, Bqv,\
		Rocal, Qvsyn, Zn_m, Zn_n, Vcoal, Vcoalinit, Coalind, Lmstrkind,\
		Vwater, Voil, Vgas, Bmob, Vclinvpor, Cwapp,\
		byref(M_LIME), byref(N_LIME), byref(M_DOLO), byref(N_DOLO), byref(M_SAND), byref(N_SAND), byref(N_MIN1), byref(M_MIN1),\
		byref(N_MIN2), byref(M_MIN2), byref(NPHIFLC), byref(NPHITOOLDL), byref(NPHITOOLQZ), byref(PEFFLLM), byref(PEFFLDL),\
		byref(PEFFLQZ), byref(PEFFLMIN1),\
		DO_MC, ITR_NO, P1P, P2P, P3P, PHIT_D_LIST_COUNT, SWT_D_LIST_COUNT, VCLW_D_LIST_COUNT, VSILT_D_LIST_COUNT,\
		RHOB_LOG_DIST, NPHI_LOG_DIST, GR_LOG_DIST,\
		RT_LOG_DIST, RHOB_CL_PAR_DIST, NPHI_CL_PAR_DIST, RHODRYSL_PAR_DIST,\
		GR_CL_PAR_DIST, GR_SD_PAR_DIST, RW_PAR_DIST, CWBGRAD_PAR_DIST,\
		M_PAR_DIST, N_PAR_DIST, NEUFAC_PAR_DIST, RHODRYSD_PAR_DIST,\
		NPHI_DRYSD_PAR_DIST, RHOGAS_PAR_DIST, RHOOIL_PAR_DIST,\
		MFRES_PAR_DIST, SILTLINE_RATIO_PAR_DIST, DEGHCCOR_PAR_DIST,\
		SYNDENSD_PAR_DIST, SYNDENCL_PAR_DIST,\
		phitMin, phitMax, phitMean, phitP1, phitP2, phitP3, phitD_List,\
		swtMin, swtMax, swtMean, swtP1, swtP2, swtP3, swtD_List,\
		vclwMin, vclwMax, vclwMean, vclwP1, vclwP2, vclwP3, vclwD_List,\
		vsiltMin, vsiltMax, vsiltMean, vsiltP1, vsiltP2, vsiltP3, vsiltD_List)
		
if(ret_code == 0):
	dlg.critical('PEP Module', '*** MODULE EXPIRED !! - CONTACT ADMINISTRATOR ***')
	exit(0)
		
MLIME = M_LIME.value
NLIME = N_LIME.value
MDOLO = M_DOLO.value
NDOLO = N_DOLO.value
MSAND = M_SAND.value
NSAND = N_SAND.value
NMIN1 = N_MIN1.value
MMIN1 = M_MIN1.value
NMIN2 = N_MIN2.value
MMIN2 = M_MIN2.value
NPHI_FLC = NPHIFLC.value
NPHI_TOOLDL = NPHITOOLDL.value
NPHI_TOOLQZ = NPHITOOLQZ.value
PEF_FLLM = PEFFLLM.value
PEF_FLDL = PEFFLDL.value
PEF_FLQZ = PEFFLQZ.value
PEF_FLMIN1 = PEFFLMIN1.value

for loopIterator in loopRange:
	lithmod = LithmodUpdated[loopIterator]
	depth = DEPTH.value(loopIterator)
	rhobhcplot_fluid_cst = MissingValue
	nphihcplot_fluid_cst = MissingValue
	rhobhcplot_drysd_cst = MissingValue
	nphihcplot_drysd_cst = MissingValue
	rhobhcplot_drysls_cst = MissingValue
	nphihcplot_drysls_cst = MissingValue
	rhobhcplot_drycls_cst = MissingValue
	nphihcplot_drycls_cst = MissingValue
	rhobhcplot_wetcls_cst = MissingValue
	nphihcplot_wetcls = MissingValue
	nphihcplot = MissingValue
	rhobhcplot = MissingValue
	mxpointplot = MissingValue
	nxpointplot = MissingValue
	
	RW = Znrw[loopIterator]
	
	if SSC_DN_CROSSPLOT=="YES" and lithmod=="SSC":
		if int(depth)==int(TERNARY_DEPTH):
			RHOBHCPLOT_FLUID=RHOB_FLUID
			NPHIHCPLOT_FLUID=NPHI_FLUID
			RHOBHCPLOT_DRYSD=pnonrhodrysand[loopIterator]
			NPHIHCPLOT_DRYSD=pnonphidrysand[loopIterator]
			RHOBHCPLOT_DRYSLS=RHOB_DRY_SLT
			NPHIHCPLOT_DRYSLS=Nphdrysl[loopIterator]
			RHOBHCPLOT_DRYCLS=Rhodrycl[loopIterator]
			NPHIHCPLOT_DRYCLS=Nphdrycl[loopIterator]
			RHOBHCPLOT_WETCLS=RHOB_CL_ar[loopIterator]
			NPHIHCPLOT_WETCLS=NPHI_CL_ar[loopIterator]
			rhobhcplot_fluid_cst=RHOB_FLUID
			nphihcplot_fluid_cst=NPHI_FLUID
			rhobhcplot_drysd_cst=pnonrhodrysand[loopIterator]
			nphihcplot_drysd_cst=pnonphidrysand[loopIterator]
			rhobhcplot_drysls_cst=RHOB_DRY_SLT
			nphihcplot_drysls_cst=Nphdrysl[loopIterator]
			rhobhcplot_drycls_cst=Rhodrycl[loopIterator]
			nphihcplot_drycls_cst=Nphdrycl[loopIterator]
			rhobhcplot_wetcls_cst=RHOB_CL_ar[loopIterator]
			nphihcplot_wetcls_cst=NPHI_CL_ar[loopIterator]
		if depth>(TERNARY_DEPTH - TERNARY_INTERVAL):
			if depth< (TERNARY_DEPTH + TERNARY_INTERVAL):
				rhobhcplot = Rhobhc[loopIterator]
				nphihcplot = Nphihc[loopIterator]

	if int(depth)==int(WATERZONE_DEPTH) and CW_VCLPHIT_PLOT=="YES":
		if RW!=0:
			LINE1_INT = 1/RW
		else:
			LINE1_INT=MissingValue
		LINE1_GRAD = cWBGRAD_VAL[loopIterator]

	if int(depth)==int(WATERZONE_DEPTH) and PICKETT_PLOT=="YES":
		if RW!=0:
			LINE2_INT = RW
		else:
			LINE2_INT=MissingValue
		LINE2_GRAD = M_ar[loopIterator]

	if CARB_XPLOT=="YES" and lithmod=="CARB":
		if int(depth)==int(CARB_TERNARY_DEPTH):
			NPHIHCPLOT_DRYCLS=Nphdrycl[loopIterator]
			RHOBHCPLOT_WETCLS=RHOB_CL_ar[loopIterator]
			NPHIHCPLOT_WETCLS=NPHI_CL_ar[loopIterator]
		if depth>(CARB_TERNARY_DEPTH - CARB_TERNARY_INTERVAL):
			if depth< (CARB_TERNARY_DEPTH + CARB_TERNARY_INTERVAL):
				if (len(LITHTYPE)==7):
					rhobhcplot = Rhobhc[loopIterator]
					nphihcplot = Nphihc[loopIterator]
				elif (len(LITHTYPE)==10):
					rhobhcplot = Rhobcc[loopIterator]
					nphihcplot = Nphicc[loopIterator]
				elif (len(LITHTYPE)==13):
					rhobhcplot = Rhobcc[loopIterator]
					nphihcplot = Nphicc[loopIterator]
					mxpointplot = Mxpoint[loopIterator]
					nxpointplot = Nxpoint[loopIterator]
	
	NPHIHC.setValue(loopIterator, Nphihc[loopIterator])
	PHIE.setValue(loopIterator, Phie[loopIterator])
	PHIT.setValue(loopIterator, Phit[loopIterator])
	RHOBBC.setValue(loopIterator, Rhobbc[loopIterator])
	RHOBFC.setValue(loopIterator, Rhobfc[loopIterator])
	RHOBHC.setValue(loopIterator, Rhobhc[loopIterator])
	VCALC.setValue(loopIterator, Vcalc[loopIterator])
	VCLB.setValue(loopIterator, Vclb[loopIterator])
	VCLD.setValue(loopIterator, Vcld[loopIterator])
	VCLW.setValue(loopIterator, Vclw[loopIterator])
	VCOAL.setValue(loopIterator, Vcoal[loopIterator])
	VDOLO.setValue(loopIterator, Vdolo[loopIterator])
	VGAS.setValue(loopIterator, Vgas[loopIterator])
	VMIN1.setValue(loopIterator, Vmin1[loopIterator])
	VMIN2.setValue(loopIterator, Vmin2[loopIterator])
	VOIL.setValue(loopIterator, Voil[loopIterator])
	VQRTZ.setValue(loopIterator, Vqrtz[loopIterator])
	VSAND.setValue(loopIterator, Vsand[loopIterator])
	VSHALE.setValue(loopIterator, Vshale[loopIterator])
	VSILT.setValue(loopIterator, Vsilt[loopIterator])
	VWATER.setValue(loopIterator, Vwater[loopIterator])
	BQV.setValue(loopIterator, Bqv[loopIterator])
	CALCFRAC.setValue(loopIterator, Calcfrac[loopIterator])
	CLAYFRAC.setValue(loopIterator, Clayfrac[loopIterator])
	CLYSLTFRAC.setValue(loopIterator, Clysltfrac[loopIterator])
	COALIND.setValue(loopIterator, Coalind[loopIterator])
	CW.setValue(loopIterator, Cw[loopIterator])
	CWAPP.setValue(loopIterator, Cwapp[loopIterator])
	DNCALCFRAC.setValue(loopIterator, Dncalcfrac[loopIterator])
	DNCLAYFRAC.setValue(loopIterator, Dnclayfrac[loopIterator])
	DNDOLOFRAC.setValue(loopIterator, Dndolofrac[loopIterator])
	DNLITH2FRAC.setValue(loopIterator, Dnlith2frac[loopIterator])
	DNMIN1FRAC.setValue(loopIterator, Dnmin1frac[loopIterator])
	DNQRTZFRAC.setValue(loopIterator, Dnqrtzfrac[loopIterator])
	DOLOFRAC.setValue(loopIterator, Dolofrac[loopIterator])
	GR_HI.setValue(loopIterator, GR_hi_ar[loopIterator])
	GR_LO.setValue(loopIterator, GR_lo_ar[loopIterator])
	LMSTRKIND.setValue(loopIterator, Lmstrkind[loopIterator])
	MIN1FRAC.setValue(loopIterator, Min1frac[loopIterator])
	MIN2FRAC.setValue(loopIterator, Min2frac[loopIterator])
	MNCALCFRAC.setValue(loopIterator, Mncalcfrac[loopIterator])
	MNDOLOFRAC.setValue(loopIterator, Mndolofrac[loopIterator])
	MNMIN1FRAC.setValue(loopIterator, Mnmin1frac[loopIterator])
	MNMIN2FRAC.setValue(loopIterator, Mnmin2frac[loopIterator])
	MNQRTZFRAC.setValue(loopIterator, Mnqrtzfrac[loopIterator])
	#MPLOT.setValue(loopIterator, mplot)
	ZN_M.setValue(loopIterator, Zn_m[loopIterator])
	MXPOINT.setValue(loopIterator, Mxpoint[loopIterator])
	NPHDRYCL.setValue(loopIterator, Nphdrycl[loopIterator])
	NPHDRYSL.setValue(loopIterator, Nphdrysl[loopIterator])
	NPHICC.setValue(loopIterator, Nphicc[loopIterator])
	NPHI_HI.setValue(loopIterator, NPHI_hi_ar[loopIterator])
	NPHI_LO.setValue(loopIterator, NPHI_lo_ar[loopIterator])
	ZN_N.setValue(loopIterator, Zn_n[loopIterator])
	NXPOINT.setValue(loopIterator, Nxpoint[loopIterator])
	PDCALCFRAC.setValue(loopIterator, Pdcalcfrac[loopIterator])
	PDDOLOFRAC.setValue(loopIterator, Pddolofrac[loopIterator])
	PDLITH2FRAC.setValue(loopIterator, Pdlith2frac[loopIterator])
	PDMIN1FRAC.setValue(loopIterator, Pdmin1frac[loopIterator])
	PDQRTZFRAC.setValue(loopIterator, Pdqrtzfrac[loopIterator])
	PEFCALCFRAC.setValue(loopIterator, Pefcalcfrac[loopIterator])
	PEFCC.setValue(loopIterator, Pefcc[loopIterator])
	PEFDOLOFRAC.setValue(loopIterator, Pefdolofrac[loopIterator])
	PEFLITH2FRAC.setValue(loopIterator, Peflith2frac[loopIterator])
	PEFMIN1FRAC.setValue(loopIterator, Pefmin1frac[loopIterator])
	PEFQRTZFRAC.setValue(loopIterator, Pefqrtzfrac[loopIterator])
	PHIT21.setValue(loopIterator, Phit21[loopIterator])
	PHIT85.setValue(loopIterator, Phit85[loopIterator])
	PHITCLY.setValue(loopIterator, Phitcly[loopIterator])
	PHITGM.setValue(loopIterator, Phitgm[loopIterator])
	QRTZFRAC.setValue(loopIterator, Qrtzfrac[loopIterator])
	QVSYN.setValue(loopIterator, Qvsyn[loopIterator])
	RHOBCC.setValue(loopIterator, Rhobcc[loopIterator])
	RHOB_HI.setValue(loopIterator, RHOB_hi_ar[loopIterator])
	RHOB_LO.setValue(loopIterator, RHOB_lo_ar[loopIterator])
	RHODRYCL.setValue(loopIterator, Rhodrycl[loopIterator])
	RHODRYSL.setValue(loopIterator, RHODRYSL_ar[loopIterator])
	RHOG.setValue(loopIterator, Rhog[loopIterator])
	ROCAL.setValue(loopIterator, Rocal[loopIterator])
	RT_HI.setValue(loopIterator, RT_hi_ar[loopIterator])
	RT_LO.setValue(loopIterator, RT_lo_ar[loopIterator])
	RWAPP.setValue(loopIterator, Rwapp[loopIterator])
	SANDFRAC.setValue(loopIterator, Sandfrac[loopIterator])
	SILTFRAC.setValue(loopIterator, Siltfrac[loopIterator])
	SNDSLTFRAC.setValue(loopIterator, Sndsltfrac[loopIterator])
	SWTU.setValue(loopIterator, Swtu[loopIterator])
	SWE.setValue(loopIterator, Swe[loopIterator])
	SWT.setValue(loopIterator, Swt[loopIterator])
	SWT_ARC.setValue(loopIterator, Swt_arc[loopIterator])
	SWE_ARC.setValue(loopIterator, Swe_arc[loopIterator])
	SYNRHOBGR.setValue(loopIterator, Synrhobgr[loopIterator])
	UCC.setValue(loopIterator, Ucc[loopIterator])
	VCLINVPOR.setValue(loopIterator, Vclinvpor[loopIterator])
	VSHDRYDN.setValue(loopIterator, Vshdrydn[loopIterator])
	VSHGR.setValue(loopIterator, Vshgr[loopIterator])
	ZNCOALCUT.setValue(loopIterator, cOALCUT_VAL[loopIterator])
	ZNCWBGRAD.setValue(loopIterator, cWBGRAD_VAL[loopIterator])
	ZNSLTLINRAT.setValue(loopIterator, SILTLINE_RATIO_ar[loopIterator])
	ZNGRCL.setValue(loopIterator, GR_CL_ar[loopIterator])
	ZNGRSD.setValue(loopIterator, GR_SD_ar[loopIterator])
	ZNBHCOR.setValue(loopIterator, bHCTYP_VAL[loopIterator])
	ZNHCOR.setValue(loopIterator, hCCOR_VAL[loopIterator])
	ZNNPHICL.setValue(loopIterator, NPHI_CL_ar[loopIterator])
	ZNOGF.setValue(loopIterator, oGF_VAL[loopIterator])
	ZNRHOBCL.setValue(loopIterator, RHOB_CL_ar[loopIterator])
	#ZNRSH.setValue(loopIterator, znrsh[loopIterator])
	ZNRW.setValue(loopIterator, Znrw[loopIterator])
	ZNRW77F.setValue(loopIterator, Znrw77f[loopIterator])
	ZNSALWTR.setValue(loopIterator, Znsalwtr[loopIterator])
	ZNSTRKCUT.setValue(loopIterator, sTRCUT_VAL[loopIterator])
	ZNSYNRCL.setValue(loopIterator, SYNDENCL_ar[loopIterator])
	ZNSYNRSD.setValue(loopIterator, SYNDENSD_ar[loopIterator])
	ZNTEMP.setValue(loopIterator, Zntemp[loopIterator])
	VCOALINIT.setValue(loopIterator, Vcoalinit[loopIterator])
	RHOBHCPLOT_FLUID_CST.setValue(loopIterator, rhobhcplot_fluid_cst)
	NPHIHCPLOT_FLUID_CST.setValue(loopIterator, nphihcplot_fluid_cst)
	RHOBHCPLOT_DRYSD_CST.setValue(loopIterator, rhobhcplot_drysd_cst)
	NPHIHCPLOT_DRYSD_CST.setValue(loopIterator, nphihcplot_drysd_cst)
	RHOBHCPLOT_DRYSLS_CST.setValue(loopIterator, rhobhcplot_drysls_cst)
	NPHIHCPLOT_DRYSLS_CST.setValue(loopIterator, nphihcplot_drysls_cst)
	RHOBHCPLOT_DRYCLS_CST.setValue(loopIterator, rhobhcplot_drycls_cst)
	NPHIHCPLOT_DRYCLS_CST.setValue(loopIterator, nphihcplot_drycls_cst)
	RHOBHCPLOT_WETCLS_CST.setValue(loopIterator, rhobhcplot_wetcls_cst)
	NPHIHCPLOT_WETCLS_CST.setValue(loopIterator, nphihcplot_wetcls)
	NPHIHCPLOT.setValue(loopIterator, nphihcplot)
	RHOBHCPLOT.setValue(loopIterator, rhobhcplot)
	MXPOINTPLOT.setValue(loopIterator, mxpointplot)
	NXPOINTPLOT.setValue(loopIterator, nxpointplot)
	SXOHC.setValue(loopIterator, Sxohc[loopIterator])
	BMOB.setValue(loopIterator, Bmob[loopIterator])
	
	if(DO_MC == 'YES'):
		VCLW_MAX.setValue(loopIterator, vclwMax[loopIterator])
		VCLW_MEAN.setValue(loopIterator, vclwMean[loopIterator])
		VCLW_MIN.setValue(loopIterator, vclwMin[loopIterator])
		VCLW_1P.setValue(loopIterator, vclwP1[loopIterator])
		VCLW_2P.setValue(loopIterator, vclwP2[loopIterator])
		VCLW_3P.setValue(loopIterator, vclwP3[loopIterator])
		for k in range(VCLW_D_LIST_COUNT):
			VCLW_D.setValue(loopIterator, k, vclwD_List[loopIterator * VCLW_D_LIST_COUNT + k])
	
		VSILT_MAX.setValue(loopIterator, vsiltMax[loopIterator])
		VSILT_MEAN.setValue(loopIterator, vsiltMean[loopIterator])
		VSILT_MIN.setValue(loopIterator, vsiltMin[loopIterator])
		VSILT_1P.setValue(loopIterator, vsiltP1[loopIterator])
		VSILT_2P.setValue(loopIterator, vsiltP2[loopIterator])
		VSILT_3P.setValue(loopIterator, vsiltP3[loopIterator])
		for k in range(VSILT_D_LIST_COUNT):
			VSILT_D.setValue(loopIterator, k, vsiltD_List[loopIterator * VSILT_D_LIST_COUNT + k])
	
		PHIT_MAX.setValue(loopIterator, phitMax[loopIterator])
		PHIT_MEAN.setValue(loopIterator, phitMean[loopIterator])
		PHIT_MIN.setValue(loopIterator, phitMin[loopIterator])
		PHIT_1P.setValue(loopIterator, phitP1[loopIterator])
		PHIT_2P.setValue(loopIterator, phitP2[loopIterator])
		PHIT_3P.setValue(loopIterator, phitP3[loopIterator])
		for k in range(PHIT_D_LIST_COUNT):
			PHIT_D.setValue(loopIterator, k, phitD_List[loopIterator * PHIT_D_LIST_COUNT + k])
			
		SWT_MAX.setValue(loopIterator, swtMax[loopIterator])
		SWT_MEAN.setValue(loopIterator, swtMean[loopIterator])
		SWT_MIN.setValue(loopIterator, swtMin[loopIterator])
		SWT_1P.setValue(loopIterator, swtP1[loopIterator])
		SWT_2P.setValue(loopIterator, swtP2[loopIterator])
		SWT_3P.setValue(loopIterator, swtP3[loopIterator])
		for k in range(SWT_D_LIST_COUNT):
			SWT_D.setValue(loopIterator, k, swtD_List[loopIterator * SWT_D_LIST_COUNT + k])


NPHIHC.save(False)
PHIE.save(False)
PHIT.save(False)
PHIT_MAX.save(False)
PHIT_MIN.save(False)
RHOBBC.save(False)
RHOBFC.save(False)
RHOBHC.save(False)
VCALC.save(False)
VCLB.save(False)
VCLD.save(False)
VCLW.save(False)
VCLW_MAX.save(False)
VCLW_MIN.save(False)
VCOAL.save(False)
VDOLO.save(False)
VGAS.save(False)
VMIN1.save(False)
VMIN2.save(False)
VOIL.save(False)
VQRTZ.save(False)
VSAND.save(False)
VSHALE.save(False)
VSILT.save(False)
VSILT_MAX.save(False)
VSILT_MIN.save(False)
VWATER.save(False)
BQV.save(False)
CALCFRAC.save(False)
CLAYFRAC.save(False)
CLYSLTFRAC.save(False)
COALIND.save(False)
CW.save(False)
CWAPP.save(False)
DNCALCFRAC.save(False)
DNCLAYFRAC.save(False)
DNDOLOFRAC.save(False)
DNLITH2FRAC.save(False)
DNMIN1FRAC.save(False)
DNQRTZFRAC.save(False)
DOLOFRAC.save(False)
GR_HI.save(False)
GR_LO.save(False)
LMSTRKIND.save(False)
MIN1FRAC.save(False)
MIN2FRAC.save(False)
MNCALCFRAC.save(False)
MNDOLOFRAC.save(False)
MNMIN1FRAC.save(False)
MNMIN2FRAC.save(False)
MNQRTZFRAC.save(False)
MPLOT.save(False)
ZN_M.save(False)
MXPOINT.save(False)
NPHDRYCL.save(False)
NPHDRYSL.save(False)
NPHICC.save(False)
NPHI_HI.save(False)
NPHI_LO.save(False)
ZN_N.save(False)
NXPOINT.save(False)
PDCALCFRAC.save(False)
PDDOLOFRAC.save(False)
PDLITH2FRAC.save(False)
PDMIN1FRAC.save(False)
PDQRTZFRAC.save(False)
PEFCALCFRAC.save(False)
PEFCC.save(False)
PEFDOLOFRAC.save(False)
PEFLITH2FRAC.save(False)
PEFMIN1FRAC.save(False)
PEFQRTZFRAC.save(False)
PHIT21.save(False)
PHIT85.save(False)
PHITCLY.save(False)
PHITGM.save(False)
PHIT_1P.save(False)
PHIT_2P.save(False)
PHIT_3P.save(False)
PHIT_D.save(False)
PHIT_MEAN.save(False)
QRTZFRAC.save(False)
QVSYN.save(False)
RHOBCC.save(False)
RHOB_HI.save(False)
RHOB_LO.save(False)
RHODRYCL.save(False)
RHODRYSL.save(False)
RHOG.save(False)
ROCAL.save(False)
RT_HI.save(False)
RT_LO.save(False)
RWAPP.save(False)
SANDFRAC.save(False)
SILTFRAC.save(False)
SNDSLTFRAC.save(False)
SWTU.save(False)
SWE.save(False)
SWT.save(False)
SWE_ARC.save(False)
SWT_ARC.save(False)
SWT_MAX.save(False)
SWT_MIN.save(False)
SWT_MEAN.save(False)
SWT_1P.save(False)
SWT_2P.save(False)
SWT_3P.save(False)
SWT_D.save(False)
SYNRHOBGR.save(False)
UCC.save(False)
VCLINVPOR.save(False)
VCLW_1P.save(False)
VCLW_2P.save(False)
VCLW_3P.save(False)
VCLW_D.save(False)
VCLW_MEAN.save(False)
VSHDRYDN.save(False)
VSHGR.save(False)
VSILT_1P.save(False)
VSILT_2P.save(False)
VSILT_3P.save(False)
VSILT_D.save(False)
VSILT_MEAN.save(False)
ZNCOALCUT.save(False)
ZNCWBGRAD.save(False)
ZNSLTLINRAT.save(False)
ZNGRCL.save(False)
ZNGRSD.save(False)
ZNBHCOR.save(False)
ZNHCOR.save(False)
ZNNPHICL.save(False)
ZNOGF.save(False)
ZNRHOBCL.save(False)
ZNRSH.save(False)
ZNRW.save(False)
ZNRW77F.save(False)
ZNSALWTR.save(False)
ZNSTRKCUT.save(False)
ZNSYNRCL.save(False)
ZNSYNRSD.save(False)
ZNTEMP.save(False)
VCOALINIT.save(False)
RHOBHCPLOT_FLUID_CST.save(False)
NPHIHCPLOT_FLUID_CST.save(False)
RHOBHCPLOT_DRYSD_CST.save(False)
NPHIHCPLOT_DRYSD_CST.save(False)
RHOBHCPLOT_DRYSLS_CST.save(False)
NPHIHCPLOT_DRYSLS_CST.save(False)
RHOBHCPLOT_DRYCLS_CST.save(False)
NPHIHCPLOT_DRYCLS_CST.save(False)
RHOBHCPLOT_WETCLS_CST.save(False)
NPHIHCPLOT_WETCLS_CST.save(False)
NPHIHCPLOT.save(False)
RHOBHCPLOT.save(False)
MXPOINTPLOT.save(False)
NXPOINTPLOT.save(False)
SXOHC.save(False)
BMOB.save(False)

FreeLibrary(DynaDLL._handle)
	
db.progressBarHide()


###################### Displaying the Layouts ###############################################

if (DisplayLayout=='YES'):

	if UseGraphicalParameterPicking=='YES':
		if LITHOLOGY_MODEL == "SSC":
			logview_name = "PEP_SSC_Graphical "+w
			Lid = plot.logViewGetIdByName(logview_name)
			if Lid==-1:
				if db.objectExists(logview_name,db.objectTypeList().index("Layout"),'project'):
					Lid = plot.logViewOpen("Project\\PEP_SSC_Graphical "+w+".xml",'project',0)
				elif db.objectExists(logview_name,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_SSC_Graphical "+w+".xml",w,False)
					plot.logViewSave(Lid,logview_name,"Project",0)
				elif db.versionTest(2015, 0, 0):
					###Creating a dialog box when the layout wasn't found.
					###Consider adding a property on the well header to know whether or not PEP module has run on the well
					###And when the property isn't there, don't show the pop up and open the initial template without dialog
					import TechlogDialogAdvanced as tda
					LayoutList = db.objectList("Layout")
					LayoutList.insert(0,"Template")
					dlg = tda.dialogAdvanced("Interpretation Layout Status")
					dlg.addLabel("Label1","The interpretation layout for this well, 'PEP_SSC_Graphical "+w+r"' is not available.\nIt can be created either from the template or from the existing one.\n")
					dlg.addListInput("layoutListInput","Choose the source of layout:",LayoutList,0,False,"Select here the layout where an interpretation is available")
					dlg.addLabel("Label2","Press Cancel to exit the process")
					if dlg.execDialog(True):
						LayoutName = dlg.getListInput("layoutListInput")
						if LayoutName == "Template":
							Lid = plot.logViewApplyTemplate("Company\\PEP_SSC_Graphical.xml",w,False)
							plot.logViewSave(Lid,logview_name,"Project",0)
						else:
							Lid = plot.logViewOpen("Project\\"+LayoutName+".xml",'project',0)
					else:
						exit(0)
				else:
					Lid = plot.logViewApplyTemplate("Company\\PEP_SSC_Graphical.xml",w,False)
					plot.logViewSave(Lid,logview_name,"Project",0)
					
				plot.logViewSetName(Lid,logview_name)
				#if u=="FT" or u=="FEET":
				if (u!="M" and u!="m" and u!="METRES" and u!="METERS" and u!="METER" and u!="meter"):
					plot.logViewSetReferenceUnit(Lid,"FEET")
			else:
				plot.logViewSave(Lid,logview_name,"Project",0)	

		if LITHOLOGY_MODEL == "CARB":
			logview_name = "PEP_CARB_Graphical "+w
			Lid = plot.logViewGetIdByName(logview_name)
			if Lid==-1:
				if db.objectExists("PEP_CARB_Graphical "+w,db.objectTypeList().index("Layout"),'project'):
					Lid = plot.logViewOpen("Project\\PEP_CARB_Graphical "+w+".xml",'project',0)
				elif db.objectExists("PEP_CARB_Graphical "+w,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_CARB_Graphical "+w+".xml",w,False)
					plot.logViewSave(Lid,"PEP_CARB_Graphical "+w,"Project",0)
				elif db.versionTest(2015, 0, 0):
					###Creating a dialog box when the layout wasn't found.
					###Consider adding a property on the well header to know whether or not PEP module has run on the well
					###And when the property isn't there, don't show the pop up and open the initial template without dialog
					import TechlogDialogAdvanced as tda
					LayoutList = db.objectList("Layout")
					LayoutList.insert(0,"Template")
					dlg = tda.dialogAdvanced("Interpretation Layout Status")
					dlg.addLabel("Label1","The interpretation layout for this well, 'PEP_CARB_Graphical "+w+r"' is not available.\nIt can be created either from the template or from the existing one.\n")
					dlg.addListInput("layoutListInput","Choose the source of layout:",LayoutList,0,False,"Select here the layout where an interpretation is available")
					dlg.addLabel("Label2","Press Cancel to exit the process")
					if dlg.execDialog(True):
						LayoutName = dlg.getListInput("layoutListInput")
						if LayoutName == "Template":
							Lid = plot.logViewApplyTemplate("Company\\PEP_CARB_Graphical.xml",w,False)
							plot.logViewSave(Lid,logview_name,"Project",0)
						else:
							Lid = plot.logViewOpen("Project\\"+LayoutName+".xml",'project',0)
					else:
						exit(0)
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
			logview_name = "PEP_SSC_Zonation "+w
			Lid = plot.logViewGetIdByName(logview_name)
			if Lid==-1:
				if db.objectExists(logview_name,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_SSC_Zonation "+w+".xml",w,False)
				else:
					Lid = plot.logViewApplyTemplate("Company\\PEP_SSC_Zonation.xml",w,False)
					
				plot.logViewSetName(Lid,logview_name)
				if (u!="M" and u!="m" and u!="METRES" and u!="METERS" and u!="METER" and u!="meter"):
					plot.logViewSetReferenceUnit(Lid,"FEET")

		if LITHOLOGY_MODEL == "CARB":
			logview_name = "PEP_CARB_Zonation "+w
			Lid = plot.logViewGetIdByName(logview_name)
			if Lid==-1:
				if db.objectExists(logview_name,db.objectTypeList().index("LayoutTemplate"),'project'):
					Lid = plot.logViewApplyTemplate("Project\\PEP_CARB_Zonation "+w+".xml",w,False)
				else:
					Lid = plot.logViewApplyTemplate("Company\\PEP_CARB_Zonation.xml",w,False)
					
				plot.logViewSetName(Lid,logview_name)
				if (u!="M" and u!="m" and u!="METRES" and u!="METERS" and u!="METER" and u!="meter"):
					plot.logViewSetReferenceUnit(Lid,"FEET")



###################### Displaying the Crossplots ###############################################

if (SSC_DN_CROSSPLOT=="YES" and LITHOLOGY_MODEL=="SSC"):

	idCP = plot.crossPlotIDFindByName("SSC D-N Crossplot "+DEPTH.wellName())
	if idCP == -1:
		idCP=plot.crossPlotCreate("SSC D-N Crossplot "+DEPTH.wellName(),DEPTH.wellName()+"."+DEPTH.datasetName()+"."+NPHIHCPLOT.variableName()+__suffix__,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+RHOBHCPLOT.variableName()+__suffix__)
		plot.setLegendVisible(idCP, True)
		plot.crossPlotDensityType(idCP, 1)
		plot.crossPlotSetColor(idCP,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+DEPTH.variableName()+__suffix__)
		plot.crossPlotSetYAxisUserLimits(idCP,2.9,0.9)
		plot.crossPlotSetXAxisUserLimits(idCP,-0.2,1.1)
		plot.crossPlotDensityType(idCP,0)
		
	if idCP!=-1:
		plot.crossPlotRemoveAllEquations(idCP)
		plot.crossPlotRemoveAllParameterPoint(idCP)
		
		#if no zonation is selected
		if 'pythonEditor' not in locals() or pythonEditor:
			if "zonationDataset" not in locals():
				zonationDataset = ''
				zoneList = ['']
		else:
			zoneList = [zoneName]
		
		plot.crossPlotSetZonation(idCP, zonationDataset)

		cnonmatdclln = MissingValue
		idDRYSD1 = MissingValue
		idDRYSD2 = MissingValue
		idDRYSD3 = MissingValue
		idDRYSD4 = MissingValue
		idDRYSD5 = MissingValue
		idDRYSD6 = MissingValue
		idDRYSD7 = MissingValue
		idDRYSLS1 = MissingValue

		for zoneName in zoneList:
			idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_FLUID', NPHIHCPLOT_FLUID, NPHIHCPLOT_FLUID, NPHIHCPLOT_FLUID, 'RHOBPLOT_FLUID', RHOBHCPLOT_FLUID, RHOBHCPLOT_FLUID, RHOBHCPLOT_FLUID)
			idWETCLS = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_CLY', NPHIHCPLOT_WETCLS, NPHIHCPLOT_WETCLS, NPHIHCPLOT_WETCLS, 'RHOBPLOT_CLY', RHOBHCPLOT_WETCLS, RHOBHCPLOT_WETCLS, RHOBHCPLOT_WETCLS)
			idDRYSD = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND_MA', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND_MA', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
			idDRYSLS = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_DRY_SLT', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_DRY_SLT', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)
			idDRYCLS = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIHCPLOT_DRYCLS', NPHIHCPLOT_DRYCLS, NPHIHCPLOT_DRYCLS, NPHIHCPLOT_DRYCLS, 'RHOBHCPLOT_DRYCLY', RHOBHCPLOT_DRYCLS, RHOBHCPLOT_DRYCLS, RHOBHCPLOT_DRYCLS)

			nonsiltfrac = (RHOBHCPLOT_DRYSLS-RHOBHCPLOT_DRYSD)/(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
			mclayln = (RHOBHCPLOT_DRYCLS-RHOBHCPLOT_FLUID)/(NPHIHCPLOT_DRYCLS-NPHIHCPLOT_FLUID)
			cclayln = RHOBHCPLOT_FLUID-mclayln*NPHIHCPLOT_FLUID
			mmatdclln = (RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)/(NPHIHCPLOT_DRYCLS-(NPHIHCPLOT_DRYSD-NPHI_OFFSET))
			cmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)
			
			if (DNXPLOTSAND=='LINEAR') :
				#Link the points together
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYSD, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYSLS, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYCLS, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD, idDRYCLS, 3)

			else:
				NPHIHCPLOT_DRYSD = 0.05+NPHI_OFFSET
				RHOBHCPLOT_DRYSD = cons1*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**3+cons2*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**2+cons3*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)+cons4
				cnonmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*NPHIHCPLOT_DRYSD
				NPHIHCPLOT_DRYCLS = (cnonmatdclln-cclayln)/(mclayln-mmatdclln)
				RHOBHCPLOT_DRYCLS = NPHIHCPLOT_DRYCLS*mclayln+cclayln
				RHOBHCPLOT_DRYSLS = RHOBHCPLOT_DRYSD+nonsiltfrac*(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
				NPHIHCPLOT_DRYSLS = (RHOBHCPLOT_DRYSLS-cnonmatdclln)/mmatdclln
				idDRYSD1 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND1', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND1', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
				idDRYSLS1 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SILT1', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_SILT1', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)

				NPHIHCPLOT_DRYSD = 0.1+NPHI_OFFSET
				RHOBHCPLOT_DRYSD = cons1*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**3+cons2*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**2+cons3*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)+cons4
				cnonmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*NPHIHCPLOT_DRYSD
				NPHIHCPLOT_DRYCLS = (cnonmatdclln-cclayln)/(mclayln-mmatdclln)
				RHOBHCPLOT_DRYCLS = NPHIHCPLOT_DRYCLS*mclayln+cclayln
				RHOBHCPLOT_DRYSLS = RHOBHCPLOT_DRYSD+nonsiltfrac*(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
				NPHIHCPLOT_DRYSLS = (RHOBHCPLOT_DRYSLS-cnonmatdclln)/mmatdclln
				idDRYSD2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND2', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND2', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
				idDRYSLS2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SILT2', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_SILT2', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)

				NPHIHCPLOT_DRYSD = 0.15+NPHI_OFFSET
				RHOBHCPLOT_DRYSD = cons1*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**3+cons2*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**2+cons3*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)+cons4
				cnonmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*NPHIHCPLOT_DRYSD
				NPHIHCPLOT_DRYCLS = (cnonmatdclln-cclayln)/(mclayln-mmatdclln)
				RHOBHCPLOT_DRYCLS = NPHIHCPLOT_DRYCLS*mclayln+cclayln
				RHOBHCPLOT_DRYSLS = RHOBHCPLOT_DRYSD+nonsiltfrac*(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
				NPHIHCPLOT_DRYSLS = (RHOBHCPLOT_DRYSLS-cnonmatdclln)/mmatdclln
				idDRYSD3 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND3', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND3', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
				idDRYSLS3 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SILT3', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_SILT3', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)

				NPHIHCPLOT_DRYSD = 0.20+NPHI_OFFSET
				RHOBHCPLOT_DRYSD = cons1*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**3+cons2*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**2+cons3*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)+cons4
				cnonmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*NPHIHCPLOT_DRYSD
				NPHIHCPLOT_DRYCLS = (cnonmatdclln-cclayln)/(mclayln-mmatdclln)
				RHOBHCPLOT_DRYCLS = NPHIHCPLOT_DRYCLS*mclayln+cclayln
				RHOBHCPLOT_DRYSLS = RHOBHCPLOT_DRYSD+nonsiltfrac*(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
				NPHIHCPLOT_DRYSLS = (RHOBHCPLOT_DRYSLS-cnonmatdclln)/mmatdclln
				idDRYSD4 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND4', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND4', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
				idDRYSLS4 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SILT4', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_SILT4', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)

				NPHIHCPLOT_DRYSD = 0.25+NPHI_OFFSET
				RHOBHCPLOT_DRYSD = cons1*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**3+cons2*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**2+cons3*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)+cons4
				cnonmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*NPHIHCPLOT_DRYSD
				NPHIHCPLOT_DRYCLS = (cnonmatdclln-cclayln)/(mclayln-mmatdclln)
				RHOBHCPLOT_DRYCLS = NPHIHCPLOT_DRYCLS*mclayln+cclayln
				RHOBHCPLOT_DRYSLS = RHOBHCPLOT_DRYSD+nonsiltfrac*(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
				NPHIHCPLOT_DRYSLS = (RHOBHCPLOT_DRYSLS-cnonmatdclln)/mmatdclln
				idDRYSD5 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND5', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND5', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
				idDRYSLS5 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SILT5', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_SILT5', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)

				NPHIHCPLOT_DRYSD = 0.30+NPHI_OFFSET
				RHOBHCPLOT_DRYSD = cons1*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**3+cons2*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**2+cons3*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)+cons4
				cnonmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*NPHIHCPLOT_DRYSD
				NPHIHCPLOT_DRYCLS = (cnonmatdclln-cclayln)/(mclayln-mmatdclln)
				RHOBHCPLOT_DRYCLS = NPHIHCPLOT_DRYCLS*mclayln+cclayln
				RHOBHCPLOT_DRYSLS = RHOBHCPLOT_DRYSD+nonsiltfrac*(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
				NPHIHCPLOT_DRYSLS = (RHOBHCPLOT_DRYSLS-cnonmatdclln)/mmatdclln
				idDRYSD6 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND6', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND6', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
				idDRYSLS6 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SILT6', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_SILT6', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)

				NPHIHCPLOT_DRYSD = 0.35+NPHI_OFFSET
				RHOBHCPLOT_DRYSD = cons1*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**3+cons2*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)**2+cons3*(NPHIHCPLOT_DRYSD-NPHI_OFFSET)+cons4
				cnonmatdclln = RHOBHCPLOT_DRYSD-mmatdclln*NPHIHCPLOT_DRYSD
				NPHIHCPLOT_DRYCLS = (cnonmatdclln-cclayln)/(mclayln-mmatdclln)
				RHOBHCPLOT_DRYCLS = NPHIHCPLOT_DRYCLS*mclayln+cclayln
				RHOBHCPLOT_DRYSLS = RHOBHCPLOT_DRYSD+nonsiltfrac*(RHOBHCPLOT_DRYCLS-RHOBHCPLOT_DRYSD)
				NPHIHCPLOT_DRYSLS = (RHOBHCPLOT_DRYSLS-cnonmatdclln)/mmatdclln
				idDRYSD7 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SAND7', NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, NPHIHCPLOT_DRYSD, 'RHOBPLOT_SAND7', RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD, RHOBHCPLOT_DRYSD)
				idDRYSLS7 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_SILT7', NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, NPHIHCPLOT_DRYSLS, 'RHOBPLOT_SILT7', RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS, RHOBHCPLOT_DRYSLS)


				#Link the points together
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYCLS, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD, idDRYCLS, 3)

				plot.crossPlotAddParameterPointLink(idCP, idDRYSD1, idDRYSD, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD2, idDRYSD1, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD3, idDRYSD2, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD4, idDRYSD3, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD5, idDRYSD4, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD6, idDRYSD5, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSD7, idDRYSD6, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYSD7, 3)

				plot.crossPlotAddParameterPointLink(idCP, idDRYSLS1, idDRYSLS, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSLS2, idDRYSLS1, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSLS3, idDRYSLS2, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSLS4, idDRYSLS3, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSLS5, idDRYSLS4, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSLS6, idDRYSLS5, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYSLS7, idDRYSLS6, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYSLS7, 3)


if (CW_VCLPHIT_PLOT=="YES" and SWT_FLAG=="YES" and SWT_METHOD=="WAXMAN_SMITS" and (LITHOLOGY_MODEL=="SSC" or (LITHOLOGY_MODEL=="CARB" and CLAYFLG=="YES"))):
	idCP = plot.crossPlotIDFindByName("CWAPP vs VCL_PHIT Ratio "+DEPTH.wellName())
	if idCP==-1:
		idCP = plot.crossPlotCreate("CWAPP vs VCL_PHIT Ratio "+DEPTH.wellName(),DEPTH.wellName()+"."+DEPTH.datasetName()+"."+VCLINVPOR.variableName()+__suffix__,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+CWAPP.variableName()+__suffix__)
		plot.crossPlotSetColor(idCP,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+VSAND.variableName()+__suffix__)
		plot.setLegendVisible(idCP, True)
		plot.crossPlotDensityType(idCP, 0)
		plot.crossPlotSetXAxisType(idCP,0)
		plot.crossPlotSetYAxisType(idCP,0)
		plot.crossPlotSetXAxisScale(idCP,0)
		plot.crossPlotSetYAxisScale(idCP,0)
		plot.crossPlotSetXAxisUserLimits(idCP,0,3)
		plot.crossPlotSetYAxisUserLimits(idCP,0,20)
	
	if idCP!=-1:
		plot.crossPlotRemoveAllEquations(idCP)
		plot.crossPlotRemoveAllParameterPoint(idCP)

		#if no zonation is selected
		if 'pythonEditor' not in locals() or pythonEditor:
			if "zonationDataset" not in locals():
				zonationDataset = ''
				zoneList = ['']
		else:
			zoneList = [zoneName]
		
		plot.crossPlotSetZonation(idCP, zonationDataset)
		plot.crossPlotAddEquation(idCP,"y="+str(LINE1_GRAD)+"*x + "+str(LINE1_INT),"Sw=100% ","red")


if (PICKETT_PLOT=="YES" and SWT_FLAG=="YES"):
	idCP = plot.crossPlotIDFindByName("Pickett Plot "+DEPTH.wellName())
	if idCP==-1:
		idCP = plot.crossPlotCreate("Pickett Plot "+DEPTH.wellName(),DEPTH.wellName()+"."+DEPTH.datasetName()+"."+PHIT.variableName()+__suffix__,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+RT.variableName()+__suffix__)
		plot.crossPlotSetColor(idCP,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+VSAND.variableName()+__suffix__)
		plot.setLegendVisible(idCP, True)
		plot.crossPlotDensityType(idCP, 0)
		plot.crossPlotSetXAxisType(idCP,0)
		plot.crossPlotSetYAxisType(idCP,0)
		plot.crossPlotSetXAxisScale(idCP,1)
		plot.crossPlotSetYAxisScale(idCP,1)
		plot.crossPlotSetXAxisUserLimits(idCP,0.01,1)
		plot.crossPlotSetYAxisUserLimits(idCP,0.01,1000)
	
	if idCP!=-1:
		plot.crossPlotRemoveAllEquations(idCP)
		plot.crossPlotRemoveAllParameterPoint(idCP)
		
		#if no zonation is selected
		if 'pythonEditor' not in locals() or pythonEditor:
			if "zonationDataset" not in locals():
				zonationDataset = ''
				zoneList = ['']
		else:
			zoneList = [zoneName]
	
		plot.crossPlotSetZonation(idCP, zonationDataset)
		plot.crossPlotAddEquation(idCP,"y="+str(LINE2_INT)+"/(x**"+str(LINE2_GRAD)+")","Sw=100% ","red")


if (CARB_XPLOT=="YES" and LITHOLOGY_MODEL=="CARB"):
	idCP = plot.crossPlotIDFindByName("CARB D-N Crossplot "+DEPTH.wellName())
	if idCP == -1:
		#idCP=plot.crossPlotCreate("CARB D-N Crossplot "+DEPTH.wellName(),DEPTH.wellName()+"."+DEPTH.datasetName()+"."+NPHIHCPLOT.variableName()+__suffix__,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+RHOBHCPLOT.variableName()+__suffix__)
		idCP=plot.crossPlotCreate("CARB D-N Crossplot "+DEPTH.wellName(),DEPTH.wellName()+"."+DEPTH.datasetName()+"."+NPHIHCPLOT.variableName()+__suffix__,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+RHOBHCPLOT.variableName()+__suffix__)
		plot.setLegendVisible(idCP, True)
		plot.crossPlotDensityType(idCP, 1)
		plot.crossPlotSetColor(idCP,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+DEPTH.variableName()+__suffix__)
		plot.crossPlotSetYAxisUserLimits(idCP,3,2)
		plot.crossPlotSetXAxisUserLimits(idCP,-0.1,0.5)
		plot.crossPlotDensityType(idCP,0)
		
	if idCP!=-1:
		plot.crossPlotRemoveAllEquations(idCP)
		plot.crossPlotRemoveAllParameterPoint(idCP)
	
		#if no zonation is selected
		if 'pythonEditor' not in locals() or pythonEditor:
			if "zonationDataset" not in locals():
				zonationDataset = ''
				zoneList = ['']
		else:
			zoneList = [zoneName]
	
		plot.crossPlotSetZonation(idCP, zonationDataset)
	
		for zoneName in zoneList:
			if LITHTYPE=="CA-[CL]":
				idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT', NPHI_FLC, NPHI_FLC, NPHI_FLC, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYLM_PLOT', NPHI_DRYLM, NPHI_DRYLM, NPHI_DRYLM, 'RHOB_DRYLM_PLOT', RHOB_DRYLM, RHOB_DRYLM, RHOB_DRYLM)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				if CLAYFLG=="YES":
					idDRYCL = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYCL_PLOT', NPHIHCPLOT_DRYCLS, NPHIHCPLOT_DRYCLS, NPHIHCPLOT_DRYCLS, 'RHOB_DRYCLY_PLOT', RHOB_DRYCLY, RHOB_DRYCLY, RHOB_DRYCLY)
					idWETCLS = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_CLY', NPHIHCPLOT_WETCLS, NPHIHCPLOT_WETCLS, NPHIHCPLOT_WETCLS, 'RHOBPLOT_CLY', RHOBHCPLOT_WETCLS, RHOBHCPLOT_WETCLS, RHOBHCPLOT_WETCLS)
					plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYCL, 3)
					plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYCL, 3)
			
			elif LITHTYPE=="DL-[CL]":
				idFLUID2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT2', NPHI_TOOLDL, NPHI_TOOLDL, NPHI_TOOLDL, 'RHOB_FLUID_PLOT2', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYDL = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYDL_PLOT', NPHI_DRYDL, NPHI_DRYDL, NPHI_DRYDL, 'RHOB_DRYDL_PLOT', RHOB_DRYDL, RHOB_DRYDL, RHOB_DRYDL)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID2, idDRYDL, 3)
				if CLAYFLG=="YES":
					idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT', NPHI_FLC, NPHI_FLC, NPHI_FLC, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
					idDRYCL = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYCL_PLOT', NPHIHCPLOT_DRYCLS, NPHIHCPLOT_DRYCLS, NPHIHCPLOT_DRYCLS, 'RHOB_DRYCLY_PLOT', RHOB_DRYCLY, RHOB_DRYCLY, RHOB_DRYCLY)
					idWETCLS = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHIPLOT_CLY', NPHIHCPLOT_WETCLS, NPHIHCPLOT_WETCLS, NPHIHCPLOT_WETCLS, 'RHOBPLOT_CLY', RHOBHCPLOT_WETCLS, RHOBHCPLOT_WETCLS, RHOBHCPLOT_WETCLS)
					plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYCL, 3)
					plot.crossPlotAddParameterPointLink(idCP, idDRYDL, idDRYCL, 3)
					
			elif LITHTYPE=="CA-DL-[CL]":
				idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT', NPHI_FLC, NPHI_FLC, NPHI_FLC, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idFLUID2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT2', NPHI_TOOLDL, NPHI_TOOLDL, NPHI_TOOLDL, 'RHOB_FLUID_PLOT2', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYLM_PLOT', NPHI_DRYLM, NPHI_DRYLM, NPHI_DRYLM, 'RHOB_DRYLM_PLOT', RHOB_DRYLM, RHOB_DRYLM, RHOB_DRYLM)
				idDRYDL = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYDL_PLOT', NPHI_DRYDL, NPHI_DRYDL, NPHI_DRYDL, 'RHOB_DRYDL_PLOT', RHOB_DRYDL, RHOB_DRYDL, RHOB_DRYDL)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID2, idDRYDL, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYDL, 3)
				
			elif LITHTYPE=="CA-QZ-[CL]":
				idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT', NPHI_FLC, NPHI_FLC, NPHI_FLC, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idFLUID2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT2', NPHI_TOOLQZ, NPHI_TOOLQZ, NPHI_TOOLQZ, 'RHOB_FLUID_PLOT2', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYLM_PLOT', NPHI_DRYLM, NPHI_DRYLM, NPHI_DRYLM, 'RHOB_DRYLM_PLOT', RHOB_DRYLM, RHOB_DRYLM, RHOB_DRYLM)
				idDRYQZ = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYQZ_PLOT', NPHI_DRYQZ, NPHI_DRYQZ, NPHI_DRYQZ, 'RHOB_DRYQZ_PLOT', RHOB_DRYQZ, RHOB_DRYQZ, RHOB_DRYQZ)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID2, idDRYQZ, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYQZ, 3)
				
			elif LITHTYPE=="CA-M1-[CL]":
				idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT', NPHI_FLC, NPHI_FLC, NPHI_FLC, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYLM_PLOT', NPHI_DRYLM, NPHI_DRYLM, NPHI_DRYLM, 'RHOB_DRYLM_PLOT', RHOB_DRYLM, RHOB_DRYLM, RHOB_DRYLM)
				idDRYM1 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYMIN1_PLOT', NPHI_DRYMIN1, NPHI_DRYMIN1, NPHI_DRYMIN1, 'RHOB_DRYMIN1_PLOT', RHOB_DRYMIN1, RHOB_DRYMIN1, RHOB_DRYMIN1)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYM1, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYM1, 3)

			elif LITHTYPE=="CA-DL-QZ-[CL]":
				idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT', NPHI_FLC, NPHI_FLC, NPHI_FLC, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idFLUID2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT2', NPHI_TOOLDL, NPHI_TOOLDL, NPHI_TOOLDL, 'RHOB_FLUID_PLOT2', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idFLUID3 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT3', NPHI_TOOLQZ, NPHI_TOOLQZ, NPHI_TOOLQZ, 'RHOB_FLUID_PLOT3', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYLM_PLOT', NPHI_DRYLM, NPHI_DRYLM, NPHI_DRYLM, 'RHOB_DRYLM_PLOT', RHOB_DRYLM, RHOB_DRYLM, RHOB_DRYLM)
				idDRYDL = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYDL_PLOT', NPHI_DRYDL, NPHI_DRYDL, NPHI_DRYDL, 'RHOB_DRYDL_PLOT', RHOB_DRYDL, RHOB_DRYDL, RHOB_DRYDL)
				idDRYQZ = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYQZ_PLOT', NPHI_DRYQZ, NPHI_DRYQZ, NPHI_DRYQZ, 'RHOB_DRYQZ_PLOT', RHOB_DRYQZ, RHOB_DRYQZ, RHOB_DRYQZ)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID2, idDRYDL, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID3, idDRYQZ, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYDL, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYQZ, 3)

			elif LITHTYPE=="CA-M1-M2-[CL]":
				idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_FLUID_PLOT', NPHI_FLC, NPHI_FLC, NPHI_FLC, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYLM_PLOT', NPHI_DRYLM, NPHI_DRYLM, NPHI_DRYLM, 'RHOB_DRYLM_PLOT', RHOB_DRYLM, RHOB_DRYLM, RHOB_DRYLM)
				idDRYM1 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYMIN1_PLOT', NPHI_DRYMIN1, NPHI_DRYMIN1, NPHI_DRYMIN1, 'RHOB_DRYMIN1_PLOT', RHOB_DRYMIN1, RHOB_DRYMIN1, RHOB_DRYMIN1)
				idDRYM2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'NPHI_DRYMIN2_PLOT', NPHI_DRYMIN2, NPHI_DRYMIN2, NPHI_DRYMIN2, 'RHOB_DRYMIN2_PLOT', RHOB_DRYMIN2, RHOB_DRYMIN2, RHOB_DRYMIN2)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYM1, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYM2, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYM1, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYM2, 3)


if (CARB_XPLOT=="YES" and LITH2FLG=="PEF-DEN" and LITHOLOGY_MODEL=="CARB"):
	idCP = plot.crossPlotIDFindByName("CARB P-D Crossplot "+DEPTH.wellName())
	if idCP == -1:
		idCP=plot.crossPlotCreate("CARB P-D Crossplot "+DEPTH.wellName(),DEPTH.wellName()+"."+DEPTH.datasetName()+"."+PEFCC.variableName()+__suffix__,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+RHOBCC.variableName()+__suffix__)
		plot.setLegendVisible(idCP, True)
		plot.crossPlotDensityType(idCP, 1)
		plot.crossPlotSetColor(idCP,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+DEPTH.variableName()+__suffix__)
		plot.crossPlotSetYAxisUserLimits(idCP,3,2)
		plot.crossPlotSetXAxisUserLimits(idCP,0,8)
		plot.crossPlotDensityType(idCP,0)
		
	if idCP!=-1:
		plot.crossPlotRemoveAllEquations(idCP)
		plot.crossPlotRemoveAllParameterPoint(idCP)
	
		#if no zonation is selected
		if 'pythonEditor' not in locals() or pythonEditor:
			if "zonationDataset" not in locals():
				zonationDataset = ''
				zoneList = ['']
		else:
			zoneList = [zoneName]
	
		plot.crossPlotSetZonation(idCP, zonationDataset)
	
		for zoneName in zoneList:
			idFLUID = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_FLUID_PLOT', PEF_FLLM, PEF_FLLM, PEF_FLLM, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
			idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_DRYLM_PLOT', PEF_DRYLM, PEF_DRYLM, PEF_DRYLM, 'RHOB_DRYLM_PLOT', RHOB_DRYLM, RHOB_DRYLM, RHOB_DRYLM)
			
			if LITHTYPE=="CA-DL-[CL]":
				idFLUID2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_FLUID_PLOT2', PEF_FLDL, PEF_FLDL, PEF_FLDL, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYDL = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_DRYDL_PLOT', PEF_DRYDL, PEF_DRYDL, PEF_DRYDL, 'RHOB_DRYDL_PLOT', RHOB_DRYDL, RHOB_DRYDL, RHOB_DRYDL)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID2, idDRYDL, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYDL, 3)
				
			if LITHTYPE=="CA-QZ-[CL]":
				idFLUID2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_FLUID_PLOT2', PEF_FLQZ, PEF_FLQZ, PEF_FLQZ, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYQZ = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_DRYQZ_PLOT', PEF_DRYQZ, PEF_DRYQZ, PEF_DRYQZ, 'RHOB_DRYQZ_PLOT', RHOB_DRYQZ, RHOB_DRYQZ, RHOB_DRYQZ)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID2, idDRYQZ, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYQZ, 3)
				
		if LITHTYPE=="CA-M1-[CL]":
				idFLUID2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_FLUID_PLOT2', PEF_FLMIN1, PEF_FLMIN1, PEF_FLMIN1, 'RHOB_FLUID_PLOT', RHOB_FLC, RHOB_FLC, RHOB_FLC)
				idDRYMIN1 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, 'PEF_DRYMIN1_PLOT', PEF_DRYMIN1, PEF_DRYMIN1, PEF_DRYMIN1, 'RHOB_DRYQZ_PLOT', RHOB_DRYMIN1, RHOB_DRYMIN1, RHOB_DRYMIN1)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID, idDRYLM, 3)
				plot.crossPlotAddParameterPointLink(idCP, idFLUID2, idDRYMIN1, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYMIN1, 3)


if (CARB_XPLOT=="YES" and len(LITHTYPE)==13 and LITHOLOGY_MODEL=="CARB"):
	idCP = plot.crossPlotIDFindByName("CARB Modified M-N Crossplot "+DEPTH.wellName())
	if idCP == -1:
		idCP=plot.crossPlotCreate("CARB Modified M-N Crossplot "+DEPTH.wellName(),DEPTH.wellName()+"."+DEPTH.datasetName()+"."+MXPOINTPLOT.variableName()+__suffix__,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+NXPOINTPLOT.variableName()+__suffix__)
		plot.setLegendVisible(idCP, True)
		plot.crossPlotDensityType(idCP, 1)
		plot.crossPlotSetColor(idCP,DEPTH.wellName()+"."+DEPTH.datasetName()+"."+DEPTH.variableName()+__suffix__)
		plot.crossPlotSetYAxisUserLimits(idCP,0.45,0.7)
		plot.crossPlotSetXAxisUserLimits(idCP,-1,11)
		plot.crossPlotDensityType(idCP,0)

	if idCP!=-1:
		plot.crossPlotRemoveAllEquations(idCP)
		plot.crossPlotRemoveAllParameterPoint(idCP)
	
		#if no zonation is selected
		if 'pythonEditor' not in locals() or pythonEditor:
			if "zonationDataset" not in locals():
				zonationDataset = ''
				zoneList = ['']
		else:
			zoneList = [zoneName]
	
		plot.crossPlotSetZonation(idCP, zonationDataset)
	
		for zoneName in zoneList:
			
			if LITHTYPE=="CA-DL-QZ-[CL]":
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, "M_LIME", MLIME, MLIME, MLIME, "N_LIME", NLIME, NLIME, NLIME)
				idDRYDL = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, "M_DOLO", MDOLO, MDOLO, MDOLO, "N_DOLO", NDOLO, NDOLO, NDOLO)
				idDRYQZ = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, "M_SAND", MSAND, MSAND, MSAND, "N_SAND", NSAND, NSAND, NSAND)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYDL, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYDL, idDRYQZ, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYQZ, idDRYLM, 3)
				
			if LITHTYPE=="CA-M1-M2-[CL]":
				idDRYLM = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, "M_LIME", MLIME, MLIME, MLIME, "N_LIME", NLIME, NLIME, NLIME)
				idDRYMIN1 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, "M_MIN1", MMIN1, MMIN1, MMIN1, "N_MIN1", NMIN1, NMIN1, NMIN1)
				idDRYMIN2 = plot.crossPlotAddParameterPointXY(idCP, DEPTH.wellName(), DEPTH.datasetName(), zonationDataset, zoneName, "M_MIN2", MMIN2, MMIN2, MMIN2, "N_MIN2", NMIN2, NMIN2, NMIN2)
				plot.crossPlotAddParameterPointLink(idCP, idDRYLM, idDRYMIN1, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYMIN1, idDRYMIN2, 3)
				plot.crossPlotAddParameterPointLink(idCP, idDRYMIN2, idDRYLM, 3)



db.datasetPropertyChange(w,'PEP','1------------------------------','General Tab  ##########')
val1=str(LITHOLOGY_MODEL)
db.datasetPropertyChange(w,'PEP','101)  LITHOLOGY_MODEL',val1)
val1=str(UseGraphicalParameterPicking)
db.datasetPropertyChange(w,'PEP','102)  UseGraphicalParameterPicking',val1)

db.datasetPropertyChange(w,'PEP','2------------------------------','SSC_Model Tab  #######')
val1=str(NPHI_FLUID)
db.datasetPropertyChange(w,'PEP','201)  NPHI_FLUID',val1)
val1=str(RHOB_FLUID)
db.datasetPropertyChange(w,'PEP','202)  RHOB_FLUID',val1)
val1=str(NPHI_DRY_SAND)
db.datasetPropertyChange(w,'PEP','203)  NPHI_DRY_SAND',val1)
val1=str(RHOB_DRY_SAND)
db.datasetPropertyChange(w,'PEP','204)  RHOB_DRY_SAND',val1)
val1=str(RHOB_DRY_SLT)
db.datasetPropertyChange(w,'PEP','205)  RHOB_DRY_SLT',val1)
val1=str(USE_SILT_ANGLE)
db.datasetPropertyChange(w,'PEP','206)  USE_SILT_ANGLE',val1)
try:
	val1=str(DEGFLSLT)
	db.datasetPropertyChange(w,'PEP','207)  DEGFLSLT',val1)
except:
	db.datasetPropertyChange(w,'PEP','207)  DEGFLSLT','VAR')
val1=str(DNXPLOTSAND)
db.datasetPropertyChange(w,'PEP','208)  DNXPLOTSAND',val1)

db.datasetPropertyChange(w,'PEP','3------------------------------','Carbonate Tab  #######')
val1=str(LITHTYPE)
db.datasetPropertyChange(w,'PEP','301)  LITHTYPE',val1)
val1=str(CLAYFLG)
db.datasetPropertyChange(w,'PEP','302)  CLAYFLG',val1)
val1=str(NEUTOOL)
db.datasetPropertyChange(w,'PEP','303)  NEUTOOL',val1)
val1=str(LITH2FLG)
db.datasetPropertyChange(w,'PEP','304)  LITH2FLG',val1)
val1=str(RHOB_FLC)
db.datasetPropertyChange(w,'PEP','305)  RHOB_FLC',val1)
val1=str(RHOB_DRYLM)
db.datasetPropertyChange(w,'PEP','306)  RHOB_DRYLM',val1)
val1=str(NPHI_DRYLM)
db.datasetPropertyChange(w,'PEP','307)  NPHI_DRYLM',val1)
val1=str(PEF_DRYLM)
db.datasetPropertyChange(w,'PEP','308)  PEF_DRYLM',val1)
val1=str(RHOB_DRYDL)
db.datasetPropertyChange(w,'PEP','309)  RHOB_DRYDL',val1)
val1=str(NPHI_DRYDL)
db.datasetPropertyChange(w,'PEP','310)  NPHI_DRYDL',val1)
val1=str(PEF_DRYDL)
db.datasetPropertyChange(w,'PEP','311)  PEF_DRYDL',val1)
val1=str(RHOB_DRYQZ)
db.datasetPropertyChange(w,'PEP','312)  RHOB_DRYQZ',val1)
val1=str(NPHI_DRYQZ)
db.datasetPropertyChange(w,'PEP','313)  NPHI_DRYQZ',val1)
val1=str(PEF_DRYQZ)
db.datasetPropertyChange(w,'PEP','314)  PEF_DRYQZ',val1)
val1=str(RHOB_DRYMIN1)
db.datasetPropertyChange(w,'PEP','315)  RHOB_DRYMIN1',val1)
val1=str(NPHI_DRYMIN1)
db.datasetPropertyChange(w,'PEP','316)  NPHI_DRYMIN1',val1)
val1=str(PEF_DRYMIN1)
db.datasetPropertyChange(w,'PEP','317)  PEF_DRYMIN1',val1)
val1=str(RHOB_DRYMIN2)
db.datasetPropertyChange(w,'PEP','318)  RHOB_DRYMIN2',val1)
val1=str(NPHI_DRYMIN2)
db.datasetPropertyChange(w,'PEP','319)  NPHI_DRYMIN2',val1)
val1=str(PEF_DRYMIN2)
db.datasetPropertyChange(w,'PEP','320)  PEF_DRYMIN2',val1)
val1=str(NEU_OFFSET)
db.datasetPropertyChange(w,'PEP','321)  NEU_OFFSET',val1)
val1=str(PEF_OFFSET)
db.datasetPropertyChange(w,'PEP','322)  PEF_OFFSET',val1)
val1=str(GR_CALC)
db.datasetPropertyChange(w,'PEP','323)  GR_CALC',val1)

db.datasetPropertyChange(w,'PEP','4------------------------------','SW_Parameters Tab  ####')
val1=str(TEMPSOURCE)
db.datasetPropertyChange(w,'PEP','401)  TEMPSOURCE',val1)
val1=str(DEPTHSOURCE)
db.datasetPropertyChange(w,'PEP','402)  DEPTHSOURCE',val1)
val1=str(WELLLOC)
db.datasetPropertyChange(w,'PEP','403)  WELLLOC',val1)
val1=str(RTKB_DEP)
db.datasetPropertyChange(w,'PEP','404)  RTKB_DEP',val1)
val1=str(SURF_TEMP)
db.datasetPropertyChange(w,'PEP','405)  SURF_TEMP',val1)
val1=str(TD_MD)
db.datasetPropertyChange(w,'PEP','406)  TD_MD',val1)
val1=str(TD_TVDSS)
db.datasetPropertyChange(w,'PEP','407)  TD_TVDSS',val1)
val1=str(BHT_TEMP)
db.datasetPropertyChange(w,'PEP','408)  BHT_TEMP',val1)
val1=str(SB_DEP)
db.datasetPropertyChange(w,'PEP','409)  SB_DEP',val1)
val1=str(SB_TEMP)
db.datasetPropertyChange(w,'PEP','410)  SB_TEMP',val1)
val1=str(GL_DEP)
db.datasetPropertyChange(w,'PEP','411)  GL_DEP',val1)
val1=str(SWT_METHOD)
db.datasetPropertyChange(w,'PEP','412)  SWT_METHOD',val1)
val1=str(CALCULATED_MSTAR)
db.datasetPropertyChange(w,'PEP','413)  CALCULATED_MSTAR',val1)
val1=str(SALFLG)
db.datasetPropertyChange(w,'PEP','414)  SALFLG',val1)
val1=str(QVFLAG)
db.datasetPropertyChange(w,'PEP','415)  QVFLAG',val1)
val1=str(QV_LOG)
db.datasetPropertyChange(w,'PEP','416)  QV_LOG',val1)
val1=str(BYPASS_LITHO_PORO_CALCULATION)
db.datasetPropertyChange(w,'PEP','417)  BYPASS_LITHO_PORO_CALC',val1)
val1=str(CLAY_VOLUME_FLAG)
db.datasetPropertyChange(w,'PEP','418)  CLAY_VOLUME_FLAG',val1)

db.datasetPropertyChange(w,'PEP','5------------------------------','HC_Correction Tab  ####')
val1=str(HCC_APP)
db.datasetPropertyChange(w,'PEP','501)  HCC_APP',val1)
val1=str(COR_METHOD)
db.datasetPropertyChange(w,'PEP','502)  COR_METHOD',val1)
val1=str(RHO_OIL)
db.datasetPropertyChange(w,'PEP','503)  RHO_OIL',val1)
val1=str(RHO_GAS)
db.datasetPropertyChange(w,'PEP','504)  RHO_GAS',val1)
val1=str(MFRES)
db.datasetPropertyChange(w,'PEP','505)  MFRES',val1)
val1=str(MFTEMP)
db.datasetPropertyChange(w,'PEP','506)  MFTEMP',val1)
val1=str(DEGHCCOR)
db.datasetPropertyChange(w,'PEP','507)  DEGHCCOR',val1)
val1=str(NEUFAC)
db.datasetPropertyChange(w,'PEP','508)  NEUFAC',val1)
val1=str(HCREF)
db.datasetPropertyChange(w,'PEP','509)  HCREF',val1)

db.datasetPropertyChange(w,'PEP','6------------------------------','BH_Correction Tab  ####')
val1=str(BH_CORR)
db.datasetPropertyChange(w,'PEP','601)  BH_CORR',val1)
val1=str(SOURCE_SYN_LOG)
db.datasetPropertyChange(w,'PEP','602)  SOURCE_SYN_LOG',val1)
val1=str(EXTRHOBFLG)
db.datasetPropertyChange(w,'PEP','603)  EXTRHOBFLG',val1)

db.datasetPropertyChange(w,'PEP','7------------------------------','Mineral_Flagging Tab  ####')
val1=str(COALFL)
db.datasetPropertyChange(w,'PEP','701)  BH_CORR',val1)
val1=str(EXTCOAL)
db.datasetPropertyChange(w,'PEP','702)  EXTCOAL',val1)
val1=str(COALFLAG_EXPANSION)
db.datasetPropertyChange(w,'PEP','703)  COALFLAG_EXPANSION',val1)
val1=str(CARSTFL)
db.datasetPropertyChange(w,'PEP','704)  CARSTFL',val1)
val1=str(EXTSTREAK)
db.datasetPropertyChange(w,'PEP','705)  EXTSTREAK',val1)



db.__connectProjectBrowser

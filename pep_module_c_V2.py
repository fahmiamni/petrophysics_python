import Techlog
import TechlogDialog as dialog
import TechlogMath
import TechlogStat as stat
sys.path.append(os.path.join(db.dirCompany(), 'External_DLLs'))
import REM_RFM_Enhancement_Equations_rev3

#******************************************************** Start of Techlog dependency function ******************************************************
#The dependency function governs the workflow layout e.g. enabling / disabling parameters etc.
def dependency():
	#By default, all input workflow parameters are disabled except for PHIS and PHICL
	parameterDict['GRAIN_RADIUS_nm'].valueChange('enable', False)
	parameterDict['m'].valueChange('enable', False)
	parameterDict['C'].valueChange('enable', False)
	parameterDict['GWC_ftTVDSS'].valueChange('enable', False)
	parameterDict['GOC_ftTVDSS'].valueChange('enable', False)
	parameterDict['OWC_ftTVDSS'].valueChange('enable', False)
	parameterDict['GAS_GRAD'].valueChange('enable', False)
	parameterDict['OIL_GRAD'].valueChange('enable', False)
	parameterDict['WTR_GRAD'].valueChange('enable', False)
	parameterDict['SCOSTG'].valueChange('enable', False)
	parameterDict['SCOSTO'].valueChange('enable', False)
	parameterDict['b0'].valueChange('enable', False)
	parameterDict['IFT_'].valueChange('enable', False)
	parameterDict['MinVCLW'].valueChange('enable', False)
	parameterDict['MaxPERM'].valueChange('enable', False)
	parameterDict['SSC_VSHALE_cutoff'].valueChange('enable', False)
	parameterDict['THINBEDS_RT_flag'].valueChange('enable', False)
	parameterDict['Pc_Cutoff'].valueChange('enable', False)
	parameterDict['CONST2'].valueChange('enable', False)
	parameterDict['CONST1'].valueChange('enable', False)
	parameterDict['CONST0'].valueChange('enable', False)
	parameterDict['MLR_OPTION'].valueChange('enable', False)
	parameterDict['PERM_OPTION'].valueChange('enable', False)
	#To check if any variable is selected,
	#If no variable is selected, .value('value').split('.')[2] == str()
	#Otherwise, .value('value').split('.')[2] != str()
	#I believe there's an easier way to check whether a variable has been selected as input curve into the workflow
	#Which I am unaware of, therefore I apologize
	
	if parameterDict['PC'].value('value').split('.')[2] != str() and parameterDict['IFT'].value('value').split('.')[2] == str():
		#If PC curve is provided and no IFT curve provided, allow users to input IFT_
		parameterDict['IFT_'].valueChange('enable', True)
	if parameterDict['CHOO_PERM_PARAMETERS_USER_INPUT'].value('value') == "YES":
		parameterDict['PERM_OPTION'].valueChange('enable', True)
		#User decides to calculate PERM_CHOO using PEP Module C
		if parameterDict['GRAIN_RAD'].value('value').split('.')[2] == str():
			#GRAIN_RAD input curve is not provided, allow users to input
			parameterDict['GRAIN_RADIUS_nm'].valueChange('enable', True)
		else:
			pass
		if parameterDict['M_EXP'].value('value').split('.')[2] == str():
			#M_EXP input curve is not provided, allow users to input
			parameterDict['m'].valueChange('enable', True)
		else:
			pass
		if parameterDict['COMP_FAC'].value('value').split('.')[2] == str():
			#COMP_FAC input curve is not provided, allow users to input
			parameterDict['C'].valueChange('enable', True)
		else:
			pass
	if parameterDict['PC_USER_INPUT'].value('value') == "YES":
		#PC input curve is not provided
		if parameterDict['PC'].value('value').split('.')[2] == str():
			parameterDict['GWC_ftTVDSS'].valueChange('enable', True)
			parameterDict['GOC_ftTVDSS'].valueChange('enable', True)
			parameterDict['OWC_ftTVDSS'].valueChange('enable', True)
			parameterDict['GAS_GRAD'].valueChange('enable', True)
			parameterDict['OIL_GRAD'].valueChange('enable', True)
			parameterDict['WTR_GRAD'].valueChange('enable', True)
		else:
			pass
	if parameterDict['CHOO_SHF_PARAMETERS_USER_INPUT'].value('value') == "YES":
		if parameterDict['PC'].value('value').split('.')[2] == str():
			if parameterDict['SCOSTH_O'].value('value').split('.')[2] == str():
			#Either SCOSTH_O or SCOSTH_G is not provided as input curve
				parameterDict['SCOSTO'].valueChange('enable', True)
			if parameterDict['SCOSTH_G'].value('value').split('.')[2] == str():
				parameterDict['SCOSTG'].valueChange('enable', True)
			else:
				pass
		if parameterDict['BO_CH'].value('value').split('.')[2] == str():
		#BO_CH input curve is not provided
			parameterDict['b0'].valueChange('enable', True)
		else:
			pass
	if parameterDict['RFM_MODULE'].value('value') == "YES":
	#User decides to run RFM as well
		parameterDict['MinVCLW'].valueChange('enable', True)
		parameterDict['MaxPERM'].valueChange('enable', True)
		parameterDict['MLR_OPTION'].valueChange('enable', True)
		if parameterDict['MLR_OPTION'].value('value') == "YES":
			parameterDict['Pc_Cutoff'].valueChange('enable', True)
			parameterDict['CONST2'].valueChange('enable', False)
			parameterDict['CONST1'].valueChange('enable', False)
			parameterDict['CONST0'].valueChange('enable', False)
		elif parameterDict['MLR_OPTION'].value('value') == "NO":
			parameterDict['Pc_Cutoff'].valueChange('enable', False)
			parameterDict['CONST2'].valueChange('enable', True)
			parameterDict['CONST1'].valueChange('enable', True)
			parameterDict['CONST0'].valueChange('enable', True)			
	if parameterDict['CUTOFF_OPTION'].value('value') == "YES":
		#User decides to have SSC evaluation in clean sand either via SSC VSHALE cutoff or FACIES flag
		parameterDict['SSC_VSHALE_cutoff'].valueChange('enable', True)
		parameterDict['THINBEDS_RT_flag'].valueChange('enable', False)
	elif parameterDict['CUTOFF_OPTION'].value('value') == "NO":
		parameterDict['SSC_VSHALE_cutoff'].valueChange('value', -1)
		parameterDict['SSC_VSHALE_cutoff'].valueChange('enable', False)
	if parameterDict['THINBEDS_RT_OPTION'].value('value') == "YES":
		parameterDict['THINBEDS_RT_flag'].valueChange('enable', True)
		parameterDict['SSC_VSHALE_cutoff'].valueChange('enable', False)
	elif parameterDict['THINBEDS_RT_OPTION'].value('value') == "NO":
		parameterDict['THINBEDS_RT_flag'].valueChange('value', -1)
		parameterDict['THINBEDS_RT_flag'].valueChange('enable', False)
	if parameterDict['PERM_OPTION'].value('value') == "YES":
		parameterDict['A_PERM_CH'].valueChange('enable', False)
		parameterDict['B_PERM_CH'].valueChange('enable', False)
		if parameterDict['CHOO_PERM_PARAMETERS_USER_INPUT'].value('value') == "YES":
			if parameterDict['GRAIN_RAD'].value('value').split('.')[2] == str():
				#GRAIN_RAD variable is not provided
				parameterDict['GRAIN_RADIUS_nm'].valueChange('enable', True)
			else:
				pass
			if parameterDict['M_EXP'].value('value').split('.')[2] == str():
				#M_EXP variable is not provided
				parameterDict['m'].valueChange('enable', True)
			else:
				pass
			if parameterDict['COMP_FAC'].value('value').split('.')[2] == str():
				#COMP_FAC variable is not provided
				parameterDict['C'].valueChange('enable', True)
			else:
				pass
	elif parameterDict['PERM_OPTION'].value('value') == "NO":
		parameterDict['A_PERM_CH'].valueChange('enable', True)
		parameterDict['B_PERM_CH'].valueChange('enable', True)
		parameterDict['GRAIN_RADIUS_nm'].valueChange('enable', False)
		parameterDict['m'].valueChange('enable', False)
		parameterDict['C'].valueChange('enable', False)


#******************************************************** End of Techlog dependency function ******************************************************

#******************************************************** Input Check *****************************************************************************
#Check user inputs
#If no variable is selected, and no user-defined input in workflow parameters, give error message
if parameterDict['GRAIN_RAD'].value('value').split('.')[2] == str() and parameterDict['CHOO_PERM_PARAMETERS_USER_INPUT'].value('value') == "NO" and parameterDict['PERM_OPTION'].value('value') == "YES":
	print("No Grain Radius Input, Kindly input Grain Radius variable or Define its value in Workflow. Thanks!")
	exit()
if parameterDict['M_EXP'].value('value').split('.')[2] == str() and parameterDict['CHOO_PERM_PARAMETERS_USER_INPUT'].value('value') == "NO" and parameterDict['PERM_OPTION'].value('value') == "YES":
	print("No m Cementation Exponent Input, Kindly input m Cementation Exponent variable or Define its value in Workflow. Thanks!")
	exit()
if parameterDict['COMP_FAC'].value('value').split('.')[2] == str() and parameterDict['CHOO_PERM_PARAMETERS_USER_INPUT'].value('value') == "NO" and parameterDict['PERM_OPTION'].value('value') == "YES":
	print("No C Compaction Factor Input, Kindly input C Compaction Factor variable or Define its value in Workflow. Thanks!")
	exit()
if parameterDict['PC'].value('value').split('.')[2] == str() and parameterDict['PC_USER_INPUT'].value('value') == "NO":
	print("No Pc Capillary Pressure Input, Kindly input Pc Capillary Pressure variable or Define FWL, gw and ghc values in Workflow. Thanks!")
	exit()
if parameterDict['SCOSTH_O'].value('value').split('.')[2] == str() and parameterDict['SCOSTH_G'].value('value').split('.')[2] == str():
	if parameterDict['CHOO_SHF_PARAMETERS_USER_INPUT'].value('value') == "NO":
		if parameterDict['PC'].value('value').split('.')[2] == str():
			print("No Interfacial Tension Input", "Kindly input SCOSTH_O / SCOSTH_G variable or Define IFT_ value in Workflow. Thanks!")
			exit()
	else:
		pass
if parameterDict['BO_CH'].value('value').split('.')[2] == str() and parameterDict['CHOO_SHF_PARAMETERS_USER_INPUT'].value('value') == "NO":
	print("No B0 Input", "Kindly input B0 variable or Define its value in Workflow. Thanks!")
	exit()
if parameterDict['CUTOFF_OPTION'].value('value') == "YES" and parameterDict['THINBEDS_RT_OPTION'].value('value') == "YES":
	print("Both CUTOFF_OPTION and THINBEDS_RT_OPTION are selected", "Kindly ensure either only CUTOFF_OPTION or THINBEDS_RT_OPTION is selected")
	exit()

#******************************************************** Initialization *****************************************************************************

#Initialize All Variables
w = DEPTH.wellName()
dsname = DEPTH.datasetName()
outlist = ["VSHALE_REM", "PHIT_REM", "VCLD_REM", "VSILT_REM", "VCLB_REM", "PHIE_REM", "VSAND_REM", "VHC_REM", "VWATER_REM", "PERM_REM", "SWE_REM", "SWT_REM", "EHC_REM", "VCLW_REM", "SWB_REM", "PC_REM", "QC_REM", "EHC_SSC", "EHC_R10", "EHC_R30"]
u = DEPTH.unitName()
n = DEPTH.size()
dpth = DEPTH.values()
dtvd = TVDSS.values()
vshale = VSHALE.values()
porosity = PHIT.values()
permeability = PERM_CH.values()
saturation = SWT.values()
shf_ssc = SW_SHF.values()
phie_ssc = PHIE.values()
swe_ssc = SWE.values()
vsand_ssc = VSAND.values()
vsilt_ssc = VSILT.values()
vclw_ssc = VCLW.values()
vclb_ssc = VCLB.values()
vcld_ssc = VCLD.values()
facies = ROCKTYPE.values()
#IFT_0 = [0] * n
deltaD = [0] * n
deltaU = [0] * n
AB = [0] * n
AC = [0] * n
enhancedvshale = [0] * n
enhancedvshale_low = [0] * n
enhancedvshale_med = [0] * n
enhancedvhshale_high = [0] * n
deltavshale = [0] * n
deltavshale_low = [0] * n
deltavshale_med = [0] * n
deltavshale_high = [0] * n
deltaporosity = [0] * n
deltaporosity_low = [0] * n
deltaporosity_med = [0] * n
deltaporosity_high = [0] * n
enhancedporosity = [0] * n
enhancedporosity_low = [0] * n
enhancedporosity_med = [0] * n
enhancedporosity_high = [0] * n
vsilt0 = [0] * n
vsilt0_low = [0] * n
vsilt0_med = [0] * n
vsilt0_high = [0] * n
vcl0 = [0] * n
vcl0_low = [0] * n
vcl0_med = [0] * n
vcl0_high = [0] * n
K0 = [0] * n
K0_low = [0] * n
K0_med = [0] * n
K0_high = [0] * n
swb0 = [0] * n
swb0_low = [0] * n
swb0_med = [0] * n
swb0_high = [0] * n
phie0 = [0] * n
phie0_low = [0] * n
phie0_med = [0] * n
phie0_high = [0] * n
vsand0 = [0] * n
vsand0_low = [0] * n
vsand0_med = [0] * n
vsand0_high = [0] * n
shf0 = [1] * n
shf0_low = [1] * n
shf0_med = [1] * n
shf0_high = [1] * n
voil0 = [0] * n
voil0_low = [0] * n
voil0_med = [0] * n
voil0_high = [0] * n
vwater0 = [0] * n
vwater0_low = [0] * n
vwater0_med = [0] * n
vwater0_high = [0] * n
swe0 = [0] * n
swe0_low = [0] * n
swe0_med = [0] * n
swe0_high = [0] * n
vclb0 = [0] * n
vclb0_low = [0] * n
vclb0_med = [0] * n
vclb0_high = [0] * n
ehc0 = [0] * n
ehc0_low = [0] * n
ehc0_med = [0] * n
ehc0_high = [0] * n
vclw0 = [0] * n
vclw0_low = [0] * n
vclw0_med = [0] * n
vclw0_high = [0] * n
Pc0 = [0] * n
gwc0 = [0] * n
goc0 = [0] * n
owc0 = [0] * n
gas_grad0 = [0] * n
oil_grad0 = [0] * n
wtr_grad0 = [0] * n
AB_LOW = [0] * n
AB_MEDIUM = [0] * n
AB_HIGH = [0] * n
AC_LOW = [0] * n
AC_MEDIUM = [0] * n
AC_HIGH = [0] * n
enhancedvshale_LOW = [0] * n
enhancedvshale_MEDIUM = [0] * n
enhancedvshale_HIGH = [0] * n
qc_flag = [0] * n
ehc0_ssc = [0] * n
ehc10 = [0] * n
ehc30 = [0] * n

CF = 1.4

# A and B Choo's parameter
A_CH = [A_PERM_CH] * n
B_CH = [B_PERM_CH] * n

# Multi Linear Regression
ssf_ = []
phit_ = []
vsilt_ = []
vclw_ = []

if parameterDict['GRAIN_RAD'].value('value').split('.')[2] != str():
	#GRAIN_RAD variable is provided
	GRAIN_RAD0 = GRAIN_RAD.values()
else:
	#GRAIN_RAD variable is not provided. Take value from workflow parameters
	GRAIN_RAD0 = [GRAIN_RADIUS_nm] * n
if parameterDict['M_EXP'].value('value').split('.')[2] != str():
	#M_EXP variable is provided
	m0 = M_EXP.values()
else:
	#M_EXP variable is not provided. Take value from workflow parameters
	m0 = [m] * n
if parameterDict['COMP_FAC'].value('value').split('.')[2] != str():
	#COMP_FAC variable is provided
	C0 = COMP_FAC.values()
else:
	#COMP_FAC variable is not provided. Take value from workflow parameters
	C0 = [C] * n
if parameterDict['BO_CH'].value('value').split('.')[2] != str():
	#BO_CH variable is provided
	b00 = BO_CH.values()
else:
	#BO_CH variable is not provided. Take value from workflow parameters
	b00 = [b0] * n
if parameterDict['SCOSTH_G'].value('value').split('.')[2] != str():
	#SCOST_G is provided
	scostg0 = SCOSTH_G.values()
else:
	scostg0 = [SCOSTG] * n
if parameterDict['SCOSTH_O'].value('value').split('.')[2] != str():
	#SCOST_O is provided
	scosto0 = SCOSTH_O.values()
else:
	scosto0 = [SCOSTO] * n
if parameterDict['IFT'].value('value').split('.')[2] != str():
	IFT_0 = IFT.values()
else:
	IFT_0 = [IFT_] * n

outlist2 = ["PHISS_RFM", "SwSS_RFM", "kSS_RFM", "NSF_RFM"]
SSF0 = [0] * n
PHISS0 = [0] * n
kss0 = [0] * n
Swss0 = [1] * n

outlist3 = ["VSHALE_REM_LOW", "VSHALE_REM_MED", "VSHALE_REM_HIGH", "PHIT_REM_LOW","PHIT_REM_MED", "PHIT_REM_HIGH", "VCLD_REM_LOW", "VCLD_REM_MED", "VCLD_REM_HIGH", "VSILT_REM_LOW",  "VSILT_REM_MED", "VSILT_REM_HIGH",\
"VCLB_REM_LOW", "VCLB_REM_MED", "VCLB_REM_HIGH", "PHIE_REM_LOW", "PHIE_REM_MED", "PHIE_REM_HIGH", "VSAND_REM_LOW", "VSAND_REM_MED", "VSAND_REM_HIGH", "VHC_REM_LOW", "VHC_REM_MED", "VHC_REM_HIGH",\
"VWATER_REM_LOW", "VWATER_REM_MED", "VWATER_REM_HIGH", "PERM_REM_LOW", "PERM_REM_MED", "PERM_REM_HIGH", "SWE_REM_LOW", "SWE_REM_MED", "SWE_REM_HIGH", "SWT_REM_LOW", "SWT_REM_MED", "SWT_REM_HIGH",\
"EHC_REM_LOW", "EHC_REM_MED", "EHC_REM_HIGH", "VCLW_REM_LOW", "VCLW_REM_MED", "VCLW_REM_HIGH", "SWB_REM_LOW", "SWB_REM_MED", "SWB_REM_HIGH"]

#Change MissingValue to zero or one
for i in range(0, n):
	if vshale[i] == MissingValue:
		vshale[i] = 0
	if porosity[i] == MissingValue:
		porosity[i] = 0
	if saturation[i] == MissingValue:
		saturation[i] = 1
	if permeability[i] == MissingValue:
		permeability[i] = 0
	
	#Assign values to GWC, GOC, OWC, GAS_GRAD, OIL_GRAD, WTR_GRAD
	if 'GWC_ftTVDSS_NUMBER' in locals():
		gwc0[i] = GWC_ftTVDSS_NUMBER.values()[i]
	else:
		gwc0[i] = GWC_ftTVDSS
	if 'GOC_ftTVDSS_NUMBER' in locals():
		goc0[i] = GOC_ftTVDSS_NUMBER.values()[i]
	else:
		goc0[i] = GOC_ftTVDSS
	if 'OWC_ftTVDSS_NUMBER' in locals():
		owc0[i] = OWC_ftTVDSS_NUMBER.values()[i]
	else:
		owc0[i] = OWC_ftTVDSS
	if 'GAS_GRAD_NUMBER' in locals():
		gas_grad0[i] = GAS_GRAD_NUMBER.values()[i]
	else:
		gas_grad0[i] = GAS_GRAD
	if 'OIL_GRAD_NUMBER' in locals():
		oil_grad0[i] = OIL_GRAD_NUMBER.values()[i]
	else:
		oil_grad0[i] = OIL_GRAD
	if 'WTR_GRAD_NUMBER' in locals():
		wtr_grad0[i] = WTR_GRAD_NUMBER.values()[i]
	else:
		wtr_grad0[i] = WTR_GRAD
	#if 'IFT__NUMBER' in locals():
		#IFT_ = IFT__NUMBER.values()[i]


#******************************************************** End Initialization *****************************************************************************


	#Calculate Pc
	if parameterDict['PC'].value('value').split('.')[2] != str():
		#PC variable is provided
		Pc0[i] = PC.value(i)
		#IFT_0[i] = IFT_
	else:
		Pc0[i], IFT_0[i] = REM_RFM_Enhancement_Equations_rev3.calcPc(dtvd[i], gwc0[i], owc0[i], goc0[i], gas_grad0[i], oil_grad0[i], wtr_grad0[i], scostg0[i], scosto0[i])


#******************************************************** REM-RFM *****************************************************************************
#REM enhancement
#By default, REM Mode MEDIUM is used. However, REM LOW, REM MEDIUM and REM HIGH will still be outputted as secondary REM outputs
LOW = "NO"
if REM_MODE_HIGH == "NO":
	MEDIUM = "YES"
	HIGH = "NO"
elif REM_MODE_HIGH == "YES":
	MEDIUM = "NO"
	HIGH = "YES"
multiplier1, multiplier2 = REM_RFM_Enhancement_Equations_rev3.REM_enhancementinputs(LOW, MEDIUM, HIGH)
multiplier1_LOW, multiplier2_LOW = REM_RFM_Enhancement_Equations_rev3.REM_enhancementinputs(LOW="YES", MEDIUM="NO", HIGH="NO")
multiplier1_MEDIUM, multiplier2_MEDIUM = REM_RFM_Enhancement_Equations_rev3.REM_enhancementinputs(LOW="NO", MEDIUM="YES", HIGH="NO")
multiplier1_HIGH, multiplier2_HIGH = REM_RFM_Enhancement_Equations_rev3.REM_enhancementinputs(LOW="NO", MEDIUM="NO", HIGH="YES")

for i in range(0, n-1):
	deltaD[i] = REM_RFM_Enhancement_Equations_rev3.REMdeltaD(vshale[i], vshale[i+1])

for i in range(1, n):
	deltaU[i] = REM_RFM_Enhancement_Equations_rev3.REMdeltaU(vshale[i], vshale[i-1])

deltaU[0] = deltaD[0]
deltaD[n-1] = deltaU[n-1]

for i in range(0, n):
	AB[i] = REM_RFM_Enhancement_Equations_rev3.function1(deltaD[i], deltaU[i], vshale[i], multiplier1, multiplier2)
	AB_LOW[i] = REM_RFM_Enhancement_Equations_rev3.function1(deltaD[i], deltaU[i], vshale[i], multiplier1_LOW, multiplier2_LOW)
	AB_MEDIUM[i] = REM_RFM_Enhancement_Equations_rev3.function1(deltaD[i], deltaU[i], vshale[i], multiplier1_MEDIUM, multiplier2_MEDIUM)
	AB_HIGH[i] = REM_RFM_Enhancement_Equations_rev3.function1(deltaD[i], deltaU[i], vshale[i], multiplier1_HIGH, multiplier2_HIGH)
	
	AC[i] = REM_RFM_Enhancement_Equations_rev3.function2(AB, i)
	AC_LOW[i] = REM_RFM_Enhancement_Equations_rev3.function2(AB_LOW, i)
	AC_MEDIUM[i] = REM_RFM_Enhancement_Equations_rev3.function2(AB_MEDIUM, i)
	AC_HIGH[i] = REM_RFM_Enhancement_Equations_rev3.function2(AB_HIGH, i)

for i in range(0, n):
	enhancedvshale[i] = REM_RFM_Enhancement_Equations_rev3.function3(AC, i, n)
	enhancedvshale_LOW[i] = REM_RFM_Enhancement_Equations_rev3.function3(AC_LOW, i, n)
	enhancedvshale_MEDIUM[i] = REM_RFM_Enhancement_Equations_rev3.function3(AC_MEDIUM, i, n)
	enhancedvshale_HIGH[i] = REM_RFM_Enhancement_Equations_rev3.function3(AC_HIGH, i, n)
	if CUTOFF_OPTION == "YES":
		if vshale[i] > SSC_VSHALE_cutoff:
			if enhancedvshale[i] < SSC_VSHALE_cutoff:
				enhancedvshale[i] = SSC_VSHALE_cutoff
			if enhancedvshale_LOW[i] < SSC_VSHALE_cutoff:
				enhancedvshale_LOW[i] = SSC_VSHALE_cutoff
			if enhancedvshale_MEDIUM[i] < SSC_VSHALE_cutoff:
				enhancedvshale_MEDIUM[i] = SSC_VSHALE_cutoff
			if enhancedvshale_HIGH[i] < SSC_VSHALE_cutoff:
				enhancedvshale_HIGH[i] = SSC_VSHALE_cutoff

for i in range(0, n):
	deltavshale[i], deltaporosity[i], enhancedporosity[i] = REM_RFM_Enhancement_Equations_rev3.function8(vshale[i], enhancedvshale[i], porosity[i], PHIS, PHICL)
	deltavshale_low[i], deltaporosity_low[i], enhancedporosity_low[i] = REM_RFM_Enhancement_Equations_rev3.function8(vshale[i], enhancedvshale_LOW[i], porosity[i], PHIS, PHICL)
	deltavshale_med[i], deltaporosity_med[i], enhancedporosity_med[i] = REM_RFM_Enhancement_Equations_rev3.function8(vshale[i], enhancedvshale_MEDIUM[i], porosity[i], PHIS, PHICL)
	deltavshale_high[i], deltaporosity_high[i], enhancedporosity_high[i] = REM_RFM_Enhancement_Equations_rev3.function8(vshale[i], enhancedvshale_HIGH[i], porosity[i], PHIS, PHICL)
	if vshale[i] == 0 or porosity[i] == 0:
		continue
	vsilt0_low[i], vcl0_low[i], K0_low[i], swb0_low[i], phie0_low[i], vsand0_low[i], shf0_low[i], swe0_low[i], vclb0_low[i], voil0_low[i], vwater0_low[i], vclw0_low[i] = \
	REM_RFM_Enhancement_Equations_rev3.function9c(vshale[i], enhancedvshale_LOW[i], PHIS, PHICL, porosity[i], GRAIN_RAD0[i], IFT_0[i], b00[i], dtvd[i], m0[i], enhancedporosity_low[i], C0[i], CF, Pc0[i], permeability[i], PERM_OPTION, A_CH[i], B_CH[i])
	vsilt0_med[i], vcl0_med[i], K0_med[i], swb0_med[i], phie0_med[i], vsand0_med[i], shf0_med[i], swe0_med[i], vclb0_med[i], voil0_med[i], vwater0_med[i], vclw0_med[i] = \
	REM_RFM_Enhancement_Equations_rev3.function9c(vshale[i], enhancedvshale_MEDIUM[i], PHIS, PHICL, porosity[i], GRAIN_RAD0[i], IFT_0[i], b00[i], dtvd[i], m0[i], enhancedporosity_med[i], C0[i], CF, Pc0[i], permeability[i], PERM_OPTION, A_CH[i], B_CH[i])
	vsilt0_high[i], vcl0_high[i], K0_high[i], swb0_high[i], phie0_high[i], vsand0_high[i], shf0_high[i], swe0_high[i], vclb0_high[i], voil0_high[i], vwater0_high[i], vclw0_high[i] = \
	REM_RFM_Enhancement_Equations_rev3.function9c(vshale[i], enhancedvshale_HIGH[i], PHIS, PHICL, porosity[i], GRAIN_RAD0[i], IFT_0[i], b00[i], dtvd[i], m0[i], enhancedporosity_high[i], C0[i], CF, Pc0[i], permeability[i], PERM_OPTION, A_CH[i], B_CH[i])

	if THINBEDS_RT_OPTION == "YES":
		if int(facies[i]) == int(THINBEDS_RT_flag):
			#Run REM
			vsilt0[i], vcl0[i], K0[i], swb0[i], phie0[i], vsand0[i], shf0[i], swe0[i], vclb0[i], voil0[i], vwater0[i], vclw0[i] = \
			REM_RFM_Enhancement_Equations_rev3.function9c(vshale[i], enhancedvshale[i], PHIS, PHICL, porosity[i], GRAIN_RAD0[i], IFT_0[i], b00[i], dtvd[i], m0[i], enhancedporosity[i], C0[i], CF, Pc0[i], permeability[i], PERM_OPTION, A_CH[i], B_CH[i])
		else:
			# Use SSC results
			vsilt0[i] = vsilt_ssc[i]
			vcl0[i] = vclw_ssc[i]
			K0[i] = permeability[i]
			swb0[i] = abs(porosity[i] - phie_ssc[i]) / porosity[i]
			phie0[i] = phie_ssc[i]
			vsand0[i] = vsand_ssc[i]
			shf0[i] = shf_ssc[i]
			swe0[i] = swe_ssc[i]
			vclb0[i] = vclb_ssc[i]
			voil0[i] = (1 - shf_ssc[i]) * porosity[i]
			vwater0[i] = phie_ssc[i] - voil0[i]
			vclw0[i] = vclw_ssc[i]
			enhancedporosity[i] = porosity[i]
			enhancedvshale[i] = vshale[i]
	else:
		if vshale[i] <= SSC_VSHALE_cutoff:
			vsilt0[i] = vsilt_ssc[i]
			vcl0[i] = vclw_ssc[i]
			K0[i] = permeability[i]
			swb0[i] = abs(porosity[i] - phie_ssc[i]) / porosity[i]
			phie0[i] = phie_ssc[i]
			vsand0[i] = vsand_ssc[i]
			shf0[i] = shf_ssc[i]
			swe0[i] = swe_ssc[i]
			vclb0[i] = vclb_ssc[i]
			voil0[i] = (1 - shf_ssc[i]) * porosity[i]
			vwater0[i] = phie_ssc[i] - voil0[i]
			vclw0[i] = vclw_ssc[i]
			enhancedporosity[i] = porosity[i]
			enhancedvshale[i] = vshale[i]
		else:
			#Run REM
			vsilt0[i], vcl0[i], K0[i], swb0[i], phie0[i], vsand0[i], shf0[i], swe0[i], vclb0[i], voil0[i], vwater0[i], vclw0[i] = \
			REM_RFM_Enhancement_Equations_rev3.function9c(vshale[i], enhancedvshale[i], PHIS, PHICL, porosity[i], GRAIN_RAD0[i], IFT_0[i], b00[i], dtvd[i], m0[i], enhancedporosity[i], C0[i], CF, Pc0[i], permeability[i], PERM_OPTION, A_CH[i], B_CH[i])

	# Generate QC
	if enhancedvshale[i] > vshale[i]:
		qc_flag[i] = -1	
	elif enhancedvshale[i] < vshale[i]:
		qc_flag[i] = 1

	#Calculate EHC
	try:
		ehc0[i] = REM_RFM_Enhancement_Equations_rev3.function10(shf0[i], enhancedporosity[i], dtvd[i], dtvd[i-1])
		ehc0_low[i] = REM_RFM_Enhancement_Equations_rev3.function10(shf0_low[i], enhancedporosity_low[i], dtvd[i], dtvd[i-1])
		ehc0_med[i] = REM_RFM_Enhancement_Equations_rev3.function10(shf0_med[i], enhancedporosity_med[i], dtvd[i], dtvd[i-1])
		ehc0_high[i] = REM_RFM_Enhancement_Equations_rev3.function10(shf0_high[i], enhancedporosity_high[i], dtvd[i], dtvd[i-1])
		ehc0_ssc[i] = REM_RFM_Enhancement_Equations_rev3.function10(shf_ssc[i], porosity[i], dtvd[i], dtvd[i-1])
	except IndexError:
		pass
	
	try:
		ehc_r = ehc0[i] / ehc0_ssc[i]
		if ehc_r >= 1.1:
			ehc10[i] = 1
		if ehc_r >= 1.3:
			ehc30[i] = 1
	except ZeroDivisionError or OverflowError:
		if ehc0[i] > 0:
			ehc10[i] = 1
			ehc30[i] = 1
		else:
			ehc10[i] = 0
			ehc30[i] = 0
		
	if RFM_MODULE == "YES":
		if THINBEDS_RT_OPTION == "YES":
			if int(facies[i]) == int(THINBEDS_RT_flag):
				#Run RFM for PC > 0
				if Pc0[i] > 0:
					PHISS0[i], kss0[i], Swss0[i], SSF0[i] = \
				REM_RFM_Enhancement_Equations_rev3.functionH2a(phie0[i], enhancedporosity[i], vclw0[i], vsilt0[i], enhancedvshale[i], K0[i], shf0[i], swb0[i], dtvd[i], Pc0[i], IFT_0[i], b00[i], GRAIN_RAD0[i], m0[i], C0[i], PHIS, PHICL, MinVCLW, MaxPERM)
					# Generate training dataset for Multi Linear Regression
					if Pc0[i] > Pc_Cutoff:
						ssf_.append(SSF0[i])
						phit_.append(enhancedporosity[i])
						vsilt_.append(vsilt0[i])
						vclw_.append(vclw0[i])
			else:
				#Use SSC results
				PHISS0[i] = enhancedporosity[i]
				kss0[i] = K0[i]
				Swss0[i] = shf0[i]
				SSF0[i] = 1
		else:
			if vshale[i] <= SSC_VSHALE_cutoff:
				#Use SSC results
				PHISS0[i] = enhancedporosity[i]
				kss0[i] = K0[i]
				Swss0[i] = shf0[i]
				SSF0[i] = 1
			else:
				#Run RFM for PC > 0
				if Pc0[i] > 0:
					PHISS0[i], kss0[i], Swss0[i], SSF0[i] = \
				REM_RFM_Enhancement_Equations_rev3.functionH2a(phie0[i], enhancedporosity[i], vclw0[i], vsilt0[i], enhancedvshale[i], K0[i], shf0[i], swb0[i], dtvd[i], Pc0[i], IFT_0[i], b00[i], GRAIN_RAD0[i], m0[i], C0[i], PHIS, PHICL, MinVCLW, MaxPERM)
					# Generate training dataset for Multi Linear Regression
					if Pc0[i] > Pc_Cutoff:
						ssf_.append(SSF0[i])
						phit_.append(enhancedporosity[i])
						vsilt_.append(vsilt0[i])
						vclw_.append(vclw0[i])
	else:
		continue

# Conduct Multi Linear Regression for SSF calculation below FWL
if len(ssf_) != 0:
	b, R2 = REM_RFM_Enhancement_Equations_rev3.SSF3MultiLinearRegression(ssf_, phit_, vsilt_, vclw_)
	y0 = b[0]
	y1 = b[1]
	y2 = b[2]
	y3 = b[3]
else:
	if RFM_MODULE == "YES":
		print("No training data points for SSF Multi Linear Regression!")
	y0 = 0
	y1 = 0
	y2 = 0
	y3 = 0

# Calculate SSF for PC < 0
for i in range(0, n):
	if vshale[i] == 0 or porosity[i] == 0:
		continue
	if RFM_MODULE == "YES":
		if MLR_OPTION == "YES":
			if THINBEDS_RT_OPTION == "YES":
				if int(facies[i]) == int(THINBEDS_RT_flag) and Pc0[i] <= 0:
					PHISS0[i], kss0[i], Swss0[i], SSF0[i] = \
					REM_RFM_Enhancement_Equations_rev3.functionH2b(phie0[i], enhancedporosity[i], vclw0[i], vsilt0[i], enhancedvshale[i], K0[i], shf0[i], swb0[i], dtvd[i], Pc0[i], IFT_0[i], b00[i], GRAIN_RAD0[i], m0[i], C0[i], PHIS, PHICL, MinVCLW, MaxPERM, y0, y1, y2, y3)
			else:
				if vshale[i] >= SSC_VSHALE_cutoff and Pc0[i] <= 0:
					PHISS0[i], kss0[i], Swss0[i], SSF0[i] = \
					REM_RFM_Enhancement_Equations_rev3.functionH2b(phie0[i], enhancedporosity[i], vclw0[i], vsilt0[i], enhancedvshale[i], K0[i], shf0[i], swb0[i], dtvd[i], Pc0[i], IFT_0[i], b00[i], GRAIN_RAD0[i], m0[i], C0[i], PHIS, PHICL, MinVCLW, MaxPERM, y0, y1, y2, y3)
		elif MLR_OPTION == "NO":
			if THINBEDS_RT_OPTION == "YES":
				if int(facies[i]) == int(THINBEDS_RT_flag):
					PHISS0[i], kss0[i], Swss0[i], SSF0[i] = \
					REM_RFM_Enhancement_Equations_rev3.functionH2c(phie0[i], enhancedporosity[i], vclw0[i], vsilt0[i], enhancedvshale[i], K0[i], shf0[i], swb0[i], dtvd[i], Pc0[i], IFT_0[i], b00[i], GRAIN_RAD0[i], m0[i], C0[i], PHIS, PHICL, MinVCLW, MaxPERM, CONST0, CONST1, CONST2)
			else:
				if vshale[i] >= SSC_VSHALE_cutoff:
					PHISS0[i], kss0[i], Swss0[i], SSF0[i] = \
					REM_RFM_Enhancement_Equations_rev3.functionH2c(phie0[i], enhancedporosity[i], vclw0[i], vsilt0[i], enhancedvshale[i], K0[i], shf0[i], swb0[i], dtvd[i], Pc0[i], IFT_0[i], b00[i], GRAIN_RAD0[i], m0[i], C0[i], PHIS, PHICL, MinVCLW, MaxPERM, CONST0, CONST1, CONST2)


#******************************************************** End of REM-RFM *****************************************************************************


for i in outlist:
	if db.variableExists(w, dsname, i):
		continue
	else:
		db.variableCreate(w, dsname, i, 1)
		db.variableGroupChange(w, dsname, i, ['REM'])

if RFM_MODULE == "YES":
	for i in outlist2:
		if db.variableExists(w, dsname, i):
			continue
		else:
			db.variableCreate(w, dsname, i, 1)
			db.variableGroupChange(w, dsname, i, ['RFM'])
	PHISS_RFM.setValues(PHISS0)
	kSS_RFM.setValues(kss0)
	SwSS_RFM.setValues(Swss0)
	NSF_RFM.setValues(SSF0)
	PHISS_RFM.saveTemp()
	kSS_RFM.saveTemp()
	SwSS_RFM.saveTemp()
	NSF_RFM.saveTemp()
else:
	pass

for i in outlist3:
	if db.variableExists(w, dsname, i):
		continue
	else:
		db.variableCreate(w, dsname, i, 1)
		db.variableGroupChange(w, dsname, i, ['REM_SECONDARY'])


PHIT_REM.setValues(enhancedporosity)
VCLD_REM.setValues(vcl0)
VSILT_REM.setValues(vsilt0)
VCLB_REM.setValues(vclb0)
PHIE_REM.setValues(phie0)
VSAND_REM.setValues(vsand0)
PERM_REM.setValues(K0)
VHC_REM.setValues(voil0)
VWATER_REM.setValues(vwater0)
SWE_REM.setValues(swe0)
SWT_REM.setValues(shf0)
EHC_REM.setValues(ehc0)
VCLW_REM.setValues(vclw0)
VSHALE_REM.setValues(enhancedvshale)
SWB_REM.setValues(swb0)
PC_REM.setValues(Pc0)
EHC_SSC.setValues(ehc0_ssc)
EHC_R10.setValues(ehc10)
EHC_R30.setValues(ehc30)
PHIT_REM.saveTemp()
VCLD_REM.saveTemp()
VSILT_REM.saveTemp()
VCLB_REM.saveTemp()
PHIE_REM.saveTemp()
VSAND_REM.saveTemp()
PERM_REM.saveTemp()
VHC_REM.saveTemp()
VWATER_REM.saveTemp()
SWE_REM.saveTemp()
SWT_REM.saveTemp()
EHC_REM.saveTemp()
VSHALE_REM.saveTemp()
VCLW_REM.saveTemp()
SWB_REM.saveTemp()
PC_REM.saveTemp()
EHC_SSC.saveTemp()
EHC_R10.saveTemp()
EHC_R30.saveTemp()

VSHALE_REM_LOW.setValues(enhancedvshale_LOW)
VSHALE_REM_MED.setValues(enhancedvshale_MEDIUM)
VSHALE_REM_HIGH.setValues(enhancedvshale_HIGH)
PHIT_REM_LOW.setValues(enhancedporosity_low)
PHIT_REM_MED.setValues(enhancedporosity_med)
PHIT_REM_HIGH.setValues(enhancedporosity_high)
VCLD_REM_LOW.setValues(vcl0_low)
VCLD_REM_MED.setValues(vcl0_med)
VCLD_REM_HIGH.setValues(vcl0_high)
VSILT_REM_LOW.setValues(vsilt0_low)
VSILT_REM_MED.setValues(vsilt0_med)
VSILT_REM_HIGH.setValues(vsilt0_high)
VCLB_REM_LOW.setValues(vclb0_low)
VCLB_REM_MED.setValues(vclb0_med)
VCLB_REM_HIGH.setValues(vclb0_high)
PHIE_REM_LOW.setValues(phie0_low)
PHIE_REM_MED.setValues(phie0_med)
PHIE_REM_HIGH.setValues(phie0_high)
VSAND_REM_LOW.setValues(vsand0_low)
VSAND_REM_MED.setValues(vsand0_med)
VSAND_REM_HIGH.setValues(vsand0_high)
VHC_REM_LOW.setValues(voil0_low)
VHC_REM_MED.setValues(voil0_med)
VHC_REM_HIGH.setValues(voil0_high)
VWATER_REM_LOW.setValues(vwater0_low)
VWATER_REM_MED.setValues(vwater0_med)
VWATER_REM_HIGH.setValues(vwater0_high)
PERM_REM_LOW.setValues(K0_low)
PERM_REM_MED.setValues(K0_med)
PERM_REM_HIGH.setValues(K0_high)
SWE_REM_LOW.setValues(swe0_low)
SWE_REM_MED.setValues(swe0_med)
SWE_REM_HIGH.setValues(swe0_high)
SWT_REM_LOW.setValues(shf0_low)
SWT_REM_MED.setValues(shf0_med)
SWT_REM_HIGH.setValues(shf0_high)
EHC_REM_LOW.setValues(ehc0_low)
EHC_REM_MED.setValues(ehc0_med)
EHC_REM_HIGH.setValues(ehc0_high)
VCLW_REM_LOW.setValues(vclw0_low)
VCLW_REM_MED.setValues(vclw0_med)
VCLW_REM_HIGH.setValues(vclw0_high)
SWB_REM_LOW.setValues(swb0_low)
SWB_REM_MED.setValues(swb0_med)
SWB_REM_HIGH.setValues(swb0_high)
QC_REM.setValues(qc_flag)

VSHALE_REM_LOW.saveTemp()
VSHALE_REM_MED.saveTemp
VSHALE_REM_HIGH.saveTemp()
PHIT_REM_LOW.saveTemp()
PHIT_REM_MED.saveTemp()
PHIT_REM_HIGH.saveTemp()
VCLD_REM_LOW.saveTemp()
VCLD_REM_MED.saveTemp()
VCLD_REM_HIGH.saveTemp()
VSILT_REM_LOW.saveTemp()
VSILT_REM_MED.saveTemp()
VSILT_REM_HIGH.saveTemp()
VCLB_REM_LOW.saveTemp()
VCLB_REM_MED.saveTemp()
VCLB_REM_HIGH.saveTemp()
PHIE_REM_LOW.saveTemp()
PHIE_REM_MED.saveTemp()
PHIE_REM_HIGH.saveTemp()
VSAND_REM_LOW.saveTemp()
VSAND_REM_MED.saveTemp()
VSAND_REM_HIGH.saveTemp()
VHC_REM_LOW.saveTemp()
VHC_REM_MED.saveTemp()
VHC_REM_HIGH.saveTemp()
VWATER_REM_LOW.saveTemp()
VWATER_REM_MED.saveTemp()
VWATER_REM_HIGH.saveTemp()
PERM_REM_LOW.saveTemp()
PERM_REM_MED.saveTemp()
PERM_REM_HIGH.saveTemp()
SWE_REM_LOW.saveTemp()
SWE_REM_MED.saveTemp()
SWE_REM_HIGH.saveTemp()
SWT_REM_LOW.saveTemp()
SWT_REM_MED.saveTemp()
SWT_REM_HIGH.saveTemp()
EHC_REM_LOW.saveTemp()
EHC_REM_MED.saveTemp()
EHC_REM_HIGH.saveTemp()
VCLW_REM_LOW.saveTemp()
VCLW_REM_MED.saveTemp()
VCLW_REM_HIGH.saveTemp()
SWB_REM_LOW.saveTemp()
SWB_REM_MED.saveTemp()
SWB_REM_HIGH.saveTemp()
QC_REM.saveTemp()

if DISPLAY_LAYOUT == "YES":
	#Display layout
	idLV = plot.logViewGetIdByName("REM_Layout_" + w)
	if idLV == -1:
		if db.objectExists("REM_Layout_" + w + ".xml", db.objectTypeList().index("Layout"), 'project'):
			idLV = plot.logViewOpen("Project/REM_Layout_" + w + ".xml", 'project', 0)
		else:
			idLV = plot.logViewApplyTemplate("Company/REM_template_rev2.xml", w, False)
			plot.logViewSave(idLV, "REM_Layout_" + w, "Project", 0)
		
		plot.logViewSetName(idLV, "REM_Layout_" + w)
	else:
		plot.logViewSave(idLV, "REM_Layout_" + w)

#Alhamdulillah

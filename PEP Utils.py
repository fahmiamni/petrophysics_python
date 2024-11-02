from math import *
from hydrocarbon_correction import HydrocarbonCorrection, HydrocarbonInputsFirstEquationInputs, HydrocarbonInputsSecondEquationInputs, HydrocarbonInputsThirdEquationInputs, HydrocarbonInputsFourthEquationInputs, HydrocarbonInputsFifthEquationInputs, HydrocarbonInputsSixthEquationInputs
from TechlogMath import *
from operator import *
import sys

if sys.version_info[0]==3:
	from six.moves import range


PI     = 3.14159265358979323846
PIO2   = 1.57079632679489661923
PIO4   = 7.85398163397448309616E-1
SQRT2  = 1.41421356237309504880
SQRTH  = 7.07106781186547524401E-1
E      = exp(1)
LN2    = log(2)
LN10   = log(10)
LOG2E  = 1.4426950408889634073599
LOG10E = 1.0 / LN10
MissingValue = -9999
def iif(condition, trueResult=MissingValue, falseResult=MissingValue):
	if condition:
		return trueResult
	else:
		return falseResult

#region **Declarations**
#The dictionary of parameters v2.0
#name,bname,type,family,measurement,unit,value,mode,description,group,min,max,list,enable,iscombocheckbox,isused
parameterDict = {}
try:
	if Parameter:
		pass
except NameError:
	class Parameter:
		def __init__(self, **d):
			pass

__pyVersion__ = """3"""
#endregion DeclarationsEnd

# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.6 (default, Jan  8 2020, 20:23:39) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pep_utils_.py
# Compiled at: 2021-06-22 10:34:47
from datetime import datetime
import TechlogDialog as tlDialog
from math import exp, log, tan, atan, degrees, radians, sin, cos, pow
from Techlog import MissingValue
from TechlogMath import limitValue, log10
from math import *
from TechlogMath import *
from operator import *
import sys
if sys.version_info[0] == 3:
	from six.moves import range
PI = 3.141592653589793
PIO2 = 1.5707963267948966
PIO4 = 0.7853981633974483
SQRT2 = 1.4142135623730951
SQRTH = 0.7071067811865476
E = exp(1)
LN2 = log(2)
LN10 = log(10)
LOG2E = 1.4426950408889634
LOG10E = 1.0 / LN10
MissingValue = -9999


def iif(condition, trueResult=MissingValue, falseResult=MissingValue):
	if condition:
		return trueResult
	else:
		return falseResult


parameterDict = {}
try:
	if Parameter:
		pass
except NameError:

	class Parameter():

		def __init__(self, **d):
			pass


parameterDict = {}
try:
	if Parameter:
		pass
except NameError:

	class Parameter():

		def __init__(self, **d):
			pass


def isNotEmpty(valueList):
	for val in valueList:
		if val != MissingValue:
			return True

	return False


def computeMonteCarlo(distribution_list, loopIterator, loopSize, ITR_NO, dist_array, P1P, P2P, P3P, val_min = 0, val_max = 1):
	DISTR_LIST = []
	for j in range(dist_array):
		DISTR_LIST.append(distribution_list[(loopIterator + loopSize * j)])

	var_min = MissingValue
	var_max = MissingValue
	var_mean = MissingValue
	var_1p = MissingValue
	var_2p = MissingValue
	var_3p = MissingValue
	if isNotEmpty(DISTR_LIST):
		var_min, var_max, var_mean, var_1p, var_2p, var_3p = MY_CALCULATION_1P2P3P(
			DISTR_LIST, dist_array, P1P, P2P, P3P, ITR_NO, val_min, val_max)
	return (var_min, var_max, var_mean, var_1p, var_2p, var_3p)
	
def populateDistribution(distribution_list, var, loopIterator, loopSize, distribution_list_count, val_min = 0, val_max = 1):
	if var != MissingValue:
		j = int((var-val_min)/(val_max-val_min) * distribution_list_count)
		if j < 0:
			j = 0
		elif j >= distribution_list_count:
			j = distribution_list_count - 1
		ss = loopIterator + loopSize * j
		if distribution_list[ss] == MissingValue:
			distribution_list[ss] = 1
		else:
			distribution_list[ss] = distribution_list[ss] + 1
	return distribution_list

def performVariableOffsetting(value, min, max, relativeOffset):
	offsettedValue = value
	if value != MissingValue and relativeOffset != MissingValue:
		if relativeOffset >= 0.0:
			if max != MissingValue:
				offsettedValue += relativeOffset * (max - value)
		elif min != MissingValue:
			offsettedValue += relativeOffset * (value - min)
	return offsettedValue

def MY_CALCULATION_1P2P3P(dat_d, dist_array, P1P, P2P, P3P, ITR_NO, val_min, val_max):
	datmin = MissingValue
	datmax = MissingValue
	dat_1p = MissingValue
	dat_2p = MissingValue
	dat_3p = MissingValue
	cum_d = [0 for j in range(dist_array)]
	if dat_d[0] != MissingValue:
		cum_d[0] = dat_d[0]
		datavg = dat_d[0]
	else:
		cum_d[0] = 0
		datavg = 0
	for j in range(1, dist_array):
		if dat_d[j] != MissingValue:
			cum_d[j] = cum_d[(j - 1)] + dat_d[j]
			datavg = datavg + j * dat_d[j]
		else:
			cum_d[j] = cum_d[(j - 1)]

	datavg = (datavg / ITR_NO / dist_array)*(val_max-val_min)+val_min
	sat1 = 0.005 * cum_d[(dist_array - 1)]
	sat2 = 0.995 * cum_d[(dist_array - 1)]
	cut1p = float(P1P) / 100 * cum_d[(dist_array - 1)]
	cut2p = float(P2P) / 100 * cum_d[(dist_array - 1)]
	cut3p = float(P3P) / 100 * cum_d[(dist_array - 1)]
	for j in range(dist_array):
		if cum_d[j] >= sat1:
			datmin = (j / dist_array)*(val_max-val_min)+val_min
			sat1 = cum_d[(dist_array - 1)] + 1
		if cum_d[j] >= sat2:
			datmax = (j / dist_array)*(val_max-val_min)+val_min
			sat2 = cum_d[(dist_array - 1)] + 1
		if cum_d[j] >= cut1p:
			dat_1p = (j / dist_array)*(val_max-val_min)+val_min
			cut1p = cum_d[(dist_array - 1)] + 1
		if cum_d[j] >= cut2p:
			dat_2p = (j / dist_array)*(val_max-val_min)+val_min
			cut2p = cum_d[(dist_array - 1)] + 1
		if cum_d[j] >= cut3p:
			dat_3p = (j / dist_array)*(val_max-val_min)+val_min
			cut3p = cum_d[(dist_array - 1)] + 1
	return (datmin, datmax, datavg, dat_1p, dat_2p, dat_3p)

def MTCARLO(mc_dist, ITR_NO):
	"""Random Number from MC
		Inputs:
		1. mc_dist [string]: Type of Unc. Dist.
		Output:
		- [number] mc_ofs: Random value
		"""
	from numpy import random
	import random as pyrandom
	mc_ofs = [MissingValue for i in range(ITR_NO)]
	if mc_dist == 'Normal':
		for i in range(ITR_NO):
			mc_ofs[i] = random.normal(0, 0.3333)

	elif mc_dist == 'Uniform':
		for i in range(ITR_NO):
			mc_ofs[i] = random.uniform(-1, 1)

	else:
		for i in range(ITR_NO):
			rn = pyrandom.random()
			if rn < 0.5:
				randomtri = -1 + (2 * rn) ** 0.5
			else:
				randomtri = 1 - (2 * (1 - rn)) ** 0.5
			mc_ofs[i] = randomtri

	return mc_ofs


def SSC_MAIN_A(LITHMOD, GR, ZNGRSD, ZNGRCL, RHODRYSL, RHOB_DRY_SAND, LITHTYPE, PEFDRYLM, PEFDRYDL, RHOBDRYLM, 
			   RHOBDRYDL, RHOBDRYQZ, RHOBFLC, RHOBDRYMIN1, PEFDRYQZ, PEFDRYMIN1, znhcor, HCREF, EXT_REF_LOG, znrw, 
			   rt, zn_m, zn_n, NEUTOOL, CLAYFLG, GRCALC, ZNGRCLN, ZNGRCLY, RHOBDRYCLY, ZNRHOWCL, 
			   nphi, NEUOFFSET, rhob, PEF, PEFOFFSET, PEFDRYCLY, PEFDRYMIN2, RHOBDRYMIN2, NPHIDRYLM, NPHIDRYDL, 
			   NPHIDRYQZ, NPHIDRYMIN1, NPHIDRYMIN2, MFRES, MFTEMP, ZNTEMPUNIT, znogf, RHO_OIL, RHO_GAS, NEUTRONFAC, 
			   COR_METHOD, DEGHCCOR, DNXPLOTSAND, RHOB_FLUID, NPHI_DRY_SAND, NPHI_OFFSET, NPHI_FLUID, ZNRHOBCL, ZNNPHICL, ZNSLTLINRAT, 
			   BH_CORR, znsynrcl, znsynrsd, BHCTYP, EXTRHOBFLG, CORR_RHOB_LOG, LITH2FLG, ZNNPHWCL, USE_SILT_ANGLE, DEGFLSLT, 
			   SOURCE_SYN_LOG, dt, SWT_FLAG, BYPASS_LITHO_PORO_CALCULATION, X_RHOB, SHALE_NEUT, RHOB_FC, NPHI_FC, sand_madens, fluid_dens, 
			   SAND_LN, SHALE_LN, XMINHCORR, XMAXHCORR, XMINHCORR_LEFTLIMB, XMAXHCORR_LEFTLIMB,COR_LIMIT_MANUAL):
	#region
	"""Calculates LITHO_VOLUMES for SSC and CARB cases, and perform hydrocarbon correction
		Inputs:
		 1. LITHMOD [string]: Lithology mode. SSC or CARB.
		 2. GR [number]: Gamma Ray log
		 3. ZNGRSD [number]: Zoned Gamma Ray Sand
		 4. ZNGRCL [number]: Zoned Gamma Ray Clay
		 5. RHODRYCL [number]: Density Dry Clay
		 6. RHODRYSL [number]: Density Dry Silt
		 7. RHOB_DRY_SAND [number]: RHOB Dry Sand
		 19. LITHTYPE [string]: Lithology Components
		 20. PEFDRYLM [number]: PEF Calcite
		 21. PEFDRYDL [number]: PEF Dolomite
		 25. RHOBDRYLM [number]: RHOB Calcite
		 26. RHOBDRYDL [number]: RHOB Dolomite
		 27. RHOBDRYQZ [number]: RHOB Quartz
		 28. RHOBFLC [number]: Fluid Density
		 29. RHOBDRYMIN1 [number]: RHOB Mineral-1
		 32. PEFDRYQZ [number]: PEF Quartz
		 33. PEFDRYMIN1 [number]: PEF Mineral-1
		 41. znhcor [number]: HC Correction Factor #1   [Auto=-1, Manual>0]. Corresponds to HCCOR parameter
		 42. HCREF [string]: Reference for Automatic HC Correction. Corresponds to ZNRW parameter
		 43. znrw [number] [ohmm]: Zoned RW at Reservoir Condition
		 44. rt [number] [ohmm]: True Resistivity Log
		 45. zn_m
		 46. zn_n
		 48. NEUTOOL [string]: Neutron Tool Type
		 49. CLAYFLG [string]: Model With Clay
		 50. GRCALC [string]: Type of VCL_GR Equation
		 51. ZNGRCLN [number]: Zoned Gamma Ray Clean (Carbonates)
		 52. ZNGRCLY [number]: Zoned Gamma Ray Clay (Carbonates)
		 53. RHOBDRYCLY [number]: RHOB Dry Clay
		 54. ZNRHOWCL [number]: Zoned RHOB Clay (Carbonates)
		 12. NPHI [number]: Neutron Porosity Log
		 13. NEUOFFSET [number]: Offset for NPHI Log
		 14. RHOB [number]: Bulk Density Log
		 15. PEF [number]: Photo Electric Log
		 16. PEFOFFSET [number]: Offset for PEF Log
		 17. PEFDRYCLY [number]: PEF Dry Clay
		 9. PEFDRYMIN2 [number]: PEF Mineral 2
		 10. RHOBDRYMIN2 [number]: RHOB Mineral 2
		 11. NPHIDRYLM [number]: Calcite Neutron Porosity
		 12. NPHIDRYDL [numbee]: Dolomite Neutron Porosity
		 13. NPHIDRYQZ [number]: Quartz Neutron Porosity
		 14. NPHIDRYMIN1 [number]: Mineral 1 Neutron Porosity
		 15. NPHIDRYMIN2 [number]: Mineral 2 Neutron Porosity
		 16. TEMP_UNIT [string]: Temperature unit DEGC or DEGF. Coming from parameters
		 17. MFRES [number]: Mud Filtrate Resistivity
		 18. MFTEMP [number]: Mud Filtrate Temperature
		 19. ZNTEMPUNIT [number]: Temperature, coming from TEMP_SAL_ZONATION
		 20. znogf [number]: Zoned Oil-Gas Flag
		 17. RHO_OIL [number] [g/cc]: Oil Density (< 0.70 g/cc)
		 18. RHO_GAS [number] [g/cc]: Gas Density
		 20. NEUTRONFAC [number]: Neutron Factor (comes from NEUFAC parameter)
		 22: COR_METHOD [string]: Correction Method (from parameters)
		 23: DEGHCCOR [number] [dega]: Angle for correction
		 24. DNXPLOTSAND [string]: Type of Sand Line on DN Crossplot
		 3. RHOB_FLUID [number]: RHOB Fluid
		 4. NPHI_DRY_SAND [number]: NPHI Dry Sand
		 5. NPHI_FLUID [number]: NPHI Fluid
		 6. ZNRHOBCL [number]: Zoned RHOB Clay
		 7. ZNNPHICL [number]: Zoned NPHI Clay
		 8. ZNSLTLINRAT [number]: Zoned Silt Line Position
		 3. BH_CORR [string]: Do Bad Hole Correction [YES/NO]
		 4. znsynrcl [g/cc]: Zoned Synthetic RHOB_CLAY
		 5. znsynrsd [g/cc]: Zoned Synthetic RHOB Sand
		 6. BHCTYP [number]: Bad Hole Flag Type (relates to parameter BHCTYP*)
		 11. CORR_RHOB_LOG [number] [g/cc]: External Bulk Density, to use to correct when Bhcorrflag==2
		 13. LITH2FLG [string]: 2-Minerals Volume Calculation Method
		 14. ZNNPHWCL [number]: Carbonates parameter, coming from CARB_ZONATION
		 15. rw [number]: Water resistivity
		X_RHOB [number]
		SHALE_NEUT [number]
		RHOB_FC [number]
		NPHI_FC [number]
		sand_madens [number]
		fluid_dens [number]
		SAND_LN [number]
		SHALE_LN [number]
		XMINHCORR [number]
		XMAXHCORR [number]
		XMINHCORR_LEFTLIMB [number]
		XMAXHCORR_LEFTLIMB [number]
		COR_LIMIT_MANUAL [number]


		 Outputs:
		 - [number] VSHGR: VSH Gamma Ray
		 - [number] grsndsltfrac: GR Sand-Silt Ratio
		 - [number] grclysltfrac: GR Clay-Silt Ratio
		 - [number] grclayfrac: GR Clay Fraction
		 - [number] grsandfrac: GR Sand Fraction
		 - [number] grsiltfrac: GR Silt Fraction
		 - [number] peflith2frac PEF Litho-2 Fraction
		 - [number] PEFCALCFRAC PEF Calc Fraction
		 - [number] PEFDOLOFRAC PEF Dolo Fraction
		 - [number] PEFQRTZFRAC PEF Qrtz Fraction
		 - [number] PEFMIN1FRAC PEF Min1 Fraction
		 - [number] RHOG: Grain Density
		 - [number] phit: Total Porosity
		 - [number] VMATRX: 1 minus Total Porosity
		 - [number] VSAND: Volume of Dry Sandstone
		 - [number] VSILT: Volume of Dry Siltstone
		 - [number] VCLD: Volume of Dry Clay
		 - [number] VCLB: Volume of Clay Bound Water
		 - [number] VCLW: Volume of Wet Clay 
		 - [number] VSHALE: Volume of Shale
		 - [number] nphicc: NPHI Clay Corrected (Carbonates)
		 - [number] rhobcc: RHOB Clay Corrected (Carbonates)
		 - [number] PEFCC: PEF Clay Corrected (Carbonates)
		 - [number] ucc: U Clay Corrected (Carbonates)
		 - [number] calcfrac: Calcite Fraction (Carbonates)
		 - [number] dolofrac: Dolomite Fraction (Carbonates)
		 - [number] QRTZFRAC: Quartz Fraction
		 - [number] MIN1FRAC: Mineral 1 Fraction
		 - [number] MIN2FRAC: Mineral 2 Fraction
		 - [number] VCALC: Volume of Calcite
		 - [number] VDOLO: Volume of Dolomite
		 - [number] VQRTZ: VOlume of Quartz
		 - [number] VMIN1: Volume of Mineral 1
		 - [number] VMIN2: Volume of Mineral 2
		 - [number] PHIE: Effective Porosity
		 - [number] PDCALCFRAC PEF-DEN Calc Fraction  (Carbonates)
		 - [number] PEF-DEN Dolo Fraction  (Carbonates)
		 - [number] PEF-DEN Qrtz Fraction  (Carbonates)
		 - [number] PEF-DEN Min1 Fraction  (Carbonates)
		 - [number] SALINWAT: Fluid Parameters for Density
		 - [number] NPHIFLC: Fluid Parameters for Neutron
		 - [number] NPHITOOLDL: Fluid Parameters for Neutron
		 - [number] NPHITOOLQZ: Fluid Parameters for Neutron
		 - [number] PEFFLLM: Fluid Parameters for PEF
		 - [number] PEFFLDL: Fluid Parameters for PEF
		 - [number] PEFFLQZ: Fluid Parameters for PEF
		 - [number] PEFFLMIN1: Fluid Parameters for PEF
		 - [number] UFL: Fluid Parameters for for M-N Plot
		 - [number] VSHGR: VSH Gamma Ray
		 - [number] GRCLAYFRAC: GR Clay Fraction
		 - [number] RHODRYCL: Density Dry Clay
		 - [number] mclayln: WetClay Angle 
		 - [number] cclayln: WetClay Angle 
		 - [number] NPHDRYCL: Neutron Dry Clay
		 - [number] PHITCLY: PHITCLY
		 - [number] NPHICC: NPHI Clay Corrected (Carbonates)
		 - [number] PEFCC: PEF Clay Corrected (Carbonates)
		 - [number] CLAYFRAC: Clay Fraction
		 - [number] UCC: U Clay Corrected (Carbonates)
		 - [number] SNDSLTFRAC: Sand-Silt Ratio
		 - [number] CLYSLTFRAC: Clay-Silt Ratio
		 - [number] SANDFRAC: Sand Fraction
		 - [number] SILTFRAC: Silt Fraction
		 - [number]: cmatdclln: Intermediate ouput (not to be saved)
		 - [number] mmatdclln: Intermediate output (not to be saved)
		 - [number] DNCLAYFRAC: DN Clay Fraction (Carbonates)
		 - [number] PDLITH2FRAC: PEF-DEN Litho-2 Fraction  (Carbonates)
		 - [number] mncalcfrac: M-N cal Fraction  (Carbonates)
		 - [number] mndolofrac: M-N Dolo Fraction  (Carbonates)
		 - [number] mnqrtzfrac: M-N Quartz Fraction (Carbonates)
		 - [number] mnmin1frac: M-N Mineral 1 Fraction (Carbonates)
		 - [number] mnmin2frac: M-N Mineral 2 Fraction (Carbonates)
		 - [number] PDCALCFRAC: PEF-DEN Calcite Fraction (Carbonates)
		 - [number] PDDOLOFRAC: PEF-DEN Dolomite Fraction (Carbonates)
		 - [number] PDQRTZFRAC: PEF-DEN Quartz Fraction (Carbonates)
		 - [number] PDMIN1FRAC: : PEF-DEN Mineral 1 Fraction (Carbonates)
		 - [number] rhorefmat: Intermediate outputs
		 - [number] PEFCALCFRAC: PEF Calc Fraction  (Carbonates)
		 - [number] phit85: Gas Porosity (0.85*PHID)
		 - [number] phit21: Gas Porosity (2/3*PHID+1/3*NPHI)
		 - [number] rhobhc: Hydrocarbon Corrected Bulk Density
		 - [number] nphihc: Hydrocarbon Corrected Neutron Porosity
		 - [number] PHITDN: PHITDN. Intermediate output
		 - [number] NPHDRYSL: Neutron Dry Silt
		 - [number] NPHDRYCL: Neutron Dry Clay
		 - [number] RHODRYCL: Densoty Dry Clay
		 - [number] SNDSLTFRAC: Sand-Silt Ratio
		 - [number] CLYSLTFRAC: Clay-Silt Ratio
		 - [number] sandfrac: Sand Fraction
		 - [number] clayfrac: Clay Fraction
		 - [number] mclayln: Intermediate Output
		 - [number] cclayln: Intermediate output
		 - [number] mmatdclln: Intermediate Output
		 - [number] vshdrydn: VSH-Dry from Density-Neutron (Linear)
		 - [number] DNLITH2FRAC: DN Litho-2 Fraction  (Carbonates)
		 - [number] DNDOLOFRAC: DN Dolo Fraction  (Carbonates)
		 - [number] DNCALCFRAC: DN Calc Fraction  (Carbonates)
		 - [number] DNMIN1FRAC: DN Mineral 1 Fraction  (Carbonates)
		 - [number] DNQRTZFRAC
		 - [number] vclinvpor
		 - [number]: rhobfc
		 - [number]: rhobbc
		 - [number]: cwapp
		 - [number]: MXPOINT
		 - [number]: NXPOINT
		 - [number]: shl_n_d: HC Corrected Shale & Sand Line
		 """
	#endregion
	#region initializating Parameters
	VSHGR = MissingValue
	grsndsltfrac = MissingValue
	grclysltfrac = MissingValue
	grclayfrac = MissingValue
	grsandfrac = MissingValue
	grsiltfrac = MissingValue
	peflith2frac = MissingValue
	PEFDOLOFRAC = MissingValue
	PEFQRTZFRAC = MissingValue
	PEFMIN1FRAC = MissingValue
	SALINWAT = MissingValue
	NPHIFLC = MissingValue
	NPHITOOLDL = MissingValue
	NPHITOOLQZ = MissingValue
	PEFFLLM = MissingValue
	PEFFLDL = MissingValue
	PEFFLQZ = MissingValue
	PEFFLMIN1 = MissingValue
	UFL = MissingValue
	mclayln = MissingValue
	cclayln = MissingValue
	NPHDRYCL = MissingValue
	PHITCLY = MissingValue
	NPHICC = MissingValue
	RHOBCC = MissingValue
	PEFCC = MissingValue
	mmatdclln = MissingValue
	cmatdclln = MissingValue
	DNCLAYFRAC = MissingValue
	pdlith2frac = MissingValue
	mncalcfrac = MissingValue
	mndolofrac = MissingValue
	mnqrtzfrac = MissingValue
	mnmin1frac = MissingValue
	mnmin2frac = MissingValue
	PDCALCFRAC = MissingValue
	PDDOLOFRAC = MissingValue
	PDQRTZFRAC = MissingValue
	PDMIN1FRAC = MissingValue
	rhorefmat = MissingValue
	PEFCALCFRAC = MissingValue
	ucc = MissingValue
	phit85 = MissingValue
	phit21 = MissingValue
	phitgm = MissingValue
	rhobhc = MissingValue
	nphihc = MissingValue
	PHITDN = MissingValue
	NPHDRYSL = MissingValue
	NPHDRYCL = MissingValue
	SNDSLTFRAC = MissingValue
	CLYSLTFRAC = MissingValue
	sandfrac = MissingValue
	clayfrac = MissingValue
	siltfrac = MissingValue
	vshdrydn = MissingValue
	DNLITH2FRAC = MissingValue
	DNDOLOFRAC = MissingValue
	DNCALCFRAC = MissingValue
	DNQRTZFRAC = MissingValue
	DNMIN1FRAC = MissingValue
	VMIN2 = MissingValue
	VMIN1 = MissingValue
	VQRTZ = MissingValue
	VDOLO = MissingValue
	VCALC = MissingValue
	VCLD = MissingValue
	VMATRX = MissingValue
	RHOG = MissingValue
	dolofrac = MissingValue
	QRTZFRAC = MissingValue
	VSAND = MissingValue
	VSILT = MissingValue
	VSHALE = MissingValue
	calcfrac = MissingValue
	MIN1FRAC = MissingValue
	MIN2FRAC = MissingValue
	HCK = MissingValue
	cwapp = MissingValue
	MXPOINT = MissingValue
	NXPOINT = MissingValue
	MLIME = MissingValue
	NLIME = MissingValue
	MDOLO = MissingValue
	NDOLO = MissingValue
	MSAND = MissingValue
	NSAND = MissingValue
	NMIN1 = MissingValue
	MMIN1 = MissingValue
	NMIN2 = MissingValue
	MMIN2 = MissingValue
	SXOHC = MissingValue
	rhobbc = MissingValue
	rhobfc = MissingValue
	nonphidrysand = MissingValue
	nonrhodrysand = MissingValue
	cons1 = MissingValue
	cons2 = MissingValue
	cons3 = MissingValue
	cons4 = MissingValue
	#endregion

	if LITHMOD == 'SSC':
		rhobcc = rhob
		nphicc = nphi
		rhorefmat = RHOB_DRY_SAND
		DEGSNDLN, DEGCLYLN, DEGSLTLN, NPHDRYSL, NPHDRYCL, RHODRYCL, PHITCLY, vshdrydn, SNDSLTFRAC, CLYSLTFRAC, sandfrac, clayfrac, siltfrac, cmatdclln, mmatdclln, mclayln, cclayln, csandln, msandln, nonphidrysand, nonrhodrysand, cons1, cons2, cons3, cons4 = SSC_DN_LITHOLOGY(
			DNXPLOTSAND, RHOB_DRY_SAND, RHOB_FLUID, NPHI_DRY_SAND, NPHI_FLUID, ZNRHOBCL, ZNNPHICL, ZNSLTLINRAT, RHODRYSL, rhobhc, nphihc, USE_SILT_ANGLE, DEGFLSLT, NPHI_OFFSET)
		vshgr, grsndsltfrac, grclysltfrac, grclayfrac, grsandfrac, grsiltfrac = SSC_GR_LITHOLOGY(
			GR, ZNGRSD, ZNGRCL, RHODRYCL, RHODRYSL, RHOB_DRY_SAND)
	else:
		SALINWAT, NPHIFLC, NPHITOOLDL, NPHITOOLQZ, PEFFLLM, PEFFLDL, PEFFLQZ, PEFFLMIN1, UFL = CARB_FLUID_PARM(
			NEUTOOL, RHOBFLC)
		
		vshgr, grclayfrac, RHODRYCL, mclayln, cclayln, NPHDRYCL, PHITCLY, nphicc, rhobcc, PEFCC, clayfrac, ucc = CARB_GR_CLAY_CORR(
			LITHTYPE, CLAYFLG, GRCALC, GR, ZNGRCLN, ZNGRCLY, RHOBDRYCLY, ZNRHOWCL, RHOBFLC, ZNNPHWCL, NPHIFLC, nphi, NEUOFFSET, rhob, PEF, PEFOFFSET, PEFDRYCLY)
		
		peflith2frac, PEFCALCFRAC, PEFDOLOFRAC, PEFQRTZFRAC, PEFMIN1FRAC = CARB_PEF_LITHOLOGY(
			LITHTYPE, PEFDRYLM, PEFDRYDL, PEFCC, clayfrac, PEFDRYQZ, PEFDRYMIN1)
		
		pdlith2frac, PDCALCFRAC, PDDOLOFRAC, PDQRTZFRAC, PDMIN1FRAC, rhorefmat = CARB_PD_LITHOLOGY(
			LITHTYPE, RHOBDRYLM, RHOBDRYDL, RHOBDRYQZ, RHOBFLC, RHOBDRYMIN1, PEFDRYLM, PEFDRYDL, PEFFLLM, PEFDRYQZ, rhobcc, PEFCC, clayfrac, PEFFLDL, PEFFLQZ, PEFDRYMIN1, PEFFLMIN1)
		
		mncalcfrac, mndolofrac, mnqrtzfrac, mnmin1frac, mnmin2frac, MXPOINT, NXPOINT, MLIME, NLIME, MDOLO, NDOLO, MSAND, NSAND, NMIN1, MMIN1, NMIN2, MMIN2 = CARB_MN_LITHOLOGY(
			PEFDRYLM, PEFDRYDL, PEFDRYQZ, RHOBDRYLM, RHOBDRYDL, RHOBDRYQZ, PEFDRYMIN1, RHOBDRYMIN1, PEFDRYMIN2, RHOBDRYMIN2, RHOBFLC, UFL, NPHIFLC, NPHIDRYLM, NPHIDRYDL, NPHIDRYQZ, NPHIDRYMIN1, NPHIDRYMIN2, rhobcc, ucc, nphicc, LITHTYPE, clayfrac)

	eq1_hc_inputs = HydrocarbonInputsFirstEquationInputs(RHOB=rhob, NPHI=nphi, X_RHOB=X_RHOB, SHALE_NEUT=SHALE_NEUT, RHOB_FC=RHOB_FC, NPHI_FC=NPHI_FC, sand_madens=sand_madens, fluid_dens=fluid_dens)    
	
	eq3_hc_inputs = HydrocarbonInputsThirdEquationInputs(SAND_LN=SAND_LN, SHALE_LN=SHALE_LN)
	if LITHMOD == "SSC":
		eq4_hc_inputs = HydrocarbonInputsFourthEquationInputs(CSANDLN=csandln, CCLAYLN=cclayln, MSANDLN=msandln, MCLAYLN=mclayln)
		eq2_hc_inputs = HydrocarbonInputsSecondEquationInputs(znhcor=znhcor)
	else:
		if znhcor == -2:
			znhcor = -1
		eq2_hc_inputs = HydrocarbonInputsSecondEquationInputs(znhcor=znhcor)
		eq4_hc_inputs = HydrocarbonInputsFourthEquationInputs(CCLAYLN=cclayln, MCLAYLN=mclayln)
	eq5_hc_inputs = HydrocarbonInputsFifthEquationInputs(RHOB_FLUID=RHOB_FLUID, NPHI_FLUID=NPHI_FLUID, CMATDCLLN=cmatdclln, MMATDCLLN=mmatdclln, RHOB_DRY_SILT=RHODRYSL, RHOB_DRY_CLAY=RHODRYCL,\
														XMINHCORR_RIGHTLIMB=XMINHCORR, XMAXHCORR_RIGHTLIMB=XMAXHCORR, XMINHCORR_LEFTLIMB=XMINHCORR_LEFTLIMB, XMAXHCORR_LEFTLIMB=XMAXHCORR_LEFTLIMB)
	eq6_hc_inputs = HydrocarbonInputsSixthEquationInputs(VSHGR=vshgr, COR_LIMIT_MANUAL=COR_LIMIT_MANUAL)
	
	
	SHI = -0.01
	HCK = 1.0
	ENDPROC = 0
	while ENDPROC != 1:
		ENDPROC = 1
		SHI = SHI + 0.01

		rhobhc, nphihc, phit85, phit21, phitgm, PHITDN, RMF, shl_n_d = HC_CORR_METHOD(
			MFRES, MFTEMP, ZNTEMPUNIT, LITHMOD, rhobcc, nphicc, rhorefmat, rhob, nphi, znrw, zn_m, zn_n, rt, znogf, RHO_OIL, RHO_GAS, HCK, NEUTRONFAC, SHI, COR_METHOD, DEGHCCOR,\
				eq1_hc_inputs, eq2_hc_inputs, eq3_hc_inputs, eq4_hc_inputs, eq5_hc_inputs, eq6_hc_inputs)
		if LITHMOD == 'SSC':
			DEGSNDLN, DEGCLYLN, DEGSLTLN, NPHDRYSL, NPHDRYCL, RHODRYCL, PHITCLY, vshdrydn, SNDSLTFRAC, CLYSLTFRAC, sandfrac, clayfrac, siltfrac, cmatdclln, mmatdclln, mclayln, cclayln, csandln, msandln, nonphidrysand, nonrhodrysand, cons1, cons2, cons3, cons4 = SSC_DN_LITHOLOGY(
				DNXPLOTSAND, RHOB_DRY_SAND, RHOB_FLUID, NPHI_DRY_SAND, NPHI_FLUID, ZNRHOBCL, ZNNPHICL, ZNSLTLINRAT, RHODRYSL, rhobhc, nphihc, USE_SILT_ANGLE, DEGFLSLT, NPHI_OFFSET)
		else:
			mclayln, cclayln, mmatdclln, cmatdclln, rhorefmat, DNCLAYFRAC, clayfrac, calcfrac, vshdrydn, HCK, DNLITH2FRAC, DNDOLOFRAC, DNCALCFRAC, DNQRTZFRAC, DNMIN1FRAC, RHOB_FLUID, NPHI_FLUID, ZNRHOBCL, dolofrac, QRTZFRAC, MIN1FRAC = CARB_DN_LITHOLOGY(
				LITHTYPE, CLAYFLG, RHOBDRYLM, RHOBFLC, NPHIDRYLM, NPHIFLC, RHOBDRYDL, NPHIDRYDL, NPHITOOLDL, RHOBDRYQZ, NPHIDRYQZ, NPHITOOLQZ, RHOBDRYMIN1, NPHIDRYMIN1, ZNRHOWCL, ZNNPHWCL, RHODRYCL, NPHDRYCL, rhobhc, nphihc, clayfrac)
		if SHI == 0:
			VSHDRYDNORG = vshdrydn
			CLAYFRACORG = clayfrac
		if znhcor == -1:
			if HCREF == 'VSHGR':
				if LITHMOD == 'SSC':
					if vshdrydn < limitValue(vshgr, 0, 1):
						ENDPROC = 0
				elif LITHMOD == 'CARB':
					if LITHTYPE == 'CA-[CL]' or LITHTYPE == 'DL-[CL]':
						if vshdrydn < limitValue(vshgr, 0, 1):
							ENDPROC = 0
			elif HCREF == 'PEF':
				if vshdrydn < peflith2frac:
					ENDPROC = 0
			elif HCREF == 'PEF-DEN':
				if vshdrydn < pdlith2frac:
					ENDPROC = 0
			elif HCREF == 'EXTERNAL':
				if vshdrydn < EXT_REF_LOG:
					ENDPROC = 0
			elif HCREF == 'SXOE_(RT)':
				try:
					SXOHC = 1 - (znrw / rt / PHITDN **
								 zn_m) ** ((1 / zn_n) ** 0.2)
				except:
					SXOHC = MissingValue

				SXOHC = limitValue(SXOHC, 0, 1)
				if SHI < SXOHC:
					SHI = SXOHC - 0.01
					ENDPROC = 0
		elif znhcor > 0:
			if LITHMOD == 'SSC':
				if MissingValue not in [rhob, nphi]:
					MLOGORI = (rhob - RHOB_FLUID) / (nphi - NPHI_FLUID)
					CLOGORI = RHOB_FLUID - MLOGORI * NPHI_FLUID
					NPHIXORI = (CLOGORI - cmatdclln) / (mmatdclln - MLOGORI)
					RHOBXORI = MLOGORI * NPHIXORI + CLOGORI
					VSHGAS = znhcor + \
						(1 - znhcor) * (RHOBXORI - rhorefmat) / \
						(RHODRYCL - rhorefmat)
					if vshdrydn < VSHGAS:
						ENDPROC = 0
			elif SHI < znhcor:
				SHI = znhcor - 0.01
				ENDPROC = 0
		if SHI > 1.2:
			ENDPROC = 1
		if VSHDRYDNORG >= 1:
			ENDPROC = 1
		if CLAYFRACORG >= 1:
			ENDPROC = 1

	rhobfc = rhobhc
	synrhobgr = 0
	if LITHMOD == 'SSC':
		if BH_CORR == 'YES':
			rhobfc, rhobbc, clayfrac, siltfrac, sandfrac, synrhobgr, vshdrydn = BH_CORRECTION(
				rhobfc, rhob, BH_CORR, SOURCE_SYN_LOG, dt, nphi, znsynrcl, znsynrsd, vshgr, BHCTYP, grclayfrac, grsiltfrac, grsandfrac, CORR_RHOB_LOG, clayfrac, siltfrac, sandfrac, vshdrydn, EXTRHOBFLG)
		RHOG, phit, VMATRX, VSAND, VSILT, VCLD, VCLB, VCLW, VSHALE, PHIE, VCALC, VDOLO, VQRTZ, VMIN1, VMIN2 = SSC_LITHO_VOLUME(
			sandfrac, RHOB_DRY_SAND, siltfrac, RHODRYSL, clayfrac, RHODRYCL, rhobfc, RHOB_FLUID, PHITCLY)
	else:
		if BH_CORR == 'YES':
			rhobfc, rhobbc, clayfrac, calcfrac, dolofrac, synrhobgr, vshdrydn = BH_CORRECTION(
				rhobfc, rhob, BH_CORR, SOURCE_SYN_LOG, dt, nphi, znsynrcl, znsynrsd, vshgr, BHCTYP, clayfrac, calcfrac, dolofrac, CORR_RHOB_LOG, clayfrac, calcfrac, dolofrac, vshdrydn, EXTRHOBFLG)
			grclayfrac = clayfrac
		nphicc, rhobcc, PEFCC, ucc, calcfrac, dolofrac, QRTZFRAC, MIN1FRAC, MIN2FRAC, RHOG, rhobhc, nphihc, phit, VMATRX, VCLD, VCALC, VDOLO, VQRTZ, VMIN1, VMIN2, PHIE, VCLB, VCLW, PHITCLY, VSILT, VSAND = CARB_LITHO_VOLUME(
			LITHTYPE, LITH2FLG, CLAYFLG, DNCALCFRAC, DNDOLOFRAC, DNQRTZFRAC, DNMIN1FRAC, PDCALCFRAC, PDDOLOFRAC, PDQRTZFRAC, PDMIN1FRAC, PEFCALCFRAC, PEFDOLOFRAC, PEFQRTZFRAC, PEFMIN1FRAC, mncalcfrac, mndolofrac, mnqrtzfrac, mnmin1frac, mnmin2frac, clayfrac, RHODRYCL, calcfrac, RHOBDRYLM, dolofrac, RHOBDRYDL, QRTZFRAC, MIN1FRAC, MIN2FRAC, RHOBDRYQZ, RHOBDRYMIN1, RHOBDRYMIN2, grclayfrac, NPHDRYCL, RHOB_FLUID, PHITCLY, nphicc, rhobcc, PEFCC, ucc, rhobfc, nphihc, ZNRHOBCL, rhobfc)
		if LITHMOD == 'CARB':
			VSAND = VQRTZ
	if SWT_FLAG == 'YES' and BYPASS_LITHO_PORO_CALCULATION == 'YES':
		VSHGR = MissingValue
		grsndsltfrac = MissingValue
		grclysltfrac = MissingValue
		grclayfrac = MissingValue
		grsandfrac = MissingValue
		grsiltfrac = MissingValue
		peflith2frac = MissingValue
		PEFDOLOFRAC = MissingValue
		PEFQRTZFRAC = MissingValue
		PEFMIN1FRAC = MissingValue
		SALINWAT = MissingValue
		NPHIFLC = MissingValue
		NPHITOOLDL = MissingValue
		NPHITOOLQZ = MissingValue
		PEFFLLM = MissingValue
		PEFFLDL = MissingValue
		PEFFLQZ = MissingValue
		PEFFLMIN1 = MissingValue
		UFL = MissingValue
		mclayln = MissingValue
		cclayln = MissingValue
		NPHDRYCL = MissingValue
		PHITCLY = MissingValue
		NPHICC = MissingValue
		RHOBCC = MissingValue
		PEFCC = MissingValue
		mmatdclln = MissingValue
		cmatdclln = MissingValue
		DNCLAYFRAC = MissingValue
		pdlith2frac = MissingValue
		mncalcfrac = MissingValue
		mndolofrac = MissingValue
		mnqrtzfrac = MissingValue
		mnmin1frac = MissingValue
		mnmin2frac = MissingValue
		PDCALCFRAC = MissingValue
		PDDOLOFRAC = MissingValue
		PDQRTZFRAC = MissingValue
		PDMIN1FRAC = MissingValue
		rhorefmat = MissingValue
		PEFCALCFRAC = MissingValue
		ucc = MissingValue
		phit85 = MissingValue
		phit21 = MissingValue
		phitgm = MissingValue
		rhobhc = MissingValue
		nphihc = MissingValue
		PHITDN = MissingValue
		NPHDRYSL = MissingValue
		NPHDRYCL = MissingValue
		SNDSLTFRAC = MissingValue
		CLYSLTFRAC = MissingValue
		sandfrac = MissingValue
		clayfrac = MissingValue
		siltfrac = MissingValue
		vshdrydn = MissingValue
		DNLITH2FRAC = MissingValue
		DNDOLOFRAC = MissingValue
		DNCALCFRAC = MissingValue
		DNQRTZFRAC = MissingValue
		DNMIN1FRAC = MissingValue
		VMIN2 = MissingValue
		VMIN1 = MissingValue
		VQRTZ = MissingValue
		VDOLO = MissingValue
		VCALC = MissingValue
		VCLD = MissingValue
		VCLW = MissingValue
		VCLB = MissingValue
		VSAND = MissingValue
		VSILT = MissingValue
		VSHALE = MissingValue
		VMATRX = MissingValue
		RHOG = MissingValue
		dolofrac = MissingValue
		QRTZFRAC = MissingValue
		calcfrac = MissingValue
		MIN1FRAC = MissingValue
		MIN2FRAC = MissingValue
		HCK = MissingValue
		cwapp = MissingValue
		MXPOINT = MissingValue
		NXPOINT = MissingValue
		MLIME = MissingValue
		NLIME = MissingValue
		MDOLO = MissingValue
		NDOLO = MissingValue
		MSAND = MissingValue
		NSAND = MissingValue
		NMIN1 = MissingValue
		MMIN1 = MissingValue
		NMIN2 = MissingValue
		MMIN2 = MissingValue
		SXOHC = MissingValue
	return (
		vshgr, grsndsltfrac, grclysltfrac, grclayfrac, grsandfrac, grsiltfrac, peflith2frac, PEFCALCFRAC, PEFDOLOFRAC, PEFQRTZFRAC,
		PEFMIN1FRAC, RHOG, phit, VMATRX, VSAND, VSILT, VCLD, VCLB, VCLW, VSHALE,
		nphicc, rhobcc, PEFCC, ucc, calcfrac, dolofrac, QRTZFRAC, MIN1FRAC, MIN2FRAC, VCALC,
		VDOLO, VQRTZ, VMIN1, VMIN2, PHIE, VCLB, VCLW, DNCLAYFRAC, pdlith2frac,
		mncalcfrac, mndolofrac, mnqrtzfrac, mnmin1frac, mnmin2frac, PDCALCFRAC, PDDOLOFRAC, PDQRTZFRAC, PDMIN1FRAC, rhorefmat,
		PEFCALCFRAC, phit85, phit21, rhobhc, nphihc, PHITDN, NPHDRYSL, NPHDRYCL, RHODRYCL, SNDSLTFRAC,
		CLYSLTFRAC, siltfrac, sandfrac, clayfrac, vshdrydn, DNLITH2FRAC, DNDOLOFRAC,
		DNCALCFRAC, DNMIN1FRAC, DNQRTZFRAC, rhobfc, rhobbc, MXPOINT, NXPOINT, synrhobgr, PHITCLY, phitgm,
		MLIME, NLIME, MDOLO, NDOLO, MSAND, NSAND, NMIN1, MMIN1, NMIN2, MMIN2,
		SXOHC, NPHIFLC, NPHITOOLDL, NPHITOOLQZ, PEFFLLM, PEFFLDL, PEFFLQZ, PEFFLMIN1,
		cmatdclln, mmatdclln, mclayln, cclayln, nonphidrysand, nonrhodrysand, cons1, cons2, cons3, cons4, shl_n_d)


def SSC_MAIN_B(SWT_METHOD, PHIT, PHIE, ZN_M, ZN_N, RT, ZNRW, QVFLAG, CALCULATED_MSTAR, ZNCWBGRAD, CLAYFRAC, VSHALE, QV_LOG, zntempunit, znogf, nphihc, rhobfc, COALFL, EXTCOAL, zncoalcut, rhobhc, rhog, CARSTFL, znstrkcut, vsand, vsilt, vcld, vclb, vclw, RHOB_FLUID, COALFLG_LOG, SWT_FLAG, vcalc, EXTSTREAK, vmin1, vmin2, vdolo, LITHMOD, ZNRW77F, BYPASS_LITHO_PORO_CALCULATION, EXT_PHIT_LOG, EXT_PHIE_LOG, EXT_VCLD_LOG, OTHER_EXT_VCLY_LOG, CLAY_VOLUME_FLAG):
	"""Commputes Archie, Waxman, porosities...
		Inputs:
		 1. SWT_METHOD [string]: SW Equation for SSC Model
		 2. PHIT [number]: Total Porosity
		 3. PHIE [number]: Effective Porosity
		 4. ZN_M [number]: Cementation Factor M (M*)
		 5. ZN_N [number]: Saturation Exponent N (N*)
		 6. RT [number]: True Resistivity Log
		 7. ZNRW [number]: Zoned RW at Reservoir Condition
		 8. QVFLAG [string]: Using External Qv Log
		 9. CALCULATED_MSTAR [string]: Using Calculated M* (from M)
		 10. ZNCWBGRAD [number]: Zoned CWB-Gradient at Reservoir Condition
		 11. VCLINVPOR [number]: VCL-PHIT Ratio
		 12. VSHALE [number]: Volume of Shale
		 13. QV_LOG [number]: External Qv Log
		 14. zntempunit [number]: Zoned Reservoir Temperature,  Output of TEMP_SAL_ZONATION
		 15. znogf [number]: Fluid type flag by zone
		 16. nphihc [number]: Neutron Porosity coming from HC_CORR_METHOD
		 17. rhobfc [number]:  Bulk Density coming from BH_CORRECTION
		 18. COALFL [string]: Coal Flaging (coming from parameters)
		 19. zncoalcut [number]: Coal indicator cutoff (coming from parameters)
		 20. rhobhc [number] [g/cc]: Density Hydrocarbon correction, coming from HC_CORR_METHOD
		 21. rhog [number] [g/cc]: Grain density (RHOG input)
		 22. CARSTFL [string]: Carbonate Streaks Flagging [YES/NO]
		 23. znstrkcut [number]: Zoned Lime Streak CUT_OFF Flag (corresponds to ZNSTRKCUT input)
		 24. vsand [number] [v/v]: Sand volume, coming from SSC_LITHO_VOLUME
		 25. vsilt [number]: Sild volume, coming from SSC_LITHO_VOLUME
		 26. vcld [number]: Clay volume, coming from SSC_LITHO_VOLUME
		 27. vclb [number] : Volume of clay bound water, coming from SSC_LITHO_VOLUME
		 28. RHOB_FLUID [number] [g/cc]: RHOB Fluid
		 29. COALFLG_LOG [number]: Interval -- Limestone Streak Flag  (ZO_LMSTREAK)
		 30. SWT_FLAG [string]: Compute Total Water Saturation 'YES/NO' flag
		 31. vcalc [number]: Calcite Volume
		 32. EXTSTREAK [number]
		 33. LITHMOD [string]
		 Output:
		- [number] SWE
		- [number] SWT
		- [number] RWAPP: Apparent RW
		- [number] SWT_ARC: SWT Archie
		- [number] SWE_ARC: SWE Archie
		- [number] SWTU: Unlimited Total Water Saturation
		- [number] CW: Zoned CW at Reservoir Condition
		- [number] BQV: B*Qv of Waxman-Smits
		- [number] ROCAL: Calculated Ro of Waxman-Smits
		- [number] QVSYN: Estimated Qv
		- [number] ZN_M: Cementation Factor M (M*)
		- [number] vcoal: Coal volume (1 or 0)
		- [number] coalind: Coal indicator
		- [number] lmstrkind:
		- [number] vcalc: sum of ssc volumes
		- [number] PHIT: total porosity
		- [number] PHIE: effective porosity
		- [number] vwater: volume of water
		- [number] vsand: volume of sand
		- [number] vsilt: volume of silt
		- [number] vcld: volume of clay
		- [number] vclb: Volume of clay bound water
		- [number] voil: volume of oil
		- [number] vgas: volume of gas
		 """
	SWE_ARC = 1
	SWT_ARC = 1
	SWTU = 1
	vwater = 1
	voil = 0
	vgas = 0
	CW = MissingValue
	BQV = MissingValue
	ROCAL = MissingValue
	QVSYN = MissingValue
	SWE = 1
	SWT = 1
	BMOB = MissingValue
	CWAPP = MissingValue
	RWAPP = MissingValue
	VCLINVPOR = MissingValue
	if SWT_FLAG == 'YES':
		if BYPASS_LITHO_PORO_CALCULATION == 'YES' and PHIT != 0:
			PHIT = EXT_PHIT_LOG
			PHIE = EXT_PHIE_LOG
			vcld = EXT_VCLD_LOG
			CLAYFRAC = vcld / (1 - PHIT)
			if CLAY_VOLUME_FLAG != 'VCLD':
				CLAYFRAC = OTHER_EXT_VCLY_LOG
		if PHIT != MissingValue:
			if PHIT != 0:
				VCLINVPOR = CLAYFRAC / PHIT
				CWAPP = 1 / (PHIT ** ZN_M * RT)
				RWAPP = 1 / CWAPP
			else:
				VCLINVPOR = 0
				CWAPP = 0
		SWT_ARC, SWE_ARC, SWTU = ARCHIE_EQU(
			SWT_METHOD, PHIT, PHIE, ZN_M, ZN_N, RT, ZNRW)
		SWT = SWT_ARC
		SWE = SWE_ARC
		if SWT_METHOD == 'WAXMAN_SMITS':
			CW, BQV, SWTU, ROCAL, QVSYN, ZN_M, BMOB = WAXMAN_EQU(
				SWT_METHOD, QVFLAG, CALCULATED_MSTAR, ZNRW, RT, ZNCWBGRAD, VCLINVPOR, ZN_M, ZN_N, PHIT, VSHALE, vcld, QV_LOG, zntempunit, ZNRW77F)
			SWT = SWTU
			if PHIE > 0:
				SWE = 1 - (1 - SWT) * PHIT / PHIE
			else:
				SWE = 1
			SWT = limitValue(SWT, 0, 1)
			SWE = limitValue(SWE, 0, 1)
		vwater = PHIE * SWE
		if znogf == 2:
			vgas = 0
			voil = PHIE - vwater
		elif znogf == 1:
			vgas = PHIE - vwater
			voil = 0
		elif znogf == 0:
			SWT = 1
			SWE = 1
			SWT_ARC = 1
			SWE_ARC = 1
			vwater = PHIE
			vgas = 0
			voil = 0
		if PHIT == MissingValue:
			SWTU = MissingValue
			SWT = MissingValue
			SWE = MissingValue
			SWT_ARC = MissingValue
			SWE_ARC = MissingValue
			vwater = MissingValue
			vgas = MissingValue
			voil = MissingValue
		if BYPASS_LITHO_PORO_CALCULATION == 'YES':
			PHIT = MissingValue
			PHIE = MissingValue
			vcld = MissingValue
			CLAYFRAC = MissingValue
	coalind, vcoal, vclw, vcld, vclb, vsilt, vsand, vcalc, vdolo, vmin1, vmin2, vgas, voil, vwater, PHIT, PHIE, VSHALE, SWTU, SWT, SWE, SWT_ARC, SWE_ARC = COAL_FLAGGING(
		nphihc, rhobfc, COALFL, EXTCOAL, zncoalcut, vclw, vcld, vclb, vsilt, vsand, vcalc, vdolo, vmin1, vmin2, vgas, voil, vwater, PHIT, PHIE, VSHALE, SWTU, SWT, SWE, SWT_ARC, SWE_ARC)
	return (
		SWE, SWT, RWAPP, SWT_ARC, SWE_ARC, SWTU, CW, BQV, ROCAL, QVSYN, ZN_M, ZN_N, vcoal, coalind, vcalc, PHIT, PHIE, vwater, vsand,
		vsilt, vcld, vclb, vclw, voil, vgas, vmin1, vmin2, vdolo, BMOB, VCLINVPOR, CWAPP, VSHALE)


def CARB_MN_LITHOLOGY(PEFDRYLM, PEFDRYDL, PEFDRYQZ, RHOBDRYLM, RHOBDRYDL, RHOBDRYQZ, PEFDRYMIN1, RHOBDRYMIN1, PEFDRYMIN2, RHOBDRYMIN2, RHOBFLC, UFL, NPHIFLC, NPHIDRYLM, NPHIDRYDL, NPHIDRYQZ, NPHIDRYMIN1, NPHIDRYMIN2, rhobcc, ucc, nphicc, LITHTYPE, clayfrac):
	"""Lithology computation
		Inputs:
		1. PEFDRYLM [number]: PEF Calcite
		2. PEFDRYDL [number]: PEF Dolomite
		3. PEFDRYQZ [number]: PEF Quartz
		4. RHOBDRYLM [number]: RHOB Calcite
		5. RHOBDRYDL [number]: RHOB Dolomite
		6. RHOBDRYQZ [number]: RHOB Quartz
		7. PEFDRYMIN1 [number]: PEF Mineral 1
		8. RHOBDRYMIN1 [number]: RHOB Mineral 1
		9. PEFDRYMIN2 [number]: PEF Mineral 2
		10. RHOBDRYMIN2 [number]: RHOB Mineral 2
		11. RHOBFLC [number]: Fluid Density
		12. UFL [number]: Fluid Parameters for for M-N Plot (coming from CARB_FLUID_PARM)
		13. NPHIFLC [number]: Fluid Parameters for Neutron
		14. NPHIDRYLM [number]: Calcite Neutron Porosity
		15. NPHIDRYDL [number]: Dolomite Neutron Porosity
		16. NPHIDRYQZ [number]: Quartz Neutron Porosity
		17. NPHIDRYMIN1 [number]: Mineral1 Neutron Porosity
		18. NPHIDRYMIN2 [number]: Mineral2 Neutron Porosity
		19. rhobcc [number] [g/cc]: RHOB Clay Corrected (Carbonates), coming from CARB_GR_CLAY_CORR
		20. ucc [number]: U Clay Corrected (Carbonates), coming from CARB_GR_CLAY_CORR
		21. NPHICC [number]: NPHI Clay Corrected (Carbonates), coming from CARB_GR_CLAY_CORR
		22. LITHTYPE [string]: Lithology Components
		23. clayfrac [number]: 
		Output:
		- MNCALCFRAC [number]: M-N Calc Fraction  (Carbonates)
		- MNDOLOFRAC [number]: M-N Dolo Fraction  (Carbonates)
		- MNQRTZFRAC [number]: M-N Qrtz Fraction  (Carbonates)
		- MNMIN1FRAC [number]: M-N Min1 Fraction  (Carbonates)
		- MNMIN2FRAC [number]: M-N Min2 Fraction  (Carbonates)
		- MXPOINT [number]
		- NXPOINT [number]
		"""
	mncalcfrac = MissingValue
	mndolofrac = MissingValue
	mnqrtzfrac = MissingValue
	mnmin1frac = MissingValue
	mnmin2frac = MissingValue
	zn_mpoint = MissingValue
	mxpoint = MissingValue
	nxpoint = MissingValue
	MLIME = MissingValue
	NLIME = MissingValue
	MDOLO = MissingValue
	NDOLO = MissingValue
	MSAND = MissingValue
	NSAND = MissingValue
	NMIN1 = MissingValue
	MMIN1 = MissingValue
	NMIN2 = MissingValue
	MMIN2 = MissingValue
	CMIN2LIME = MissingValue
	MMIN2LIME = MissingValue
	CMIN1MIN2 = MissingValue
	MMIN1MIN2 = MissingValue
	CLIMEMIN1 = MissingValue
	MLIMEMIN1 = MissingValue
	CSANDLIME = MissingValue
	MSANDLIME = MissingValue
	MDOLOSAND = MissingValue
	CDOLOSAND = MissingValue
	CLIMEDOLO = MissingValue
	MLIMEDOLO = MissingValue
	UDRYLM = RHOBDRYLM * PEFDRYLM
	UDRYDL = RHOBDRYDL * PEFDRYDL
	UDRYQZ = RHOBDRYQZ * PEFDRYQZ
	UDRYMIN1 = RHOBDRYMIN1 * PEFDRYMIN1
	UDRYMIN2 = RHOBDRYMIN2 * PEFDRYMIN2
	if RHOBDRYLM - RHOBFLC != 0:
		MLIME = (UDRYLM - UFL) / (RHOBDRYLM - RHOBFLC)
	if RHOBDRYLM - RHOBFLC != 0:
		NLIME = (NPHIFLC - NPHIDRYLM) / (RHOBDRYLM - RHOBFLC)
	if RHOBDRYDL - RHOBFLC != 0:
		MDOLO = (UDRYDL - UFL) / (RHOBDRYDL - RHOBFLC)
	if RHOBDRYDL - RHOBFLC != 0:
		NDOLO = (NPHIFLC - NPHIDRYDL) / (RHOBDRYDL - RHOBFLC)
	if RHOBDRYQZ - RHOBFLC != 0:
		MSAND = (UDRYQZ - UFL) / (RHOBDRYQZ - RHOBFLC)
	if RHOBDRYQZ - RHOBFLC != 0:
		NSAND = (NPHIFLC - NPHIDRYQZ) / (RHOBDRYQZ - RHOBFLC)
	if RHOBDRYMIN1 - RHOBFLC != 0:
		MMIN1 = (UDRYMIN1 - UFL) / (RHOBDRYMIN1 - RHOBFLC)
	if RHOBDRYMIN1 - RHOBFLC != 0:
		NMIN1 = (NPHIFLC - NPHIDRYMIN1) / (RHOBDRYMIN1 - RHOBFLC)
	if RHOBDRYMIN2 - RHOBFLC != 0:
		MMIN2 = (UDRYMIN2 - UFL) / (RHOBDRYMIN2 - RHOBFLC)
	if RHOBDRYMIN2 - RHOBFLC != 0:
		NMIN2 = (NPHIFLC - NPHIDRYMIN2) / (RHOBDRYMIN2 - RHOBFLC)
	if NLIME - NDOLO != 0:
		MLIMEDOLO = (MLIME - MDOLO) / (NLIME - NDOLO)
		CLIMEDOLO = MLIME - MLIMEDOLO * NLIME
	if NDOLO - NSAND != 0:
		MDOLOSAND = (MDOLO - MSAND) / (NDOLO - NSAND)
		CDOLOSAND = MDOLO - MDOLOSAND * NDOLO
	if NSAND - NLIME != 0:
		MSANDLIME = (MSAND - MLIME) / (NSAND - NLIME)
		CSANDLIME = MSAND - MSANDLIME * NSAND
	if NLIME - NMIN1 != 0:
		MLIMEMIN1 = (MLIME - MMIN1) / (NLIME - NMIN1)
		CLIMEMIN1 = MLIME - MLIMEMIN1 * NLIME
	if NMIN1 - NMIN2 != 0:
		MMIN1MIN2 = (MMIN1 - MMIN2) / (NMIN1 - NMIN2)
		CMIN1MIN2 = MMIN1 - MMIN1MIN2 * NMIN1
	if NMIN2 - NLIME != 0:
		MMIN2LIME = (MMIN2 - MLIME) / (NMIN2 - NLIME)
		CMIN2LIME = MMIN2 - MMIN2LIME * NMIN2
	if rhobcc > RHOBFLC:
		mxpoint = (ucc - UFL) / (rhobcc - RHOBFLC)
		nxpoint = (NPHIFLC - nphicc) / (rhobcc - RHOBFLC)
		if nxpoint == NLIME or nxpoint == NDOLO or nxpoint == NSAND or nxpoint == NMIN1 or nxpoint == NMIN2:
			nxpoint = nxpoint + 0.001
		if LITHTYPE == 'CA-DL-QZ-[CL]':
			if MissingValue not in [PEFDRYLM, RHOBDRYLM, NPHIDRYLM, PEFDRYDL, RHOBDRYDL, NPHIDRYDL, PEFDRYQZ, RHOBDRYQZ, NPHIDRYQZ, MLIME, MDOLO, NLIME, NDOLO, MSANDLIME, MDOLOSAND, CDOLOSAND, NSAND, MSAND, MLIMEDOLO, CLIMEDOLO]:
				MXLIMEP = (mxpoint - MLIME) / (nxpoint - NLIME)
				CXLIMEP = MLIME - MXLIMEP * NLIME
				MXDOLOP = (mxpoint - MDOLO) / (nxpoint - NDOLO)
				CXDOLOP = MDOLO - MXDOLOP * NDOLO
				MXSANDP = (mxpoint - MSAND) / (nxpoint - NSAND)
				CXSANDP = MSAND - MXSANDP * NSAND
				NLIMEP = (CDOLOSAND - CXLIMEP) / (MXLIMEP - MDOLOSAND)
				MLIMEP = MXLIMEP * NLIMEP + CXLIMEP
				NDOLOP = (CSANDLIME - CXDOLOP) / (MXDOLOP - MSANDLIME)
				MDOLOP = MXDOLOP * NDOLOP + CXDOLOP
				NSANDP = (CLIMEDOLO - CXSANDP) / (MXSANDP - MLIMEDOLO)
				MSANDP = MXSANDP * NSANDP + CXSANDP
				mncalcfrac = (mxpoint - MLIMEP) / (MLIME - MLIMEP)
				mndolofrac = (mxpoint - MDOLOP) / (MDOLO - MDOLOP)
				mnqrtzfrac = (mxpoint - MSANDP) / (MSAND - MSANDP)
				if mncalcfrac < 0:
					mndolofrac = mndolofrac / (mndolofrac + mnqrtzfrac)
					mnqrtzfrac = 1 - mndolofrac
					mncalcfrac = 0
					mnmin1frac = 0
					mnmin2frac = 0
				elif mndolofrac < 0:
					mnqrtzfrac = mnqrtzfrac / (mnqrtzfrac + mncalcfrac)
					mncalcfrac = 1 - mnqrtzfrac
					mndolofrac = 0
					mnmin1frac = 0
					mnmin2frac = 0
				elif mnqrtzfrac < 0:
					mncalcfrac = mncalcfrac / (mncalcfrac + mndolofrac)
					mndolofrac = 1 - mncalcfrac
					mnqrtzfrac = 0
					mnmin1frac = 0
					mnmin2frac = 0
		elif LITHTYPE == 'CA-M1-M2-[CL]':
			if MissingValue not in [PEFDRYLM, RHOBDRYLM, NPHIDRYLM, PEFDRYMIN1, RHOBDRYMIN1, NPHIDRYMIN1, PEFDRYMIN2, RHOBDRYMIN2, NPHIDRYMIN2, NLIME, NMIN1, NMIN2, MMIN2, MLIME, MMIN1, MMIN2LIME, MMIN1MIN2, MLIMEMIN1]:
				MXLIMEP = (mxpoint - MLIME) / (nxpoint - NLIME)
				CXLIMEP = MLIME - MXLIMEP * NLIME
				MXMIN1P = (mxpoint - MMIN1) / (nxpoint - NMIN1)
				CXMIN1P = MMIN1 - MXMIN1P * NMIN1
				MXMIN2P = (mxpoint - MMIN2) / (nxpoint - NMIN2)
				CXMIN2P = MMIN2 - MXMIN2P * NMIN2
				NLIMEP = (CMIN1MIN2 - CXLIMEP) / (MXLIMEP - MMIN1MIN2)
				MLIMEP = MXLIMEP * NLIMEP + CXLIMEP
				NMIN1P = (CMIN2LIME - CXMIN1P) / (MXMIN1P - MMIN2LIME)
				MMIN1P = MXMIN1P * NMIN1P + CXMIN1P
				NMIN2P = (CLIMEMIN1 - CXMIN2P) / (MXMIN2P - MLIMEMIN1)
				MMIN2P = MXMIN2P * NMIN2P + CXMIN2P
				mncalcfrac = (mxpoint - MLIMEP) / (MLIME - MLIMEP)
				mnmin1frac = (mxpoint - MMIN1P) / (MMIN1 - MMIN1P)
				mnmin2frac = (mxpoint - MMIN2P) / (MMIN2 - MMIN2P)
				if mncalcfrac < 0:
					mnmin1frac = mnmin1frac / (mnmin1frac + mnmin2frac)
					mnmin2frac = 1 - mnmin1frac
					mncalcfrac = 0
					mndolofrac = 0
					mnqrtzfrac = 0
				elif mnmin1frac < 0:
					mnmin2frac = mnmin2frac / (mnmin2frac + mncalcfrac)
					mncalcfrac = 1 - mnmin2frac
					mnmin1frac = 0
					mndolofrac = 0
					mnqrtzfrac = 0
				elif mnmin2frac < 0:
					mncalcfrac = mncalcfrac / (mncalcfrac + mnmin1frac)
					mnmin1frac = 1 - mncalcfrac
					mnmin2frac = 0
					mndolofrac = 0
					mnqrtzfrac = 0
		if mncalcfrac != MissingValue:
			mncalcfrac = (1 - clayfrac) * limitValue(mncalcfrac, 0, 1)
		if mndolofrac != MissingValue:
			mndolofrac = (1 - clayfrac) * limitValue(mndolofrac, 0, 1)
		if mnqrtzfrac != MissingValue:
			mnqrtzfrac = (1 - clayfrac) * limitValue(mnqrtzfrac, 0, 1)
		if mnmin1frac != MissingValue:
			mnmin1frac = (1 - clayfrac) * limitValue(mnmin1frac, 0, 1)
		if mnmin2frac != MissingValue:
			mnmin2frac = (1 - clayfrac) * limitValue(mnmin2frac, 0, 1)
	return (
		mncalcfrac, mndolofrac, mnqrtzfrac, mnmin1frac, mnmin2frac, mxpoint, nxpoint, MLIME, NLIME, MDOLO, NDOLO, MSAND, NSAND, NMIN1, MMIN1, NMIN2, MMIN2)


def CARB_PEF_LITHOLOGY(LITHTYPE, PEFDRYLM, PEFDRYDL, PEFCC, CLAYFRAC, PEFDRYQZ, PEFDRYMIN1):
	"""Calculate LITHO2FRAC from PEF
		Inputs:
		 1. LITHTYPE [string]: Lithology Components
		 2. PEFDRYLM [number]: PEF Calcite
		 3. PEFDRYDL [number]: PEF Dolomite
		 4. PEFCC [number]: PEF Clay Corrected (Carbonates)
		 5. CLAYFRAC [number]: Clay Fraction
		 6. PEFDRYQZ [number]: PEF Quartz
		 7. PEFDRYMIN1 [number]: PEF Mineral 1
		Outputs:
		 - [number] PEFLITH2FRAC PEF Litho-2 Fraction
		 - [number] PEFCALCFRAC PEF Calc Fraction
		 - [number] PEFDOLOFRAC PEF Dolo Fraction
		 - [number] PEFQRTZFRAC PEF Qrtz Fraction
		 - [number] PEFMIN1FRAC PEF Min1 Fraction
		"""
	PEFLITH2FRAC = MissingValue
	PEFDOLOFRAC = MissingValue
	PEFQRTZFRAC = MissingValue
	PEFMIN1FRAC = MissingValue
	PEFCALCFRAC = MissingValue
	try:
		if LITHTYPE == 'CA-DL-[CL]':
			PEFLITH2FRAC = (PEFDRYLM - PEFCC) / (PEFDRYLM - PEFDRYDL)
			PEFLITH2FRAC = limitValue(PEFLITH2FRAC, 0, 1)
			PEFCALCFRAC = 1 - PEFLITH2FRAC
			PEFDOLOFRAC = PEFLITH2FRAC
			PEFQRTZFRAC = 0
			PEFMIN1FRAC = 0
		elif LITHTYPE == 'CA-QZ-[CL]':
			PEFLITH2FRAC = (PEFDRYLM - PEFCC) / (PEFDRYLM - PEFDRYQZ)
			PEFLITH2FRAC = limitValue(PEFLITH2FRAC, 0, 1)
			PEFCALCFRAC = 1 - PEFLITH2FRAC
			PEFDOLOFRAC = 0
			PEFQRTZFRAC = PEFLITH2FRAC
			PEFMIN1FRAC = 0
		elif LITHTYPE == 'CA-M1-[CL]':
			PEFLITH2FRAC = (PEFDRYLM - PEFCC) / (PEFDRYLM - PEFDRYMIN1)
			PEFLITH2FRAC = limitValue(PEFLITH2FRAC, 0, 1)
			PEFCALCFRAC = 1 - PEFLITH2FRAC
			PEFDOLOFRAC = 0
			PEFQRTZFRAC = 0
			PEFMIN1FRAC = PEFLITH2FRAC
		else:
			return (
				MissingValue, MissingValue, MissingValue, MissingValue, MissingValue)
		PEFCALCFRAC = PEFCALCFRAC * (1 - CLAYFRAC)
		PEFDOLOFRAC = PEFDOLOFRAC * (1 - CLAYFRAC)
		PEFQRTZFRAC = PEFQRTZFRAC * (1 - CLAYFRAC)
		PEFMIN1FRAC = PEFMIN1FRAC * (1 - CLAYFRAC)
		return (
			PEFLITH2FRAC, PEFCALCFRAC, PEFDOLOFRAC, PEFQRTZFRAC, PEFMIN1FRAC)
	except:
		return (
			MissingValue, MissingValue, MissingValue, MissingValue, MissingValue)


def CARB_PD_LITHOLOGY(LITHTYPE, RHOBDRYLM, RHOBDRYDL, RHOBDRYQZ, RHOBFLC, RHOBDRYMIN1, PEFDRYLM, PEFDRYDL, PEFFLLM, PEFDRYQZ, RHOBCC, PEFCC, CLAYFRAC, PEFFLDL=2.6, PEFFLQZ=1.7, PEFDRYMIN1=1.1, PEFFLMIN1=1):
	"""Calculate LITHO2FRAC from PEF-DEN X-Plot
		Inputs:
		 1. LITHTYPE [string]: Lithology Components
		 2. RHOBDRYLM [number]: RHOB Calcite
		 3. RHOBDRYDL [number]: RHOB Dolomite
		 4. RHOBDRYQZ [number]: RHOB Quartz
		 5. RHOBFLC [number]: Fluid Density
		 6. RHOBDRYMIN1 [number]: RHOB Mineral-1
		 7. PEFDRYLM [number]: PEF Calcite
		 8. PEFDRYDL [number]: PEF Dolomite
		 9. PEFDRYQZ [number]: PEF Quartz
		 10. PEFDRYMIN1 [number]: PEF Mineral-1
		 11. RHOBCC [number]: RHOB Clay Corrected (Carbonates)
		 12. PEFCC [number]: PEF Clay Corrected (Carbonates)
		 13. CLAYFRAC [number]: Clay Fraction
		 14. PEFFLLM [number][=2.6]: Fluid Parameters for PEF
		 15. PEFFLDL [number][=1.7]: Fluid Parameters for PEF
		 16. PEFFLQZ [number][=1.1]: Fluid Parameters for PEF
		 17. PEFFLMIN1 [number][=1]: Fluid Parameters for PEF
		Outputs:
		 - [number] PEF-DEN Litho-2 Fraction  (Carbonates)
		 - [number] PDCALCFRAC PEF-DEN Calc Fraction  (Carbonates)
		 - [number] PEF-DEN Dolo Fraction  (Carbonates)
		 - [number] PEF-DEN Qrtz Fraction  (Carbonates)
		 - [number] PEF-DEN Min1 Fraction  (Carbonates)
		 - [number] rhorefmat
		"""
	PDLITH2FRAC = MissingValue
	PDCALCFRAC = MissingValue
	PDDOLOFRAC = MissingValue
	PDQRTZFRAC = MissingValue
	PDMIN1FRAC = MissingValue
	rhorefmat = MissingValue
	rhorefmat = RHOBDRYLM
	try:
		mcalcln = (RHOBDRYLM - RHOBFLC) / (PEFDRYLM - PEFFLLM)
		ccalcln = RHOBDRYLM - mcalcln * PEFDRYLM
		mdololn = (RHOBDRYDL - RHOBFLC) / (PEFDRYDL - PEFFLDL)
		cdololn = RHOBDRYDL - mdololn * PEFDRYDL
		mqrtzln = (RHOBDRYQZ - RHOBFLC) / (PEFDRYQZ - PEFFLQZ)
		cqrtzln = RHOBDRYQZ - mqrtzln * PEFDRYQZ
		mmin1ln = (RHOBDRYMIN1 - RHOBFLC) / (PEFDRYMIN1 - PEFFLMIN1)
		cmin1ln = RHOBDRYMIN1 - mmin1ln * PEFDRYMIN1
		if LITHTYPE == 'CA-DL-[CL]':
			mmatdclln = (RHOBDRYDL - RHOBDRYLM) / (PEFDRYDL - PEFDRYLM)
			cmatdclln = RHOBDRYLM - mmatdclln * PEFDRYLM
			rhorefmat = RHOBDRYLM
		elif LITHTYPE == 'CA-QZ-[CL]':
			mmatdclln = (RHOBDRYQZ - RHOBDRYLM) / (PEFDRYQZ - PEFDRYLM)
			cmatdclln = RHOBDRYLM - mmatdclln * PEFDRYLM
			rhorefmat = RHOBDRYLM
		elif LITHTYPE == 'CA-M1-[CL]':
			mmatdclln = (RHOBDRYMIN1 - RHOBDRYLM) / (PEFDRYMIN1 - PEFDRYLM)
			cmatdclln = RHOBDRYLM - mmatdclln * PEFDRYLM
			rhorefmat = RHOBDRYLM
		else:
			return (
				PDLITH2FRAC, PDCALCFRAC, PDDOLOFRAC, PDQRTZFRAC, PDMIN1FRAC, rhorefmat)
		if LITHTYPE == 'CA-DL-[CL]':
			xcmatdclln = RHOBCC - mmatdclln * PEFCC
			pefx1 = (ccalcln - xcmatdclln) / (mmatdclln - mcalcln)
			rhobx1 = mmatdclln * pefx1 + xcmatdclln
			pefx2 = (cdololn - xcmatdclln) / (mmatdclln - mdololn)
			rhobx2 = mmatdclln * pefx2 + xcmatdclln
			PDLITH2FRAC = (RHOBCC - rhobx1) / (rhobx2 - rhobx1)
			PDLITH2FRAC = limitValue(PDLITH2FRAC, 0, 1)
			PDCALCFRAC = 1 - PDLITH2FRAC
			PDDOLOFRAC = PDLITH2FRAC
			PDQRTZFRAC = 0
			PDMIN1FRAC = 0
		elif LITHTYPE == 'CA-QZ-[CL]':
			xcmatdclln = RHOBCC - mmatdclln * PEFCC
			pefx1 = (cqrtzln - xcmatdclln) / (mmatdclln - mqrtzln)
			rhobx1 = mmatdclln * pefx1 + xcmatdclln
			pefx2 = (ccalcln - xcmatdclln) / (mmatdclln - mcalcln)
			rhobx2 = mmatdclln * pefx2 + xcmatdclln
			PDLITH2FRAC = (RHOBCC - rhobx1) / (rhobx2 - rhobx1)
			PDLITH2FRAC = limitValue(PDLITH2FRAC, 0, 1)
			PDCALCFRAC = PDLITH2FRAC
			PDDOLOFRAC = 0
			PDQRTZFRAC = 1 - PDLITH2FRAC
			PDMIN1FRAC = 0
		elif LITHTYPE == 'CA-M1-[CL]':
			xcmatdclln = RHOBCC - mmatdclln * PEFCC
			pefx1 = (cmin1ln - xcmatdclln) / (mmatdclln - mmin1ln)
			rhobx1 = mmatdclln * pefx1 + xcmatdclln
			pefx2 = (ccalcln - xcmatdclln) / (mmatdclln - mcalcln)
			rhobx2 = mmatdclln * pefx2 + xcmatdclln
			PDLITH2FRAC = (RHOBCC - rhobx1) / (rhobx2 - rhobx1)
			PDLITH2FRAC = limitValue(PDLITH2FRAC, 0, 1)
			PDCALCFRAC = PDLITH2FRAC
			PDDOLOFRAC = 0
			PDQRTZFRAC = 0
			PDMIN1FRAC = 1 - PDLITH2FRAC
		PDCALCFRAC = PDCALCFRAC * (1 - CLAYFRAC)
		PDDOLOFRAC = PDDOLOFRAC * (1 - CLAYFRAC)
		PDQRTZFRAC = PDQRTZFRAC * (1 - CLAYFRAC)
		PDMIN1FRAC = PDMIN1FRAC * (1 - CLAYFRAC)
		return (
			PDLITH2FRAC, PDCALCFRAC, PDDOLOFRAC, PDQRTZFRAC, PDMIN1FRAC, rhorefmat)
	except:
		return (
			PDLITH2FRAC, PDCALCFRAC, PDDOLOFRAC, PDQRTZFRAC, PDMIN1FRAC, rhorefmat)


def CARB_FLUID_PARM(NEUTOOL, RHOBFLC):
	"""Carbonate Fluid Parameters Setp-Up
		Inputs:
		 1. NEUTOOL [string]: Neutron Tool Type
		 2. RHOBFLC [number]: Fluid Density
		Outputs:
		 - [number] SALINWAT: Fluid Parameters for Density
		 - [number] NPHIFLC: Fluid Parameters for Neutron
		 - [number] NPHITOOLDL: Fluid Parameters for Neutron
		 - [number] NPHITOOLQZ: Fluid Parameters for Neutron
		 - [number] PEFFLLM: Fluid Parameters for PEF
		 - [number] PEFFLDL: Fluid Parameters for PEF
		 - [number] PEFFLQZ: Fluid Parameters for PEF
		 - [number] PEFFLMIN1: Fluid Parameters for PEF
		 - [number] UFL: Fluid Parameters for for M-N Plot
		"""
	SALINWAT = (RHOBFLC - 1) / 0.73 * 1000000
	NPHIFLC = 1
	NPHITOOLDL = MissingValue
	NPHITOOLQZ = MissingValue
	if NEUTOOL == 'SLB-CNL':
		NPHITOOLDL = 1.15 + 0.1 * (SALINWAT / 250000)
		NPHITOOLQZ = 0.85
	elif NEUTOOL == 'SLB-ADN675':
		NPHITOOLDL = 1.1
		NPHITOOLQZ = 0.93
	elif NEUTOOL == 'SLB-APLC':
		NPHITOOLDL = 1.0
		NPHITOOLQZ = 0.93
	elif NEUTOOL == 'BA-2435CN':
		NPHITOOLDL = 1.17 + 0.1 * (SALINWAT / 250000)
		NPHITOOLQZ = 0.85
	PEFFLLM = 2.6
	PEFFLDL = 1.7
	PEFFLQZ = 1.1
	PEFFLMIN1 = 1
	UFL = 0.4 + 0.96 * (SALINWAT / 200000)
	return (
		SALINWAT, NPHIFLC, NPHITOOLDL, NPHITOOLQZ, PEFFLLM, PEFFLDL, PEFFLQZ, PEFFLMIN1, UFL)


def CARB_GR_CLAY_CORR(LITHTYPE, CLAYFLG, GRCALC, GR, ZNGRCLN, ZNGRCLY, RHOBDRYCLY, ZNRHOWCL, RHOBFLC, ZNNPHWCL, NPHIFLC, NPHI, NEUOFFSET, RHOB, PEF, PEFOFFSET, PEFDRYCLY):
	"""Calculate VCLGR and Clay Correction
		Inputs:
		 1. LITHTYPE [string]: Lithology Components
		 2. CLAYFLG [string]: Model With Clay
		 3. GRCALC [string]: Type of VCL_GR Equation
		 4. GR [number]: Gamma Ray log
		 5. ZNGRCLN [number]: Zoned Gamma Ray Clean (Carbonates)
		 6. ZNGRCLY [number]: Zoned Gamma Ray Clay (Carbonates)
		 7. RHOBDRYCLY [number]: RHOB Dry Clay
		 8. ZNRHOWCL [number]: Zoned RHOB Clay (Carbonates)
		 9. RHOBFLC [number]: Fluid Density
		 10. ZNNPHWCL [number]: Zoned NPHI Clay (Carbonates)
		 11. NPHIFLC [number]: NPHIFLC
		 12. NPHI [number]: Neutron Porosity Log
		 13. NEUOFFSET [number]: Offset for NPHI Log
		 14. RHOB [number]: Bulk Density Log
		 15. PEF [number]: Photo Electric Log
		 16. PEFOFFSET [number]: Offset for PEF Log
		 17. PEFDRYCLY [number]: PEF Dry Clay
		Outputs:
		 - [number] VSHGR: VSH Gamma Ray
		 - [number] GRCLAYFRAC: GR Clay Fraction
		 - [number] RHODRYCL: Density Dry Clay
		 - [number] mclayln: WetClay Angle 
		 - [number] cclayln: WetClay Angle 
		 - [number] NPHDRYCL: Neutron Dry Clay
		 - [number] PHITCLY: PHITCLY
		 - [number] NPHICC: NPHI Clay Corrected (Carbonates)
		 - [number] RHOBCC: RHOB Clay Corrected (Carbonates)
		 - [number] PEFCC: PEF Clay Corrected (Carbonates)
		 - [number] CLAYFRAC: Clay Fraction
		 - [number] UCC: U Clay Corrected (Carbonates)
		"""
	GRCLAYFRAC = MissingValue
	VSHGR = MissingValue
	if MissingValue not in [GR, ZNGRCLN, ZNGRCLN]:
		try:
			GRCLAYFRAC = (GR - ZNGRCLN) / (ZNGRCLY - ZNGRCLN)
			if GRCALC == 'NON-LINEAR':
				GRCLAYFRAC = 0.083 * (2 ** (3.7 * GRCLAYFRAC) - 1)
			GRCLAYFRAC = limitValue(GRCLAYFRAC, 0, 1)
			VSHGR = GRCLAYFRAC
		except:
			pass

	if CLAYFLG == 'NO':
		GRCLAYFRAC = 0
		VSHGR = 0
	RHODRYCL = RHOBDRYCLY
	NPHDRYCL = MissingValue
	PHITCLY = MissingValue
	mclayln = MissingValue
	cclayln = MissingValue
	if MissingValue not in [ZNRHOWCL, RHOBFLC, ZNNPHWCL, NPHIFLC]:
		try:
			mclayln = (ZNRHOWCL - RHOBFLC) / (ZNNPHWCL - NPHIFLC)
			cclayln = RHOBFLC - mclayln * NPHIFLC
			NPHDRYCL = (RHODRYCL - cclayln) / mclayln
			PHITCLY = (RHODRYCL - ZNRHOWCL) / (RHODRYCL - RHOBFLC)
		except:
			pass

	NPHICC = MissingValue
	RHOBCC = MissingValue
	PEFCC = MissingValue
	UCC = MissingValue
	CLAYFRAC = 0
	if MissingValue not in [NPHI, NEUOFFSET]:
		NPHICC = NPHI + NEUOFFSET
	if MissingValue not in [RHOB]:
		RHOBCC = RHOB
	if MissingValue not in [PEF, PEFOFFSET]:
		PEFCC = PEF + PEFOFFSET
	if MissingValue not in [PEFCC, RHOBCC]:
		UCC = PEFCC * RHOBCC
	CLAYFRAC = 0
	if LITHTYPE != 'CA-[CL]' and LITHTYPE != 'DL-[CL]':
		if CLAYFLG == 'YES':
			if MissingValue not in [NPHICC, GRCLAYFRAC, NPHDRYCL]:
				NPHICC = (NPHICC - GRCLAYFRAC * NPHDRYCL) / (1.01 - GRCLAYFRAC)
			if MissingValue not in [RHOB, GRCLAYFRAC, RHODRYCL]:
				RHOBCC = (RHOB - GRCLAYFRAC * RHODRYCL) / (1.01 - GRCLAYFRAC)
			if MissingValue not in [PEFCC, GRCLAYFRAC, PEFDRYCLY]:
				PEFCC = (PEFCC - GRCLAYFRAC * PEFDRYCLY) / (1.01 - GRCLAYFRAC)
			if MissingValue not in [PEFCC, RHOBCC]:
				UCC = PEFCC * RHOBCC
			if MissingValue not in [GRCLAYFRAC]:
				CLAYFRAC = GRCLAYFRAC
	return (
		VSHGR, GRCLAYFRAC, RHODRYCL, mclayln, cclayln, NPHDRYCL, PHITCLY, NPHICC, RHOBCC, PEFCC, CLAYFRAC, UCC)


def CARB_LITHO_VOLUME(LITHTYPE, LITH2FLG, CLAYFLG, DNCALCFRAC, DNDOLOFRAC, DNQRTZFRAC, DNMIN1FRAC, PDCALCFRAC, PDDOLOFRAC, PDQRTZFRAC, PDMIN1FRAC, PEFCALCFRAC, PEFDOLOFRAC, PEFQRTZFRAC, PEFMIN1FRAC, MNCALCFRAC, MNDOLOFRAC, MNQRTZFRAC, MNMIN1FRAC, MNMIN2FRAC, CLAYFRAC, RHODRYCL, CALCFRAC, RHOBDRYLM, DOLOFRAC, RHOBDRYDL, QRTZFRAC, MIN1FRAC, MIN2FRAC,RHOBDRYQZ, RHOBDRYMIN1, RHOBDRYMIN2, GRCLAYFRAC, NPHDRYCL, RHOB_FLUID, PHITCLY, NPHICC, RHOBCC, PEFCC, UCC, RHOBHC, NPHIHC, ZNRHOBCL, RHOBFC):
	#region Lithology Volume Calculation Parameters
	"""Lithology Volume Calculation
		Inputs:
		 1. LITHTYPE [string]: Lithology Components
		 2. LITH2FLG [string]: 2-Minerals Volume Calculation Method
		 3. CLAYFLG [string]: Model With Clay
		 4. DNCALCFRAC [number]: DN Calc Fraction  (Carbonates)
		 5. DNDOLOFRAC [number]: DN Dolo Fraction  (Carbonates)
		 6. DNQRTZFRAC [number]: DN Qrtz Fraction  (Carbonates)
		 7. DNMIN1FRAC [number]: DN Min1 Fraction  (Carbonates)
		 8. PDCALCFRAC [number]: PEF-DEN Calc Fraction  (Carbonates)
		 9. PDDOLOFRAC [number]: PEF-DEN Dolo Fraction  (Carbonates)
		 10. PDQRTZFRAC [number]: PEF-DEN Qrtz Fraction  (Carbonates)
		 11. PDMIN1FRAC [number]: PEF-DEN Min1 Fraction  (Carbonates)
		 12. PEFCALCFRAC [number]: PEF Calc Fraction  (Carbonates)
		 13. PEFDOLOFRAC [number]: PEF Dolo Fraction  (Carbonates)
		 14. PEFQRTZFRAC [number]: PEF Qrtz Fraction  (Carbonates)
		 15. PEFMIN1FRAC [number]: EF Min1 Fraction  (Carbonates)
		 16. MNCALCFRAC [number]: M-N Calc Fraction  (Carbonates)
		 17. MNDOLOFRAC [number]: M-N Dolo Fraction  (Carbonates)
		 18. MNQRTZFRAC [number]: M-N Qrtz Fraction  (Carbonates)
		 19. MNMIN1FRAC [number]: M-N Min1 Fraction  (Carbonates)
		 20. MNMIN2FRAC [number]: M-N Min2 Fraction  (Carbonates)
		 21. CLAYFRAC [number]: Clay Fraction
		 22. RHODRYCL [number]: Density Dry Clay
		 23. CALCFRAC [number]: Calcite Fraction  (Carbonates)
		 24. RHOBDRYLM [number]:RHOB Calcite
		 25. DOLOFRAC [number]: Dolomite Fraction  (Carbonates)
		 26. RHOBDRYDL [number]: RHOB Dolomite
		 27. QRTZFRAC [number]: Quartz Fraction  (Carbonates)
		 27. MIN1FRAC [number]: Mineral 1 Fraction  (Carbonates)
		 27. MIN2FRAC [number]: Mineral 2 Fraction  (Carbonates)
		 28. RHOBDRYQZ [number]: RHOB Quartz
		 30. RHOBDRYMIN1 [number]: RHOB Mineral-1
		 32. RHOBDRYMIN2 [number]: RHOB Mineral-2
		 33. GRCLAYFRAC [number]: GR Clay Fraction
		 34. NPHDRYCL [number]: Neutron Dry Clay
		 35. RHOB_FLUID [number]: RHOB Fluid
		 36. PHITCLY [number]: Zoned Total Porosity of 100% Clay
		 37. NPHICC [number]: NPHI Clay Corrected (Carbonates)
		 38. RHOBCC[number]: RHOB Clay Corrected (Carbonates)
		 39. PEFCC [number]: PEF Clay Corrected (Carbonates)
		 40. UCC [number]: U Clay Corrected (Carbonates)
		 41. RHOBHC [number]: InOut RHOBHC
		 42. NPHIHC [number]: InOut NPHIHC
		Outputs:
		 - [number] NPHICC: NPHI Clay Corrected (Carbonates)
		 - [number] RHOBCC: RHOB Clay Corrected (Carbonates)
		 - [number] PEFCC: PEF Clay Corrected (Carbonates)
		 - [number] UCC: U Clay Corrected (Carbonates)
		 - [number] CALCFRAC: Calcite Fraction  (Carbonates)
		 - [number] DOLOFRAC: Dolomite Fraction  (Carbonates)
		 - [number] QRTZFRAC: Quartz Fraction  (Carbonates)
		 - [number] MIN1FRAC: Mineral-1 Fraction  (Carbonates)
		 - [number] MIN2FRAC: Mineral-2 Fraction  (Carbonates)
		 - [number] RHOG: Grain Density
		 - [number] RHOBHC: HC Corrected Bulk Density
		 - [number] NPHIHC: HC Corrected Neutron Porosity
		 - [number] PHIT: Total Porosity
		 - [number] VMATRX: Volume of Matrix (vsand+vsilt+vcld)
		 - [number] VCLD: Volume of Dry Clay
		 - [number] VCALC: Volume of Calcite
		 - [number] VDOLO: Volume of Dolomite
		 - [number] VQRTZ: Volume of Quartz
		 - [number] VMIN1: Volume of Mineral-1
		 - [number] VMIN2: Volume of Mineral-2
		 - [number] PHIE: Effective Porosity
		 - [number] VCLB: Volume of Clay Bound Water
		 - [number] VCLW: Volume of Wet Clay
		"""
	#endregion
	#MIN1FRAC = MissingValue
	#MIN2FRAC = MissingValue
	PHITCLAY = MissingValue
	if LITHTYPE == 'CA-[CL]' or LITHTYPE == 'DL-[CL]':
		NPHICC = MissingValue
		RHOBCC = MissingValue
		PEFCC = MissingValue
		UCC = MissingValue
		MIN2FRAC = 0
	elif LITHTYPE == 'CA-DL-[CL]' or LITHTYPE == 'CA-QZ-[CL]' or LITHTYPE == 'CA-M1-[CL]':
		if LITH2FLG == 'DEN-NEU':
			CALCFRAC = DNCALCFRAC
			DOLOFRAC = DNDOLOFRAC
			QRTZFRAC = DNQRTZFRAC
			MIN1FRAC = DNMIN1FRAC
			MIN2FRAC = 0
		elif LITH2FLG == 'PEF-DEN':
			CALCFRAC = PDCALCFRAC
			DOLOFRAC = PDDOLOFRAC
			QRTZFRAC = PDQRTZFRAC
			MIN1FRAC = PDMIN1FRAC
			MIN2FRAC = 0
		else:
			CALCFRAC = PEFCALCFRAC
			DOLOFRAC = PEFDOLOFRAC
			QRTZFRAC = PEFQRTZFRAC
			MIN1FRAC = PEFMIN1FRAC
			MIN2FRAC = 0
	else:
		if LITHTYPE == 'CA-DL-QZ-[CL]' or LITHTYPE == 'CA-M1-M2-[CL]':
			CALCFRAC = MNCALCFRAC
			DOLOFRAC = MNDOLOFRAC
			QRTZFRAC = MNQRTZFRAC
			MIN1FRAC = MNMIN1FRAC
			MIN2FRAC = MNMIN2FRAC
	RHOG = 0
	if CLAYFRAC != MissingValue:
		RHOG = RHOG + CLAYFRAC * RHODRYCL
	else:
		RHOBHC = MissingValue
		NPHIHC = MissingValue
	if CALCFRAC != MissingValue:
		RHOG = RHOG + CALCFRAC * RHOBDRYLM
	if DOLOFRAC != MissingValue:
		RHOG = RHOG + DOLOFRAC * RHOBDRYDL
	if QRTZFRAC != MissingValue:
		RHOG = RHOG + QRTZFRAC * RHOBDRYQZ
	if MIN1FRAC != MissingValue:
		RHOG = RHOG + MIN1FRAC * RHOBDRYMIN1
	if MIN2FRAC != MissingValue:
		RHOG = RHOG + MIN2FRAC * RHOBDRYMIN2
	sumMin = CALCFRAC + DOLOFRAC + QRTZFRAC
	if LITHTYPE != 'CA-[CL]' and LITHTYPE != 'DL-[CL]':
		if CLAYFLG == 'YES':
			if MissingValue not in [RHOBHC, NPHIHC]:
				RHOBHC = RHOBHC * (1.01 - GRCLAYFRAC) + \
					GRCLAYFRAC * RHODRYCL
				NPHIHC = NPHIHC * (1.01 - GRCLAYFRAC) + \
					GRCLAYFRAC * NPHDRYCL
			else:
				RHOBHC = MissingValue
				NPHIHC = MissingValue
	PHIT = MissingValue
	try:
		if MissingValue not in [RHOG, RHOBHC, RHOB_FLUID, CLAYFRAC]:
			PHIT = (RHOG - RHOBHC) / (RHOG - RHOB_FLUID)
			PHIT = max(0, PHIT)
	except:
		pass

	VCLD = MissingValue
	VCALC = MissingValue
	VDOLO = MissingValue
	VQRTZ = MissingValue
	VMIN1 = MissingValue
	VMIN2 = MissingValue
	VMATRX = MissingValue
	PHIE = MissingValue
	VCLB = MissingValue
	VCLW = MissingValue
	VSILT = MissingValue
	VSAND = MissingValue
	if PHIT != MissingValue:
		VMATRX = 1 - PHIT
		if CLAYFRAC != MissingValue:
			VCLD = CLAYFRAC * VMATRX
		if CALCFRAC != MissingValue:
			VCALC = CALCFRAC * VMATRX
		if DOLOFRAC != MissingValue:
			VDOLO = DOLOFRAC * VMATRX
		if QRTZFRAC != MissingValue:
			VQRTZ = QRTZFRAC * VMATRX
		if MIN1FRAC != MissingValue:
			VMIN1 = MIN1FRAC * VMATRX
		if MIN2FRAC != MissingValue:
			VMIN2 = MIN2FRAC * VMATRX
		if RHODRYCL != RHOB_FLUID:
			PHITCLY = (RHODRYCL - ZNRHOBCL) / (RHODRYCL - RHOB_FLUID)
			if CLAYFRAC != MissingValue:
				PHIE = PHIT - CLAYFRAC * PHITCLY
			else:
				PHIE = PHIT
			if PHITCLY > PHIT:
				PHIE = PHIT - CLAYFRAC * PHIT
		VCLB = MissingValue
		if MissingValue not in [PHIT, PHIE]:
			VCLB = PHIT - PHIE
		VCLW = MissingValue
		if MissingValue not in [VCLD, VCLB]:
			VCLW = VCLD + VCLB
		VSILT = 0
		VSAND = 0
	return (
		NPHICC, RHOBCC, PEFCC, UCC, CALCFRAC, DOLOFRAC, QRTZFRAC, MIN1FRAC, MIN2FRAC, RHOG, RHOBHC, NPHIHC, PHIT, VMATRX, VCLD, VCALC, VDOLO, VQRTZ, VMIN1, VMIN2, PHIE, VCLB, VCLW, PHITCLAY, VSILT, VSAND)


def CARB_DN_LITHOLOGY(LITHTYPE, CLAYFLG, RHOBDRYLM, RHOBFLC, NPHIDRYLM, NPHIFLC, RHOBDRYDL, NPHIDRYDL, NPHITOOLDL, RHOBDRYQZ, NPHIDRYQZ, NPHITOOLQZ, RHOBDRYMIN1, NPHIDRYMIN1, ZNRHOWCL, ZNNPHWCL, RHODRYCL, NPHDRYCL, RHOBHC, NPHIHC, CLAYFRAC):
	"""Lithology Volume Calculation
		Inputs:
		 1. LITHTYPE [string]: Lithology Components
		 2. CLAYFLG [string]: Model With Clay
		 3. RHOBDRYLM [number]:RHOB Calcite
		 4. RHOBFLC [number]: Fluid Density
		 5. NPHIDRYLM [number]: NPHI Calcite
		 6. NPHIFLC [number]: Fluid Parameters for Neutron
		 7. RHOBDRYDL [number]: RHOB Dolomite
		 8. NPHIDRYDL [number]: NPHI Dolomite
		 9. NPHITOOLDL [number]: Fluid Parameters for Neutron
		 10. RHOBDRYQZ [number]: RHOB Quartz
		 11. NPHIDRYQZ [number]: NPHI Quartz
		 12. NPHITOOLQZ [number]: Fluid Parameters for Neutron
		 13. RHOBDRYMIN1 [number]: RHOB Mineral-1
		 14. NPHIDRYMIN1 [number]: NPHI Mineral-1
		 15. ZNRHOWCL [number]: Zoned RHOB Clay (Carbonates)
		 16. ZNNPHWCL [number]: Zoned NPHI Clay (Carbonates)
		 17. RHODRYCL [number]: Density Dry Clay
		 18. NPHDRYCL [number]: Neutron Dry Clay
		 19. RHOBHC [number]: HC Corrected Bulk Density
		 20. NPHIHC [number]: HC Corrected Neutron Porosity
		Outputs:
		 - [number] mclayln: WetClay Angle, also used in SSC_DN_LITHOLOGY 
		 - [number] cclayln: WetClay Angle, also used in SSC_DN_LITHOLOGY 
		 - [number] mmatdclln: DryMat-DryClay Line, also used in SSC_DN_LITHOLOGY and SSC_MAIN_A
		 - [number] cmatdclln: DryMat-DryClay Line, also used in SSC_DN_LITHOLOGY and SSC_MAIN_A
		 - [number] rhorefmat: RHOB Dry Sand, also used in SSC_MAIN_A and HC_CORR_METHOD
		 - [number] DNCLAYFRAC: DN Clay Fraction (Carbonates)
		 - [number] CLAYFRAC: Clay Fraction
		 - [number] CALCFRAC: Calcite Fraction  (Carbonates)
		 - [number] VSHDRYDN: VSH-Dry from Density-Neutron (Linear)
		 - [number] hck: local variable also used in SSC_MAIN_A and HC_CORR_METHOD
		 - [number] DNLITH2FRAC: DN Litho-2 Fraction  (Carbonates)
		 - [number] DNDOLOFRAC: DN Dolo Fraction  (Carbonates)
		 - [number] DNCALCFRAC: DN Calc Fraction  (Carbonates)
		 - [number] DNQRTZFRAC: DN Qrtz Fraction  (Carbonates)
		 - [number] DNMIN1FRAC: DN Min1 Fraction  (Carbonates)
		 - [number] RHOB_FLUID: RHOB Fluid
		 - [number] NPHI_FLUID: NPHI Fluid
		 - [number] ZNRHOBCL: Zoned RHOB Clay
		 - [number] DOLOFRAC

		"""
	mcalcln = MissingValue
	ccalcln = MissingValue
	DOLOFRAC = MissingValue
	QRTZFRAC = MissingValue
	MIN1FRAC = MissingValue
	if MissingValue not in [RHOBDRYLM, RHOBFLC, NPHIDRYLM, NPHIFLC]:
		try:
			mcalcln = (RHOBDRYLM - RHOBFLC) / (NPHIDRYLM - NPHIFLC)
			ccalcln = RHOBDRYLM - mcalcln * NPHIDRYLM
		except:
			pass

	mdololn = MissingValue
	cdololn = MissingValue
	if MissingValue not in [RHOBDRYDL, RHOBFLC, NPHIDRYDL, NPHITOOLDL]:
		try:
			mdololn = (RHOBDRYDL - RHOBFLC) / (NPHIDRYDL - NPHITOOLDL)
			cdololn = RHOBDRYDL - mdololn * NPHIDRYDL
		except:
			pass

	mqrtzln = MissingValue
	cqrtzln = MissingValue
	if MissingValue not in [RHOBDRYQZ, RHOBFLC, NPHIDRYQZ, NPHITOOLQZ]:
		try:
			mqrtzln = (RHOBDRYQZ - RHOBFLC) / (NPHIDRYQZ - NPHITOOLQZ)
			cqrtzln = RHOBDRYQZ - mqrtzln * NPHIDRYQZ
		except:
			pass

	mmin1ln = MissingValue
	cmin1ln = MissingValue
	if MissingValue not in [RHOBDRYMIN1, RHOBFLC, NPHIDRYMIN1, NPHIFLC]:
		try:
			mmin1ln = (RHOBDRYMIN1 - RHOBFLC) / (NPHIDRYMIN1 - NPHIFLC)
			cmin1ln = RHOBDRYMIN1 - mmin1ln * NPHIDRYMIN1
		except:
			pass

	mclayln = MissingValue
	cclayln = MissingValue
	if MissingValue not in [ZNRHOWCL, RHOBFLC, ZNNPHWCL, NPHIFLC]:
		try:
			mclayln = (ZNRHOWCL - RHOBFLC) / (ZNNPHWCL - NPHIFLC)
			cclayln = RHOBFLC - mclayln * NPHIFLC
		except:
			pass

	if CLAYFLG == 'NO':
		mclayln = (2.5 - RHOBFLC) / (0.4 - NPHIFLC)
		cclayln = RHOBFLC - mclayln * NPHIFLC
	mmatdclln = MissingValue
	cmatdclln = MissingValue
	rhorefmat = MissingValue
	if MissingValue not in [RHOBHC, NPHIHC]:
		if LITHTYPE == 'CA-[CL]':
			mmatdclln = (RHODRYCL - RHOBDRYLM) / (NPHDRYCL - NPHIDRYLM)
			cmatdclln = RHOBDRYLM - mmatdclln * NPHIDRYLM
			rhorefmat = RHOBDRYLM
		elif LITHTYPE == 'DL-[CL]':
			mmatdclln = (RHODRYCL - RHOBDRYDL) / (NPHDRYCL - NPHIDRYDL)
			cmatdclln = RHOBDRYDL - mmatdclln * NPHIDRYDL
			rhorefmat = RHOBDRYDL
		elif LITHTYPE == 'CA-DL-[CL]':
			mmatdclln = (RHOBDRYDL - RHOBDRYLM) / (NPHIDRYDL - NPHIDRYLM)
			cmatdclln = RHOBDRYLM - mmatdclln * NPHIDRYLM
			rhorefmat = RHOBDRYLM
		elif LITHTYPE == 'CA-QZ-[CL]':
			mmatdclln = (RHOBDRYQZ - RHOBDRYLM) / (NPHIDRYQZ - NPHIDRYLM)
			cmatdclln = RHOBDRYLM - mmatdclln * NPHIDRYLM
			rhorefmat = RHOBDRYLM
		elif LITHTYPE == 'CA-M1-[CL]':
			mmatdclln = (RHOBDRYMIN1 - RHOBDRYLM) / (NPHIDRYMIN1 - NPHIDRYLM)
			cmatdclln = RHOBDRYLM - mmatdclln * NPHIDRYLM
			rhorefmat = RHOBDRYLM
	DNLITH2FRAC = MissingValue
	DNDOLOFRAC = MissingValue
	DNCALCFRAC = MissingValue
	DNQRTZFRAC = MissingValue
	DNMIN1FRAC = MissingValue
	CALCFRAC = MissingValue
	DNCLAYFRAC = MissingValue
	VSHDRYDN = MissingValue
	hck = MissingValue
	if MissingValue not in [RHOBHC, NPHIHC]:
		if LITHTYPE == 'CA-[CL]':
			try:
				xcmatdclln = RHOBHC - mmatdclln * NPHIHC
				nphix1 = (ccalcln - xcmatdclln) / (mmatdclln - mcalcln)
				rhobx1 = mmatdclln * nphix1 + xcmatdclln
				nphix2 = (cclayln - xcmatdclln) / (mmatdclln - mclayln)
				rhobx2 = mmatdclln * nphix2 + xcmatdclln
				DNCLAYFRAC = (RHOBHC - rhobx1) / (rhobx2 - rhobx1)
				if CLAYFLG == 'YES':
					CLAYFRAC = limitValue(DNCLAYFRAC, 0, 1)
					CALCFRAC = 1 - CLAYFRAC
				else:
					CLAYFRAC = 0
					CALCFRAC = 1
				DNCALCFRAC = CALCFRAC
				DNDOLOFRAC = 0
				DNQRTZFRAC = 0
				DNMIN1FRAC = 0
				DOLOFRAC = 0
				QRTZFRAC = 0
				MIN1FRAC = 0
				VSHDRYDN = DNCLAYFRAC
				hck = 1.046
			except:
				pass

		elif LITHTYPE == 'DL-[CL]':
			try:
				xcmatdclln = RHOBHC - mmatdclln * NPHIHC
				nphix1 = (cdololn - xcmatdclln) / (mmatdclln - mdololn)
				rhobx1 = mmatdclln * nphix1 + xcmatdclln
				nphix2 = (cclayln - xcmatdclln) / (mmatdclln - mclayln)
				rhobx2 = mmatdclln * nphix2 + xcmatdclln
				DNCLAYFRAC = (RHOBHC - rhobx1) / (rhobx2 - rhobx1)
				if CLAYFLG == 'YES':
					CLAYFRAC = limitValue(DNCLAYFRAC, 0, 1)
					DOLOFRAC = 1 - CLAYFRAC
				else:
					CLAYFRAC = 0
					DOLOFRAC = 1
				DNCALCFRAC = 0
				DNDOLOFRAC = DOLOFRAC
				DNQRTZFRAC = 0
				DNMIN1FRAC = 0
				CALCFRAC = 0
				QRTZFRAC = 0
				MIN1FRAC = 0
				VSHDRYDN = DNCLAYFRAC
				hck = 1.173
			except:
				pass

		elif LITHTYPE == 'CA-DL-[CL]':
			try:
				xcmatdclln = RHOBHC - mmatdclln * NPHIHC
				nphix1 = (ccalcln - xcmatdclln) / (mmatdclln - mcalcln)
				rhobx1 = mmatdclln * nphix1 + xcmatdclln
				nphix2 = (cdololn - xcmatdclln) / (mmatdclln - mdololn)
				rhobx2 = mmatdclln * nphix2 + xcmatdclln
				DNLITH2FRAC = (RHOBHC - rhobx1) / (rhobx2 - rhobx1)
				DNDOLOFRAC = limitValue(DNLITH2FRAC, 0, 1)
				DNCALCFRAC = 1 - DNDOLOFRAC
				DNQRTZFRAC = 0
				DNMIN1FRAC = 0
				VSHDRYDN = DNLITH2FRAC
				directflg = 0
				hck = 1.046 * DNCALCFRAC + 1.173 * DNDOLOFRAC
			except:
				pass

		elif LITHTYPE == 'CA-QZ-[CL]':
			try:
				xcmatdclln = RHOBHC - mmatdclln * NPHIHC
				nphix1 = (ccalcln - xcmatdclln) / (mmatdclln - mcalcln)
				rhobx1 = mmatdclln * nphix1 + xcmatdclln
				nphix2 = (cqrtzln - xcmatdclln) / (mmatdclln - mqrtzln)
				rhobx2 = mmatdclln * nphix2 + xcmatdclln
				DNLITH2FRAC = (RHOBHC - rhobx1) / (rhobx2 - rhobx1)
				DNQRTZFRAC = limitValue(DNLITH2FRAC, 0, 1)
				DNCALCFRAC = 1 - DNQRTZFRAC
				DNDOLOFRAC = 0
				DNMIN1FRAC = 0
				VSHDRYDN = 1 - DNLITH2FRAC
				directflg = 1
				hck = 1.046 * DNCALCFRAC + 1.0 * DNQRTZFRAC
			except:
				pass

		elif LITHTYPE == 'CA-M1-[CL]':
			try:
				xcmatdclln = RHOBHC - mmatdclln * NPHIHC
				nphix1 = (ccalcln - xcmatdclln) / (mmatdclln - mcalcln)
				rhobx1 = mmatdclln * nphix1 + xcmatdclln
				nphix2 = (cmin1ln - xcmatdclln) / (mmatdclln - mmin1ln)
				rhobx2 = mmatdclln * nphix2 + xcmatdclln
				DNLITH2FRAC = (RHOBHC - rhobx1) / (rhobx2 - rhobx1)
				DNMIN1FRAC = limitValue(DNLITH2FRAC, 0, 1)
				DNCALCFRAC = 1 - DNMIN1FRAC
				DNDOLOFRAC = 0
				DNQRTZFRAC = 0
				if mmin1ln > mcalcln:
					directflg = 1
				else:
					directflg = 0
				hck = 1.046
			except:
				pass

	RHOB_FLUID = RHOBFLC
	NPHI_FLUID = NPHIFLC
	ZNRHOBCL = ZNRHOWCL
	if LITHTYPE != 'CA-[CL]' and LITHTYPE != 'DL-[CL]':
		if MissingValue not in [DNCALCFRAC, CLAYFRAC]:
			DNCALCFRAC = DNCALCFRAC * (1 - CLAYFRAC)
		if MissingValue not in [DNDOLOFRAC, CLAYFRAC]:
			DNDOLOFRAC = DNDOLOFRAC * (1 - CLAYFRAC)
		if MissingValue not in [DNQRTZFRAC, CLAYFRAC]:
			DNQRTZFRAC = DNQRTZFRAC * (1 - CLAYFRAC)
		if MissingValue not in [DNMIN1FRAC, CLAYFRAC]:
			DNMIN1FRAC = DNMIN1FRAC * (1 - CLAYFRAC)
	return (
		mclayln, cclayln, mmatdclln, cmatdclln, rhorefmat, DNCLAYFRAC, CLAYFRAC, CALCFRAC, VSHDRYDN, hck, DNLITH2FRAC, DNDOLOFRAC, DNCALCFRAC,
		DNQRTZFRAC, DNMIN1FRAC, RHOB_FLUID, NPHI_FLUID, ZNRHOBCL, DOLOFRAC, QRTZFRAC, MIN1FRAC)


def SSC_GR_LITHOLOGY(GR, ZNGRSD, ZNGRCL, RHODRYCL, RHODRYSL, RHOB_DRY_SAND):
	"""Lithology from GR Calculation
		Inputs:
		 1. GR [number]: Gamma Ray log
		 2. ZNGRSD [number]: Zoned Gamma Ray Sand
		 3. ZNGRCL [number]: Zoned Gamma Ray Clay
		 4. RHODRYCL [number]: Density Dry Clay
		 5. RHODRYSL [number]: Density Dry Silt
		 6. RHOB_DRY_SAND [number]: RHOB Dry Sand
		 7. ca1 [number][=0.3]: SSC Parameters
		 8. ca2 [number][=0.17355]: SSC Parameters
		 9. ca3 [number][=0.1285]: SSC Parameters
		 10. sa1 [number][=3]: SSC Parameters
		 11. sa2 [number][=-11.4]: SSC Parameters
		 12. sa3 [number][=3.8]: SSC Parameters
		 13. cb1 [number][=0.5]: SSC Parameters
		 14. cb2 [number][=0.375]: SSC Parameters
		 15. cb3 [number][=1.2]: SSC Parameters
		 16. sb1 [number][=1]: SSC Parameters
		 17. sb2 [number][=0]: SSC Parameters
		 18. sb3 [number][=0]: SSC Parameters
		Outputs:
		 - [number] VSHGR: VSH Gamma Ray
		 - [number] grsndsltfrac: GR Sand-Silt Ratio
		 - [number] grclysltfrac: GR Clay-Silt Ratio
		 - [number] grclayfrac: GR Clay Fraction
		 - [number] grsandfrac: GR Sand Fraction
		 - [number] grsiltfrac: GR Silt Fraction
		"""
	VSHGR = MissingValue
	rhobxvshgr = MissingValue
	grsndsltfrac = MissingValue
	grclysltfrac = MissingValue
	grclayfrac = MissingValue
	grsandfrac = MissingValue
	grsiltfrac = MissingValue
	if MissingValue in [GR, ZNGRSD, ZNGRCL, RHODRYCL, RHODRYSL, RHOB_DRY_SAND]:
		return (MissingValue, MissingValue, MissingValue, MissingValue, MissingValue, MissingValue)
	try:
		VSHGR = (GR - ZNGRSD) / (ZNGRCL - ZNGRSD)
		rhobxvshgr = limitValue(VSHGR, 0, 1) * \
			(RHODRYCL - RHOB_DRY_SAND) + RHOB_DRY_SAND
		grsndsltfrac = (rhobxvshgr - RHODRYSL) / (RHOB_DRY_SAND - RHODRYSL)
		grclysltfrac = (rhobxvshgr - RHODRYSL) / (RHODRYCL - RHODRYSL)
		grsandfrac, grsiltfrac, grclayfrac = LITHOLOGY_CHART(
			grsndsltfrac, grclysltfrac)
		return (
			VSHGR, grsndsltfrac, grclysltfrac, grclayfrac, grsandfrac, grsiltfrac)
	except:
		return (
			MissingValue, MissingValue, MissingValue, MissingValue, MissingValue, MissingValue)


def SSC_DN_LITHOLOGY(DNXPLOTSAND, RHOB_DRY_SAND, RHOB_FLUID, NPHI_DRY_SAND, NPHI_FLUID, ZNRHOBCL, ZNNPHICL, ZNSLTLINRAT, RHODRYSL, RHOBHC, NPHIHC, USE_SILT_ANGLE, DEGFLSLT, NPHI_OFFSET):
	"""Lithology Volume Calculation
		Inputs:
		 1. DNXPLOTSAND [string]: Type of Sand Line on DN Crossplot
		 2. RHOB_DRY_SAND [number]: RHOB Dry Sand
		 3. RHOB_FLUID [number]: RHOB Fluid
		 4. NPHI_DRY_SAND [number]: NPHI Dry Sand
		 5. NPHI_FLUID [number]: NPHI Fluid
		 6. ZNRHOBCL [number]: Zoned RHOB Clay
		 7. ZNNPHICL [number]: Zoned NPHI Clay
		 8. ZNSLTLINRAT [number]: Zoned Silt Line Position
		 9. RHODRYSL [number]: Density Dry Silt
		 10. RHOBHC [number]: HC Corrected Bulk Density
		 11. NPHIHC [number]: HC Corrected Neutron Porosity
		Outputs:
		 - [number] DEGSNDLN: Sand Line Angle
		 - [number] DEGCLYLN: Clay Line Angle
		 - [number] DEGSLTLN: Silt Line Angle
		 - [number] NPHDRYSL: Neutron Dry Silt
		 - [number] NPHDRYCL: Neutron Dry Clay
		 - [number] RHODRYCL: Density Dry Clay
		 - [number] PHITCLY: Zoned Total Porosity of 100% Clay
		 - [number] VSHDRYDN: VSH-Dry from Density-Neutron (Linear)
		 - [number] SNDSLTFRAC: Sand-Silt Ratio
		 - [number] CLYSLTFRAC: Clay-Silt Ratio
		 - [number] SANDFRAC: Sand Fraction
		 - [number] CLAYFRAC: Clay Fraction
		 - [number] SILTFRAC: Silt Fraction
		 - [number] cmatdclln: Intermediate output
		 - [number] mmatdclln: Intermediate output
		"""
	cclayln = MissingValue
	mclayln = MissingValue
	mlogln = MissingValue
	msandln = MissingValue
	csandln = MissingValue
	msiltln = MissingValue
	csiltln = MissingValue
	nonphidrysand = NPHI_DRY_SAND
	nonrhodrysand = RHOB_DRY_SAND
	cons1 = MissingValue
	cons2 = MissingValue
	cons3 = MissingValue
	cons4 = MissingValue
	mrhoffset = MissingValue
	crhoffset = MissingValue
	if DNXPLOTSAND == 'SLB-CNL':
		nonphidrysand = -0.02
		cons1 = -0.852
		cons2 = 1.357
		cons3 = -2.112
		cons4 = 2.607
	elif DNXPLOTSAND == 'SLB-ECOSC':
		nonphidrysand = -0.0078
		cons1 = -0.039
		cons2 = 0.512
		cons3 = -2.107
		cons4 = 2.634
	else:
		if DNXPLOTSAND == 'SLB-ADN475':
			nonphidrysand = -0.02
			cons1 = 0.072
			cons2 = 0.284
			cons3 = -1.967
			cons4 = 2.611
		elif DNXPLOTSAND == 'SLB-ADN675':
			nonphidrysand = -0.02
			cons1 = 0.035
			cons2 = 0.199
			cons3 = -1.847
			cons4 = 2.613
		elif DNXPLOTSAND == 'SLB-ADN825':
			nonphidrysand = -0.018
			cons1 = -0.502
			cons2 = 0.84
			cons3 = -1.953
			cons4 = 2.615
		elif DNXPLOTSAND == 'BA-2420CN':
			nonphidrysand = -0.041
			cons1 = 0.143
			cons2 = -0.115
			cons3 = -1.612
			cons4 = 2.584
		elif DNXPLOTSAND == 'BA-2435CN':
			nonphidrysand = -0.0215
			cons1 = -0.821
			cons2 = 1.324
			cons3 = -2.108
			cons4 = 2.604
		elif DNXPLOTSAND == 'BA-2446CN':
			nonphidrysand = -0.029
			cons1 = 0.301
			cons2 = -0.162
			cons3 = -1.737
			cons4 = 2.6
		elif DNXPLOTSAND == 'HAL-CTN434':
			nonphidrysand = -0.025
			cons1 = -0.438
			cons2 = 0.85
			cons3 = -2.012
			cons4 = 2.599
		elif DNXPLOTSAND == 'HAL-CTN634':
			nonphidrysand = -0.018
			cons1 = -1.065
			cons2 = 1.603
			cons3 = -2.149
			cons4 = 2.611
		elif DNXPLOTSAND == 'HAL-CTN800':
			nonphidrysand = -0.018
			cons1 = -0.155
			cons2 = 0.486
			cons3 = -1.946
			cons4 = 2.615
		elif DNXPLOTSAND == 'NON-LINEAR':
			nonphidrysand = -0.041
			cons1 = 0.338
			cons2 = -0.167
			cons3 = -1.752
			cons4 = 2.581
		if DNXPLOTSAND != 'LINEAR':
			if NPHI_OFFSET < 0.11 and NPHI_OFFSET > -0.11:
				nonphidrysand = nonphidrysand + NPHI_OFFSET
		DEGCLYLN = MissingValue
		if MissingValue not in [ZNRHOBCL, RHOB_FLUID, ZNNPHICL, NPHI_FLUID]:
			try:
				mclayln = (ZNRHOBCL - RHOB_FLUID) / (ZNNPHICL - NPHI_FLUID)
				cclayln = RHOB_FLUID - mclayln * NPHI_FLUID
				DEGCLYLN = 180 + degrees(atan(mclayln))
			except:
				pass

		DEGSNDLN = MissingValue
		if MissingValue not in [nonrhodrysand, RHOB_FLUID, nonphidrysand, NPHI_FLUID]:
			try:
				msandln = (nonrhodrysand - RHOB_FLUID) / \
					(nonphidrysand - NPHI_FLUID)
				csandln = RHOB_FLUID - msandln * NPHI_FLUID
				DEGSNDLN = 180 + degrees(atan(msandln))
			except:
				pass

		DEGSLTLN = MissingValue
		NPHDRYSL = MissingValue
		if MissingValue not in [DEGSNDLN, DEGCLYLN, ZNSLTLINRAT, RHOB_FLUID, NPHI_FLUID, RHODRYSL]:
			try:
				if USE_SILT_ANGLE == 'YES':
					DEGSLTLN = DEGFLSLT
					ZNSLTLINRAT = 100 * \
						(DEGSLTLN - DEGSNDLN) / (DEGCLYLN - DEGSNDLN)
				else:
					DEGSLTLN = DEGSNDLN + \
						(DEGCLYLN - DEGSNDLN) * ZNSLTLINRAT / 100
				msiltln = tan(radians(DEGSLTLN))
				csiltln = RHOB_FLUID - msiltln * NPHI_FLUID
				NPHDRYSL = (RHODRYSL - csiltln) / msiltln
			except:
				pass

		NPHDRYCL = MissingValue
		RHODRYCL = MissingValue
		mmatdclln = MissingValue
		cmatdclln = MissingValue
		if MissingValue not in [RHODRYSL, nonrhodrysand, NPHDRYSL, nonphidrysand]:
			try:
				mmatdclln = (RHODRYSL - nonrhodrysand) / \
					(NPHDRYSL - nonphidrysand)
				cmatdclln = nonrhodrysand - mmatdclln * nonphidrysand
				NPHDRYCL = (cmatdclln - cclayln) / (mclayln - mmatdclln)
				RHODRYCL = NPHDRYCL * mclayln + cclayln
				rhorefmat = RHOB_DRY_SAND
			except:
				pass

		PHITCLY = MissingValue
		if MissingValue not in [RHODRYCL, ZNRHOBCL, RHODRYCL, RHOB_FLUID]:
			try:
				PHITCLY = (RHODRYCL - ZNRHOBCL) / (RHODRYCL - RHOB_FLUID)
			except:
				pass

		VSHDRYDN = MissingValue
		SNDSLTFRAC = MissingValue
		CLYSLTFRAC = MissingValue
		if DNXPLOTSAND == 'LINEAR':
			if MissingValue not in [RHOBHC, RHOB_FLUID, NPHIHC, NPHI_FLUID]:
				try:
					mlogln = (RHOBHC - RHOB_FLUID) / (NPHIHC - NPHI_FLUID)
					clogln = RHOB_FLUID - mlogln * NPHI_FLUID
					nphixmatdcl = (clogln - cmatdclln) / (mmatdclln - mlogln)
					rhobxmatdcl = mlogln * nphixmatdcl + clogln
					VSHDRYDN = (rhobxmatdcl - RHOB_DRY_SAND) / \
						(RHODRYCL - RHOB_DRY_SAND)
					SNDSLTFRAC = (rhobxmatdcl - RHODRYSL) / \
						(RHOB_DRY_SAND - RHODRYSL)
					CLYSLTFRAC = (rhobxmatdcl - RHODRYSL) / \
						(RHODRYCL - RHODRYSL)
				except:
					pass

		else:
			if nonrhodrysand != 2.65:
				nphiz1 = nonphidrysand
				nphiz2 = nonphidrysand + 0.02
				rhobz1 = cons1 * (nphiz1 - NPHI_OFFSET) ** 3 + cons2 * (
					nphiz1 - NPHI_OFFSET) ** 2 + cons3 * (nphiz1 - NPHI_OFFSET) + cons4
				rhobz2 = cons1 * (nphiz2 - NPHI_OFFSET) ** 3 + cons2 * (
					nphiz2 - NPHI_OFFSET) ** 2 + cons3 * (nphiz2 - NPHI_OFFSET) + cons4
				mrhoffset = (rhobz1 - rhobz2) / (nphiz1 - nphiz2)
				crhoffset = rhobz1 - mrhoffset * nphiz1
				nonphidrysand = (nonrhodrysand - crhoffset) / mrhoffset
			rhobnonxsand = MissingValue
			nphixtemp = 0.45
			nphixsand = -0.1
			cnlsndclyln = RHOBHC - mmatdclln * NPHIHC
			for iter1 in range(20):
				if MissingValue not in [nphixsand]:
					rhobnonxsand = cons1 * (nphixsand - NPHI_OFFSET) ** 3 + cons2 * (
						nphixsand - NPHI_OFFSET) ** 2 + cons3 * (nphixsand - NPHI_OFFSET) + cons4
				if MissingValue not in [mmatdclln, nphixsand, cnlsndclyln, rhobnonxsand]:
					rhobxsand = mmatdclln * nphixsand + cnlsndclyln
					delrhobxsand = rhobnonxsand - rhobxsand
					delta = abs((nphixsand - nphixtemp) / 2)
					nphixtemp = nphixsand
					if delrhobxsand > 0:
						nphixsand = nphixsand + delta
					else:
						nphixsand = nphixsand - delta
					nphixclay = (cnlsndclyln - cclayln) / (mclayln - mmatdclln)
					rhobxclay = nphixclay * mclayln + cclayln
					siltxfrac = (RHODRYSL - nonrhodrysand) / \
						(RHODRYCL - nonrhodrysand)
					rhobxsilt = rhobxsand + siltxfrac * (rhobxclay - rhobxsand)
					VSHDRYDN = (RHOBHC - rhobxsand) / (rhobxclay - rhobxsand)
					SNDSLTFRAC = (RHOBHC - rhobxsilt) / (rhobxsand - rhobxsilt)
					CLYSLTFRAC = (RHOBHC - rhobxsilt) / (rhobxclay - rhobxsilt)

	SANDFRAC, SILTFRAC, CLAYFRAC = LITHOLOGY_CHART(SNDSLTFRAC, CLYSLTFRAC)
	return (
		DEGSNDLN, DEGCLYLN, DEGSLTLN, NPHDRYSL, NPHDRYCL, RHODRYCL, PHITCLY, VSHDRYDN, SNDSLTFRAC, CLYSLTFRAC, SANDFRAC, CLAYFRAC, SILTFRAC,
		cmatdclln, mmatdclln, mclayln, cclayln, csandln, msandln, nonphidrysand, nonrhodrysand, cons1, cons2, cons3, cons4)


def LITHOLOGY_CHART(SNDSLTFRAC, CLYSLTFRAC):
	SA1 = 3
	SA2 = -11.4
	SA3 = 3.8
	SB1 = 1
	SB2 = 0
	SB3 = 0
	CA1 = 0.3
	CA2 = 0.17355
	CA3 = 0.1285
	CB1 = 0.5
	CB2 = 0.375
	CB3 = 1.2
	CLAYFRAC = MissingValue
	SANDFRAC = MissingValue
	SILTFRAC = MissingValue
	if SNDSLTFRAC >= 0 and SNDSLTFRAC < 1:
		SANDFRAC = SA3 + SA2 * (SNDSLTFRAC + SA1) ** (-1)
		CLAYFRAC = CA2 * (SNDSLTFRAC + CA1) ** (-1) - CA3
		SILTFRAC = 1 - SANDFRAC - CLAYFRAC
	elif SNDSLTFRAC >= 1:
		SANDFRAC = 0.95
		CLAYFRAC = 0.005
		SILTFRAC = 1 - SANDFRAC - CLAYFRAC
	if CLYSLTFRAC >= 0 and CLYSLTFRAC < 1:
		SANDFRAC = SB3 + SB2 * (CLYSLTFRAC + SB1) ** (-1)
		CLAYFRAC = CB3 - CB2 * (CLYSLTFRAC + CB1) ** (-1)
		SILTFRAC = 1 - SANDFRAC - CLAYFRAC
	elif CLYSLTFRAC >= 1:
		SANDFRAC = 0
		CLAYFRAC = 0.95
		SILTFRAC = 1 - SANDFRAC - CLAYFRAC
	if SNDSLTFRAC == MissingValue or CLYSLTFRAC == MissingValue:
		SNDSLTFRAC = MissingValue
		CLYSLTFRAC = MissingValue
		SANDFRAC = MissingValue
		CLAYFRAC = MissingValue
		SILTFRAC = MissingValue
	return (
		SANDFRAC, SILTFRAC, CLAYFRAC)


def SSC_LITHO_VOLUME(SANDFRAC, RHOB_DRY_SAND, SILTFRAC, RHODRYSL, CLAYFRAC, RHODRYCL, RHOBFC, RHOB_FLUID, PHITCLY):
	"""Lithology Volume Calculation
		Inputs:
		 1. SANDFRAC [number]: Gamma Ray log
		 2. RHOB_DRY_SAND [number]: RHOB Dry Sand
		 3. SILTFRAC [number]: Silt Fraction
		 4. RHODRYSL [number]: Density Dry Silt
		 5. CLAYFRAC [number]: Clay Fraction
		 6. RHODRYCL [number]: Density Dry Clay
		 7. RHOBFC [number]: HC & BH Corrected Bulk Density
		 8. RHOB_FLUID [number]: RHOB Fluid
		 9. PHITCLY [number]: Zoned Total Porosity of 100% Clay
		Outputs:
		 - [number] RHOG: Grain Density
		 - [number] PHIT: Total Porosity
		 - [number] VMATRX: Volume of Matrix (vsand+vsilt+vcld)
		 - [number] VSAND: Volume of Dry Sandstone
		 - [number] VSILT: Volume of Dry Siltstone
		 - [number] VCLD: Volume of Dry Clay
		 - [number] VCLB: Volume of Clay Bound Water
		 - [number] VCLW: Volume of Wet Clay
		 - [number] VSHALE: Volume of Shale
		 - [number] PHIE: Effective Porosity
		"""
	RHOG = MissingValue
	if MissingValue not in [SANDFRAC, RHOB_DRY_SAND, SILTFRAC, RHODRYSL, CLAYFRAC, RHODRYCL]:
		RHOG = SANDFRAC * RHOB_DRY_SAND + SILTFRAC * RHODRYSL + CLAYFRAC * RHODRYCL
	PHIT = MissingValue
	if MissingValue not in [RHOG, RHOBFC, RHOG, RHOB_FLUID] and RHOG - RHOB_FLUID != 0:
		PHIT = (RHOG - RHOBFC) / (RHOG - RHOB_FLUID)
	if PHIT != MissingValue:
		PHIT = max(0, PHIT)
	VMATRX = MissingValue
	VSAND = MissingValue
	VSILT = MissingValue
	VCLD = MissingValue
	VCALC = MissingValue
	VDOLO = MissingValue
	VQRTZ = MissingValue
	VMIN1 = MissingValue
	VMIN2 = MissingValue
	if MissingValue not in [PHIT]:
		VMATRX = 1 - PHIT
	if MissingValue not in [VMATRX, SANDFRAC]:
		VSAND = SANDFRAC * VMATRX
	if MissingValue not in [VMATRX, SILTFRAC]:
		VSILT = SILTFRAC * VMATRX
	if MissingValue not in [VMATRX, CLAYFRAC]:
		VCLD = CLAYFRAC * VMATRX
	PHIE = MissingValue
	if MissingValue not in [PHIT, CLAYFRAC, PHITCLY]:
		PHIE01 = PHIT - CLAYFRAC * PHITCLY
		PHIE02 = PHIT - CLAYFRAC * PHIT
		PHIE03 = (1 - CLAYFRAC) * (PHIT - CLAYFRAC * PHITCLY) + \
			CLAYFRAC * (PHIT - CLAYFRAC * PHIT)
		PHIE = PHIE03
	if PHIE != MissingValue:
		PHIE = max(0, PHIE)
	VCLB = MissingValue
	VCLW = MissingValue
	VSHALE = MissingValue
	if MissingValue not in [PHIT, PHIE]:
		VCLB = PHIT - PHIE
	if MissingValue not in [VCLD, VCLB]:
		VCLW = VCLD + VCLB
	if MissingValue not in [VCLW, VSILT]:
		VSHALE = VCLW + VSILT
	VCALC = 0
	VDOLO = 0
	VQRTZ = 0
	VMIN1 = 0
	VMIN2 = 0
	return (
		RHOG, PHIT, VMATRX, VSAND, VSILT, VCLD, VCLB, VCLW, VSHALE, PHIE, VCALC, VDOLO, VQRTZ, VMIN1, VMIN2)


def TEMP_SAL_ZONATION(TEMPSOURCE, DEPTHSOURCE, TVDSS, RTKB_DEP, TD_TVDSS, DEPTH, TD_MD, WELLLOC, BHT_TEMP, SB_TEMP, SB_DEP, SURF_TEMP, GL_DEP, TEMP_LOG, SALFLG, SALW, ZNRW):
	"""Sets the coal volume using Coal Flags
		Inputs:
		 1. TEMPSOURCE [string]: Source of Formation Temperature
		 2. DEPTHSOURCE [string]: Depth Source for Temperature Calculation (MD/TVDSS)
		 3. TVDSS [number]: TVDSS Depth
		 4. RTKB_DEP [number]: DF/KB from MSL (M/FT)
		 5. TD_TVDSS [number]: Bottom Hole Depth in TVDSS (M/FT)
		 6. DEPTH [number]: DEPTH
		 7. TD_MD [number]: Bottom Hole Depth (M/FT)
		 8. WELLLOC [string]: Well Location
		 9. BHT_TEMP [number]: Bottom Hole Temp.
		 10. SB_TEMP [number]: Sea Bed Temp.
		 11. SB_DEP [number]: Sea Bed from MSL (M/FT)
		 12. SURF_TEMP [number]: Surface Temp.
		 13. GL_DEP [number]: GL from MSL (M/FT)
		 14. TEMP_LOG [number]: External Temperature Log
		 16. SALFLG [string]: Calculate Rw from Water Salinity (SALW)
		 17. ZNSALWTR: [number]: Formation Water Salinity
		 18. ZNRW [number] Water resistivity
		Output:
		 - [number] ZNTEMP: Zoned Reservoir Temperature
		 - [number] zntempunit: Zoned Reservoir Temperature
		 - [number] ZNRW77F: Zoned RW at 77 Deg F
		 - [number] ZNSALWTR: ormation Water Salinity
		 - [number] ZNRW: Zoned RW at Reservoir Condition
		"""
	tdtmpx = MissingValue
	deptmpx = MissingValue
	tgrad = MissingValue
	ZNTEMP = MissingValue
	zntempunit = MissingValue
	ZNRW77F = MissingValue
	ZNSALWTR = MissingValue
	if TEMPSOURCE == 'CALCULATED':
		if DEPTHSOURCE == 'DEPTH_TVDSS':
			if MissingValue not in [TVDSS, RTKB_DEP, TD_TVDSS]:
				deptmpx = TVDSS + RTKB_DEP
				tdtmpx = TD_TVDSS + RTKB_DEP
		elif MissingValue not in [DEPTH, TD_MD]:
			deptmpx = DEPTH
			tdtmpx = TD_MD
		if WELLLOC == 'OFF_SHORE':
			if MissingValue not in [BHT_TEMP, SB_TEMP, tdtmpx, RTKB_DEP, SB_DEP]:
				tgrad = (BHT_TEMP - SB_TEMP) / \
					(tdtmpx - RTKB_DEP - abs(SB_DEP))
				ZNTEMP = SB_TEMP + tgrad * (deptmpx - RTKB_DEP - abs(SB_DEP))
			if deptmpx < RTKB_DEP + abs(SB_DEP):
				ZNTEMP = SURF_TEMP
		elif MissingValue not in [BHT_TEMP, SURF_TEMP, tdtmpx, RTKB_DEP, GL_DEP]:
			tgrad = (BHT_TEMP - SURF_TEMP) / (tdtmpx - (RTKB_DEP - GL_DEP))
			ZNTEMP = SURF_TEMP + tgrad * (deptmpx - (RTKB_DEP - GL_DEP))
			if deptmpx < RTKB_DEP - GL_DEP:
				ZNTEMP = SURF_TEMP
	else:
		ZNTEMP = TEMP_LOG
	zntempunit = ZNTEMP
	if SALFLG == 'YES':
		if MissingValue not in [SALW, zntempunit]:
			if SALW > 1000000.0:
				ZNSALWTR = SALW / 1000000.0
			else:
				ZNSALWTR = SALW
			ZNRW77F = 0.0123 + 3647.5 / ZNSALWTR ** 0.955
			ZNRW = ZNRW77F * 83.77 / (zntempunit + 6.77)
	elif MissingValue not in [ZNRW, zntempunit]:
		ZNRW77F = ZNRW * (zntempunit + 6.77) / 83.77
		ZNRW77F = limitValue(ZNRW77F, 0.0133, 50)
		ZNSALWTR = (3647.5 / (ZNRW77F - 0.0123)) ** 1.0471204188481675
	return (
		ZNTEMP, zntempunit, ZNRW77F, ZNSALWTR, ZNRW)


def ARCHIE_EQU(SWT_METHOD, PHIT, PHIE, ZN_M, ZN_N, RT, ZNRW):
	"""Archie Calculation
		Inputs:
		 1. SWT_METHOD [string]: SW Equation for SSC Model
		 2. PHIT [number]: Total Porosity
		 3. PHIE [number]: Effective Porosity
		 4. ZN_M [number]: Cementation Factor M (M*)
		 5. ZN_N [number]: Saturation Exponent N (N*)
		 6. RT [number]: True Resistivity Log
		 7. ZNRW [number]: Zoned RW at Reservoir Condition
		Output:
		 - [number] SWT_ARC: SWT Archie
		 - [number] SWE_ARC: SWE Archie
		 - [number] SWTU: Unlimited Total Water Saturation
		"""
	try:
		if MissingValue in [PHIT, PHIE, ZN_M, ZN_N, RT, ZNRW]:
			return (MissingValue, MissingValue, MissingValue)
		else:
			SWTU = MissingValue
			if PHIE != 0:
				SWE_ARC = (ZNRW / (PHIE ** ZN_M * RT)) ** (1 / ZN_N)
				SWT_ARC = 1 - (1 - SWE_ARC) * PHIE / PHIT
			else:
				SWT_ARC = 1
				SWE_ARC = 1
			SWT_ARC = limitValue(SWT_ARC, 0, 1)
			SWE_ARC = limitValue(SWE_ARC, 0, 1)
			SWTU = SWT_ARC
			return (
				SWT_ARC, SWE_ARC, SWTU)

	except:
		return (
			MissingValue, MissingValue, MissingValue)


def WAXMAN_EQU(SWT_METHOD, QVFLAG, CALCULATED_MSTAR, ZNRW, RT, ZNCWBGRAD, VCLINVPOR, ZN_M, ZN_N, PHIT, VSHALE, VCLD, QV_LOG, zntempunit, ZNRW77F):
	"""Modified Waxman-Smitt
		Inputs:
		 1. SWT_METHOD [string]: SW Equation for SSC Model
		 2. QVFLAG [string]: Using External Qv Log
		 3. CALCULATED_MSTAR [string]: Using Calculated M* (from M)
		 4. ZNRW [number]: Zoned RW at Reservoir Condition
		 5. RT [number]: True Resistivity Log
		 6. ZNCWBGRAD [number]: Zoned CWB-Gradient at Reservoir Condition
		 7. VCLINVPOR [number]: VCL-PHIT Ratio
		 8. ZN_M [number]: Cementation Factor M (M*)
		 9. ZN_N [number]: Saturation Exponent N (N*)
		 10. PHIT [number]: Total Porosity
		 11. VCLW [number]: Volume of Wet Clay
		 12. QV_LOG [number]: External Qv Log
		 13. zntempunit [number]: Zoned Reservoir Temperature,  Output of TEMP_SAL_ZONATION
		Output:
		 - [number] CW: Zoned CW at Reservoir Condition
		 - [number] BQV: B*Qv of Waxman-Smits
		 - [number] SWTU: Unlimited Total Water Saturation
		 - [number] ROCAL: Calculated Ro of Waxman-Smits
		 - [number] QVSYN: Estimated Qv
		 - [number] ZN_M: Cementation Factor M (M*)
		"""
	CW = MissingValue
	CT = MissingValue
	BQV = MissingValue
	ROCAL = MissingValue
	QVSYN = MissingValue
	BMOB = MissingValue
	SWTU = MissingValue
	if SWT_METHOD == 'WAXMAN_SMITS':
		BMOB = MissingValue
		try:
			CW = 1 / ZNRW
			CT = 1 / RT
			BMOB = 4.6 * (1 - 0.6 * exp(-0.77 / ZNRW77F))
		except:
			pass

		if PHIT != 0:
			if QVFLAG == 'YES':
				if MissingValue not in [BMOB, QV_LOG]:
					BQV = BMOB * QV_LOG
			elif MissingValue not in [ZNCWBGRAD, VCLINVPOR]:
				BQV = ZNCWBGRAD * VCLINVPOR
			if CALCULATED_MSTAR == 'YES':
				if MissingValue not in [ZN_M, ZNRW, BQV, PHIT]:
					MSVAR = ZN_M - log10(1 + ZNRW * BQV) / log10(PHIT)
					ZN_M = MSVAR
			if MissingValue not in [BMOB, BQV]:
				QVSYN = BQV / BMOB
			sat1 = 0.01
			sat2 = 2
			SWTU = MissingValue
			if VCLD > 0.2:
				BQV = BQV * (1 - (VCLD - 0.2) ** 0.2)
			if MissingValue not in [ZN_N, PHIT, ZN_M, CW, BQV]:
				for iter2 in range(20):
					fxa = sat2 ** ZN_N * PHIT ** ZN_M * (CW + BQV / sat2) - CT
					delta = abs((sat2 - sat1) / 2)
					sat1 = sat2
					if fxa < 0:
						sat2 = sat2 + delta
					else:
						sat2 = sat2 - delta

				SWTU = sat2
			if MissingValue not in [PHIT, ZN_M, ZNRW, BQV]:
				ROCAL = 1 / (PHIT ** ZN_M * (1 / ZNRW + BQV))
		else:
			SWTU = 1
	return (
		CW, BQV, SWTU, ROCAL, QVSYN, ZN_M, BMOB)


def COAL_FLAGGING(nphihc, rhobfc, COALFL, EXTCOAL, zncoalcut, vclw, vcld, vclb, vsilt, vsand, vcalc, vdolo, vmin1, vmin2, vgas, voil, vwater, phit, phie, vshale, swtu, swt, swe, swt_arc, swe_arc):
	"""Sets the coal volume using Coal Flags
		Inputs:
		1. nphihc [number]: Neutron Porosity coming from HC_CORR_METHOD
		2. rhobfc [number]: Bulk Density coming from BH_CORRECTION
		3. COALFL [string]: Coal Flaging (coming from parameters)
		4. zncoalcut [number]: Coal indicator cutoff (coming from parameters)
		Output:
		- [number] vcoal: Coal volume (1 or 0)
		- [number] coalind: Coal indicator
		"""
	try:
		vcoal = 0
		if MissingValue not in [nphihc, rhobfc]:
			coalind = nphihc / rhobfc
		else:
			coalind = MissingValue
		if COALFL == 'YES' and zncoalcut != MissingValue and EXTCOAL == 'NO':
			if coalind > zncoalcut:
				vcoal = 1
				vclw = 0
				vcld = 0
				vclb = 0
				vsilt = 0
				vsand = 0
				vcalc = 0
				vdolo = 0
				vmin1 = 0
				vmin2 = 0
				vgas = 0
				voil = 0
				vwater = 0
				phit = 0
				phie = 0
				vshale = 0
				swtu = MissingValue
				swt = MissingValue
				swe = MissingValue
				swt_arc = MissingValue
				swe_arc = MissingValue
	except:
		coalind = MissingValue
		vcoal = MissingValue
		vclw = MissingValue
		vcld = MissingValue
		vclb = MissingValue
		vsilt = MissingValue
		vsand = MissingValue
		vcalc = MissingValue
		vdolo = MissingValue
		vmin1 = MissingValue
		vmin2 = MissingValue
		vgas = MissingValue
		voil = MissingValue
		vwater = MissingValue
		phit = MissingValue
		phie = MissingValue
		vshale = MissingValue
		swtu = MissingValue
		swt = MissingValue
		swe = MissingValue
		swt_arc = MissingValue
		swe_arc = MissingValue

	return (
		coalind, vcoal, vclw, vcld, vclb, vsilt, vsand, vcalc, vdolo, vmin1, vmin2, vgas, voil, vwater, phit, phie, vshale, swtu, swt, swe, swt_arc, swe_arc)


def HC_CORR_METHOD(MFRES, MFTEMP, ZNTEMPUNIT, LITHMOD, rhobcc, nphicc, RHOREFMAT, rhob, nphi, znrw, 
				   zn_m, zn_n, rt, znogf, RHO_OIL, RHO_GAS, HCK, NEUTRONFAC, SHI, COR_METHOD, 
				   DEGHCCOR, gas_correction_eq1=None, gas_correction_eq2=None, gas_correction_eq3=None, gas_correction_eq4=None, gas_correction_eq5=None, gas_correction_eq6=None):
	"""Hydrocarbon correction method
		Inputs:
		2. MFRES [number]: Mud Filtrate Resistivity
		3. MFTEMP [number]: Mud Filtrate Temperature
		4. ZNTEMPUNIT [number]: Temperature, coming from TEMP_SAL_ZONATION
		5. LITHMOD [string]: Lithology Mode, eith SSC or CARB
		6. rhobcc [number] [g/cc]: RHOB Clay Corrected (Carbonates)
		7. nphicc [number] [v/v]: Neutron Porosity, Clay Corrected (Carbonates)
		8. RHOREFMAT [number]: Coming likely from CARB_PD_LITHO
		9. rhob [number] [g/cc]: Bulk Density
		10. nphi [number] [v/v]: Neutron Porosity
		11. znrw [number] [ohmm]: Water resistivity
		12. zn_m [number]: archie's m
		13. zn_n [number]: archie's n
		14. rt [number] [ohmm]: True resistivity
		15. znogf [number]: Zoned Oil-Gas Flag
		16. RHO_OIL [number] [g/cc]: Oil Density (< 0.70 g/cc)
		17. RHO_GAS [number] [g/cc]: Gas Density
		18. HCK [numver]: Coming from CARB_DN_LITHOLOGY
		19. NEUTRONFAC [number]: Neutron Factor (comes from NEUFAC parameter)
		20: SHI [number] [v/v]: ??? Probably defined in the Hydrocarbon correction loop in MAIN
		21: COR_METHOD [string]: Correction Method (from parameters)
		22: DEGHCCOR [number] [dega]: Angle for correction
		23: gas_correction_eq1 [HydrocarbonInputsFirstEquationInputs] : RHOB, NPHI, X_RHOB, SHALE_NEUT, RHOB_FC, NPHI_FC, sand_madens, fluid_dens 
		24: gas_correction_eq2 [HydrocarbonInputsSecondEquationInputs] : znhcor, HCA, HCB, phitgm
		25: gas_correction_eq3 [HydrocarbonInputsThirdEquationInputs]: SAND_LN, SHALE_LN 
		26: gas_correction_eq4 [HydrocarbonInputsFourthEquationInputs]: CSANDLN, CCLAYLN, MSANDLN, MCLAYLN
		27: gas_correction_eq5 [HydrocarbonInputsFifthEquationInputs]: RHOB_FLUID, NPHI_FLUID, CMATDCLLN, MMATDCLLN, RHOB_DRY_SILT, RHOB_DRY_CLAY, XMINHCORR_RIGHTLIMB, XMAXHCORR_RIGHTLIMB, XMINHCORR_LEFTLIMB, XMAXHCORR_LEFTLIMB 
		28: gas_correction_eq6 [HydrocarbonInputsSixthEquationInputs]: VSHGR, COR_LIMIT_MANUAL
		Output:
		- [number] [g/cc] rhobhc: Hydrocarbon corrected Bulk Density
		- [number] [v/v] nphihc: Hydrocarbon corrected Neutron Porosity
		- [number] [v/v] phit85: Gas Porosity
		- [number] [v/v] phit21: Gas Porosity (2/3*PHID+1/3*NPHI)
		- [number] [v/v] phitgm: Gaymard Porosity
		- [number] PHITDN: Porosity from Neutron Density
		- [number] RMF: Resistivity Mud Filtrate
		- [number] shl_n_d: HC Corrected Shale & Sand Line
		"""
	rhobhc = MissingValue
	nphihc = MissingValue
	phit85 = MissingValue
	phit21 = MissingValue
	phitgm = MissingValue
	SWA = MissingValue
	PHIDE = MissingValue
	PHITDN = MissingValue
	RHOMF = MissingValue
	RMF = MissingValue
	shl_n_d = MissingValue
	try:
		RMF = MFRES * (MFTEMP + 6.77) / (ZNTEMPUNIT + 6.77)
		MF_SAL = (MFRES * (MFTEMP + 6.77) / 83.77 /
				  2422) ** (-1.107297087808659)
	except:
		RMF = MissingValue
		MF_SAL = MissingValue

	if LITHMOD == 'CARB':
		rhob = rhobcc
		nphi = nphicc
	if MissingValue not in [MF_SAL, RHOREFMAT, rhob, nphi, rt, zn_m, zn_n]:
		RHOMF = 1 + 0.73 * (MF_SAL / 1000000)
		PHIDE = (RHOREFMAT - rhob) / (RHOREFMAT - RHOMF)
		PHITDN = ((2.71 - rhob) / (2.71 - RHOMF) + nphi) / 2
		phitgm = ((((2.71 - rhob) / (2.71 - RHOMF))
				  ** 2 + nphi ** 2) / 2) ** 0.5
		phit21 = 0.667 * (2.71 - rhob) / (2.71 - RHOMF) + 0.333 * nphi
		phit85 = 0.85 * (2.71 - rhob) / (2.71 - RHOMF)
		try:
			SWA = (znrw / rt / PHITDN ** zn_m) ** (1 / zn_n)
			SWA = limitValue(SWA, 0, 1)
		except:
			SWA = MissingValue

	# if HC_CORR flag == -2, user automatic correction (PHIX_METHOD)
	if gas_correction_eq2.znhcor == -2:
		COR_METHOD = "PHIX_METHOD"

	if COR_METHOD == 'STANDARD' or COR_METHOD == 'SECOND_METHOD':
		if MissingValue not in [RHO_GAS, RHO_OIL, RHOMF, MF_SAL, SHI]:
			HCA = (1.19 - 0.16 * MF_SAL / 1000000) * RHOMF - 1.33 * RHO_GAS
			HIHC = 9 * (4 - 2.5 * RHO_GAS) / (16 - 2.5 * RHO_GAS) * RHO_GAS
			if znogf == 2:
				HCA = (1.19 - 0.16 * MF_SAL / 1000000) * \
					RHOMF - 1.19 * RHO_OIL - 0.032
				HIHC = 9 * (4 - 2.5 * RHO_OIL) / (16 - 2.5 * RHO_OIL) * RHO_OIL
			HIW = RHOMF * (1 - MF_SAL / 1000000)
			HCB = 1 - HIHC / HIW
			HCSWH = SHI * HIHC + (1 - SHI) * HIW
			HCEXC = HCK * (1 - HCSWH) * (2 * PHITDN **
										 2 * HCSWH + 0.04 * PHITDN)
			DERHOB = HCA * PHITDN * SHI
			DENPHI = HCB * PHITDN * SHI + HCEXC
			rhobhc = rhob + DERHOB
			nphihc = nphi + DENPHI
			if LITHMOD == "SSC":
				shale_calculation = HydrocarbonCorrection(inputsEq1=gas_correction_eq1, inputsEq3=gas_correction_eq3)
				shl_n_d = shale_calculation.calculate_shale()
	elif COR_METHOD == 'EMPIRICAL' or COR_METHOD == 'DEFAULT':
		if MissingValue not in [SWA, SHI, NEUTRONFAC, rhob, nphi]:
			DERHOB = (1 - SWA) * SHI
			DENPHI = NEUTRONFAC * DERHOB
			rhobhc = rhob + DERHOB
			nphihc = nphi + DENPHI
			if LITHMOD == "SSC":
				shale_calculation = HydrocarbonCorrection(inputsEq1=gas_correction_eq1, inputsEq3=gas_correction_eq3)
				shl_n_d = shale_calculation.calculate_shale()
	elif COR_METHOD == 'FIX_ANGLE' or COR_METHOD == 'THIRD_METHOD':
		if MissingValue not in [rhob, nphi, DEGHCCOR]:
			rhobhc = rhob + SHI * sin(radians(DEGHCCOR))
			nphihc = nphi + SHI * cos(radians(DEGHCCOR))
			if LITHMOD == "SSC":
				shale_calculation = HydrocarbonCorrection(inputsEq1=gas_correction_eq1, inputsEq3=gas_correction_eq3)
				shl_n_d = shale_calculation.calculate_shale()
	elif COR_METHOD == "PHIX_METHOD":
		if MissingValue not in [rhob, nphi]:
			if LITHMOD == "SSC":
				HCA = (1.19 - 0.16 * MF_SAL / 1000000) * RHOMF - 1.33 * RHO_GAS
				HIHC = 9 * (4 - 2.5 * RHO_GAS) / (16 - 2.5 * RHO_GAS) * RHO_GAS
				if znogf == 2:
					HCA = (1.19 - 0.16 * MF_SAL / 1000000) * \
						RHOMF - 1.19 * RHO_OIL - 0.032
					HIHC = 9 * (4 - 2.5 * RHO_OIL) / (16 - 2.5 * RHO_OIL) * RHO_OIL
				HIW = RHOMF * (1 - MF_SAL / 1000000)
				HCB = 1 - HIHC / HIW

				gas_correction_eq2.HCA = HCA
				gas_correction_eq2.HCB = HCB
				gas_correction_eq2.phitgm = phitgm

				hydrocarbon_correction_calculation =  HydrocarbonCorrection(inputsEq1=gas_correction_eq1, inputsEq2=gas_correction_eq2, inputsEq3=gas_correction_eq3, inputsEq4=gas_correction_eq4, inputsEq5=gas_correction_eq5, inputsEq6=gas_correction_eq6)
				rhobhc, nphihc, shl_n_d = hydrocarbon_correction_calculation.calculate_fourth_method()
			else:
				tlDialog.critical(f"PHIX METHOD is not supported for CARB", "PHIX METHOD is not supported for CARB lithology model. Please select different method to compute hydrocarbon correction.")
				exit()
	return (
		rhobhc, nphihc, phit85, phit21, phitgm, PHITDN, RMF, shl_n_d)

def BH_CORRECTION(rhobfc, rhob, BH_CORR, SOURCE_SYN_LOG, dt, nphi, znsynrcl, znsynrsd, vshgr, BHCTYP, GRCLAYFRAC, GRSILTFRAC, GRSANDFRAC, CORR_RHOB_LOG, clayfrac, siltfrac, sandfrac, vshdrydn, EXTRHOBFLG):
	"""Bad hole corrections
		Inputs:
		1. rhobhc [number] [g/cc]: Hydrocarbon corrected Bulk Density
		2. rhob [number] [g/cc]: Bulk Density
		3. BH_CORR [string]: Do Bad Hole Correction [YES/NO]
		4. znsynrcl [g/cc]: Zoned Synthetic RHOB_CLAY
		5. znsynrsd [g/cc]: Zoned Synthetic RHOB Sand
		6. vshgr [v/v]: Shale volume from Gamma Ray
		7. BHCTYP [number]: Bad Hole Flag Type (relates to parameter BHCTYP*)
		8. GRCLAYFRAC [number] [v/v]: Clay fraction from Gamma Ray
		9. GRSILTFRAC [number] [v/v]: Silt fraction from Gamma Ray
		10. GRSANDFRAC [number] [v/v]: Sand fraction from Gamma Ray
		11. CORR_RHOB_LOG [number] [g/cc]: External Bulk Density, to use to correct when Bhcorrflag==2
		12. clayfrac [number] [v/v]: Clay volume fraction to be corrected
		13. siltfrac [number] [v/v]: Silt volume fraction to be corrected
		14. sandfrac [number] [v/v]: Sand volume fraction to be corrected
		Output:
		- [number] rhobfc: Mud Filtrate Density
		- [number] rhobbc: Borehole corrected Bulk Density
		- [number] clayfrac: Corrected clay fraction
		- [number] siltfrac: Corrected silt fraction
		- [number] sandfrac: Corrected sand fraction
		"""
	rhobbc = rhob
	synrhobgr = MissingValue
	dtrhobcon = MissingValue
	MRHOBSYN = znsynrcl - znsynrsd
	CRHOBSYN = znsynrsd
	if SOURCE_SYN_LOG == 'VSHGR':
		if MissingValue not in [MRHOBSYN, vshgr, CRHOBSYN]:
			synrhobgr = MRHOBSYN * vshgr + CRHOBSYN
	elif SOURCE_SYN_LOG == 'DT':
		if MissingValue not in [MRHOBSYN, dt, CRHOBSYN]:
			dtrhobcon = -0.021 * dt + 2.2
			synrhobgr = MRHOBSYN * dtrhobcon + CRHOBSYN
	elif SOURCE_SYN_LOG == 'NPHI':
		if MissingValue not in [MRHOBSYN, nphi, CRHOBSYN]:
			dtrhobcon = -2.9 * nphi + 0.96
			synrhobgr = MRHOBSYN * dtrhobcon + CRHOBSYN
	if BHCTYP == 1 or BHCTYP == 4:
		clayfrac = GRCLAYFRAC
		siltfrac = GRSILTFRAC
		sandfrac = GRSANDFRAC
		vshdrydn = vshgr
		rhobfc = synrhobgr
		rhobbc = synrhobgr
	elif BHCTYP == 2 and EXTRHOBFLG == 'YES':
		clayfrac = GRCLAYFRAC
		siltfrac = GRSILTFRAC
		sandfrac = GRSANDFRAC
		vshdrydn = vshgr
		rhobfc = CORR_RHOB_LOG
		rhobbc = CORR_RHOB_LOG
	elif BHCTYP == -1:
		clayfrac = MissingValue
		siltfrac = MissingValue
		sandfrac = MissingValue
		rhobfc = MissingValue
		rhobcc = MissingValue
	return (
		rhobfc, rhobbc, clayfrac, siltfrac, sandfrac, synrhobgr, vshdrydn)


def check_PERMEABILITY(PHIT, VCLW, VSILT):
	return isNotEmpty(PHIT) and isNotEmpty(VCLW) and isNotEmpty(VSILT)


def PERMEABILITY(choo_cons, PHIT, VCLW, VSILT, znagen, znaphit, znaclw, znasilt, rsvr_depthx, pobx, pfx, por_avgx, ZN_M, r_grainx, r_effx):
	"""Lithology from GR Calculation
		Inputs:
		 1. choo_cons [string]: YES or NO, Using Choo's Permeability Parameters         Output of PERM_ZONATION
		 2. PHIT_PERM [number]: Total Porosity
		 3. VCLW_PERM [number]: Volume of Wet Claystone
		 4. VSILT_PERM [number]: Volume of Dry Siltstone
		 5. znagen [number]: General Constant   Output of PERM_ZONATION
		 6. znaphit [number]: Constant for Porosity     Output of PERM_ZONATION
		 7. znaclw [number]: Constant for Clay  Output of PERM_ZONATION
		 8. znasilt [number]: Constant for Silt         Output of PERM_ZONATION
		 9. rsvr_depthx [number]: Reservoir Depth in TVD        Output of PERM_ZONATION
		 10. pobx [number]: Overburden Pressure Gradient        Output of PERM_ZONATION
		 11. pfx [number]: Formation Pressure Gradient  Output of PERM_ZONATION
		 12. por_avgx [number]: Average Porosity in Cleanest Sand       Output of PERM_ZONATION
		 13. ZN_M [number]: Cementation Factor M (M*)
		 14. r_grainx [number]: Dominant Grain Size in Cleanest Sand (from P50 of LPSA/SA)      Output of PERM_ZONATION
		 15. r_effx [number]: Dominant Pore Throat in Cleanest Sand (from HPMI)         Output of PERM_ZONATION
		Output:
		 - [number] PERM_CH: Permeability Estimation (Choo)
		"""
	PERM_CH = MissingValue
	if MissingValue in [PHIT, VCLW, VSILT]:
		return MissingValue
	if choo_cons == 'YES':
		nob_ch = rsvr_depthx * (pobx - pfx)
		alpha_ch = 2.71828 ** (nob_ch * 2e-05)
		b1 = 1 / (alpha_ch * por_avgx ** ZN_M)
		b2 = r_grainx / r_effx
		beta_ch = log10(b1) / log10(b2)
		znagen = r_grainx ** 2 / (8 * alpha_ch ** (2 / beta_ch)) / 100
		znaphit = (2 / beta_ch + 1) * ZN_M
	PHIT = limitValue(PHIT, 0, 1)
	VCLW = limitValue(VCLW, 0, 1)
	VSILT = limitValue(VSILT, 0, 1)
	PERM_CH = znagen * PHIT ** znaphit / \
		10 ** (znaclw * VCLW + znasilt * VSILT)
	if PERM_CH == 0.0:
		PERM_CH = 1e-05
	return PERM_CH


def ROCK_TYPING(ROCK_TYPING_METHOD, EXT_INDIC_LOG, CUT_OFF_ORDER, NZN_ROCKTP, NR_CUT_OFF, RT1_CUT_OFF, RT2_CUT_OFF, RT3_CUT_OFF, RT4_CUT_OFF, RT5_CUT_OFF, RT6_CUT_OFF, VCLW, VSILT, VSH_DN, VSHALE, VCOAL):
	"""Rock-Typing
		Inputs:
		 1. ROCK_TYPING_METHOD [string]: Method of Rock-Typing
		 2. EXT_INDIC_LOG [number]: External Rock-Type  Indicator (100% Sand = 0, 100% Shale = 1)
		 3. NZN_ROCKTP [number]: Number of Rock-Types (Reservoirs only)
		 4. NR_CUT_OFF [number]: CUT_OFF for RT#0 (Non-Reservoir)
		 5. RT1_CUT_OFF [number]: CUT_OFF for RT#1
		 6. RT2_CUT_OFF [number]: CUT_OFF for RT#2
		 7. RT3_CUT_OFF [number]: CUT_OFF for RT#3
		 8. RT4_CUT_OFF [number]: CUT_OFF for RT#4
		 9. RT5_CUT_OFF [number]: CUT_OFF for RT#5
		 10. RT6_CUT_OFF [number]: CUT_OFF for RT#6
		 11. VCLW [number]: Volume of Wet Claystone
		 12. VSILT [number]: Volume of Dry Siltstone
		 13. VSH_DN [number]: Volume of Shale (D-N)
		 14. VCOAL [number]: Coal Indicator
		Output:
		 - [number] ROCKTYPE: Rock Type Number
		"""
	ROCKTYPE = 0
	RTC = MissingValue
	DNSILTFRAC = MissingValue
	if (ROCK_TYPING_METHOD == 'VSH-DN') & (VSH_DN != MissingValue):
		DNSILTFRAC = VSH_DN
	elif (ROCK_TYPING_METHOD == 'VCLW') & (VCLW != MissingValue):
		DNSILTFRAC = VCLW
	elif (ROCK_TYPING_METHOD == 'VSHALE') & (VSHALE != MissingValue):
		DNSILTFRAC = VSHALE
	elif (ROCK_TYPING_METHOD == 'RTC<VCLW+0.5*VSILT>') & (VCLW != MissingValue or VSILT != MissingValue):
		RTC = VCLW + 0.5 * VSILT
		DNSILTFRAC = RTC
	elif ROCK_TYPING_METHOD == 'EXTERNAL':
		DNSILTFRAC = EXT_INDIC_LOG
	if CUT_OFF_ORDER == 'HIGH_TO_LOW':
		if RT1_CUT_OFF >= NR_CUT_OFF:
			RT1_CUT_OFF = 0
			NR_CUT_OFF = 0
		if RT2_CUT_OFF >= RT1_CUT_OFF:
			RT2_CUT_OFF = 0
		if RT3_CUT_OFF >= RT2_CUT_OFF:
			RT3_CUT_OFF = 0
		if RT4_CUT_OFF >= RT3_CUT_OFF:
			RT4_CUT_OFF = 0
		if RT5_CUT_OFF >= RT4_CUT_OFF:
			RT5_CUT_OFF = 0
		if RT6_CUT_OFF >= RT5_CUT_OFF:
			RT6_CUT_OFF = 0
		if DNSILTFRAC < NR_CUT_OFF and NZN_ROCKTP > 0:
			ROCKTYPE = 1
		if DNSILTFRAC < RT1_CUT_OFF and NZN_ROCKTP > 1:
			ROCKTYPE = 2
		if DNSILTFRAC < RT2_CUT_OFF and NZN_ROCKTP > 2:
			ROCKTYPE = 3
		if DNSILTFRAC < RT3_CUT_OFF and NZN_ROCKTP > 3:
			ROCKTYPE = 4
		if DNSILTFRAC < RT4_CUT_OFF and NZN_ROCKTP > 4:
			ROCKTYPE = 5
		if DNSILTFRAC < RT5_CUT_OFF and NZN_ROCKTP > 5:
			ROCKTYPE = 6
		if DNSILTFRAC < RT6_CUT_OFF and NZN_ROCKTP > 6:
			ROCKTYPE = 7
	else:
		if RT1_CUT_OFF <= NR_CUT_OFF:
			RT1_CUT_OFF = 1000
			NR_CUT_OFF = 1000
		if RT2_CUT_OFF <= RT1_CUT_OFF:
			RT2_CUT_OFF = 1000
		if RT3_CUT_OFF <= RT2_CUT_OFF:
			RT3_CUT_OFF = 1000
		if RT4_CUT_OFF <= RT3_CUT_OFF:
			RT4_CUT_OFF = 1000
		if RT5_CUT_OFF <= RT4_CUT_OFF:
			RT5_CUT_OFF = 1000
		if RT6_CUT_OFF <= RT5_CUT_OFF:
			RT6_CUT_OFF = 1000
		if DNSILTFRAC > NR_CUT_OFF and NZN_ROCKTP > 0:
			ROCKTYPE = 1
		if DNSILTFRAC > RT1_CUT_OFF and NZN_ROCKTP > 1:
			ROCKTYPE = 2
		if DNSILTFRAC > RT2_CUT_OFF and NZN_ROCKTP > 2:
			ROCKTYPE = 3
		if DNSILTFRAC > RT3_CUT_OFF and NZN_ROCKTP > 3:
			ROCKTYPE = 4
		if DNSILTFRAC > RT4_CUT_OFF and NZN_ROCKTP > 4:
			ROCKTYPE = 5
		if DNSILTFRAC > RT5_CUT_OFF and NZN_ROCKTP > 5:
			ROCKTYPE = 6
		if DNSILTFRAC > RT6_CUT_OFF and NZN_ROCKTP > 6:
			ROCKTYPE = 7
	if DNSILTFRAC == MissingValue:
		ROCKTYPE = MissingValue
	if VCOAL > 0.01:
		ROCKTYPE = 0
	return (
		ROCKTYPE, RTC)


def PERM_TRANSFORM(TRANSTYP, NZN_ROCKTPEXT, TRANS_A1, TRANS_B1, TRANS_A2, TRANS_B2, TRANS_A3, TRANS_B3, TRANS_A4, TRANS_B4, TRANS_A5, TRANS_B5, TRANS_A6, TRANS_B6, TRANS_A7, TRANS_B7, ROCKTYPE, PHIT):
	"""Rock-Typing
		Inputs:
		 1. TRANSTYP [string]: K-Transform Type
		 2. TRANS_A1 [number]: Coefficient A of K-Transform for RT1
		 2. TRANS_B1 [number]: Coefficient B of K-Transform for RT1
		 2. TRANS_A2 [number]: Coefficient A of K-Transform for RT2
		 2. TRANS_B2 [number]: Coefficient B of K-Transform for RT2
		 2. TRANS_A3 [number]: Coefficient A of K-Transform for RT3
		 2. TRANS_B3 [number]: Coefficient B of K-Transform for RT3
		 2. TRANS_A4 [number]: Coefficient A of K-Transform for RT4
		 2. TRANS_B4 [number]: Coefficient B of K-Transform for RT4
		 2. TRANS_A5 [number]: Coefficient A of K-Transform for RT5
		 2. TRANS_B5 [number]: Coefficient B of K-Transform for RT5
		 2. TRANS_A6 [number]: Coefficient A of K-Transform for RT6
		 2. TRANS_B6 [number]: Coefficient B of K-Transform for RT6
		 2. TRANS_A7 [number]: Coefficient A of K-Transform for RT7
		 2. ROCKTYPE [number]: Rocktype number
		 2. PHIT [number]: Total Porosity
		Output:
		 - [number] PERM_TRFM: Permeability from K-Transform
		"""
	PERM_TRFM = 0.001
	if PHIT > 0:
		if TRANSTYP == 'POWER':
			if ROCKTYPE == 1:
				PERM_TRFM = TRANS_A1 * PHIT ** TRANS_B1
			if NZN_ROCKTPEXT > 1:
				if ROCKTYPE == 2:
					PERM_TRFM = TRANS_A2 * PHIT ** TRANS_B2
			if NZN_ROCKTPEXT > 2:
				if ROCKTYPE == 3:
					PERM_TRFM = TRANS_A3 * PHIT ** TRANS_B3
			if NZN_ROCKTPEXT > 3:
				if ROCKTYPE == 4:
					PERM_TRFM = TRANS_A4 * PHIT ** TRANS_B4
			if NZN_ROCKTPEXT > 4:
				if ROCKTYPE == 5:
					PERM_TRFM = TRANS_A5 * PHIT ** TRANS_B5
			if NZN_ROCKTPEXT > 5:
				if ROCKTYPE == 6:
					PERM_TRFM = TRANS_A6 * PHIT ** TRANS_B6
			if NZN_ROCKTPEXT > 6:
				if ROCKTYPE == 7:
					PERM_TRFM = TRANS_A7 * PHIT ** TRANS_B7
		else:
			if ROCKTYPE == 1:
				PERM_TRFM = TRANS_A1 * exp(TRANS_B1 * PHIT)
			if NZN_ROCKTPEXT > 1:
				if ROCKTYPE == 2:
					PERM_TRFM = TRANS_A2 * exp(TRANS_B2 * PHIT)
			if NZN_ROCKTPEXT > 2:
				if ROCKTYPE == 3:
					PERM_TRFM = TRANS_A3 * exp(TRANS_B3 * PHIT)
			if NZN_ROCKTPEXT > 3:
				if ROCKTYPE == 4:
					PERM_TRFM = TRANS_A4 * exp(TRANS_B4 * PHIT)
			if NZN_ROCKTPEXT > 4:
				if ROCKTYPE == 5:
					PERM_TRFM = TRANS_A5 * exp(TRANS_B5 * PHIT)
			if NZN_ROCKTPEXT > 5:
				if ROCKTYPE == 6:
					PERM_TRFM = TRANS_A6 * exp(TRANS_B6 * PHIT)
			if NZN_ROCKTPEXT > 6:
				if ROCKTYPE == 7:
					PERM_TRFM = TRANS_A7 * exp(TRANS_B7 * PHIT)
	return PERM_TRFM


def SHF_COMPUTATION(unitsys, u, SHF_METHOD, PERM_SOURCE, EXT_PERM_LOG, PERM_CH, PERM_TRFM, RTC, DEPTH, SCOSTG, SCOSTO, PHIT, PHIE, VCLW, VSILT, BO_CHOO, gwc_depth, owc_depth, goc_depth, wtr_grad, oil_grad, gas_grad, ja, jb, ZA, ZB, CUTP1, TVDSS, CONTACT_DEPTH_SOURCE, SWIR_EQU, INPUT_LOG_FOR_SWIR, EXT_INPUT_LOG_FOR_SWIR, MAX_HEIGHT_OF_SWIR_PC):
	"""Rock-Typing
		Inputs:
		 1. DEPTH_UNIT [string]: Depth Unit (METRES, FEET)
		 2. SHF_METHOD [string]: SHF Methods
		 3. DEPTH [number]: MD Depth
		 4. SCOSTG [number]: G-W Sigma_Cos_Theta
		 5. SCOSTO [number]: O-W Sigma_Cos_Theta
		 6. perm_shf [number]: Permeability
		 7. PHIT_SHF [number]: Total Porosity
		 8. PHIE_SHF [number]: Effective Porosity
		 9. BO_CHOO [number]: Bo Constant of Choo's SHF ( 0.3 - 0.5 )
		 10. gwc_depth [number]: FWL [G-W]  (TVDSS)     Output of SHF_ZONATION
		 11. owc_depth [number]: FWL [O-W] (TVDSS)      Output of SHF_ZONATION
		 12. goc_depth [number]: GOC [G-O] (TVDSS)      Output of SHF_ZONATION
		 13. wtr_grad [number]: Water Gradient  Output of SHF_ZONATION
		 14. oil_grad [number]: Oil Gradient    Output of SHF_ZONATION
		 15. gas_grad [number]: Gas Gradient    Output of SHF_ZONATION
		 16. ja [number]: Coeff_A of J=A*SW**(-B)
		 17. jb [number]: Coeff_B of J=A*SW**(-B)
		 18. CUTP1 [number]: Permeability CUT_OFF
		 19. TVDSS [number]: TVDSS Depth
		 20. RTC [number]]: Rock Type Coeficient
		Output:
		 - [number] SW_SHF
		 - [number]: HT 
		  above FWL
		 - [number]: PC Calculated Capillary Pressure
		 - [number]: JFN
		"""
	
	
	convx = 3.281
	PC = 0
	HT = 0
	JFN = 0
	RQI = 0
	FZI = 0
	SWIRR = 1
	SWIRR_PC_MAX_OIL = 1
	SWIRR_PC_MAX_GAS = 1
	SW_SHF = 1
	scostx = 50
	perm_shf = 0
	root_k_phi = 3
	pc_max_gas = 0
	pc_max_oil = 0
	jfn_max_gas = 0
	jfn_max_oil = 0
	ift = 0
	if PERM_SOURCE == 'K-TRANSFORM':
		perm_shf = PERM_TRFM
	elif PERM_SOURCE == 'CHOO':
		perm_shf = PERM_CH
	elif PERM_SOURCE == 'EXTERNAL':
		perm_shf = EXT_PERM_LOG
	if CONTACT_DEPTH_SOURCE == 'DEPTH_TVDSS':
		if gwc_depth > 0:
			if TVDSS < gwc_depth:
				scostx = SCOSTG
				ift = SCOSTG
				HT = gwc_depth - TVDSS
				PC = convx * HT * (wtr_grad - gas_grad)
		elif owc_depth > 0:
			if TVDSS < owc_depth:
				scostx = SCOSTO
				ift = SCOSTO
				HT = owc_depth - TVDSS
				PC = convx * HT * (wtr_grad - oil_grad)
				if goc_depth > 0 and goc_depth < owc_depth:
					if TVDSS < goc_depth:
						HT = owc_depth - TVDSS
						scostx = SCOSTG
						ift = SCOSTG
						PC = convx * (owc_depth - goc_depth) * (wtr_grad - oil_grad) + \
							convx * (goc_depth - TVDSS) * (wtr_grad - gas_grad)
	elif gwc_depth > 0:
		if DEPTH < gwc_depth:
			scostx = SCOSTG
			ift = SCOSTG
			HT = gwc_depth - DEPTH
			PC = convx * HT * (wtr_grad - gas_grad)
	elif owc_depth > 0:
		if DEPTH < owc_depth:
			scostx = SCOSTO
			ift = SCOSTO
			HT = owc_depth - DEPTH
			PC = convx * HT * (wtr_grad - oil_grad)
			if goc_depth > 0 and goc_depth < owc_depth:
				if DEPTH < goc_depth:
					HT = owc_depth - DEPTH
					scostx = SCOSTG
					ift = SCOSTG
					PC = convx * (owc_depth - goc_depth) * (wtr_grad - oil_grad) + \
						convx * (goc_depth - DEPTH) * (wtr_grad - gas_grad)
	if (PHIT > 0) & (perm_shf > 0):
		root_k_phi = (perm_shf / PHIT) ** 0.5
		RQI = 0.0314 * root_k_phi
		FZI = RQI / (PHIT / (1 - PHIT))
		pc_max_gas = MAX_HEIGHT_OF_SWIR_PC * (wtr_grad - gas_grad)
		pc_max_oil = MAX_HEIGHT_OF_SWIR_PC * (wtr_grad - oil_grad)
		JFN = 0.2166 * PC / scostx * root_k_phi
		jfn_max_gas = 0.2166 * pc_max_gas / SCOSTG * root_k_phi
		jfn_max_oil = 0.2166 * pc_max_oil / SCOSTO * root_k_phi
		if SHF_METHOD == 'J-FUNC':
			if JFN <= 0:
				SW_SHF = 1
			else:
				SW_SHF = (JFN / ja) ** (1 / jb)
			if MAX_HEIGHT_OF_SWIR_PC > 0:
				SWIRR_PC_MAX_GAS = (jfn_max_gas / ja) ** (1 / jb)
				SWIRR_PC_MAX_OIL = (jfn_max_oil / ja) ** (1 / jb)
		elif SHF_METHOD == 'CHOO':
			if PHIE > 0:
				if JFN <= 0:
					SW_SHF = 1
				else:
					if PHIT == PHIE:
						PHIE = PHIT * 0.995
					swb_shf = abs(PHIT - PHIE) / PHIT
					b_star = BO_CHOO * (log10(1 + 1 / swb_shf) / 3)
					choo_up = (2 * BO_CHOO - 1) * \
						log10(1 + 1 / swb_shf) + log10(1 + swb_shf)
					SW_SHF = 10 ** choo_up / JFN ** b_star
		elif SHF_METHOD == 'SKELT-KA':
			a1_c1 = 17.619
			a1_c2 = 17.402
			a2_c1 = -1.2053
			a2_c2 = 5.9832
			a3_c1 = 0.3245
			a3_c2 = 0.4363
			a4_c1 = -0.7757
			a4_c2 = 3.1192
			if root_k_phi > 78:
				root_k_phi = 78
			a1_sk = a1_c1 * log(root_k_phi) + a1_c2
			a2_sk = a2_c1 * log(root_k_phi) + a2_c2
			a3_sk = a3_c1 * log(root_k_phi) + a3_c2
			a4_sk = a4_c1 * log(root_k_phi) + a4_c2
			a2_sk = limitValue(a2_sk, 0.1, 10000)
			a4_sk = limitValue(a4_sk, 0.01, 10000)
			aa = PC - a4_sk
			aa = limitValue(aa, 0, 10000)
			if aa > 0:
				a2_a4 = (a2_sk / aa) ** a3_sk
				SW_SHF = (100 - a1_sk * exp(-a2_a4)) / 100
			else:
				SW_SHF = 1.0
		elif SHF_METHOD == 'NORMALIZED-J':
			corrlog = 0
			if INPUT_LOG_FOR_SWIR == 'RQI':
				corrlog = RQI
			elif INPUT_LOG_FOR_SWIR == 'FZI':
				corrlog = FZI
			elif INPUT_LOG_FOR_SWIR == 'PERM':
				corrlog = perm_shf
			elif INPUT_LOG_FOR_SWIR == 'RTC':
				corrlog = RTC
			else:
				corrlog = EXT_INPUT_LOG_FOR_SWIR
			if SWIR_EQU == 'SWIR = A x (INPUT)^B':
				if corrlog == 0:
					corrlog = 0.0000001
				SWIRR = ZA * corrlog ** ZB
			elif SWIR_EQU == 'SWIR = A x e^(B.(INPUT))':
				SWIRR = ZA * exp(ZB * corrlog)
			elif SWIR_EQU == 'SWIR = A x log(INPUT)+B':
				SWIRR = ZA * log10(corrlog) + ZB
			elif SWIR_EQU == 'SWIR = A x ln(INPUT)+B':
				SWIRR = ZA * log(corrlog) + ZB
			if JFN <= 0:
				SW_SHF = 1
			else:
				SW_SHF = (JFN / ja) ** (1 / jb) * (1 - SWIRR) + SWIRR
			if MAX_HEIGHT_OF_SWIR_PC > 0:
				SWIRR_PC_MAX_GAS = (
					jfn_max_gas / ja) ** (1 / jb) * (1 - SWIRR) + SWIRR
				SWIRR_PC_MAX_OIL = (
					jfn_max_oil / ja) ** (1 / jb) * (1 - SWIRR) + SWIRR
	try:
		SW_SHF = limitValue(SW_SHF, 0, 1)
		SWIRR_PC_MAX_GAS = limitValue(SWIRR_PC_MAX_GAS, 0, 1)
		SWIRR_PC_MAX_OIL = limitValue(SWIRR_PC_MAX_OIL, 0, 1)
	except TypeError:
		SW_SHF = 1
		SWIRR_PC_MAX_GAS = 1
		SWIRR_PC_MAX_OIL = 1
	if perm_shf < CUTP1:
		SW_SHF = 1.0
		SWIRR_PC_MAX_GAS = 1
		SWIRR_PC_MAX_OIL = 1
	return (
		SW_SHF, HT, PC, JFN, RQI, FZI, SWIRR, SWIRR_PC_MAX_OIL, SWIRR_PC_MAX_GAS, ift)


def APPLY_OFFSET(RHOB, RHOB_ofs, RHOB_hi, RHOB_lo, RHOB_CL, RHOB_CL_ofs, RHOB_CL_hi, RHOB_CL_lo, RHOB_CL_max, RHOB_CL_hi_max, RHOB_CL_lo_max, RHOB_CL_min, RHOB_CL_hi_min, RHOB_CL_lo_min, NPHI, NPHI_ofs, NPHI_hi, NPHI_lo, NPHI_CL, NPHI_CL_ofs, NPHI_CL_hi, NPHI_CL_lo, NPHI_CL_max, NPHI_CL_hi_max, NPHI_CL_lo_max, NPHI_CL_min, NPHI_CL_hi_min, NPHI_CL_lo_min, GR, GR_ofs, GR_hi, GR_lo, GR_CL, GR_CL_ofs, GR_CL_hi, GR_CL_lo, GR_CL_max, GR_CL_hi_max, GR_CL_lo_max, GR_CL_min, GR_CL_hi_min, GR_CL_lo_min, GR_SD, GR_SD_ofs, GR_SD_hi, GR_SD_lo, GR_SD_max, GR_SD_hi_max, GR_SD_lo_max, GR_SD_min, GR_SD_hi_min, GR_SD_lo_min, SILTLINE_RATIO, SILTLINE_RATIO_ofs, SILTLINE_RATIO_max, SILTLINE_RATIO_min, RHODRYSL, RHODRYSL_ofs, RHODRYSL_max, RHODRYSL_min, RT, RT_ofs, RT_hi, RT_lo, M, M_ofs, M_max, M_min, N, N_ofs, N_max, N_min, NEUFAC, NEUFAC_ofs, NEUFAC_max, NEUFAC_min, SYNDENSD, SYNDENSD_ofs, SYNDENSD_max, SYNDENSD_min, SYNDENCL, SYNDENCL_ofs, SYNDENCL_max, SYNDENCL_min, RHOB_DRY_SAND, RHODRYSD_ofs, RHODRYSD_max, RHODRYSD_min, NPHI_DRY_SAND, NPHI_DRYSD_ofs, NPHI_DRYSD_max, NPHI_DRYSD_min, RHO_GAS, RHOGAS_ofs, RHOGAS_max, RHOGAS_min, RHO_OIL, RHOOIL_ofs, RHOOIL_max, RHOOIL_min, MFRES, MFRES_ofs, MFRES_max, MFRES_min, DEGHCCOR, DEGHCCOR_ofs, DEGHCCOR_max, DEGHCCOR_min):
	if RHOB_ofs >= 0.0:
		rhob = RHOB + RHOB_ofs * (RHOB_hi - RHOB)
		rhob_cl_max = RHOB_CL_max + RHOB_ofs * (RHOB_CL_hi_max - RHOB_CL_max)
		rhob_cl_min = RHOB_CL_min + RHOB_ofs * (RHOB_CL_hi_min - RHOB_CL_min)
		rhob_cly = RHOB_CL + RHOB_ofs * (RHOB_CL_hi - RHOB_CL)
		rhob_wcl = RHOB_CL + RHOB_ofs * (RHOB_CL_hi - RHOB_CL)
	else:
		rhob = RHOB + RHOB_ofs * (RHOB - RHOB_lo)
		rhob_cl_max = RHOB_CL_max + RHOB_ofs * (RHOB_CL_max - RHOB_CL_lo_max)
		rhob_cl_min = RHOB_CL_min + RHOB_ofs * (RHOB_CL_min - RHOB_CL_lo_min)
		rhob_cly = RHOB_CL + RHOB_ofs * (RHOB_CL - RHOB_CL_lo)
		rhob_wcl = RHOB_CL + RHOB_ofs * (RHOB_CL - RHOB_CL_lo)
	if RHOB_CL_ofs >= 0.0:
		rhob_cly = rhob_cly + RHOB_CL_ofs * (rhob_cl_max - rhob_cly)
		rhob_wcl = rhob_cly + RHOB_CL_ofs * (rhob_cl_max - rhob_cly)
	else:
		rhob_cly = rhob_cly + RHOB_CL_ofs * (rhob_cly - rhob_cl_min)
		rhob_wcl = rhob_cly + RHOB_CL_ofs * (rhob_cl_max - rhob_cly)
	if NPHI_ofs >= 0.0:
		nphi = NPHI + NPHI_ofs * (NPHI_hi - NPHI)
		nphicl_max = NPHI_CL_max + NPHI_ofs * (NPHI_CL_hi_max - NPHI_CL_max)
		nphicl_min = NPHI_CL_min + NPHI_ofs * (NPHI_CL_hi_min - NPHI_CL_min)
		nphi_cly = NPHI_CL + NPHI_ofs * (NPHI_CL_hi - NPHI_CL)
		nphi_wcl = NPHI_CL + NPHI_ofs * (NPHI_CL_hi - NPHI_CL)
	else:
		nphi = NPHI + NPHI_ofs * (NPHI - NPHI_lo)
		nphicl_max = NPHI_CL_max + NPHI_ofs * (NPHI_CL_max - NPHI_CL_lo_max)
		nphicl_min = NPHI_CL_min + NPHI_ofs * (NPHI_CL_min - NPHI_CL_lo_min)
		nphi_cly = NPHI_CL + NPHI_ofs * (NPHI_CL - NPHI_CL_lo)
		nphi_wcl = NPHI_CL + NPHI_ofs * (NPHI_CL - NPHI_CL_lo)
	if NPHI_CL_ofs >= 0.0:
		nphi_cly = nphi_cly + NPHI_CL_ofs * (nphicl_max - nphi_cly)
		nphi_wcl = nphi_cly + NPHI_CL_ofs * (nphicl_max - nphi_cly)
	else:
		nphi_cly = nphi_cly + NPHI_CL_ofs * (nphi_cly - nphicl_min)
		nphi_wcl = nphi_cly + NPHI_CL_ofs * (nphi_cly - nphicl_min)
	if GR_ofs >= 0.0:
		gr = GR + GR_ofs * (GR_hi - GR)
		gr_cl_max = GR_CL_max + GR_ofs * (GR_CL_hi_max - GR_CL_max)
		gr_cl_min = GR_CL_min + GR_ofs * (GR_CL_hi_min - GR_CL_min)
		gr_cl = GR_CL + GR_ofs * (GR_CL_hi - GR_CL)
		gr_cly = GR_CL + GR_ofs * (GR_CL_hi - GR_CL)
		gr_sd_max = GR_SD_max + GR_ofs * (GR_SD_hi_max - GR_SD_max)
		gr_sd_min = GR_SD_min + GR_ofs * (GR_SD_hi_min - GR_SD_min)
		gr_sd = GR_SD + GR_ofs * (GR_SD_hi - GR_SD)
		gr_cln = GR_SD + GR_ofs * (GR_SD_hi - GR_SD)
	else:
		gr = GR + GR_ofs * (GR - GR_lo)
		gr_cl_max = GR_CL_max + GR_ofs * (GR_CL_max - GR_CL_lo_max)
		gr_cl_min = GR_CL_min + GR_ofs * (GR_CL_min - GR_CL_lo_min)
		gr_cl = GR_CL + GR_ofs * (GR_CL - GR_CL_lo)
		gr_cly = GR_CL + GR_ofs * (GR_CL - GR_CL_lo)
		gr_sd_max = GR_SD_max + GR_ofs * (GR_SD_max - GR_SD_lo_max)
		gr_sd_min = GR_SD_min + GR_ofs * (GR_SD_min - GR_SD_lo_min)
		gr_sd = GR_SD + GR_ofs * (GR_SD - GR_SD_lo)
		gr_cln = GR_SD + GR_ofs * (GR_SD - GR_SD_lo)
	if GR_CL_ofs >= 0.0:
		gr_cl = gr_cl + GR_CL_ofs * (gr_cl_max - gr_cl)
		gr_cly = gr_cl + GR_CL_ofs * (gr_cl_max - gr_cl)
	else:
		gr_cl = gr_cl + GR_CL_ofs * (gr_cl - gr_cl_min)
		gr_cly = gr_cl + GR_CL_ofs * (gr_cl - gr_cl_min)
	if GR_SD_ofs >= 0.0:
		gr_sd = gr_sd + GR_SD_ofs * (gr_sd_max - gr_sd)
		gr_cln = gr_sd + GR_SD_ofs * (gr_sd_max - gr_sd)
	else:
		gr_sd = gr_sd + GR_SD_ofs * (gr_sd - gr_sd_min)
		gr_cln = gr_sd + GR_SD_ofs * (gr_sd - gr_sd_min)
	if SILTLINE_RATIO_ofs >= 0.0:
		siltline_ratio = SILTLINE_RATIO + SILTLINE_RATIO_ofs * \
			(SILTLINE_RATIO_max - SILTLINE_RATIO)
	else:
		siltline_ratio = SILTLINE_RATIO + SILTLINE_RATIO_ofs * \
			(SILTLINE_RATIO - SILTLINE_RATIO_min)
	if RHODRYSL_ofs >= 0.0:
		rhob_dry_slt = RHODRYSL + RHODRYSL_ofs * (RHODRYSL_max - RHODRYSL)
	else:
		rhob_dry_slt = RHODRYSL + RHODRYSL_ofs * (RHODRYSL - RHODRYSL_min)
	if RT_ofs >= 0.0:
		rt = RT + RT_ofs * (RT_hi - RT)
	else:
		rt = RT + RT_ofs * (RT - RT_lo)
	if M_ofs >= 0.0:
		m = M + M_ofs * (M_max - M)
	else:
		m = M + M_ofs * (M - M_min)
	if N_ofs >= 0.0:
		n = N + N_ofs * (N_max - N)
	else:
		n = N + N_ofs * (N - N_min)
	if NEUFAC_ofs >= 0.0:
		neufac = NEUFAC + NEUFAC_ofs * (NEUFAC_max - NEUFAC)
	else:
		neufac = NEUFAC + NEUFAC_ofs * (NEUFAC - NEUFAC_min)
	if SYNDENSD_ofs >= 0.0:
		syndensd = SYNDENSD + SYNDENSD_ofs * (SYNDENSD_max - SYNDENSD)
	else:
		syndensd = SYNDENSD + SYNDENSD_ofs * (SYNDENSD - SYNDENSD_min)
	if SYNDENCL_ofs >= 0.0:
		syndencl = SYNDENCL + SYNDENCL_ofs * (SYNDENCL_max - SYNDENCL)
	else:
		syndencl = SYNDENCL + SYNDENCL_ofs * (SYNDENCL - SYNDENCL_min)
	if RHODRYSD_ofs >= 0.0:
		rhob_dry_sand = RHOB_DRY_SAND + RHODRYSD_ofs * \
			(RHODRYSD_max - RHOB_DRY_SAND)
	else:
		rhob_dry_sand = RHOB_DRY_SAND + RHODRYSD_ofs * \
			(RHOB_DRY_SAND - RHODRYSD_min)
	if NPHI_DRYSD_ofs >= 0.0:
		nphi_dry_sand = NPHI_DRY_SAND + NPHI_DRYSD_ofs * \
			(NPHI_DRYSD_max - NPHI_DRY_SAND)
	else:
		nphi_dry_sand = NPHI_DRY_SAND + NPHI_DRYSD_ofs * \
			(NPHI_DRY_SAND - NPHI_DRYSD_min)
	if RHOGAS_ofs >= 0.0:
		rho_gas = RHO_GAS + RHOGAS_ofs * (RHOGAS_max - RHO_GAS)
	else:
		rho_gas = RHO_GAS + RHOGAS_ofs * (RHO_GAS - RHOGAS_min)
	if RHOOIL_ofs >= 0.0:
		rho_oil = RHO_OIL + RHOOIL_ofs * (RHOOIL_max - RHO_OIL)
	else:
		rho_oil = RHO_OIL + RHOOIL_ofs * (RHO_OIL - RHOOIL_min)
	if MFRES_ofs >= 0.0:
		mfres = MFRES + MFRES_ofs * (MFRES_max - MFRES)
	else:
		mfres = MFRES + MFRES_ofs * (MFRES - MFRES_min)
	if DEGHCCOR_ofs >= 0.0:
		deghccor = DEGHCCOR + DEGHCCOR_ofs * (DEGHCCOR_max - DEGHCCOR)
	else:
		deghccor = DEGHCCOR + DEGHCCOR_ofs * (DEGHCCOR - DEGHCCOR_min)
	return (rhob_cly, rhob_wcl, nphi_cly, nphi_wcl, gr_cl, gr_cly, gr_cln, gr_sd, siltline_ratio, rhob_dry_slt, m, n, neufac,
			syndensd, syndencl, rhob_dry_sand, nphi_dry_sand, rho_gas, rho_oil, mfres, deghccor)




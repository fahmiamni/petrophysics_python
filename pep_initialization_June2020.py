##import TechlogDialog

db.objectApplyModeChange(winId,1)

if pythonEditor:
	TechlogDialog.critical('PEP Error','This script should only be run within a workflow')
	exit(0)


#Get zone top / bottom details & Reference & Unit
w = DEPTH.wellName()
d = DEPTH.datasetName()
u = db.datasetPropertyUnit(w,d,"STEP")
Unit = db.variableUnit(w,d,DEPTH.variableName()) 
Reference = zoneRefFamily 
Top = zoneTopBottomDetail[0]+10
Bottom= zoneTopBottomDetail[1]-10
Middle= zoneTopBottomDetail[0]+(Bottom-Top)/2
Size = db.datasetSize(w,d)


#Define Raw output variables
VarInitRaw={}
VarInitRaw['GR']={"value":-9999,"Unit":"gAPI","Family":"Gamma Ray","Description":"Gamma Ray"}
VarInitRaw['GR_P']={"value":-9999,"Unit":"gAPI","Family":"Gamma Ray","Description":"Gamma Ray"}
VarInitRaw['CALI']={"value":-9999,"Unit":"in","Family":"Caliper","Description":"Caliper"}
VarInitRaw['CALI_P']={"value":-9999,"Unit":"in","Family":"Caliper","Description":"Caliper"}
VarInitRaw['NPHI']={"value":-9999,"Unit":"frac","Family":"Neutron Porosity","Description":"Neutron Porosity"}
VarInitRaw['NEUT']={"value":-9999,"Unit":"frac","Family":"Neutron Porosity","Description":"Neutron Porosity"}
VarInitRaw['NEUT_P']={"value":-9999,"Unit":"frac","Family":"Neutron Porosity","Description":"Neutron Porosity"}
VarInitRaw['RHOB']={"value":-9999,"Unit":"g/cm3","Family":"Bulk Density","Description":"Bulk Density"}
VarInitRaw['DENS_P']={"value":-9999,"Unit":"g/cm3","Family":"Bulk Density","Description":"Bulk Density"}
VarInitRaw['DENB']={"value":-9999,"Unit":"g/cm3","Family":"Bulk Density","Description":"Bulk Density"}
VarInitRaw['DRHO']={"value":-9999,"Unit":"g/cm3","Family":"Bulk Density Correction","Description":"Bulk Density Correction"}
VarInitRaw['DENSC_P']={"value":-9999,"Unit":"g/cm3","Family":"Bulk Density Correction","Description":"Bulk Density Correction"}
VarInitRaw['RT']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - True Formation","Description":"Resistivity - True Formation"}
VarInitRaw['RT_P']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - True Formation","Description":"Resistivity - True Formation"}
VarInitRaw['RXO']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Flushed Zone","Description":"Resistivity - Flushed Zone"}
VarInitRaw['RXO_P']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Flushed Zone","Description":"Resistivity - Flushed Zone"}
VarInitRaw['RDEP']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Deep","Description":"Resistivity - Deep"}
VarInitRaw['RDEP_P']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Deep","Description":"Resistivity - Deep"}
VarInitRaw['RD']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Deep","Description":"Resistivity - Deep"}
VarInitRaw['RDEEP']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Deep","Description":"Resistivity - Deep"}
VarInitRaw['RMED']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Medium","Description":"Resistivity - Medium"}
VarInitRaw['RMED_P']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Medium","Description":"Resistivity - Medium"}
VarInitRaw['RM']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Medium","Description":"Resistivity - Medium"}
VarInitRaw['RSHAL']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Shallow","Description":"Resistivity - Shallow"}
VarInitRaw['RSHAL_P']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Shallow","Description":"Resistivity - Shallow"}
VarInitRaw['RS']={"value":-9999,"Unit":"ohm.m","Family":"Resistivity - Shallow","Description":"Resistivity - Shallow"}
VarInitRaw['DT']={"value":-9999,"Unit":"us/ft","Family":"Compressional Slowness","Description":"Compressional Slowness"}
VarInitRaw['DTC']={"value":-9999,"Unit":"us/ft","Family":"Compressional Slowness","Description":"Compressional Slowness"}
VarInitRaw['DTC_P']={"value":-9999,"Unit":"us/ft","Family":"Compressional Slowness","Description":"Compressional Slowness"}
VarInitRaw['DTCOMP']={"value":-9999,"Unit":"us/ft","Family":"Compressional Slowness","Description":"Compressional Slowness"}
VarInitRaw['DTS']={"value":-9999,"Unit":"us/ft","Family":"Compressional Slowness","Description":"Compressional Slowness"}
VarInitRaw['DTS_P']={"value":-9999,"Unit":"us/ft","Family":"Compressional Slowness","Description":"Compressional Slowness"}
VarInitRaw['PEF']={"value":-9999,"Unit":"b/e","Family":"Photoelectric Factor","Description":"Photoelectric Factor"}
VarInitRaw['PEF_P']={"value":-9999,"Unit":"b/e","Family":"Photoelectric Factor","Description":"Photoelectric Factor"}
VarInitRaw['SP']={"value":-9999,"Unit":"mV","Family":"Spontaneous Potential","Description":"Spontaneous Potential"}
VarInitRaw['SP_P']={"value":-9999,"Unit":"mV","Family":"Spontaneous Potential","Description":"Spontaneous Potential"}

#Define final output variables
VarInitFinal={}
VarInitFinal['PHIT']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['PHIE']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['PERM_CH']={"value":-9999,"Unit":"mD","Family":""}
VarInitFinal['PERM_TRFM']={"value":-9999,"Unit":"mD","Family":""}
VarInitFinal['ROCKTYPE']={"value":-9999,"Unit":"unitless","Family":""}
VarInitFinal['SWE']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['SWT']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['SW_SHF']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VCALC']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VCLB']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VCLD']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VCLW']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VCOAL']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VDOLO']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VGAS']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VMIN1']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VMIN2']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VOIL']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VSAND']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VSILT']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VWATER']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VSHALE']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['VSH_DN']={"value":-9999,"Unit":"frac","Family":""}
VarInitFinal['RHOBHC']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitFinal['RHOBBC']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitFinal['RHOBFC']={"value":-9999,"Unit":"g/cm3","Family":""}

#Define secondary output variables
VarInitSecond={}
VarInitSecond['ZNRHOBCL']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['ZNNPHICL']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['ZNSLTLINRAT']={"value":-9999,"Unit":"%","Family":""}
VarInitSecond['ZNGRCL']={"value":-9999,"Unit":"gAPI","Family":""}
VarInitSecond['ZNGRSD']={"value":-9999,"Unit":"gAPI","Family":""}
VarInitSecond['ZN_M']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['ZN_N']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['ZNRW']={"value":-9999,"Unit":"ohm.m","Family":""}
VarInitSecond['ZNCWBGRAD']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['ZNSALWTR']={"value":-9999,"Unit":"ppm","Family":""}
VarInitSecond['ZNTEMP']={"value":-9999,"Unit":"degC","Family":""}
VarInitSecond['ZNOGF']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['ZNHCOR']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['ZNSYNRCL']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['ZNSYNRSD']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['ZNBHCOR']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['ZNCOALCUT']={"value":0.35,"Unit":"unitless","Family":""}
VarInitSecond['ZNSTRKCUT']={"value":0.65,"Unit":"unitless","Family":""}

VarInitSecond['VSHGR']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['RWAPP']={"value":-9999,"Unit":"ohm.m","Family":""}
VarInitSecond['QVSYN']={"value":-9999,"Unit":"meq/cm3","Family":""}
VarInitSecond['SWTU']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWT_ARC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHIHC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SYNRHOBGR']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['COALIND']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['LMSTRKIND']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['CLAYFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['DNQRTZFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['DNCALCFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['DNDOLOFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['DNMIN1FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PEFQRTZFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PEFCALCFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PEFDOLOFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PEFMIN1FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PDQRTZFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PDCALCFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PDDOLOFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PDMIN1FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MNQRTZFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MNCALCFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MNDOLOFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MNMIN1FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MNMIN2FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['BMOB']={"value":-9999,"Unit":"mS/m","Family":""}
VarInitSecond['BQV']={"value":-9999,"Unit":"mS/m","Family":""}
VarInitSecond['CALCFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['CLYSLTFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['CWAPP']={"value":-9999,"Unit":"mS/m","Family":""}
VarInitSecond['ZNCW']={"value":-9999,"Unit":"mS/m","Family":""}
VarInitSecond['DNLITH2FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['DNCLAYFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['DOLOFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MIN1FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MIN2FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MPLOT']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['PDLITH2FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PEFLITH2FRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['RHOBCC']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['NPHDRYCL']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHDRYSL']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHICC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHIHCPLOT']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHIHCPLOT_DRYCLS_CST']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHIHCPLOT_DRYSD_CST']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHIHCPLOT_DRYSLS_CST']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHIHCPLOT_FLUID_CST']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHIHCPLOT_WETCLS']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['MXPOINT']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['NXPOINT']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['MXPOINTPLOT']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['NXPOINTPLOT']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['PEFCC']={"value":-9999,"Unit":"b/e","Family":""}
VarInitSecond['PHIT21']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT85']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHITCLY']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHITGM']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['QRTZFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['RHOBHCPLOT']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHOBHCPLOT_DRYCLS_CST']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHOBHCPLOT_DRYSD_CST']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHOBHCPLOT_DRYSLS_CST']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHOBHCPLOT_FLUID_CST']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHOBHCPLOT_WETCLS_CST']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHODRYCL']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHODRYSL']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHOG']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['ROCAL']={"value":-9999,"Unit":"ohm.m","Family":""}
VarInitSecond['SANDFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SILTFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SNDSLTFRAC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWE_ARC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SXOHC']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['UCC']={"value":-9999,"Unit":"b/cm3","Family":""}
VarInitSecond['VCL_PHIT_RAT']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCOALINIT']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VQRTZ']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['ZNRSH']={"value":-9999,"Unit":"ohm.m","Family":""}
VarInitSecond['ZNRW77F']={"value":-9999,"Unit":"ohm.m","Family":""}
VarInitSecond['HT']={"value":-9999,"Unit":"ft","Family":""}
VarInitSecond['PC']={"value":-9999,"Unit":"psi","Family":""}
VarInitSecond['JFN']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['RQI']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['FZI']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['RTC']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['SWIRR']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWIRR_PC_MAX_GAS']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWIRR_PC_MAX_OIL']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['GRAIN_RAD']={"value":-9999,"Unit":"um","Family":""}
VarInitSecond['M_EXP']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['COMP_FAC']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['BO_CH']={"value":-9999,"Unit":"unitless","Family":""}
VarInitSecond['SCOSTH_O']={"value":-9999,"Unit":"dyne/cm","Family":""}
VarInitSecond['SCOSTH_G']={"value":-9999,"Unit":"dyne/cm","Family":""}
VarInitSecond['GR_LO']={"value":-9999,"Unit":"gAPI","Family":""}
VarInitSecond['GR_HI']={"value":-9999,"Unit":"gAPI","Family":""}
VarInitSecond['NPHI_LO']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['NPHI_HI']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT_D']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT_MAX']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT_MEAN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT_MIN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT_P1']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT_P2']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['PHIT_P3']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['RHOB_LO']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RHOB_HI']={"value":-9999,"Unit":"g/cm3","Family":""}
VarInitSecond['RT_HI']={"value":-9999,"Unit":"ohm.m","Family":""}
VarInitSecond['RT_LO']={"value":-9999,"Unit":"ohm.m","Family":""}
VarInitSecond['SWT_D']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWT_MAX']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWT_MEAN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWT_MIN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWT_P1']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWT_P2']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['SWT_P3']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCLW_D']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCLW_MAX']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCLW_MEAN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCLW_MIN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCLW_P1']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCLW_P2']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VCLW_P3']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VSILT_D']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VSILT_MAX']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VSILT_MEAN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VSILT_MIN']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VSILT_P1']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VSILT_P2']={"value":-9999,"Unit":"frac","Family":""}
VarInitSecond['VSILT_P3']={"value":-9999,"Unit":"frac","Family":""}

#Define zonation parameter sets
VarInitZonePar1={}
VarInitZonePar1["ZON_RHOB_CLY"]={"value":2.5,"Unit":"g/cm3","type":"checkshots",'varName':"VAR_RHOB_CLY"}
VarInitZonePar1["ZON_NPHI_CLY"]={"value":0.4,"Unit":"frac","type":"checkshots",'varName':"VAR_NPHI_CLY"}
VarInitZonePar1["ZON_SILTPOSRAT"]={"value":50,"Unit":"%","type":"checkshots",'varName':"VAR_SILTPOSRAT"}
VarInitZonePar1["ZON_GR_CLN"]={"value":30,"Unit":"gAPI","type":"checkshots","varName":"VAR_GR_CLN"}
VarInitZonePar1["ZON_GR_CLY"]={"value":150,"Unit":"gAPI","type":"checkshots","varName":"VAR_GR_CLY"}
VarInitZonePar1["ZON_RWF"]={"value":0.1,"Unit":"ohm.m","type":"checkshots",'varName':"VAR_RWF"}
VarInitZonePar1["ZON_SALW"]={"value":5000,"Unit":"ppm","type":"checkshots",'varName':"VAR_SALW"}
VarInitZonePar1["ZON_CWB_GRAD"]={"value":0,"Unit":"unitless","type":"checkshots",'varName':'VAR_CWB_GRAD'}
VarInitZonePar1["ZON_SYNDENSD"]={"value":2.3,"Unit":"g/cm3","type":"checkshots","varName":"VAR_SYNDENSD"}
VarInitZonePar1["ZON_SYNDENCL"]={"value":2.6,"Unit":"g/cm3","type":"checkshots","varName":"VAR_SYNDENCL"}
VarInitZonePar1["ZON_COALCUT"]={"value":0.35,"Unit":"unitless","type":"checkshots","varName":"VAR_COALCUT"}
VarInitZonePar1["ZON_LMSTRKCUT"]={"value":0.65,"Unit":"unitless","type":"checkshots","varName":"VAR_LMSTRKCUT"}

VarInitZonePar2={}
VarInitZonePar2["ZON_M"]={"value":1.85,"Unit":"unitless","type":"interval",'varName':"VAR_M"}
VarInitZonePar2["ZON_N"]={"value":1.85,"Unit":"unitless","type":"interval",'varName':"VAR_N"}
VarInitZonePar2["ZON_OGF"]={"value":1,"Unit":"unitless","type":"interval","varName":"VAR_OGF"}
VarInitZonePar2["ZON_HC_CORRECTION"]={"value":0,"Unit":"unitless","type":"interval",'varName':"VAR_HC_CORRECTION"}
VarInitZonePar2["ZON_BADHOLE"]={"value":0,"Unit":"unitless","type":"interval","varName":"VAR_BADHOLE"}



#Create empty "PEP" Dataset (with FINAL & SECONDARY Groups)
if db.datasetExists(w,"PEP_FINAL"):
	if db.datasetExists(w,"PEP") and not db.datasetExists(w,"GL_PEP"):
		db.datasetRename(w,"PEP","GL_PEP")

if not db.datasetExists(w,"PEP"):
	db.datasetDuplicate(w,d,w,"PEP")
	db.datasetGroupChange(w,"PEP",[])
	
	#Delete all variable in "PEP" Dataset except DEPTH variable
	for key in db.variableList(w,"PEP"):
		if db.variableFamily(w,"PEP",key) == "Measured Depth":
			db.variableRename(w,"PEP",key,"DEPTH")
			db.variableGroupChange(w,"PEP","DEPTH",["FINAL"])
		if (key!="DEPTH"):
			db.variableDelete(w,"PEP",key)
			
	#Create final and secondary output variables in "PEP" Dataset
	for var in VarInitFinal.keys():
		db.variableCreate(w,"PEP",var,1)
		db.variableUnitChange(w,"PEP",var,VarInitFinal[var]["Unit"])
		db.variableGroupChange(w,"PEP",var,['FINAL'])
		if var == "VWATER":
			db.variableSave(w,"PEP",var,None,"frac",[1]*Size)
	for var in VarInitSecond.keys():
		db.variableCreate(w,"PEP",var,1)
		db.variableUnitChange(w,"PEP",var,VarInitSecond[var]["Unit"])
		db.variableGroupChange(w,"PEP",var,['SECONDARY'])

for key in db.datasetPropertyList(w,"PEP"):
	db.datasetPropertyDelete(w,"PEP",key)



#Create empty "PEP_VAR_PAR" Dataset
if UseGraphicalParameterPicking=='YES':
	
	if not db.datasetExists(w,"PEP_VAR_PAR"):
		db.datasetDuplicate(w,d,w,"PEP_VAR_PAR")
		db.datasetGroupChange(w,"PEP_VAR_PAR",[])
		for key in db.datasetPropertyList(w,"PEP_VAR_PAR"):
			db.datasetPropertyDelete(w,"PEP_VAR_PAR",key)
				
		for key in db.variableList(w,"PEP_VAR_PAR"):
			if db.variableFamily(w,"PEP_VAR_PAR",key) != "Measured Depth":
				db.variableDelete(w,"PEP_VAR_PAR",key)
			else:
				db.variableRename(w,"PEP_VAR_PAR",key,"DEPTH")

		for key in VarInitZonePar1.keys():
			if not db.variableExists(w,"PEP_VAR_PAR",VarInitZonePar1[key]["varName"]):
				db.variableCreate(w,"PEP_VAR_PAR",VarInitZonePar1[key]["varName"],1)
				db.variableSave(w,"PEP_VAR_PAR",VarInitZonePar1[key]["varName"],None,VarInitZonePar1[key]['Unit'],[VarInitZonePar1[key]['value']]*Size)
				if VarInitZonePar1[key]["type"]=="interval":
					db.variableTypeChange(w,"PEP_VAR_PAR",VarInitZonePar1[key]["varName"],'BlockedCurve')

		for key in VarInitZonePar2.keys():
			if not db.variableExists(w,"PEP_VAR_PAR",VarInitZonePar2[key]["varName"]):
				db.variableCreate(w,"PEP_VAR_PAR",VarInitZonePar2[key]["varName"],1)
				db.variableSave(w,"PEP_VAR_PAR",VarInitZonePar2[key]["varName"],None,VarInitZonePar2[key]['Unit'],[VarInitZonePar2[key]['value']]*Size)
				if VarInitZonePar2[key]["type"]=="interval":
					db.variableTypeChange(w,"PEP_VAR_PAR",VarInitZonePar2[key]["varName"],'BlockedCurve')

		db.variableCreate(w,"PEP_VAR_PAR",'X_-0_5',1)
		db.variableSave(w,"PEP_VAR_PAR",'X_-0_5',"Element_Plot","unitless",[-0.5]*Size)
		db.variableCreate(w,"PEP_VAR_PAR",'X_+0_0',1)
		db.variableSave(w,"PEP_VAR_PAR",'X_+0_0',"Element_Plot","unitless",[0]*Size)
		db.variableCreate(w,"PEP_VAR_PAR",'X_+0_5',1)
		db.variableSave(w,"PEP_VAR_PAR",'X_+0_5',"Element_Plot","unitless",[0.5]*Size)
		db.variableCreate(w,"PEP_VAR_PAR",'X_+1_0',1)
		db.variableSave(w,"PEP_VAR_PAR",'X_+1_0',"Element_Plot","unitless",[1]*Size)
		db.variableCreate(w,"PEP_VAR_PAR",'X_+1_5',1)
		db.variableSave(w,"PEP_VAR_PAR",'X_+1_5',"Element_Plot","unitless",[1.5]*Size)
		db.variableCreate(w,"PEP_VAR_PAR",'X_+2_0',1)
		db.variableSave(w,"PEP_VAR_PAR",'X_+2_0',"Element_Plot","unitless",[2]*Size)



#Create empty "PEP_ZON_PAR" Dataset Group and its datasets
if UseGraphicalParameterPicking=='NO':

	#Create trend-line datasets
	for key in VarInitZonePar1.keys():
		if not db.datasetExists(w,key):
			db.datasetCreate(w,key,"DEPTH","Measured Depth",Unit,[Top,Middle,Bottom],'double')
			db.datasetTypeChange(w,key,VarInitZonePar1[key]['type'])
			db.variableCreate(w,key,key,1)
			db.variableSave(w,key,key,[],VarInitZonePar1[key]['Unit'],[VarInitZonePar1[key]['value'],VarInitZonePar1[key]['value'],VarInitZonePar1[key]['value']])
			if VarInitZonePar1[key]["type"]=="interval":
				db.variableTypeChange(w,key,key,'BlockedCurve')
			db.datasetGroupChange(w,key,["PEP_ZON_PAR"])

	#Create flag datasets
	for key in VarInitZonePar2.keys(): 
		if not db.datasetExists(w,key):
			db.datasetDuplicate(w,"PEP",w,key)
			db.datasetTypeChange(w,key,VarInitZonePar2[key]['type'])
			db.datasetGroupChange(w,key,["PEP_ZON_PAR"])
			for var in db.variableList(w,key):
				if (var!="DEPTH"):
					db.variableDelete(w,key,var)
			db.variableGroupChange(w,key,"DEPTH",[])
			db.variableCreate(w,key,key,1)
			db.variableSave(w,key,key,[],VarInitZonePar2[key]['Unit'],[VarInitZonePar2[key]['value']]*Size)
			if VarInitZonePar2[key]["type"]=="interval":
				db.variableTypeChange(w,key,key,'BlockedCurve')

	#Create Element-Plot dataset
	if not db.datasetExists(w,"ZU"):
		db.datasetDuplicate(w,"PEP",w,"ZU")
		db.datasetGroupChange(w,"ZU",["PEP_ZON_PAR"])
		for var in db.variableList(w,"ZU"):
			if (var!="DEPTH"):
				db.variableDelete(w,"ZU",var)
		db.variableGroupChange(w,"ZU","DEPTH",[])
		db.variableCreate(w,"ZU",'X_-0_5',1)
		db.variableSave(w,"ZU",'X_-0_5',"Element_Plot","unitless",[-0.5]*Size)
		db.variableCreate(w,"ZU",'X_+0_0',1)
		db.variableSave(w,"ZU",'X_+0_0',"Element_Plot","unitless",[0]*Size)
		db.variableCreate(w,"ZU",'X_+0_5',1)
		db.variableSave(w,"ZU",'X_+0_5',"Element_Plot","unitless",[0.5]*Size)
		db.variableCreate(w,"ZU",'X_+1_0',1)
		db.variableSave(w,"ZU",'X_+1_0',"Element_Plot","unitless",[1]*Size)
		db.variableCreate(w,"ZU",'X_+1_5',1)
		db.variableSave(w,"ZU",'X_+1_5',"Element_Plot","unitless",[1.5]*Size)
		db.variableCreate(w,"ZU",'X_+2_0',1)
		db.variableSave(w,"ZU",'X_+2_0',"Element_Plot","unitless",[2]*Size)



#Copy main input variables to "PEP" Dataset
for key in VarInitRaw.keys():
	if (d != "SSS"):
		if db.variableExists(w,d,key):
			if (key=="RHOB") or (key=="DENS_P")  or (key=="DENB"):
				NewKey="RHOB"
			elif (key=="NPHI") or (key=="NEUT_P") or (key=="NEUT"):
				NewKey="NPHI"
			elif (key=="GR") or (key=="GR_P"):
				NewKey="GR"
			elif (key=="PEF") or (key=="PEF_P"):
				NewKey="PEF"
			elif (key=="CALI") or (key=="CALI_P"):
				NewKey="CALI"
			elif (key=="RT") or (key=="RT_P"):
				NewKey="RT"
			elif (key=="RXO") or (key=="RXO_P"):
				NewKey="RXO"
			elif (key=="RDEP") or (key=="RDEP_P") or (key=="RD") or (key=="RDEEP"):
				NewKey="RDEP"
			elif (key=="RMED") or (key=="RMED_P") or (key=="RM"):
				NewKey="RMED"
			elif (key=="RSHAL") or (key=="RSHAL_P") or (key=="RS"):
				NewKey="RSHAL"
			elif (key=="DRHO") or (key=="DENSC_P"):
				NewKey="DRHO"
			elif (key=="DT") or (key=="DTC_P") or (key=="DTCOMP") or (key=="DTC"):
				NewKey="DTC"
			elif (key=="DTS") or (key=="DTS_P"):
				NewKey="DTS"
			elif (key=="SP") or (key=="SP_P"):
				NewKey="SP"
	
			db.variableDelete(w,"PEP",NewKey)
			db.variableCopy(w,d,key,"PEP",NewKey,['linear'])
			db.variableFamilyChange(w,"PEP",NewKey,VarInitRaw[NewKey]["Family"])
			if (db.variableUnit(w,"PEP",NewKey)!=MissingValue):
				db.variableUnitChange(w,"PEP",NewKey,VarInitRaw[NewKey]["Unit"])
			else:
				db.variableUnitConvert(w,"PEP",NewKey,VarInitRaw[NewKey]["Unit"])
			db.variableDescriptionChange(w,"PEP",NewKey,VarInitRaw[NewKey]["Description"])
			db.variableGroupChange(w,"PEP",NewKey,["FINAL"])



#Overwrite variables in "PEP" Dataset with variables from Geolog's SSS_FINAL Dataset
if (d == "SSS_FINAL") or (d == "CLIPS") or (d == "PEP_FINAL"):
	varVer = 0
	varNameNoVer = ""
	coalfg = 0
	for key in db.variableList(w,d):
		if (key!="DEPTH") and (key!="RHOB") and (key!="NPHI") and (key!="RT") and (key!="GR")\
		and (key!="DT") and (key!="PEF") and (key!="CALI") and (key!="RXO") and (key!="DRHO"):
			
			varTemp = db.variableNameWithoutVersion(key)
			
			if (db.variableExists(w,"PEP",varTemp)) or (varTemp=="COAL") or (varTemp=="FCOAL") or (varTemp=="COALF")\
			or (varTemp=="VCOA") or (varTemp=="VLIME") or (varTemp=="SWTF_WAXMAN") or (varTemp=="SWE_WAXMAN")\
			or (varTemp=="SWTF_DUALWATER") or (varTemp=="SWE_DUALWATER") or (varTemp=="SWTF_ARCHIE")\
			or (varTemp=="PERM_TRANSFORM") or (varTemp=="VWC") or (varTemp=="VDC") or (varTemp=="CLAY")\
			or (varTemp=="CLAY_WET") or (varTemp=="SAND") or (varTemp=="SILT") or (varTemp=="FACIES_GROUP"):
				
				if (varNameNoVer!=varTemp):
					varNameNoVer = varTemp
					varVer = db.variableVersion(key)
					
					if (varNameNoVer=="COAL") or (varNameNoVer=="COALF") or (varNameNoVer=="VCOA"):
						coalfg = 1
						varFamily = db.variableFamily(w,"PEP","VCOAL")
						varUnit = db.variableUnit(w,"PEP","VCOAL")
						varGroup = db.variableGroup(w,"PEP","VCOAL")
						varName = "VCOAL"
						keyfin = key
					elif (varNameNoVer=="FCOAL"):
						if (coalfg!=1):
							varFamily = db.variableFamily(w,"PEP","VCOAL")
							varUnit = db.variableUnit(w,"PEP","VCOAL")
							varGroup = db.variableGroup(w,"PEP","VCOAL")
							varName = "VCOAL"
							keyfin = key
						else:
							varName = ""
							keyfin = ""
					elif (varNameNoVer=="VLIME"):
						varFamily = db.variableFamily(w,"PEP","VCALC")
						varUnit = db.variableUnit(w,"PEP","VCALC")
						varGroup = db.variableGroup(w,"PEP","VCALC")
						varName = "VCALC"
						keyfin = key
					elif (varNameNoVer=="SWTF_WAXMAN" or varNameNoVer=="SWTF_DUALWATER"):
						varFamily = db.variableFamily(w,"PEP","SWT")
						varUnit = db.variableUnit(w,"PEP","SWT")
						varGroup = db.variableGroup(w,"PEP","SWT")
						varName = "SWT"
						keyfin = key
					elif (varNameNoVer=="SWE_WAXMAN" or varNameNoVer=="SWE_DUALWATER"):
						varFamily = db.variableFamily(w,"PEP","SWE")
						varUnit = db.variableUnit(w,"PEP","SWE")
						varGroup = db.variableGroup(w,"PEP","SWE")
						varName = "SWE"
						keyfin = key
					elif (varNameNoVer=="SWTF_ARCHIE"):
						varFamily = db.variableFamily(w,"PEP","SWT_ARC")
						varUnit = db.variableUnit(w,"PEP","SWT_ARC")
						varGroup = db.variableGroup(w,"PEP","SWT_ARC")
						varName = "SWT_ARC"
						keyfin = key
					elif (varNameNoVer=="PERM_TRANSFORM") or (varNameNoVer=="PERM"):
						varFamily = db.variableFamily(w,"PEP","PERM_TRFM")
						varUnit = db.variableUnit(w,"PEP","PERM_TRFM")
						varGroup = db.variableGroup(w,"PEP","PERM_TRFM")
						varName = "PERM_TRFM"
						keyfin = key
					elif (varNameNoVer=="VWC") or (varNameNoVer=="CLAY_WET"):
						varFamily = db.variableFamily(w,"PEP","VCLW")
						varUnit = db.variableUnit(w,"PEP","VCLW")
						varGroup = db.variableGroup(w,"PEP","VCLW")
						varName = "VCLW"
						keyfin = key
					elif (varNameNoVer=="VDC") or (varNameNoVer=="CLAY"):
						varFamily = db.variableFamily(w,"PEP","VCLD")
						varUnit = db.variableUnit(w,"PEP","VCLD")
						varGroup = db.variableGroup(w,"PEP","VCLD")
						varName = "VCLD"
						keyfin = key
					elif (varNameNoVer=="SAND"):
						varFamily = db.variableFamily(w,"PEP","VSAND")
						varUnit = db.variableUnit(w,"PEP","VSAND")
						varGroup = db.variableGroup(w,"PEP","VSAND")
						varName = "VSAND"
						keyfin = key
					elif (varNameNoVer=="SILT"):
						varFamily = db.variableFamily(w,"PEP","VSILT")
						varUnit = db.variableUnit(w,"PEP","VSILT")
						varGroup = db.variableGroup(w,"PEP","VSILT")
						varName = "VSILT"
						keyfin = key
					elif (varNameNoVer=="FACIES_GROUP"):
						varFamily = db.variableFamily(w,"PEP","ROCKTYPE")
						varUnit = db.variableUnit(w,"PEP","ROCKTYPE")
						varGroup = db.variableGroup(w,"PEP","ROCKTYPE")
						varName = "ROCKTYPE"
						keyfin = key
					else:
						varFamily = db.variableFamily(w,"PEP",varNameNoVer)
						varUnit = db.variableUnit(w,"PEP",varNameNoVer)
						varGroup = db.variableGroup(w,"PEP",varNameNoVer)
						varName = varNameNoVer
						keyfin = key
					
				elif (db.variableVersion(key)<varVer):
					varNameNoVer = ""	
				else:	
					varVer = db.variableVersion(key)	

				db.variableDelete(w,"PEP",varName)
				db.variableCopy(w,d,keyfin,"PEP",varName,['linear'])
				db.variableFamilyChange(w,"PEP",varName,varFamily)
				db.variableUnitChange(w,"PEP",varName,varUnit)
				db.variableGroupChange(w,"PEP",varName,varGroup)

	# Computation outside the LOOP (preferable), because the output needs to be saved to another dataset
	PHITValues = db.variableLoad(w,"PEP","PHIT")
	PHIEValues = db.variableLoad(w,"PEP","PHIE")
	SWTValues = db.variableLoad(w,"PEP","SWT")
	SWEValues = db.variableLoad(w,"PEP","SWE")
	VGASValues = db.variableLoad(w,"PEP","VGAS")
	VOILValues = db.variableLoad(w,"PEP","VOIL")
	VWATERValues = db.variableLoad(w,"PEP","PHIE")
	VCLBValues = db.variableLoad(w,"PEP","VCLB")
	VCLDValues = db.variableLoad(w,"PEP","VCLD")
	VCLWValues = db.variableLoad(w,"PEP","VCLW")
	VSILTValues = db.variableLoad(w,"PEP","VSILT")
	VSANDValues = db.variableLoad(w,"PEP","VSAND")
	VCALCValues = db.variableLoad(w,"PEP","VCALC")
	VDOLOValues = db.variableLoad(w,"PEP","VDOLO")
	VSHALEValues = db.variableLoad(w,"PEP","VSHALE")
	VCOALValues = db.variableLoad(w,"PEP","VCOAL")

	if db.variableExists(w,d,"VDOLO") :
		db.variableCopy(w,d,"VDOLO","PEP","VDOLO")
		VDOLOValues = db.variableLoad(w,"PEP","VDOLO")
	else:
		VDOLOValues = db.variableLoad(w,"PEP","PHIE")
		for i in range(len(VDOLOValues)):
			if (VDOLOValues[i]!=MissingValue):
				VDOLOValues[i] = 0

	if db.variableExists(w,d,"VLIME") :
		db.variableCopy(w,d,"VLIME","PEP","VLIME")
		VLIMEValues = db.variableLoad(w,"PEP","VLIME")
	else:
		VLIMEValues = db.variableLoad(w,"PEP","PHIE")
		for i in range(len(VLIMEValues)):
			if (VLIMEValues[i]!=MissingValue):
				VLIMEValues[i] = 0

	if db.variableExists(w,d,"VGAS"):
		db.variableCopy(w,d,"VGAS","PEP","VGAS")
		VGASValues = db.variableLoad(w,"PEP","VGAS")
	else:
		VGASValues = db.variableLoad(w,"PEP","PHIE")
		for i in range(len(VGASValues)):
			if (VGASValues[i]!=MissingValue):
				VGASValues[i] = 0
		
	if db.variableExists(w,d,"VOIL"):
		db.variableCopy(w,d,"VOIL","PEP","VOIL")
		VOILValues = db.variableLoad(w,"PEP","VOIL")
	else:
		VOILValues = db.variableLoad(w,"PEP","PHIE")
		for i in range(len(VOILValues)):
			if (VOILValues[i]!=MissingValue):
				VOILValues[i] = 0
		
	if db.variableExists(w,d,"VGAS_IR"):
		db.variableCopy(w,d,"VGAS_IR","PEP","VGAS_IR")
		VGASIRValues = db.variableLoad(w,"PEP","VGAS_IR")
		GasIrFlg = 1
	else:
		VGASIRValues = db.variableLoad(w,"PEP","PHIE")
		GasIrFlg = 0
		
	if db.variableExists(w,d,"VOIL_IR"):
		db.variableCopy(w,d,"VOIL_IR","PEP","VOIL_IR")
		VOILIRValues = db.variableLoad(w,"PEP","VOIL_IR")
		OilIrFlg = 1
	else:
		VOILIRValues = db.variableLoad(w,"PEP","PHIE")
		OilIrFlg = 0
		
	if db.variableExists(w,d,"BVW"):
		BVWValues = db.variableLoad(w,d,"BVW")
		for i in range(len(BVWValues)):
			VGASValues[i]=PHIEValues[i]-BVWValues[i]
	if db.variableExists(w,d,"BVW_G"):
		BVW_GValues = db.variableLoad(w,d,"BVW_G")
		for i in range(len(BVW_GValues)):
			VGASValues[i]=PHIEValues[i]-BVW_GValues[i]
	if db.variableExists(w,d,"BVW_O"):
		BVW_OValues = db.variableLoad(w,d,"BVW_O")
		for i in range(len(BVW_OValues)):
			VOILValues[i]=PHIEValues[i]-BVW_OValues[i]

	# Limit the values between 0 & 1
	for i in range(len(PHITValues)):
		if (PHIEValues[i]<0):
			PHIEValues[i]=0
		if (VGASValues[i]==MissingValue):
			VGASValues[i]=0
		if (VOILValues[i]==MissingValue):
			VOILValues[i]=0
		if (VGASIRValues[i]==MissingValue) or (GasIrFlg==0):
			VGASIRValues[i]=0
		if (VOILIRValues[i]==MissingValue) or (OilIrFlg==0):
			VOILIRValues[i]=0

		VGASValues[i]=VGASValues[i]+VGASIRValues[i]
		VOILValues[i]=VOILValues[i]+VOILIRValues[i]
		if (VCLWValues[i]>=0) and (VCLDValues[i]>=0):
			VCLBValues[i]=VCLWValues[i]-VCLDValues[i]

		# Compute final "VWATER"
		VWATERValues[i]=PHIEValues[i]-VGASValues[i]-VOILValues[i]

		# Compute final "SWE"
		if (PHIEValues[i]!=MissingValue):
			if (PHIEValues[i]!=0):
				SWEValues[i]=1-(1-SWTValues[i])*PHITValues[i]/PHIEValues[i]
			else:
				SWEValues[i]=1
			if (SWTValues[i]==MissingValue):
				SWEValues[i]=MissingValue

	# Perform coal flagging
			if (VCOALValues[i]>0):
				VCOALValues[i]=1
				PHITValues[i]=0
				PHIEValues[i]=0
				SWTValues[i]=1
				SWEValues[i]=1
				VGASValues[i]=0
				VOILValues[i]=0
				VWATERValues[i]=0
				VCLBValues[i]=0
				VCLDValues[i]=0
				VCLWValues[i]=0
				VSILTValues[i]=0
				VSANDValues[i]=0
				VCALCValues[i]=0
				VDOLOValues[i]=0
				VSHALEValues[i]=0

	print(db.variableSave(w,"PEP",PHIT.variableName(),PHIT.familyName(),PHIT.unitName(),PHITValues))
	print(db.variableSave(w,"PEP",PHIE.variableName(),PHIE.familyName(),PHIE.unitName(),PHIEValues))
	print(db.variableSave(w,"PEP",SWT.variableName(),SWT.familyName(),SWT.unitName(),SWTValues))
	print(db.variableSave(w,"PEP",SWE.variableName(),SWE.familyName(),SWE.unitName(),SWEValues))
	print(db.variableSave(w,"PEP",VGAS.variableName(),VGAS.familyName(),VGAS.unitName(),VGASValues))
	print(db.variableSave(w,"PEP",VOIL.variableName(),VOIL.familyName(),VOIL.unitName(),VOILValues))
	print(db.variableSave(w,"PEP",VWATER.variableName(),VWATER.familyName(),VWATER.unitName(),VWATERValues))
	print(db.variableSave(w,"PEP",VCLB.variableName(),VCLB.familyName(),VCLB.unitName(),VCLBValues))
	print(db.variableSave(w,"PEP",VCLD.variableName(),VCLD.familyName(),VCLD.unitName(),VCLDValues))
	print(db.variableSave(w,"PEP",VCLW.variableName(),VCLW.familyName(),VCLW.unitName(),VCLWValues))
	print(db.variableSave(w,"PEP",VSILT.variableName(),VSILT.familyName(),VSILT.unitName(),VSILTValues))
	print(db.variableSave(w,"PEP",VSAND.variableName(),VSAND.familyName(),VSAND.unitName(),VSANDValues))
	print(db.variableSave(w,"PEP",VCALC.variableName(),VCALC.familyName(),VCALC.unitName(),VCALCValues))
	print(db.variableSave(w,"PEP",VDOLO.variableName(),VDOLO.familyName(),VDOLO.unitName(),VDOLOValues))
	print(db.variableSave(w,"PEP",VSHALE.variableName(),VSHALE.familyName(),VSHALE.unitName(),VSHALEValues))
	print(db.variableSave(w,"PEP",VCOAL.variableName(),VCOAL.familyName(),VCOAL.unitName(),VCOALValues))

	db.variableDelete(w,"PEP","VGAS_IR")
	db.variableDelete(w,"PEP","VOIL_IR")
	db.variableDescriptionChange(w,"PEP","VWATER","Water Volume Fraction")
	db.variableGroupChange(w,"PEP","VWATER",["FINAL"])
	db.variableGroupChange(w,"PEP","VLIME",["FINAL"])
	db.variableGroupChange(w,"PEP","VDOLO",["FINAL"])
	db.variableGroupChange(w,"PEP","VGAS",["FINAL"])
	db.variableGroupChange(w,"PEP","VOIL",["FINAL"])


	#Overwrite variables in "PEP" Dataset with variables from Geolog's "SSS" Dataset
	if db.datasetExists(w,"SSS"):
		varVer = 0
		varNameNoVer = ""
		for key in db.variableList(w,"SSS"):
			varTemp = db.variableNameWithoutVersion(key)
			
			if (varTemp=="VSH_DN") or (varTemp=="ZNRHOBCL") or (varTemp=="ZNNPHICL") or (varTemp=="ZNGRCL")\
			or (varTemp=="ZNGRSD") or (varTemp=="M_STAR") or (varTemp=="TEMP_GRAD") or (varTemp=="RWF_FLAG")\
			or (varTemp=="CWB_GRAD_FLAG") or (varTemp=="RHOB_SYN_CL") or (varTemp=="RHOB_SYN_SD")	or (varTemp=="HYDROCARBON_FLAG")\
			or (varTemp=="HC_TYPE_FLAG") or (varTemp=="HC_CORRECTION_FLAG") or (varTemp=="BADHOLE_FLAG") or (varTemp=="SYN_RHOB"):

				if (varNameNoVer!=varTemp):
					varNameNoVer = varTemp
					varVer = db.variableVersion(key)
					
					if (varNameNoVer=="RWF_FLAG"):
						varFamily = db.variableFamily(w,"PEP","ZNRW")
						varUnit = db.variableUnit(w,"PEP","ZNRW")
						varGroup = db.variableGroup(w,"PEP","ZNRW")
						varName = "ZNRW"
					elif (varNameNoVer=="CWB_GRAD_FLAG"):
						varFamily = db.variableFamily(w,"PEP","ZNCWBGRAD")
						varUnit = db.variableUnit(w,"PEP","ZNCWBGRAD")
						varGroup = db.variableGroup(w,"PEP","ZNCWBGRAD")
						varName = "ZNCWBGRAD"
					elif (varNameNoVer=="TEMP_GRAD"):
						varFamily = db.variableFamily(w,"PEP","ZNTEMP")
						varUnit = db.variableUnit(w,"PEP","ZNTEMP")
						varGroup = db.variableGroup(w,"PEP","ZNTEMP")
						varName = "ZNTEMP"
					elif (varNameNoVer=="RHOB_SYN_CL"):
						varFamily = db.variableFamily(w,"PEP","ZNSYNRCL")
						varUnit = db.variableUnit(w,"PEP","ZNSYNRCL")
						varGroup = db.variableGroup(w,"PEP","ZNSYNRCL")
						varName = "ZNSYNRCL"
					elif (varNameNoVer=="RHOB_SYN_SD"):
						varFamily = db.variableFamily(w,"PEP","ZNSYNRSD")
						varUnit = db.variableUnit(w,"PEP","ZNSYNRSD")
						varGroup = db.variableGroup(w,"PEP","ZNSYNRSD")
						varName = "ZNSYNRSD"
					elif (varNameNoVer=="HYDROCARBON_FLAG") or (varNameNoVer=="HC_TYPE_FLAG"):
						varFamily = db.variableFamily(w,"PEP","ZNOGF")
						varUnit = db.variableUnit(w,"PEP","ZNOGF")
						varGroup = db.variableGroup(w,"PEP","ZNOGF")
						varName = "ZNOGF"	
					elif (varNameNoVer=="HC_CORRECTION_FLAG"):
						varFamily = db.variableFamily(w,"PEP","ZNHCOR")
						varUnit = db.variableUnit(w,"PEP","ZNHCOR")
						varGroup = db.variableGroup(w,"PEP","ZNHCOR")
						varName = "ZNHCOR"
					elif (varNameNoVer=="BADHOLE_FLAG"):
						varFamily = db.variableFamily(w,"PEP","ZNBHCOR")
						varUnit = db.variableUnit(w,"PEP","ZNBHCOR")
						varGroup = db.variableGroup(w,"PEP","ZNBHCOR")
						varName = "ZNBHCOR"
					elif (varNameNoVer=="SYN_RHOB"):
						varFamily = db.variableFamily(w,"PEP","SYNRHOBGR")
						varUnit = db.variableUnit(w,"PEP","SYNRHOBGR")
						varGroup = db.variableGroup(w,"PEP","SYNRHOBGR")
						varName = "SYNRHOBGR"
					elif (varNameNoVer=="M_STAR"):
						varFamily = db.variableFamily(w,"PEP","ZN_M")
						varUnit = db.variableUnit(w,"PEP","ZN_M")
						varGroup = db.variableGroup(w,"PEP","ZN_M")
						varName = "ZN_M"
					else:
						varFamily = db.variableFamily(w,"PEP",varNameNoVer)
						varUnit = db.variableUnit(w,"PEP",varNameNoVer)
						varGroup = db.variableGroup(w,"PEP",varNameNoVer)
						varName = varNameNoVer
						
				elif (db.variableVersion(key)<varVer):
					varNameNoVer = ""	
				else:
					varVer = db.variableVersion(key)	
						
				db.variableDelete(w,"PEP",varName)
				db.variableResampling(w,"SSS",key,"PEP",varName,'automatic',0.5)
				db.variableFamilyChange(w,"PEP",varName,varFamily)
				db.variableUnitChange(w,"PEP",varName,varUnit)
				db.variableGroupChange(w,"PEP",varName,varGroup)

		ZNHCORValues = db.variableLoad(w,"PEP","ZNHCOR")
		for i in range(len(ZNHCORValues)):
			if (ZNHCORValues[i]<=-2) and (ZNHCORValues[i]!=-9999):
				ZNHCORValues[i]=0.5
		print(db.variableSave(w,"PEP",ZNHCOR.variableName(),ZNHCOR.familyName(),ZNHCOR.unitName(),ZNHCORValues))

		ZNBHCORValues = db.variableLoad(w,"PEP","ZNBHCOR")
		for i in range(len(ZNBHCORValues)):
			if (ZNBHCORValues[i]>0):
				ZNBHCORValues[i]=1
		print(db.variableSave(w,"PEP",ZNBHCOR.variableName(),ZNBHCOR.familyName(),ZNBHCOR.unitName(),ZNBHCORValues))

		SWTValues = db.variableLoad(w,"PEP","SWT")
		PHITValues = db.variableLoad(w,"PEP","PHIT")
		VGASValues = db.variableLoad(w,"PEP","VGAS")
		VOILValues = db.variableLoad(w,"PEP","VOIL")
		VWATERValues = db.variableLoad(w,"PEP","VWATER")
		ZNOGFValues = db.variableLoad(w,"PEP","ZNOGF")
		for i in range(len(ZNOGFValues)):
		
			if (ZNOGFValues[i]==3):
				ZNOGFValues[i]=1
			if (ZNOGFValues[i]==4):
				ZNOGFValues[i]=2
			if (ZNOGFValues[i]==1):
				VGASValues[i]=(1-SWTValues[i])*PHITValues[i]
			if (ZNOGFValues[i]==2):
				VOILValues[i]=(1-SWTValues[i])*PHITValues[i]
		print(db.variableSave(w,"PEP",ZNOGF.variableName(),ZNOGF.familyName(),ZNOGF.unitName(),ZNOGFValues))
		print(db.variableSave(w,"PEP",VGAS.variableName(),VGAS.familyName(),VGAS.unitName(),VGASValues))
		print(db.variableSave(w,"PEP",VOIL.variableName(),VOIL.familyName(),VOIL.unitName(),VOILValues))

		# Copy some PEP variables to PEP_VAR_PAR dataset 
		if UseGraphicalParameterPicking=='YES':
			db.variableDelete(w,"PEP_VAR_PAR","VAR_OGF")
			db.variableCopy(w,"PEP","ZNOGF","PEP_VAR_PAR","VAR_OGF",['linear'])
			db.variableGroupChange(w,"PEP_VAR_PAR","VAR_OGF",[])
			db.variableDelete(w,"PEP_VAR_PAR","VAR_HC_CORRECTION")
			db.variableCopy(w,"PEP","ZNHCOR","PEP_VAR_PAR","VAR_HC_CORRECTION",['linear'])
			db.variableGroupChange(w,"PEP_VAR_PAR","VAR_HC_CORRECTION",[])
			db.variableDelete(w,"PEP_VAR_PAR","VAR_BADHOLE")
			db.variableCopy(w,"PEP","ZNBHCOR","PEP_VAR_PAR","VAR_BADHOLE",['linear'])
			db.variableGroupChange(w,"PEP_VAR_PAR","VAR_BADHOLE",[])


	#Overwrite variables in "PEP" Dataset with variables from Geolog's "GL_PEP" Dataset
	if db.datasetExists(w,"GL_PEP"):
		varVer = 0
		varNameNoVer = ""
		for key in db.variableList(w,"GL_PEP"):
			varTemp = db.variableNameWithoutVersion(key)
			
			if (varTemp=="ZNRHOBCL") or (varTemp=="ZNNPHICL")  or (varTemp=="ZNDEGSILT") or (varTemp=="ZNGRCL")\
			or (varTemp=="ZNGRSD") or (varTemp=="VSH_DN") or (varTemp=="VSHGR") or (varTemp=="ZNRW") or (varTemp=="ZNCWBGRAD")\
			or (varTemp=="ZNSALWTR") or (varTemp=="ZNTEMP") or (varTemp=="MX") or (varTemp=="NX") or (varTemp=="QVSYN")\
			or (varTemp=="SWTU") or (varTemp=="SWT_ARC") or (varTemp=="ZNOGF") or (varTemp=="ZNHCOR") or (varTemp=="ZNSYNRCL")\
			or (varTemp=="ZNSYNRSD") or (varTemp=="SYNRHOBGR") or (varTemp=="BHCORFLG") or (varTemp=="ZNCOALCUT")\
			or (varTemp=="COALIND") or (varTemp=="ZNSTRKCUT") or (varTemp=="LMSTRKIND"):

				if (varNameNoVer!=varTemp):
					varNameNoVer = varTemp
					varVer = db.variableVersion(key)
					
					if (varNameNoVer=="ZNDEGSILT"):
						varFamily = db.variableFamily(w,"PEP","ZNSLTLINRAT")
						varUnit = db.variableUnit(w,"PEP","ZNSLTLINRAT")
						varGroup = db.variableGroup(w,"PEP","ZNSLTLINRAT")
						varName = "ZNSLTLINRAT"
					elif (varNameNoVer=="MX"):
						varFamily = db.variableFamily(w,"PEP","ZN_M")
						varUnit = db.variableUnit(w,"PEP","ZN_M")
						varGroup = db.variableGroup(w,"PEP","ZN_M")
						varName = "ZN_M"
					elif (varNameNoVer=="NX"):
						varFamily = db.variableFamily(w,"PEP","ZN_N")
						varUnit = db.variableUnit(w,"PEP","ZN_N")
						varGroup = db.variableGroup(w,"PEP","ZN_N")
						varName = "ZN_N"
					elif (varNameNoVer=="BHCORFLG"):
						varFamily = db.variableFamily(w,"PEP","ZNBHCOR")
						varUnit = db.variableUnit(w,"PEP","ZNBHCOR")
						varGroup = db.variableGroup(w,"PEP","ZNBHCOR")
						varName = "ZNBHCOR"
					else:
						varFamily = db.variableFamily(w,"PEP",varNameNoVer)
						varUnit = db.variableUnit(w,"PEP",varNameNoVer)
						varGroup = db.variableGroup(w,"PEP",varNameNoVer)
						varName = varNameNoVer
						
				elif (db.variableVersion(key)<varVer):
					varNameNoVer = ""	
				else:
					varVer = db.variableVersion(key)	
						
				db.variableDelete(w,"PEP",varName)
				db.variableResampling(w,"GL_PEP",key,"PEP",varName,'automatic',0.5)
				db.variableFamilyChange(w,"PEP",varName,varFamily)
				db.variableUnitChange(w,"PEP",varName,varUnit)
				db.variableGroupChange(w,"PEP",varName,varGroup)

		ZNSLTLINRATValues = db.variableLoad(w,"PEP","ZNSLTLINRAT")
		for i in range(len(ZNSLTLINRATValues)):
			ZNSLTLINRATValues[i]=ZNSLTLINRATValues[i]*100
		print(db.variableSave(w,"PEP",ZNSLTLINRAT.variableName(),ZNSLTLINRAT.familyName(),ZNSLTLINRAT.unitName(),ZNSLTLINRATValues))

		# Copy some PEP variables to PEP_VAR_PAR dataset 
		if UseGraphicalParameterPicking=='YES':
			db.variableDelete(w,"PEP_VAR_PAR","VAR_OGF")
			db.variableCopy(w,"PEP","ZNOGF","PEP_VAR_PAR","VAR_OGF",['linear'])
			db.variableGroupChange(w,"PEP_VAR_PAR","VAR_OGF",[])
			db.variableDelete(w,"PEP_VAR_PAR","VAR_HC_CORRECTION")
			db.variableCopy(w,"PEP","ZNHCOR","PEP_VAR_PAR","VAR_HC_CORRECTION",['linear'])
			db.variableGroupChange(w,"PEP_VAR_PAR","VAR_HC_CORRECTION",[])
			db.variableDelete(w,"PEP_VAR_PAR","VAR_BADHOLE")
			db.variableCopy(w,"PEP","ZNBHCOR","PEP_VAR_PAR","VAR_BADHOLE",['linear'])
			db.variableGroupChange(w,"PEP_VAR_PAR","VAR_BADHOLE",[])



#Copy and overwrite ZON_PAR datasets with datasets from Geolog's PCSB_SSS "zonation" datasets
if UseGraphicalParameterPicking=='NO':
	if (d == "SSS_FINAL"):
		if db.datasetExists(w,'BADHOLE'):	
			db.datasetDelete(w,'ZON_BADHOLE')	
			db.datasetDuplicate(w,'BADHOLE',w,'ZON_BADHOLE')
			ZNBHCORValues = db.variableLoad(w,'ZON_BADHOLE','INTERVAL')
			for i in range(len(ZNBHCORValues)):
				if (ZNBHCORValues[i]>0):
					ZNBHCORValues[i]=1
			print(db.variableSave(w,'ZON_BADHOLE',INTERVAL.variableName(),INTERVAL.familyName(),INTERVAL.unitName(),ZNBHCORValues))
		if db.datasetExists(w,'COAL'):	
			db.datasetDelete(w,'ZON_COALFLG')	
			db.datasetDuplicate(w,'COAL',w,'ZON_COALFLG')
		if db.datasetExists(w,'RWF'):	
			db.datasetDelete(w,'ZON_RWF')	
			db.datasetDuplicate(w,'RWF',w,'ZON_RWF')
		if db.datasetExists(w,'CWB_GRAD'):	
			db.datasetDelete(w,'ZON_CWB_GRAD')	
			db.datasetDuplicate(w,'CWB_GRAD',w,'ZON_CWB_GRAD')
		if db.datasetExists(w,'DEGFLSLT'):	
			db.datasetDelete(w,'ZON_DEGFLSLT')	
			db.datasetDuplicate(w,'DEGFLSLT',w,'ZON_DEGFLSLT')
		if db.datasetExists(w,'RHOB_CLY_ZONE'):	
			db.datasetDelete(w,'ZON_RHOB_CLY')	
			db.datasetDuplicate(w,'RHOB_CLY_ZONE',w,'ZON_RHOB_CLY')
		if db.datasetExists(w,'NPHI_CLY_ZONE'):	
			db.datasetDelete(w,'ZON_NPHI_CLY')	
			db.datasetDuplicate(w,'NPHI_CLY_ZONE',w,'ZON_NPHI_CLY')
		if db.datasetExists(w,'HC_TYPE'):	
			db.datasetDelete(w,'ZON_OGF')	
			db.datasetDuplicate(w,'HC_TYPE',w,'ZON_OGF')
		if db.datasetExists(w,'NEUTRON_FACTOR'):	
			db.datasetDelete(w,'ZON_NEUFAC')	
			db.datasetDuplicate(w,'NEUTRON_FACTOR',w,'ZON_NEUFAC')
		if db.datasetExists(w,'RHOB_SYN_CL'):	
			db.datasetDelete(w,'ZON_SYNDENCL')	
			db.datasetDuplicate(w,'RHOB_SYN_CL',w,'ZON_SYNDENCL')
		if db.datasetExists(w,'RHOB_SYN_SD'):	
			db.datasetDelete(w,'ZON_SYNDENSD')	
			db.datasetDuplicate(w,'RHOB_SYN_SD',w,'ZON_SYNDENSD')
		if db.datasetExists(w,'HC_CORRECTION'):	
			db.datasetDelete(w,'ZON_HC_CORRECTION')	
			db.datasetDuplicate(w,'HC_CORRECTION',w,'ZON_HC_CORRECTION')
		if db.datasetExists(w,'M'):	
			db.datasetDelete(w,'ZON_M')	
			db.datasetDuplicate(w,'M',w,'ZON_M')
		if db.datasetExists(w,'GR_CL_ZONE'):	
			db.datasetDelete(w,'ZON_GR_CL')	
			db.datasetDelete(w,'ZON_GR_CLY')	
			db.datasetDuplicate(w,'GR_CL_ZONE',w,'ZON_GR_CL')
			db.datasetDuplicate(w,'GR_CL_ZONE',w,'ZON_GR_CLY')
		if db.datasetExists(w,'GR_SD_ZONE'):	
			db.datasetDelete(w,'ZON_GR_SD')	
			db.datasetDelete(w,'ZON_GR_CLN')	
			db.datasetDuplicate(w,'GR_SD_ZONE',w,'ZON_GR_SD')
			db.datasetDuplicate(w,'GR_SD_ZONE',w,'ZON_GR_CLN')

	if (d == "PEP_FINAL"):
		if db.datasetExists(w,'ZO_COAL'):	
			db.datasetDelete(w,'ZON_COALFLG')	
			db.datasetDuplicate(w,'ZO_COAL',w,'ZON_COALFLG')
		if db.datasetExists(w,'ZO_GR_CL_ZONE'):	
			db.datasetDelete(w,'ZON_GR_CL')	
			db.datasetDelete(w,'ZON_GR_CLY')	
			db.datasetDuplicate(w,'ZO_GR_CL_ZONE',w,'ZON_GR_CL')
			db.datasetDuplicate(w,'ZO_GR_CL_ZONE',w,'ZON_GR_CLY')
		if db.datasetExists(w,'ZO_GR_SD_ZONE'):	
			db.datasetDelete(w,'ZON_GR_SD')	
			db.datasetDelete(w,'ZON_GR_CLN')	
			db.datasetDuplicate(w,'ZO_GR_SD_ZONE',w,'ZON_GR_SD')
			db.datasetDuplicate(w,'ZO_GR_SD_ZONE',w,'ZON_GR_CLN')
		if db.datasetExists(w,'ZO_HC_TYPE'):	
			db.datasetDelete(w,'ZON_OGF')	
			db.datasetDuplicate(w,'ZO_HC_TYPE',w,'ZON_OGF')
		if db.datasetExists(w,'ZO_LMSTREAK'):	
			db.datasetDelete(w,'ZON_LMSTRKFLG')	
			db.datasetDuplicate(w,'ZO_LMSTREAK',w,'ZON_LMSTRKFLG')
		if db.datasetExists(w,'ZO_NEUTRON_FACTOR'):	
			db.datasetDelete(w,'ZON_NEUFAC')	
			db.datasetDuplicate(w,'ZO_NEUTRON_FACTOR',w,'ZON_NEUFAC')
		if db.datasetExists(w,'ZO_RHOB_CLY_ZONE'):	
			db.datasetDelete(w,'ZON_RHOB_CLY')	
			db.datasetDuplicate(w,'ZO_RHOB_CLY_ZONE',w,'ZON_RHOB_CLY')
		if db.datasetExists(w,'ZO_NPHI_CLY_ZONE'):	
			db.datasetDelete(w,'ZON_NPHI_CLY')	
			db.datasetDuplicate(w,'ZO_NPHI_CLY_ZONE',w,'ZON_NPHI_CLY')
		if db.datasetExists(w,'ZO_RHOB_SYN_CL'):	
			db.datasetDelete(w,'ZON_SYNDENCL')	
			db.datasetDuplicate(w,'ZO_RHOB_SYN_CL',w,'ZON_SYNDENCL')
		if db.datasetExists(w,'ZO_RHOB_SYN_SD'):	
			db.datasetDelete(w,'ZON_SYNDENSD')	
			db.datasetDuplicate(w,'ZO_RHOB_SYN_SD',w,'ZON_SYNDENSD')

	if (d == "SSS_FINAL") or (d == "PEP_FINAL"):
		for key in ['ZON_BADHOLE','ZON_COALFLG','ZON_HC_CORRECTION','ZON_LITHOLOGY_TYPE','ZON_LMSTRKFLG','ZON_M','ZON_N','ZON_OGF','ZON_NEUFAC','ZON_NEUOFFSET','ZON_PEFOFFSET']:
			db.datasetTypeChange(w,key,'interval')	
			db.datasetGroupChange(w,key,["PEP_ZON_PAR"])

		for key in ['ZON_COALCUT','ZON_CWB_GRAD','ZON_GR_CL','ZON_GR_CLN','ZON_GR_CLY','ZON_GR_SD','ZON_LMSTRKCUT','ZON_NPHI_CLY','ZON_RHOB_CLY','ZON_RHOB_DRYSILT','ZON_RWF',\
		'ZON_SALW','ZON_SILTPOSRAT','ZON_DEGFLSLT','ZON_SYNDENCL','ZON_SYNDENSD']:
			db.datasetTypeChange(w,key,'checkshots')	
			db.datasetGroupChange(w,key,["PEP_ZON_PAR"])

		for key in db.datasetList(w):
			if (db.datasetGroup(w,key) == ["PEP_ZON_PAR"]):
				Varver = 0
				for v in db.variableList(w,key):
					if db.variableFamily(w,key,v) == 'Measured Depth':
						db.variableRename(w,key,v,'DEPTH')
					else:
						if (db.variableNameWithoutVersion(v) == 'INTERVAL'):
							Varfin = db.variableVersion(v)
							if (Varfin > Varver):
								db.variableDelete(w,key,key)
								db.variableRename(w,key,v,key)					
								if (db.datasetType(w,key) == 'interval'):
									db.variableTypeChange(w,key,key,'BlockedCurve')
									db.variableUnitChange(w,key,key,'unitless')
								if (key == 'ZON_LITHOLOGY_TYPE'):
									db.variableFamilyChange(w,key,key,"Zone Name")
								if (key == 'ZON_CWB_GRAD'):
									db.variableUnitChange(w,key,key,'unitless')
									db.variableFamilyChange(w,key,key,"CWB Parameters")
								if (key == 'ZON_DEGFLSLT'):
									db.variableUnitChange(w,key,key,'DEG')
									db.variableFamilyChange(w,key,key,"Silt Line Angle")
								if (key == 'ZON_NEUFAC'):
									db.variableUnitChange(w,key,key,'unitless')
									db.variableFamilyChange(w,key,key,"Neutron Factor")
								if (key == 'ZON_RWF'):
									db.variableUnitChange(w,key,key,'ohm.m')
									db.variableFamilyChange(w,key,key,"Formation Water Resistivity")
								if (key == 'ZON_BADHOLE'):
									db.variableFamilyChange(w,key,key,"Bad Hole Flag")
								if (key == 'ZON_HC_CORRECTION'):
									db.variableFamilyChange(w,key,key,"Hydrocarbon Correction")
								if (key == 'ZON_COALFLG'):
									db.variableFamilyChange(w,key,key,"Coal Flag")
								if (key == 'ZON_M'):
									db.variableFamilyChange(w,key,key,"Cementation Exponent")
								if (key == 'ZON_NPHI_CLY'):
									db.variableFamilyChange(w,key,key,"NPHI Clay")
								if (key == 'ZON_OGF'):
									db.variableFamilyChange(w,key,key,"Fluid Type Flag")
								if (key == 'ZON_RHOB_CLY'):
									db.variableUnitChange(w,key,key,'g/cm3')
									db.variableFamilyChange(w,key,key,"RHOB Clay")
								if (key == 'ZON_SYNDENCL'):
									db.variableUnitChange(w,key,key,'g/cm3')
									db.variableFamilyChange(w,key,key,"RHOB Synthetic Clay")
								if (key == 'ZON_SYNDENSD'):
									db.variableUnitChange(w,key,key,'g/cm3')
									db.variableFamilyChange(w,key,key,"RHOB Synthetic Sand")
								if (key == 'ZON_GR_CL'):
									db.variableFamilyChange(w,key,key,"GR Clay")
								if (key == 'ZON_GR_CLN'):
									db.variableFamilyChange(w,key,key,"GR Clean")
								if (key == 'ZON_GR_CLY'):
									db.variableFamilyChange(w,key,key,"GR Clay")
								if (key == 'ZON_GR_SD'):
									db.variableFamilyChange(w,key,key,"GR Sand")
								Varver = Varfin	



#Overwrite variables in "PEP" Dataset with variables from Geolog's FACIES Dataset
if (d == 'SSS_FINAL') and db.datasetExists(w,'FACIES'):	

	varFamily = db.variableFamily(w,"PEP","ROCKTYPE")
	varUnit = db.variableUnit(w,"PEP","ROCKTYPE")
	varGroup = db.variableGroup(w,"PEP","ROCKTYPE")
	varVer = 0
	varNameNoVer = ""
	
	for key in db.variableList(w,"FACIES"):
		varTemp = db.variableNameWithoutVersion(key)	
		if (varTemp=="FACIES_GROUP"):
				
			if (varNameNoVer!=varTemp):
				varNameNoVer = varTemp
				varVer = db.variableVersion(key)
			elif (db.variableVersion(key)<varVer):
				varNameNoVer = ""	
			else:	
				varVer = db.variableVersion(key)

			db.variableDelete(w,"PEP","ROCKTYPE")
			db.variableCopy(w,"FACIES",key,"PEP","ROCKTYPE",['linear'])
			db.variableFamilyChange(w,"PEP","ROCKTYPE",varFamily)
			db.variableUnitChange(w,"PEP","ROCKTYPE",varUnit)
			db.variableGroupChange(w,"PEP","ROCKTYPE",varGroup)



#Overwrite variables in "PEP" Dataset with variables from Geolog's PC_SAT Dataset
if (d == "SSS_FINAL"):
	varFamily = db.variableFamily(w,"PEP","SW_SHF")
	varUnit = db.variableUnit(w,"PEP","SW_SHF")
	varGroup = db.variableGroup(w,"PEP","SW_SHF")
	varVer = 0
	varNameNoVer = ""
	
	for key in db.variableList(w,"PC_SAT"):
		varTemp = db.variableNameWithoutVersion(key)	
		if (varTemp=="SW_CHOO") or (varTemp=="SW_J") or (varTemp=="SW_SKELT"):
				
			if (varNameNoVer!=varTemp):
				varNameNoVer = varTemp
				varVer = db.variableVersion(key)
			elif (db.variableVersion(key)>varVer):
				varVer = db.variableVersion(key)
			else:	
				varNameNoVer = ""	

			if db.variableExists(w,"PEP",varNameNoVer+"_SSS"):
				db.variableDelete(w,"PEP",varNameNoVer+"_SSS")
			db.variableCopy(w,d,key,"PEP",varNameNoVer+"_SSS",['linear'])
			db.variableUnitChange(w,"PEP",varNameNoVer+"_SSS",varUnit)
			db.variableGroupChange(w,"PEP",varNameNoVer+"_SSS",varGroup)
			db.variableFamilyChange(w,"PEP",varNameNoVer+"_SSS",varFamily)



#Relocate Geolog "SSS" or "PEP" data sets into one group of datasets.
if (d == "SSS_FINAL"):
	for key in ['EDIT','BADHOLE','BCP','COAL','CWB_GRAD','CWB_INT_PICKS','DEGFLSLT','DT_MAT','DT_MAT_CLAY','PHIT_SH',\
	'DT_MAT_SILT','DT_SH','HC_CORRECTION','HC_TYPE','LITHOLOGY_TYPE','M','NEUTRON_FACTOR','NOTHING','RHO_GRAIN',\
	'TOP_BOTTOM','GR_CL_ZONE','GR_SD_ZONE','NPHI_CLY_ZONE','RHOB_CLY_ZONE','RHOB_SYN_CL','RHOB_SYN_SD','REFERENCE',\
	'RT_SH','RWF','PC_SAT','PC_SAT_QC','FACIES','SSS','EDIT_CLASTICS','EDIT_CARB','SSS_CLASTICS','SSS_CARB','SSS_FINAL']:
		db.datasetGroupChange(w,key,["GEOLOG_SSS"])

if (d == "PEP_FINAL"):
	for key in ['ZO_BADHOLE','ZO_COAL','ZO_CWB_GRAD','ZO_CWB_INT_PICKS','ZO_GR_CL_ZONE','ZO_GR_SD_ZONE','ZO_HC_CORRECTION',\
	'ZO_HC_TYPE','ZO_LITHOLOGY_TYPE','ZO_LMSTREAK','ZO_M','ZO_N','ZO_NEUTRON_FACTOR','ZO_NPHI_CLY_ZONE','ZO_RHOB_CLY_ZONE',\
	'ZO_RHOB_SYN_CL','ZO_RHOB_SYN_SD','ZO_RWF','ZO_SALW','ZO_SILTPOSRAT','TOP_BOTTOM','ZO_TOP_BOTTOM','GL_PEP','PEP_FINAL','REFERENCE']:
		db.datasetGroupChange(w,key,["GEOLOG_PEP"])



#Store properties in "SSS_FINAL" to "PEP_VAR_PAR" Dataset
if UseGraphicalParameterPicking=='YES':
	Var1='PEP_VAR_PAR'
	Var2=''
	Var3=''
else:
	Var1='ZON_RHOB_CLY'
	Var2='ZON_NPHI_CLY'
	Var3='ZU'

DatSet1=d
DatSet2=d
Flag1=1
Satr1=''
MNZon1=0
Perm1=''
RTMet1=''
Trans1=0
ResNum1=0
RTNum1=0
DegFS1=0
DegRT1=0
Rat0=-99
Rat1=-99
Rat2=-99
Rat3=-99
Rat0N=-99
Rat1N=-99
Rat3N=-99
SiltRat1=-99
RTRat1=-99
mrocktpln=0

if (d=='SSS_FINAL'):
	for key in db.wellPropertyList(w):
		ProValue1=db.wellPropertyValue(w,key)
		db.datasetPropertyChange(w,d,key,ProValue1)

	if (db.datasetExists(w,'SSS')):
		for key in db.datasetPropertyList(w,'SSS'):
			ProValue1=db.datasetPropertyValue(w,'SSS',key)
			db.datasetPropertyChange(w,d,key,ProValue1)

	if (db.datasetExists(w,'EDIT')):
		for key in db.datasetPropertyList(w,'EDIT'):
			ProValue1=db.datasetPropertyValue(w,'EDIT',key)
			db.datasetPropertyChange(w,d,key,ProValue1)

	for key in db.datasetPropertyList(w,'SSS_FINAL'):
		ValTemp=db.datasetPropertyValue(w,'SSS_FINAL',key)
		if (key=='FINAL_SWT'): 
			Satr1=ValTemp
		if (key=='PP_PERM_OPTION') or (key=='CH_PERM_OPTION'): 
			Perm1=ValTemp
		if (key=='ROCK_TYPE_METHOD'): 
			RTMet1=ValTemp
		try:	
			if (key=='G_NO_ZONES_A_M_N'): 
				MNZon1=int(ValTemp)
			if (key=='PP_NO_FACIES'): 
				Trans1=int(ValTemp)
			if (key=='CONTACTS_NO'): 
				ResNum1=int(ValTemp)
			if (key=='FACIES_NO'): 
				RTNum1=int(ValTemp)
			if (key=='SSC_RHOB_FLUID'): 
				Rat0=float(ValTemp)
			if (key=='SSC_NPHI_FLUID'): 
				Rat0N=float(ValTemp)
			if (key=='SSC_RHOB_SAND_MA'): 
				Rat1=float(ValTemp)
			if (key=='SSC_NPHI_SAND_MA'): 
				Rat1N=float(ValTemp)
			if (key=='SSC_RHOB_DRY_SILT'): 
				Rat2=float(ValTemp)
			if (key=='RHOB_DRYCL'): 
				Rat3=float(ValTemp)
			if (key=='NPHI_DRYCL'): 
				Rat3N=float(ValTemp)
			if (key=='SSC_DEGFLSLT'): 
				DegFS1=float(ValTemp)
			if (key=='DEGFACI'):
				DegRT1=float(ValTemp)
		except:
				pass
	if (DegRT1>0):
		mrocktpln=tan(radians(DegRT1))
	if (Rat0>0) and (Rat1>0) and (Rat2>0) and (Rat3>0) and (Rat0N!=-9999) and (Rat1N!=-9999) and (Rat3N!=-9999):
		SiltRat1=round((Rat2-Rat1)/(Rat3-Rat1)*100)
		crocktpln=Rat0-mrocktpln*Rat0N
		msndclyln=(Rat3-Rat1)/(Rat3N-Rat1N)
		csndclyln=Rat1-msndclyln*Rat1N
		RatRTN=(csndclyln-crocktpln)/(mrocktpln-msndclyln)
		RTRat1=(RatRTN-Rat1N)/(Rat3N-Rat1N)

	for key in db.datasetPropertyList(w,'SSS_FINAL'):
		ValTemp=db.datasetPropertyValue(w,'SSS_FINAL',key)

		for Varx in [Var1,Var2,Var3]:
			db.datasetPropertyChange(w,Varx,'########################','/// GEOLOG SSC PARAMETERS ///')

			db.datasetPropertyChange(w,Varx,'1-----------------------','----- PROC_INTERVAL -----')
			if (key=='G_DEPTHTOP'): 
				db.datasetPropertyChange(w,Varx,'1__PROC_START',ValTemp)
			if (key=='G_DEPTHBT'): 
				db.datasetPropertyChange(w,Varx,'1__PROC_STOP',ValTemp)

			db.datasetPropertyChange(w,Varx,'2-----------------------','----- SSC_MODEL -----')
			if (key=='SSC_NPHI_FLUID'): 
				ValTemp=str(Rat0N)
				db.datasetPropertyChange(w,Varx,'2__NPHI_FLUID',ValTemp+' frac')
			if (key=='SSC_NPHI_SAND_MA'): 
				db.datasetPropertyChange(w,Varx,'2__NPHI_DRY_SAND',ValTemp+' frac')
			if (key=='SSC_RHOB_SAND_MA'): 
				db.datasetPropertyChange(w,Varx,'2__RHOB_DRY_SAND',ValTemp+' g/cm3')
			if (key=='SSC_RHOB_DRY_SILT'): 
				db.datasetPropertyChange(w,Varx,'2__RHOB_DRY_SILT',ValTemp+' g/cm3')
			if (key=='SSC_RHOB_FLUID'): 
				ValTemp=str(Rat0)
				db.datasetPropertyChange(w,Varx,'2__RHOB_FLUID',ValTemp+' g/cm3')
			if (key=='SSC_DEGFLSLT'): 
				db.datasetPropertyChange(w,Varx,'2__SILT_LINE_ANGLE',ValTemp+' deg')
				db.datasetPropertyChange(w,Varx,'2__SILT_POS_RATIO',str(SiltRat1)+' %')	

			db.datasetPropertyChange(w,Varx,'3-----------------------','----- SW PARAMETER -----')
			if (key=='G_BHT_TEMP'): 
				db.datasetPropertyChange(w,Varx,'3___TEMP_TD',ValTemp)
			if (key=='G_DF_TEMP'): 
				db.datasetPropertyChange(w,Varx,'3___TEMP_SURF',ValTemp)
			if (key=='G_TEMP_UNIT'):
				db.datasetPropertyChange(w,Varx,'3___TEMP_UNIT',ValTemp)
			if (key=='G_DEPTHBT'): 
				db.datasetPropertyChange(w,Varx,'3___TOTAL_DEPTH',ValTemp)
			if (key=='FINAL_SWT'): 
				db.datasetPropertyChange(w,Varx,'3__EQU_OF_SW',ValTemp)
			if (key=='SSC_M_STAR_VAL') and (Satr1=='WAXMAN_SMITS'):
				if (ValTemp=='USER_DEFINED'):
					ValTemp='CONSTANT'
				else:
					ValTemp='CALC FROM M'
				db.datasetPropertyChange(w,Varx,'3__M_STAR_SOURCE',ValTemp)
			if (key=='SSC_HAVE_QV') and (Satr1=='WAXMAN_SMITS'): 
				db.datasetPropertyChange(w,Varx,'3__EXT_QV_LOG',ValTemp)
			if (key=='G_NO_ZONES_A_M_N'): 
				db.datasetPropertyChange(w,Varx,'3__NO_OF_M-N_ZONE',ValTemp)
			if (key=='G_TOP_A_M_N') and (MNZon1>=1): 
				db.datasetPropertyChange(w,Varx,'3__TOP_ZONE1',ValTemp)
			if (key=='G_M_ZONE1') and (MNZon1>=1): 
				db.datasetPropertyChange(w,Varx,'3__ZONE1_M/M*',ValTemp)
			if (key=='G_N_ZONE1') and (MNZon1>=1): 
				db.datasetPropertyChange(w,Varx,'3__ZONE1_N/N*',ValTemp)
			if (key=='G_TOP_A_M_N2') and (MNZon1>=2): 
				db.datasetPropertyChange(w,Varx,'3__TOP_ZONE2',ValTemp)
			if (key=='G_M_ZONE2') and (MNZon1>=2): 
				db.datasetPropertyChange(w,Varx,'3__ZONE2_M/M*',ValTemp)
			if (key=='G_N_ZONE2') and (MNZon1>=2): 
				db.datasetPropertyChange(w,Varx,'3__ZONE2_N/N*',ValTemp)
			if (key=='G_TOP_A_M_N3') and (MNZon1>=3): 
				db.datasetPropertyChange(w,Varx,'3__TOP_ZONE3',ValTemp)
			if (key=='G_M_ZONE3') and (MNZon1>=3): 
				db.datasetPropertyChange(w,Varx,'3__ZONE3_M/M*',ValTemp)
			if (key=='G_N_ZONE3') and (MNZon1>=3): 
				db.datasetPropertyChange(w,Varx,'3__ZONE3_N/N*',ValTemp)
			if (key=='G_TOP_A_M_N4') and (MNZon1>=3): 
				db.datasetPropertyChange(w,Varx,'3__TOP_ZONE4',ValTemp)

			db.datasetPropertyChange(w,Varx,'4-----------------------','----- HC_CORRECTION -----')
			if (key=='COR_METHOD') or (key=='HC_COR_METHOD'): 
				if (ValTemp=='DEFAULT'):
					ValTemp='EMPIRICAL' 
				elif (ValTemp=='SECOND_METHOD'):
					ValTemp='STANDARD' 
				db.datasetPropertyChange(w,Varx,'4__HC_COR_METHOD',ValTemp)
			if (key=='HC_RHO_OIL'): 
				db.datasetPropertyChange(w,Varx,'4__RHO_OIL',ValTemp+' g/cm3')
			if (key=='HC_RHO_GAS'): 
				db.datasetPropertyChange(w,Varx,'4__RHO_GAS',ValTemp+' g/cm3')
			if (key=='HC_RHO_MUD_FL'): 
				RoundNum=round(float(ValTemp),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'4__RHO_MUD_FLTR',ValTemp+' g/cm3')
			if (key=='HC_RMF_SAL'): 
				db.datasetPropertyChange(w,Varx,'4__SAL_MUD_FLTR',ValTemp+' ppm')

			db.datasetPropertyChange(w,Varx,'5-----------------------','----- BH_CORRECTION -----')
			if (key=='RHOB_OPT') or (key=='BH_RHOB_OPT'): 
				db.datasetPropertyChange(w,Varx,'5__BH_COR_OPT',ValTemp)
			if (key=='BH_BAD_MOD_REF'): 
				db.datasetPropertyChange(w,Varx,'5__SOURCE_SYN_RHOB',ValTemp)

			db.datasetPropertyChange(w,Varx,'6-----------------------','----- PERM_CHOO -----')
			if (key=='PP_CLAY_CONS') or (key=='CH_CLAY_CONS'): 
				db.datasetPropertyChange(w,Varx,'6__CONS_CLAY',ValTemp)
			if (key=='PP_SILT_CONS') or (key=='CH_SILT_CONS'): 
				db.datasetPropertyChange(w,Varx,'6__CONS_SILT',ValTemp)
			if ((key=='PP_CONST_CHIEW') or (key=='PERM_CH_CONST_CHIEW')) and (Perm1=='YES'): 
				db.datasetPropertyChange(w,Varx,'6__PERM_CHOO_CONS',ValTemp)
			if ((key=='PP_EXPO_CHIEW') or (key=='CH_EXPO_CHIEW')) and (Perm1=='YES'): 
				db.datasetPropertyChange(w,Varx,'6__PERM_CHOO_EXPO',ValTemp)
			if ((key=='PP_POR_AVG') or (key=='CH_POR_AVG')) and (Perm1=='NO'): 
				db.datasetPropertyChange(w,Varx,'6__POR_AVG',ValTemp)
			if ((key=='PP_R_GRAIN') or (key=='CH_R_GRAIN')) and (Perm1=='NO'): 
				db.datasetPropertyChange(w,Varx,'6__R_GRAIN',ValTemp)
			if ((key=='PP_R_EFF') or (key=='CH_R_EFF')) and (Perm1=='NO'): 
				db.datasetPropertyChange(w,Varx,'6__R_EFF',ValTemp)
			if ((key=='PP_POB') or (key=='CH_POB')) and (Perm1=='NO'): 
				db.datasetPropertyChange(w,Varx,'6__OVB_PRESS_GRAD',ValTemp)
			if ((key=='PP_PF') or (key=='CH_PF')) and (Perm1=='NO'): 
				db.datasetPropertyChange(w,Varx,'6__FORM_PRESS_GRAD',ValTemp)
			if ((key=='PP_RE_DEPTH') or (key=='CH_RE_DEPTH')) and (Perm1=='NO'): 
				db.datasetPropertyChange(w,Varx,'6__RES_DEPTH',ValTemp)	

			db.datasetPropertyChange(w,Varx,'7-----------------------','----- ROCK-TYPING -----')
			if (key=='ROCK_TYPE_METHOD'): 
				if (ValTemp=='DENSITY_NEUTRON'): 
					ValTemp='VSH-DN'
				db.datasetPropertyChange(w,Varx,'7__METHOD',ValTemp)
			if (key=='DEGFACI') and (RTMet1=='DENSITY_NEUTRON'): 
				RoundNum=round(RTRat1,2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VSH-DN_CUTOFF_OF_NON-RES/RES-1',ValTemp+' frac')
			if (key=='FC1') and (RTMet1=='DENSITY_NEUTRON'): 
				RoundNum=round(RTRat1*(1-float(ValTemp)),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VSH-DN_CUTOFF_OF_RES-1/RES-2',ValTemp+' frac')
			if (key=='FC2') and (RTMet1=='DENSITY_NEUTRON'): 
				RoundNum=round(RTRat1*(1-float(ValTemp)),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VSH-DN_CUTOFF_OF_RES-2/RES-3',ValTemp+' frac')
			if (key=='FC3') and (RTMet1=='DENSITY_NEUTRON'): 
				RoundNum=round(RTRat1*(1-float(ValTemp)),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VSH-DN_CUTOFF_OF_RES-3/RES-4',ValTemp+' frac')
			if (key=='FC4') and (RTMet1=='DENSITY_NEUTRON'): 
				RoundNum=round(RTRat1*(1-float(ValTemp)),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VSH-DN_CUTOFF_OF_RES-4/RES-5',ValTemp+' frac')
			if (key=='FC0_CLAY_CUTOFF') and (RTMet1=='VOL_CLAY'): 
				RoundNum=round(RTRat1*(1-float(ValTemp)),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VCL_CUTOFF_OF_NON-RES/RES-1',ValTemp+' frac')
			if (key=='FC1_CLAY_CUTOFF') and (RTMet1=='VOL_CLAY'): 
				RoundNum=round(float(ValTemp),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VCL_CUTOFF_OF_RES-1/RES-2',ValTemp+' frac')
			if (key=='FC2_CLAY_CUTOFF') and (RTMet1=='VOL_CLAY'): 
				RoundNum=round(float(ValTemp),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VCL_CUTOFF_OF_RES-2/RES-3',ValTemp+' frac')
			if (key=='FC3_CLAY_CUTOFF') and (RTMet1=='VOL_CLAY'): 
				RoundNum=round(float(ValTemp),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VCL_CUTOFF_OF_RES-3/RES-4',ValTemp+' frac')
			if (key=='FC4_CLAY_CUTOFF') and (RTMet1=='VOL_CLAY'): 
				RoundNum=round(float(ValTemp),2)
				ValTemp=str(RoundNum)
				db.datasetPropertyChange(w,Varx,'7__VCL_CUTOFF_OF_RES-4/RES-5',ValTemp+' frac')	

			db.datasetPropertyChange(w,Varx,'8-----------------------','----- PERM_TRANSFORM -----')	
			if (key=='PP_NO_FACIES'): 
				db.datasetPropertyChange(w,Varx,'8__NO_OF_ROCKTYPE',ValTemp)
			if (key=='PP_K_PHI_FUNCTION'): 
				db.datasetPropertyChange(w,Varx,'8__FUNCTION_TYPE',ValTemp)
			if (key=='PP_A1_G1') and (Trans1>=1): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT1_A',ValTemp)
			if (key=='PP_B1_G1') and (Trans1>=1): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT1_B',ValTemp)
			if (key=='PP_A2_G2') and (Trans1>=2): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT2_A',ValTemp)
			if (key=='PP_B2_G2') and (Trans1>=2): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT2_B',ValTemp)
			if (key=='PP_A3_G3') and (Trans1>=3): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT3_A',ValTemp)
			if (key=='PP_B3_G3') and (Trans1>=3): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT3_B',ValTemp)
			if (key=='PP_A4_G4') and (Trans1>=4): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT4_A',ValTemp)
			if (key=='PP_B4_G4') and (Trans1>=4): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT4_B',ValTemp)
			if (key=='PP_A3_G3') and (Trans1>=5): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT5_A',ValTemp)
			if (key=='PP_B3_G3') and (Trans1>=5): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT5_B',ValTemp)
			if (key=='PP_A4_G4') and (Trans1>=6): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT6_A',ValTemp)
			if (key=='PP_B4_G4') and (Trans1>=6): 
				db.datasetPropertyChange(w,Varx,'8__TRANSF_RT6_B',ValTemp)

			db.datasetPropertyChange(w,Varx,'9-----------------------','----- SHF PARAMETERS-----')
			if (key=='CONTACTS_NO'): 
				db.datasetPropertyChange(w,Varx,'9__NO_OF_RES',ValTemp)
			if (key=='BNOT'): 
				db.datasetPropertyChange(w,Varx,'9__BNOT_SW_CHOO',ValTemp)
			if (key=='FACIES_NO'): 
				db.datasetPropertyChange(w,Varx,'9__JF_NO_OF_RT_(INC_NON-RES)',ValTemp)
			if (key=='LEVERETT_REGRESSION'): 
				db.datasetPropertyChange(w,Varx,'9__JF_FUNCTION_TYPE',ValTemp)
			if (key=='A_J0'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT0_A',ValTemp)
			if (key=='B_J0'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT0_B',ValTemp)
			if (key=='A_J1'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT1_A',ValTemp)
			if (key=='B_J1'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT1_B',ValTemp)
			if (key=='A_J2'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT2_A',ValTemp)
			if (key=='B_J2'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT2_B',ValTemp)
			if (key=='A_J3'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT3_A',ValTemp)
			if (key=='B_J3'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT3_B',ValTemp)
			if (key=='A_J4'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT4_A',ValTemp)
			if (key=='B_J4'): 
				db.datasetPropertyChange(w,Varx,'9__JF_RT4_B',ValTemp)
			if (key=='PERM_LIMIT'): 
				db.datasetPropertyChange(w,Varx,'9__LIMIT_PERM',ValTemp+' mD')
			if (key=='RES_1_TOP'): 
				db.datasetPropertyChange(w,Varx,'9__RES1__START',ValTemp)
			if (key=='RES_1_BOT'): 
				db.datasetPropertyChange(w,Varx,'9__RES1__STOP',ValTemp)
			if (key=='RES_1_SYSTEM'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_FLUID_SYSTEM',ValTemp)
			if (key=='RES_1_FWL'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_FWL',ValTemp)
			if (key=='RES_1_GOC'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_GOC',ValTemp)
			if (key=='GAS_GRAD1'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_GRAD_GAS',ValTemp+' psi/ft')
			if (key=='OIL_GRAD1'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_GRAD_OIL',ValTemp+' psi/ft')
			if (key=='GAS_DYNE_LAB1'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_GAS_DYNE_LAB',ValTemp)
			if (key=='GAS_DYNE_RES1'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_GAS_DYNE_RES',ValTemp)
			if (key=='OIL_DYNE_LAB1'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_OIL_DYNE_LAB',ValTemp)
			if (key=='OIL_DYNE_LAB1'): 
				db.datasetPropertyChange(w,Varx,'9__RES1_OIL_DYNE_RES',ValTemp)
			if (key=='RES_2_TOP') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2__START',ValTemp)
			if (key=='RES_2_BOT') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2__STOP',ValTemp)
			if (key=='RES_2_SYSTEM') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_FLUID_SYSTEM',ValTemp)
			if (key=='RES_2_FWL') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_FWL',ValTemp)
			if (key=='RES_2_GOC') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_GOC',ValTemp)
			if (key=='GAS_GRAD2') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_GRAD_GAS',ValTemp+' psi/ft')
			if (key=='OIL_GRAD2') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_GRAD_OIL',ValTemp+' psi/ft')
			if (key=='GAS_DYNE_LAB2') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_GAS_DYNE_LAB',ValTemp)
			if (key=='GAS_DYNE_RES2') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_GAS_DYNE_RES',ValTemp)
			if (key=='OIL_DYNE_LAB2') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_OIL_DYNE_LAB',ValTemp)
			if (key=='OIL_DYNE_LAB2') and (ResNum1>1): 
				db.datasetPropertyChange(w,Varx,'9__RES2_OIL_DYNE_RES',ValTemp)
			if (key=='RES_3_TOP') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3__START',ValTemp)
			if (key=='RES_3_BOT') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3__STOP',ValTemp)
			if (key=='RES_3_SYSTEM') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_FLUID_SYSTEM',ValTemp)
			if (key=='RES_3_FWL') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_FWL',ValTemp)
			if (key=='RES_3_GOC') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_GOC',ValTemp)
			if (key=='GAS_GRAD3') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_GRAD_GAS',ValTemp+' psi/ft')
			if (key=='OIL_GRAD3') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_GRAD_OIL',ValTemp+' psi/ft')
			if (key=='GAS_DYNE_LAB3') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_GAS_DYNE_LAB',ValTemp)
			if (key=='GAS_DYNE_RES3') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_GAS_DYNE_RES',ValTemp)
			if (key=='OIL_DYNE_LAB3') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_OIL_DYNE_LAB',ValTemp)
			if (key=='OIL_DYNE_LAB3') and (ResNum1>2): 
				db.datasetPropertyChange(w,Varx,'9__RES3_OIL_DYNE_RES',ValTemp)
			if (key=='RES_4_TOP') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4__START',ValTemp)
			if (key=='RES_4_BOT') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4__STOP',ValTemp)
			if (key=='RES_4_SYSTEM') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_FLUID_SYSTEM',ValTemp)
			if (key=='RES_4_FWL') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_FWL',ValTemp)
			if (key=='RES_4_GOC') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_GOC',ValTemp)
			if (key=='GAS_GRAD4') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_GRAD_GAS',ValTemp+' psi/ft')
			if (key=='OIL_GRAD4') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_GRAD_OIL',ValTemp+' psi/ft')
			if (key=='GAS_DYNE_LAB4') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_GAS_DYNE_LAB',ValTemp)
			if (key=='GAS_DYNE_RES4') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_GAS_DYNE_RES',ValTemp)
			if (key=='OIL_DYNE_LAB4') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_OIL_DYNE_LAB',ValTemp)
			if (key=='OIL_DYNE_LAB4') and (ResNum1>3): 
				db.datasetPropertyChange(w,Varx,'9__RES4_OIL_DYNE_RES',ValTemp)
			if (key=='RES_5_TOP') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5__START',ValTemp)
			if (key=='RES_5_BOT') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5__STOP',ValTemp)
			if (key=='RES_5_SYSTEM') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_FLUID_SYSTEM',ValTemp)
			if (key=='RES_5_FWL') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_FWL',ValTemp)
			if (key=='RES_5_GOC') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_GOC',ValTemp)
			if (key=='GAS_GRAD5') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_GRAD_GAS',ValTemp+' psi/ft')
			if (key=='OIL_GRAD5') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_GRAD_OIL',ValTemp+' psi/ft')
			if (key=='GAS_DYNE_LAB5') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_GAS_DYNE_LAB',ValTemp)
			if (key=='GAS_DYNE_RES5') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_GAS_DYNE_RES',ValTemp)
			if (key=='OIL_DYNE_LAB5') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_OIL_DYNE_LAB',ValTemp)
			if (key=='OIL_DYNE_LAB5') and (ResNum1>4): 
				db.datasetPropertyChange(w,Varx,'9__RES5_OIL_DYNE_RES',ValTemp)
			if (key=='WAT_GRAD'): 
				db.datasetPropertyChange(w,Varx,'9__RES_GRAD_WTR',ValTemp+' psi/ft')

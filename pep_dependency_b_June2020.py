def updateParameterDict(pDict):
	pDict['PERM_OPTION'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES')
	pDict['POR_AVG'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'YES')
	pDict['R_GRAIN'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'YES')
	pDict['M'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'YES')
	pDict['R_EFF'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'YES')
	pDict['POB'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'YES')
	pDict['PF'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'YES')
	pDict['RSVR_DEPTH'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'YES')
	pDict['CONST_CHOO'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'NO')
	pDict['EXPO_CHOO'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES' and pDict["PERM_OPTION"].value('value') == 'NO')
	pDict['CLAY_CONS'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES')
	pDict['SILT_CONS'].valueChange('enable', pDict["PERMCRT"].value('value') == 'YES')
	pDict['ROCK_TYPING_METHOD'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES')
	pDict['CUT_OFF_ORDER'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES')
	pDict['EXT_INDIC_LOG'].valueChange('enable', pDict["ROCK_TYPING_METHOD"].value('value') in ('EXTERNAL','EXTERNAL(REVERSE)') and pDict["RTCRT"].value('value') == 'YES')
	pDict['NZN_ROCKTP'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES')
	pDict['NR_CUT_OFF'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 0)
	pDict['RT1_CUT_OFF'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 1)
	pDict['RT2_CUT_OFF'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 2)
	pDict['RT3_CUT_OFF'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 3)
	pDict['RT4_CUT_OFF'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 4)
	pDict['RT5_CUT_OFF'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 5)
	pDict['RT6_CUT_OFF'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 6)
	pDict['EXT_RCKTYP_LOG'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and pDict["RTCRT"].value('value') == 'NO')
	pDict['NZN_ROCKTPEXT'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and pDict["RTCRT"].value('value') == 'NO')
	pDict['TRANSTYP'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and pDict["RTCRT"].value('value') in ('NO','YES'))
	pDict['TRANS_A1'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES')
	pDict['TRANS_B1'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES')
	pDict['TRANS_A2'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 1) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 1))
	pDict['TRANS_B2'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 1) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 1))
	pDict['TRANS_A3'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 2) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 2))
	pDict['TRANS_B3'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 2) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 2))
	pDict['TRANS_A4'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 3) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 3))
	pDict['TRANS_B4'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 3) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 3))
	pDict['TRANS_A5'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 4) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 4))
	pDict['TRANS_B5'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 4) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 4))
	pDict['TRANS_A6'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 5) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 5))
	pDict['TRANS_B6'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 5) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 5))
	pDict['TRANS_A7'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 6) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 6))
	pDict['TRANS_B7'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES' and (pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 6) or (pDict["RTCRT"].value('value') == 'NO' and pDict["NZN_ROCKTPEXT"].value('value') > 6))
	pDict['SHF_METHOD'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['PERM_SOURCE'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['EXT_PERM_LOG'].valueChange('enable', pDict["PERM_SOURCE"].value('value') == 'EXTERNAL' and pDict["SHFCRT"].value('value') == 'YES')
	pDict['BO_CHOO'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES' and pDict["SHF_METHOD"].value('value') == 'CHOO')
	pDict['SCOSTG'].valueChange('enable', pDict["SHF_METHOD"].value('value') != 'SKELT-KA' and pDict["SHFCRT"].value('value') == 'YES')
	pDict['SCOSTO'].valueChange('enable', pDict["SHF_METHOD"].value('value') != 'SKELT-KA' and pDict["SHFCRT"].value('value') == 'YES')
	pDict['SWIR_EQU'].valueChange('enable', pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J' and pDict["SHFCRT"].value('value') == 'YES')
	pDict['INPUT_LOG_FOR_SWIR'].valueChange('enable', pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J' and pDict["SHFCRT"].value('value') == 'YES')
	pDict['EXT_INPUT_LOG_FOR_SWIR'].valueChange('enable', pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J' and pDict["SHFCRT"].value('value') == 'YES' and pDict["INPUT_LOG_FOR_SWIR"].value('value') == 'EXTERNAL')
	pDict['ZA'].valueChange('enable', pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J' and pDict["SHFCRT"].value('value') == 'YES')
	pDict['ZB'].valueChange('enable', pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J' and pDict["SHFCRT"].value('value') == 'YES')
	pDict['NZN_RTSHF'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO')
	pDict['EXT_RTSHF_LOG'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') != 0)
	pDict['JA1'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES')
	pDict['JB1'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES')
	pDict['JA2'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 1) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 1) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 1)))
	pDict['JB2'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 1) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 1) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 1)))
	pDict['JA3'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 2) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 2) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 2)))
	pDict['JB3'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 2) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 2) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 2)))
	pDict['JA4'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 3) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 3) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 3)))
	pDict['JB4'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 3) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 3) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 3)))
	pDict['JA5'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 4) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 4) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 4)))
	pDict['JB5'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 4) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 4) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 4)))
	pDict['JA6'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 5) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 5) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 5)))
	pDict['JB6'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 5) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 5) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 5)))
	pDict['JA7'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 6) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 6) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 6)))
	pDict['JB7'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES' and ((pDict["RTCRT"].value('value') == 'YES' and pDict["NZN_ROCKTP"].value('value') > 6) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'YES' and pDict["NZN_ROCKTPEXT"].value('value') > 6) or (pDict["RTCRT"].value('value') == 'NO' and pDict["TRANSCRT"].value('value') == 'NO' and pDict["NZN_RTSHF"].value('value') > 6)))
	pDict['CUTP1'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['MAX_HEIGHT_OF_SWIR_PC'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES')
	pDict['__________FLUID_CONTACT__SECTION'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['CONTACT_DEPTH_SOURCE'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['GWC_DEPTH'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['GOC_DEPTH'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['OWC_DEPTH'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['GAS_GRAD'].valueChange('enable',  pDict["SHFCRT"].value('value') == 'YES')
	pDict['OIL_GRAD'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['WTR_GRAD'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['TVDSS'].valueChange('enable', pDict["CONTACT_DEPTH_SOURCE"].value('value') == 'DEPTH_TVDSS')
	pDict['ROCKTYPE'].valueChange('enable', pDict["RTCRT"].value('value') == 'YES')
	pDict['PERM_TRFM'].valueChange('enable', pDict["TRANSCRT"].value('value') == 'YES')
	pDict['SW_SHF'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['HT'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['PC'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['JFN'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['RQI'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['FZI'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES')
	pDict['SWIRR'].valueChange('enable', pDict["SHFCRT"].value('value') == 'YES' and pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J')
	pDict['SWIRR_PC_MAX_OIL'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES')
	pDict['SWIRR_PC_MAX_GAS'].valueChange('enable', (pDict["SHF_METHOD"].value('value') == 'J-FUNC' or pDict["SHF_METHOD"].value('value') == 'NORMALIZED-J') and pDict["SHFCRT"].value('value') == 'YES')

__pyVersion__ = """3"""
# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: \\file03-sea-pet.x-00is5x.ps\techlog-pp\COMPANY_FOLDER\External_DLLs\REM_RFM_Enhancement_Equations_rev3.py
# Bytecode version: 3.6rc1 (3379)
# Source timestamp: 2024-02-13 19:16:04 UTC (1707851764)

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
    return falseResult
parameterDict = {}
try:
    if Parameter:
        pass
    pass
except NameError:

    class Parameter:

        def __init__(self, **d):
            return
__author__ = 'Ismail MARZUKI (ismail.gazali)'
__date__ = '2019-04-15'
__version__ = '1.0'
__pyVersion__ = '3'
__group__ = ''
__suffix__ = ''
__prefix__ = ''
__applyMode__ = '0'
__awiEngine__ = 'v1'
__layoutTemplateMode__ = ''
__includeMissingValues__ = 'True'
__keepPreviouslyComputedValues__ = 'True'
__areInputDisplayed__ = 'True'
__useMultiWellLayout__ = 'True'
__idForHelp__ = ''
__executionGranularity__ = 'full'
import numpy as np
import math
import TechlogStat
import TechlogMath
import TechlogDialog
import Techlog
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
    return falseResult
parameterDict = {}
try:
    if Parameter:
        pass
    pass
except NameError:

    class Parameter:

        def __init__(self, **d):
            return

def REM_enhancementinputs(LOW, MEDIUM, HIGH):
    if LOW == 'YES':
        c1 = 3
    else:
        c1 = 0
    if MEDIUM == 'YES':
        c2 = 4
    else:
        c2 = 0
    if HIGH == 'YES':
        c3 = 8
    else:
        c3 = 0
    c4 = c1 + c2 + c3
    if HIGH == 'YES' or MEDIUM == 'YES':
        d1 = -1000000
    else:
        d1 = c1
    if LOW == 'YES' or HIGH == 'YES':
        d2 = -1000000
    else:
        d2 = c2
    if LOW == 'YES' or MEDIUM == 'YES':
        d3 = -1000000
    else:
        d3 = c3
    d4 = int(d1 + d2 + d3 + 2000000)
    if d4 == 8:
        multiplier1 = 1.1
    else:
        multiplier1 = 1.02
    multiplier2 = d4
    return (multiplier1, multiplier2)

def REMdeltaD(vshale, vshale2):
    if vshale == 0:
        deltaD = 0
    else:
        deltaD = (vshale - vshale2) / vshale
    return deltaD

def REMdeltaU(vshale, vshale2):
    if vshale == 0:
        deltaU = 0
    else:
        deltaU = (vshale - vshale2) / vshale
    return deltaU

def function1(deltaD, deltaU, vshale, multiplier1, multiplier2):
    A = multiplier1 * vshale * math.exp(deltaD * multiplier2)
    B = multiplier1 * vshale * math.exp(deltaU * multiplier2)
    if A >= 1:
        expD = 1
    else:
        expD = A
    if B >= 1:
        expU = 1
    else:
        expU = B
    if deltaD <= 0:
        selection = expD
    else:
        selection = expU
    exp1 = 0
    limit1 = 0
    if deltaD > 0 and deltaU > 0:
        if deltaD > deltaU:
            exp1 = deltaD
        else:
            exp1 = deltaU
    else:
        AA = vshale * math.exp(exp1 * 0.5 * multiplier2)
        if AA > 1:
            limit1 = 0.99
        else:
            limit1 = AA
    AB = selection * 0.7 + limit1 * 0.3
    return AB

def function2(AB, i):
    if AB[i] > 1:
        if i == 0:
            AC = stat.average([AB[i], AB[i + 1], AB[i + 2]])
        elif i == 1:
            AC = stat.average([AB[i], AB[i + 1], AB[i + 2], AB[i - 1]])
        elif i > 1 and i < n - 2:
            AC = stat.average([AB[i], AB[i - 1], AB[i - 2], AB[i + 1], AB[i + 2]])
        elif i == n - 2:
            AC = stat.average([AB[i], AB[i - 1], AB[i - 2], AB[i + 1]])
        elif i == n - 1:
            AC = stat.average([AB[i], AB[i - 1], AB[i - 2]])
    else:
        AC = AB[i]
    return AC

def function3(AC, i, n):
    if i == 0:
        enhancedvshale = 0.5 * AC[i] + 0.25 * AC[i + 1]
    elif i == n - 1:
        enhancedvshale = 0.5 * AC[i] + 0.25 * AC[i - 1]
    else:
        enhancedvshale = 0.5 * AC[i] + 0.25 * AC[i - 1] + 0.25 * AC[i + 1]
    return enhancedvshale

def function4(vshale, porosity):
    A = 2.252 - 0.7 * porosity
    B = 1.04 + 1.5 * porosity
    if vshale <= 0.85:
        vsilt = vshale ** (A - 1) * (1 - vshale) ** (B - 1)
    elif vshale > 0.85 and vshale <= 0.91:
        vsilt = 0.48
    elif vshale > 0.91:
        vsilt = 5.33 * (1 - vshale)
    else:
        vsilt = 0
    return vsilt

def function5(enhancedporosity, vsilt, vclay, GRAIN_RADIUS, m):
    a = GRAIN_RADIUS ** 2 / 80
    c = enhancedporosity * -2.5 + 1.7
    B = m * (2 / c + 1) + 2
    if enhancedporosity <= 0:
        enhancedporosity = 0
    A1 = a * enhancedporosity ** B
    A2 = TechlogMath.pow10(6 * vclay + 3 * vsilt)
    A = A1 / A2
    K = 0.0001
    if A > 0.0001:
        K = A
    return K

def function6(enhancedvshale):
    c0 = 0.0037
    c1 = -0.08569
    c2 = 1.6054
    c3 = -6.2252
    c4 = 13.3869
    c5 = -13.437
    c6 = 5.38375
    swb = c6 * enhancedvshale ** 6 + c5 * enhancedvshale ** 5 + c4 * enhancedvshale ** 4 + c3 * enhancedvshale ** 3 + c2 * enhancedvshale ** 2 + c1 * enhancedvshale + c0
    return swb

def function7(TVDSS, perm, phit, swb, FWL, gw, gh, IFT, b0):
    HAFWL = FWL - TVDSS
    if HAFWL > 0:
        Pc = (gw - gh) * HAFWL
        Je = 10 ** ((2 * b0 - 1) * math.log10(1 + TechlogMath.inv(swb)) + math.log10(1 + swb))
        B = b0 / 3 * math.log10(1 + TechlogMath.inv(swb))
        J_DE = 0.2166 * Pc / IFT * (perm / phit) ** 0.5
        shf = Je / J_DE ** B
        if shf > 1:
            shf = 1
    else:
        shf = 1
        Pc = 0
    return (shf, Pc)

def function7a(TVDSS, perm, phit, swb, Pc, IFT, b0):
    try:
        if Pc > 0:
            Je = 10 ** ((2 * b0 - 1) * math.log10(1 + TechlogMath.inv(swb)) + math.log10(1 + swb))
            B = b0 / 3 * math.log10(1 + TechlogMath.inv(swb))
            J_DE = 0.2166 * Pc / IFT * (perm / phit) ** 0.5
            shf = Je / J_DE ** B
            if shf > 1:
                shf = 1
        else:
            shf = 1
    except ValueError:
        shf = 1
    except ZeroDivisionError:
        shf = 1
    except OverflowError:
        shf = 1
    except TypeError:
        shf = 1
    return shf

def function8(vshale, enhancedvshale, porosity, PHIS, PHICL):
    deltavshale = vshale - enhancedvshale
    deltaporosity = PHIS * deltavshale - PHICL * deltavshale
    enhancedporosity = deltaporosity + porosity
    return (deltavshale, deltaporosity, enhancedporosity)

def function9(vshale, enhancedvshale, PHIS, PHICL, porosity, GRAIN_RADIUS, FWL, gw, gh, IFT, b0, dtvd, m, enhancedporosity, C, CF, permeability):
    deltavshale2 = (enhancedvshale - vshale) / vshale
    vsilt1 = function4(vshale, porosity)
    vcl1 = vshale - vsilt1
    vsilt0 = vsilt1 + vsilt1 * deltavshale2
    vcl0 = vcl1 + vcl1 * deltavshale2
    K0 = function11(m, PHIS, PHICL, C, CF, enhancedporosity, vsilt0, vcl0, GRAIN_RADIUS, permeability)
    swb0 = function6(enhancedvshale)
    phie0 = enhancedporosity * (1 - swb0)
    vsand0 = 1 - enhancedvshale - enhancedporosity
    if vsand0 < 0:
        vsand0 = 0
    shf0, Pc0 = function7(dtvd, K0, enhancedporosity, swb0, FWL, gw, gh, IFT, b0)
    swe0 = 1 - enhancedporosity / phie0 * (1 - shf0)
    vclb0 = enhancedporosity - phie0
    voil0 = (1 - swe0) * phie0
    vwater0 = phie0 - voil0
    vclw0 = vclb0 + vcl0
    return (vsilt0, vcl0, K0, swb0, phie0, vsand0, shf0, swe0, vclb0, voil0, vwater0, vclw0, Pc0)

def function9a(vshale, enhancedvshale, PHIS, PHICL, porosity, GRAIN_RADIUS, IFT, b0, dtvd, m, enhancedporosity, C, CF, Pc, permeability):
    deltavshale2 = (enhancedvshale - vshale) / vshale
    vsilt1 = function4(vshale, porosity)
    vcl1 = vshale - vsilt1
    vsilt0 = vsilt1 + vsilt1 * deltavshale2
    vcl0 = vcl1 + vcl1 * deltavshale2
    K0 = function11(m, PHIS, PHICL, C, CF, enhancedporosity, vsilt0, vcl0, GRAIN_RADIUS, permeability)
    swb0 = function6(enhancedvshale)
    phie0 = enhancedporosity * (1 - swb0)
    vsand0 = 1 - enhancedvshale - enhancedporosity
    if vsand0 < 0:
        vsand0 = 0
    shf0 = function7a(dtvd, K0, enhancedporosity, swb0, Pc, IFT, b0)
    swe0 = 1 - enhancedporosity / phie0 * (1 - shf0)
    vclb0 = enhancedporosity - phie0
    voil0 = (1 - swe0) * phie0
    vwater0 = phie0 - voil0
    vclw0 = vcl0
    vcl0 = vclw0 - vclb0
    return (vsilt0, vcl0, K0, swb0, phie0, vsand0, shf0, swe0, vclb0, voil0, vwater0, vclw0)

def function9b(vshale, enhancedvshale, PHIS, PHICL, porosity, GRAIN_RADIUS, FWL, gw, gh, IFT, b0, dtvd, m, enhancedporosity, C, CF, permeability, PERM_OPTION, A_PERM_CH, B_PERM_CH):
    deltavshale2 = (enhancedvshale - vshale) / vshale
    vsilt1 = function4(vshale, porosity)
    vcl1 = vshale - vsilt1
    vsilt0 = vsilt1 + vsilt1 * deltavshale2
    vcl0 = vcl1 + vcl1 * deltavshale2
    K0 = function11a(m, PHIS, PHICL, C, CF, enhancedporosity, vsilt0, vcl0, GRAIN_RADIUS, permeability, PERM_OPTION, A_PERM_CH, B_PERM_CH)
    swb0 = function6(enhancedvshale)
    phie0 = enhancedporosity * (1 - swb0)
    vsand0 = 1 - enhancedvshale - enhancedporosity
    if vsand0 < 0:
        vsand0 = 0
    shf0, Pc0 = function7(dtvd, K0, enhancedporosity, swb0, FWL, gw, gh, IFT, b0)
    swe0 = 1 - enhancedporosity / phie0 * (1 - shf0)
    vclb0 = enhancedporosity - phie0
    voil0 = (1 - swe0) * phie0
    vwater0 = phie0 - voil0
    vclw0 = vclb0 + vcl0
    return (vsilt0, vcl0, K0, swb0, phie0, vsand0, shf0, swe0, vclb0, voil0, vwater0, vclw0, Pc0)

def function9c(vshale, enhancedvshale, PHIS, PHICL, porosity, GRAIN_RADIUS, IFT, b0, dtvd, m, enhancedporosity, C, CF, Pc, permeability, PERM_OPTION, A_PERM_CH, B_PERM_CH):
    deltavshale2 = (enhancedvshale - vshale) / vshale
    vsilt1 = function4(vshale, porosity)
    vcl1 = vshale - vsilt1
    vsilt0 = vsilt1 + vsilt1 * deltavshale2
    vcl0 = vcl1 + vcl1 * deltavshale2
    K0 = function11a(m, PHIS, PHICL, C, CF, enhancedporosity, vsilt0, vcl0, GRAIN_RADIUS, permeability, PERM_OPTION, A_PERM_CH, B_PERM_CH)
    swb0 = function6(enhancedvshale)
    phie0 = enhancedporosity * (1 - swb0)
    vsand0 = 1 - enhancedvshale - enhancedporosity
    if vsand0 < 0:
        vsand0 = 0
    shf0 = function7a(dtvd, K0, enhancedporosity, swb0, Pc, IFT, b0)
    swe0 = 1 - enhancedporosity / phie0 * (1 - shf0)
    vclb0 = enhancedporosity - phie0
    voil0 = (1 - shf0) * enhancedporosity
    vwater0 = 1 - vcl0 - vsilt0 - vsand0 - voil0
    vclw0 = vcl0
    vcl0 = vclw0 - vclb0
    return (vsilt0, vcl0, K0, swb0, phie0, vsand0, shf0, swe0, vclb0, voil0, vwater0, vclw0)

def function10(shf0, enhancedporosity, dtvd1, dtvd2):
    ehc0 = (1 - shf0) * enhancedporosity * (dtvd1 - dtvd2)
    return ehc0

def function11(m, PHIS, PHICL, C, CF, PHIT_REM, VSILT_REM, VCLW_REM, rg, permeability):
    slope = (C - CF) / (PHIS - PHICL)
    constant = -slope * PHICL + CF
    c1 = PHIT_REM * slope + constant
    b1 = m * (2 / c1 + 1) + 2
    rg1 = rg ** 2 / 80
    try:
        K = rg1 * PHIT_REM ** b1 / 10 ** (6 * VCLW_REM + 3 * VSILT_REM)
    except OverflowError:
        K = permeability
    except ValueError:
        K = 0.0001
    except ZeroDivisionError:
        K = 0.0001
    if K <= 0.0001:
        K = 0.0001
    return K

def function11a(m, PHIS, PHICL, C, CF, PHIT_REM, VSILT_REM, VCLW_REM, rg, permeability, PERM_OPTION, A_PERM_CH, B_PERM_CH):
    if PERM_OPTION == 'NO':
        rg1 = A_PERM_CH
        b1 = B_PERM_CH
    else:
        if CF > 1.4 * C:
            CF = 1.4 * C
        slope = (C - CF) / (PHIS - PHICL)
        constant = -slope * PHICL + CF
        c1 = PHIT_REM * slope + constant
        b1 = m * (2 / c1 + 1) + 2
        rg1 = rg ** 2 / 80
    try:
        K = rg1 * PHIT_REM ** b1 / 10 ** (6 * VCLW_REM + 3 * VSILT_REM)
    except OverflowError:
        K = permeability
    except ValueError:
        K = 0.0001
    except ZeroDivisionError:
        K = 0.0001
    try:
        if K <= 0.0001:
            K = 0.0001
    except TypeError:
        K = 0.0001
    return K

def function11b(m, PHIS, PHICL, C, CF, PHIT_REM, VSILT_REM, VCLW_REM, rg):
    slope = (C - CF) / (PHIS - PHICL)
    constant = -slope * PHICL + CF
    c1 = PHIT_REM * slope + constant
    b1 = m * (2 / c1 + 1) + 2
    rg1 = rg ** 2 / 80
    try:
        K = rg1 * PHIT_REM ** b1 / 10 ** (6 * VCLW_REM + 3 * VSILT_REM)
    except OverflowError:
        K = 100000
    except ValueError:
        K = 0.0001
    if K <= 0.0001:
        K = 0.0001
    return K

def calcPc(TVDSS, GWC_DEPTH_ft, OWC_DEPTH_ft, GOC_DEPTH_ft, GAS_GRAD, OIL_GRAD, WTR_GRAD, SCOSTG, SCOSTO):
    Pc = 0
    IFT = MissingValue
    if GWC_DEPTH_ft > 0:
        if TVDSS < GWC_DEPTH_ft:
            HAFWL = GWC_DEPTH_ft - TVDSS
            Pc = HAFWL * (WTR_GRAD - GAS_GRAD)
            IFT = SCOSTG
    elif OWC_DEPTH_ft > 0:
        if TVDSS < OWC_DEPTH_ft:
            HAFWL = OWC_DEPTH_ft - TVDSS
            Pc = HAFWL * (WTR_GRAD - OIL_GRAD)
            IFT = SCOSTO
        if TVDSS < GOC_DEPTH_ft:
            HAFWL = OWC_DEPTH_ft - TVDSS
            Pc = (OWC_DEPTH_ft - GOC_DEPTH_ft) * (WTR_GRAD - OIL_GRAD) + (GOC_DEPTH_ft - TVDSS) * (WTR_GRAD - GAS_GRAD)
            IFT = SCOSTG
    return (Pc, IFT)

def function12(vshale, porosity, grainradius, interfacialtension, b0, dtvd, m, compactionfactor, CF, capillarypressure, PHIS, PHICL):
    vsilt = function4(vshale, porosity)
    vclw = vshale - vsilt
    permeability = function11b(m, PHIS, PHICL, compactionfactor, CF, porosity, vsilt, vclw, grainradius)
    swb = function6(vshale)
    phie = porosity * (1 - swb)
    vsand = 1 - vshale - porosity
    if vsand < 0:
        vsand = 0
    shf = function7a(dtvd, permeability, porosity, swb, capillarypressure, interfacialtension, b0)
    swe = 1 - porosity / phie * (1 - shf)
    vclb = porosity - phie
    vhc = (1 - shf) * porosity
    vwater = 1 - vclw - vsilt - vsand - vhc
    vcld = vclw - vclb
    return (vsilt, vcld, permeability, swb, phie, vsand, shf, swe, vclb, vhc, vwater, vclw)

def getMax(a, b):
    if a >= b:
        return a
    return b

def getMin(a, b):
    if a <= b:
        return a
    return b

def functionA(vclw, vshale, phit, phie, PHIS):
    try:
        PHISS1 = phie / (1 - vclw)
    except ZeroDivisionError:
        PHISS1 = PHIS
    PHISS2 = getMin(PHIS, PHISS1)
    if vshale > 0.95:
        PHISS3 = phit
    else:
        PHISS3 = PHISS2
    PHISSt = getMax(PHISS3, phit)
    return PHISSt

def functionB(phit):
    AChoo = 20000000
    Cfperm = -1.6 * phit + 1.64
    BChoo = 1.75 * (2 / Cfperm + 1) + 2
    return (AChoo, BChoo)

def functionB2(GRAIN_RADIUS_nm, m, C):
    AChoo = 0.0125 * GRAIN_RADIUS_nm ** 2
    BChoo = m * (2 / C + 1) + 2
    return (AChoo, BChoo)

def functionC(A, B, MinVCLW, MaxPERM, PHISSt, vshale, vsilt, perm):
    try:
        kss1 = A * PHISSt ** B / 10 ** (6 * MinVCLW + 3 * vsilt)
    except OverflowError:
        kss1 = MaxPERM
    except ValueError:
        kss1 = perm
    if vshale > 0.95:
        kss2 = perm
    else:
        kss2 = kss1
    kss3 = getMax(perm, kss2)
    Ksst = getMin(MaxPERM, kss3)
    return Ksst

def functionD(MinVCLW, Swb, PHICL, phit):
    if phit <= 0:
        return 1
    Swbss1 = MinVCLW * PHICL / phit
    Swbsst = getMin(Swb, Swbss1)
    return Swbsst

def functionE(TVDSS, gw, gh, IFT, b0, Ksst, PHISSt, Swbsst, FWL):
    HAFWL = FWL - TVDSS
    if HAFWL > 0:
        Pc = (gw - gh) * HAFWL
        J = 0.2166 * Pc / IFT * (Ksst / PHISSt) ** 0.5
        term1 = 10 ** ((2 * b0 - 1) * math.log10(1 + TechlogMath.inv(Swbsst)) + math.log10(1 + Swbsst))
        term2 = b0 / 3 * math.log10(1 + TechlogMath.inv(Swbsst))
        Swsst = term1 / J ** term2
    else:
        Swsst = 1
    Swsst = getMin(Swsst, 1)
    return Swsst

def functionE2(TVDSS, Pc, IFT, b0, Ksst, PHISSt, Swbsst):
    try:
        if Pc > 0:
            J = 0.2166 * Pc / IFT * (Ksst / PHISSt) ** 0.5
            term1 = 10 ** ((2 * b0 - 1) * math.log10(1 + TechlogMath.inv(Swbsst)) + math.log10(1 + Swbsst))
            term2 = b0 / 3 * math.log10(1 + TechlogMath.inv(Swbsst))
            Swsst = term1 / J ** term2
        else:
            Swsst = 1
    except ValueError:
        Swsst = 1
    return Swsst

def functionF(phit, swt, PHISSt, Swsst, vshale, TVDSS, FWL):
    HAFWL = FWL - TVDSS
    if HAFWL > 0:
        SSF3 = phit * (1 - swt) / (PHISSt * (1 - Swsst))
    else:
        SSF3 = -0.2852 * vshale ** 2 - 0.865 * vshale + 1.077
    SSF4 = getMin(1, SSF3)
    SSF = getMax(0, SSF4)
    return SSF

def functionF2(phit, swt, PHISSt, Swsst, vshale, TVDSS, Pc):
    if Pc > 0:
        SSF3 = phit * (1 - swt) / (PHISSt * (1 - Swsst))
    else:
        SSF3 = -0.2852 * vshale ** 2 - 0.865 * vshale + 1.077
    SSF4 = getMin(1, SSF3)
    SSF = getMax(0, SSF4)
    return SSF

def functionF2a(phit, swt, PHISSt, Swsst, vshale, TVDSS, Pc):
    try:
        SSF3 = phit * (1 - swt) / (PHISSt * (1 - Swsst))
    except ZeroDivisionError:
        SSF3 = 0
    SSF4 = getMin(1, SSF3)
    SSF = getMax(0, SSF4)
    return SSF

def functionF2b(phit, vsilt, vclw, y0, y1, y2, y3):
    SSF = y1 * phit + y2 * vsilt + y3 * vclw + y0
    return SSF

def functionF2c(phit, swt, PHISSt, Swsst, vshale, TVDSS, Pc, CONST0, CONST1, CONST2):
    if Pc > 0:
        SSF3 = phit * (1 - swt) / (PHISSt * (1 - Swsst))
    else:
        SSF3 = CONST2 * vshale ** 2 + CONST1 * vshale + CONST0
    SSF4 = getMin(1, SSF3)
    SSF = getMax(0, SSF4)
    return SSF

def functionG2(phit, perm, swt, PHISSt, kSSt, Swsst, SSF, Pc):
    if SSF > 0:
        PHISS = PHISSt
        kss = kSSt
        Swss = Swsst
    else:
        PHISS = phit
        kss = perm
        Swss = swt
    if Pc <= 0:
        Swss = 1
    return (PHISS, kss, Swss)

def functionH(phie, phit, vclw, vsilt, vshale, perm, swt, Swb, TVDSS, FWL, gw, gh, IFT, b0, GRAIN_RADIUS_nm, m, C, PHIS, PHICL, MinVCLW, MaxPERM):
    PHISSt = functionA(vclw, vshale, phit, phie, PHIS)
    A, B = functionB2(GRAIN_RADIUS_nm, m, C)
    Ksst = functionC(A, B, MinVCLW, MaxPERM, PHISSt, vshale, vsilt, perm)
    Swbsst = functionD(MinVCLW, Swb, PHICL, phit)
    Swsst = functionE(TVDSS, gw, gh, IFT, b0, Ksst, PHISSt, Swbsst, FWL)
    SSF = functionF(phit, swt, PHISSt, Swsst, vshale, TVDSS, FWL)
    PHISS, kss, Swss = functionG(phit, perm, swt, PHISSt, kSSt, Swsst, SSF)
    return (PHISS, kss, Swss, SSF)

def functionH2(phie, phit, vclw, vsilt, vshale, perm, swt, Swb, TVDSS, Pc, IFT, b0, GRAIN_RADIUS_nm, m, C, PHIS, PHICL, MinVCLW, MaxPERM):
    PHISSt = functionA(vclw, vshale, phit, phie, PHIS)
    A, B = functionB2(GRAIN_RADIUS_nm, m, C)
    Ksst = functionC(A, B, MinVCLW, MaxPERM, PHISSt, vshale, vsilt, perm)
    Swbsst = functionD(MinVCLW, Swb, PHICL, phit)
    Swsst = functionE2(TVDSS, Pc, IFT, b0, Ksst, PHISSt, Swbsst)
    SSF = functionF2(phit, swt, PHISSt, Swsst, vshale, TVDSS, Pc)
    PHISS, kss, Swss = functionG2(phit, perm, swt, PHISSt, Ksst, Swsst, SSF, Pc)
    return (PHISS, kss, Swss, SSF)

def functionH2a(phie, phit, vclw, vsilt, vshale, perm, swt, Swb, TVDSS, Pc, IFT, b0, GRAIN_RADIUS_nm, m, C, PHIS, PHICL, MinVCLW, MaxPERM):
    PHISSt = functionA(vclw, vshale, phit, phie, PHIS)
    A, B = functionB2(GRAIN_RADIUS_nm, m, C)
    Ksst = functionC(A, B, MinVCLW, MaxPERM, PHISSt, vshale, vsilt, perm)
    Swbsst = functionD(MinVCLW, Swb, PHICL, phit)
    Swsst = functionE2(TVDSS, Pc, IFT, b0, Ksst, PHISSt, Swbsst)
    SSF = functionF2a(phit, swt, PHISSt, Swsst, vshale, TVDSS, Pc)
    PHISS, kss, Swss = functionG2(phit, perm, swt, PHISSt, Ksst, Swsst, SSF, Pc)
    return (PHISS, kss, Swss, SSF)

def functionH2b(phie, phit, vclw, vsilt, vshale, perm, swt, Swb, TVDSS, Pc, IFT, b0, GRAIN_RADIUS_nm, m, C, PHIS, PHICL, MinVCLW, MaxPERM, y0, y1, y2, y3):
    PHISSt = functionA(vclw, vshale, phit, phie, PHIS)
    A, B = functionB2(GRAIN_RADIUS_nm, m, C)
    Ksst = functionC(A, B, MinVCLW, MaxPERM, PHISSt, vshale, vsilt, perm)
    Swbsst = functionD(MinVCLW, Swb, PHICL, phit)
    Swsst = functionE2(TVDSS, Pc, IFT, b0, Ksst, PHISSt, Swbsst)
    SSF = functionF2b(phit, vsilt, vclw, y0, y1, y2, y3)
    PHISS, kss, Swss = functionG2(phit, perm, swt, PHISSt, Ksst, Swsst, SSF, Pc)
    return (PHISS, kss, Swss, SSF)

def functionH2c(phie, phit, vclw, vsilt, vshale, perm, swt, Swb, TVDSS, Pc, IFT, b0, GRAIN_RADIUS_nm, m, C, PHIS, PHICL, MinVCLW, MaxPERM, CONST0, CONST1, CONST2):
    PHISSt = functionA(vclw, vshale, phit, phie, PHIS)
    A, B = functionB2(GRAIN_RADIUS_nm, m, C)
    Ksst = functionC(A, B, MinVCLW, MaxPERM, PHISSt, vshale, vsilt, perm)
    Swbsst = functionD(MinVCLW, Swb, PHICL, phit)
    Swsst = functionE2(TVDSS, Pc, IFT, b0, Ksst, PHISSt, Swbsst)
    SSF = functionF2c(phit, swt, PHISSt, Swsst, vshale, TVDSS, Pc, CONST0, CONST1, CONST2)
    PHISS, kss, Swss = functionG2(phit, perm, swt, PHISSt, Ksst, Swsst, SSF, Pc)
    return (PHISS, kss, Swss, SSF)

def SSF3MultiLinearRegression(SSF3, phit, vsilt, vclw):
    SSF3 = np.array(SSF3)
    phit = np.array(phit)
    vsilt = np.array(vsilt)
    vclw = np.array(vclw)
    er = [1] * len(SSF3)
    er = np.array(er)
    SSF3 = np.asmatrix(SSF3).T
    phit = np.asmatrix(phit).T
    vsilt = np.asmatrix(vsilt).T
    vclw = np.asmatrix(vclw).T
    er = np.asmatrix(er).T
    x = np.bmat([er, phit, vsilt, vclw])
    xtranspose = x.T
    xtransposex = np.matmul(xtranspose, x)
    xtransposey = np.matmul(xtranspose, SSF3)
    xtransposex_inverse = xtransposex.I
    b = np.matmul(xtransposex_inverse, xtransposey)
    Ymean = SSF3.mean()
    Ymean2 = Ymean * Ymean
    nYmean2 = len(SSF3) * Ymean2
    ESS = np.matmul(b.T, xtransposey) - nYmean2
    TSS = np.matmul(SSF3.T, SSF3) - nYmean2
    R2 = ESS / TSS
    print('SSF3 = %.4f * PHIT + %.4f * VSILT + %.4f * VCLW + %.4f' % (b[1], b[2], b[3], b[0]))
    print('R2 value = %.4f' % R2)
    return (b, R2)
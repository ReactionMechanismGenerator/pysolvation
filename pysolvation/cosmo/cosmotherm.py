import os
import subprocess

class COSMOOutput:
    """
    Class for storing the output of a COSMOtherm job parsed from a .tab file
    intended to be able to store any results, but currently can only
    store results of GSOLV henry and flashpoint calculations
    """
    def __init__(self,spcs,mole_fractions,H=None,Lngamma=None,Pvap=None,
                 Gsolv=None,T=None,Tflash=None,PVsat=None):
        self.mole_fractions = mole_fractions
        if H:
            self.H = {spcs[i]:H[i] for i in range(len(spcs))}
        else:
            self.H = None
        if Lngamma:
            self.Lngamma = {spcs[i]:Lngamma[i] for i in range(len(spcs))}
        else:
            self.Lngamma = None
        if Pvap:
            self.Pvap = {spcs[i]:Pvap[i] for i in range(len(spcs))}
        else:
            self.Pvap = None
        if Gsolv:
            self.Gsolv = {spcs[i]:Gsolv[i] for i in range(len(spcs))}
        else:
            self.Gsolv = None
        if T:
            self.T = T
        else:
            self.T = None
        if Tflash:
            self.Tflash = Tflash
        else:
            self.Tflash = None
        if PVsat:
            self.PVsat = PVsat
        else:
            self.PVsat = None

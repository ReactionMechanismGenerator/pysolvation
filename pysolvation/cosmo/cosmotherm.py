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

class COSMOJob:
    """
    Class for running COSMOtherm jobs. Generates input file runs COSMOtherm parses output
    file. Currently can only supports GSOLV, henry and flashpoint calculations.
    species should be a list of COSMOSpecies objects, mole_fractions should be a dictionary mapping
    COSMOSpecies objects to mole fractions
    The type of job is determined by the requested_outputs currently supports:
    ["GSOLV","henry","flashpoint"]
    path is where you want the files saved and the name denoted on the files
    path = /directory/H2O will give you /directory/H2O.inp /directory/H2O.tab etc.
    the COSMOOutput objects are stored in the cosmo_outputs attribute
    """
    supported_outputs = ["GSOLV","henry","flashpoint"]

    def __init__(self,species,mole_fractions=None,requested_outputs=["GSOLV"],Tlist=[298.0],path="",
                 level="TZVPD-FINE"):
        if mole_fractions is None and len(species) == 1:
            mole_fractions = {species[0]:1.0}
        elif mole_fractions is None:
            raise ValueError("Must specify mole fractions if more than one species")
        self.species = species
        self.mole_fractions = mole_fractions
        if any([output not in self.supported_outputs for output in requested_outputs]):
            raise ValueError("Only {} outputs are supported".format(self.supported_outputs))
        self.requested_outputs = requested_outputs
        self.Tlist = Tlist
        self.path = path #no suffix path
        self.cosmo_outputs = []
        self.level = level

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

    def generate_input_file(self):
        """
        Create COSMO input file for job
        """
        if self.level == 'TZVPD-FINE':
            first_lines = 'ctd = BP_TZVPD_FINE_20.ctd '
        elif self.level == 'TZVP':
            first_lines = 'ctd = BP_TZVP_20.ctd '
        else:
            print(f'{level} is  a wrong input for level')

        if not "COSMOTHERMPATH" in os.environ.keys():
            raise ValueError("""$COSMOTHERMPATH environment variable not defined assign path
                             of the COSMOtherm directory ex: /home/gridsan/groups/RMG/Software/COSMOtherm2021""")
        else:
            cosmo_path = os.environ["COSMOTHERMPATH"]

        first_lines += '''cdir = "{cosmo_path}/COSMOthermX/../COSMOtherm/CTDATA-FILES" ldir = "{cosmo_path}/COSMOthermX/../licensefiles"
notempty wtln ehfile
!! generated by COSMOthermX !!
'''
        first_lines = first_lines.format(cosmo_path=cosmo_path)

        with open("".join((self.path,".inp")), 'wt') as f:
            f.write(first_lines)
            mole_fraction_string = ""
            for spc in self.species:
                mf = self.mole_fractions[spc]
                mole_fraction_string += " " + str(mf)
                f.write("f = \"" + spc.name + "_c0.cosmo\" fdir=\"" + spc.path + "\"")
                if int(spc.n_conf) > 1:
                    f.write(" Comp = \"" + spc.name + "\" [ VPfile")
                    for k in range(1, int(spc.n_conf)):
                        f.write("\nf = \"" + spc.name + "_c" + str(k) + ".cosmo\" fdir=\"" + spc.path + "\"")
                    f.write(" ]\n")
                else:
                    f.write(" VPfile\n")
            if "GSOLV" in self.requested_outputs or "henry" in self.requested_outputs:
                for T in self.Tlist:
                    f.write("henry xh={"+mole_fraction_string + "} tk=" + str(T) + " GSOLV \n")
            if "flashpoint" in self.requested_outputs:
                f.write("flashpoint tc=25.0 x={"+mole_fraction_string+"}use_tboil use_pvapt\n")

        return

    def process_output(self):
        """
        Read output from .tab file
        Store the output in a COSMOOutput object
        Delete all files associated with the job
        """
        index = 0
        jobtype = ""
        with open("".join((self.path,".tab")), 'r') as f:
            for line in f.readlines():

                spl = line.split()
                if len(spl) > 0:
                    if spl[0] == "Property":
                        if jobtype == "Henry law coefficients H":
                            self.cosmo_outputs.append(COSMOOutput(self.species,self.mole_fractions,
                                                                      H=Hs,Lngamma=Lngammas,Pvap=Pvaps,
                                                                      Gsolv=Gsolvs,T=self.Tlist[index-1]))
                        jobtype = " ".join(spl[4:-1])
                    s = line.split()[0].strip()
                else:
                    s = ""

                if s.isdigit() and jobtype == "Henry law coefficients H":
                    if s == "1":
                        index += 1
                        Hs = []
                        Lngammas = []
                        Pvaps = []
                        Gsolvs = []
                    outs = line.split()
                    H = outs[2]
                    Lngamma = outs[3]
                    Pvap = outs[4]
                    Gsolv = outs[5]
                    Hs.append(float(H)*100000.0)
                    Lngammas.append(float(Lngamma))
                    Pvaps.append(float(Pvap)*100000.0)
                    Gsolvs.append(float(Gsolv)*4184.0)

                elif s != "" and s[0].isdigit() and jobtype == "Flash point temperature":
                    Tflash = float(spl[0])
                    PVsat = float(spl[1])*100.0
                    self.cosmo_outputs.append(COSMOOutput(self.species,self.mole_fractions,
                                                          Tflash=Tflash,PVsat=PVsat))
            else:
                if jobtype == "Henry law coefficients H":
                    self.cosmo_outputs.append(COSMOOutput(self.species,self.mole_fractions,
                                                                  H=Hs,Lngamma=Lngammas,Pvap=Pvaps,
                                                                  Gsolv=Gsolvs,T=self.Tlist[index-1]))

        os.remove("".join((self.path,".inp")))
        os.remove("".join((self.path,".tab")))
        os.remove("".join((self.path,".out")))
        os.remove("".join((self.path,"_status.xml")))

    def run(self):
        """
        Run the COSMOtherm job
        """
        self.generate_input_file()
        if not "COSMOTHERM" in os.environ.keys():
            raise ValueError("""$COSMOTHERM environment variable not defined assign
                path of the COSMOtherm executable ex: /home/gridsan/groups/RMG/Software/COSMOtherm2021/COSMOtherm/BIN-LINUX/cosmotherm""")
        cmd = [os.environ["COSMOTHERM"], "".join((self.path,".inp"))]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
        self.process_output()

def calculate_dG_dH_solutes(solvent_mole_fractions,cosmo_solute_db,T=298.15,dT=1.0):
    """
    Primarily for calculating solvent parameters
    takes in the dictionary of mole fractions {COSMOSpecies:0.2}
    and a database of Solute objects
    generates dictionaries mapping solute inchis to dGsolv and dHsolv
    """
    spcs = list(solvent_mole_fractions.keys())
    spcs.append(solute)
    dGsolv_dict = dict()
    dHsolv_dict = dict()
    for solute in cosmo_solute_db.spcs:
        mole_fractions = deepcopy(solvent_mole_fractions)
        solvent_mole_fractions[solute] = 0.0
        try:
            job = COSMOJob(species=spcs,mole_fractions=mole_fractions,
                       cosmo_path=cosmotherm2021_path,cosmo_executable=cosmotherm_command,
                       path=solute.name,Tlist=[T-dT,T,T+dT])
            job.run()
            Gsolvs = [output.Gsolv[solute] for output in job.cosmo_outputs]
            Gsolv = Gsolvs[1]
            Ssolv = -(Gsolvs[2]-Gsolvs[0])/(2.0*dT)
            Hsolv = Gsolv + T*Ssolv
            dGsolv_dict[solute.inchi] = Gsolv
            dHsolv_dict[solute.inchi] = Hsolv
        except:
            print("Couldn't run:")
            print(solute.smiles)

    return dGsolv_dict,dHsolv_dict

import os
import subprocess
from cosmo.cosmotherm import COSMOSpecies

class TurbomoleJob:
    """
    Class for running Turbomole jobs relevant to solvation.
    path is where you want the files saved and the name denoted on the files
    path = /directory/H2O will give you /directory/H2O.inp /directory/H2O.tab etc.
    the COSMOOutput objects are stored in the cosmo_outputs attribute
    """

    def __init__(self,name,xyz,charge,multiplicity,path="",cosmo_level="BP-TZVPD-FINE-COSMO-SP",
                energy_level="BP-TZVPD-GAS-SP"):
        self.name = name
        self.xyz = xyz.strip()
        self.charge = charge
        self.multiplicity = multiplicity
        self.cosmo_level = cosmo_level
        self.energy_level = energy_level
        self.path = path
        self.num_atoms = xyz.count('\n') + 1
        self.output_energy_file = None
        self.output_cosmo_file = None

    def generate_input_file(self):
        """
        Create Turbomole input files for job
        """
        try:
            os.mkdir(os.path.join(self.path,"xyz"))
        except:
            pass

        with open(os.path.join(self.path,self.name+".txt"),'wt') as f:
            f.write(self.name+" "+str(self.charge)+" "+str(self.multiplicity))

        with open(os.path.join(self.path,"xyz",self.name+".xyz"),"wt") as f:
            f.write(str(self.num_atoms)+"\n\n"+self.xyz)

        return

    def process_output(self):
        """
        checks that the output file is there
        """
        os.rename(os.path.join(self.path,"CosmofilesBP-TZVPD-FINE-COSMO-SP",self.name+".cosmo"),
                 os.path.join(self.path,self.name+"_c0.cosmo"))
        os.rename(os.path.join(self.path,"EnergyfilesBP-TZVPD-FINE-COSMO-SP",self.name+".energy"),
                 os.path.join(self.path,self.name+"_c0.energy"))
        if os.path.isfile(os.path.join(self.path,self.name+"_c0.energy")):
            self.output_energy_file = os.path.abspath(os.path.join(self.path,self.name+"_c0.energy"))
        if os.path.isfile(os.path.join(self.path,self.name+"_c0.cosmo")):
            self.output_cosmo_file = os.path.abspath(os.path.join(self.path,self.name+"_c0.cosmo"))
        os.remove(os.path.join(self.path,"xyz",self.name+".xyz"))
        os.remove(os.path.join(self.path,self.name+".txt"))

    def run(self):
        """
        Run the COSMOtherm job
        """
        self.generate_input_file()
        #Note you need to have sourced Turbomole for this to work
        #ex: source /home/gridsan/groups/RMG/Software/TmoleX19/TURBOMOLE/Config_turbo_env
        cmd = ['calculate', '-l', self.name+'.txt','-m',self.cosmo_level,'-f','xyz','-din','xyz','>',self.name+'.log']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
        cmd = ['calculate', '-l', self.name+'.txt','-m',self.energy_level,'-f','xyz','-din','xyz','>',self.name+'.log']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
        self.process_output()

def turbomoletospecies(name,inchi,smiles,job):
    if not isinstance(job,list):
        path = os.path.split(job.output_cosmo_file)[0]
        return COSMOSpecies(name,inchi,smiles,1,path)
    else:
        raise ValueError("Cannot handle more than 1 conformer yet")

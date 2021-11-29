from pysolvation.database import InchiKeyedDatabase
import pandas as pd

class COSMOSpecies:
    """
    Object holding all the information necessary for
    """
    def __init__(self, name, inchi, smiles, n_conf, path):
        self.name = name
        self.inchi = inchi
        self.smiles = smiles
        self.n_conf = n_conf
        self.path = path

class COSMODatabase(InchiKeyedDatabase):
    """
    Database for holding COSMOSpecies objects
    """
    def __init__(self,spcs,level):
        super().__init__(spcs)
        self.level = level

def database_summary_to_species(path):
    """
    Loads COSMOSpecies objects from a csv
    """
    db = pd.read_csv(path)
    spcs =  []
    for i in range(len(db)):
        spcs.append(COSMOSpecies(name=db["cosmo name"][i],
                                inchi=db["inchi"][i],
                                smiles=db["smiles"][i],
                                n_conf=db["number of conformers"][i],
                                path=db["file path"][i]))
    return spcs

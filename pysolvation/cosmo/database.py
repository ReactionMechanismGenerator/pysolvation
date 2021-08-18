from database import InchiKeyedDatabase
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

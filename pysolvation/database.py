from rdkit import Chem

class InchiKeyedDatabase:
    def __init__(self,spcs):
        self.spcs = spcs

    def get_species_inchi(self,inchi):
        for spc in self.spcs:
            if spc.inchi == inchi:
                return spc
        else:
            return None

    def get_species_smiles(self,smiles):
        mol = Chem.MolFromSmiles(smiles)
        inchi = Chem.MolToInchi(mol, options='/FixedH')
        return self.get_species_inchi(inchi)

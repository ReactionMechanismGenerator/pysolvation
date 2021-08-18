import pandas as pd

class Solute:
    """
    Stores Solute identifiers and parameters
    """
    def __init__(self,smiles,inchi,E,S,A,B,L):
        self.smiles = smiles
        self.inchi = inchi
        self.E = E
        self.S = S
        self.A = A
        self.B = B
        self.L = L

def load_solutes(path):
    """
    Function for loading Solute objects from a csv
    with the solute parameters and smiles and inchi identifiers
    """
    db = pd.read_csv(path)
    spcs =  []
    for i in range(len(db)):
        spcs.append(Solute(smiles=db["smiles"][i],
                                inchi=db["inchi"][i],
                                E=db["E"][i],
                                S=db["S"][i],
                                A=db["A"][i],
                                B=db["B"][i],
                                L=db["L"][i]))
    return spcs

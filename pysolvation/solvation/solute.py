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


class Solvent:
    """
    Stores Solvent identifiers and parameters
    """
    def __init__(self,name,smiles,inchi,cg,eg,sg,ag,bg,lg,ch,eh,sh,ah,bh,lh):
        self.smiles = smiles
        self.inchi = inchi
        self.cg = cg
        self.eg = eg
        self.sg = sg
        self.ag = ag
        self.bg = bg
        self.lg = lg
        self.ch = ch
        self.eh = eh
        self.sh = sh
        self.ah = ah
        self.bh = bh
        self.lh = lh

def getsolvrmgdb(rmgdb,curated_names=None):
    solvlib = rmgdb.solvation.libraries['solvent']
    solvs = []
    for index,entry in solvlib.entries.items():
        if len(entry.item) > 1:
            continue #ignore mixture solvents

        if curated_names and not (entry.label in curated_names):
            continue

        spc = entry.item[0]
        mol = Chem.MolFromSmiles(spc.smiles)
        inchi = Chem.MolToInchi(mol, options='/FixedH')
        d = entry.data
        solv = Solvent(entry.label,spc.smiles,inchi,d.c_g,d.e_g,d.s_g,d.a_g,d.b_g,d.l_g,
                       d.c_h,d.e_h,d.s_h,d.a_h,d.b_h,d.l_h)
        solvs.append(solv)
    return InchiKeyedDatabase(solvs)

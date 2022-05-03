import numpy as np
from sklearn import linear_model
from sklearn.cross_decomposition import PLSRegression
from scipy.optimize import least_squares, minimize, fsolve, shgo, dual_annealing

def loss_function(x,A,b):
    return np.mean(np.abs(np.dot(A,x)-b))

def linear_fit(A,b):
    """
    Attempts to use three methods: Linear Regression, Least Squares
    and Dual Annealing to fit the best x to minimize |Ax-b|
    returns the best found parameters, the loss_function value at the
    best found parameters and the string for the method used
    """
    reg = linear_model.LinearRegression()
    reg.fit(A, b)
    lrparam = reg.coef_.tolist()
    lrparam[-1] = reg.intercept_

    param = least_squares(loss_function, lrparam, args=(A,b))
    lsparam = param.x

    bound   = [(-5, 10), # (lower bound for e,  upper bound for e)
                       (-8, 10),  # (lower bound for s,  upper bound for s)
                       (-2, 12), # (lower bound for a, upper bound for a)
                       (-2, 25), # (lower bound for b, upper bound for b)
                       (-1, 3), # (lower bound for l, upper bound for l)
                       (-6, 6)] # (lower bound for c, upper bound for c)

    param   = dual_annealing(loss_function,bound,args=(A,b))

    daparam = param.x

    xs = [lrparam,lsparam,daparam]
    methods = ["LR","LS","DA"]
    vals = [loss_function(x,A,b) for x in xs]
    ind = np.argmin(vals)

    return xs[ind],vals[ind],methods[ind]

def fit_solvent_parameters(solute_db,dGsolv_dict,dHsolv_dict,T=298.15):
    """
    fits solvent parameters to the species in the dGsolv_dict nad dHsolv_dict
    where these dictionaries map inchis to dG or dH in J/mol
    assumes each of these species is in solute_db
    returns a dictionary mapping labels to the fitted solvent parameters
    the MAE in dG and the MAE in dH in J/mol
    """
    inchis = list(dGsolv_dict.keys())
    dGsolv = [dGsolv_dict[inchi] for inchi in inchis]
    dHsolv = [dHsolv_dict[inchi] for inchi in inchis]

    log10K = (-np.array(dGsolv)/(np.log(10)*8.314*298.15))
    dHsolvkJmol = np.array(dHsolv)/1000.0
    Es = [solute_db.get_species_inchi(inchi).E for inchi in inchis]
    Ss = [solute_db.get_species_inchi(inchi).S for inchi in inchis]
    As = [solute_db.get_species_inchi(inchi).A for inchi in inchis]
    Bs = [solute_db.get_species_inchi(inchi).B for inchi in inchis]
    Ls = [solute_db.get_species_inchi(inchi).L for inchi in inchis]
    A = np.array([Es,Ss,As,Bs,Ls,np.ones(len(Es))]).T

    dG_params,MAE_log10K,_ = linear_fit(A,log10K)
    dH_params,MAE_dHsolvkJmol,_ = linear_fit(A,dHsolvkJmol)

    param_dict = dict()
    param_dict["e_g"] = dG_params[0]
    param_dict["s_g"] = dG_params[1]
    param_dict["a_g"] = dG_params[2]
    param_dict["b_g"] = dG_params[3]
    param_dict["l_g"] = dG_params[4]
    param_dict["c_g"] = dG_params[5]

    param_dict["e_h"] = dH_params[0]
    param_dict["s_h"] = dH_params[1]
    param_dict["a_h"] = dH_params[2]
    param_dict["b_h"] = dH_params[3]
    param_dict["l_h"] = dH_params[4]
    param_dict["c_h"] = dH_params[5]

    return param_dict,MAE_log10K*np.log(10.0)*8.314*T,MAE_dHsolvkJmol*1000.0

def fit_solute_parameters(solvent_db,dGsolv_dict,dHsolv_dict,T=298.15):
    """
    fits solute parameters to the species in the dGsolv_dict and dHsolv_dict
    where these dictionaries map inchis to dG or dH in J/mol
    assumes each of these species is in solute_db
    returns a dictionary mapping labels to the fitted solvent parameters
    the MAE in dG and the MAE in dH in J/mol
    """
    inchis = list(dGsolv_dict.keys())
    dGsolv = [dGsolv_dict[inchi] for inchi in inchis]
    dHsolv = [dHsolv_dict[inchi] for inchi in inchis]

    log10K = (-np.array(dGsolv)/(np.log(10)*8.314*T))
    dHsolvkJmol = np.array(dHsolv)/1000.0
    A = []
    b = []
    scalefactor = np.log(10)*8.314*T/1000.0
    for i,inchi in enumerate(inchis):
        solv = solvent_db.get_species_inchi(inchi)
        if solv.cg:
            print(solv.smiles)
            A.append((scalefactor*np.array([solv.eg,solv.sg,solv.ag,solv.bg,solv.lg])).tolist())
            b.append((log10K[i]-solv.cg)*scalefactor)
#         if solv.ch:
#             A.append([solv.eh,solv.sh,solv.ah,solv.bh,solv.lh])
#             b.append(dHsolvkJmol[i]-solv.ch)

    A = np.array(A)
    b = np.array(b)

    params,MAE,_ = linear_fit(A,b)

    param_dict = dict()
    param_dict["E"] = params[0]
    param_dict["S"] = params[1]
    param_dict["A"] = params[2]
    param_dict["B"] = params[3]
    param_dict["L"] = params[4]

    return param_dict,MAE*1000

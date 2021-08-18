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

    param = least_squares(loss_function, lrparam, args=(A,log10K))
    lsparam = param.x

    bound   = [(-5, 10), # (lower bound for e,  upper bound for e)
                       (-8, 10),  # (lower bound for s,  upper bound for s)
                       (-2, 12), # (lower bound for a, upper bound for a)
                       (-2, 25), # (lower bound for b, upper bound for b)
                       (-1, 3), # (lower bound for l, upper bound for l)
                       (-6, 6)] # (lower bound for c, upper bound for c)

    param   = dual_annealing(loss_function,bound,args=(A,log10K))

    daparam = param.x

    xs = [lrparam,lsparam,daparam]
    methods = ["LR","LS","DA"]
    vals = [loss_function(x,A,b) for x in xs]
    ind = np.argmin(vals)

    return xs[ind],vals[ind],methods[ind]

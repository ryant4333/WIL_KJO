import numpy as np
from pymop.problems.zdt import ZDT6 as test6

def ZDT4(x):
    x = np.array(x)
    D = len(x)
    problem = test6(n_var=D)
    F = problem.evaluate(x)

    return F
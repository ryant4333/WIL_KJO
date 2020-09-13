import numpy as np
from pymop.problems.zdt import ZDT4 as test4

def ZDT4(x):
    x = np.array(x)
    D = len(x)
    problem = test4(n_var=D)
    F = problem.evaluate(x)

    return F
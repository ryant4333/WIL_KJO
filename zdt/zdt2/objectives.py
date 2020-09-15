import numpy as np
from pymop.problems.zdt import ZDT2 as test2

def ZDT2(x):
    D = len(x)
    problem = test2(n_var=D)
    F = problem.evaluate(x)

    return F

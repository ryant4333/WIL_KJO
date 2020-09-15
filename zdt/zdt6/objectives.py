import numpy as np
from pymop.problems.zdt import ZDT6 as test6

def ZDT6(x):
    D = len(x)
    problem = test6(n_var=D)
    F = problem.evaluate(x)

    return F
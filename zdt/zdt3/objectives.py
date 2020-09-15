import numpy as np
from pymop.problems.zdt import ZDT3 as test3

def ZDT3(x):
    D = len(x)
    problem = test3(n_var=D)
    F = problem.evaluate(x)

    return F
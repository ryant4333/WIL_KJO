import numpy as np
from pymop.problems.zdt import ZDT1 as test1

def ZDT1(x):
    D = len(x)
    problem = test1(n_var=D)
    F = problem.evaluate(x)
    return F
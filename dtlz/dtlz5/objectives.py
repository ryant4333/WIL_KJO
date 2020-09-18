import numpy as np
import pymop

def DTLZ5(x):
    D = len(x)
    problem = pymop.DTLZ5(n_var=D)
    F = problem.evaluate(x)
    return F
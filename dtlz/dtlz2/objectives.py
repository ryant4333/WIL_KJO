import numpy as np
import pymop

def DTLZ2(x):
    D = len(x)
    problem = pymop.DTLZ2(n_var=D)
    F = problem.evaluate(x)
    return F
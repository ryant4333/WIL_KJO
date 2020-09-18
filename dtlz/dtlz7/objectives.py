import numpy as np
import pymop

def DTLZ7(x):
    D = len(x)
    problem = pymop.DTLZ7(n_var=D)
    F = problem.evaluate(x)
    return F
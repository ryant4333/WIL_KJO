import numpy as np
import pymop

def DTLZ6(x):
    D = len(x)
    problem = pymop.DTLZ6(n_var=D)
    F = problem.evaluate(x)
    return F
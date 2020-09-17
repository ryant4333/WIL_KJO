import numpy as np
import pymop

def DTLZ1(x):
    D = len(x)
    problem = pymop.DTLZ1(n_var=D)
    F = problem.evaluate(x)
    return F
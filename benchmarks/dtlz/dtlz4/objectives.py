import numpy as np
import pymop

def DTLZ4(x):
    D = len(x)
    problem = pymop.DTLZ4(n_var=D)
    F = problem.evaluate(x)
    return F
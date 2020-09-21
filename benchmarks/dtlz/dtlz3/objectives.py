import numpy as np
import pymop

def DTLZ3(x):
    D = len(x)
    problem = pymop.DTLZ3(n_var=D)
    F = problem.evaluate(x)
    return F
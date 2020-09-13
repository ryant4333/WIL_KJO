import numpy as np
import math

def viennet(x):
    x = np.array(x)
    f1 = (0.5*(x[0]**2 + x[1]**2)) + math.sin(x[0]**2 + x[1]**2)
    f2 = (((3 * x[0] + 2 * x[1] + 4) ** 2) / 8) + (((x[0] - x[1] + 1) ** 2) / 27) + 15
    f3 = 1/(x[0]**2 + x[1]**2 + 1) - (1.1 * math.exp(-(x[0] + x[1]**2)))
    return np.array([f1, f2, f3])

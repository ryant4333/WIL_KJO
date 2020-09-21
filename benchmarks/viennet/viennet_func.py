import math
import numpy as np

def viennet(input):
    x = input[0]
    y = input[1]
    
    z = x**2 + y**2
    
    f1 = 0.5 * z + math.sin(z)
    
    f2_1 = (3*x - 2*y + 4)**2
    f2_2 = (x-y+1)**2
    f2 = f2_1/8 + f2_2/27 + 15

    f3_1 = x**2 + y**2 + 1
    f3 = 1/f3_1 - 1.1*math.exp(-(z))

    out = np.array((f1, f2, f3))
    return out
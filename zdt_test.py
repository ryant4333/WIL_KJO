import numpy as np

def ZDT1(x):
    D = len(x)
    f1 = x[0]
    g = 1 + 9 * np.sum(x[1:D]  / (D-1))
    h = 1 - np.sqrt(f1 / g)
    f2 = g * h

    return [f1, f2]

def ZDT2(x):
    D = len(x)
    f1 = x[0]
    g = 1 + 9 * np.sum(x[1:D]  / (D-1))
    h = 1 - (f1 / g)**2
    f2 = g * h

    return [f1, f2]

def ZDT3(x):
    D = len(x)
    f1 = x[0]
    g = 1 + 9 * np.sum(x[1:D]  / (D-1))
    h = (1 - np.sqrt(f1/g)) - ((f1/g) * np.sin(10*np.pi*f1))
    f2 = g * h

    return [f1, f2]



parts = 30
x = np.random.rand(parts)
print(x)

objectiveValues = ZDT3(x)
print(objectiveValues)

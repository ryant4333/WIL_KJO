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

def ZDT4(x):
    #x[0] = between 0-1
    #x[1:D] = between -5 to 5
    #D = 2-10
    D = len(x)
    f1 = x[0]
    g = 1 + 10*(D-1) + np.sum(x[1:D]**2 - 10*np.cos(4*np.pi*x[1:D]))
    h = 1 - np.sqrt(f1/g)
    f2 = g * h

    return [f1, f2]

def genZDTInputs(D):
    x = np.random.rand(D)
    return x

x = genZDTInputs(30)
objectiveValues = [ZDT1(x), ZDT2(x), ZDT3(x)]
print(objectiveValues)

#ZDT4 has to have different initial values
import numpy as np
from pymop.problems.zdt import ZDT1 as test1
from pymop.problems.zdt import ZDT2 as test2
from pymop.problems.zdt import ZDT3 as test3
from pymop.problems.zdt import ZDT4 as test4
from pymop.problems.zdt import ZDT6 as test6

def ZDT1(x):
    x = np.array(x)
    D = len(x)
    problem = test1(n_var=D)
    F = problem.evaluate(x)
    return F


def ZDT2(x):
    x = np.array(x)
    D = len(x)
    problem = test2(n_var=D)
    F = problem.evaluate(x)

    return F


def ZDT3(x):
    x = np.array(x)
    D = len(x)
    problem = test3(n_var=D)
    F = problem.evaluate(x)

    return F


def ZDT4(x):
    x = np.array(x)
    D = len(x)
    problem = test4(n_var=D)
    F = problem.evaluate(x)

    return F

def ZDT6(x):
    x = np.array(x)
    D = len(x)
    problem = test6(n_var=D)
    F = problem.evaluate(x)

    return F


def genZDTInputs(D):
    x = np.random.rand(D)
    return x


def genZDT4Inputs(D):
    x1 = np.random.rand(1)
    x2 = np.random.uniform(-5, 5, D - 1)
    x = np.concatenate((x1, x2), axis=0)
    return x


if __name__ == "__main__":
    x = genZDTInputs(30)
    print('ZDT1-3 input:\n', x)
    print('ZDT1 output:', ZDT1(x))
    print('ZDT2 output:', ZDT2(x))
    print('ZDT3 output:', ZDT3(x))

    x = genZDT4Inputs(10)
    print('ZDT4 input:\n', x)
    print('ZDT4 output:', ZDT4(x))
    # ZDT4 has to have different initial values

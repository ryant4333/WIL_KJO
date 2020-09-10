import numpy as np
from pymop.problems.zdt import ZDT1 as test1
from pymop.problems.zdt import ZDT2 as test2
from pymop.problems.zdt import ZDT3 as test3
from pymop.problems.zdt import ZDT4 as test4
from pymop.problems.zdt import ZDT6 as test6
from pymop.factory import get_problem

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

def Kursawe(x):
    x = np.array(x)
    D = len(x)
    problem = get_problem("kursawe")
    F = problem.evaluate(x)

    return F

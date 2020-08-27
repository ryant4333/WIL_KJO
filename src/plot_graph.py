import matplotlib.pyplot as plt
import numpy as np
file = open('pareto_front').read().splitlines()
front = np.loadtxt('pareto_front')


def plot():

    plt.scatter(front[:, 0], front[:, 1], c='b')
    plt.title(r'ZDT1 Search Domain: $0\leq x_i\leq1,1\leq i\leq30.\mathrm{}$')
    plt.xlabel(r'$f_1(x)$')
    plt.ylabel(r'$f_2(x)$')
    plt.legend(["Pareto front"])
    plt.ylim(0,10)
    plt.xlim(0,10)
    plt.show()



if __name__ == "__main__":
    plot()



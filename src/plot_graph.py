import matplotlib.pyplot as plt
import numpy as np


def plot(title, x_range, y_range):
    front = np.loadtxt('front_output')
    plt.scatter(front[:, 0], front[:, 1], c='b')
    plt.title(title)
    plt.xlabel(r'$f_1(x)$')
    plt.ylabel(r'$f_2(x)$')
    plt.legend(["Front"])
    plt.ylim(y_range)
    plt.xlim(x_range)
    plt.show()


if __name__ == "__main__":

    plot(r'ZDT1 Search Domain: $0\leq x_i\leq1,1\leq i\leq30.\mathrm{}$', [0, 11], [0, 12])



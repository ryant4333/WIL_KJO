from zdt_test import ZDT1
from solution import Solution
import numpy as np

class Hypercubes:
    def __init__(self, d_min, d_max, objective, cube_count):

        self.cube_dict = {}

        s_min = objective(d_min)
        s_max = objective(d_max)
        
        key_dist = []
        self.bin_size = []
        for i in range(len(s_min)):
            key_dist.append(s_max[i] - s_min[i])
            self.bin_size.append(key_dist[i] / cube_count)

    def get_bin_key(self, sol):
        """
        input is solution object
        """
        key_list = []
        for i in range(len(sol.objectives)):
            key_val = int(sol.objectives[i] / self.bin_size[i])
            key_list.append(key_val)
        return str(key_list)

    def add_sol(self, sol):
        #What if they exactly the same
        key = get_bin_key(sol)
        if key in self.cube_dict:
            self.cube_dict[key].append(sol)
        else:
            self.cube_dict[key] = [sol]

        


if __name__ == "__main__":
    mini = np.array([0,0,0,0,0,0,0,0])
    maxi = np.array([1,1,1,1,1,1,1,1])
    
    sol1 = Solution([], [.5, 3.4])
    # sol2 = Solution([], [.6, 3.1])
    
    hype = Hypercubes(mini, maxi, ZDT1, 5)
    print(hype.get_bin_key(sol1))
    

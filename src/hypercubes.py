from zdt_test import ZDT1
from solution import Solution
import numpy as np

class Hypercubes:
    def __init__(self, d_min, d_max, objective, cube_count):

        self.cube_dict = {}
        self.sol_count = 0
        self.max_sol_count = 100

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
        returns a string of which bin each of its values fall into
        Used as key for dictionary
        """
        key_list = []
        for i in range(len(sol.objectives)):
            key_val = int(sol.objectives[i] / self.bin_size[i])
            key_list.append(key_val)
        return str(key_list)

    def push_sol(self, new_solution, optimizaton_type):
        """
        If new solution check == True
        add new solution to a cube
        """

        if self.new_sol_check(new_solution, optimizaton_type):
            key = self.get_bin_key(new_solution)
            if key in self.cube_dict:
                self.cube_dict[key].append(new_solution)
            else:
                self.cube_dict[key] = [new_solution]
        
        return

    def new_sol_check(self, new_solution, optimizaton_type):
        """
        Checks new sol against all items
        return False if new solution bad
        return true if new solution is non-dom
        """
        for cube in self.cube_dict:
            for sol in self.cube_dict[cube]:
                dom_status = new_solution.dominated(sol, optimizaton_type)

                if dom_status == -1:
                    return False
                elif dom_status == 1:
                    self.remove_sol(sol)
                elif dom_status == 0:
                    pass
        return True

    def remove_sol(self, sol):
        key = self.get_bin_key(sol)
        self.cube_dict[key].remove(sol)

    def full_remove(self):
        pass

    def output(self):
        return self.cube_dict


        


if __name__ == "__main__":
    mini = np.array([0,0,0,0,0,0,0,0])
    maxi = np.array([1,1,1,1,1,1,1,1])
    
    sol1 = Solution([], [0.2, 3.4])
    sol2 = Solution([], [0.8, 3.1])
    sol3 = Solution([], [0.3, 3.3])
    
    cube = Hypercubes(mini, maxi, ZDT1, 5)

    cube.push_sol(sol1, ["MIN", "MIN"])
    cube.push_sol(sol2, ["MIN", "MIN"])
    cube.push_sol(sol3, ["MIN", "MIN"])

    print(cube.output())
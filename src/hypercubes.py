import zdt_test
from solution import Solution
import numpy as np
import matplotlib.pyplot as plt
import random

"""
Problems/todo:
In random selection sometimes nothing is deleated as random value is
larger than any of the probablilities
"""


class Hypercubes:
    def __init__(self, d_min, d_max, objective, cube_count):
        """
        Init dict to hold solutions, keys will be sub-cubes
        Counter to keep track of # solutions
        Bin size to calculate which sub-cube solution goes into
        """
        self.cube_dict = {}
        self.sol_count = 0
        self.max_sol_count = 15

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
            if self.sol_count >= self.max_sol_count:
                print(self.sol_count, "is greater than 15")
                # If full remove 1
                self.full_remove(1)

            key = self.get_bin_key(new_solution)
            if key in self.cube_dict:
                self.cube_dict[key].append(new_solution)
            else:
                self.cube_dict[key] = [new_solution]
        
        return


    def new_sol_check(self, new_solution, optimizaton_type):
        """
        Checks new sol against all items
        return False if new solution dominated
        If new sol dominates sol in hypercube:
            store in to_del then deleate once done in that cube
        return true if new solution is non-dom
        """
        
        for cube in self.cube_dict:
            to_del = []
            for i, sol in enumerate(self.cube_dict[cube]):
                dom_status = new_solution.dominated(sol, optimizaton_type)

                if dom_status == -1:
                    return False
                elif dom_status == 1:
                    to_del.append(i)
                elif dom_status == 0:
                    pass

            for i in sorted(to_del, reverse=True):
                del self.cube_dict[cube][i]
                self.sol_count -= 1
        self.sol_count += 1
        return True

    def remove_empty_cubes(self):
        empty_cubes = []
        for cube in self.cube_dict:
            size = len(self.cube_dict[cube])
            if (size == 0):
                empty_cubes.append(cube)
        for i in empty_cubes:
            del self.cube_dict[i]
        return

    def full_remove(self, num):
        """
        Could add int to input to deleate multiple
        """
        self.remove_empty_cubes()
        
        cube_fitness = {}
        keys = self.cube_dict.keys()
        for cube in keys:
            cube_len = len(self.cube_dict[cube])
            cube_fitness[cube] = cube_len
        
        relative_fitness = [f/self.sol_count for f in cube_fitness.values()]
        #relative fitness adds to 1

        for n in range(num):
            r = random.random()
            for (i, key) in enumerate(keys):
                if r <= relative_fitness[i]:
                    chosen = random.randrange(len(self.cube_dict[key]))
                    print("Shits Full, Deleating:", self.cube_dict[key][chosen])
                    del self.cube_dict[key][chosen]
                    self.sol_count -= 1
                    break


        return


    def output(self):
        return self.cube_dict


    def output_front(self):
        """
        Return list of non dominated solutions
        """
        front = []
        for cube in self.cube_dict:
            for sol in self.cube_dict[cube]:
                front.append(sol.objectives)
        return front

    def draw_front(self):
        front = self.output_front()
        x, y = [], []
        for i in front:
            x.append(i[0])
            y.append(i[1])
        
        plt.scatter(x, y)
        plt.savefig('front.png')


        


if __name__ == "__main__":
    mini = np.zeros(30)
    maxi = np.ones(30)

    solutions = []
    for i in range(1000):
        x = zdt_test.genZDTInputs(30)
        sol = zdt_test.ZDT1(x)
        solutions.append(Solution(x, sol))
        

    cube = Hypercubes(mini, maxi, zdt_test.ZDT1, 5)

    for i in solutions:
        cube.push_sol(i, ["MIN", "MIN"])

    print(cube.output_front())
    #cube.draw_front()

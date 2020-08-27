import zdt_test
from solution import Solution
import numpy as np
import matplotlib.pyplot as plt
import random

"""
Problems/todo:
In random selection sometimes nothing is deleated as random value is
larger than any of the probablilities

Remove cube when empty
figure out why solution count wrong
"""


class Hypercubes:
    def __init__(self, d_min, d_max, objective, cube_count, max_solutions):
        """
        Init dict to hold solutions, keys will be sub-cubes
        Counter to keep track of # solutions
        Bin size to calculate which sub-cube solution goes into
        """
        self.cube_dict = {}
        self.sol_count = 0
        self.max_sol_count = max_solutions

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
                self.delete_sol()

            key = self.get_bin_key(new_solution)
            if key in self.cube_dict:
                self.cube_dict[key].append(new_solution)
            else:
                self.cube_dict[key] = [new_solution]
            self.sol_count += 1
        
        return


    def new_sol_check(self, new_solution, optimizaton_type):
        """
        Checks new sol against all items
        return False if new solution dominated
        If new sol dominates sol in hypercube:
            store in to_del then deleate once done in that cube
        return true if new solution is non-dom
        """
        
        empty_cubes = []
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

            if len(self.cube_dict[cube]) == 0:
                empty_cubes.append(cube)
                #Check if cube empty

        for cube in empty_cubes:
            del self.cube_dict[cube]

        return True

    def select_gbest(self):
        cube = self.select_min_cube()

        chosen = random.randrange(len(self.cube_dict[cube]))
        return self.cube_dict[cube][chosen]



    def select_min_cube(self):
        cube_fitness = {}
        keys = self.cube_dict.keys()
        for cube in keys:
            cube_len = len(self.cube_dict[cube])
            cube_fitness[cube] = cube_len
        
        relative_fitness = [(self.sol_count/f) for f in cube_fitness.values()]
        total_fit = sum(relative_fitness)
        relative_fitness = [(f/total_fit) for f in relative_fitness]
        #relative fitness adds to 1
        
        r = random.random()
        counter = 0
        for (i, key) in enumerate(keys):
            counter += relative_fitness[i]
            if r <= counter:
                return key
        return keys[-1]


    def select_cube(self):
        cube_fitness = {}
        keys = self.cube_dict.keys()
        for cube in keys:
            cube_len = len(self.cube_dict[cube])
            cube_fitness[cube] = cube_len
        
        relative_fitness = [f/self.sol_count for f in cube_fitness.values()]
        #relative fitness adds to 1

        r = random.random()
        counter = 0
        for (i, key) in enumerate(keys):
            counter += relative_fitness[i]
            if r <= counter:
                return key
        return keys[-1]
            

    def delete_sol(self):
        cube = self.select_cube()
        
        chosen = random.randrange(len(self.cube_dict[cube]))
        del self.cube_dict[cube][chosen]
        
        if len(self.cube_dict[cube]) == 0:
            del self.cube_dict[cube]

        self.sol_count -= 1


    def output(self):
        count = 0
        for i in self.cube_dict.keys():
            print("Cube:", i, "Has count: ", len(self.cube_dict[i]))
            count += len(self.cube_dict[i])
        print("Summed len: ", count)
        return


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
        

    cube = Hypercubes(mini, maxi, zdt_test.ZDT1, 5, 15)

    for i in solutions:
        cube.push_sol(i, ["MIN", "MIN"])

    # print(cube.select_min_cube())
    # print(cube.output_front())
    #cube.draw_front()
    cube.output()
    print(cube.sol_count)

    

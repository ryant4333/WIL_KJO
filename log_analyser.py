import math
import json
import os
import numpy as np

class Analyser:
    """
    Compares found pareto fronts between different runs of the optimiser.
    Looks in analyse folder for .json result files, outputs a text file comparing
    the fronts.
    Basic comparisons include min, mean, max in each dimension.
    Total distance to common minimum.
    Best solution found.
    """
    def __init__(self):
        self.output_file = open('./analyse/results.txt', 'w')
        """Handler for output file"""

        self.minimums = []
        """Location to store minimum in each dimension"""

    def get_f_names(self):
        """Looks in analyse folder and returns all file names
        Can be edited later to look at entered folder name.
        """
        arr = os.listdir('./analyse')
        return arr

    def get_raw_solutions(self, file_name):
        """Returns the raw solutions json data
        """
        with open('./analyse/' + file_name) as json_file:
            data = json.load(json_file)
            return data['solutions']
        
        return 0

    def summarize(self, data):
        """Returns a 3 number summary of each objective
        To save time writing this straigh to file rather than double handling in run
        """
        lst = self.get_sorted_lists(data)
        
        self.output_file.write("Objective x: min,   mean,   max\n")
        for index, obj in enumerate(lst):
            # obj.sort()
            obj_mean = np.sum(obj)/len(obj)
            obj_min, obj_max = min(obj), max(obj)

            o_summary = "Objective {}: {:0.2f},  {:0.2f},  {:0.2f}\n".format(index, obj_min, obj_mean, obj_max)
            self.output_file.write(o_summary)

    def get_sorted_lists(self, data):
        """Returns sorted list of values for each objective
        Each time this is run checks for new global minimums
        """
        obj_len = len(data[0]['objectives'])
        lst = [[] for j in range(obj_len)]

        for solution in data:
            for i in range(obj_len):
                lst[i].append(solution['objectives'][i])
        for i in range(len(lst)):
            lst[i].sort()
        
        """
        Populate global minimum list
        """
        if not self.minimums:
            for i in lst:
                self.minimums.append([i[0]])
        elif (obj_len != len(self.minimums)):
            print("Length of objective not == length of minimums")
        else:
            for index, i in enumerate(lst):
                if self.minimums[index][0] > i[0]:
                    self.minimums[index][0] = i[0]


        return lst

    def get_avg_dist(self, data):
        """Must be run after global minimums are filled
        Input is one logs data
        Output is the avgerage distance to each solution
        And the closest particle to the origin"""
        no_solutions = len(data)
        total_dist = 0
        best_sol_dist = float('Inf')
        best_sol = None

        for sol in data:
            dist = self.calc_dist(sol)
            total_dist += dist     
            if dist < best_sol_dist:
                best_sol = sol
            
        avg_dist = total_dist/no_solutions
        return (avg_dist, best_sol)


    def calc_dist(self, solution):
        """
        Takes a solution and returns its distance to the global minimum
        """
        obj = solution['objectives']
        counter = 0

        for index, i in enumerate(obj):
            counter += (i - self.minimums[index][0])**2
        dist = math.sqrt(counter)
        return dist



    def run(self):
        """Driver code, does most of writing to file"""
        f_names = self.get_f_names()
        global_best = None
        global_best_dist = float('Inf')

        for file in f_names:
            if (file[-4:] != 'json'):
                pass
            else:
                self.output_file.write("\nFile name: {}\n".format(file))
                data = self.get_raw_solutions(file)
                self.output_file.write("# of Solutions: {}\n".format(len(data)))
                self.summarize(data)
                avg_dist, best_sol = self.get_avg_dist(data)
                avg_dist_output = "Average dist: {:0.2f}\n".format(avg_dist)
                self.output_file.write(avg_dist_output)

                if self.calc_dist(best_sol) < global_best_dist:
                    global_best = best_sol

                best_sol['position'] = [round(num, 2) for num in best_sol['position']]
                best_sol['objectives'] = [round(num, 2) for num in best_sol['objectives']]
                
                best_sol_output = "Best Solution:\n{}\n".format(best_sol)
                self.output_file.write(best_sol_output)

        global_best['position'] = [round(num, 2) for num in global_best['position']]
        global_best['objectives'] = [round(num, 2) for num in global_best['objectives']]
                
        global_best_sol_output = "\nGlobal Best Solution:\n{}\n".format(global_best)
        self.output_file.write(best_sol_output)


        

        return 0


if __name__ == "__main__":
    analyser = Analyser()
    analyser.run()

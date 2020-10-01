from testModel_pygmo_short import my_problem
import random
import gc
musc = 'piri_r'
dof = 'hip_flexion_r'

class WrappingSurfaces:
    def __init__(self):
        self.p = my_problem(1, muscName = musc, dof = dof)

    def objectives(self, x):
        fitness = self.p.fitness(x)
        return fitness

    def get_bounds(self):
        return self.p.get_bounds()

if __name__ == "__main__":
    ws = WrappingSurfaces()
    bounds = ws.get_bounds()
    minimum = bounds[0]
    maximum = bounds[1]
    for i in range(10000):
        xs = []
        for i in range(len(minimum)):
            x = random.uniform(minimum[i], maximum[i])
            xs.append(x)
        print(ws.objectives(xs))
        gc.collect()
from testModel_pygmo_short import my_problem
musc = 'piri_r'
dof = 'hip_flexion_r'
p = my_problem(1, muscName = musc, dof = dof)

def WrappingSurfaces(x):
    fitness = p.fitness(x)
    return fitness

def get_bounds():
    return p.get_bounds()

print(get_bounds())
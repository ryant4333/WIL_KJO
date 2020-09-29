from testModel_pygmo_short import my_problem

def WrappingSurfaces(x):
    musc = 'piri_r'
    dof = 'hip_flexion_r'
    p = my_problem(1, muscName = musc, dof = dof)
    print(p.get_bounds())

WrappingSurfaces([])
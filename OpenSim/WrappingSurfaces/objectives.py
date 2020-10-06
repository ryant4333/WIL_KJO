from testModel_pygmo_short import my_problem
import os
musc = 'piri_r'
dof = 'hip_flexion_r'
p = my_problem(1, muscName = musc, dof = dof)

def WrappingSurfaces(x):
    null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
    # save the current file descriptors to a tuple
    save = os.dup(1), os.dup(2)
    # put /dev/null fds on 1 and 2
    os.dup2(null_fds[0], 1)
    os.dup2(null_fds[1], 2)

    fitness = p.fitness(x)

    os.dup2(save[0], 1)
    os.dup2(save[1], 2)
    # close the temporary fds
    os.close(null_fds[0])
    os.close(null_fds[1])

    return fitness

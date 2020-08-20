import particle as particle
import numpy as np
import main as main

config = main.Problem("config.json")
arr_list = []
eval_counter = 0    #TODO: Not really sure what to do with this yet.


class Swarm:

    def __init__(self, num_particles):
        self.swarm = [particle.Particle() for _ in range(num_particles)]
        set_x(self)


def set_x(self):
    for i in range(len(config.min)):
        arr_list.append(np.random.uniform(config.min[i], config.max[i], config.particle_num))
    np_arr = np.array(arr_list)

    for j in range(config.particle_num):
        np.random.shuffle(np_arr[j])
        x_pos = np_arr[:, j]
        self.swarm[j].x = x_pos


if __name__ == "__main__":

    test_swarm = Swarm(config.particle_num)
    for i in range(len(test_swarm.swarm)):
        print(test_swarm.swarm[i].x)
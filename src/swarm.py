import particle as particle
import numpy as np
import main as main

config = main.Problem("config.json")
arr_list = []
eval_counter = 0    #TODO: Not really sure what to do with this yet.


class Swarm:

    def __init__(self, num_particles, e_dist):
        self.swarm = [particle.Particle() for _ in range(num_particles)]
        self.even_dist = e_dist
        set_x(self)


def set_x(self):

    if self.even_dist:
        # Evenly distribute data within ranges
        for i in range(len(config.max)):
            dist = (config.max[i] - config.min[i]) / config.particle_num
            arr_list.append(np.arange(config.min[i], config.max[i], dist))
    else:
        # Randomly distribute within ranges
        for i in range(len(config.min)):
            arr_list.append(np.random.uniform(config.min[i], config.max[i], config.particle_num))

    # Shuffle array
    np_arr = np.array(arr_list)
    for x in range(len(config.min)):
        np.random.shuffle(np_arr[x,:])

    # Randomly assign value to dimension from appropriate array
    for j in range(config.particle_num):
        x_pos = np_arr[:, j]
        self.swarm[j].x = x_pos


if __name__ == "__main__":
    test_swarm = Swarm(config.particle_num, True)
    test = []
    for i in range(len(test_swarm.swarm)):
        test.append(test_swarm.swarm[i].x[2])
    print(np.sort(test))

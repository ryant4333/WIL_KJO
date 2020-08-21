import particle as particle
import numpy as np
import problem

config = problem.Problem("config.json")
arr_list = []
eval_counter = 0  # TODO: Not really sure what to do with this yet.


class Swarm:

    def __init__(self, num_particles, min_, max_):
        self.swarm = [particle.Particle() for _ in range(num_particles)]
        self.even_dist = e_dist
        self.set_x(self)

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
            
        self.eval_count = 0
        self.arr_list = []

        for i in range(len(min_)):
            self.arr_list.append(np.random.uniform(min_[i], max_[i], num_particles))

        self.np_arr = np.array(self.arr_list)

        for x in range(len(min_)):
            np.random.shuffle(self.np_arr[x,:])
        for j in range(num_particles):
            x_pos = self.np_arr[:, j]
            self.swarm[j].x = x_pos


if __name__ == "__main__":
    test_swarm = Swarm(13, [0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1])
    for i in range(len(test_swarm.swarm)):
        print(test_swarm.swarm[i].x)

# KJO

## Writing a config file

The optimiser uses a *config.json* file as input. 
```
{
  "objective": "zdt_test.ZDT1",
  "c1": 2.0,
  "c2": 1.0,
  "min_w": 0.4,
  "max_w": 0.7,
  "particle_num": 30,
  "max_iterations": 400,
  "min_avg_velocity": 0.01,
  "max":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  "min":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "cube_count": 20,
  "solution_count": 100,
  "optimization_type": ["MIN", "MIN"]
  "swarm_distribution": "RANDOM"
}
```
This table describes the *config.json* file attributes:

| Name              | Type             | Description  |
| ----------------- | ---------------- | ------------ |
| objective         | string           | Location of the objective function. E.g. Inside my *zdt_test.py* file I have a *ZDT1* objective function method. Thus, I give the input `zdt_test.ZDT1` |
| c1                | float            | C1 coefficent. |
| c2                | float            | C2 coefficent. |
| min_w             | float            | Minimum weight coefficent. |
| max_w             | float            | Maximum weight coefficent. |
| particle_num      | int              | Number of particles to be used. |
| max_iterations    | int              | Maximum number of iterations until the optimisation stops. |
| min_avg_velocity  | float            | Minimum average velocity a particle can achieve until the optimisation stops. |
| max               | array of floats  | Maximum input values to the objective funciton. Dimension size should be the same as the min. |
| min               | array of floats  | Minimum input values to the objective funciton. Dimension size should be the same as the max. |
| cube_count        | int              | Number of hypercubes. |
| solution_count    | int              | Total number of solutions able to be kept in the hypercube (that is, all combined hypercubes). |
| optimization_type | array of strings | Optimization type of the objective functions (either `MIN` or `MAX`). This denotes whether the objective function is seeking a minimum or maximum value. E.g. *ZDT1* has 2 objective functions: *F1* and *F2* which are both seeking minimization. Thus, I give the input `["MIN", "MIN"]`.
| swarm_distribution| string           | Type of particle distribution used (either `EVEN` or `RANDOM`). |

# KJO

## Writing a config file

The optimiser uses a *config.json* file as input. 
```
{
 "objective": "objectives.ZDT1",
 "c1": 1.1,
 "c2": 2.2,
 "min_w": 2.1,
 "max_w": 9.3,
 "particle_num": 70,
 "max_iterations": 100,
 "min_avg_velocity": 0.3,
 "cube_count": 30,
 "solution_count": 100,
 "variables": [
  {
   "name": "Radius",
   "max": 15.0,
   "min": 3.0
  },
  {
   "name": "Length",
   "max": 5.0,
   "min": 1.0
  },
  {
   "name": "Height",
   "max": "inf",
   "min": 0.1
  }
 ],
 "optimization_type": [
  "MIN",
  "MIN"
 ]
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
| variables         | array of dicts   | The variable name, maximum value, and minimum value. (max and min are floats but can also be `inf` and `-inf`.)|
| cube_count        | int              | Number of hypercubes. |
| solution_count    | int              | Total number of solutions able to be kept in the hypercube (that is, all combined hypercubes). |
| optimization_type | array of strings | Optimization type of the objective functions (either `MIN` or `MAX`). This denotes whether the objective function is seeking a minimum or maximum value. E.g. *ZDT1* has 2 objective functions: *F1* and *F2* which are both seeking minimization. Thus, I give the input `["MIN", "MIN"]`.

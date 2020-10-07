# KJO

## Running MOPSO
The program can run by starting the optimiser.py script and passing a problem folder. The following is an example of running the zdt1 benchmark.
```shell
    python optimiser.py ./benchmarks/zdt/zdt1
``` 
IMPORTANT: Need to run script from the root directory of the project.

## Problem Folder Structure
A problem folder has an objective.py file which has an objective function which each particle uses to evaluate its position. The folder also has a config.json which changes settings of the MOPSO.

## Writing a config file
The optimiser uses a *config.json* file as input. This process can be done using the Wizard.
```
{
 "objective": "objectives.ZDT1",
 "c1": 1.1,
 "c2": 2.2,
 "min_w": 0.4,
 "max_w": 0.7,
 "particle_num": 30,
 "max_iterations": 400,
 "min_avg_velocity": 0.1,
 "cube_count": 10,
 "solution_count": 1000,
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

## Using the Wizard for building config files
The Wizard is a CLI tool for building config.json files.

Steps:  
- Run the wizard.py file (`python -m wizard.py`).
- Enter input to the prompts.
- The config.json file should now be saved in the directory you have specified.

## Running log_analyser

<ol>
    <li> Copy solution log .json file from output folder into top level analyse folder. </li>
    <li> Run log_analyser.py, it will analyse all files in analyse folder. </li>
    <li> Output printed in a results text file, viewable form command line if run remotely. </li>
</ol>

## Recommendations for further development
A limitation with the current implementation is how the hypercube dynamically updates. 
It can update successful by extending the minimum and maximum points in the objective space. However,
it cannot shrink when solutions are removed. By doing this, you can remove hypercubes that are potential
unused and are not near the optimal pereto front.
<br/><br/>
Another recommendation is to add a way for a researcher to define the bounds of a problem's search space
via a function in the objectives.py script, instead of manually entering it in the config file.


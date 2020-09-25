#!/bin/bash
#PBS -M ryan.taylor5@griffithuni.edu.au
#PBS -N KJO1
#PBS -q workq
#PBS -l select=1:ncpus=10:mem=2gb,walltime=0:10:00

cd $PBS_O_WORKDIR
cd /export/home/s2896663/WIL_KJO2/
module load anaconda3/2019.07py3
source activate 3point6

python ./optimiser.py ./benchmarks/zdt/zdt3

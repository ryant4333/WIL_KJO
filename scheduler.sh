#!/bin/bash
user="ryan.taylor5@griffithuni.edu.au"
problem_folder="./benchmarks/zdt/zdt3"
griffith_number="s2896663"
#PBS -M $user
#PBS -N KJO
#PBS -q workq
#PBS -l select=1:ncpus=1:mem=2gb,walltime=0:10:00

cd $PBS_O_WORKDIR
cd /export/home/$griffith_number/WIL_KJO/
module load anaconda3/2019.07py3
source /usr/local/bin/s3proxy.sh
source activate 3point6
pip install pymop

python ./optimiser.py $problem_folder

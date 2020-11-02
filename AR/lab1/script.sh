#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 3
#SBATCH --exclusive
#SBATCH --constraint="intel"
#SBATCH --time=01:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgjano2020a

loadMPI() {
  module add plgrid/tools/openmpi
  module add plgrid/tools/python-intel/3.6.5
}

run() {
  mpirun -np 3 ./lab1.py 1000
}

loadMPI &&
run
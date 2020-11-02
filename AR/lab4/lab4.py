#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import random
import sys
import math


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = int(sys.argv[1])
m = int(sys.argv[2])
g = int(sys.argv[3])
l = int(sys.argv[4])
eps_factor = float(sys.argv[5])

eps = eps_factor * m * n

net = np.zeros((n+2, m+2))
net_prev = np.zeros((n+2, m+2))

next_iteration = True

task_range = math.ceil(m / size)

if rank == 0:
    for i in range(1, n+1):
        for j in range(1, m+1):
            net_prev[i, j] = random.uniform(0, 100)

def calulateIteration(net, net_prev):
    end = task_range * (rank+1) if rank != size-1 else m+1
    for i in range(1, n+1):
        for j in range(task_range* rank + 1, end):
            net[i, j] = (g / l + net_prev[i+1, j] + net_prev[i-1, j] + net_prev[i, j+1] + net_prev[i, j-1]) / 4

    comm.gather(net, root=0)
    if root == 0:
        print(net)

def calculateDifference(net, net_prev, next_iteration, eps):
    diff = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            diff += abs(net[i, j] - net_prev[i, j])

    print(diff)
    next_iteration = False if diff < eps else True
    return next_iteration

def changeNets(net, net_prev):
    net_prev = np.copy(net)
    net = np.zeros((n+2, m+2))
    return net, net_prev

print(net_prev)

while next_iteration:
    comm.scatter(net_prev, root=0)
    calulateIteration(net, net_prev)
    next_iteration = calculateDifference(net, net_prev, next_iteration, eps)
    net, net_prev = changeNets(net, net_prev)

print(net_prev)

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
next_iteration = True
task_range = int((n / size))
if rank == size-1:
    task_range = n - task_range*rank

net = np.zeros((task_range, m))
net_prev = np.zeros((task_range, m))

for i in range(0, task_range):
    for j in range(0, m):
        net_prev[i, j] = random.uniform(0, 100)

upper_prev = np.zeros(m)
lower_prev = np.zeros(m)

def calulateIteration(net, net_prev, lower_prev, upper_prev):
    for i in range(0, task_range):
        for j in range(0, m):
            upper_i = upper_prev[i] if i == 0  else net_prev[i-1, j]
            lower_i = lower_prev[i] if i == task_range -1 else net_prev[i+1, j]
            left_j = 0 if j == 0 else net_prev[i, j-1]
            right_j = 0 if j == m-1 else net_prev[i, j+1]
            net[i, j] = (g / l + lower_i + upper_i + right_j + left_j) / 4

def calculateDifference(net, net_prev, next_iteration, eps):
    diff = 0
    for i in range(0, task_range):
        for j in range(0, m):
            diff += abs(net[i, j] - net_prev[i, j])

    return diff

def changeNets(net, net_prev):
    net_prev = np.copy(net)
    net = np.zeros((task_range, m))
    return net, net_prev


start = MPI.Wtime()

while next_iteration:
    if rank!=0:
        comm.Send(net_prev[0], dest=rank-1)

    if rank!=size-1:
        comm.Send(net_prev[task_range-1], dest=rank+1)

    if rank!=0:
        comm.Recv(upper_prev, source=rank-1)

    if rank!=size-1:
        comm.Recv(lower_prev, source=rank+1)

    calulateIteration(net, net_prev, lower_prev, upper_prev)
    diff = calculateDifference(net, net_prev, next_iteration, eps)
    diffs = comm.gather(diff, root=0)
    if rank == 0:
        diff_sum = diff
        for i in range(size-1):
            diff_other = comm.recv(source=MPI.ANY_SOURCE)
            diff_sum += diff_other
        
        #print(diff_sum)
        if diff_sum < eps:
            next_iteration = False


        for i in range(1, size):
            comm.send(next_iteration, dest=i)

    else:
        comm.send(diff, dest=0)
        next_iteration = comm.recv(source=0)
    
    net, net_prev = changeNets(net, net_prev)

end = MPI.Wtime()

#print(rank, net_prev)
if(rank == 0):
    print('Time ', end - start)
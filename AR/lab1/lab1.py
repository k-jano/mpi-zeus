#!/usr/bin/env python
from mpi4py import MPI
import socket
import sys
import math
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

threshold = int(sys.argv[1])
threshold_B = math.floor(math.sqrt(threshold))

def erastotenes(threshold):
    primes = [True] * (threshold+1)
    sqrt_threshold = math.floor(math.sqrt(threshold))
    for i in range(2, sqrt_threshold+1):
        if primes[i] == False:
            continue

        acc = i
        while acc+i < threshold:
            acc += i
            primes[acc] = False

    primes_list = []
    for i in range(2, threshold+1):
        if primes[i] == True:
            primes_list.append(i)

    print('--B PRIMES--')
    print(primes_list)

    return primes_list

def erastotenesParallel(threshold, threshold_B, primes_B):
    taskRange = threshold-threshold_B-1
    taskSubrange = math.ceil(taskRange/size)
    start = threshold_B+1 + rank*taskSubrange

    end = start + taskSubrange if rank != size-1 else threshold

    primes = [True] * (end - start+1)
    for i in primes_B:
        acc = start
        while acc % i != 0:
            acc +=1

        primes[acc-start] = False
            
        while acc+i <= end:
            acc += i
            primes[acc-start] = False

    primes_list = []
    for i in range(end - start +1):
        if primes[i] == True:
            primes_list.append(i+start)

    if rank != 0:
        own_primes = np.array(primes_list, dtype='i')
        print('--OWN PRIMES--')
        print(own_primes)
        comm.Send(own_primes, dest=0)
    else:
        all_primes = []
        all_primes += primes_B
        all_primes += primes_list
        for i in range(0, size-1):
            other_primes = np.zeros(taskSubrange, dtype='i')
            comm.Recv(other_primes, source=MPI.ANY_SOURCE)
            print('--RECEIVED--')
            print(other_primes)
            for prime in other_primes:
                if prime!=0:
                    all_primes.append(prime)

        all_primes.sort()

        print('--ALL PRIMES--')
        print(all_primes)

        print('Number of prime numbers: ' + str(len(all_primes)))
    
    return primes_list

print('$$--Process--$$ ' + str(rank))

erastotenesParallel(threshold, threshold_B, erastotenes(threshold_B))

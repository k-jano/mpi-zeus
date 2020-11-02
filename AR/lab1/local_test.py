import sys
import math
import numpy as np

threshold = int(sys.argv[1])
threshold_B = math.floor(math.sqrt(threshold))

def erastotenes(threshold):
    primes = [True] * (threshold+1)
    sqrt_threshold = math.floor(math.sqrt(threshold))
    for i in range(2, sqrt_threshold):
        if primes[i] == False:
            continue

        multiplier = i
        while multiplier+i < threshold:
            multiplier += i
            primes[multiplier] = False

    print(primes)
    primes_list = []
    for i in range(2, threshold+1):
        if primes[i] == True:
            primes_list.append(i)

    return primes_list

prime_numbers = erastotenes(threshold_B)
print(prime_numbers)
#!/usr/bin/env python
from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor
import numpy as np
import sys

filename='cities.txt'
actual_min = 1000000

def tsp(distances, city, city_left, result, first, order):
  global actual_min
  if(result >= actual_min):
    #print("Rejected " + str(result) + " " + "".join(str(e) for e in order))
    return
  if not city_left:
    if result + distances[city][first] < actual_min:
      actual_min = result + distances[city][first]
      #print("Actualized " + str(actual_min) + " " + "".join(str(e) for e in order))
    #else:
      #print("Rejected " + str(result) + " " + "".join(str(e) for e in order))
  else:
    for i in city_left:
      city_left_cp = city_left[:]
      distance = distances[city][i]
      city_left_cp.remove(i)
      order_cp = order[:]
      order_cp.append(i)
      tsp(distances, i, city_left_cp, result + distance, first, order_cp)
  
  return actual_min

def tsp_routine(i, distances, city_left):
  city = city_left[i]
  min_path = tsp(distances, city, list(filter(lambda x: x!=city, city_left)), distances[0][city], 0, [0, city])
  return min_path.to_bytes(10, byteorder='big')

def load_data():
  with open(filename, 'r') as f:
    lines = f.readlines()
    results = []
    for line in lines:
      results.append(list(map(int, line.split('\n')[0].split(';'))))

    n = len(results[0])
    return n, results

if __name__ == "__main__":
  n, distances = load_data()
  city_left = list(range(n))
  city_left.pop(0)
  distances_arg = []
  city_left_arg = []
  for i in range(n-1):
    distances_arg.append(distances)
    city_left_arg.append(city_left)
    #tsp_routine(i, distances_arg[0], city_left_arg[0])
  #print(str(distances[0][1]) + ' ' + str(distances[1][4]) + ' ' + str(distances[4][3]) + ' ' + str(distances[3][2]) + ' ' + str(distances[2][0]))
  start = MPI.Wtime()
  with MPIPoolExecutor() as executor: 
    exec_results = executor.map(tsp_routine, range(n-1), distances_arg, city_left_arg)
    #print(results)
    res_int = []
    for line in exec_results:
      res_int.append(int.from_bytes(line, byteorder='big'))

    #print(min(res_int))
  
  end = MPI.Wtime()
  print('Time ', end - start)

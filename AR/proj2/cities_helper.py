import random
import sys

filename = 'cities.txt'
n = int(sys.argv[1])
distances = []
max_distance = 1000

def generate_coordinates():
  for _ in range(n):
    dist_line = []
    for _ in range(n):
      dist = random.randint(1, max_distance)
      dist_line.append(dist)

    distances.append(dist_line)

def save_coordinates():
  with open(filename, 'w+') as f:
    for i in range(n):
      for j in range(n):
        #f.write(str(distances[i][j]))
        f.write(str(100))
        if j != n-1:
          f.write(';')
      if i != n-1:
        f.write('\n')


if __name__ == "__main__":
  generate_coordinates()
  save_coordinates()

import math
from mpi4py import MPI
import numpy as np

STARS_COUNT = 1000

stars = {
    'mass': [10, 12, 9, 25, 3, 30, 16, 11, 12],
    'x': [10, 12, 40, -12, 1, 0, -24, 8, 100],
    'y': [0, 12, 55, -2, -12, 53, 11, 2, 11],
    'z': [45, -23, -19, -99, 24, 98, 10, 4, 2]
}

# stars = {
#     'mass': [10, 12],
#     'x': [10, 12],
#     'y': [0, 12],
#     'z': [45, -23]
# }

G = 6.67

acceleration = {
    'x': [],
    'y': [],
    'z': []
}

own_stars = {}

transitive_stars = {}

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def single_acc(i, own, last=False):
    local_acc_x = acceleration.get('x')[i]
    local_acc_y = acceleration.get('y')[i]
    local_acc_z = acceleration.get('z')[i]

    

    i_x = own_stars.get('x')[i]
    i_y = own_stars.get('y')[i]
    i_z = own_stars.get('z')[i]

    for j in range(len(transitive_stars.get('mass'))):
        if own and j == i:
            pass
        else:
            j_x = transitive_stars.get('x')[j]
            j_y = transitive_stars.get('y')[j]
            j_z = transitive_stars.get('z')[j]


            vec_len_3 = math.sqrt((i_x - j_x) ** 2 + (i_y - j_y) ** 2 + (i_z - j_z) ** 2) ** 3

            local_acc_x += (transitive_stars.get('mass')[j] / vec_len_3) * (own_stars.get('x')[i] - transitive_stars.get('x')[j])
            local_acc_y += (transitive_stars.get('mass')[j] / vec_len_3) * (own_stars.get('y')[i] - transitive_stars.get('y')[j])
            local_acc_z += (transitive_stars.get('mass')[j] / vec_len_3) * (own_stars.get('z')[i] - transitive_stars.get('z')[j])

            if not own and not last:
                local_acc_trans_x = transitive_stars.get('acceleration').get('x')[j]
                local_acc_trans_y = transitive_stars.get('acceleration').get('y')[j]
                local_acc_trans_z = transitive_stars.get('acceleration').get('z')[j]

                local_acc_trans_x += (own_stars.get('mass')[i] / vec_len_3) * (transitive_stars.get('x')[j] - own_stars.get('x')[i])
                local_acc_trans_y += (own_stars.get('mass')[i] / vec_len_3) * (transitive_stars.get('y')[j] - own_stars.get('y')[i])
                local_acc_trans_z += (own_stars.get('mass')[i] / vec_len_3) * (transitive_stars.get('z')[j] - own_stars.get('z')[i])

                transitive_stars.get('acceleration').get('x')[j] = local_acc_trans_x
                transitive_stars.get('acceleration').get('y')[j] = local_acc_trans_y
                transitive_stars.get('acceleration').get('z')[j] = local_acc_trans_z

    acceleration.get('x')[i] = local_acc_x
    acceleration.get('y')[i] = local_acc_y
    acceleration.get('z')[i] = local_acc_z

    

def calculate_acc_own():
    for i in range(len(own_stars.get('mass'))):
        single_acc(i, True)

def calculate_acc():
    global transitive_stars
    calculate_acc_own()
    for i in range(size/2):
        comm.send(transitive_stars, dest=(rank+1)%size)
        transitive_stars = comm.recv(source=(rank-1)%size)
        for j in range(len(own_stars.get('mass'))):
            single_acc(j, False, size%2 == 0 and i==size/2-1)

    if size >2:
        comm.send(transitive_stars, dest=transitive_stars.get('acceleration').get('rank'))
        transitive_stars = comm.recv(source=MPI.ANY_SOURCE)

        for i in range(len(transitive_stars.get('acceleration').get('x'))):
            acceleration['x'][i] += transitive_stars['acceleration']['x'][i]
            acceleration['y'][i] += transitive_stars['acceleration']['y'][i]
            acceleration['z'][i] += transitive_stars['acceleration']['z'][i]

    acceleration['x'] = acceleration.get('x') * G
    acceleration['y'] = acceleration.get('y') * G
    acceleration['z'] = acceleration.get('z') * G

    

def split_stars():
    global transitive_stars
    own_stars['mass'] = np.array_split(stars.get('mass'), size)[rank]
    own_stars['x'] = np.array_split(stars.get('x'), size)[rank]
    own_stars['y'] = np.array_split(stars.get('y'), size)[rank]
    own_stars['z'] = np.array_split(stars.get('z'), size)[rank]

    transitive_stars = own_stars.copy()

    acc_len = len(own_stars['mass'])
    acceleration['x'] = np.zeros(acc_len)
    acceleration['y'] = np.zeros(acc_len)
    acceleration['z'] = np.zeros(acc_len)

    transitive_stars['acceleration'] = {}
    transitive_stars['acceleration']['x'] = np.zeros(acc_len)
    transitive_stars['acceleration']['y'] = np.zeros(acc_len)
    transitive_stars['acceleration']['z'] = np.zeros(acc_len)
    transitive_stars['acceleration']['rank'] = rank

if __name__ == '__main__':
    stars = comm.bcast(stars, root=0)
    split_stars()
    calculate_acc()
    print('Rank ' + str(rank) + ' acc'), acceleration

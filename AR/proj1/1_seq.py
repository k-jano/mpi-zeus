import math

mass = [10, 12, 9, 25, 3, 30, 16, 11, 12]
position = {
    'x': [10, 12, 40, -12, 1, 0, -24, 8, 100],
    'y': [0, 12, 55, -2, -12, 53, 11, 2, 11],
    'z': [45, -23, -19, -99, 24, 98, 10, 4, 2]
}

G = 6.67

acceleration = {
    'x': [],
    'y': [],
    'z': []
}

def single_acc(i):
    local_acc_x = 0
    local_acc_y = 0
    local_acc_z = 0

    i_x = position.get('x')[i]
    i_y = position.get('y')[i]
    i_z = position.get('z')[i]

    for j in range(len(mass)):
        if j == i:
            pass
        else:
            j_x = position.get('x')[j]
            j_y = position.get('y')[j]
            j_z = position.get('z')[j]

            vec_len_3 = math.sqrt((i_x - j_x) ** 2 + (i_y - j_y) ** 2 + (i_z - j_z) ** 2) ** 3

            local_acc_x += (mass[j] / vec_len_3) * (position.get('x')[i] - position.get('x')[j])
            local_acc_y += (mass[j] / vec_len_3) * (position.get('y')[i] - position.get('y')[j])
            local_acc_z += (mass[j] / vec_len_3) * (position.get('z')[i] - position.get('z')[j])

    acceleration.get('x').append(G * local_acc_x)
    acceleration.get('y').append(G * local_acc_y)
    acceleration.get('z').append(G * local_acc_z)

def calculate_acc():
    for i in range(len(mass)):
        single_acc(i)


if __name__ == '__main__':
    calculate_acc()
    print(acceleration)
cell = (3, 6)
row = cell[0]
column = cell[1]

for i in range(-1, 2):
    for j in range(-1, 2):
        g = row + i
        a = column + j

        cell = (g, a)
        print(cell)

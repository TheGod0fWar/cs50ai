EMPTY = None
X = "X"
O = "O"
board = [[EMPTY, X, EMPTY], [O, X, EMPTY], [EMPTY, EMPTY, EMPTY]]

# for row in board:
#     for column in row:
#         print(column)


res = set()
for row_counter, row in enumerate(board):
    for column_counter, column in enumerate(row):
        if column == EMPTY:
            res.add((row_counter, column_counter))
print(res)

action = (2, 1)

if action in res:
    print(action)

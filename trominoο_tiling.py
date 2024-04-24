import argparse
parser = argparse.ArgumentParser()
parser.add_argument("n", help="The parameter n indicates the dim of the square we want to cover", type=int)
args = parser.parse_args()

n = args.n
dim = 2**n

board = [['X' for i in range(dim)] for j in range(dim)]

def board_printer(board):
    for row in board:
        for item in row:
            print(item, end=" ")
        print()

def place(board, color, x, y, type):
    #if there is a 2by2 square the type of the tromino is determined by the quarter in which the corner of the tromino is
    #eg the L shaped tromino is of type 3
    board[x][y] = color
    if (type==1):
        board[x+1][y] = color
        board[x][y-1] = color
    elif (type==2):
        board[x+1][y] = color
        board[x][y+1] = color
    elif(type==3):
        board[x-1][y] = color
        board[x][y+1] = color
    elif(type==4):
        board[x-1][y] = color
        board[x][y-1] = color

def search4exc(board):
    max_i = len(board)-1
    cords = [-1, -1]
    for i in [0, max_i]:
        for j in [0, max_i]:
            if (board[i][j]!='X'):
                cords[0], cords[1] = [i, j]   
    return cords

def paste_part(board, topl, board_part):
    #extracting coordinates of the top-left corner for both destination and part boards
    dest_top_left_row, dest_top_left_col = topl
    
    #calculating dimensions
    part_rows = len(board_part)
    part_cols = len(board_part[0])
    
    #pasting the board part onto the board
    for i in range(part_rows):
        for j in range(part_cols):
            dest_row = dest_top_left_row + i
            dest_col = dest_top_left_col + j
            board[dest_row][dest_col] = board_part[i][j]

def divide(board):
    n = len(board)
    half_n = n // 2
    
    q1 = [row[half_n:] for row in board[:half_n]]
    q2 = [row[:half_n] for row in board[:half_n]]
    q3 = [row[:half_n] for row in board[half_n:]]
    q4 = [row[half_n:] for row in board[half_n:]]
    
    return q1, q2, q3, q4

def tiling(board):
    n = len(board)/2
    if (n==1):
        place(board, 'G', 1, 0, 3)
    elif (n==2):
        corner = search4exc(board)
        if (corner == [-1, -1] or (corner[0]==corner[1] and corner[0]==(len(board)-1))): # if there is no different color square place as intented or if there is a square at the bottom right corner
            place(board, 'G', 1, 1, 2)
            place(board, 'B', 0, 0, 2)
            place(board, 'B', 2, 2, 2)
            place(board, 'R', 0, 3, 1)
            place(board, 'R', 3, 0, 3)
        elif (corner[0]==corner[1]): #if there is a square in the main diagonal its the bottom right
            size = len(board)

            dupl = [['G' for i in range(size)] for j in range(size)]
            place(dupl, 'G', 1, 1, 2)
            place(dupl, 'B', 0, 0, 2)
            place(dupl, 'B', 2, 2, 2)
            place(dupl, 'R', 0, 3, 1)
            place(dupl, 'R', 3, 0, 3)

            #matrix transpotion relative to the second diagonal
            flipped_sec = [[0] * size for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    flipped_sec[i][j] = dupl[size - 1 - j][size - 1 - i]

            #placing the transposed 2d list
            paste_part(board, [0, 0], flipped_sec)
        elif (corner[0]>corner[1]): #if there is a square in the top right corner
            place(board, 'G', 1, 2, 1)
            place(board, 'R', 0, 3, 1)
            place(board, 'R', 2, 1, 1)
            place(board, 'B', 0, 0, 2)
            place(board, 'B', 3, 3, 4)
        elif (corner[0]<corner[1]):
            size = len(board)

            dupl = [['G' for i in range(size)] for j in range(size)]
            place(dupl, 'G', 1, 2, 1)
            place(dupl, 'R', 0, 3, 1)
            place(dupl, 'R', 2, 1, 1)
            place(dupl, 'B', 0, 0, 2)
            place(dupl, 'B', 3, 3, 4)

            #matrix transpotion relative to the second diagonal
            flipped_sec = [[0] * size for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    flipped_sec[i][j] = dupl[j][i]

            #placing the transposed 2d list
            paste_part(board, [0, 0], flipped_sec)
    else:
        
        corner = search4exc(board)
        btr = len(board)//2 #the bottom right corner coordinates of the center square - center bottom right
        if (corner == [-1, -1]): # if there is no different color square place as intented
            place(board, 'G', btr, btr, 4)
        elif (corner[0]>corner[1]): #if there is a square in the top right corner
            place(board, 'G', btr-1, btr, 1)
        elif (corner[0]==corner[1] and corner[0]==(len(board)-1)): #if there is a square at the bottom right corner
            place(board, 'G', btr-1, btr-1, 2)
        elif (corner[0]<corner[1]): #if the square is at the bottom left corner
            place(board, 'G', btr, btr-1, 3)
        elif (corner[0]==corner[1]): #if there is a square in top left corner
            place(board, 'G', btr, btr, 4)

        q = divide(board)
        qf = tiling(q[1]) #quarter filled
        paste_part(board, [0, 0], qf) #placing the filled quarter
        ############################################################
        half_n = len(board)//2
        qf = tiling(q[0])
        paste_part(board, [0, half_n], qf)
        qf = tiling(q[2])
        paste_part(board, [half_n, 0], qf)
        qf = tiling(q[3])
        paste_part(board, [btr, btr], qf)

    return board
    
solution = tiling(board)
print()
board_printer(solution)

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
    cords = [-1, -1]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j]!='X'):
                cords[0], cords[1] = [i, j]   
    return cords

def copy_part(board, topl, botr):
    #extracting coordinates of the top-left and bottom-right corners
    top_left_row, top_left_col = topl
    bottom_right_row, bottom_right_col = botr
    
    #copying the portion of the board we want to copy
    part = []
    for i in range(top_left_row, bottom_right_row + 1):
        part_row = board[i][top_left_col:bottom_right_col + 1]
        part.append(part_row)
    
    return part

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
    
    q1 = [row[:half_n] for row in board[:half_n]]
    q2 = [row[half_n:] for row in board[:half_n]]
    q3 = [row[:half_n] for row in board[half_n:]]
    q4 = [row[half_n:] for row in board[half_n:]]
    
    return q1, q2, q3, q4

def tiling(board):
    n = len(board)/2
    if (n==1):
        res = search4exc(board)
        if (res[0] == -1):
            place(board, 'G', 1, 0, 3)
    elif (n==2):
        place(board, 'G', 1, 1, 2)
        place(board, 'B', 0, 0, 2)
        place(board, 'B', 2, 2, 2)
        place(board, 'R', 0, 3, 1)
        place(board, 'R', 3, 0, 3)
    else:
        q = divide(board)
        qf = tiling(q[1]) #quarter filled
        paste_part(board, [0, 0], qf) #placing the filled quarter
        btr = len(board)//2 #the bottom right corner coordinates of the center square - center bottom right
        place(board, 'G', btr, btr, 4)
    return board

    

solution = tiling(board)
board_printer(solution)

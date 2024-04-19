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

if (n==1):
    place(board, 'G', 1, 0, 3)
    board_printer(board)

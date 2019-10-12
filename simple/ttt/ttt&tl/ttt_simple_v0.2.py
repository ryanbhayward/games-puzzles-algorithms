# BedirT 2019
# Tic-Tac-Toe & Terni-Lapilli
# CMPUT 355 
# UofA

#   TIC-TAC-TOE
#
#       C1 C2 C3
#       |  |  |
#       0  1  2 - R1
#       3  4  5 - R2
#       6  7  8 - R3
#      /        \
#    D1          D2
# The board example for Tic-Tac-Toe
#
# Game Rules:
#  
#   - Players play in alternating order
#   - The goal is to place 3 stones in order that they will align 
#   in one of the rows (R1, R2, R3) or columns (C1, C2, C3) or diagonals (R1, R2)
#   - The game ends (draw) when there is no possible winning state

#   TERNI-LAPILLI
#
#       C1 C2 C3
#       |  |  |
#       0--1--2 - R1
#       |\ | /|
#       | \|/ |
#       3--4--5 - R2
#       | /|\ |
#       |/ | \|
#       6--7--8 - R3
#      /        \
#    D1          D2
# The board example for Terni Lapilli
#
# Game Rules:
#  
#   - Players play in alternating order
#   - The goal is to place 3 stones in order that they will align 
#   in one of the rows (R1, R2, R3) or columns (C1, C2, C3) or diagonals (R1, R2)
#   - Each player only has 3 stones
#   - Once all stones are places, each stone can move in column, row, or diagnoally.
#   - There is no repetition in states: Meaning that if a state has occured already,
#   then a player cannot repeat the state. The immediate move that leads to a repetition
#   is illegal
#   - The game ends (draw) when there is no possible winning state

# Done: 
#     - Environment is ready
#     - 1v1 mode
#     - Added terni-lapili
#
# To-Do:
#     - Implement solver
#         - Alpha-beta pruning (best case O(b^(d/2)))
#         - Minimax wo AlphaBeta
#     - Explanation for the solvers (algorithms)
#     - Update the UI accordingly -new solver-
#     - Add a terni-lapilli solver -more research on that-

def initBoard():
    # Creating the initial board position with 9 cells.
    # Empty points are represented with a '.'

    board = ['.'] * 9
    return board

def printBoard(board):
    # Parameters:
    #     board:  the current game board state
    #
    # Printing the board in a 3x3 form

    for i in range(len(board)):
        if i % 3 == 0:
            print("\n\t", end="")
        print(board[i] + " ", end="")
    print("\n")

def addStone(board, cell, color):
    # Parameters:
    #     board:  the current game board state
    #     cell:   to which cell are we putting the stone to
    #     color:  the color of the stone being placed (b/w)
    #
    # We will place the stone to corresponding cell
    # We first will need to check if the action chosen is valid
    # If valid we will return True otherwise False

    if board[cell] == '.': # Meaning the move is valid
        board[cell] = color
    else:
        # Invalid move
        return False
    return True

def checkGameState(board, cell):
    # Parameters:
    #     board:  the current game board state
    #     cell:   to which cell are we putting the stone to
    #
    # There are three things to check when a
    # new stone has been placed. 
    #     1- Row that the stone has been placed
    #     2- Column that the stone has been placed
    #     3- The diagonals if needed
    # That's the exact way we are going to follow

    # Checking the game state, returning true if the game is over
    return checkRow(board,cell) or \
        checkColumn(board,cell) or \
        checkDiag(board,cell)

def checkRow(board, cell):
    # Parameters:
    #     board:  the current game board state
    #     cell:   to which cell are we putting the stone to
    #
    # ROW
    #   - If we are on the left/right side we need to check two cells
    #         ahead or back.
    #   - If we are on the mid we need to check both sides

    if cell % 3 == 0:        # Meaning we are on the left-most cell
        return board[cell] == board[cell+1] == board[cell+2]
    elif cell % 3 == 1:      # Meaning we are on the middle
        return board[cell] == board[cell+1] == board[cell-1]
    else:                    # We are on the right-most cell
        return board[cell] == board[cell-1] == board[cell-2]

def checkColumn(board, cell):
    # Parameters:
    #     board:  the current game board state
    #     cell:   to which cell are we putting the stone to
    #
    # COLUMN
    #   - If we are on the top row, we need to check +3 & +6
    #   - If we are on the middle row, we need to check -3 & +3
    #   - If we are on the bottom row, we need to check -3 & -6
    # 
    #  One trick is to use %9 for the calculations so we don't 
    # have to create if-else for each condition, instead we can
    # (n + 3) % 9 and (n - 3) % 9 -n being the cell number-

    return board[cell] == board[(cell + 3) % 9] == \
        board[(cell - 3) % 9]

def checkDiag(board, cell):
    # Parameters:
    #     board:  the current game board state
    #     cell:   to which cell are we putting the stone to
    #
    # DIAGONALS
    #   We only have two diagonal cases 0-4-8 and 2-4-6
    # We will check for the diagonals the cell belongs
    # Since we have 4 on each diag, we need to check both
    # before returning anything
    
    solved = False # If the board is solved given state
    
    if cell in [0, 4, 8]:
        solved = board[0] == board[4] == board[8]
    if cell in [2, 4, 6] and not solved: 
        # I only want to check this if I didn't 
        # already solved therefore added -not solved-
        return board[2] == board[4] == board[6]
    return solved

def moveStones(board, cells):
    print("MOVING")
    print(board[cells[0]], "to", board[cells[1]])
    board[cells[1]] = board[cells[0]]
    board[cells[0]] = '.'

def addToHistory(board, theHistory):
    theHistory.add(tuple(board))

def checkHistory(board, cells, theHistory):
    checkBoard = board.copy()
    checkBoard[cells[1]] = checkBoard[cells[0]]
    checkBoard[cells[0]] = '.'

    if tuple(checkBoard) in theHistory:
    	return True
    addToHistory(checkBoard, theHistory)
    return False

def playTTT():
    # This is the runner function, we will call needed functions
    # to start the game and play. 
    #
    # What we need is a sequential game with steps:
    #    - Initialize the board
    #    - Repeat until game is over
    #        - Let first player play
    #        - Let second player play
    #    - Let the same player play if the given input is invalid
    #    - Let players know the result of the game

    gameBoard = initBoard() # initializing the board

    # . . .
    # . . .
    # . . .
    #
    # Current board state

    print("It's time to play Tic-Tac-Toe.\
    \n\n\t0 1 2\
    \n\t3 4 5\
    \n\t6 7 8\
    \n\nThese are the board cells, please just pick\
    \nwhich cell you want to place your stone (mark)\n")

    color = 'w' # w for white and b for black
                # we are going to alternate the color as
                # a player makes a move
    
    # variable to see if the game is over yet
    done = False

    while(True):
        cell = int(input("\tNext move please: "))

        # First statement: for user to not enter a weird input
        # Adding a stone
        if cell in [i for i in range(9)] and \
            addStone(gameBoard, cell, color): 
            printBoard(gameBoard)
            done = checkGameState(gameBoard, cell) # checking the game state
        else:
            print("Invalid input, please make a valid move.")
            # we didn't alternate the color so the game goes on
            continue

        # checking if the game is over
        if done:
            again = input("Congragulations, the game is over!\n" + color +
                " is the winner. Do you want to play one more round ?(Y/N): ")
            if again in ['Y', 'y']:
                return True
            return False

        # alternating colors
        color = ('b' if color == 'w' else 'w')

def playTL():
    # This is the runner function for Terni Lapilli
    # we will call needed functions
    # to start the game and play. 
    #
    # What we need is a sequential game with steps:
    #    - Initialize the board
    #    - Repeat until game is over
    #        - If 3 stones are placed, let them move the stones
    #        - Let first player play
    #        - Let second player play
    #    - Let the same player play if the given input is invalid
    #    - Let players know the result of the game

    gameBoard = initBoard() # initializing the board
    theHistory = set() # creating an empty set to keep history of states

    # . . .
    # . . .
    # . . .
    #
    # Current board state

    color = 'w' # w for white and b for black
                # we are going to alternate the color as
                # a player makes a move
    
    # variable to see if the game is over yet
    done = False

    count = 0
    while count < 6:
        print("\tTurn for " + color)
        cell = int(input("\tNext move please: "))

        # First check is for user to not enter a weird input
        # Adding a stone
        if cell in [i for i in range(9)] and \
            addStone(gameBoard, cell, color): 
            printBoard(gameBoard)
            done = checkGameState(gameBoard, cell) # checking the game state
        else:
            print("Invalid input, please make a valid move.")
            # we didn't alternate the color so the game goes on
            
            continue
        # checking if the game is over
        if done:
            again = input("Congragulations, the game is over!\n" + color +
                " is the winner. Do you want to play one more round ?(Y/N): ")
            if again in ['Y', 'y']:
                return True
            return False
        # alternating colors
        color = ('b' if color == 'w' else 'w')
        count += 1

    addToHistory(gameBoard, theHistory) #adding the current board state to history
    while True:
        print("\tTurn for " + color)
        cells = list(map(int, input("\tNext move please (All stones are placed so you need to move them)\n\
        Please enter the cell of the stone you want to move, and the cell you \n\
        want to move it to with a space in between (i.e. 2 1): ").split(' ')))

        # Checking if the stone player want to move is his/her own
        # and if the cell we want to move is empty
        if gameBoard[cells[0]] == color and \
            gameBoard[cells[1]] == '.':

            # calling check history
            if checkHistory(gameBoard, cells, theHistory):
                print("This state has already happened, please try another move.")
                continue
            else:
                moveStones(gameBoard, cells)
                printBoard(gameBoard)
                done = checkGameState(gameBoard, cells[1])
        else:
            print("Invalid input, please make a valid move.")
            # we didn't alternate the color so the game goes on
            continue

        if done:
            again = input("Congragulations, the game is over!\n" + color +
                " is the winner. Do you want to play one more round ?(Y/N): ")
            if again in ['Y', 'y']:
                return True
            return False
        # alternating colors
        color = ('b' if color == 'w' else 'w')



    # Playing infinetely till user says no
while(playTL()):
    pass




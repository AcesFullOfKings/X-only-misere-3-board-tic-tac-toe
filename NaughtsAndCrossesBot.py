# misere, X-only, 3-board naughts and crosses

from copy import deepcopy
import time
from random import choice

class SquareTakenException(Exception):
    def __init__(self):
         self.value = ""

class Board:
    def __init__(self):
        self.boards = [[["-" for c in range(3)] for r in range(3)] for b in range(3)] #board row column

    def show(self):
        for i in range(1,4):
            print("Board " + str(i) + " "*6, end="")
        print("\n")
        for row in range(3):
            count = 0
            for board in range(3):
                print("|", end="")
                for col in range(3):
                    print(self.boards[board][row][col], end="")
                    print("|", end="")
                print("  ||  " if count < 2 else "", end="")
                count += 1
            print("\n")

    def is_win(self, board):
        b = self.boards[board]
        return (("-" != b[0][0] == b[0][1] == b[0][2]) or # top row win
                ("-" != b[1][0] == b[1][1] == b[1][2]) or # middle row win
                ("-" != b[2][0] == b[2][1] == b[2][2]) or # bottom row win
                ("-" != b[0][0] == b[1][0] == b[2][0]) or # left colum win
                ("-" != b[0][1] == b[1][1] == b[2][1]) or # middle column win
                ("-" != b[0][2] == b[1][2] == b[2][2]) or # right column win
                ("-" != b[0][0] == b[1][1] == b[2][2]) or # TL-BR diagonal win
                ("-" != b[2][0] == b[1][1] == b[0][2]))   # TR-BL diagonal win

    def is_game_over(self):
        return self.is_win(0) and self.is_win(1) and self.is_win(2)

    def kill_board(self, board):
        b = self.boards[board]
        for r in range(3):
            for c in range(3):
                b[r][c] = "O"
        self.boards[board] = b        

    def move(self, piece, board, row, column):
        if row > 2 or column > 2 or board > 2 or row < 0 or column < 0 or board < 0:
            raise IndexError
        if self.boards[board][row][column] != "-":
            raise SquareTakenException
        else:
            self.boards[board][row][column] = piece

class Player:
    def __init__(self):
        self.name = ""

class Human(Player):
    def __init__(self):
        self.name = input("Please enter player's name:")
    
    def make_move(self, board):
        print(self.name + " - make a move:")
        while True:
            try:
                b = int(input("Board: ")) - 1
                r = int(input("Row: ")) - 1
                c = int(input("Column: ")) - 1
                board.move("X", b, r, c)
                move = (b,r,c)
                return move
            except IndexError:
                print("Value must be between 1 and 3!")
            except ValueError:
                print("Input must be an integer!")
            except SquareTakenException:
                print("That square is already taken! Try another.")

class Bot(Player):
    def __init__(self, name):
        self.name = name

    def make_move(self, board):

        def get_board_rating(b):
            if b[0][0] == "O": #if board is dead return 1
                return ""
         
            boards = {
            "000000000" : "c",
            "100000000" : "",
            "010000000" : "",
            "000010000" : "cc",
            "110000000" : "ad",
            "101000000" : "b",
            "100010000" : "b",
            "100001000" : "b",
            "100000001" : "a",
            "010100000" : "a",
            "010010000" : "b",
            "010000010" : "a",
            "110100000" : "b",
            "110010000" : "ab",
            "110001000" : "d",
            "110000100" : "a",
            "110000010" : "d",
            "110000001" : "d",
            "101010000" : "a",
            "101000100" : "ab",
            "101000010" : "a",
            "100011000" : "a",
            "100001010" : "",
            "010110000" : "ab",
            "010101000" : "b",
            "110110000" : "a",
            "110101000" : "a",
            "110100001" : "a",
            "110011000" : "b",
            "110010100" : "b",
            "110001100" : "b",
            "110001010" : "ab",
            "110001001" : "ab",
            "110000110" : "b",
            "110000101" : "b",
            "110000011" : "a",
            "101010010" : "b",
            "101000101" : "a",
            "100011010" : "b",
            "010101010" : "a",
            "110101010" : "b",
            "110101001" : "b",
            "110011100" : "a",
            "110001110" : "a",
            "110001101" : "a",
            "110101011" : "a"}

            def rotate_90(board):
                new_board = [["-" for c in range(3)] for r in range(3)]
                new_board[0][0] = board[0][2]
                new_board[0][1] = board[1][2]
                new_board[0][2] = board[2][2]
                new_board[1][0] = board[0][1]
                new_board[1][1] = board[1][1]
                new_board[1][2] = board[2][1]
                new_board[2][0] = board[0][0]
                new_board[2][1] = board[1][0]
                new_board[2][2] = board[2][0]
                return new_board

            def reflect(board):
                new_board = [["-" for c in range(3)] for r in range(3)]
                new_board[0][0] = board[0][2]
                new_board[0][1] = board[0][1]
                new_board[0][2] = board[0][0]
                new_board[1][0] = board[1][2]
                new_board[1][1] = board[1][1]
                new_board[1][2] = board[1][0]
                new_board[2][0] = board[2][2]
                new_board[2][1] = board[2][1]
                new_board[2][2] = board[2][0]
                return new_board

            def is_win(bd):
                return (("-" != bd[0][0] == bd[0][1] == bd[0][2]) or # top row win
                        ("-" != bd[1][0] == bd[1][1] == bd[1][2]) or # middle row win
                        ("-" != bd[2][0] == bd[2][1] == bd[2][2]) or # bottom row win
                        ("-" != bd[0][0] == bd[1][0] == bd[2][0]) or # left colum win
                        ("-" != bd[0][1] == bd[1][1] == bd[2][1]) or # middle column win
                        ("-" != bd[0][2] == bd[1][2] == bd[2][2]) or # right column win
                        ("-" != bd[0][0] == bd[1][1] == bd[2][2]) or # TL-BR diagonal win
                        ("-" != bd[2][0] == bd[1][1] == bd[0][2]))   # TR-BL diagonal win
        
            if is_win(b):
                return ""            

            for j in range(2): # all reflections
                for i in range(4): # all roations
                    board_fingerprint = ""
                    for r in range(3): # generate fingerprint
                        for c in range(3):
                            if b[r][c] == "X":
                                board_fingerprint += "1"
                            else:
                             board_fingerprint += "0" 

                    if board_fingerprint in boards.keys():
                        return boards[board_fingerprint]
                    else:
                        b= rotate_90(b)
                b = reflect(b)
            return "?"

        def get_position_rating(boards):
            position_rating = ""
            for i in range(3):
                position_rating += get_board_rating(boards[i])
        
            temp = list(position_rating) #create list of chars
            temp.sort() #sort list 
            position_rating = "".join(temp) #merge list into string. String is now sorted alphabetically
            return position_rating

        avail_moves = []
        for b in range(3):
            for r in range(3):
                for c in range(3):
                    if board.boards[b][r][c] == "-":
                        avail_moves.append((b,r,c))

        wins = ["cc", "a", "bb", "bc"]
        good_moves = []
        
        position_rating = get_position_rating(board.boards)
        for move in avail_moves:
            board_copy = deepcopy(board)
            b,r,c = move
            board_copy.move("X", b, r, c)
            move_rating = get_position_rating(board_copy.boards)
            if move_rating in wins:
                good_moves.append(move)
        if len(good_moves) > 0:
            return choice(good_moves)
        else: 
            return choice(avail_moves)
        

player_1 = Human()
player_2 = Bot("The Second Computer")

while True:
    #new game
    turn_player = choice(player_1, player_2) # so play starts with player_1
    b = Board()
    while not game_over:
        if turn_player == player_2:
            turn_player = player_1
        else:
            turn_player = player_2
        print("It's " + turn_player.name + "'s turn!")
        b.show()
        move = turn_player.make_move(deepcopy(b))
        
        board, row, col = move
        b.move("X", board, row, col)

        if b.is_win(board):
            b.show()
            print("\nBoard " + str(board+1) + " is dead!")
            b.kill_board(board) #only passes the board number as an integer, not the actual board
            if b.is_game_over():
                b.show()
                if turn_player == player_2:
                    winner = player_1.name
                else:
                    winner = player_2.name
                print(winner + " wins!")
                game_over = True

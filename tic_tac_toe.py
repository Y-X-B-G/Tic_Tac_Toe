from typing import Optional, List

class TicTacToe:
    """Tic-Tac-Toe class this class holds a game board of size nxn
    with all associated functions for manipulating the game state
    
    The board itself is a 2D array where empty arrays are 0, X's are 1s and O is -1.

    Please note that the starting value must be X 
    """
    def __init__(self, size: int):
        self.board: List[List[int]] = [[0 for _ in range(size)] for _ in range(size)]
        self.size: int = size
        #I'm creating the round variable to easily tell who's turn it is
        self.round: int = 0

    def check_win(self) -> Optional[int]:
        """
        Check the current board to see if its a winner
        @params 
            None: This function takes no Parameters
        @returns
            int: 1 if X is the winner
                 -1 if O is the winner
                 0 if tie
                 2 if the winner is undecided
        """
        dim: int = self.size
        last: int  = dim - 1

        #variables for checking the dagonals
        downward: int = self.board[0][0]
        upward: int = self.board[last][0]
        index: int = 1

        #Check's the rows for winners
        for index, rows in enumerate(self.board):
            #If the first value isn't initialized we just skip the row    
            if rows[0] == 0: continue

            winner: int = rows[0]
            #Winner decides who can "win the row" since all values in a row must be the same
            next_value: int = 1
            while next_value < dim and rows[next_value] == winner: next_value += 1

            if next_value == dim:
                print(f"Winner in row ${index}")
                return winner

        #Checks columns for winners
        for columns in range(dim):
            #if the first value of the column is 0 skip the column
            if self.board[0][columns] == 0: continue

            victor: int = self.board[0][columns]
            successor: int = 1
            while successor < dim and self.board[successor][columns] == victor: successor += 1

            if successor == dim:
                print(f"Winner in column ${columns}")
                return victor

        #Checks diagonals for winners

        if downward != 0:
            while index < dim and downward == self.board[index][index]: index += 1

            if index == dim:
                print("Winner upper left diagonal")
                return downward

        if upward != 0:
            index = 1
            while index < dim and downward == self.board[last-index][index]: index += 1

            if index == dim:
                print("Winner upper right diagonal")
                return upward

        if self.round == dim**2:
            return 0

        return 2

    def get_board(self) -> List[List[int]]:
        """
        Gets the current board
        @params
            None:
        @returns
            self.board: List[List[int]] - The current board state
        """
        return self.board

    def set_board(self, row: int, column: int, value: int) -> None:
        """
        Sets the value of a space on the board without checking if the move is valid
     
        ***FOR TESTING ONLY***

        @params
            row: int - row index
            column: int - column index
        @returns
            none:
        """
        assert row >= 0 and row < self.size, "invalid row value"
        assert column >=0 and column < self.size, "invalid column value"
        assert value >= -1 and value <= 1, "invalid value"

        self.board[row][column] = value

    def set_round(self, value: int) -> None:
        """
        Sets the current round without checking to make sure its valid 

        ***FOR TESTING ONLY***

        @params
            value: The new round number
        @returns
            None:
        """
        self.round = value

    def play(self, row: int, column: int) -> int:
        """
        Plays the next move assuming the first person to play chose X

        @params
            row: int - index of the row 
            column: int - index of the column
        @returns
            value: int - 1 if successfully played
                       - 0 if unsuccessful 
        """
        if self.board[row][column] != 0: return 0

        value: int = (self.round + 1)%2
        value = value if value == 1 else -1
        return 1

    def __str__(self) -> str:
        output: str = ""
        for index, row in enumerate(self.board):
            for num, column in enumerate(row):
                if column == 0:
                    output += " "
                elif column == 1:
                    output += "X"
                else:
                    output += "O"
                
                if num != self.size - 1:
                    output += "|"
                else:
                    output += "\n"
            
            if index != self.size - 1:
                output += "_"*(2*self.size - 2)
                output += "\n"

        return output
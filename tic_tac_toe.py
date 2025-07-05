from typing import Optional, List, Self
import copy

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
                 None if the winner is undecided
        """
        dim: int = self.size
        last: int  = dim - 1

        #variables for checking the dagonals
        downward: int = self.board[0][0]
        upward: int = self.board[last][0]
        index_diag: int = 1

        #Check's the rows for winners
        for index, rows in enumerate(self.board):
            #If the first value isn't initialized we just skip the row
            if rows[0] == 0: continue

            winner: int = rows[0]
            #Winner decides who can "win the row" since all values in a row must be the same
            next_value: int = 1
            while next_value < dim and rows[next_value] == winner: next_value += 1

            if next_value == dim:
                print(f"Winner in row {index}")
                return winner

        #Checks columns for winners
        for columns in range(dim):
            #if the first value of the column is 0 skip the column
            if self.board[0][columns] == 0: continue

            victor: int = self.board[0][columns]
            successor: int = 1
            while successor < dim and self.board[successor][columns] == victor: successor += 1

            if successor == dim:
                print(f"Winner in column {columns}")
                return victor

        #Checks diagonals for winners

        if downward != 0:
            while index_diag < dim and downward == self.board[index_diag][index_diag]: index_diag += 1

            if index_diag == dim:
                print("Winner upper left diagonal")
                return downward

        if upward != 0:
            index_diag = 1
            while index_diag < dim and upward == self.board[last-index_diag][index_diag]: index_diag += 1

            if index_diag == dim:
                print("Winner upper right diagonal")
                return upward

        if self.round == dim**2:
            return 0

        return None

    def get_board(self) -> List[List[int]]:
        """
        Gets the current board
        @params
            None:
        @returns
            self.board: List[List[int]] - The current board state
        """
        return copy.deepcopy(self.board)

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
        self.board[row][column] = value
        self.round += 1
        return 1

    def next_states(self) -> List[Self]:
        """
        This generates an array that contains all possible future states 1 move into the future

        @params
            None:
        @returns
            If the current state is a winning state or a tie state return an empty list
            else return a list of future states

        """
        next_moves: List[Self] = []
        if self.check_win() is None:
            for row_index, row in enumerate(self.board):
                for col_index, column in enumerate(row):
                    if column == 0:
                        new_board: Self = copy.deepcopy(self)
                        new_board.play(row_index, col_index)
                        next_moves.append(new_board)

        return next_moves

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
                output += "_"*(2*self.size-1)
                output += "\n"

        output += f"Turn: {self.round}"
        return output
        
class MinimaxAI:#assuming 1 is AI and -1 is Playuer
    def __init__(self, maximizing_player: int):
        """
        Initializes the MinimaxAI.
        
        @params
            maximizing_player: The player (1 for X, -1 for O) for whom the AI is maximizing.
        """
        self.maximizing_player = maximizing_player

    def minimax(self, game_state: TicTacToe) -> int:
        """
        Implements the Minimax algorithm to find the optimal score for the current state.
        
        @params
            game_state: The current TicTacToe game state.
        @returns
            The optimal score for the current player in this state.
        """
        winner = game_state.check_win()

        if winner == self.maximizing_player:
            return 1  #AI wins
        elif winner == -self.maximizing_player:
            return -1 #Opponent wins
        elif winner == 0:
            return 0  #Tie

        if game_state.get_current_player() == self.maximizing_player:#if the player that were maximizing's turn
            max_eval = -float('inf')# set the max (alpha) to -inf
            for next_state in game_state.next_states():#go through all the next possible game states
                eval = self.minimax(next_state)#keep going until all base case is found (by base case win loss or tie)
                max_eval = max(max_eval, eval)#find the max that leads to the highest scores
            return max_eval
        else:
            min_eval = float('inf')#same thing as max but if were minimizing but for the ai
            for next_state in game_state.next_states():
                eval = self.minimax(next_state)
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, game_state: TicTacToe) -> Optional[tuple[int, int]]:
        """
        Finds the best move for the AI using the Minimax algorithm.
        
        @params
            game_state: The current TicTacToe game state.
        @returns
            A tuple (row, col) representing the best move, or None if no moves are possible.
        """
        best_score = -float('inf') if game_state.get_current_player() == self.maximizing_player else float('inf')#check whether were going for higherst or lowest score
        best_move = None
        
        # We need to iterate through possible moves and evaluate them
        # For each empty cell, create a hypothetical new game state and apply the move
        for r in range(game_state.size):#by row
            for c in range(game_state.size):#by column
                if game_state.board[r][c] == 0:#choose a spot
                    temp_game = copy.deepcopy(game_state)#create a temporary game so we can try and see the best score we can get
                    temp_game.play(r, c)
                    
                    score = self.minimax(temp_game)#get the score of the game if we were to play the chosen spot

                    if game_state.get_current_player() == self.maximizing_player:#if were going for highest score 
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)#current best moves ( may change after testing new spots)
                    else: #if were going for the lowest score
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
        return best_move#return the best mvoe

def main():
    board_size = 3
    game = TicTacToe(board_size)

    ai = MinimaxAI(maximizing_player=-1) # AI plays as O. Since O is -1, we are truomg tp maximizE

    print("You are X. The AI is O.")
    print("Enter your moves as 'row,column' (0-2, 0-2)")

    while True:
        print("\n" + "="*20)
        print_board(game)

        winner = game.check_win()
        if winner is not None:
            if winner == 1:
                print("Game Over! You (X) win!")
            elif winner == -1:
                print("Game Over! AI (O) wins!")
            else:
                print("Game Over! It's a Tie!")
            break 

        current_player = game.get_current_player()

        if current_player == 1:#player turn 
            while True:
                move_input = input("Your turn (X). Enter row,column: ")
                r, c = map(int, move_input.split(','))
                if game.play(r, c) == 1:
                    break #if valid. ,pve on
                else:
                    print("Invalid move. Cell occupied or out of bounds. Try again.")

        else: #AI turn
            best_move = ai.find_best_move(game)
            if best_move:
                game.play(best_move[0], best_move[1])
                print(f"AI (O) played at {best_move[0]},{best_move[1]}")
            else:
                print("AI has no valid moves left. This shouldn't happen before a tie/win.")
                break # Should be caught by check_win earlier


main()

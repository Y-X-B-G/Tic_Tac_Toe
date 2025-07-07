from tic_tac_toe import TicTacToe
from typing import Optional, List, Self


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
    
#######################################################################################################################################################################

def print_board(game: TicTacToe):
    """Prints the board with X in red and O in blue for better visualization."""

    size = game.size
    output = ""
    for r_idx, row in enumerate(game.board):
        for c_idx, cell in enumerate(row):
            if cell == 1:
                output += f"X"
            elif cell == -1:
                output += f"O"
            else:
                output += " "
            if c_idx < size - 1:
                output += "|"
        output += "\n"
        if r_idx < size - 1:
            output += "—" * (size * 2 - 1) + "\n" 
    print(output)
    print(f"Current Turn: {'X' if game.get_current_player() == 1 else 'O'} (Round: {game.round})")


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


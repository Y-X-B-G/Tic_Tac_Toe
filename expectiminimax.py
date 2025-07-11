from tic_tac_toe import TicTacToe
from typing import Optional, List, Self
import copy

class ExpectiminimaxAI:#assuming 1 is AI and -1 is Playuer
    def __init__(self, maximizing_player: int):
        """
        Initializes the MinimaxAI.
        
        @params
            maximizing_player: The player (1 for X, -1 for O) for whom the AI is maximizing.
        """
        self.maximizing_player = maximizing_player

    def expectiminimax(self, game_state: TicTacToe, depth: int = 0) -> float:
        """
        Implements the Expectiminimax algorithm


        
        @params
            game_state: The current TicTacToe game state.
            depth; depth of recursion (keeps track of turns)
        @returns
            Expected utility value of current game state
        """
        winner = game_state.check_win()

        if winner == self.maximizing_player:
            return 1  #AI wins
        elif winner == -self.maximizing_player:
            return -1 #Opponent wins
        elif winner == 0:
            return 0  #Tie

        #Chance node (after each round(every 2 plies), apply stochastic delete
        if depth > 0 and depth % 2 == 0:
            total_utility = 0   #sum of utilities from all different deletions
            count = 0           #count of valid cells(filled) that can be deleted

            #go through each cell
            for row in range(game_state.size):
                for col in range(game_state.size):
                    #check if a cell can be deleted(either 1 or -1)
                    if game_state.board[row][col] != 0:
                        original_val = game_state.board[row][col] #store the current value for retrieval
                        game_state.set_board(row, col, 0) # delete (set to 0) the cell temporarily to determine utility

                        # evaluate new state after deltion
                        utility = self.expectiminimax(game_state, depth + 1)
                        total_utility += utility   #sum utility values
                        count += 1                 #keep track of deletions


                        game_state.set_board(row, col, original_val) #restore original val to board
            if count > 0:
                return total_utility / count
            else: 
                return 0
        
        #MAX node(Player maximizing score)
        if game_state.get_current_player() == self.maximizing_player:#if the player that were maximizing's turn
            max_eval = -float('inf')# set the max (alpha) to -inf
            for next_state in game_state.next_states():#go through all the next possible game states
                eval = self.expectiminimax(next_state, depth + 1)#keep going until all base case is found (by base case win loss or tie)
                max_eval = max(max_eval, eval)#find the max that leads to the highest scores
            return max_eval
        #MIN node(opponent minimizing score)
        else:
            min_eval = float('inf')#same thing as max but if were minimizing but for the ai
            for next_state in game_state.next_states():
                eval = self.expectiminimax(next_state, depth + 1)
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, game_state: TicTacToe) -> Optional[tuple[int, int]]:
        """
        Finds the best move for the AI using the Expectiminimax algorithm.
        
        @params
            game_state: The current TicTacToe game state.
        @returns
            A tuple (row, col) representing the best move, or None if no moves are possible.
        """
        best_score = -float('inf') if game_state.get_current_player() == self.maximizing_player else float('inf')#check whether were going for higherst or lowest score
        best_move = None
        
        for r in range(game_state.size):#by row
            for c in range(game_state.size):#by column
                if game_state.board[r][c] == 0:#choose a spot
                    temp_game = copy.deepcopy(game_state)#create a temporary game so we can try and see the best score we can get
                    temp_game.play(r, c)
                    
                    score = self.expectiminimax(temp_game, depth = 1)#get the score of the game if we were to play the chosen spot

                    if game_state.get_current_player() == self.maximizing_player:#if were going for highest score 
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)#current best moves ( may change after testing new spots)
                    else: #if were going for the lowest score
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
        return best_move#return the best mvoe



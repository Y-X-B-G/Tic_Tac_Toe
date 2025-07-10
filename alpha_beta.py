from tic_tac_toe import TicTacToe
from typing import Optional, List, Self
import copy

class Minimax_AB:#assuming 1 is AI and -1 is Playuer
    def __init__(self, maximizing_player: int):
        """
      
        
        @params
            maximizing_player: The player (1 for X, -1 for O) for whom the AI is maximizing.
        """
        self.maximizing_player = maximizing_player

    def minimax(self, game_state: TicTacToe, alpha: float, beta: float) -> int:
        #When calling, start with self.minimax(game_state, -float('inf'), float('inf'))
        """
        Implements the Minimax algorithm to find the optimal score for the current state.
        This function assumes that the current player is the maximizing player. 
        Alpha-beta pruning added for efficiency.
        
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
                alpha = max(alpha, eval)  # Update alpha for pruning
            if beta <= alpha:  
                return max_eval  # Beta cut-off
            
            #If reached, no cut-off, return the max evaluation found
            return max_eval

        else:
            min_eval = float('inf')#same thing as max but if were minimizing but for the ai
            for next_state in game_state.next_states():
                eval = self.minimax(next_state)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)  # Update beta for pruning
            if beta <= alpha:
                return min_eval  # Alpha cut-off

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
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
    
    def chance_node(self, game_state: TicTacToe, depth:int ) -> float:
        """
        Calculates the expected utility of a chance node in the Expectiminimax algorithm.
        Add rest of docstring later. 
        """
        winner = game_state.check_win()

        if winner == self.maximizing_player:
            return float(1) #AI wins
        elif winner == -self.maximizing_player:
            return float(-1) #Opponent wins
        elif winner == 0:
            return (0) #Tie
        else:
            stochastic_result = game_state.stochastic_delete()
            if stochastic_result is None:
                winner = game_state.check_win()
                if winner == self.maximizing_player:
                    return float(1)
                elif winner == -self.maximizing_player:
                    return float(-1)
                elif winner == 0:
                    return float(0)
                else:
                    # No winner and nothing left to delete → tie
                    return float(0)
            else:
                row, col, value = stochastic_result
                utility = self.expectiminimax(game_state, depth+1)
                game_state.set_board(row,col,value)
                return utility


    def expectiminimax(self, game_state: TicTacToe, depth: int) -> float:
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
            return float(1)
        elif winner == -self.maximizing_player:
            return float(-1)
        elif winner == 0:
            return float(0)

        if depth %2 ==0:
            return self.chance_node(game_state,depth)
        else:
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



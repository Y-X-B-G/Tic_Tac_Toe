from tic_tac_toe import TicTacToe
from typing import Optional, List, Self
import copy
import random
class ExpectiminimaxAI:
    def __init__(self, maximizing_player: int, max_depth: int = 4):
        self.maximizing_player = maximizing_player # X: 1, O: -1
        self.max_depth = max_depth

    def chance_node(self, game_state: TicTacToe, depth: int, alpha, beta): 
 
        filled_positions = game_state.get_filled_positions()
        if not filled_positions:
            return self.expectiminimax(game_state,depth+1,alpha,beta,is_chance_turn = True)
        
        expected_val = 0
        boardSize = game_state.size
        num_samples = len(filled_positions) if boardSize <= 4 else min(5, len(filled_positions))

        for _ in range(num_samples):
            temp_game = copy.deepcopy(game_state)
            result = temp_game.stochastic_delete(filled_positions)

            if result is None:
                continue  

            eval_val = self.expectiminimax(temp_game, depth + 1, alpha, beta, is_chance_turn=True)

            if eval_val is not None:
                expected_val += eval_val

        return expected_val / num_samples if num_samples else 0
            


    def expectiminimax(self, game_state: TicTacToe, depth: int, alpha, beta, is_chance_turn: bool = False):
        winner = game_state.check_win()
        if winner is not None:
            if winner == self.maximizing_player:
                return 1.0
            elif winner == -self.maximizing_player:
                return -1.0
            else: #Tie
                return 0.0
            
        if depth >= self.max_depth:
            return 0.0 #return 0 at max depth
        if not is_chance_turn and game_state.round > 0 and game_state.round % 2 == 0:#if the turn is even and not 0 then delete random piece
            return self.chance_node(game_state, depth, alpha, beta) #alpha be
        
        if game_state.get_current_player() == self.maximizing_player:
            max_eval = -float('inf')
            for next_state in game_state.next_states():
                eval_val = self.expectiminimax(next_state, depth + 1, alpha, beta)
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha,eval_val)
                if beta <= alpha: 
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for next_state in game_state.next_states():
                eval_val = self.expectiminimax(next_state, depth + 1, alpha, beta)
                min_eval = min(min_eval, eval_val)
                beta = min(beta,eval_val)
                if beta <= alpha: 
                    break
            return min_eval

    def find_best_move(self, game_state: TicTacToe):
        best_score = -float('inf') if game_state.get_current_player() == self.maximizing_player else float('inf')
        best_move = None
        
        for r in range(game_state.size):
            for c in range(game_state.size):
                if game_state.board[r][c] == 0:
                    temp_game = copy.deepcopy(game_state)
                    temp_game.play(r, c)
                    
                    score = self.expectiminimax(temp_game, depth=0, alpha = -float('inf'),beta = float('inf'))
                    if game_state.get_current_player() == self.maximizing_player:
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
        return best_move

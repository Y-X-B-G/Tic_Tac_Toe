from tic_tac_toe import TicTacToe
from typing import Optional, List, Self
import copy

class ExpectiminimaxAI:
    def __init__(self, maximizing_player: int, max_depth: int = 4):
        self.maximizing_player = maximizing_player # X: 1, O: -1
        self.max_depth = max_depth

    def chance_node(self, game_state: TicTacToe, depth: int):
        filled_positions = []

        for r in range(game_state.size):
            for c in range(game_state.size):
                if game_state.board[r][c] != 0:
                    filled_positions.append((r, c))#find all the occupied spaces (non zero) and add them to the board
        if not filled_positions:#if empty board , run expectiminimax normally
            return self.expectiminimax(game_state, depth, is_chance_turn=True)
        expected_value = 0
        num_outcomes = len(filled_positions)

        for r, c in filled_positions:
            temp_game = copy.deepcopy(game_state)
            temp_game.board[r][c] = 0#create a copy of the game with one of the filled positions set to 0
            expected_value += self.expectiminimax(temp_game, depth + 1, is_chance_turn=True)#run expectiminimax

        return expected_value / num_outcomes

    def expectiminimax(self, game_state: TicTacToe, depth: int, is_chance_turn: bool = False):
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
            return self.chance_node(game_state, depth)
        if game_state.get_current_player() == self.maximizing_player:
            max_eval = -float('inf')
            for next_state in game_state.next_states():
                eval_val = self.expectiminimax(next_state, depth + 1)
                max_eval = max(max_eval, eval_val)
            return max_eval
        else:
            min_eval = float('inf')
            for next_state in game_state.next_states():
                eval_val = self.expectiminimax(next_state, depth + 1)
                min_eval = min(min_eval, eval_val)
            return min_eval

    def find_best_move(self, game_state: TicTacToe):
        best_score = -float('inf') if game_state.get_current_player() == self.maximizing_player else float('inf')
        best_move = None
        
        for r in range(game_state.size):
            for c in range(game_state.size):
                if game_state.board[r][c] == 0:
                    temp_game = copy.deepcopy(game_state)
                    temp_game.play(r, c)
                    
                    score = self.expectiminimax(temp_game, depth=0)
                    if game_state.get_current_player() == self.maximizing_player:
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
        return best_move

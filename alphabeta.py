from tic_tac_toe import TicTacToe
from typing import Optional, List, Self
import copy

class AlphaBetaAI:
    def __init__(self, maximizing_player: int):
        self.maximizing_player = maximizing_player
        self.max_depth = None

    def _calculate_ways_to_win(self, game_state: TicTacToe, player: int) -> int:
        ways = 0
        size = game_state.size
        board = game_state.board
        opponent = -player

        for r in range(size):
            if opponent not in board[r]:
                ways += 1

        for c in range(size):
            col = [board[r][c] for r in range(size)]
            if opponent not in col:
                ways += 1

        diag1 = [board[i][i] for i in range(size)]
        if opponent not in diag1:
                ways += 1

        diag2 = [board[i][size - 1 - i] for i in range(size)]
        if opponent not in diag2:
                ways += 1

        return ways

    def _heuristic_evaluation(self, game_state: TicTacToe) -> float:
        our_ways = self._calculate_ways_to_win(game_state, self.maximizing_player)
        opponent_ways = self._calculate_ways_to_win(game_state, -self.maximizing_player)

        if (our_ways + opponent_ways) == 0:
            return 0.0

        return (our_ways - opponent_ways) / (our_ways + opponent_ways)

    def minimax(self, game_state: TicTacToe, depth: int, alpha: float, beta: float) -> float:
        winner = game_state.check_win()

        if winner == self.maximizing_player:
            return 1
        elif winner == -self.maximizing_player:
            return -1
        elif winner == 0:
            return 0
        
        if self.max_depth is not None and depth == self.max_depth:
            return self._heuristic_evaluation(game_state)

        if game_state.get_current_player() == self.maximizing_player:
            max_eval = -float('inf')
            for next_state in game_state.next_states():
                eval = self.minimax(next_state, depth + 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break 
            return max_eval

        else:
            min_eval = float('inf')
            for next_state in game_state.next_states():
                eval = self.minimax(next_state, depth + 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break 
            return min_eval

    def find_best_move(self, game_state: TicTacToe) -> Optional[tuple[int, int]]:
        if game_state.size > 3:
            self.max_depth = 3
        else:
            self.max_depth = None

        current_player = game_state.get_current_player()
        
        best_score = -float('inf') if current_player == self.maximizing_player else float('inf')
        best_move = None
        
        for r in range(game_state.size):
            for c in range(game_state.size):
                if game_state.board[r][c] == 0:
                    temp_game = copy.deepcopy(game_state)
                    temp_game.play(r, c)
                    
                    score = self.minimax(temp_game, 1, -float('inf'), float('inf'))

                    if current_player == self.maximizing_player:
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
        
        return best_move

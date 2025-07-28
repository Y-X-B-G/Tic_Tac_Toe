from tic_tac_toe import TicTacToe
from typing import Optional, List, Self
import copy

class MinimaxAI:#assuming 1 is AI and -1 is Playuer
    def __init__(self, maximizing_player: int):
        
        self.maximizing_player = maximizing_player
        self.max_depth = None # Initialize max_depth, will be set in find_best_move

    def _calculate_ways_to_win(self, game_state: TicTacToe, player: int) -> int:
        """
        Calculates the number of ways a player can win based on the current board state.
        
        @params 
            game_state: TicTacToe - The current game state.
            player: int - The player (1 or -1) for whom the winning ways are calculated.
        @returns
            ways: int - The number of ways the given player can still win.
        """
        ways = 0
        size = game_state.size
        board = game_state.board
        opponent = -player

        #check rows
        for r in range(size):
            if opponent not in board[r]:
                ways += 1

        #check columns
        for c in range(size):
            col = [board[r][c] for r in range(size)]
            if opponent not in col:
                ways += 1

        #check diagonals
        diag1 = [board[i][i] for i in range(size)]
        if opponent not in diag1:
            ways += 1

        diag2 = [board[i][size - 1 - i] for i in range(size)]
        if opponent not in diag2:
            ways += 1

        return ways

    def _heuristic_evaluation(self, game_state: TicTacToe) -> float:
        """
        Evaluates the current game state using a heuristic function.
        
        @params 
            game_state: TicTacToe - The current game state.
        @returns
            float - A score between -1 and 1 that represents how favorable the board is for the AI relative to the opponent.
        """
        our_ways = self._calculate_ways_to_win(game_state, self.maximizing_player)
        opponent_ways = self._calculate_ways_to_win(game_state, -self.maximizing_player)

        if (our_ways + opponent_ways) == 0:
            return 0.0

        return (our_ways - opponent_ways) / (our_ways + opponent_ways)

    def minimax(self, game_state: TicTacToe, depth: int) -> float:
        """
        Recursively uses the minimax algorithm to evaluate the score of a given game state.
        
        @params 
            game_state: TicTacToe - The current game state.
            depth: int - The current depth of the recursion tree.
        @returns
            float - The score of the game state. 1 for AI win, -1 for opponent win, 0 for a tie, or a heuristic value otherwise.
        """
        winner = game_state.check_win()

        if winner == self.maximizing_player:
            return 1  #AI wins
        elif winner == -self.maximizing_player:
            return -1 #Opponent wins
        elif winner == 0:
            return 0  #Tie
        
        if self.max_depth is not None and depth == self.max_depth:
            return self._heuristic_evaluation(game_state)

        if game_state.get_current_player() == self.maximizing_player:#if the player that were maximizing's turn
            max_eval = -float('inf')# set the max (alpha) to -inf
            for next_state in game_state.next_states():#go through all the next possible game states
                eval = self.minimax(next_state, depth + 1)#keep going until all base case is found (by base case win loss or tie), increment depth
                max_eval = max(max_eval, eval)#find the max that leads to the highest scores
            return max_eval
        else:
            min_eval = float('inf')#same thing as max but if were minimizing but for the ai
            for next_state in game_state.next_states():
                eval = self.minimax(next_state, depth + 1)
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, game_state: TicTacToe) -> Optional[tuple[int, int]]:
        """
        Finds the best move for the current player using the minimax algorithm.
        
        @params 
            game_state: TicTacToe - The current game state.
        @returns
            best_move: Optional[tuple[int, int]] - The (row, column) coordinates of the best move or None if no moves are available.
        """
        if game_state.size > 3:
            self.max_depth = 3 #chosen depth for larger boards
        else:
            self.max_depth = None #no depth limit for 3x3 or smaller since its fast enough anywys

        best_score = -float('inf') if game_state.get_current_player() == self.maximizing_player else float('inf')#check whether were going for higherst or lowest score
        best_move = None
        
        for r in range(game_state.size):#by row
            for c in range(game_state.size):#by column
                if game_state.board[r][c] == 0:#choose a spot
                    temp_game = copy.deepcopy(game_state)#create a temporary game so we can try and see the best score we can get
                    temp_game.play(r, c)
                    
                    score = self.minimax(temp_game, 1) #start initial depth at 1

                    if game_state.get_current_player() == self.maximizing_player:#if were going for highest score 
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)#current best moves ( may change after testing new spots)
                    else: #if were going for the lowest score
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
        return best_move#return the best mvoe

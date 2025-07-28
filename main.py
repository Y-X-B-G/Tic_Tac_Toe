import time
import random
from tic_tac_toe import TicTacToe
from minimax import MinimaxAI
from expectiminimax import ExpectiminimaxAI
from alphabeta import AlphaBetaAI
from Gemini import GeminiAI
from Gemini import parse_gemini_response
from csvLogger import CSVLogger


def Human_vs_Minimax(board_size):
    """
        Plays a game of Tic Tac Toe between a human player (X) and Minimax AI (O).
        The human player goes first and provides input in the format 'row, column'.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Human (X) vs Minimax AI (O)")
    print("Enter your moves as 'row,column' (0-2,0-2)")

    while True:
        print(game)
        r, c = map(int, input("Your move: ").split(","))
        if not game.play(r, c):
            print("Invalid move. Try again.")
            continue
        if (winner := game.check_win()) is not None:
            print(game)
            print("Human (X) wins!" if winner == 1 else "Minimax AI (O) wins!" if winner == -1 else "It's a draw!")
            break
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"AI (O) played at {r},{c}")
        else:
            print("No valid moves left for AI (O).")
        if (winner := game.check_win()) is not None:
            print(game)
            print("Human (X) wins!" if winner == 1 else "Minimax AI (O) wins!" if winner == -1 else "It's a draw!")
            break

def Gemini_vs_Minimax(board_size):                                                        ##Has CSV version
    """
        Plays a game of Tic Tac Toe between Gemini AI (X) and Minimax AI (O).
        Gemini AI goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    """Gemini AI (X) goes first vs Minimax AI (O)"""
    game = TicTacToe(board_size)
    print("Gemini AI (X) vs Minimax AI (O)")
    was_wrong = [-1,-1,-1]
    while True:
        print(game)
        response = GeminiAI(game.board, was_wrong)
        r, c = map(int, response.split(","))
        game.play(r, c)
        print(f"X (Gemini) played at {r},{c}")
        if game.check_win() is not None: break
        
        print(game)
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Minimax) played at {r},{c}")
        else:
            print("No valid moves left for O (Minimax).")
            break
        if game.check_win() is not None: break

    print(game)
    winner = game.check_win()
    print("Gemini (X) wins!" if winner == 1 else "Minimax (O) wins!" if winner == -1 else "It's a draw!")

def Minimax_vs_AlphaBeta(board_size):                                           #Has CSV version
    """
        Plays a game of Tic Tac Toe between Minimax AI (X) and AlphaBeta AI (O).
        Minimax AI goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Minimax AI (X) vs Alpha-Beta AI (O)")
    while True:
        print(game)
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        if move is None:
            print("No valid moves left for X (Minimax).")
            break
        r, c = move
        game.play(r, c)
        print(f"X (Minimax) played at {r},{c}")
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        move = AlphaBetaAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Alpha-Beta) played at {r},{c}")
        else:
            print("No valid moves left for O (Alpha-Beta).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Minimax (X) wins!" if winner == 1 else "Alpha-Beta (O) wins!" if winner == -1 else "It's a draw!")

def AlphaBeta_vs_Minimax(board_size):                                               #Has CSV 
    """
        Plays a game of Tic Tac Toe between Alphabeta AI (X) and Minimax AI (O).
        AlphaBeta AI goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Alpha-Beta AI (X) vs Minimax AI (O)")
    while True:
        print(game)
        move = AlphaBetaAI(maximizing_player=1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"X (Alpha-Beta) played at {r},{c}")
        else:
            print("No valid moves left for X (Alpha-Beta).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Minimax) played at {r},{c}")
        else:
            print("No valid moves left for O (Minimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Alpha-Beta (X) wins!" if winner == 1 else "Minimax (O) wins!" if winner == -1 else "It's a draw!")

def Minimax_vs_Expectiminimax(board_size):                                      #Has CSV version
    """
        Plays a game of Tic Tac Toe between Minimax AI (X) and Expectiminimax AI (O).
        Minimax AI goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Minimax AI (X) vs Expectiminimax AI (O)")
    while True:
        print(game)
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"X (Minimax) played at {r},{c}")
        else:
            print("No valid moves left for X (Minimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        move = ExpectiminimaxAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Expectiminimax) played at {r},{c}")
        else:
            print("No valid moves left for O (Expectiminimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Minimax (X) wins!" if winner == 1 else "Expectiminimax (O) wins!" if winner == -1 else "It's a draw!")

def Expectiminimax_vs_Minimax(board_size):                         #Has CSV version
    """
        Plays a game of Tic Tac Toe between Expectiminimax AI (X) and Minimax AI (O).
        Expectiminimax AI goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Expectiminimax AI (X) vs Minimax AI (O)")
    while True:
        print(game)
        move = ExpectiminimaxAI(maximizing_player=1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"X (Expectiminimax) played at {r},{c}")
        else:
            print("No valid moves left for X (Expectiminimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Minimax) played at {r},{c}")
        else:
            print("No valid moves left for O (Minimax).")
            break
        if game.check_win() is not None: break
    print(game)
    winner = game.check_win()
    print("Expectiminimax (X) wins!" if winner == 1 else "Minimax (O) wins!" if winner == -1 else "It's a draw!")

def Minimax_self_play(board_size):                                                      #Doens't have CSV
    """
        Plays a self-play game of Tic Tac Toe between two Minimax AI players (X and O).
        Minimax AI (X) goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    """Minimax AI (X) vs Minimax AI (O)"""
    game = TicTacToe(board_size)
    print("Minimax AI (X) vs Minimax AI (O)")
    while True:
        print(game)
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"X (Minimax) played at {r},{c}")
        else:
            print("No valid moves left for X (Minimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Minimax) played at {r},{c}")
        else:
            print("No valid moves left for O (Minimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Minimax (X) wins!" if winner == 1 else "Minimax (O) wins!" if winner == -1 else "It's a draw!")

def AlphaBeta_self_play(board_size): #NO CSV
    """
        Plays a self-play game of Tic Tac Toe between two AlphaBeta AI players (X and O).
        AlphaBeta AI (X) goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Alpha-Beta AI (X) vs Alpha-Beta AI (O)")
    while True:
        print(game)
        move = AlphaBetaAI(maximizing_player=1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"X (Alpha-Beta) played at {r},{c}")
        else:
            print("No valid moves left for X (Alpha-Beta).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        move = AlphaBetaAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Alpha-Beta) played at {r},{c}")
        else:
            print("No valid moves left for O (Alpha-Beta).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Alpha-Beta (X) wins!" if winner == 1 else "Alpha-Beta (O) wins!" if winner == -1 else "It's a draw!")

def Expectiminimax_self_play(board_size):
    """
        Plays a self-play game of Tic Tac Toe between two Expectiminimax AI players (X and O).
        Expectiminimax AI (X) goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Expectiminimax AI (X) vs Expectiminimax AI (O)")
    while True:
        print(game)
        move = ExpectiminimaxAI(maximizing_player=1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"X (Expectiminimax) played at {r},{c}")
        else:
            print("No valid moves left for X (Expectiminimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        move = ExpectiminimaxAI(maximizing_player=-1).find_best_move(game)
        if move is not None:
            r, c = move
            game.play(r, c)
            print(f"O (Expectiminimax) played at {r},{c}")
        else:
            print("No valid moves left for O (Expectiminimax).")
            break
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Expectiminimax (X) wins!" if winner == 1 else "Expectiminimax (O) wins!" if winner == -1 else "It's a draw!")

##Doens't work yet
def Gemini_self_play(board_size):
    """
        Plays a self-play game of Tic Tac Toe between two Gemini AI players (X and O).
        Gemini AI (X) goes first and the game runs until a result is determined.
        
        @params 
            board_size: int - The size of the Tic Tac Toe board (n x n).
        @returns
            None
    """
    game = TicTacToe(board_size)
    print("Gemini AI (X) vs Gemini AI (O)")
    was_wrong_x = [-1, -1, -1]
    was_wrong_o = [-1, -1, -1]
    while True:
        print(game)
        response = GeminiAI(game.board, was_wrong_x)
        r, c = map(int, response.split(","))
        game.play(r, c)
        print(f"X (Gemini) played at {r},{c}")
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        response = GeminiAI(game.board, was_wrong_o)
        r, c = map(int, response.split(","))
        game.play(r, c)
        print(f"O (Gemini) played at {r},{c}")
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Gemini (X) wins!" if winner == 1 else "Gemini (O) wins!" if winner == -1 else "It's a draw!")

######################################################################################################################
    """Below contains all of the of the CSV logging code -- DO NOT TOUCH WITHOUT INFORMING HUMAYOUN"""
#####################################################################################################################

def Gemini_vs_Minimax_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    was_wrong = [-1, -1, -1]
    turn_count = 0

    start_time = time.time()
    gemini_time = 0
    mini_time = 0


    while True:
        # Gemini's move
        a1_start = time.time()
        response = GeminiAI(game.board, was_wrong)
    
        move = parse_gemini_response(response, board_size)
       
        a1_end = time.time()
        gemini_time += a1_start- a1_end
        
        if move is None:
            valid_moves = [
                (r, c)
                for r in range(board_size)
                for c in range(board_size)
                if game.board[r][c] == 0
            ]
            if valid_moves:
                r, c = random.choice(valid_moves)
            else:
                break
        else:
            r, c = move
        result = game.play(r, c)
        if result:
            turn_count += 1
    
        if game.check_win() is not None:
            break

        # Minimax's move
        a2_start = time.time()
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        a2_end = time.time()

        mini_time += a2_start - a2_end
        if move is not None:
            r, c = move
            result = game.play(r, c)
            if result:
                turn_count += 1
        else:
            break
       
        if game.check_win() is not None:
            break

    end_time = time.time()
    total_runtime = end_time - start_time

    winner_value = game.check_win()
    if winner_value == 1:
        winner = "X"
    elif winner_value == -1:
        winner = "O"
    elif winner_value == 0:
        winner = "Draw"
    else:
        winner = "Unknown"

    csv_logger.log_game(
        board_size=board_size,
        player_x="GeminiAI",
        playerx_runtime = gemini_time,
        player_o="MinimaxAI",
        playero_runtime = mini_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )
    time.sleep(0.2)
    total_runtime -= 0.2

def Minimax_vs_AlphaBeta_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()
    a1_time = 0
    a2_time = 0
    while True:
        # Minimax X
        a1_start = time.time()
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        a1_end = time.time()

        a1_time += a1_start - a1_end
        if move is None:
            break
        r, c = move
        result = game.play(r, c)
        if result:
            turn_count += 1
        if game.check_win() is not None:
            break

        # AlphaBeta O
        a2_start = time.time()
        move = AlphaBetaAI(maximizing_player=-1).find_best_move(game)
        a2_end = time.time()
        a2_time += a2_start- a2_end
        if move is None:
            break
        r, c = move
        result = game.play(r, c)
        if result:
            turn_count += 1
        if game.check_win() is not None:
            break

    end_time = time.time()
    total_runtime = end_time - start_time

    winner_value = game.check_win()
    if winner_value == 1:
        winner = "X"
    elif winner_value == -1:
        winner = "O"
    elif winner_value == 0:
        winner = "Draw"
    else:
        winner = "Unknown"

    csv_logger.log_game(
        board_size=board_size,
        player_x="MinimaxAI",
        playerx_runtime = a1_time,
        player_o="AlphaBetaAI",
        playero_runtime = a2_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )
def Minimax_vs_Expectiminimax_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()
    a1_time = 0
    a2_time = 0
    while True:
        a1_start = time.time()
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        a1_end = time.time()

        a1_time += a1_start - a1_end
        if move is None:
            break
        r, c = move
        result = game.play(r, c)
        if result:
            turn_count += 1
        if game.check_win() is not None:
            break
        a2_start = time.time()
        move = ExpectiminimaxAI(maximizing_player=-1).find_best_move(game)
        a2_end = time.time()
        a2_time += a2_start- a2_end

        if move is None:
            break
        r, c = move
        result = game.play(r, c)
        if result:
            turn_count += 1
        if game.check_win() is not None:
            break

    end_time = time.time()
    total_runtime = end_time - start_time

    winner_value = game.check_win()
    if winner_value == 1:
        winner = "X"
    elif winner_value == -1:
        winner = "O"
    elif winner_value == 0:
        winner = "Draw"
    else:
        winner = "Unknown"

    csv_logger.log_game(
        board_size=board_size,
        player_x="MinimaxAI",
        playerx_runtime = a1_time,
        player_o="ExpectiminimaxAI",
        playero_runtime = a2_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )
def Gemini_vs_AlphaBeta_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    was_wrong = [-1, -1, -1]
    turn_count = 0

    start_time = time.time()
    gemini_runtime = 0
    opponent_runtime = 0

    while True:
        gem_start = time.time()
        response = GeminiAI(game.board, was_wrong)
        gem_end = time.time()
        gemini_runtime += (gem_end - gem_start)

        move = parse_gemini_response(response, board_size)
        if move is None:
            valid_moves = [(r, c) for r in range(board_size) for c in range(board_size) if game.board[r][c] == 0]
            if valid_moves:
                r, c = random.choice(valid_moves)
            else:
                break
        else:
            r, c = move

        if game.play(r, c):
            turn_count += 1
        if game.check_win() is not None:
            break

        opp_start = time.time()
        move = AlphaBetaAI(maximizing_player=-1).find_best_move(game)
        opp_end = time.time()
        opponent_runtime += (opp_end - opp_start)

        if move is not None:
            r, c = move
            if game.play(r, c):
                turn_count += 1
        else:
            break
        if game.check_win() is not None:
            break

    total_runtime = time.time() - start_time
    winner_value = game.check_win()
    winner = "X" if winner_value == 1 else "O" if winner_value == -1 else "Draw"

    csv_logger.log_game(
        board_size=board_size,
        player_x="GeminiAI",
        playerx_runtime=gemini_runtime,
        player_o="AlphaBetaAI",
        playero_runtime=opponent_runtime,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )


def Gemini_vs_Expectiminimax_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    was_wrong = [-1, -1, -1]
    turn_count = 0

    start_time = time.time()
    gemini_runtime = 0
    opponent_runtime = 0

    while True:
        gem_start = time.time()
        response = GeminiAI(game.board, was_wrong)
        gem_end = time.time()
        gemini_runtime += (gem_end - gem_start)

        move = parse_gemini_response(response, board_size)
        if move is None:
            valid_moves = [(r, c) for r in range(board_size) for c in range(board_size) if game.board[r][c] == 0]
            if valid_moves:
                r, c = random.choice(valid_moves)
            else:
                break
        else:
            r, c = move

        if game.play(r, c):
            turn_count += 1
        if game.check_win() is not None:
            break

        opp_start = time.time()
        move = ExpectiminimaxAI(maximizing_player=-1).find_best_move(game)
        opp_end = time.time()
        opponent_runtime += (opp_end - opp_start)

        if move is not None:
            r, c = move
            if game.play(r, c):
                turn_count += 1
        else:
            break
        if game.check_win() is not None:
            break

    total_runtime = time.time() - start_time
    winner_value = game.check_win()
    winner = "X" if winner_value == 1 else "O" if winner_value == -1 else "Draw"

    csv_logger.log_game(
        board_size=board_size,
        player_x="GeminiAI",
        playerx_runtime=gemini_runtime,
        player_o="ExpectiminimaxAI",
        playero_runtime=opponent_runtime,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )


def AlphaBeta_vs_Minimax_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()
    alpha_time = 0
    mini_time = 0

    while True:
        a_start = time.time()
        move = AlphaBetaAI(maximizing_player=1).find_best_move(game)
        a_end = time.time()
        alpha_time += (a_end - a_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count +=1
        else:
            break
        if game.check_win() is not None: break

        m_start = time.time()
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        m_end = time.time()
        mini_time += (m_end - m_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count += 1 
        else:
            break
        if game.check_win() is not None: break

    total_runtime = time.time() - start_time
    winner_value = game.check_win()
    winner = "X" if winner_value == 1 else "O" if winner_value == -1 else "Draw"

    csv_logger.log_game(
        board_size=board_size,
        player_x="AlphaBetaAI",
        playerx_runtime=alpha_time,
        player_o="MinimaxAI",
        playero_runtime=mini_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )

def Expectiminimax_vs_Minimax_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()
    exp_time = 0
    mini_time = 0

    while True:
        e_start = time.time()
        move = ExpectiminimaxAI(maximizing_player=1).find_best_move(game)
        e_end = time.time()
        exp_time += (e_end - e_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count +=1
        else:
            break
        if game.check_win() is not None: break

        m_start = time.time()
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        m_end = time.time()
        mini_time += (m_end - m_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count += 1
        else:
            break
        if game.check_win() is not None: break

    total_runtime = time.time() - start_time
    winner_value = game.check_win()
    winner = "X" if winner_value == 1 else "O" if winner_value == -1 else "Draw"

    csv_logger.log_game(
        board_size=board_size,
        player_x="ExpectiminimaxAI",
        playerx_runtime=exp_time,
        player_o="MinimaxAI",
        playero_runtime=mini_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )

def Minimax_self_play_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()
    x_time = 0
    o_time = 0

    while True:
        x_start = time.time()
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        x_end = time.time()
        x_time += (x_end - x_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count += 1
        else:
            break
        if game.check_win() is not None: break

        o_start = time.time()
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
        o_end = time.time()
        o_time += (o_end - o_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count +=1
        else:
            break
        if game.check_win() is not None: break

    total_runtime = time.time() - start_time
    winner_value = game.check_win()
    winner = "X" if winner_value == 1 else "O" if winner_value == -1 else "Draw"

    csv_logger.log_game(
        board_size=board_size,
        player_x="MinimaxAI",
        playerx_runtime=x_time,
        player_o="MinimaxAI",
        playero_runtime=o_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )

def Expectiminimax_self_play_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()
    x_time = 0
    o_time = 0

    while True:
        x_start = time.time()
        move = ExpectiminimaxAI(maximizing_player=1).find_best_move(game)
        x_end = time.time()
        x_time += (x_end - x_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count+=1 
        else:
            break
        if game.check_win() is not None: break

        o_start = time.time()
        move = ExpectiminimaxAI(maximizing_player=-1).find_best_move(game)
        o_end = time.time()
        o_time += (o_end - o_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count+=1
        else:
            break
        if game.check_win() is not None: break

    total_runtime = time.time() - start_time
    winner_value = game.check_win()
    winner = "X" if winner_value == 1 else "O" if winner_value == -1 else "Draw"

    csv_logger.log_game(
        board_size=board_size,
        player_x="ExpectiminimaxAI",
        playerx_runtime=x_time,
        player_o="ExpectiminimaxAI",
        playero_runtime=o_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )

def AlphaBeta_self_play_CSV(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()
    x_time = 0
    o_time = 0

    while True:
        x_start = time.time()
        move = AlphaBetaAI(maximizing_player=1).find_best_move(game)
        x_end = time.time()
        x_time += (x_end - x_start)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count +=1
        else:
            break
        if game.check_win() is not None: break

        o_start = time.time()
        move = AlphaBetaAI(maximizing_player=-1).find_best_move(game)
        o_end = time.time()
        o_time += (o_start-o_end)

        if move is not None:
            r, c = move
            game.play(r, c)
            turn_count += 1
        else:
            break
        if game.check_win() is not None: break

    total_runtime = time.time() - start_time
    winner_value = game.check_win()
    winner = "X" if winner_value == 1 else "O" if winner_value == -1 else "Draw"

    csv_logger.log_game(
        board_size=board_size,
        player_x="AlphaBetaAI",
        playerx_runtime=x_time,
        player_o="AlphaBetaAI",
        playero_runtime=o_time,
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )




if __name__ == "__main__":
    #Human_vs_Minimax(4)
    #Gemini_vs_Minimax(5)
    #Minimax_vs_AlphaBeta(4)
    #AlphaBeta_vs_Minimax(4)
    #Expectiminimax_vs_Minimax(6)
    #Minimax_self_play(3)
    #AlphaBeta_self_play(6)
    #Expectiminimax_self_play()
    #Gemini_self_play(3)

    csv_logger = CSVLogger("ai_game_results3.csv")


        
    board_sizes = [3,4,5,6]
    number_of_test_cycles = 5
    number_of_test_cycles = number_of_test_cycles +1 # to g  range
    for size in range(len(board_sizes)):
        board_size = board_sizes[size]
        for i in range(1,number_of_test_cycles):
            print(f"running test Cycle: {i}")
            print(f"board size: {board_size}\n ")
        
        
            print("Running Gemini vs Minimax")
            Gemini_vs_Minimax_CSV(board_size, csv_logger)

            print("Running Gemini VS Alphabeta")
            Gemini_vs_AlphaBeta_CSV(board_size,csv_logger)

            print("Running Gemini VS Expectminimax")
            Gemini_vs_Expectiminimax_CSV(board_size,csv_logger)
            print("Running Minimax VS Alpha Beta")
            Minimax_vs_AlphaBeta_CSV(board_size, csv_logger) 

            print("Running Minimax VS Expectminimax")
            Minimax_vs_Expectiminimax_CSV(board_size, csv_logger)


            print("Running AlphaBeta VS Minimax")
            AlphaBeta_vs_Minimax_CSV(board_size,csv_logger)

            print("Running Expectminimax VS Minimax")
            Expectiminimax_vs_Minimax_CSV(board_size,csv_logger)

            print("Running Minimax VS Minimax")
            Minimax_self_play_CSV(board_size,csv_logger) 

            print("Running AlphaBeta VS AlphaBeta")
            AlphaBeta_self_play_CSV(board_size,csv_logger)

            print("Running Expectminimax vs Expectminimax")
            Expectiminimax_self_play_CSV(board_size,csv_logger)

            print("\n===============================================================\n")
    csv_logger.close()
    
    print(f"Testing completed")

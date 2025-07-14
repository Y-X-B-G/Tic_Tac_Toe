import time
from tic_tac_toe import TicTacToe
from minimax import MinimaxAI
from expectiminimax import ExpectiminimaxAI
from alphabeta import AlphaBetaAI
from Gemini import GeminiAI
from csvLogger import CSVLogger

def Human_vs_Minimax(board_size):
    """Human (X) goes first vs Minimax AI (O)"""
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
        time.sleep(0.2)

def Gemini_vs_Minimax(board_size, csv_logger):
    game = TicTacToe(board_size)
    was_wrong = [-1, -1, -1]
    turn_count = 0

    start_time = time.time()

    while True:
        # Gemini's move
        response = GeminiAI(game.board, was_wrong)
        r, c = map(int, response.split(","))
        result = game.play(r, c)
        if result:
            turn_count += 1
        if game.check_win() is not None:
            break

        # Minimax's move
        move = MinimaxAI(maximizing_player=-1).find_best_move(game)
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
        player_o="MinimaxAI",
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )

def Minimax_vs_AlphaBeta(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()

    while True:
        # Minimax X
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        if move is None:
            break
        r, c = move
        result = game.play(r, c)
        if result:
            turn_count += 1
        if game.check_win() is not None:
            break

        # AlphaBeta O
        move = AlphaBetaAI(maximizing_player=-1).find_best_move(game)
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
        player_o="AlphaBetaAI",
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )

def AlphaBeta_vs_Minimax(board_size):
    """Alpha-Beta AI (X) goes first vs Minimax AI (O)"""
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

def Minimax_vs_Expectiminimax(board_size, csv_logger):
    game = TicTacToe(board_size)
    turn_count = 0
    start_time = time.time()

    while True:
        move = MinimaxAI(maximizing_player=1).find_best_move(game)
        if move is None:
            break
        r, c = move
        result = game.play(r, c)
        if result:
            turn_count += 1
        if game.check_win() is not None:
            break

        move = ExpectiminimaxAI(maximizing_player=-1).find_best_move(game)
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
        player_o="ExpectiminimaxAI",
        winner=winner,
        num_turns=turn_count,
        runtime_sec=total_runtime
    )

def Minimax_self_play(board_size):
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

def AlphaBeta_self_play(board_size):
    """Alpha-Beta AI (X) vs Alpha-Beta AI (O)"""
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
    """Expectiminimax AI (X) vs Expectiminimax AI (O)"""
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

def Gemini_self_play(board_size):
    """Gemini AI (X) vs Gemini AI (O)"""
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

if __name__ == "__main__":
    csv_logger = CSVLogger("ai_game_results.csv")

    for _ in range(10):
        Gemini_vs_Minimax(3, csv_logger)
        Minimax_vs_AlphaBeta(3, csv_logger)
        Minimax_vs_Expectiminimax(3, csv_logger)

    csv_logger.close()




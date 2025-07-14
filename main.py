import time
from tic_tac_toe import TicTacToe
from minimax import MinimaxAI
from expectiminimax import ExpectiminimaxAI
from alphabeta import AlphaBetaAI
from Gemini import GeminiAI

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

def Gemini_vs_Minimax(board_size):
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

def Minimax_vs_AlphaBeta(board_size):
    """Minimax AI (X) goes first vs Alpha-Beta AI (O)"""
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

def Minimax_vs_Expectiminimax(board_size):
    """Minimax AI (X) goes first vs Expectiminimax AI (O)"""
    game = TicTacToe(board_size)
    print("Minimax AI (X) vs Expectiminimax AI (O)")
    while True:
        print(game)
        r, c = MinimaxAI(maximizing_player=1).find_best_move(game)
        game.play(r, c)
        print(f"X (Minimax) played at {r},{c}")
        if game.check_win() is not None: break
        time.sleep(0.2)
        print(game)
        r, c = ExpectiminimaxAI(maximizing_player=-1).find_best_move(game)
        game.play(r, c)
        print(f"O (Expectiminimax) played at {r},{c}")
        if game.check_win() is not None: break
        time.sleep(0.2)
    print(game)
    winner = game.check_win()
    print("Minimax (X) wins!" if winner == 1 else "Expectiminimax (O) wins!" if winner == -1 else "It's a draw!")

def Expectiminimax_vs_Minimax(board_size):
    """Expectiminimax AI (X) goes first vs Minimax AI (O)"""
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
    #Human_vs_Minimax(4)
    #Gemini_vs_Minimax(4)
    Minimax_vs_AlphaBeta(4)
    #AlphaBeta_vs_Minimax(4)
    #Expectiminimax_vs_Minimax(4)
    #Minimax_self_play(3)
    #AlphaBeta_self_play(3)
    #Expectiminimax_self_play(3)
    #Gemini_self_play(3)


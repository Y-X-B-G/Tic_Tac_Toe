import time
import os
from tic_tac_toe import TicTacToe 
from minimax import MinimaxAI
from Gemini import GeminiAI

def Gemini_vs_Minimax():
    was_wrong = [-1,-1,-1]
    board_size = 3
    game = TicTacToe(board_size)

    ai = MinimaxAI(maximizing_player=-1) # AI plays as O. Since O is -1, we are truomg tp maximizE

    print("You are X. The AI is O.")
    print("Enter your moves as 'row,column' (0-2, 0-2)")

    while True:
        print("\n" + "="*20)
        print(game)

        winner = game.check_win()
        if winner is not None:
            if winner == 1:
                print("Game Over! GEMINI (X) win!")
            elif winner == -1:
                print("Game Over! MINIMAX_AI (O) wins!")
            else:
                print("Game Over! It's a Tie!")
            break 

        current_player = game.get_current_player()

        if current_player == 1:#gemini
            while True:
                print(game.get_board())
                move_input = GeminiAI(game.get_board(), was_wrong)
                print(move_input)
                r, c = map(int, move_input.split(','))
                if game.play(r, c) == 1:    
                    break #if valid. ,pve on
                else:
                    print("Invalid move. Cell occupied or out of bounds. Try again.")
                    was_wrong[0] = 1
                    was_wrong[1] = r
                    was_wrong[2] = c

        else: #AI turn
            best_move = ai.find_best_move(game)
            if best_move:
                game.play(best_move[0], best_move[1])
                print(f"AI (O) played at {best_move[0]},{best_move[1]}")
            else:
                print("AI has no valid moves left. This shouldn't happen before a tie/win.")
                GeminiAI(game.get_board())
                break

def Player_vs_Minimax():
    board_size = 3
    game = TicTacToe(board_size)

    ai = MinimaxAI(maximizing_player=-1) # AI plays as O. Since O is -1, we are truomg tp maximizE

    print("You are X. The AI is O.")
    print("Enter your moves as 'row,column' (0-2, 0-2)")

    while True:
        print("\n" + "="*20)
        print(game)

        winner = game.check_win()
        if winner is not None:
            if winner == 1:
                print("Game Over! You (X) win!")
            elif winner == -1:
                print("Game Over! AI (O) wins!")
            else:
                print("Game Over! It's a Tie!")
            break 

        current_player = game.get_current_player()

        if current_player == 1:#player turn 
            while True:
                move_input = input("Your turn (X). Enter row,column: ")
                r, c = map(int, move_input.split(','))
                if game.play(r, c) == 1:    
                    break 
                else:
                    print("Invalid move. Cell occupied or out of bounds. Try again.")

        else: #AI turn
            best_move = ai.find_best_move(game)
            if best_move:
                game.play(best_move[0], best_move[1])
                print(f"AI (O) played at {best_move[0]},{best_move[1]}")
            else:
                print("AI has no valid moves left. This shouldn't happen before a tie/win.")
                break # Should be caught by check_win earlier

def Minimax_vs_Minimax():
    board_size = 3                

Gemini_vs_Minimax()
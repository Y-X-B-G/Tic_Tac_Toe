import tkinter as tk
from tkinter import messagebox
from tic_tac_toe import TicTacToe
from minimax import MinimaxAI
from Gemini import GeminiAI

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("CP468 Tic Tac Toe")
        self.master.resizable(True, True)
        
        self.mode = tk.StringVar(value="Player vs Minimax")
        self.board_size = 3
        self.buttons = []
        self.game = None
        self.ai = MinimaxAI(maximizing_player=-1)

        self.create_menu()
        self.create_board()
        self.reset_game()

    def create_menu(self):
        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        tk.Label(frame, text="Game Mode:", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)

        modes = ["Player vs Minimax", "Minimax vs Gemini"]
        self.mode_dropdown = tk.OptionMenu(frame, self.mode, *modes, command=lambda _: self.reset_game())
        self.mode_dropdown.config(width=18, font=("Courier", 12))
        self.mode_dropdown.pack(side=tk.LEFT)

        tk.Button(frame, text="Restart", command=self.reset_game, font=("Courier", 12)).pack(side=tk.LEFT, padx=10)

    def create_board(self):
        board_frame = tk.Frame(self.master)
        board_frame.pack()

        self.buttons = []
        for r in range(self.board_size):
            row = []
            for c in range(self.board_size):
                btn = tk.Button(board_frame, text="", font=("Courier", 36, "bold"), width=3, height=1,
                command=lambda row=r, col=c: self.handle_click(row, col))
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

    def reset_game(self):
        self.game = TicTacToe(self.board_size)
        for r in range(self.board_size):
            for c in range(self.board_size):
                self.buttons[r][c]["text"] = ""
                self.buttons[r][c]["state"] = "normal"
        if self.mode.get() == "Minimax vs Gemini":
            self.master.after(1000, self.run_ai_vs_ai)

    def handle_click(self, r, c):
        if self.mode.get() != "Player vs Minimax":
            return
        if self.game.get_board()[r][c] != 0 or self.game.check_win() is not None:
            return

        self.game.play(r, c)
        self.update_button(r, c, 1)
        if self.check_game_over():
            return
        self.master.after(500, self.ai_move)

    def ai_move(self):
        move = self.ai.find_best_move(self.game)
        if move:
            r, c = move
            self.game.play(r, c)
            self.update_button(r, c, -1)
            self.check_game_over()

    def run_ai_vs_ai(self):
        winner = self.game.check_win()
        if winner is not None:
            self.check_game_over()
            return

        current = self.game.get_current_player()
        if current == 1:
            move = GeminiAI(self.game.get_board(), 0)
            try:
                r, c = map(int, move.strip().split(","))
                if self.game.get_board()[r][c] == 0:
                    self.game.play(r, c)
                    self.update_button(r, c, 1)
            except:
                print("Gemini AI made an invalid move:", move)
        else:
            move = self.ai.find_best_move(self.game)
            if move:
                r, c = move
                self.game.play(r, c)
                self.update_button(r, c, -1)

        self.master.after(1000, self.run_ai_vs_ai)

    def update_button(self, r, c, player):
        symbol = "X" if player == 1 else "O"
        color = "green" if player == 1 else "red"

        btn = self.buttons[r][c]
        btn.config(
            text=symbol,
            state="disabled",
            fg="white",                     
            bg=color,                               
            highlightbackground=color,      
            font=("Courier", 36, "bold")
    )

    def check_game_over(self):
        winner = self.game.check_win()
        if winner is not None:
            if winner == 1:
                msg = "X wins!" if self.mode.get() == "Player vs Minimax" else "Gemini AI (X) wins!"
            elif winner == -1:
                msg = "O wins!" if self.mode.get() == "Player vs Minimax" else "Minimax AI (O) wins!"
            else:
                msg = "It's a tie!"
            messagebox.showinfo("Game Over", msg)
            for row in self.buttons:
                for btn in row:
                    btn["state"] = "disabled"
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
from tic_tac_toe import TicTacToe
from minimax import MinimaxAI
from Gemini import GeminiAI
from alphabeta import AlphaBetaAI
from expectiminimax import ExpectiminimaxAI

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("CP468 Tic Tac Toe")
        self.master.resizable(True, True)

        self.mode = tk.StringVar(value="Player vs Minimax")
        self.size_var = tk.StringVar(value="3x3")
        self.board_size = int(self.size_var.get().split("x")[0])

        self.buttons = []
        self.board_frame = None
        self.game = None
        self.ai_X = None
        self.ai_O = None
        self.game_started = False
        self.previous_gemini_move = None
        self.after_id = None

        self.create_menu()
        self.create_board()
        self.reset_game()  # Called manually via Restart button, not on dropdown change

    def create_menu(self):
        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        tk.Label(frame, text="Game Mode:", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
        modes = [
            "Player vs Minimax",
            "Gemini vs Minimax",
            "Player vs Expectiminimax",
            "Gemini vs Expectiminimax",
            "Player vs AlphaBeta",
            "Gemini vs AlphaBeta"
        ]
        self.mode_dropdown = tk.OptionMenu(frame, self.mode, *modes, command=lambda _: self.notify_mode_change())
        self.mode_dropdown.config(width=28, font=("Courier", 12))
        self.mode_dropdown.pack(side=tk.LEFT)

        tk.Label(frame, text="Board Size:", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
        sizes = [f"{i}x{i}" for i in range(3, 7)]
        self.size_dropdown = tk.OptionMenu(frame, self.size_var, *sizes, command=lambda _: self.notify_restart_required())
        self.size_dropdown.config(width=6, font=("Courier", 12))
        self.size_dropdown.pack(side=tk.LEFT)

        tk.Button(frame, text="Restart", command=self.reset_game, font=("Courier", 12)).pack(side=tk.LEFT, padx=10)

    def create_board(self):
        if self.board_frame:
            self.board_frame.destroy()

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.buttons = []
        for r in range(self.board_size):
            row = []
            for c in range(self.board_size):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Courier", 36, "bold"),
                    width=3, height=1,
                    fg="black",
                    command=lambda row=r, col=c: self.handle_click(row, col)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def notify_mode_change(self):
        new_mode = self.mode.get()
        if new_mode != getattr(self, 'current_mode', None):
            messagebox.showinfo("Game Mode Changed", "Game mode changed. Please press Restart to apply the new mode.")

    def notify_restart_required(self):
        size_str = self.size_var.get()
        selected_size = int(size_str.split("x")[0])
        if selected_size != self.board_size:
            messagebox.showinfo("Board Size Changed", "Board size changed. Please press Restart to apply the new board.")

    def reset_game(self):
        size_str = self.size_var.get()
        self.board_size = int(size_str.split("x")[0])
        self.create_board()
        self.game = TicTacToe(self.board_size)

        self.current_mode = self.mode.get()
        self.ai_X = None
        self.ai_O = None
        self.game_started = False
        self.previous_gemini_move = None

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        if self.current_mode == "Player vs Minimax":
            self.ai_O = MinimaxAI(-1)
        elif self.current_mode == "Gemini vs Minimax":
            self.ai_X = GeminiAI
            self.ai_O = MinimaxAI(-1)
        elif self.current_mode == "Player vs Expectiminimax":
            self.ai_O = ExpectiminimaxAI(-1)
        elif self.current_mode == "Gemini vs Expectiminimax":
            self.ai_X = GeminiAI
            self.ai_O = ExpectiminimaxAI(-1)
        elif self.current_mode == "Player vs AlphaBeta":
            self.ai_O = AlphaBetaAI(-1)
        elif self.current_mode == "Gemini vs AlphaBeta":
            self.ai_X = GeminiAI
            self.ai_O = AlphaBetaAI(-1)

        self.hide_start_button()
        if "Gemini vs" in self.current_mode:
            self.show_start_button()
        else:
            self.game_started = True
            if self.ai_X or self.ai_O:
                self.after_id = self.master.after(1000, self.run_ai_vs_ai)

    def handle_click(self, r, c):
        if not self.game_started or self.game is None:
            return
        if self.game.get_board()[r][c] != 0 or self.game.check_win() is not None:
            return

        current_player = self.game.get_current_player()
        if current_player == 1 and self.ai_X is None:
            self.game.play(r, c)
            self.update_button(r, c, 1)
            if self.check_game_over():
                return
            self.master.after(500, self.ai_move)
        elif current_player == -1 and self.ai_O is None:
            self.game.play(r, c)
            self.update_button(r, c, -1)
            if self.check_game_over():
                return
            self.master.after(500, self.ai_move)

    def ai_move(self):
        if not self.game_started or self.game is None:
            return
        player = self.game.get_current_player()
        ai = self.ai_X if player == 1 else self.ai_O

        if isinstance(ai, (MinimaxAI, AlphaBetaAI, ExpectiminimaxAI)):
            move = ai.find_best_move(self.game)
        elif ai == GeminiAI:
            move = GeminiAI(self.game.get_board(), (0,))
            try:
                move = tuple(map(int, move.strip().split(",")))
            except:
                print("Invalid Gemini move:", move)
                return
        else:
            return

        if move:
            r, c = move
            if self.game.get_board()[r][c] == 0:
                self.game.play(r, c)
                self.previous_gemini_move = (r, c)
                self.update_button(r, c, player)
                self.check_game_over()

    def run_ai_vs_ai(self):
        if not self.game_started or self.game is None or self.game.check_win() is not None:
            self.game_started = False
            self.check_game_over()
            return

        player = self.game.get_current_player()
        ai = self.ai_X if player == 1 else self.ai_O
        board = self.game.get_board()
        board_size = self.board_size
        wrong = (0,)
        move = None
        retries = 0
        max_retries = 40

        while retries < max_retries:
            if isinstance(ai, (MinimaxAI, AlphaBetaAI, ExpectiminimaxAI)):
                move = ai.find_best_move(self.game)
                break
            elif ai == GeminiAI:
                if len(board) != self.board_size or len(board[0]) != self.board_size:
                    print(f"WARNING: Gemini received mismatched board size: {len(board)}x{len(board[0])} expected {self.board_size}x{self.board_size}")
                gemini_output = GeminiAI(board, wrong)
                try:
                    r, c = map(int, gemini_output.strip().split(","))
                    if not (0 <= r < board_size and 0 <= c < board_size):
                        raise ValueError("Out of bounds")
                    if board[r][c] != 0:
                        # Subtle glow for Gemini's invalid move attempt
                        btn = self.buttons[r][c]
                        original_bg = btn.cget("bg")
                        btn.config(bg="orange")
                        self.master.after(300, lambda b=btn, bg=original_bg: b.config(bg=bg))
                        raise ValueError("Cell already taken")
                    if board[r][c] == 0:
                        move = (r, c)
                        self.previous_gemini_move = (r, c)
                        break
                    else:
                        raise ValueError("Cell already taken")
                except Exception as e:
                    print(f"Gemini invalid move: {e}")
                    wrong = (1,) + self.previous_gemini_move if self.previous_gemini_move else (0,)
                    retries += 1
                    continue
            else:
                return

        if move is None:
            print("Gemini failed to produce a valid move after 5 attempts.")
            self.game_started = False
            messagebox.showerror("Gemini Error", "Gemini could not produce a valid move. Match has been stopped.")
            return

        if move:
            r, c = move
            if self.game.get_board()[r][c] == 0:
                self.game.play(r, c)
                self.update_button(r, c, player)

        self.after_id = self.master.after(1000, self.run_ai_vs_ai)

    def update_button(self, r, c, player):
        symbol = "X" if player == 1 else "O"
        color = "green" if player == 1 else "red"

        btn = self.buttons[r][c]
        btn.config(
            text=symbol,
            state="disabled",
            fg="black",
            bg=color,
            highlightbackground=color,
            font=("Courier", 36, "bold")
        )

    def check_game_over(self):
        if self.game is None:
            return False
        winner = self.game.check_win()
        if winner is not None:
            if winner == 1:
                msg = "X wins!" if self.ai_X is None else "Gemini (X) wins!"
            elif winner == -1:
                msg = "O wins!" if self.ai_O is None else "AI (O) wins!"
            else:
                msg = "It's a tie!"
            messagebox.showinfo("Game Over", msg)
            for row in self.buttons:
                for btn in row:
                    btn["state"] = "disabled"
            return True
        return False

    def show_start_button(self):
        if not hasattr(self, 'start_button') or not self.start_button:
            self.start_button = tk.Button(self.master, text="Start Match", font=("Courier", 12),
                                          command=self.start_gemini_match)
        self.start_button.pack(pady=10)

    def hide_start_button(self):
        if hasattr(self, 'start_button'):
            self.start_button.pack_forget()

    def start_gemini_match(self):
        self.game_started = True
        self.after_id = self.master.after(1000, self.run_ai_vs_ai)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

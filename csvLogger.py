import csv

class CSVLogger:
    def __init__(self, filename):
        """
        Initializes the CSV logger and creates a new CSV file.
        
        @params 
            filename: str - The name of the CSV file to write logs to.
        @returns
            None
        """
        self.filename = filename
        self.file = open(self.filename, mode='w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            'GameID',
            'BoardSize',
            'PlayerX',
            'PlayerX_Runtime',
            'PlayerO',
            'PlayerO_Runtime'
            'Winner',
            'NumTurns',
            'TotalRunTimeSec'
        ])
        self.game_id = 1

    def log_game(self, board_size, player_x, playerx_runtime, player_o, playero_runtime, winner, num_turns, runtime_sec):
        """
        Logs a single game's details into the CSV file.

        @params
            board_size: int - The size of the Tic Tac Toe board (e.g., 3 for a 3x3 board).
            player_x: str - The name or type of the X player.
            playerx_runtime: float - Runtime (in seconds) for Player X's turns.
            player_o: str - The name or type of the O player.
            playero_runtime: float - Runtime (in seconds) for Player O's turns.
            winner: str|int - The winner of the game (e.g., 'X', 'O', or 'Draw').
            num_turns: int - Total number of turns played in the game.
            runtime_sec: float - Total runtime of the game in seconds.
        @returns
            None
        """
        self.writer.writerow([
            self.game_id,
            f"{board_size}x{board_size}",
            player_x,
            f"{abs(playerx_runtime):.6f}",
            player_o,
            f"{abs(playero_runtime): .6f}",
            winner,
            num_turns,
            f"{runtime_sec:.6f}"
        ])
        self.game_id += 1

    def close(self):
        """
        Closes the CSV file.

        @params
            None
        @returns
            None
        """
        self.file.close()

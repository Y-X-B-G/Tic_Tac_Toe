import csv

class CSVLogger:
    def __init__(self, filename):
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
        self.file.close()

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
            'PlayerO',
            'Winner',
            'NumTurns',
            'TotalRunTimeSec'
        ])
        self.game_id = 1

    def log_game(self, board_size, player_x, player_o, winner, num_turns, runtime_sec):
        self.writer.writerow([
            self.game_id,
            f"{board_size}x{board_size}",
            player_x,
            player_o,
            winner,
            num_turns,
            f"{runtime_sec:.6f}"
        ])
        self.game_id += 1

    def close(self):
        self.file.close()

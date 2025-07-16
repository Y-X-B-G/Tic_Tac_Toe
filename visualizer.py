"""
This file contains the code used to visualize the data from the AI game results CSV file
"""
#Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class dataVisualizer:

    def __init__(self, csv_file: str, board_size=None, player_name=None):
        # Load CSV
        self.data_frame = pd.read_csv(csv_file)

        # Strip column names
        self.data_frame.columns = self.data_frame.columns.str.strip()

        # Strip text columns to avoid whitespace errors
        for col in ["Winner", "PlayerX", "PlayerO"]:
            if col in self.data_frame.columns:
                self.data_frame[col] = self.data_frame[col].astype(str).str.strip()

        # Convert numeric
        if "TotalRunTimeSec" in self.data_frame.columns:
            self.data_frame["TotalRunTimeSec"] = pd.to_numeric(
                self.data_frame["TotalRunTimeSec"],
                errors="coerce"
            )

        # Create WinnerAI column
        if all(col in self.data_frame.columns for col in ["Winner", "PlayerX", "PlayerO"]):
            self._generate_winner_col()
        else:
            print("Missing columns for generating WinnerAI!")




    
    def _generate_winner_col(self):
        #loop over every column and find who the winner is
        #Faster with numpy vectorized if
        self.data_frame["WinnerAI"] = np.where(self.data_frame["Winner"] == "X", self.data_frame["PlayerX"],
                                               np.where(self.data_frame["Winner"]=="O", self.data_frame["PlayerO"], "Draw")
                                               )
        return 

    def _calculate_win_rates(self):
        #Want to group things by board size, winner AI and then get the count of games in that group
       grouped_data = self.data_frame.groupby(["BoardSize","WinnerAI"]).size().reset_index(name= "Count")
       #find total games per board size
       num_games = grouped_data.groupby(["BoardSize"]).sum().reset_index()
       num_games = num_games.rename(columns={"Count": "TotalGames"})
       result = pd.merge(grouped_data,num_games, on="BoardSize")
       result["WinPercentage"]= (result["Count"]/result["TotalGames"]) * 100
       return result
    
    #This does not work
    """def plot_win_rates(self, save_path=None):
        result = self._calculate_win_rates()

        # Pivot the data for grouped bar plotting
        pivot_df = result.pivot_table(
            index="BoardSize",
            columns="WinnerAI",
            values="WinPercentage",
            fill_value=0
        )

        board_sizes = pivot_df.index.tolist()
        winner_ais = pivot_df.columns.tolist()
        x = np.arange(len(board_sizes))
        bar_width = 0.15

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, ai in enumerate(winner_ais):
            offsets = x + i * bar_width
            ax.bar(
                offsets,
                pivot_df[ai].to_numpy(),
                width=bar_width,
                label=ai
            )

        ax.set_title("Win Rates per AI by Board Size")
        ax.set_xlabel("Board Size")
        ax.set_ylabel("Win Percentage (%)")
        ax.set_xticks(x + (bar_width * (len(winner_ais)-1) / 2))
        ax.set_xticklabels(board_sizes)
        ax.legend(title="Winner AI")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()"""
    
    def plot_avg_runtime(self, save_path=None):
        # Group and compute average runtime
        avg_runtime = (
            self.data_frame
            .groupby(["BoardSize", "PlayerX"])["TotalRunTimeSec"]
            .mean()
            .reset_index(name="AvgRunTimeSec")
        )

        pivot_df = avg_runtime.pivot_table(
            index="BoardSize",
            columns="PlayerX",
            values="AvgRunTimeSec",
            fill_value=0
        )

        board_sizes = pivot_df.index.tolist()
        ais = pivot_df.columns.tolist()
        x = np.arange(len(board_sizes))
        bar_width = 0.15

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, ai in enumerate(ais):
            offsets = x + i * bar_width
            ax.bar(
                offsets,
                pivot_df[ai].to_numpy(),
                width=bar_width,
                label=ai
            )

        ax.set_title("Average Runtime per AI by Board Size")
        ax.set_xlabel("Board Size")
        ax.set_ylabel("Average Runtime (sec)")
        ax.set_xticks(x + (bar_width * (len(ais)-1) / 2))
        ax.set_xticklabels(board_sizes)
        ax.legend(title="AI")
        plt.tight_layout()

        if save_path:
            fig.savefig(save_path)
            plt.close(fig)
        else:
            plt.show()

    def plot_time_trend(self, save_path=None):
        fig, ax = plt.subplots(figsize=(10, 6))

        x_vals = self.data_frame["GameID"]
        y_vals = self.data_frame["TotalRunTimeSec"]

        # Plot original runtime values
        ax.plot(
            x_vals,
            y_vals,
            marker='o',
            linestyle='-',
            color='',
            markersize=5,
            linewidth=2,
            label='Runtime'
        )

        # Create a smoothed rolling average
        smoothed_y = y_vals.rolling(window=5, min_periods=1).mean()

        # Plot smoothed trend line
        ax.plot(
            x_vals,
            smoothed_y,
            linestyle='--',
            color='red',
            linewidth=2,
            label='Smoothed Trend'
        )

        ax.set_title("Runtime Trend Over Games")
        ax.set_xlabel("Game ID")
        ax.set_ylabel("Total Runtime (sec)")
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
        ax.legend()
        plt.tight_layout()

        if save_path:
            fig.savefig(save_path)
            plt.close(fig)
        else:
            plt.show()
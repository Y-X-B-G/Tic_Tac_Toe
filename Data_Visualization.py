from visualizer import dataVisualizer

vis = dataVisualizer("ai_game_results.csv")
vis.plot_avg_runtime()
vis.plot_time_trend()
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = 'gemini-2.0-flash-lite'


def GeminiAI(current_board, wrong):
    model = genai.GenerativeModel(MODEL_NAME)
    

    if wrong ==1:
        prompt = f"""You are playing Tic Tac Toe and You are 1 (Enemy is -1). Each section is set by row,column, so for example, 0,0 will be top left, 2,0 will be bottom left, 0,2 would be top right, and 0,0 would be bottom right.
        Your last input was {wrong[1]},{wrong[2]} which you cannot play as there is already a 1 or -1 there. Make sure you choose a row and column with no 1 or -1.
        This is the current board: {current_board}. The first row is the first list, second row is second list, third row is third list. Choose the best choice so that you can win the game. Make sure your response is ONLY formatted as row,column and nothing else.
        If you see that the opponent can win if they place a -1 somewhere, make sure you put a 1 there so you cannot win even if it means that you wont win either. For example, look out for [[-1, 0, 0], [0,0,0], [-1,0,0]] as if they play 0,1, they win.
        For example, if you want want it in the middle, your only response should be 1,1."""
    else:
    #prompt created by gemini as original wasnt working well
        prompt = f"""You are playing Tic Tac Toe and You are 1 (Enemy is -1). Each section is set by row,column, so for example, 0,0 will be top left, 2,0 will be bottom left, 0,2 would be top right, and 0,0 would be bottom right.
        This is the current board: {current_board}. The first row is the first list, second row is second list, third row is third list. Choose the best choice so that you can win the game. Make sure your response is ONLY formatted as row,column and nothing else.
        If you see that the opponent can win if they place a -1 somewhere, make sure you put a 1 there so you cannot win even if it means that you wont win either. For example, look out for [[-1, 0, 0], [0,0,0], [-1,0,0]] as if they play 0,1, they win.
        For example, if you want want it in the middle, your only response should be 1,1."""
    response = model.generate_content(prompt)
        
    return response.text.strip() 



import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = 'gemini-2.0-flash-lite'
def GeminiAI(current_board, wrong):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    game_string = "\n".join(
         f"Row {i}: " + " ".join(str(x) for x in row)
        for i, row in enumerate(current_board)
    )

    if isinstance(wrong, (list, tuple)) and len(wrong) > 0 and wrong[0] == 1:
        prompt = f"""You are playing Tic Tac Toe as player 1 (X). Your opponent is player -1 (O). It is your turn now.

        Your last move was at {wrong[1]},{wrong[2]}, which was invalid because that cell is already occupied, you must chance your approch. DO NOT GIVE THE SAME ANSWER ONCE NOTIFIED THAT IT IS INCORRECT.
        A cell is occupied if it has a value of 1 (X) or -1 (O). An empty cell has a value of 0.
        Pay close attention to the board, since the board size is dynamically changed.

        The current board is:
        {game_string}

        The board has {len(current_board)} rows and {len(current_board[0])} columns.


        Your objective is to maximize your chances of winning. If your opponent can win on their next move, you must block them even if it means you might not win.
        Your goal is to win as quickly as possible. 
        Check if you have a winning move this turn and play it. If not, block your opponent if they can win on their next move. 
        Otherwise, pick the move that gives you the best chance to win in future turns.
        Choose a valid, unoccupied cell for your next move. Respond ONLY with a single line in this format:
        row,column
        For example: 1,1"""
    else:
    #prompt created by gemini as original wasnt working well
        prompt = f"""You are playing Tic Tac Toe as player 1 (X). Your opponent is player -1 (O). It is your turn now.
         A cell is occupied if it has a value of 1 (X) or -1 (O). An empty cell has a value of 0.
          Your objective is to maximize your chances of winning. If your opponent can win on their next move, you must block them even if it means you might not win. 
          Pay close attention to the board, since the board size is dynamically changed.
          Here is the current game board:
          {game_string}

        The board has {len(current_board)} rows and {len(current_board[0])} columns.


        Your objective is to maximize your chances of winning. If your opponent can win on their next move, you must block them even if it means you might not win.
    
        Your goal is to win as quickly as possible. 
        Check if you have a winning move this turn and play it. If not, block your opponent if they can win on their next move. 
        Otherwise, pick the move that gives you the best chance to win in future turns.

        Respond only with the coordinates of your chosen move, in this format:
          row,column
          For example: 1,1"""
    response = model.generate_content(prompt)
        
    return response.text.strip()

def parse_gemini_response(response,board_size):
    """
    Parses Gemini's text response into a move tuple (row,col)
    Returns None if parsing fails
    """
    try: 
        #find frist line that looks like digits
        lines  = response.split("\n")
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 2:
                r,c = int(parts[0]), int(parts[1])
                if 0 <= r < board_size and 0 <= c < board_size:
                    return (r,c)
    except Exception: 
        pass

    return None



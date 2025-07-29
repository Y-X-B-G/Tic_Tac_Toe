import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = 'gemini-2.0-flash-lite'
def GeminiAI(current_board, wrong, num_retries = 10):
    """
        Generates the next move for the Gemini AI based on the board state.
        
        @params
        current_board: List[List[int]] - The current state of the Tic Tac Toe board (1 = X, -1 = O, 0 = empty).
        wrong: tuple - Information about a previous invalid move or error (used for feedback/correction).
        num_retries: int (default = 10) - Maximum number of attempts to generate a valid move.

        @returns
        str - The chosen move in the format "row,column".
    """
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    game_string = "\n".join(
         f"Row {i}: " + " ".join(str(x) for x in row)
        for i, row in enumerate(current_board)
    )
    flat_board = [cell for row in current_board for cell in row]
    if isinstance(wrong, (list, tuple)) and len(wrong) > 0 and wrong[0] == 1:
        
        if flat_board.count(0) == 1:
            prompt = f"""
            You are playing Tic Tac Toe as player 1 (X). The board has only one empty cell left.

            Just return the coordinates of that one empty cell in this exact format:
            row,column

            Do not explain or add any other text. Here is the board:
                {game_string}
                """
        else:
            prompt = f"""You are playing Tic Tac Toe as player 1 (X). Your opponent is player -1 (O). It is your turn now.

            Your last move was at {wrong[1]},{wrong[2]}, which was invalid because that cell is already occupied (has a value other than 0), DO NOT GIVE THE SAME ANSWER ONCE NOTIFIED THAT IT IS INCORRECT.
            
            A cell is occupied if it has a value of 1 (X) or -1 (O). An empty cell has a value of 0.
            Pay close attention to the board, since the board size is dynamically changed.
            In the event you recieve an emptu board, you are going first. 
            The current board is:
            {game_string}

            The board has {len(current_board)} rows and {len(current_board[0])} columns.

            Come up with a new answer after closely studying the board and ONLY select a location where the value is 0 it is not occupied.
            Your objective is to maximize your chances of winning. If your opponent can win on their next move, you must block them even if it means you might not win.
            Your goal is to win as quickly as possible. 
            Check if you have a winning move this turn and play it. If not, generate possible moves using an alpha beta AI algorithm to get your opponents next move and block your opponent if they can win on their next move. 
            Otherwise, pick the move that gives you the best chance to win in future turns.
            Choose a valid, unoccupied cell for your next move. Respond ONLY with a single line in this format:
            row,column
            For example: 1,1"""
    else:
        if flat_board.count(0) == 1:
            prompt = f"""
            You are playing Tic Tac Toe as player 1 (X). The board has only one empty cell left.

            Just return the coordinates of that one empty cell in this exact format:
            row,column

            Do not explain or add any other text. Here is the board:
            {game_string}
            """
        else:
    #prompt created by gemini as original wasnt working well
            prompt = f"""You are playing Tic Tac Toe as player 1 (X). Your opponent is player -1 (O). It is your turn now.
            A cell is occupied if it has a value of 1 (X) or -1 (O). An empty cell has a value of 0.
            In the event you recieve an emptu board, you are going first. 
            Your objective is to maximize your chances of winning. If your opponent can win on their next move, you must block them even if it means you might not win. 
            Pay close attention to the board, since the board size is dynamically changed.
            Here is the current game board:
            {game_string}

            The board has {len(current_board)} rows and {len(current_board[0])} columns.


            Your objective is to maximize your chances of winning. If your opponent can win on their next move, you must block them even if it means you might not win.
            Use the AlphaBeta AI algortitm to check which moves your opponent can make.
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



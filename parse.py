import chess.pgn
from object import Game,Color,Output

def parse_chess_games(file_path: str, player_name:str) -> list[Game]:
    games_data = []
    
    with open(file_path, encoding="utf-8") as pgn_file:
        while True:
            # Read games one by one from the file
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
                
            headers = game.headers
            white = headers.get("White")
            black = headers.get("Black")
            result = headers.get("Result")
            
            # Determine your color and the relative result
            if white == player_name:
                user_color = Color.WHITE
                if result == "1-0":
                    user_outcome = Output.WIN
                elif result == "0-1":
                    user_outcome = Output.LOSE
                else:
                    user_outcome = Output.DRAW
            elif black == player_name:
                user_color = Color.BLACK
                if result == "0-1":
                    user_outcome = Output.WIN
                elif result == "1-0":
                    user_outcome = Output.LOSE
                else:
                    user_outcome = Output.DRAW
            else:
                # Skip games where you are not playing
                continue

            # Extract the moves in Standard Algebraic Notation (SAN)
            moves = [move for move in game.mainline_moves()]
            
            games_data.append(Game(user_color,user_outcome,moves))
            
    return games_data

if __name__ == "__main__":
    my_username = "Bfx-de-Blr"
    parsed_games = parse_chess_games("lichess_games.pgn", my_username)

    print(f"Successfully parsed {len(parsed_games)} games for {my_username}.")
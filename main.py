from parse import parse_chess_games
from tree import print_tree,build_opening_tree


if __name__ == "__main__":
    my_username = "Bfx-de-Blr"
    parsed_games = parse_chess_games("lichess_games.pgn", my_username)
    print("Games parsed")
    tree = build_opening_tree(parsed_games, max_depth=6)
    print_tree(tree, max_display_depth=4)

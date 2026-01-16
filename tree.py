import chess
from object import Output,Game,Color
from tqdm import tqdm

class OpeningNode:
    def __init__(self, move_san: str = "Root"):
        self.move_san = move_san
        self.stats = {Output.WIN: 0, Output.LOSE: 0, Output.DRAW: 0}
        self.children: dict[str, 'OpeningNode'] = {}

    def add_game_result(self, outcome: Output):
        self.stats[outcome] += 1

    def get_total(self):
        return sum(self.stats.values())

    def get_percentages(self):
        total = self.get_total()
        if total == 0:
            return 0, 0, 0
        return (
            (self.stats[Output.WIN] / total) * 100,
            (self.stats[Output.DRAW] / total) * 100,
            (self.stats[Output.LOSE] / total) * 100
        )

def build_opening_tree(games: list[Game], max_depth: int):
    # Root node represents the start of any game
    root = OpeningNode()
    # First level branches: White or Black
    root.children["White"] = OpeningNode("White")
    root.children["Black"] = OpeningNode("Black")

    for game in games:
        # Navigate to the correct starting branch (White or Black)
        try:
            current_node = root.children[game.color.value]
            current_node.add_game_result(game.output)
            
            board = chess.Board()
            # Process moves up to the desired depth
            for i, move in enumerate(game.moves):
                if i >= max_depth:
                    break
                
                # Convert Move object to SAN (e.g., "e4", "Nf6")
                move_san = board.san(move)
                board.push(move)
                
                if move_san not in current_node.children:
                    current_node.children[move_san] = OpeningNode(move_san)
                
                current_node = current_node.children[move_san]
                current_node.add_game_result(game.output)
        except Exception as e:
            print(f"{game.color} {game.output} {game.moves}")
            
    return root

def print_tree(node: OpeningNode, depth: int = 0, max_display_depth: int = 3):
    if depth > max_display_depth:
        return

    indent = "  " * depth
    w, d, l = node.get_percentages()
    total = node.get_total()
    
    if depth > 0: # Don't print stats for the hidden Root
        print(f"{indent} {node.move_san} | {total} games | W: {w:.1f}% D: {d:.1f}% L: {l:.1f}%")

    # Sort children by number of games played to see popular openings first
    sorted_children = sorted(node.children.values(), key=lambda x: x.get_total(), reverse=True)
    
    for child in sorted_children:
        print_tree(child, depth + 1, max_display_depth)

if __name__ == "__main__":
    parsed_games = [Game(Color.WHITE,Output.WIN,[])]
    tree = build_opening_tree(parsed_games, max_depth=6)
    print_tree(tree, max_display_depth=4)
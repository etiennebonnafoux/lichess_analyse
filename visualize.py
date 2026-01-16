import chess.pgn
import chess
from dataclasses import dataclass
from enum import Enum
import plotly.graph_objects as go
from object import Game,Output
from parse import parse_chess_games

def create_sankey_chart(games: list[Game], max_depth: int = 5, min_games: int = 1):
    nodes = ["Start"]
    path_to_idx = {("Start",): 0}
    stats = {} # (source_idx, target_idx) -> {WIN: count, ...}

    for game in games:
        try:
            board = chess.Board()
            # Initial step: Start -> Color
            current_path = ("Start",)
            next_path = ("Start", game.color.value)
            
            for step in range(max_depth + 1):
                if next_path not in path_to_idx:
                    path_to_idx[next_path] = len(nodes)
                    nodes.append(next_path[-1])
                
                # Record transition
                link = (path_to_idx[current_path], path_to_idx[next_path])
                if link not in stats: stats[link] = {Output.WIN:0, Output.DRAW:0, Output.LOSE:0}
                stats[link][game.output] += 1
                
                # Prepare next move
                if step >= len(game.moves) or step >= max_depth: break
                
                current_path = next_path
                move_san = board.san(game.moves[step])
                board.push(game.moves[step])
                
                # Prefix with move number for clarity (e.g. "1. e4" or "1... e5")
                move_num = (step // 2) + 1
                prefix = f"{move_num}." if step % 2 == 0 else f"{move_num}..."
                next_path = current_path + (f"{prefix} {move_san}",)
        except Exception as e:
            pass
    # Prepare Plotly lists
    sources, targets, values, labels, colors = [], [], [], [], []

    for (src, tgt), s in stats.items():
        total = sum(s.values())
        if total < min_games: continue
        
        win_p, lose_p = (s[Output.WIN]/total)*100, (s[Output.LOSE]/total)*100
        sources.append(src)
        targets.append(tgt)
        values.append(total)
        labels.append(f"Win: {win_p:.1f}% | Loss: {lose_p:.1f}% ({total} games)")
        
        # Color coding: Green for success, Red for failure
        if win_p > 55: colors.append("rgba(46, 204, 113, 0.5)")
        elif lose_p > 55: colors.append("rgba(231, 76, 60, 0.5)")
        else: colors.append("rgba(189, 195, 199, 0.5)")

    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=nodes),
        link=dict(source=sources, target=targets, value=values, label=labels, color=colors)
    )])
    
    fig.update_layout(title_text="Chess Opening Flow: Which lines should I study?", font_size=12)
    fig.write_html("chess_opening_analysis.html")
    print("Success! Open 'chess_opening_analysis.html' in your browser.")

# --- Execution ---
if __name__ == "__main__":
    my_games = parse_chess_games("lichess_games.pgn", "Bfx-de-Blr")
    create_sankey_chart(my_games, max_depth=6, min_games=2)
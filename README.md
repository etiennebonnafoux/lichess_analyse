# Lichess Game Analyser

The aim of this project is to know which opening to study based on the games played on Lichess.
The dataflow is as follow :
- Download of the games
- Parsing of the PGN format
- Creation of a opening tree with win/draw/lose pourcentage at each node
- Visualisation of the results

## Installation

This project follow [PEP-621](https://peps.python.org/pep-0621/) and can be bootstrapped by `uv` for example as easily as 
```bash
uv sync
```

## Entrypoint

You should first download the PNG in the folder `data` and then launch `uv run src/visualize.py` or `uv run src/main.py`
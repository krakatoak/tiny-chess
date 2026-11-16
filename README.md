# Tiny Chess (4 KB)

A compact chess engine in under 4,096 bytes of Python (3.13, stdlib only). Plays the make.fun tiny-chess-01 gauntlet via `MAKEFUN_ENV_URL`: negamax alpha-beta search (depth 3) with material + mirrored piece-square evaluation and a node budget.

Run: `MAKEFUN_ENV_URL=<url> python3 main.py`

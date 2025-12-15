import chess
import chess.pgn
import time
import datetime
from engine import RandomEngine, MinimaxEngine


def play_match(white_engine, black_engine):
    """
    Runs a game and returns the PGN string.
    """
    # 1. Setup Board and PGN Object
    board = chess.Board()
    pgn = chess.pgn.Game()

    # 2. Set Headers
    pgn.headers["Event"] = "Engine Arena Match"
    pgn.headers["Site"] = "Local"
    pgn.headers["Date"] = datetime.date.today().strftime("%Y.%m.%d")
    pgn.headers["White"] = white_engine.__class__.__name__
    pgn.headers["Black"] = black_engine.__class__.__name__

    # We need a 'node' variable to track where we are in the PGN tree
    node = pgn

    # 3. Game Loop
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move = white_engine.get_best_move(board)
        else:
            move = black_engine.get_best_move(board)

        if move in board.legal_moves:
            board.push(move)

            # Add move to PGN
            node = node.add_variation(move)

            # Optional: Print live moves to console for viewing
            # print(f"{board.fullmove_number}. {move.uci()}")
        else:
            print(f"Illegal move attempted: {move}")
            break

    # 4. Finalize
    pgn.headers["Result"] = board.result()
    # 5. Output PGN
    print(pgn)

    # Optional: Save to file
    with open("game.pgn", "w") as f:
        print(pgn, file=f)


if __name__ == "__main__":
    # Setup engines
    player1 = RandomEngine(depth=2)
    player2 = MinimaxEngine(depth=4)

    play_match(player1, player2)

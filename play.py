#!/usr/bin/env python3
import chess
import random
import argparse
import time

from game import RandomEngine 


def print_unicode_board(board, perspective=chess.WHITE):
    """Prints the position from a given perspective with nice colors."""
    sc, ec = "\x1b[0;30;107m", "\x1b[0m"
    for r in range(8) if perspective == chess.BLACK else range(7, -1, -1):
        line = [f"{sc} {r+1}"]
        for c in range(8) if perspective == chess.WHITE else range(7, -1, -1):
            # Chess board coloring logic
            color = "\x1b[48;5;255m" if (r + c) % 2 == 1 else "\x1b[48;5;253m"
            
            # Highlight last move
            if board.move_stack:
                last_move = board.move_stack[-1]
                if last_move.to_square == 8 * r + c or last_move.from_square == 8 * r + c:
                    color = "\x1b[48;5;153m"
            
            piece = board.piece_at(8 * r + c)
            symbol = chess.UNICODE_PIECE_SYMBOLS[piece.symbol()] if piece else " "
            line.append(color + symbol)
            
        print(" " + " ".join(line) + f" {sc} {ec}")
    
    if perspective == chess.WHITE:
        print(f" {sc}   a b c d e f g h  {ec}\n")
    else:
        print(f" {sc}   h g f e d c b a  {ec}\n")

def get_user_move(board):
    """Handles user input, validating SAN (e.g., Nf3) and UCI (e.g., g1f3)."""
    move = None
    while move is None:
        # Show a random example of a valid move to help the user
        valid_moves = list(board.legal_moves)
        if not valid_moves: return None # Checkmate/Stalemate
        
        example_san = board.san(random.choice(valid_moves))
        
        uci_input = input(f"Your move (e.g. {example_san}): ").strip()
        
        if uci_input.lower() in ("quit", "exit"):
            return "quit"

        # Try to parse as SAN (e.g. "Nf3") then UCI (e.g. "g1f3")
        try:
            move = board.parse_san(uci_input)
        except ValueError:
            try:
                move = chess.Move.from_uci(uci_input)
            except ValueError:
                print("Invalid format. Try again.")
                continue

        if move not in board.legal_moves:
            print("Illegal move. Try again.")
            move = None

    return move

def get_user_color():
    """Asks the user to play White or Black."""
    while True:
        color = input("Play as (w)hite or (b)lack? ").lower()
        if color in ('w', 'white'): return chess.WHITE
        if color in ('b', 'black'): return chess.BLACK


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-fen", help="Start from specific FEN", default=chess.STARTING_FEN)
    parser.add_argument("-depth", type=int, help="Search depth", default=2)
    parser.add_argument("-engine", choices=['random', 'minimax'], default='minimax', help="Choose engine type")
    args = parser.parse_args()

    # 1. Initialize Board
    board = chess.Board(args.fen)
    user_color = get_user_color()

    # 2. Initialize Engine
    print(f"\nInitializing {args.engine.title()} Engine with depth {args.depth}...")
    engine = RandomEngine()

    # 3. Game Loop
    while not board.is_game_over():
        print_unicode_board(board, perspective=user_color)

        if board.turn == user_color:
            # --- HUMAN TURN ---
            move = get_user_move(board)
            if move == "quit":
                break
            board.push(move)
        else:
            # --- AI TURN ---
            print("\nThinking...")
            start_time = time.time()
            
            # This calls your class directly!
            best_move = engine.get_best_move(board) 
            
            elapsed = time.time() - start_time
            print(f"Engine played: {board.san(best_move)} ({elapsed:.2f}s)")
            board.push(best_move)

    # 4. End Game
    print_unicode_board(board, perspective=user_color)
    print("Game Over:", board.result())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame aborted.")

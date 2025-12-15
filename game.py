import chess
import random

def search(board: chess.Board):
    print(board.legal_moves)

board = chess.Board()

search(board)

class Engine:
    def get_best_move(self, board: chess.Board) -> chess.Move:
        """The main method the game loop calls."""
        raise NotImplementedError("Subclasses must implement this method")

class RandomEngine(Engine):
    def get_best_move(self, board: chess.Board) -> chess.Move:
        moves = list(board.legal_moves) 

        return random.choice(moves)

def play_game():
    # 1. Setup
    board = chess.Board()
    
    # Initialize your specific engine here
    ai_engine = RandomEngine() 
    
    # 2. Game Loop
    while not board.is_game_over():
        print(board)
        
        if board.turn == chess.WHITE:
            move_uci = input("Enter your move (e.g., e2e4): ")
            try:
                move = chess.Move.from_uci(move_uci)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move, try again.")
            except ValueError:
                print("Invalid format.")
                
        else:
            print("AI is thinking...")
            best_move = ai_engine.get_best_move(board)
            board.push(best_move)
            print(f"AI played: {best_move}")
            
    print("Game Over:", board.result())

if __name__ == "__main__":
    play_game()

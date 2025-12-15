import chess
import random
from evaluator import Evaluator

class Engine:
    def __init__(self, depth: int) -> None:
        self.depth = depth

    def get_best_move(self, board: chess.Board) -> chess.Move | None:
        raise NotImplementedError("Subclasses must implement this method")

class RandomEngine(Engine):
    def __init__(self, depth: int) -> None:
        super().__init__(depth)

    def get_best_move(self, board: chess.Board) -> chess.Move | None:
        moves = list(board.legal_moves)
        if not moves:
            return None
        return random.choice(moves)

class MinimaxEngine(Engine):
    def __init__(self, depth):
        super().__init__(depth)
        self.evaluator = Evaluator()

    def get_best_move(self, board: chess.Board) -> chess.Move | None:
        if board.turn == chess.WHITE:
            _, move = self.max_value(board, self.depth, -float("inf"), float("inf"))
        else:
            _, move = self.min_value(board, self.depth, -float("inf"), float("inf"))
        return move

    def order_moves(self, board: chess.Board):
        moves = list(board.legal_moves)
        random.shuffle(moves)
        moves.sort(key=lambda m: (board.is_capture(m), m.promotion is not None), reverse=True)
        return moves

    def max_value(self, board: chess.Board, depth: int, alpha: float, beta: float) -> tuple[float, chess.Move | None]:
        if depth == 0 or board.is_game_over():
            return self.utility(board, depth), None

        val, best_move = -float("inf"), None

        for move in self.order_moves(board):
            board.push(move)
            v, _ = self.min_value(board, depth - 1, alpha, beta)
            board.pop()
            
            if v > val:
                val, best_move = v, move
                alpha = max(alpha, v)
            
            if val >= beta:
                return val, best_move

        return val, best_move

    def min_value(self, board: chess.Board, depth: int, alpha: float, beta: float) -> tuple[float, chess.Move | None]:
        if depth == 0 or board.is_game_over():
            return self.utility(board, depth), None

        val, best_move = float("inf"), None

        for move in self.order_moves(board):
            board.push(move)
            v, _ = self.max_value(board, depth - 1, alpha, beta)
            board.pop()
            
            if v < val:
                val, best_move = v, move
                beta = min(beta, val)
            
            if val <= alpha:
                return val, best_move

        return val, best_move

    def utility(self, board: chess.Board, depth: int) -> float:
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -20000 - depth
            else:
                return 20000 + depth
                
        return self.evaluator.evaluate(board)
import chess
import chess.pgn
import io
import os

def is_fen_string(s: str) -> bool:
    """
    Heuristic check for FEN: should have 6 fields separated by spaces.
    """
    parts = s.strip().split()
    if len(parts) != 6:
        return False
    # first part should contain ranks with '/' characters
    return "/" in parts[0]

def parse_fen(fen_string):
    try:
        board = chess.Board(fen_string)
        return {
            'initial_fen': fen_string,
            'moves': [],
            'moves_san': [],
            'position': board
        }
    except ValueError as e:
        raise ValueError(f"Invalid FEN: {str(e)}")

def parse_pgn(pgn_string):
    """
    Parse PGN strictly. Reject if no moves found.
    Returns dict with initial_fen, moves (list of Move), moves_san (list of SAN strings), position, headers.
    """
    try:
        text = pgn_string.strip()
        game = chess.pgn.read_game(io.StringIO(text))
        if not game:
            raise ValueError("Invalid PGN format or empty PGN.")

        moves = list(game.mainline_moves())
        if not moves:
            raise ValueError("No moves found in PGN.")

        # Build SAN list by replaying moves on a fresh board
        board = game.board()
        moves_san = []
        # board at start of game
        board = chess.Board(game.headers.get("FEN", chess.STARTING_FEN))
        for m in moves:
            san = board.san(m)
            moves_san.append(san)
            board.push(m)

        return {
            'initial_fen': chess.STARTING_FEN,
            'moves': moves,
            'moves_san': moves_san,
            'position': game.board(),
            'headers': dict(game.headers)
        }
    except Exception as e:
        # Wrap all parsing errors as ValueError so callers can handle uniformly
        raise ValueError(f"Invalid PGN: {str(e)}")

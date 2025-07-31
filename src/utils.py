import chess
import chess.pgn
import io

def parse_fen(fen_string):
    try:
        board = chess.Board(fen_string)
        return {
            'initial_fen': fen_string,
            'moves': [],
            'position': board
        }
    except ValueError as e:
        raise ValueError(f"Invalid FEN: {str(e)}")

def parse_pgn(pgn_string):
    try:
        game = chess.pgn.read_game(io.StringIO(pgn_string))
        if not game:
            raise ValueError("Invalid PGN format")
        
        moves = list(game.mainline_moves())
        return {
            'initial_fen': chess.STARTING_FEN,
            'moves': moves,
            'position': game.board(),
            'headers': dict(game.headers)
        }
    except Exception as e:
        raise ValueError(f"Invalid PGN: {str(e)}")
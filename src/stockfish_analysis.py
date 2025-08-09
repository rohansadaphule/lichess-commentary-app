import os
from dotenv import load_dotenv
import chess
import chess.engine

load_dotenv()

def analyze_moves(moves, time_limit=0.05):
    """
    Analyze each position after the move is played and return a list of dicts:
      { move: <Move>, score_cp: <int or None>, mate_in: <int or None>, best_move: <Move or None> }
    """
    stockfish_paths = [p for p in [os.getenv("STOCKFISH_PATH")] if p]
    engine_path = None
    for path in stockfish_paths:
        if path and os.path.exists(path):
            engine_path = path
            break

    if not engine_path:
        raise FileNotFoundError("Stockfish executable not found. Set STOCKFISH_PATH in .env to the stockfish binary.")

    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    try:
        results = []
        board = chess.Board()
        for move in moves:
            board.push(move)
            info = engine.analyse(board, chess.engine.Limit(time=time_limit))
            score = info.get("score")
            mate = None
            cp = None
            try:
                if score is not None:
                    if score.is_mate():
                        mate = score.mate()
                    else:
                        cp = score.relative.score()
            except Exception:
                cp = None
                mate = None

            pv = info.get("pv") or info.get("pv_lines") or info.get("pv_line")
            best_move = None
            if pv:
                try:
                    best_move = pv[0]
                except Exception:
                    best_move = pv

            results.append({
                "move": move,
                "score_cp": cp,
                "mate_in": mate,
                "best_move": best_move
            })
        return results
    finally:
        engine.quit()

import os
from dotenv import load_dotenv
import chess
import chess.engine

load_dotenv()

def analyze_moves(moves):
    # Define possible Stockfish paths
    stockfish_paths = [
        os.getenv("STOCKFISH_PATH"),
        # Add your actual Stockfish path here
    ]
    
    # Find working Stockfish path
    engine_path = None
    for path in stockfish_paths:
        if os.path.exists(path):
            engine_path = path
            break
    
    if not engine_path:
        raise FileNotFoundError("Stockfish executable not found. Please install Stockfish and update the path.")

    # Initialize the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    
    try:
        analysis_results = []
        board = chess.Board()
        
        for move in moves:
            board.push(move)
            result = engine.analyse(board, chess.engine.Limit(time=0.1))
            analysis_results.append({
                "move": move,
                "score": result["score"].relative.score(),
                "best_move": result.get("pv", [None])[0]
            })
            
        return analysis_results
    finally:
        engine.quit()
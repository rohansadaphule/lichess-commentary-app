import requests
import os

OLLAMA_API = os.getenv("OLLAMA_API") or "http://localhost:11434/api/generate"
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL") or "llama3.2:1b"

def _summarize_analysis(game_data):
    """
    Build a short human-readable analysis summary using SAN moves and the stockfish analysis list.
    """
    analysis = game_data.get('analysis', [])
    san_moves = game_data.get('moves_san') or []
    lines = []
    # Build board progressively to convert engine best_move (if UCI) to SAN for readability
    board = None
    try:
        from copy import deepcopy
        import chess
        # start from initial fen if provided
        board = chess.Board(game_data.get('initial_fen', chess.STARTING_FEN))
    except Exception:
        board = None

    for idx, a in enumerate(analysis):
        san = san_moves[idx] if idx < len(san_moves) else str(a.get('move'))
        cp = a.get('score_cp')
        mate = a.get('mate_in')
        best = a.get('best_move')
        best_san = None
        try:
            if board and best:
                # best may be a Move object or a UCI string
                if isinstance(best, str):
                    best_move = chess.Move.from_uci(best)
                else:
                    best_move = best
                best_san = board.san(best_move)
        except Exception:
            best_san = str(best)

        # push the actual move to keep board in sync
        try:
            if board:
                # push the move object if available
                move_obj = a.get('move')
                if move_obj:
                    board.push(move_obj)
        except Exception:
            pass

        score_part = f"cp {cp}" if cp is not None else (f"mate {mate}" if mate is not None else "no score")
        bm_part = f", best: {best_san or best}" if best else ""
        lines.append(f"{idx+1}. {san} ({score_part}{bm_part})")

    return "\n".join(lines)


def generate_commentary(game_data):
    """
    Generate chess commentary using Ollama API with SAN moves and a short analysis summary.
    """
    moves_san = game_data.get('moves_san') or []
    moves_str = ' '.join(moves_san) if moves_san else ' '.join(str(m) for m in game_data.get('moves', []))
    analysis_summary = _summarize_analysis(game_data)

    prompt = f"""You are a helpful chess commentator. Provide an engaging, human-readable commentary on this game.

Game moves (SAN): {moves_str}

Stockfish short analysis (per move):
{analysis_summary}

Provide a commentary that highlights key moments, tactical ideas, turning points, and a brief conclusion at the end. Keep it natural and easy to read."""
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        # tolerate multiple shapes
        if isinstance(data, dict):
            if 'response' in data and isinstance(data['response'], str):
                return data['response']
            if 'results' in data and isinstance(data['results'], list):
                parts = []
                for r in data['results']:
                    c = r.get('content') or r.get('text') or r.get('response')
                    if isinstance(c, str):
                        parts.append(c)
                if parts:
                    return "\n".join(parts)
            if 'text' in data and isinstance(data['text'], str):
                return data['text']
        # fallback to raw text
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama API error: {str(e)}")

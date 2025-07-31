from typing import List, Dict, Any

class GameData:
    def __init__(self, moves: List[str], fen: str, player_white: str, player_black: str):
        self.moves = moves
        self.fen = fen
        self.player_white = player_white
        self.player_black = player_black

class Commentary:
    def __init__(self, text: str, audio_file: str):
        self.text = text
        self.audio_file = audio_file

def parse_game_data(data: Dict[str, Any]) -> GameData:
    return GameData(
        moves=data.get('moves', []),
        fen=data.get('fen', ''),
        player_white=data.get('player_white', ''),
        player_black=data.get('player_black', '')
    )
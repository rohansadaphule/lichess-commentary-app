import sys
from ollama_integration import generate_commentary
from stockfish_analysis import analyze_moves
from audio_generation import generate_audio
from visualization import create_visualization
from utils import parse_fen, parse_pgn

def main():
    try:
        # Get user input for FEN or PGN
        user_input = input("Enter FEN or PGN: ").strip()
        
        # Parse the input
        if user_input.startswith('rnbqkbnr'):
            game_data = parse_fen(user_input)
        else:
            game_data = parse_pgn(user_input)
        
        # Analyze moves using Stockfish
        moves_analysis = analyze_moves(game_data['moves'])
        
        # Add analysis to game data
        game_data['analysis'] = moves_analysis
        
        # Generate commentary using Ollama
        commentary = generate_commentary(game_data)
        
        # Generate audio from commentary
        audio_file = generate_audio(commentary)
        
        # Create visual representation of the game
        create_visualization(game_data, audio_file)
        
        print("Commentary, audio, and visualization generated successfully.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
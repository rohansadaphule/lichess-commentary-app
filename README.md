# Lichess Commentary App

This project is designed to generate engaging commentary for chess games played on Lichess using a combination of a small LLM model (Llama 3.2:1b) and a local Stockfish engine for move analysis. The application takes game data in the form of FEN or PGN strings and produces synchronized audio commentary and visual previews of the game.

## Project Structure

```
lichess-commentary-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── ollama_integration.py   # Functions to interact with the Ollama API
│   ├── stockfish_analysis.py    # Integration with the Stockfish engine for move analysis
│   ├── audio_generation.py      # Converts commentary to audio
│   ├── visualization.py         # Creates visual representation of the game
│   ├── utils.py                # Utility functions for parsing and formatting
│   └── types
│       └── __init__.py         # Custom types and data structures
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd lichess-commentary-app
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python src/main.py
```

2. Input a FEN or PGN string when prompted.

3. The application will generate commentary, create an audio file, and produce a visual preview of the game.

## Components

- **Ollama Integration**: Utilizes the Ollama API to generate commentary based on the game data.
- **Stockfish Analysis**: Analyzes the game moves using the local Stockfish engine to provide insights and evaluations.
- **Audio Generation**: Converts the generated commentary into an audio file for playback.
- **Visualization**: Creates a visual representation of the chess game that is synchronized with the audio commentary.
- **Utilities**: Contains helper functions for parsing FEN/PGN strings and formatting data.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
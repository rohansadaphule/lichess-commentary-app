from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from utils import parse_pgn, parse_fen
from ollama_integration import generate_commentary
from stockfish_analysis import analyze_moves
from audio_generation import generate_audio
from visualization import create_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        content = request.form.get('content')
        if not content:
            return jsonify({'error': 'No content provided'}), 400

        # Parse input
        try:
            if content.startswith('rnbqkbnr'):
                game_data = parse_fen(content)
            else:
                game_data = parse_pgn(content)
        except ValueError as e:
            return jsonify({'error': f'Invalid game format: {str(e)}'}), 400

        # Analyze moves
        moves_analysis = analyze_moves(game_data['moves'])
        game_data['analysis'] = moves_analysis

        # Generate commentary
        commentary = generate_commentary(game_data)

        # Generate audio
        audio_file = generate_audio(commentary)

        # Create video
        video_path = create_video(game_data, audio_file)

        return jsonify({
            'commentary': commentary,
            'video_url': f'/download/{os.path.basename(video_path)}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
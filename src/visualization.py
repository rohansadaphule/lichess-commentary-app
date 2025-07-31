from matplotlib import pyplot as plt
import chess
import chess.pgn
import numpy as np
import matplotlib.animation as animation
import os
import chess.svg
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip
import cairosvg
import tempfile

def create_visualization(game_data, audio_file):
    board = chess.Board(game_data['initial_fen'])
    moves = game_data['moves']
    
    fig, ax = plt.subplots()
    ax.set_title("Lichess Game Visualization")
    
    def draw_board():
        ax.clear()
        ax.set_title("Lichess Game Visualization")
        board_image = np.zeros((8, 8, 3), dtype=np.uint8)
        for i in range(8):
            for j in range(8):
                piece = board.piece_at(chess.square(j, 7-i))
                if piece:
                    board_image[i, j] = piece_color(piece.color)
                else:
                    board_image[i, j] = [255, 255, 255] if (i + j) % 2 == 0 else [0, 0, 0]
        ax.imshow(board_image)
        ax.axis('off')

    def piece_color(is_white):
        return [255, 255, 255] if is_white else [0, 0, 0]

    def update(frame):
        if frame < len(moves):
            move = moves[frame]
            board.push(move)
            draw_board()

    ani = animation.FuncAnimation(fig, update, frames=len(moves), repeat=False)
    
    plt.tight_layout()
    plt.show()

    # Save the animation as a video or GIF if needed
    # ani.save('game_visualization.mp4', writer='ffmpeg')

    # Optionally, you can add audio synchronization logic here if needed
    # For example, using a library like pydub to play audio alongside the visualization.

def create_video(game_data, audio_file):
    board = chess.Board(game_data['initial_fen'])
    moves = game_data['moves']
    
    # Create temporary directory for frames
    with tempfile.TemporaryDirectory() as temp_dir:
        frames = []
        
        # Generate frame for initial position
        svg_data = chess.svg.board(board=board, size=400)
        png_path = os.path.join(temp_dir, f"frame_0.png")
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_path)
        frames.append(png_path)
        
        # Generate frame for each move
        for i, move in enumerate(moves):
            board.push(move)
            svg_data = chess.svg.board(board=board, size=400)
            png_path = os.path.join(temp_dir, f"frame_{i+1}.png")
            cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_path)
            frames.append(png_path)
        
        # Create video from frames
        clip = ImageSequenceClip(frames, fps=1)
        
        # Add audio
        audio = AudioFileClip(audio_file)
        final_clip = clip.set_audio(audio)
        
        # Export video
        output_path = os.path.join('..', 'uploads', 'analysis.mp4')
        final_clip.write_videofile(output_path)
        
        return output_path
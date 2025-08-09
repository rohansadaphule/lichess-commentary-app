import chess
import chess.svg
import cairosvg
import tempfile
import os
from moviepy.editor import AudioFileClip, ImageSequenceClip

def create_video(game_data, audio_file):
    """
    Creates an MP4 video synchronized with the commentary audio.
    Each frame (initial position + one per move) will share the audio duration equally.
    """
    uploads_dir = os.getenv("UPLOAD_PATH") or os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    board = chess.Board(game_data.get('initial_fen', chess.STARTING_FEN))
    moves = list(game_data.get('moves', []))

    with tempfile.TemporaryDirectory() as temp_dir:
        frames = []

        # initial position frame
        svg_data = chess.svg.board(board=board, size=400)
        png_path = os.path.join(temp_dir, "frame_0.png")
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_path)
        frames.append(png_path)

        # frames for each move
        for i, move in enumerate(moves):
            board.push(move)
            svg_data = chess.svg.board(board=board, size=400)
            png_path = os.path.join(temp_dir, f"frame_{i+1}.png")
            cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_path)
            frames.append(png_path)

        # load audio and compute durations
        audio = AudioFileClip(audio_file)
        total_duration = audio.duration or 1.0
        num_frames = len(frames)
        frame_duration = total_duration / num_frames

        # Create a clip where each image has the computed duration
        clip = ImageSequenceClip(frames, durations=[frame_duration] * num_frames)

        # attach audio
        final_clip = clip.set_audio(audio)

        # output mp4 in uploads directory
        output_path = os.path.join(uploads_dir, 'analysis.mp4')
        # write file (moviepy uses ffmpeg)
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        return output_path

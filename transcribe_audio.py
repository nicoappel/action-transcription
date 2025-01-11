import whisper
import os
import subprocess
from typing import Optional

def download_video_audio(video_url: str, output_path: Optional[str] = None) -> str:
    """
    Download audio from video using yt-dlp.
    
    Args:
        video_url: URL of the video to download
        output_path: Optional custom output path for the audio file
    
    Returns:
        Path to the downloaded audio file
    """
    if output_path is None:
        output_path = "downloaded_audio.mp3"
    
    try:
        subprocess.run([
            "yt-dlp", 
            "-x",  # extract audio
            "--audio-format", "mp3", 
            "-o", output_path, 
            video_url
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        raise
    
    return output_path

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribe audio using local Whisper installation.
    
    Args:
        audio_path: Path to the audio file
        model_size: Size of the Whisper model to use
    
    Returns:
        Transcribed text
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

def main(video_url: str):
    """
    Main transcription workflow.
    
    Args:
        video_url: URL of the video to transcribe
    """
    try:
        audio_path = download_video_audio(video_url)
        transcript = transcribe_audio(audio_path)
        
        # Save transcript
        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
        
        # Clean up downloaded audio
        os.remove(audio_path)
        
        print("Transcription completed successfully.")
    except Exception as e:
        print(f"Transcription failed: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please provide a video URL")
        sys.exit(1)
    main(sys.argv[1])

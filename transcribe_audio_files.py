import os
import subprocess
from pathlib import Path
from typing import List, Optional

def find_audio_files(base_dir: str = 'voices') -> List[str]:
    """
    Scan the directory and its subdirectories for .wav and .mp3 files.

    :param base_dir: Base directory to start scanning
    :return: List of full paths to audio files
    """
    audio_files = []
    base_path = Path(base_dir)

    # Check if base directory exists
    if not base_path.exists():
        print(f"Directory {base_dir} does not exist.".encode('utf-8').decode())
        return audio_files

    # Find all .wav and .mp3 files recursively
    for file_path in base_path.rglob('*'):
        if file_path.suffix.lower() in ['.wav', '.mp3']:
            audio_files.append(str(file_path))

    return audio_files

def convert_to_16khz_wav(input_file: str) -> Optional[str]:
    """
    Convert input audio file to 16kHz .wav using ffmpeg.

    :param input_file: Path to the input audio file
    :return: Path to the temporary 16kHz .wav file
    """
    # Create a temporary filename in the same directory
    temp_file = Path(input_file).with_suffix('.16khz.wav')
    print(f"converting {input_file} to {temp_file}".encode('utf-8').decode())

    try:
        # Use ffmpeg to convert to 16kHz wav
        subprocess.run([
            'ffmpeg',
            '-i', input_file,
            '-ar', '16000',  # Set audio rate to 16kHz
            '-ac', '1',      # Convert to mono
            str(temp_file)
        ], check=True, capture_output=True)

        return str(temp_file)

    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}".encode('utf-8').decode())
        return None

def transcribe_audio(audio_file: str) -> Optional[str]:
    """
    Transcribe audio file using Whisper.

    :param audio_file: Path to the 16kHz wav file
    :return: Transcription text
    """
    try:
        # Run Whisper transcription
        result = subprocess.run([
            'D:/Diffusion_Auto_F111/Whisper.cpp/main.exe',
            audio_file,
            '-m', 'D:/Diffusion_Auto_F111/Whisper.cpp/ggml-medium.en-q8_0.bin',  # You can change the model as needed
            '-np', '-nt',
        ], check=True, capture_output=True, text=True)

        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(f"Error transcribing {audio_file}: {e}".encode('utf-8').decode())
        return None

def process_audio_files(base_dir: str = 'voices') -> None:
    """
    Main function to process all audio files in the directory.

    :param base_dir: Base directory to start scanning
    """
    # Find all audio files
    audio_files = find_audio_files(base_dir)

    print(f"Found {len(audio_files)} audio files.".encode('utf-8').decode())

    for audio_file in audio_files:
        try:
            # Convert to 16kHz wav
            temp_wav = convert_to_16khz_wav(audio_file)

            if not temp_wav:
                continue

            # Transcribe
            transcription = transcribe_audio(temp_wav)

            if transcription:
                # Save the transcription as a .txt file in the same directory as the audio file
                txt_file = Path(audio_file).with_suffix('.txt')
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(transcription)

                print(f"Saved transcription {audio_file} -> {txt_file}".encode('utf-8').decode())

            # Always clean up temporary file
            if Path(temp_wav).exists():
                Path(temp_wav).unlink()

        except Exception as e:
            print(f"Error processing {audio_file}: {e}".encode('utf-8').decode())

if __name__ == '__main__':
    process_audio_files()

import os
from pathlib import Path

def rename_audio_files(base_dir: str) -> None:
    """
    Walk through the subdirectories and rename .wav, .mp3, and .ogg files to match the directory name.
    If there are multiple audio files in a directory, add a counter to the filename.

    :param base_dir: Base directory to start scanning
    """
    base_path = Path(base_dir)

    # Check if base directory exists
    if not base_path.exists():
        print(f"Directory {base_dir} does not exist.".encode('utf-8').decode())
        return

    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(base_path):
        audio_files = [f for f in filenames if f.lower().endswith(('.wav', '.mp3', '.ogg'))]
        if audio_files:
            dir_name = Path(dirpath).name
            counter = 1
            for audio_file in audio_files:
                ext = Path(audio_file).suffix
                new_name = f"{dir_name}{counter if len(audio_files) > 1 else ''}{ext}"
                old_path = Path(dirpath) / audio_file
                new_path = Path(dirpath) / new_name
                old_path.rename(new_path)
                print(f"Renamed: {old_path} -> {new_path}".encode('utf-8').decode())
                counter += 1

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python rename_audio_files.py <base_dir>".encode('utf-8').decode())
        sys.exit(1)
    base_dir = sys.argv[1]
    rename_audio_files(base_dir)

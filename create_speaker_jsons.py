import os
from pathlib import Path
import outetts
import torch
from typing import List, Optional

def find_audio_and_transcription_files(base_dir: str = 'voices') -> List[tuple]:
    """
    Scan the directory and its subdirectories for .wav and .mp3 files and their corresponding .txt files.

    :param base_dir: Base directory to start scanning
    :return: List of tuples containing full paths to audio files and their corresponding transcription files
    """
    file_pairs = []
    base_path = Path(base_dir)

    # Check if base directory exists
    if not base_path.exists():
        print(f"Directory {base_dir} does not exist.".encode('utf-8').decode())
        return file_pairs

    # Find all .wav and .mp3 files recursively
    for file_path in base_path.rglob('*'):
        if file_path.suffix.lower() in ['.wav', '.mp3', '.ogg']:
            txt_file = file_path.with_suffix('.txt')
            if txt_file.exists():
                file_pairs.append((str(file_path), str(txt_file)))

    return file_pairs

def process_audio_and_transcription_files(base_dir: str = 'voices', interface: Optional[outetts.InterfaceGGUF] = None) -> None:
    """
    Main function to process all audio files and their corresponding transcription files in the directory.

    :param base_dir: Base directory to start scanning
    :param interface: The interface object for creating and saving speakers
    """
    # Find all audio and transcription file pairs
    file_pairs = find_audio_and_transcription_files(base_dir)

    print(f"Found {len(file_pairs)} audio and transcription file pairs.".encode('utf-8').decode())

    # Create the speakers directory in the current directory if it doesn't exist
    speakers_dir = Path('./speakers')
    speakers_dir.mkdir(parents=True, exist_ok=True)

    for audio_file, txt_file in file_pairs:
        try:
            # Read the transcription
            with open(txt_file, 'r', encoding='utf-8') as f:
                transcription = f.read().strip()

            # Create a speaker using the interface
            speaker = interface.create_speaker(audio_file, transcription)

            # Remove the existing extension and append .json
            json_file = speakers_dir / (Path(audio_file).stem + '.json')

            # Save the speaker using the interface
            interface.save_speaker(speaker, json_file)

            print(f"Saved speaker data {audio_file} -> {json_file}".encode('utf-8').decode())

        except Exception as e:
            print(f"Error processing {audio_file}: {e}".encode('utf-8').decode())

def main() -> None:
    """
    Main function to configure the model and process audio and transcription files.
    """
    # Configure the model
    model_config = outetts.GGUFModelConfig_v1(
        model_path="model/OuteTTS-0.2-500M-FP16.gguf",
        language="en", # Supported languages in v0.2: en, zh, ja, ko
        dtype=torch.bfloat16,
        additional_model_config={
            'attn_implementation': "flash_attention_2"
        },
        n_gpu_layers=0,
    )

    # Initialize the GGUF interface
    interface = outetts.InterfaceGGUF(model_version="0.2", cfg=model_config)
    # Run the audio and transcription processing
    process_audio_and_transcription_files(interface=interface)

if __name__ == '__main__':
    main()

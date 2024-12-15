import outetts
import torch
import sys
import os
import json
from pathlib import Path
import argparse
import pandas as pd

def configure_model(model_path: str, language: str, dtype: torch.dtype) -> outetts.HFModelConfig_v1:
    """
    Configure the GGUF model.

    :param model_path: Path to the model file
    :param language: Language code for the model
    :param dtype: Data type for the model
    :return: Configured HFModelConfig_v1 object
    """
    try:
        model_config = outetts.HFModelConfig_v1(
            model_path=model_path,
            language=language,
            dtype=dtype,
        )
        print(f"Model configured successfully with path: {model_path}".encode('utf-8').decode())
        return model_config
    except Exception as e:
        print(f"Error configuring model: {e}".encode('utf-8').decode())
        sys.exit(1)

def initialize_interface(model_version: str, model_config: outetts.GGUFModelConfig_v1) -> outetts.InterfaceGGUF:
    """
    Initialize the GGUF interface.

    :param model_version: Version of the model
    :param model_config: Configured GGUFModelConfig_v1 object
    :return: Initialized InterfaceGGUF object
    """
    try:
        interface = outetts.InterfaceHF(model_version=model_version, cfg=model_config)
        print("Interface initialized successfully.".encode('utf-8').decode())
        return interface
    except Exception as e:
        print(f"Error initializing interface: {e}".encode('utf-8').decode())
        sys.exit(1)

def load_speakers(speakers_dir: str) -> dict:
    """
    Load speaker JSON files from the speakers directory.

    :param speakers_dir: Path to the speakers directory
    :return: Dictionary mapping speaker names to their JSON file paths
    """
    speakers = {}
    for file in os.listdir(speakers_dir):
        if file.endswith(".json"):
            speaker_name = os.path.splitext(file)[0]
            speakers[speaker_name] = os.path.join(speakers_dir, file)
    return speakers

def main(config: dict, csv_file: str) -> None:
    """
    Main function to configure the model, initialize the interface, and generate speech.

    :param config: Dictionary containing the configuration parameters
    :param csv_file: Path to the CSV file containing the input data
    """
    # Configure the model
    dtype_map = {
        'bfloat16': torch.bfloat16,
        'float16': torch.float16,
        'float32': torch.float32,
    }
    dtype = dtype_map.get(config['dtype'], torch.bfloat16)

    model_config = configure_model(config['model_path'], config['language'], dtype)

    # Initialize the GGUF interface
    interface = initialize_interface(config['model_version'], model_config)

    # Load speakers from the speakers directory
    speakers_dir = config['speakers_dir']  # Path to the speakers directory from config
    speakers = load_speakers(speakers_dir)

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Ensure the outputs directory exists
    outputs_dir = config['outputs_dir']  # Path to the outputs directory from config
    os.makedirs(outputs_dir, exist_ok=True)

    for index, row in df.iterrows():
        speaker_name = row['SpeakerID']
        text = row['Text']
        text = text.strip().strip('"').strip("'") + " "
        output_name = row['OutputName']

        if speaker_name not in speakers:
            print(f"Speaker {speaker_name} not found in the speakers directory.".encode('utf-8').decode())
            continue

        speaker_path = speakers[speaker_name]

        # Load speaker from the JSON file
        speaker = interface.load_speaker(speaker_path)

        # Generate speech
        output = interface.generate(
            text=text,
            temperature=config['temperature'],
            repetition_penalty=config['repetition_penalty'],
            max_length=config['max_length'],
            speaker=speaker,
        )

        # Save the synthesized speech to a file in the outputs directory
        output_path = Path(outputs_dir) / f"{output_name}.wav"
        output.save(str(output_path))
        print(f"Synthesized speech saved to {output_path}".encode('utf-8').decode())

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate speech using OuteTTS.')
    parser.add_argument('--csv_file', type=str, required=True, help='Path to the CSV file containing the input data')
    args = parser.parse_args()

    # Load configuration from outtsconfig.json
    config_path = Path('outtsconfig.json')
    if not config_path.exists():
        print(f"Configuration file {config_path} does not exist.".encode('utf-8').decode())
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    main(config, args.csv_file)

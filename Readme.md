# OuteTTS Toolkit

This repository contains a collection of Python scripts for processing audio files and generating speech using OutteTTS (https://github.com/edwko/OuteTTS)
The code here revolves around the three subdirectories: (a) voices (b) speakers (c) outputs.

(a) Voices:  Contains the .wav and .mp3 of the voices you want to use/clone for TTS
(b) Speakers: Voices are tokenized and stored a as .json files in 'Speakers'. Once you have the speaker json files, you don't need the original .wav files anymore.
(c) Output: Once you infer (That is, do text to speech) with 'infer_csv.py', the outputs are stored here.


This code has been tested to run on Windows. It will probably need some modifications to run on other platforms.

## Scripts

### `AdjustVolumeAndDenoise.py`

This script adjusts the volume of audio files, applies noise reduction, and adds a small amount of silence at the end.

**Command-line arguments:**

-   `volume`: (required) Desired final volume level in decibels (dB).
-   `-d` or `--directory`: (optional) Directory containing audio files to process. Defaults to "outputs".
-   `-e` or `--extension`: (optional) Output file extension (e.g., wav, mp3). If not provided, the original extension is used.
-   `-n` or `--NoiseFilter`: (optional) Noise filtering method: 1 = RNNoise (cb.rnnn), 2 = Bandpass + Noise Gate.

**Example:**

```bash
python AdjustVolumeAndDenoise.py 0 -d outputs -e wav -n 1
```

### `create_speaker_jsons.py`

This script scans a directory for audio files and their corresponding transcriptions, then creates speaker JSON files.

This script does not take any command line arguments.

**Example:**

```bash
python create_speaker_jsons.py
```

### `infer.py`

This script generates speech from a given text using the OuteTTS model.

This script does not take any command line arguments.

**Example:**

```bash
python infer.py
```

### `infer_csv.py`

This script generates speech from a CSV file, using speaker profiles.

**Command-line arguments:**

-   `--csv_file`: (required) Path to the CSV file containing the input data.

**Example:**

```bash
python infer_csv.py --csv_file input.csv
```

### `infer_gguf_config.py`

This script generates speech using a GGUF model configuration.

This script does not take any command line arguments.

**Example:**

```bash
python infer_gguf_config.py
```

### `normalize_outputs.py`

This script normalizes the volume of audio files in the outputs directory.

This script does not take any command line arguments.

**Example:**

```bash
python normalize_outputs.py
```

### `rename_audio_files.py`

This script renames audio files in a directory to match their parent directory name. You need to have ffmpeg in your system $PATH variable.

**Command-line arguments:**

-   `base_dir`: (required) Base directory to start scanning.

**Example:**

```bash
python rename_audio_files.py voices
```

### `transcribe_audio_files.py`

This script transcribes audio files using Whisper binary. I have used whisper.cpp (https://github.com/ggerganov/whisper.cpp) for that. You need to download a whisper binary and store it somewhere in your system. Then edit the script to point to the binary.

This script does not take any command line arguments. It will automatically transcribes all the .wav and .mp3 files in the voices/ directory. It will place a .txt file in the same place as the audio file. The .txt file contains the transcription.

**Example:**

```bash
python transcribe_audio_files.py
```

## Configuration

The `outtsconfig.json` file contains configuration parameters for the OuteTTS model and other settings.

```json
{
    "model_path": "OuteAI/OuteTTS-0.2-500M",
    "language": "en",
    "dtype": "bfloat16",
    "attn_implementation": "flash_attention_2",
    "n_gpu_layers": 0,
    "model_version": "0.2",
    "text": "Speech synthesis is the artificial production of human speech. A computer system used for this purpose is called a speech synthesizer, and it can be implemented in software or hardware products.",
    "temperature": 0.1,
    "repetition_penalty": 1.0,
    "max_length": 4096,
    "speaker_name": "male_1",
    "speakers_dir": "speakers",
    "outputs_dir": "outputs"
}
```

## Dependencies

The required Python packages are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## Batch Files

### `run_adjust_volume.bat`

This batch file executes the `AdjustVolumeAndDenoise.py` script with predefined arguments.

**Example:**

```batch
run_adjust_volume.bat
```

### `run_create_speaker_jsons.bat`
Assuming that there is a python venv named 'env' in the current directory, This batch file activates the virtual environment and executes the `create_speaker_jsons.py` script.

**Example:**

```batch
run_create_speaker_jsons.bat
```

### `run_infer_csv.bat`

Assuming that there is a python venv named 'env' in the current directory, This batch file activates the virtual environment and executes the `infer_csv.py` script with `outtsinput.csv` as input.

**Example:**

```batch
run_infer_csv.bat
```

### `run_transcribe_audio_files.bat`

This batch file executes the `transcribe_audio_files.py` script.

**Example:**

```batch
run_transcribe_audio_files.bat
```
```

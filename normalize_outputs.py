import os
import subprocess
from ffmpeg_normalize import FFmpegNormalize

def normalize_volume(input_path, output_path):
    """
    Normalize the volume of an audio file using ffmpeg-normalize.

    :param input_path: Path to the input audio file
    :param output_path: Path to the output audio file
    """
    try:
        # Normalize the volume and add 0.1 seconds of silence at the end
        ffmpeg_normalize = FFmpegNormalize(
            true_peak =-0.50,    # Set the true peak level
            print_stats=True          # Print statistics
        )

        # Add input file and set output file
        ffmpeg_normalize.add_media_file(input_path, output_path)

        # Perform normalization
        ffmpeg_normalize.run_normalization()

        print(f"Normalized volume and added silence for {input_path} and saved to {output_path}")

    except Exception as e:
        print(f"Error processing file {input_path}: {e}")

def main():
    outputs_dir = 'outputs'
    temp_dir = 'temp_normalized'

    # Create the temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    # Loop through each file in the outputs directory
    for file_name in os.listdir(outputs_dir):
        if file_name.endswith('.wav') or file_name.endswith('.mp3'):
            input_path = os.path.join(outputs_dir, file_name)
            output_path = os.path.join(temp_dir, file_name)

            # Normalize the volume of the file and add silence
            normalize_volume(input_path, output_path)

            # Replace the original file with the normalized file
            os.replace(output_path, input_path)

    # Remove the temporary directory
    os.rmdir(temp_dir)

    print("Volume normalization completed.")

if __name__ == '__main__':
    main()

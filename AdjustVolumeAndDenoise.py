import os
import sys
import subprocess
import argparse
import re

def detect_volume(file_path):
    """
    Detect volume using ffmpeg volumedetect
    
    Args:
        file_path (str): Full path to the audio file
    
    Returns:
        dict: Volume detection metrics
    """
    try:
        volumedetect_cmd = [
            'ffmpeg', 
            '-i', file_path,
            '-filter:a', 'volumedetect',
            '-f', 'null',
            '/dev/null'
        ]
        
        # Run volume detection
        result = subprocess.run(volumedetect_cmd, 
                                capture_output=True, 
                                text=True)
        
        # Parse volume metrics
        metrics = {}
        volume_patterns = {
            'max_volume': r'max_volume: (-?\d+\.\d+) dB',
            'mean_volume': r'mean_volume: (-?\d+\.\d+) dB',
            'max_peak': r'max_peak: (-?\d+\.\d+) dB'
        }
        
        for metric, pattern in volume_patterns.items():
            match = re.search(pattern, result.stderr)
            if match:
                metrics[metric] = float(match.group(1))
        
        return metrics
    
    except Exception as e:
        print(f"Error detecting volume for {file_path}: {e}")
        return {}

def process_audio_file(file_path, desired_volume, output_ext=None, noise_filter=None):
    """
    Process audio file with volume adjustment, noise filtering, and padding
    
    Args:
        file_path (str): Full path to the audio file
        desired_volume (float): Desired final volume adjustment in dB
        output_ext (str, optional): Desired output file extension
        noise_filter (int, optional): Noise filtering method
    """
    try:
        # Detect current volume
        metrics = detect_volume(file_path)
        if not metrics:
            print(f"Could not detect volume for {file_path}")
            return
        
        # Calculate real adjustment based on max volume
        real_adjustment = desired_volume - metrics['max_volume']
        
        # Determine output file extension
        file_name, original_ext = os.path.splitext(file_path)
        if output_ext is None:
            output_ext = original_ext
        
        # Ensure extension starts with a dot
        if not output_ext.startswith('.'):
            output_ext = '.' + output_ext
        
        # Prepare intermediate and final output files
        intermediate_file_1 = file_path + '.vol_adj' + output_ext
        intermediate_file_2 = file_path + '.noise_filt' + output_ext
        final_output_file = file_path + '.tmp' + output_ext

        # 1. Volume Adjustment
        ffmpeg_volume_cmd = [
            'ffmpeg', 
            '-i', file_path,
            '-filter:a', f'volume={real_adjustment}dB',
            '-y', intermediate_file_1
        ]
        
        print(f'Currently Processing {os.path.basename(file_path)}')
        print(f'Current Max Volume: {metrics["max_volume"]} dB')
        print(f'Desired Volume: {desired_volume} dB')
        print(f'Real Volume Adjustment: {real_adjustment} dB')
        
        subprocess.run(ffmpeg_volume_cmd, check=True)

        # 2. Noise Filtering
        ffmpeg_noise_cmd = ['ffmpeg', '-i', intermediate_file_1]
        
        if noise_filter == 1:
            print("Applying Noise Reduction: RNNoise (cb.rnnn)")
            ffmpeg_noise_cmd.extend(['-af', 'arnndn=m=cb.rnnn'])
        elif noise_filter == 2:
            print("Applying Noise Reduction: Bandpass + Noise Gate")
            ffmpeg_noise_cmd.extend(['-af', 'highpass=200,lowpass=3000,afftdn'])
        
        ffmpeg_noise_cmd.extend(['-y', intermediate_file_2])
        
        subprocess.run(ffmpeg_noise_cmd, check=True)

        # 3. Padding with Silence
        ffmpeg_padding_cmd = [
            'ffmpeg',
            '-i', intermediate_file_2,
            '-af', 'apad=whole_dur=0.1',
            '-y', final_output_file
        ]

        subprocess.run(ffmpeg_padding_cmd, check=True)

        # Replace original file
        os.replace(final_output_file, file_path)

        # If extension is different, rename the file
        if output_ext != original_ext:
            new_file_path = file_name + output_ext
            os.rename(file_path, new_file_path)
            print(f'Renamed to {os.path.basename(new_file_path)}')

        print(f'Successfully processed {os.path.basename(file_path)}')

        # Clean up intermediate files
        os.remove(intermediate_file_1)
        os.remove(intermediate_file_2)

    except subprocess.CalledProcessError as e:
        print(f"Error processing {file_path}: {e}")
        # Clean up intermediate files in case of error
        if os.path.exists(intermediate_file_1):
            os.remove(intermediate_file_1)
        if os.path.exists(intermediate_file_2):
            os.remove(intermediate_file_2)
        if os.path.exists(final_output_file):
            os.remove(final_output_file)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Audio Volume Adjustment and Noise Reduction Script')
    parser.add_argument('volume', type=float, help='Desired final volume level in decibels (dB).')
    parser.add_argument('-d', '--directory', type=str, default='outputs', help='Directory containing audio files to process. Defaults to "outputs".')
    parser.add_argument('-e', '--extension', type=str, help='Optional output file extension (e.g., wav, mp3). If not provided, original extension is used.')
    parser.add_argument('-n', '--NoiseFilter', type=int, choices=[1, 2], help='Noise filtering method: 1 = RNNoise (cb.rnnn), 2 = Bandpass + Noise Gate')

    args = parser.parse_args()

    audio_extensions = ['.wav', '.mp3']

    sys.stdout.reconfigure(encoding='utf-8')

    for filename in os.listdir(args.directory):
        file_path = os.path.join(args.directory, filename)

        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in audio_extensions:
            process_audio_file(file_path, args.volume, args.extension, args.NoiseFilter)

if __name__ == '__main__':
    main()

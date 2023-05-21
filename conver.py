import subprocess

def convert_wav_to_flac(input_file, output_file, compression_level=8, bit_depth=16):
    command = ['ffmpeg', '-y', '-i', input_file, '-c:a', 'flac', '-compression_level', str(compression_level), '-sample_fmt', f's16', '-ar', '44100', output_file]
    subprocess.run(command)

input_file = '/home/luis/chat/static/audio.wav'
output_file = '/home/luis/chat/static/audio.flac'
compression_level = 8  # Adjust the compression level as desired (0-8)
bit_depth = 8  # Set the desired bit depth (e.g., 16, 24)

convert_wav_to_flac(input_file, output_file, compression_level, bit_depth)

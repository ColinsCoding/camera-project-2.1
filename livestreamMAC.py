import subprocess
import time
#testing
# Set your YouTube stream key
YOUTUBE_STREAM_KEY = "dktr-20au-bqkh-3gac-cy62"

# Video settings
WIDTH = 1280
HEIGHT = 720
FRAMERATE = 30
BITRATE = 2000  # kbps

# Create a command for ffmpeg to stream to YouTube using the AVFoundation input device
command = (
    f"ffmpeg -f avfoundation -video_size {WIDTH}x{HEIGHT} -framerate {FRAMERATE} -i \"0:none\" "
    f"-c:v libx264 -b:v {BITRATE}k -maxrate {BITRATE}k -bufsize {BITRATE}k -g {FRAMERATE} -pix_fmt yuv420p "
    f"-f flv rtmp://x.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"
)

def livestream(duration):
    """Stream video from the camera to YouTube."""
    # Start ffmpeg as a subprocess
    ffmpeg_process = subprocess.Popen(command, shell=True)

    # Record for the specified duration
    time.sleep(duration)

    # Stop recording and close the ffmpeg subprocess
    ffmpeg_process.terminate()

if __name__ == "__main__":
    # Stream for 60 seconds as an example
    livestream_duration = 600
    livestream(livestream_duration)

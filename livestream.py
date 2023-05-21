import subprocess
import picamera2
import time
import signal
from datetime import datetime
import threading


# Set your YouTube stream key
YOUTUBE_STREAM_KEY = "your-stream-key"

# Video settings
WIDTH = 1280
HEIGHT = 720
FRAMERATE = 30
BITRATE = 2000  # kbps


# Create a command for ffmpeg to stream to YouTube
command = (
    f"ffmpeg -f h264 -i - -f lavfi -i anullsrc -c:v copy -c:a aac -f flv rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"
)

def start_ffmpeg():
    """Start the ffmpeg subprocess."""
    return subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)


def stop_ffmpeg(ffmpeg_process):
    """Stop the ffmpeg subprocess."""
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()


def livestream(duration):
    """Stream video from the camera to YouTube."""
    # Start ffmpeg as a subprocess
    ffmpeg_process = start_ffmpeg()

    # Initialize the camera
    with picamera2.PiCamera(resolution=(WIDTH, HEIGHT), framerate=FRAMERATE) as camera:
        # Allow the camera to warm up
        time.sleep(2)

        # Start capturing video and piping it to the ffmpeg subprocess
        camera.start_recording(ffmpeg_process.stdin, format="h264", bitrate=BITRATE * 1000)

        # Record for the specified duration
        camera.wait_recording(duration)

        # Stop recording and close the ffmpeg subprocess
        camera.stop_recording()

    stop_ffmpeg(ffmpeg_process)


if __name__ == "__main__":
    # Stream for 60 seconds as an example
    livestream_duration = 60
    livestream(livestream_duration)


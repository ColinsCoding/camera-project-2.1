import subprocess
import picamera2
import time
import signal
import boto3
from datetime import datetime
import threading


# Set your YouTube stream key
YOUTUBE_STREAM_KEY = "your-stream-key"

# Video settings
WIDTH = 1280
HEIGHT = 720
FRAMERATE = 30
BITRATE = 2000  # kbps
# LIVESTREAM_DURATION = 60 # time in seconds 

# Timelapse settings
TIMELAPSE_INTERVAL = 60  # seconds between images
TIMELAPSE_DURATION = 3600  # total duration of the timelapse in seconds

# AWS S3 settings
S3_BUCKET = "your-s3-bucket-name"

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


# def capture_timelapse_image():
#     """Capture a timelapse image and return the image data."""
#     with picamera2.PiCamera(resolution=(WIDTH, HEIGHT)) as camera:
#         time.sleep(2)  # Allow the camera to warm up
#         image_data = camera.capture(output_format="jpeg")
#     return image_data


# def upload_to_s3(image_data, s3_key):
#     """Upload the given image data to the specified S3 key."""
#     s3 = boto3.client("s3")
#     s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=image_data, ContentType="image/jpeg")


# def timelapse():
#     """Capture timelapse images and upload them to S3."""
#     start_time = time.time()
#     while time.time() - start_time < TIMELAPSE_DURATION:
#         # Capture a timelapse image
#         image_data = capture_timelapse_image()

#         # Generate a unique key for the image in S3
#         timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
#         s3_key = f"timelapse/{timestamp}.jpg"

#         # Upload the image to S3
#         upload_to_s3(image_data, s3_key)

#         # Wait for the next timelapse interval
#         time.sleep(TIMELAPSE_INTERVAL)



if __name__ == "__main__":
    # Stream for 60 seconds as an example
    livestream_duration = 60
    livestream(livestream_duration)

    # Run the timelapse
    # timelapse()

# def livestream_and_timelapse():
#     livestream_thread = threading.Thread(target=livestream, args=(LIVESTREAM_DURATION,))
#     timelapse_thread = threading.Thread(target=timelapse)

#     livestream_thread.start()
#     timelapse_thread.start()

#     livestream_thread.join()
#     timelapse_thread.join()

# if __name__ == "__main__":
#     livestream_and_timelapse()

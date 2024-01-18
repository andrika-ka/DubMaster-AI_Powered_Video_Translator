import time
from moviepy.editor import VideoFileClip
import gc
import os
import subprocess


class LipSynchronization:

    def __init__(self):
        pass

    def mute_video(self, input_path):
        # Record the start time
        start_time = time.time()

        # Load the video clip from the input file
        videoclip = VideoFileClip(input_path)

        # Remove the audio from the video clip
        new_clip = videoclip.without_audio()

        # Write the muted video to a new file ("muted_video.mp4")
        new_clip.write_videofile("muted_video.mp4")

        # Specify the path of the muted video file
        video_file = "muted_video.mp4"

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert elapsed time to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        # Print the execution time for video muting
        print(
            f"⏱️ Execution time for video muting: {int(minutes)} minutes and {round(seconds, 2)} seconds")

        # Return the path of the muted video file
        return video_file

    def lip_sync(self, muted_video_path, generated_voice_path, target_language):
        # Record the start time
        start_time = time.time()

        # Perform garbage collection
        gc.collect()

        # Switch to the directory /content/Wav2Lip-HD
        os.chdir("/content/Wav2Lip-HD")

        # Set target directories for audio and video inputs
        target_audio = "/content/Wav2Lip-HD/input_audios"
        target_video = "/content/Wav2Lip-HD/input_videos"

        # Copy generated voice and muted video to target directories
        command = (
            f'cp -r "{generated_voice_path}" "{target_audio}"; '
            f'cp -r "{muted_video_path}" "{target_video}"; '
        )
        subprocess.run(command, shell=True, capture_output=True, text=True)

        print("Lip synchronization is loading...")

        # Install required dependencies using specified versions
        c = "pip install -qq librosa==0.8.0"
        c1 = "pip install -qq numpy==1.22.0"
        os.system(c)
        os.system(c1)

        # Set paths for model checkpoints and input/output files
        checkpoint_path = "checkpoints/wav2lip_gan.pth"
        segment_path = "checkpoints/face_segmentation.pth"
        sr_p = "checkpoints/esrgan_yunying.pth"
        face_video_path = "input_videos/muted_video.mp4"
        audio_path = "input_audios/generated_voice.wav"
        outfile_path = "output_videos_wav2lip/final_dubbed_video.mp4"

        # Build the command for lip synchronization
        command = (f"cd /content/Wav2Lip-HD && python inference.py "
                   f"--checkpoint_path {checkpoint_path} "
                   f"--face {face_video_path} "
                   f"--audio {audio_path} "
                   "--pads 0 20 0 0 "
                   f"--outfile {outfile_path} "
                   f"--segmentation_path {segment_path} "
                   f"--sr_path {sr_p} "
                   "--save_frames "
                   "--resize_factor 2 "
                   "--no_sr "
                   "--no_segmentation "
                   "--nosmooth ")

        # Execute the lip synchronization command
        os.system(command)

        # Build the command to extract frames from the output video
        command2 = (
            'python video2frames.py '
            '--input_video "output_videos_wav2lip/final_dubbed_video.mp4" '
            '--frames_path "frames_wav2lip/muted_video"'
        )

        # Execute the command to extract frames
        os.system(command2)

        synced_video_path = "/content/Wav2Lip-HD/output_videos_wav2lip/final_dubbed_video.mp4"

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        # Print information about the lip synchronization process
        print("Frames have been created and can be found under /content/Wav2Lip-HD/frames_wav2lip")
        print("✅ Lip synchronization has been performed")
        print(
            f"⏱️ Execution time for lip syncing: {int(minutes)} minutes and {round(seconds, 2)} "
            f"seconds for language: {target_language}")

        # Return the path of the synchronized video
        return synced_video_path

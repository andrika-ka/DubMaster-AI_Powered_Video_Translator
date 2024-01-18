import time
from moviepy.editor import VideoFileClip
import gc
import os


class LipSynchronization:

    def __init__(self):
        pass

    def mute_video(self, input_path):
        # Record the start time
        start_time = time.time()

        videoclip = VideoFileClip(input_path)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile("muted_video.mp4")

        video_file = "/content/muted_video.mp4"

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        print(
            f"⏱️ Execution time for video muting: {int(minutes)} minutes and {round(seconds, 2)} seconds")

        return video_file

    def lip_sync(self, muted_video_path, generated_voice_path, target_language):
        # Record the start time
        start_time = time.time()

        gc.collect()

        # Wechsle zum Verzeichnis /content/Wav2Lip-HD
        os.chdir("/content/Wav2Lip-HD")

        target_audio = "/content/Wav2Lip-HD/input_audios"
        target_video = "/content/Wav2Lip-HD/input_videos"

        # Downsample input video to avoid blurry regin around mouth
        # --resize_factor
        # ffmpeg -i input_video.mp4 -vf scale=96:96 output_video.mp4
        import subprocess
        command = (
            f'cp -r "{generated_voice_path}" "{target_audio}"; '
            f'cp -r "{muted_video_path}" "{target_video}"; '
        )
        subprocess.run(command, shell=True, capture_output=True, text=True)

        print("Lip synchronization is loading ...")
        # Baue den Befehl als Zeichenkette

        c = "pip install -qq librosa==0.8.0"
        c1 = "pip install -qq numpy==1.22.0"
        os.system(c)
        os.system(c1)
        # subprocess.run(c, shell=True, capture_output=True, text=True)
        # subprocess.run(c1, shell=True, capture_output=True, text=True)

        # Setze die Pfade entsprechend
        checkpoint_path = "checkpoints/wav2lip_gan.pth"
        segment_path = "checkpoints/face_segmentation.pth"
        sr_p = "checkpoints/esrgan_yunying.pth"
        face_video_path = "input_videos/muted_video.mp4"
        audio_path = "input_audios/generated_voice.wav"
        gt_p = "data/gt"
        pred_p = "data/lq"
        outfile_path = "output_videos_wav2lip/final_dubbed_video.mp4"

        # Baue den Befehl zusammen
        command = (f"cd /content/Wav2Lip-HD && python inference.py "
                   f"--checkpoint_path {checkpoint_path} "
                   f"--face {face_video_path} "
                   f"--audio {audio_path} "
                   "--pads 0 20 0 0 "
                   f"--outfile {outfile_path} "
                   f"--segmentation_path {segment_path} "
                   f"--sr_path {sr_p} "
                   "--save_frames "
                   # f"--gt_path {gt_p}"
                   # f"--pred_path {pred_p} "
                   "--resize_factor 2 "
                   "--no_sr "
                   "--no_segmentation "
                   "--nosmooth ")

        # Führe den Befehl aus
        os.system(command)

        # Baue den Befehl als Zeichenkette
        command2 = (
            'python video2frames.py '
            '--input_video "output_videos_wav2lip/final_dubbed_video.mp4" '
            '--frames_path "frames_wav2lip/muted_video"'
        )

        # Führe den Befehl in der Shell aus
        os.system(command2)

        synced_video_path = "/content/Wav2Lip-HD/output_videos_wav2lip/final_dubbed_video.mp4"

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        print("Frames have been created and can be found under /content/Wav2Lip-HD/frames_wav2lip")
        print("✅ Lip synchronization has been performed")
        print(
            f"⏱️ Execution time for lip syncing: {int(minutes)} minutes and {round(seconds, 2)} "
            f"seconds for language: {target_language}")

        return synced_video_path

    def setup_environment(self):
        # Record the start time
        start_time = time.time()

        os.chdir("/content/Wav2Lip-HD")
        command = (
            'pip uninstall -qq -y -r requirements.txt '
            'pip uninstall -qq -y librosa==0.8.1 '
        )

        # Führe den Befehl in der Shell aus
        os.system(command)

        os.chdir("/content/Real-ESRGAN")

        # Set up the environment
        command2 = (
            'pip install -qq basicsr '
            'pip install -qq facexlib '
            'pip install -qq gfpgan '
            'pip install -qq -r requirements.txt '
            'python setup.py develop '
        )
        os.system(command2)

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        print("✅ Environment is set!")
        print(f"⏱️ Execution time for environment setting: {int(minutes)} minutes and {round(seconds, 2)} seconds")

    def increase_lip_sync_quality(self):
        # Record the start time
        start_time = time.time()

        os.chdir("/content/Real-ESRGAN")

        # creating a subfolder "upload"
        command = "mkdir upload"
        os.system(command)
        # copy all the generated frames from wav2lip into the upload folder from Real-ESRGAN
        command2 = "cp -r /content/Wav2Lip-HD/frames_wav2lip/muted_video/* /content/Real-ESRGAN/upload/"
        os.system(command2)
        # enhance each frame
        command3 = "python inference_realesrgan.py -n RealESRGAN_x4plus -i upload --outscale 3.5 --face_enhance"
        os.system(command3)
        # copy audio file into results folder from Real-ESRGAN
        command4 = "cp -r /content/generated_voice.wav /content/Real-ESRGAN/results/"
        os.system(command4)

        os.chdir("/content/Real-ESRGAN/results")

        # combine all of the frames and the audio file to macke the enhanced video
        command5 = ("ffmpeg -r 30 -i frame_%05d_out.jpg -i generated_voice.wav "
                    "-vcodec libx264 -crf 25 -preset veryslow -acodec copy final_dubbed_video_HD.mkv")
        os.system(command5)

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        print("✅ Quality increasing is done! \nThe final HD video can be found under "
              "/content/generated_voice.wav /content/Real-ESRGAN/results/final_dubbed_video_HD.mkv")
        print(f"⏱️ Execution time quality increasing: {int(minutes)} minutes and {round(seconds, 2)} seconds")

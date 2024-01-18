import time
# Import the moviepy.editor library as mp
import moviepy.editor as mp
# Import the whisper library
import whisper


class SpeechToText:

    def __init__(self):
        pass

    def extract_audio(self, video_path):
        '''
        Extracting the audio from a video file using *moviepy*
        :return:
        '''

        # Record the start time
        start_time = time.time()

        # Load the video file using moviepy
        video = mp.VideoFileClip(video_path)

        # Extract the audio from the video
        audio = video.audio

        # Write the extracted audio to an MP3 file
        audio.write_audiofile('/content/extracted_audio.mp3')

        # Specify the path to the extracted audio file
        extracted_audio = '/content/extracted_audio.mp3'

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        print("✅ The audio was extracted from the video")
        print(f"⏱️ Execution time for audio extraction: {int(minutes)} minutes and {round(seconds, 2)} seconds")

        # Return the path to the extracted audio file
        return extracted_audio

    def speech_to_text(self, audio_path):
        '''
        Speech To Text (S2TT)
        Transcribing extracted audio into text using *OpenAI whisper*
        :return:
        '''
        # Record the start time
        start_time = time.time()

        # Load the pre-trained whisper model ("medium" level is used in this example)
        model = whisper.load_model("medium")  # this model has different "levels" and large is the best one

        # Set decoding options, for example, specifying the language as German
        options = {
            "language": "de"}  # set German language as decode option, "task": "translate" only translates in English

        # Transcribe the audio using the loaded model and decoding options
        result = model.transcribe(audio_path, **options)

        # Extract the transcribed text from the result
        transcribtion = result["text"]

        # Print the transcribed text to the console
        # print("Transcribtion: " + transcribtion)

        # Write the transcribed text to a text file
        with open("/content/audio_transcription.txt", "w") as txt:
            txt.write(result["text"])

        # Specify the path to the text file containing the transcribed text
        text_path = "/content/audio_transcription.txt"

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        print("✅ The spoken words were transcribed from the audio ")
        print(f"⏱️ Execution time for STT: {int(minutes)} minutes and {round(seconds, 2)} seconds")
        # Return the transcribed text and the path to the text file
        return transcribtion, text_path

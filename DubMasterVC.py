import time
import sys

sys.path.append('/content/DeepFilterNet')
from df.enhance import enhance, init_df, load_audio, save_audio
# Converting mp3-file into a wav-file
from pydub import AudioSegment
from TTS.api import TTS


class VoiceCloning:

    def __init__(self):
        pass

    def voice_cloning(self, translated_text, mp3_file_path, target_language):
        '''
        Perform voice cloning by converting translated text to speech with a cloned voice.
        :param translated_text: Text translated into the target language
        :param mp3_file_path: Path to the original MP3 audio file
        :param target_language: Target language for voice cloning
        :return: Path to the generated cloned voice audio file
        '''

        # Record the start time for performance measurement
        start_time = time.time()

        # 1. Convert mp3 to wav file
        wav_audio = AudioSegment.from_mp3(mp3_file_path)

        # Export the audio to WAV format
        wav_file = "/content/extracted_audio.wav"
        wav_audio.export(wav_file, format="wav")

        # 2. Remove noise from audio

        # Load default model for noise removal
        model, df_state, _ = init_df()
        # Download and open the audio file.
        audio, _ = load_audio(wav_file, sr=df_state.sr())
        # Denoise the audio
        enhanced = enhance(model, df_state, audio)
        # Save for listening
        wav_file_enhanced = "/content/enhanced_audio.wav"
        save_audio(wav_file_enhanced, enhanced, df_state.sr())

        # 3. Voice cloning
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=True)

        lang = ""
        # Here you can add other languages. If you e.g. added Spanish in the Gradio Dropdown menu,
        # then you have to extend this list like this:
        # elif target_language == "Spanish":
        #   lang = "es"
        if target_language == "Turkish":
            lang = "tr"
        elif target_language == "Hindi":
            lang = "hi"
        elif target_language == "English":
            lang = "en"

        # Generate speech by cloning a voice using default settings
        tts.tts_to_file(
            text=translated_text,
            file_path="/content/generated_voice.wav",
            speaker_wav=wav_file_enhanced,
            language=lang)

        target_path = "/content/generated_voice.wav"

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time for voice cloning
        elapsed_time = end_time - start_time

        # Convert elapsed time to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        # Display completion message with execution time
        print("✅ The voice was cloned")
        print(
            f"⏱️ Execution time for voice cloning: {int(minutes)} minutes and {round(seconds, 2)} "
            f"seconds for language: {target_language}")

        return target_path

from DubMasterSTT import SpeechToText
from DubMasterTTT import TextToText
from DubMasterVC import VoiceCloning
from DubMasterLipSync import LipSynchronization


class TranslationPipeline:

    def __init__(self):
        pass

    def pipeline(self, video_file, target_language):
        '''
        Translation Pipeline with web application
        :param video_file: Input video file path
        :param target_language: Target language for translation
        :return: Path to the final synchronized video
        '''

        # Creating instances of the pipeline elements
        sst = SpeechToText()  # Instance for SpeechToText module
        ttt = TextToText()  # Instance for TextToText module
        vc = VoiceCloning()  # Instance for VoiceCloning module
        ls = LipSynchronization()  # Instance for LipSynchronization module

        # Extract audio from the video
        extracted_audio = sst.extract_audio(video_file)

        # Transcribe the audio to get the original text
        transcribed_text, text_path = sst.speech_to_text(extracted_audio)

        # Translating the transcribed text based on the chosen language
        translated_text, translated_text_path = ttt.text_to_text(text_path, tgt_lang=target_language)

        # Voice cloning component
        mp3_file_path = '/content/extracted_audio.mp3'
        filepath_cloned_voice = vc.voice_cloning(translated_text, mp3_file_path, target_language)

        # Lipsyncing component
        muted_video_path = ls.mute_video(video_file)
        synced_video_path = ls.lip_sync(muted_video_path, filepath_cloned_voice, target_language)

        # Printing completion message
        print("🩷🎤Dubbing is completed. Please look at the output window of the gradio app.")

        # Returning the path to the final synchronized video
        return synced_video_path

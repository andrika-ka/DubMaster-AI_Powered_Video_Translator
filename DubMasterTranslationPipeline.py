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
        :param target_language:
        :return:
        '''

        sst = SpeechToText()
        ttt = TextToText()
        vc = VoiceCloning()
        ls = LipSynchronization()

        # Extract audio from the video
        extracted_audio = sst.extract_audio(video_file)

        # Transcribe the audio to get the original text
        transcribed_text, text_path = sst.speech_to_text(extracted_audio)

        # Translating the transcribed text based on the chosen language
        # target languages (English:eng, Turkish:tur, Hindi:hin, Macedonian:mkd)
        translated_text, translated_text_path = ttt.text_to_text(text_path, tgt_lang=target_language)

        # Voice cloning
        mp3_file_path = '/content/extracted_audio.mp3'
        filepath_cloned_voice = vc.voice_cloning_final(translated_text, mp3_file_path, target_language)

        # lip syncing
        muted_video_path = ls.mute_video(video_file)
        synced_video_path = ls.lip_sync(muted_video_path, filepath_cloned_voice, target_language)

        print("🩷🎤Dubbing is completed. Please look at the output window of the gradio app.")

        return synced_video_path

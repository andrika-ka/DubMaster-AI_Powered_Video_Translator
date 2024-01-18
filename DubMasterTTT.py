import time
# Import necessary libraries
from deep_translator import GoogleTranslator


class TextToText:

    def __init__(self):
        pass

    def text_to_text(self, text_input, tgt_lang):  # Google Translator
        '''
        Translating the text into text in another language using Google Translator
        :param text_input: Path to the input text file for translation
        :param tgt_lang: Target language for translation
        :return: Tuple containing translated text and the path to the translated text file
        '''

        # Record the start time for performance measurement
        start_time = time.time()

        # Open the file in read mode
        with open(text_input, 'r') as file:
            # Read the content of the file
            text_content = file.read()

        # Mapping target language to language code for Google Translator
        target_lang = ''
        if tgt_lang == 'Turkish':
            target_lang = 'tr'
        elif tgt_lang == 'Hindi':
            target_lang = 'hi'
        elif tgt_lang == 'English':
            target_lang = 'en'

        # Initialize the GoogleTranslator with auto-detection of source language
        translator = GoogleTranslator(source='auto', target=target_lang)

        # Translate the text using Google Translator
        translated_text = translator.translate(text_content)

        # Display the translated text
        print("Translated Text: " + translated_text)

        # Create a new txt file with the translated text
        with open("/content/translated_transcription.txt", "w") as txt:
            txt.write(translated_text)

        # Specify the path to the text file containing the translated text
        translated_text_path = "/content/translated_transcription.txt"

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time for translation
        elapsed_time = end_time - start_time

        # Convert elapsed time to minutes and seconds
        minutes, seconds = divmod(elapsed_time, 60)

        # Display completion message with execution time
        print("✅ The transcription was translated into the target language")

        print(
            f"⏱️ Execution time for text translation: {int(minutes)} minutes and {round(seconds, 2)} "
            f"seconds for language: {tgt_lang}")

        # Return the translated text and the path to the text file
        return translated_text, translated_text_path

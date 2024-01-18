from DubMasterTranslationPipeline import TranslationPipeline


class WebApplication:

    def __init__(self):
        pass

    def show_welcome_page(self):
        '''
        Display the welcome page for DubMaster, prompting the user to agree to the terms.
        :return: True if the user agrees, False otherwise
        '''

        welcome_text = """
           Willkommen bei DubMaster.
           Bitte lesen Sie die Nutzungsbedingungen und tippen Sie 'Verstanden' in das untere Feld ein, um fortzufahren.
           """

        # Prompt the user to input 'Verstanden' to proceed
        user_input = input(welcome_text + "\nGeben Sie 'Verstanden' ein: ")

        # Return True if the user input is 'Verstanden', otherwise return False
        return user_input.lower() == 'verstanden'

    def create_web_application(self):
        '''
        Create and launch the DubMaster web application using Gradio.
        '''

        # Create an instance of the TranslationPipeline
        translation_pipeline = TranslationPipeline()

        # Display the welcome page and proceed only if the user agrees
        if not self.show_welcome_page():
            print("Sie haben die Zustimmung nicht erteilt. Die Anwendung wird beendet.")
            return

        # Creating a Gradio Interface
        import gradio as gr
        iface = gr.Interface(
            fn=translation_pipeline.pipeline,
            inputs=[gr.Video(label="Video hochladen"),
                    gr.Dropdown(["Turkish", "Hindi", "English"], label="Zielsprache")],
            outputs=gr.Video(label="Übersetztes Video"),
        )

        # Launch the Gradio Interface
        iface.launch(inbrowser=True, show_error=True, debug=True)

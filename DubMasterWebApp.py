from DubMasterTranslationPipeline import TranslationPipeline


class WebApplication:

    def __init__(self):
        pass

    def show_welcome_page(self):
        welcome_text = """
        Willkommen bei DubMaster.
        Bitte lesen Sie die Nutzungsbedingungen und tippen Sie 'Verstanden' in das untere Feld ein, um fortzufahren.
        """

        user_input = input(welcome_text + "\nGeben Sie 'Verstanden' ein: ")
        return user_input.lower() == 'verstanden'

    def create_web_application(self):
        '''

        :return:
        '''

        translation_pipeline = TranslationPipeline()

        # Willkommensseite anzeigen und nur fortfahren, wenn der Benutzer 'Verstanden' eingegeben hat
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

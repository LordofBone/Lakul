from .functions.run_speech_inference import SpeechInferencer
from .functions.speech_input import listen

import logging

logger = logging.getLogger(__name__)
logger.debug("Initialized")


def main():
    logging.basicConfig(level="DEBUG")
    SpeechtoTextTest = SpeechtoTextHandler()
    SpeechtoTextTest.initiate_recording()
    print(SpeechtoTextTest.run_inference())


class SpeechtoTextHandler:
    def __init__(self):
        """
        Initialize the speech to text handler with current state.
        """
        self.listening = False
        self.inferencing = False

    def initiate_recording(self, seconds=6):
        """
        Initiate recording.
        :return:
        """
        self.listening = True
        listen(seconds)

        self.listening = False

    def run_inference(self):
        """
        Run speech inference.
        :return:
        """
        self.inferencing = True

        text_output = SpeechInferencer.run_stt()

        self.inferencing = False

        return text_output

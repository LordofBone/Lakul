import logging

from .functions.run_speech_inference import SpeechInferencer
from .functions.speech_input import AudioRecorder

logger = logging.getLogger(__name__)
logger.debug("Initialized")


def main():
    logging.basicConfig(level="DEBUG")
    SpeechtoTextTest = SpeechtoTextHandler()
    SpeechtoTextTest.initiate_recording()
    print(SpeechtoTextTest.run_inference())


class SpeechtoTextHandler:
    def __init__(self, microphone_name="Microphone"):
        """
        Initialize the speech to text handler with current state.
        """
        self.listening = False
        self.inferencing = False
        self.recorder = AudioRecorder(microphone_name=microphone_name)  # Initialize the AudioRecorder

    def initiate_recording(self, max_seconds=60, silence_threshold=100, silence_duration=200):
        """
        Initiate recording.
        :return:
        """
        self.listening = True
        # Use the recorder's listen method
        self.recorder.listen(max_seconds, silence_threshold, silence_duration)

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

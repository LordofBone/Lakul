import whisper

from config.whisper_config import *

import logging

root_dir = Path(__file__).parent

logger = logging.getLogger("inferencing")


class SpeechInference(object):
    def __init__(self):
        """
        Initialize the speech inference class.
        """
        self.model = whisper.load_model(model_size)

    def run_stt(self):
        """
        Run speech inference.
        :return:
        """
        logger.debug("Started Inferencing")

        result = self.model.transcribe(audio_file)
        return result["text"]


SpeechInferencer = SpeechInference()

if __name__ == "__main__":
    print(SpeechInferencer.run_stt())

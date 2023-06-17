import whisper
import openai

from config.whisper_config import *

import logging

root_dir = Path(__file__).parent

logger = logging.getLogger("inferencing")


class SpeechInference(object):
    def __init__(self):
        """
        Initialize the speech inference class.
        """
        self.offline_mode = offline_mode
        self.model = whisper.load_model(model_size)

    def run_stt(self):
        """
        Run speech inference.
        :return:
        """
        if self.offline_mode:
            logger.debug("Started Inferencing using Offline method")

            result = self.model.transcribe(audio_file)
            return result["text"]
        else:
            file = open(audio_file, "rb")
            transcription = openai.Audio.transcribe("whisper-1", file)

            return transcription


SpeechInferencer = SpeechInference()

if __name__ == "__main__":
    print(SpeechInferencer.run_stt())

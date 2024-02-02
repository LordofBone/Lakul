import logging
from pathlib import Path

import openai
import whisper

root_dir = Path(__file__).parent

# Initialize logger with the given name
logger = logging.getLogger(__name__)


class SpeechInference:
    def __init__(self, audio_file, offline_mode, model_size, api_key, init_on_launch=True):
        """
        Initialize the speech inference class.
        """

        self.audio_file = audio_file

        self.offline_mode = offline_mode

        # this is for code calling this to have the option to not initialize the STT model until later or on init of
        # the class
        if init_on_launch:
            self.init_models()

    def init_models(self):
        """
        Initialize the models.
        :return:
        """
        if self.offline_mode:
            logger.debug("Initializing Speech Inference model")
            self.model = whisper.load_model(self.model_size)
            logger.debug("Initialized Speech Inference model")
        else:
            logger.debug("Initializing OpenAI API")
            openai.api_key = self.api_key
            logger.debug("Initialized OpenAI API")

    def run_stt(self):
        """
        Run speech inference.
        :return:
        """
        logger.debug(f"Started running speech inference, offline_mode: {self.offline_mode}, file: {self.audio_file}")

        if self.offline_mode:
            result = self.model.transcribe(str(self.audio_file))
        else:
            file = open(self.audio_file, "rb")
            result = transcription = openai.Audio.transcribe("whisper-1", file)

        logger.debug(f"Completed running speech inference, output: {result['text']}")

        return result["text"]

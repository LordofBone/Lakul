import logging
from pathlib import Path

import whisper
from openai import OpenAI

root_dir = Path(__file__).parent

# Initialize logger with the given name
logger = logging.getLogger(__name__)


class SpeechInference:
    def __init__(self, audio_file, offline_mode, model_size, api_key):
        """
        Initialize the speech inference class.
        """
        self.client = None

        self.audio_file = audio_file

        self.offline_mode = offline_mode

        self.model = None

        self.model_size = model_size

        self.api_key = api_key

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
            self.client = OpenAI(
                api_key=self.api_key,
            )
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
            result = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=file,
                response_format="text",
            )

        logger.debug(f"Completed running speech inference, output: {result}")

        return result

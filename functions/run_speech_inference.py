import logging
from pathlib import Path

import openai
import whisper

root_dir = Path(__file__).parent

# Initialize logger with the given name
logger = logging.getLogger(__name__)


class SpeechInference:
    def __init__(self, audio_file, offline_mode, model_size, api_key):
        """
        Initialize the speech inference class.
        """

        self.audio_file = audio_file

        self.offline_mode = offline_mode

        if self.offline_mode:
            logger.debug("Initializing Speech Inference model")
            self.model = whisper.load_model(model_size)
            logger.debug("Initialized Speech Inference model")
        else:
            logger.debug("Initializing OpenAI API")
            openai.api_key = api_key
            logger.debug("Initialized OpenAI API")

        logger.debug("Initialized")

    def run_stt(self):
        """
        Run speech inference.
        :return:
        """
        logger.debug(f"Started running speech inference, offline_mode: {self.offline_mode} file: {self.audio_file}")

        if self.offline_mode:
            result = self.model.transcribe(str(self.audio_file))
        else:
            file = open(self.audio_file, "rb")
            result = transcription = openai.Audio.transcribe("whisper-1", file)

        logger.debug(f"Completed running speech inference, output: {result['text']}")

        return result["text"]

import logging

from .components.openai_api_key import openai_api_key
from .components.run_speech_inference import SpeechInference
from .components.speech_input import AudioRecorder
from .config.whisper_config import (offline_mode, model_size, microphone_name, audio_file,
                                    find_high_quality_audio)

logger = logging.getLogger(__name__)


class SpeechtoTextHandler:
    def __init__(self, stt_microphone_name=microphone_name, stt_audio_file=audio_file, stt_offline_mode=offline_mode,
                 stt_model_size=model_size, stt_api_key=openai_api_key, init_on_launch=True, custom_name=""):
        """
        Initialize the speech to text handler with current state.
        """
        self.custom_name = custom_name
        self.mode = "Offline" if stt_offline_mode else "Online"

        self.listening = False
        self.inferencing = False
        self.recorder = AudioRecorder(microphone_name=stt_microphone_name, audio_file=stt_audio_file,
                                      highest_quality=find_high_quality_audio)
        self.inferencer = SpeechInference(audio_file=stt_audio_file, offline_mode=stt_offline_mode,
                                          model_size=stt_model_size, api_key=stt_api_key)

        # this is for code calling this to have the option to not initialize the STT model until later or on init of
        # the class
        if init_on_launch:
            self.init_models()

        logger.debug(f"{self.__class__.__name__} ({self.custom_name}) initialized in {self.mode} mode.")

    def init_models(self):
        """
        Initialize the models.
        :return:
        """
        self.inferencer.init_models()

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

        text_output = self.inferencer.run_stt()

        self.inferencing = False

        return text_output

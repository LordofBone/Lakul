import logging

from .config.whisper_config import (offline_mode, model_size, microphone_name, api_key, audio_file,
                                    find_high_quality_audio)
from .functions.run_speech_inference import SpeechInference
from .functions.speech_input import AudioRecorder

logger = logging.getLogger(__name__)


class SpeechtoTextHandler:
    def __init__(self, stt_microphone_name=microphone_name, stt_audio_file=audio_file, stt_offline_mode=offline_mode,
                 stt_model_size=model_size, stt_api_key=api_key, init_on_launch=find_high_quality_audio):
        """
        Initialize the speech to text handler with current state.
        """
        self.listening = False
        self.inferencing = False
        self.recorder = AudioRecorder(microphone_name=stt_microphone_name, audio_file=stt_audio_file,
                                      highest_quality=True)
        self.inferencer = SpeechInference(audio_file=stt_audio_file, offline_mode=stt_offline_mode,
                                          model_size=stt_model_size, api_key=stt_api_key)

        # this is for code calling this to have the option to not initialize the STT model until later or on init of
        # the class
        if init_on_launch:
            self.init_models()

        logger.debug("Initialized")

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

import logging

from .config.whisper_config import offline_mode, model_size, microphone_name, api_key, audio_file
from .functions.run_speech_inference import SpeechInference
from .functions.speech_input import AudioRecorder

logger = logging.getLogger(__name__)


class SpeechtoTextHandler:
    def __init__(self, stt_microphone_name=microphone_name, stt_audio_file=audio_file, stt_offline_mode=offline_mode,
                 stt_model_size=model_size, stt_api_key=api_key):
        """
        Initialize the speech to text handler with current state.
        """
        self.listening = False
        self.inferencing = False
        self.recorder = AudioRecorder(microphone_name=stt_microphone_name, audio_file=stt_audio_file)
        self.inferencer = SpeechInference(audio_file=stt_audio_file, offline_mode=stt_offline_mode,
                                          model_size=stt_model_size, api_key=stt_api_key)

        logger.debug("Initialized")

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

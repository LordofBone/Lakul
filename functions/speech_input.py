import logging
import wave

import numpy as np
import pyaudio

# Initialize logger with the given name
logger = logging.getLogger(__name__)


class AudioRecorder:
    def __init__(self, microphone_name, audio_file):
        self.p = pyaudio.PyAudio()
        self.microphone_name = microphone_name
        self.input_device = self.find_usb_microphone_device()
        self.sample_rates = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 176400, 192000, 384000]
        self.chunk_sizes = [128, 256, 512, 1024, 2048]

        self.RATE = self.find_compatible_sample_rate()
        self.CHUNK = self.find_compatible_chunk_size()

        self.audio_file = audio_file

        logger.debug("Initialized")

    def find_usb_microphone_device(self):
        # List all audio devices
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            logger.debug(f"Device index: {info['index']} - {info['name']}")

            # Check if the device name contains the microphone name
            if self.microphone_name in info['name']:
                logger.debug(f"{self.microphone_name} at index: {info['index']}")
                return info['index']

        # If the device was not found
        logger.debug(f"{self.microphone_name} not found")
        raise Exception(f"{self.microphone_name} not found, please ensure it is plugged in.")

    def find_compatible_sample_rate(self):
        # Check for supported sample rates
        for rate in self.sample_rates:
            try:
                is_supported = self.p.is_format_supported(rate,
                                                          input_device=self.input_device,
                                                          input_channels=1,
                                                          input_format=pyaudio.paInt16)
                logger.debug(f"  Sample rate {rate} is supported: {is_supported}")
                return rate
            except ValueError as err:
                logger.debug(f"  Sample rate {rate} is NOT supported: {err}")

    # Check for supported chunk sizes
    def find_compatible_chunk_size(self):
        for chunk_size in self.chunk_sizes:
            try:
                # Attempt to open a stream with the given chunk size
                # If this fails, it will throw an exception which is caught in the except block
                stream = self.p.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=self.RATE,  # Use the rate determined previously
                                     input=True,
                                     frames_per_buffer=chunk_size,
                                     input_device_index=self.input_device)

                # If we reach this line, the chunk size is supported. Close the stream and return the chunk size.
                stream.close()
                logger.debug(f"  Chunk size {chunk_size} is supported.")
                return chunk_size
            except Exception as err:
                # This chunk size is not supported. Continue checking the next one.
                logger.debug(f"  Chunk size {chunk_size} is NOT supported: {err}")

    def rms(self, data):
        """Calculate root mean square of data."""
        count = len(data) / 2
        format = "%dh" % (count)
        shorts = np.frombuffer(data, dtype=np.int16).astype(np.int32)  # Convert to int32
        squared = shorts ** 2
        if np.isnan(squared).any() or np.isinf(squared).any():
            logger.warning("NaN or Inf values detected in squared audio data.")
            squared = np.nan_to_num(squared)  # Replace NaN or Inf with 0
        return np.sqrt(np.mean(squared))

    def listen(self, max_seconds, silence_threshold, silence_duration):
        """
        Listen to the microphone and save the recorded sound.
        Stops recording after silence_duration seconds of silence or after max_seconds.
        """
        logger.debug("Listening")

        frames = []
        silence_frames = 0
        total_frames = 0

        stream = self.p.open(format=pyaudio.paInt16,
                             channels=1,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK,
                             input_device_index=self.input_device)

        while total_frames < int(self.RATE / self.CHUNK * max_seconds):
            data = stream.read(self.CHUNK, exception_on_overflow=False)

            frames.append(data)

            # Check for silence
            if self.rms(data) < silence_threshold:
                silence_frames += 1
                if silence_frames >= silence_duration:
                    break
            else:
                silence_frames = 0

            total_frames += 1

        stream.stop_stream()
        stream.close()

        logger.debug("Finished listening")

        with wave.open(str(self.audio_file), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

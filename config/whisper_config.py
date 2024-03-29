from pathlib import Path

file_path = Path(__file__).parent.parent / f"audio"

audio_file = str(file_path / "recording.wav")

# available_models = ["tiny", "base", "small", "medium", "large"]
model_size = "base"

microphone_name = "Microphone"

offline_mode = True

find_high_quality_audio = True

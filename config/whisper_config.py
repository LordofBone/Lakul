from pathlib import Path

file_path = Path(__file__).parent.parent / f"audio"

audio_file = str(file_path / "recording.wav")

# available_models = ["tiny", "base", "small", "medium", "large"]
model_size = "base"

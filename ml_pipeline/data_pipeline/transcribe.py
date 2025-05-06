import whisper
import tempfile

# Load the Whisper model once at import time
model = whisper.load_model("small")

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribes audio from a bytes object using Whisper.

    Args:
        audio_bytes (bytes): Raw audio bytes from S3 (e.g., from BytesIO.read())

    Returns:
        str: Transcribed text
    """
    # Whisper requires a file path, so we temporarily write the bytes
    with tempfile.NamedTemporaryFile(suffix=".flac") as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        result = model.transcribe(tmp.name)
        return result["text"]
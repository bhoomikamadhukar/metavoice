from prefect import flow, task, wait_for
import soundfile as sf

from data_pipeline.config import BUCKET_NAME
from data_pipeline.load_data import get_s3_client, list_audio_files, fetch_audio_stream
from data_pipeline.transcribe import transcribe_audio
from data_pipeline.tokenizer import tokenise
from data_pipeline.orchestrator import save_outputs

@task
def get_keys():
    client = get_s3_client()
    return list_audio_files(client)

@task
def process(key):
    client = get_s3_client()
    print(f"Processing: {key}")
    stream = fetch_audio_stream(client, key)
    audio_np, sr = sf.read(stream)
    stream.seek(0)
    transcription = transcribe_audio(stream.read())
    tokens = tokenise(audio_np)
    return {
        "id": key,
        "duration_sec": len(audio_np) / sr,
        "sampling_rate": sr,
        "transcription": transcription,
        "tokens": tokens
    }

@flow(name="metavoice-pipeline")
def main():
    keys = get_keys()
    results = [process.submit(key) for key in keys]
    completed = wait_for(results)
    save_outputs([r.result() for r in completed])

if __name__ == "__main__":
    main()
# Metavoice

This project builds a GPU-accelerated data pipeline using Prefect for orchestrating the transcription and tokenization of .flac audio files stored in Cloudflare R2 (S3-compatible object storage). The final output includes transcriptions, duration, sampling rate, and tokenized audio representations stored in Parquet format for downstream analysis.



## Features

	•	Fetches .flac audio files from Cloudflare R2 (S3-compatible).
	•	Uses OpenAI Whisper for transcription.
	•   Tokenizes audio using a synthetic GPU-bound tokenizer (simulates load).
	•	Saves structured data to Parquet format for analytics.
	•	Generates a summary.json for quick insights.
	•	Modular, GPU-enabled, and horizontally scalable via Prefect.

##  Installation & Setup

1. Clone this repo - https://github.com/bhoomikamadhukar/metavoice.git
2. cd ml_pipeline

2. Install dependencies. Use a GPU-supported environment (e.g., Google Colab or local CUDA setup) (I personally used colab because Mac and CUDA dont get along.)
3. pip install -r requirements.txt to get all the requirements. 
4. Ensure you have ffmpeg installed for Whisper to work: apt-get update && apt-get install -y ffmpeg


## Project structure
ml_pipeline/
├── config.py                   # Environment config (keys, endpoints, paths)
├── load_data.py               # S3 client, list and fetch audio
├── transcribe.py              # Whisper-based transcription
├── tokenizer.py               # GPU token generation
├── orchestrator.py            # Save outputs to parquet and summary
├── prefect_pipeline.py        # Prefect pipeline entry point
├── data/
│   ├── metavoice_output.parquet
│   └── summary.json

#### Run the pipeline 
python ml_pipeline/prefect_pipeline.py

## Output Schema Explained
The output is saved in a .parquet file and contains the following columns:

id:	The object key of the audio file in S3
duration_sec:	Duration of the audio in seconds
sampling_rate:	Audio sampling rate (Hz), usually 48k or 16k
transcription:	Transcribed text from the audio via Whisper
tokens:	Tokenized representation of the audio (int16)
## Why?
transcription: Needed for any NLP, search, or captioning tasks.
duration_sec + sampling_rate: Crucial metadata for playback validation, audio quality checks, and downstream signal processing.
tokens: Abstracted GPU-heavy token sequence mimicking embeddings or other tokenized features, suitable for vector storage or ML models.

This schema balances textual output (transcription) with numerical features (duration, sampling, tokens) and supports various downstream applications — from speech search to large-scale modeling.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Horizontal Scalability

This pipeline is horizontally scalable due to:
	•	Task-level parallelism via Prefect’s .submit() method.
	•	Each audio file is processed independently — making it ideal for:
	•	Distributed task queues
	•	Serverless execution
	•	GPU-based containers
	•	Integration with Prefect Cloud or Dask allows dynamic worker pools to process thousands of files in parallel with autoscaling.

This design ensures minimal bottlenecks and supports massive scale across CPUs and GPUs.






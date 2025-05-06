# ️ Metavoice

This project builds a **GPU-accelerated data pipeline** using [Prefect](https://www.prefect.io/) for orchestrating the transcription and tokenization of `.flac` audio files stored in **Cloudflare R2** (S3-compatible object storage). The final output includes **transcriptions**, **audio metadata**, and **tokenized representations**, all saved in **Parquet** format for downstream analysis.

---

## Features

- Fetches `.flac` audio files from Cloudflare R2
- Uses OpenAI Whisper for transcription
- Tokenizes audio using a synthetic GPU-bound tokenizer (simulated load)
- Saves structured output to `.parquet` format
- Generates a `summary.json` with audio and transcription insights
- Modular, GPU-enabled, and horizontally scalable using Prefect

---

##  Installation & Setup

1. **Clone this repo**
   ```bash
   git clone https://github.com/bhoomikamadhukar/metavoice.git
   cd metavoice/ml_pipeline
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ffmpeg** (required by Whisper)
   ```bash
   sudo apt-get update && sudo apt-get install -y ffmpeg
   ```

4. **(Recommended)** Use a **GPU-supported environment** like:
   - Google Colab (tested here since it was tedious to get cuda on mac.)
   - CUDA-enabled local machine (Linux/Windows)
   - Docker with GPU runtime (NVIDIA)

---

## Project Structure

```
ml_pipeline/
├── config.py               # API keys, endpoints, output paths
├── load_data.py           # S3 client, list and fetch logic
├── transcribe.py          # Whisper-based transcription
├── tokenizer.py           # Synthetic GPU token generation
├── orchestrator.py        # Output saving and summary generation
├── prefect_pipeline.py    # Main pipeline entry using Prefect
└── data/
    ├── metavoice_output.parquet
    └── summary.json
```

---

##  Running the Pipeline

```bash
python ml_pipeline/prefect_pipeline.py
```

---

## 📑 Output Schema Explained

| Column         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `id`           | Object key of the audio file in Cloudflare R2                               |
| `duration_sec` | Duration of the audio file in seconds                                       |
| `sampling_rate`| Sampling rate in Hz (typically 48k or 16k)                                  |
| `transcription`| Whisper-generated transcript of the spoken content                         |
| `tokens`       | GPU-simulated token sequence (random `int16` values representing features) |

---

## Why This Schema?

- **`transcription`**: Essential for NLP tasks, search indexing, subtitles, or analytics.
- **`duration_sec` & `sampling_rate`**: Key for validating audio quality, syncing timelines, and preprocessing.
- **`tokens`**: Simulated stand-in for embeddings or audio features — useful for downstream ML or vector databases.

This schema offers a balance of **natural language**, **acoustic metadata**, and **structured embeddings**, enabling everything from search to training speech-aware models.

---

##  Horizontal Scalability

This pipeline is **horizontally scalable** by design:

-  **Task-level parallelism** using Prefect’s `.submit()` for concurrent task execution
-  Each audio file is processed independently (perfect for:
  - Distributed queues (e.g., Celery, Ray, Dask)
  - Serverless workloads
  - GPU/CPU auto-scaling containers
-  Easy integration with **Prefect Cloud**, **Kubernetes**, or **Dask clusters** for high-throughput use cases

> This architecture ensures minimal bottlenecks and linear scalability across thousands of files.

---

## Questions or Feedback?

Open an issue on the [GitHub repository](https://github.com/bhoomikamadhukar/metavoice) or reach out on [LinkedIn](https://linkedin.com/in/bhoomikamadhukar) if you'd like to collaborate or share feedback!

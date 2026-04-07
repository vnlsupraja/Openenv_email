# OpenEnv Email Triage Environment

## Overview
Simulates real-world email triage tasks for AI agents:
- Spam filtering
- Prioritization
- Customer response

## Tasks
1. Easy: Spam classification
2. Medium: Prioritization
3. Hard: Full workflow

## Action Space
- classify
- prioritize
- reply
- archive
- escalate

## Observation Space
- Inbox emails
- Last action result

## Reward Design
- Correct action: +1.0
- Partial: +0.7
- Wrong: -0.3

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)

**Note:** Environment variables are optional. If not provided, the inference script will use a deterministic fallback mode.

Copy `.env.example` to `.env` (optional):

```bash
cp .env.example .env
```

Edit `.env` with your credentials (optional):

```
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
HF_TOKEN=your_actual_api_key_here
```

**Available Variables:**
- `API_BASE_URL`: The API endpoint for your LLM (default: `https://api.openai.com/v1`)
- `MODEL_NAME`: The model identifier (default: `gpt-3.5-turbo`)
- `HF_TOKEN`: Your API key (if empty, deterministic fallback is used)

### 3. Run Baseline Inference

```bash
python inference.py
```

#### Without API Key (Deterministic Fallback)
```bash
# No configuration needed - runs with deterministic fallback
# Results: Easy 1.00, Medium 1.00, Hard 1.00
python inference.py
```

#### With OpenAI API Key
```bash
export API_BASE_URL=https://api.openai.com/v1
export MODEL_NAME=gpt-3.5-turbo
export HF_TOKEN=sk-your-openai-key
python inference.py
```

#### With Hugging Face
```bash
export API_BASE_URL=https://api-inference.huggingface.co/v1
export MODEL_NAME=mistral-7b
export HF_TOKEN=hf_your-hugging-face-token
python inference.py
```

### 4. Run the FastAPI Server

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

Then access the API at `http://localhost:7860`

## Fallback Mode

The environment includes intelligent fallback support:
- **No API Required**: Works out-of-the-box without API credentials
- **Perfect Reproducibility**: Deterministic actions achieve perfect scores
- **Graceful Degradation**: Automatically falls back if API fails
- **Flexible**: Works with any OpenAI-compatible endpoint

See [API_FALLBACK_SOLUTION.md](API_FALLBACK_SOLUTION.md) for more details.
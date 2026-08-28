# Call Summary Agent

An agentic LLM pipeline that extracts structured insights from call transcripts using Google Gemini. Built with FastAPI and a two-step prompt chain that mirrors the Speech Intelligence extraction layer used in real-time communication platforms.

## What it does

Given a raw call transcript, the agent runs a **two-step reasoning chain**:

1. **Step 1 — Extract**: Gemini reads the transcript and pulls out summary, key topics, sentiment, action items, and speaker intent
2. **Step 2 — Validate & Enrich**: A second Gemini call reviews the Step 1 output, catches missed action items, determines if follow-up is required, and assigns a confidence score

All output is returned as **validated, structured JSON** via a FastAPI REST endpoint.

## Output schema

```json
{
  "summary": "string",
  "key_topics": ["string"],
  "sentiment": "positive | neutral | negative",
  "sentiment_reasoning": "string",
  "action_items": [
    { "task": "string", "owner": "string | null", "deadline": "string | null" }
  ],
  "speaker_intents": [{ "speaker": "string", "intent": "string" }],
  "follow_up_required": true,
  "confidence_score": 0.93
}
```

## Project structure

```
call-summary-agent/
├── src/
│   ├── main.py        # FastAPI app + CORS
│   ├── routes.py      # API route handlers
│   ├── llm.py         # Two-step Gemini prompt chain
│   └── schemas.py     # Pydantic request/response models
├── tests/
│   └── test_api.py    # Pytest test suite (mocked LLM calls)
├── samples/
│   └── sample_transcript.txt
├── .env.example
├── requirements.txt
└── README.md
```

## Setup & run locally

```bash
# 1. Clone the repo
git clone https://github.com/lowkeyprisha/call-summary-agent.git
cd call-summary-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Gemini API key
cp .env.example .env
# Open .env and paste your key from https://aistudio.google.com/app/apikey

# 5. Run the server
uvicorn src.main:app --reload
```

Server runs at `http://localhost:8000`  
Interactive API docs at `http://localhost:8000/docs`

## API usage

**POST** `/api/analyze`

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Agent: Hello, how can I help? Customer: I was charged twice this month..."
  }'
```

**GET** `/api/health` — health check

## Run tests

```bash
pytest tests/ -v
```

## Get a free Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com/app/apikey)
2. Sign in with Google → click **Get API key** → **Create API key**
3. Paste it into your `.env` file

## Tech stack

- **FastAPI** — REST API framework
- **Google Gemini 1.5 Flash** — LLM for transcript analysis
- **Pydantic v2** — schema validation on all LLM outputs
- **Pytest** — test suite with mocked LLM calls
- **Uvicorn** — ASGI server

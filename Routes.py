from fastapi import APIRouter, HTTPException
from src.schemas import TranscriptRequest, CallSummaryResponse, ErrorResponse
from src.llm import analyze_transcript
import json

router = APIRouter()

@router.post(
    "/analyze",
    response_model=CallSummaryResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Analyze a call transcript",
    description="Runs a two-step agentic LLM pipeline to extract summary, topics, sentiment, action items, and speaker intent from a raw transcript."
)
async def analyze(request: TranscriptRequest):
    if len(request.transcript.strip()) < 20:
        raise HTTPException(status_code=400, detail="Transcript too short to analyze.")
    try:
        result = analyze_transcript(request.transcript)
        return result
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"LLM returned malformed JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    summary="Health check"
)
def health():
    return {"status": "ok"}
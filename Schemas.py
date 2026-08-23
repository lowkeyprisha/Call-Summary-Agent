from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SentimentEnum(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class TranscriptRequest(BaseModel):
    transcript: str = Field(..., min_length=20, description="Raw call transcript text")
    language: Optional[str] = Field(default="en", description="Language code (default: en)")

class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = None
    deadline: Optional[str] = None

class SpeakerIntent(BaseModel):
    speaker: str
    intent: str

class CallSummaryResponse(BaseModel):
    summary: str
    key_topics: List[str]
    sentiment: SentimentEnum
    sentiment_reasoning: str
    action_items: List[ActionItem]
    speaker_intents: List[SpeakerIntent]
    follow_up_required: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
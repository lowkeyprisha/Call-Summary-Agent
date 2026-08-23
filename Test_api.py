mport pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app
from src.schemas import CallSummaryResponse, SentimentEnum
 
client = TestClient(app)
 
MOCK_RESPONSE = CallSummaryResponse(
    summary="Customer called about a duplicate charge and requested a refund.",
    key_topics=["duplicate charge", "refund", "billing error"],
    sentiment=SentimentEnum.positive,
    sentiment_reasoning="Issue was resolved quickly and customer expressed satisfaction.",
    action_items=[
        {"task": "Process refund of $29.99", "owner": "Agent", "deadline": "3-5 business days"},
        {"task": "Escalate billing bug to engineering", "owner": "Billing team", "deadline": None},
    ],
    speaker_intents=[
        {"speaker": "Customer", "intent": "Report duplicate charge and request refund"},
        {"speaker": "Agent", "intent": "Resolve billing issue and retain customer"},
    ],
    follow_up_required=True,
    confidence_score=0.93
)
 
 
def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
 
 
def test_root():
    response = client.get("/")
    assert response.status_code == 200
 
 
@patch("src.routes.analyze_transcript", return_value=MOCK_RESPONSE)

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
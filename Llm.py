import google.generativeai as genai
import json
import os
import re
from src.schemas import CallSummaryResponse
 
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
 
 
def _clean_json(text: str) -> str:
    """Strip markdown code fences if Gemini wraps output in them."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    return text.strip()


STEP1_PROMPT = """You are an expert call analyst. Read the transcript below and extract:
1. A concise 2-3 sentence summary of what the call was about
2. All key topics discussed (list of short noun phrases)
3. Overall sentiment: positive / neutral / negative, with one-sentence reasoning
4. Every action item mentioned (task, who owns it, any deadline if stated)
5. Each speaker's primary intent in this call
 
Respond ONLY with valid JSON. No preamble, no markdown fences.
 
Schema:
{{
  "summary": "string",
  "key_topics": ["string"],
  "sentiment": "positive|neutral|negative",
  "sentiment_reasoning": "string",
  "action_items": [{{"task": "string", "owner": "string or null", "deadline": "string or null"}}],
  "speaker_intents": [{{"speaker": "string", "intent": "string"}}]
}}
 
TRANSCRIPT:
{transcript}
"""
 
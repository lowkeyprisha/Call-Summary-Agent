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


# ── Step 1: Extract raw facts ────────────────────────────────────────────────
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

# ── Step 2: Validate and enrich ──────────────────────────────────────────────
STEP2_PROMPT = """You are a QA agent reviewing a call analysis JSON.
Given the original transcript and the initial analysis, do the following:
1. Check if any action items were missed — add them
2. Determine if follow-up is required (true/false)
3. Assign a confidence score 0.0–1.0 for how complete the analysis is

Return the COMPLETE updated JSON with two new fields added: "follow_up_required" (bool) and "confidence_score" (float).
Respond ONLY with valid JSON. No preamble, no markdown fences.

ORIGINAL TRANSCRIPT:
{transcript}

INITIAL ANALYSIS:
{initial_analysis}
"""


def analyze_transcript(transcript: str) -> CallSummaryResponse:
    """
    Two-step agentic chain:
      Step 1 — extract raw facts from transcript
      Step 2 — validate, enrich, add follow_up + confidence_score
    """
    # Step 1
    step1_response = model.generate_content(
        STEP1_PROMPT.format(transcript=transcript)
    )
    step1_text = _clean_json(step1_response.text)
    step1_data = json.loads(step1_text)

    # Step 2
    step2_response = model.generate_content(
        STEP2_PROMPT.format(
            transcript=transcript,
            initial_analysis=json.dumps(step1_data, indent=2)
        )
    )
    step2_text = _clean_json(step2_response.text)
    step2_data = json.loads(step2_text)

    return CallSummaryResponse(**step2_data)
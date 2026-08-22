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
 
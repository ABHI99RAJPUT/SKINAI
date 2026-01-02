from typing import Dict, Any, Callable, Optional
import json
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai_api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=genai_api_key)

def build_prompt(profile: Dict[str, Any]) -> str:
    profile_json = json.dumps(profile, indent=2, ensure_ascii=False)

    prompt = textwrap.dedent(f"""
    You are a certified skincare advisor. Use the PROFILE below and produce ONLY valid JSON that fits the schema.

    PROFILE:
    {profile_json}

    INSTRUCTIONS:
    - Output JSON with the following keys:
        "routine": [
            {{ "step": int, "when": "AM"|"PM", "action": str, "notes": str (optional) }}
        ],
        "products": [
            {{ "name": str, "why": str, "key_ingredients": [str,...], "suitable_for": str }}
        ],
        "safety_notes": [str, ...],
        "progress_plan": {{
            "weeks": int,
            "checkpoints": [str,...],
            "photo_schedule": str
        }}

    RULES:
    - Respect sensitivity, allergies, and risk_flags.
    - If acne severity is Severe, include dermatologist guidance.
    - Keep JSON clean, structured, and valid. No extra commentary.
    """).strip()

    return prompt


def gemini_llm_call(prompt: str) -> str:


    model = genai.GenerativeModel("models/gemini-2.5-flash")

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.4,
            "max_output_tokens": 4096
        }
    )

    return response.text

def generate_recommendations(profile: Dict[str, Any], llm_call: Callable[[str], str]) -> Dict[str, Any]:
    prompt = build_prompt(profile)
    raw = llm_call(prompt)

 
    try:
        parsed = json.loads(raw)
        return {"ok": True, "recommendations": parsed}

    except Exception:
        # Recover from markdown formatting or noise
        start = raw.find("{")
        end = raw.rfind("}")
        cleaned = raw[start:end+1]

        try:
            parsed = json.loads(cleaned)
            return {"ok": True, "recommendations": parsed}
        except:
            return {"ok": False, "error": "JSON parse failed", "raw": raw}


def recommend_from_inputs(
    q_profile: Dict[str, Any],
    image_metrics: Dict[str, Any],
    llm_call: Optional[Callable[[str], str]] = None
) -> Dict[str, Any]:

    from questionnaire import combine_profile_with_image_metrics

    if llm_call is None:
        llm_call = gemini_llm_call

    combined = combine_profile_with_image_metrics(q_profile, image_metrics)

    return generate_recommendations(combined, llm_call)
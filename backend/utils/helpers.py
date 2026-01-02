def build_llm_prompt(disease, severity):
    return f"""
You are a medical assistant. The AI model detected:

Disease: {disease}
Severity: {severity}

Provide the following in simple language:
1. What this condition generally is.
2. Home care steps and precautions.
3. What to avoid.
4. When to see a dermatologist.
5. Red-flag symptoms to watch out for.

Avoid medical jargon.
Do NOT prescribe medicines.
Do NOT confirm diagnosis — give general advice only.
"""

from typing import Dict, Any, Tuple, List

ALLOWED = {
    "skin_type": {"Oily","Dry","Combination","Normal"},
    "sensitivity": {"Yes","No"},
    "frequency_of_product_use": {"Daily","Weekly","Occasionally"},
    "sun_exposure": {"Low","Moderate","High"},
    "sleep_quality": {"Good","Average","Poor"},
    "goal": {"Reduce acne","Reduce blackheads","Hydration","Tone correction","Other"},
    "diet_habits": {"High oily food","Balanced","Hydrated"},
}

def validate_questionnaire(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    required = [
        "skin_type",
        "sensitivity",
        "frequency_of_product_use",
        "sun_exposure",
        "sleep_quality",
        "goal",
    ]
    for k in required:
        if k not in data:
            errors.append(f"Missing: {k}")

    for k, allowed in ALLOWED.items():
        if k in data and data[k] not in allowed:
            errors.append(f"Invalid value for {k}")

    if data.get("medication_affecting_skin") == "Yes" and not data.get("medication_text"):
        pass

    return (len(errors) == 0, errors)

def _normalize_routine(routine) -> List[str]:
    if routine is None:
        return []
    if isinstance(routine, str):
        return [r.strip() for r in routine.split(",") if r.strip()]
    if isinstance(routine, list):
        return [str(r).strip() for r in routine if str(r).strip()]
    return []

def questionnaire_to_profile(data: Dict[str, Any]) -> Dict[str, Any]:
    routine = _normalize_routine(data.get("current_skincare_routine"))
    freq_map = {"Daily": 1.0, "Weekly": 0.5, "Occasionally": 0.2}
    sun_map = {"Low": 0.5, "Moderate": 2.0, "High": 5.0}
    diet_map = {"High oily food": "high_oily", "Balanced": "balanced", "Hydrated": "hydrated"}

    profile = {
        "skin_type": data.get("skin_type"),
        "sensitivity": True if data.get("sensitivity") == "Yes" else False,
        "known_allergies": data.get("known_allergies", "") or "",
        "current_skincare_routine": routine,
        "frequency_of_product_use": data.get("frequency_of_product_use"),
        "frequency_score": float(freq_map.get(data.get("frequency_of_product_use"), 0.0)),
        "medication_affecting_skin": True if data.get("medication_affecting_skin") == "Yes" else False,
        "medication_text": data.get("medication_text", "") or "",
        "diet_habits": diet_map.get(data.get("diet_habits"), data.get("diet_habits", "")),
        "sun_exposure_hours": float(data.get("sun_exposure_hours")) if isinstance(data.get("sun_exposure_hours"), (int,float,str)) and str(data.get("sun_exposure_hours")).replace('.','',1).isdigit() else float(sun_map.get(data.get("sun_exposure"), 1.0)),
        "sleep_quality": data.get("sleep_quality"),
        "goal": data.get("goal"),
    }
    return profile

def combine_profile_with_image_metrics(q_profile: Dict[str, Any], image_metrics: Dict[str, Any]) -> Dict[str, Any]:
    combined = dict(q_profile)
    combined["image_metrics"] = image_metrics

    risk_flags = []
    if combined.get("sensitivity"):
        risk_flags.append("sensitive_skin")
    if combined.get("medication_affecting_skin"):
        risk_flags.append("on_medication")
    acne_sev = image_metrics.get("acne", {}).get("acne_severity")
    if acne_sev in ("Moderate","Severe"):
        risk_flags.append("active_acne")
    if image_metrics.get("oiliness", {}).get("oiliness_label") == "High":
        risk_flags.append("oily_skin")
    if image_metrics.get("blackheads", {}).get("blackhead_count", 0) > 20:
        risk_flags.append("many_blackheads")

    combined["risk_flags"] = risk_flags

    summary = (
        f"Skin type: {combined.get('skin_type')}; "
        f"Sensitivity: { 'Yes' if combined.get('sensitivity') else 'No' }; "
        f"Oiliness: { image_metrics.get('oiliness',{}).get('oiliness_label') }; "
        f"Acne: { acne_sev }; "
        f"Blackheads: { image_metrics.get('blackheads',{}).get('blackhead_count') }; "
        f"Goal: { combined.get('goal') }"
    )
    combined["summary"] = summary
    return combined
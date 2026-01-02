def get_severity(confidence: float):
    """
    Convert model confidence → Mild / Moderate / Severe.
    """
    if confidence < 0.50:
        return "Mild"
    elif confidence < 0.75:
        return "Moderate"
    else:
        return "Severe"

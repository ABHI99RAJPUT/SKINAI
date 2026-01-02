import sys
import json

from preprocess import preprocess_image, crop_face_region
from analysis import analyze_image
from questionnaire import questionnaire_to_profile, combine_profile_with_image_metrics
from recommend import recommend_from_inputs


def main():
    # Read JSON from FastAPI (stdin)
    raw = sys.stdin.read()
    data = json.loads(raw)

    image_path = data["image_path"]
    q_data = data["questionnaire"]

    # Load image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Step 1 → Image metrics
    image_metrics = analyze_image(image_bytes)

    # Step 2 → Questionnaire → User profile
    q_profile = questionnaire_to_profile(q_data)

    # Step 3 → Combine both
    combined = combine_profile_with_image_metrics(q_profile, image_metrics)

    # Step 4 → LLM recommended routine
    result = recommend_from_inputs(q_profile, image_metrics)

    # Output JSON to FastAPI
    print(json.dumps(result))


if __name__ == "__main__":
    main()

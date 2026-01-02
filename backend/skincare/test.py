from preprocess import preprocess_image, crop_face_region
from analysis import analyze_image
from questionnaire import questionnaire_to_profile, combine_profile_with_image_metrics
from recommend import recommend_from_inputs

# --------------------------
# 1. Load test image
# --------------------------

# Replace with your test image path
image_path = "test_image.jpg"

with open(image_path, "rb") as f:
    image_bytes = f.read()

# --------------------------
# 2. Run image analysis
# --------------------------
print("Running image analysis...")
image_metrics = analyze_image(image_bytes)
print("Image metrics:")
print(image_metrics)

# --------------------------
# 3. Sample questionnaire data
# --------------------------
sample_questionnaire = {
    "skin_type": "Oily",
    "sensitivity": "No",
    "frequency_of_product_use": "Daily",
    "sun_exposure": "Moderate",
    "sleep_quality": "Average",
    "goal": "Reduce acne",
    "diet_habits": "Balanced",
    "current_skincare_routine": "cleanser, moisturizer",
    "sun_exposure_hours": "2",
    "medication_affecting_skin": "No"
}

# Convert questionnaire → normalized profile
q_profile = questionnaire_to_profile(sample_questionnaire)

# --------------------------
# 4. Run recommendation engine
# --------------------------
print("\nRunning recommendation engine...")
result = recommend_from_inputs(q_profile, image_metrics)

print("\nFinal Output:\n")
print(result)

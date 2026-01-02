import numpy as np
from disease_model.model import load_feature_extractor, load_classifier
from disease_model.preprocess import preprocess_image

# Load VGG19 feature extractor (frozen)
vgg = load_feature_extractor()

# Load trained classifier head
classifier = load_classifier(r"C:\Users\rajpu\Desktop\SKINAI\ml_training\best_vgg19_skin_model.h5")

# Your actual dataset folder names (already renamed)
CLASS_NAMES = [
    "Acne",
    "Atopic",
    "Eczema",
    "Melanoma",
    "Psoriasis",
    "Tinea"
]

def predict_disease(image_path):
    """Run full prediction pipeline and return disease + confidence."""
    
    # Preprocess input image → (1,180,180,3)
    img = preprocess_image(image_path)

    # Extract VGG19 features → (1,12800)
    feat = vgg.predict(img)
    feat = feat.reshape(1, -1)

    # Classifier prediction → array of probabilities
    pred = classifier.predict(feat)[0]

    # Final predicted class index
    class_idx = int(np.argmax(pred))
    predicted_class = CLASS_NAMES[class_idx]

    return {
        "class": predicted_class,
        "confidence": float(pred[class_idx]),
        "class_index": class_idx
    }

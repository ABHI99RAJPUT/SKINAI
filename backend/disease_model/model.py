import tensorflow as tf
from tensorflow.keras.applications import VGG19 # type: ignore

IMG_SIZE = (180, 180)

def load_feature_extractor():
    """Load VGG19 with frozen layers for feature extraction."""
    vgg = VGG19(weights="imagenet", include_top=False, input_shape=(*IMG_SIZE, 3))
    for layer in vgg.layers:
        layer.trainable = False
    return vgg

def load_classifier(model_path: str):
    """Load the trained dense classifier (.h5)."""
    return tf.keras.models.load_model(model_path)

import tensorflow as tf
from tensorflow.keras.applications import VGG19
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

IMG_SIZE = (180, 180)

def build_feature_extractor():
    vgg = VGG19(weights="imagenet", include_top=False, input_shape=(*IMG_SIZE, 3))
    
    for layer in vgg.layers:
        layer.trainable = False  # freeze
    
    return vgg

def build_classifier(num_classes):
    model = Sequential([
        Dense(200, activation='relu'),
        Dense(170, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    return model

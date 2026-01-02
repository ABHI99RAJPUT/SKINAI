import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications import VGG19

from model import build_feature_extractor, build_classifier
from dataset import load_dataset

# ----------------------------
# CONFIGURATION
# ----------------------------
TRAIN_DIR = r"C:\Users\rajpu\Desktop\SKINAI\ml_training\dataset_raw\train"
MODEL_SAVE_PATH = "best_vgg19_skin_model.h5"

IMG_SIZE = (180, 180)

# ----------------------------
# LOAD DATASET
# ----------------------------
print("📥 Loading images...")
X, y, CLASS_NAMES = load_dataset(TRAIN_DIR)

num_classes = len(CLASS_NAMES)
print("Detected Classes:", CLASS_NAMES)
print("Total Images:", len(X))

# ----------------------------
# PREPARE LABELS
# ----------------------------
y_cat = to_categorical(y, num_classes)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.20, random_state=42, shuffle=True
)

print(f"Training samples: {len(X_train)}  |  Testing samples: {len(X_test)}")

# ----------------------------
# VGG19 FEATURE EXTRACTION
# ----------------------------
print("\n🔵 Loading VGG19 Feature Extractor...")
vgg = build_feature_extractor()

print("Extracting features for training images...")
feat_train = vgg.predict(X_train, batch_size=32)

print("Extracting features for testing images...")
feat_test = vgg.predict(X_test, batch_size=32)

# Flatten shape: (N, 5,5,512) → (N, 12800)
feat_train = feat_train.reshape(len(feat_train), -1)
feat_test = feat_test.reshape(len(feat_test), -1)

print("Feature shape:", feat_train.shape)

# ----------------------------
# BUILD CLASSIFIER
# ----------------------------
print("\n🧱 Building top-level classifier...")
clf = build_classifier(num_classes)

clf.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ----------------------------
# TRAINING
# ----------------------------
print("\n🚀 Training classifier head...")
history = clf.fit(
    feat_train,
    y_train,
    epochs=25,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)

# ----------------------------
# EVALUATION
# ----------------------------
print("\n📊 Evaluating on test set...")
loss, acc = clf.evaluate(feat_test, y_test)
print(f"Test Accuracy: {acc:.4f}")

# ----------------------------
# SAVE MODEL
# ----------------------------
print("\n💾 Saving trained classifier...")
clf.save(MODEL_SAVE_PATH)
print("Model saved as:", MODEL_SAVE_PATH)

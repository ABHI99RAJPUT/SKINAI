import cv2
import numpy as np

IMG_SIZE = (180, 180)

def preprocess_image(image_path: str):
    """Read → resize → normalize → batch dimension."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, IMG_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

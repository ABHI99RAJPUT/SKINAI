import cv2
import numpy as np
from typing import Tuple

try:
    import mediapipe as mp # type: ignore
    _MP_AVAILABLE = True
    _mp_face = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
except Exception:
    _MP_AVAILABLE = False
    _mp_face = None


def preprocess_image(image_bytes: bytes, size: int = 512) -> np.ndarray:
    arr = np.frombuffer(image_bytes, np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("Invalid")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]
    scale = size / max(h, w)
    if scale != 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        rgb = cv2.resize(rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return rgb


def _crop_with_mediapipe(rgb_image: np.ndarray) -> Tuple[int,int,int,int]:
    if not _MP_AVAILABLE:
        raise RuntimeError("Error")
    img_h, img_w = rgb_image.shape[:2]
    results = _mp_face.process(rgb_image)
    if not results.detections:
        raise RuntimeError("No face detected")
    det = results.detections[0]
    bbox = det.location_data.relative_bounding_box
    x1 = int(max(0, bbox.xmin * img_w))
    y1 = int(max(0, bbox.ymin * img_h))
    x2 = int(min(img_w, (bbox.xmin + bbox.width) * img_w))
    y2 = int(min(img_h, (bbox.ymin + bbox.height) * img_h))
    return x1, y1, x2, y2


def _crop_with_haar(rgb_image: np.ndarray) -> Tuple[int,int,int,int]:
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))
    if len(faces) == 0:
        raise RuntimeError("No face detected")
    x, y, w, h = faces[0]
    return x, y, x + w, y + h


def crop_face_region(rgb_image: np.ndarray, pad_ratio: float = 0.25) -> np.ndarray:
    h, w = rgb_image.shape[:2]
    try:
        x1, y1, x2, y2 = _crop_with_mediapipe(rgb_image)
    except Exception:
        try:
            x1, y1, x2, y2 = _crop_with_haar(rgb_image)
        except Exception:
            short = min(h, w)
            ch = int(short * 0.9)
            cx, cy = w // 2, h // 2
            x1 = max(0, cx - ch // 2)
            y1 = max(0, cy - ch // 2)
            x2 = min(w, cx + ch // 2)
            y2 = min(h, cy + ch // 2)
            return rgb_image[y1:y2, x1:x2]

    box_h = y2 - y1
    pad = int(box_h * pad_ratio)
    x1p = max(0, x1 - pad)
    y1p = max(0, y1 - pad)
    x2p = min(w, x2 + pad)
    y2p = min(h, y2 + pad)
    return rgb_image[y1p:y2p, x1p:x2p]
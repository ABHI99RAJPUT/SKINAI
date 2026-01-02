import cv2
import numpy as np
from typing import Dict, Any, List, Tuple
from preprocess import preprocess_image, crop_face_region

def detect_face_and_roi(image_bytes: bytes) -> np.ndarray:
    rgb = preprocess_image(image_bytes)
    face_roi = crop_face_region(rgb)
    return face_roi


def estimate_skin_tone(face_roi: np.ndarray) -> Dict[str, Any]:
    h, w = face_roi.shape[:2]
    cy1, cy2 = h // 3, 2 * h // 3
    cx1, cx2 = w // 3, 2 * w // 3
    patch = face_roi[cy1:cy2, cx1:cx2]
    mean_bgr = cv2.mean(cv2.cvtColor(patch, cv2.COLOR_RGB2BGR))[:3]
    r, g, b = (int(mean_bgr[2]), int(mean_bgr[1]), int(mean_bgr[0]))
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    tone_label = "Light" if luminance > 180 else "Medium" if luminance > 110 else "Dark"
    return {"tone_hex": hex_color, "tone_label": tone_label, "luminance": float(round(luminance,2))}


def estimate_oiliness(face_roi: np.ndarray) -> Dict[str, Any]:
    gray = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    _, th = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY)
    bright_ratio = float(np.count_nonzero(th) / (th.size + 1e-9))
    if bright_ratio > 0.035:
        label = "High"
    elif bright_ratio > 0.01:
        label = "Moderate"
    else:
        label = "Low"
    dryness_flag = label == "Low"
    return {"oiliness_score": round(bright_ratio,4), "oiliness_label": label, "dryness_flag": dryness_flag}


def detect_acne_and_count(face_roi: np.ndarray) -> Dict[str, Any]:
    hsv = cv2.cvtColor(face_roi, cv2.COLOR_RGB2HSV)
    lower1 = np.array([0, 30, 40])
    upper1 = np.array([12, 255, 255])
    lower2 = np.array([160, 30, 40])
    upper2 = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bboxes: List[Tuple[int,int,int,int]] = []
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if area < 15 or area > face_roi.shape[0]*face_roi.shape[1]*0.06:
            continue
        bboxes.append((int(x),int(y),int(w),int(h)))

    acne_count = len(bboxes)
    if acne_count >= 15:
        severity = "Severe"
    elif acne_count >= 6:
        severity = "Moderate"
    elif acne_count >= 1:
        severity = "Mild"
    else:
        severity = "None"

    s = hsv[:,:,1]
    conf = float(np.mean(s[mask>0]) / 255.0) if np.count_nonzero(mask) > 0 else 0.0

    return {"acne_count": acne_count, "acne_bboxes": bboxes, "acne_severity": severity, "acne_confidence": round(conf,3)}


def detect_blackheads(face_roi: np.ndarray) -> Dict[str, Any]:
    gray = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    norm = cv2.normalize(blackhat, None, 0, 255, cv2.NORM_MINMAX)
    _, th = cv2.threshold(norm, 30, 255, cv2.THRESH_BINARY)
    th_inv = th

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 3
    params.maxArea = 200
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(th_inv)
    points = [(int(k.pt[0]), int(k.pt[1])) for k in keypoints]
    return {"blackhead_count": len(points), "blackhead_points": points}


def analyze_image(image_bytes: bytes) -> Dict[str, Any]:
    face = detect_face_and_roi(image_bytes)
    tone = estimate_skin_tone(face)
    oil = estimate_oiliness(face)
    acne = detect_acne_and_count(face)
    blackheads = detect_blackheads(face)

    return {
        "face_roi_shape": face.shape,
        "tone": tone,
        "oiliness": oil,
        "acne": acne,
        "blackheads": blackheads,
    }
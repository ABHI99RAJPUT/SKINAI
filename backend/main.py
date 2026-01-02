from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import uuid
import os
import json
import subprocess

# -------------------------------
# Backend (Disease Detection)
# -------------------------------
from disease_model.inference import predict_disease
from utils.constants import get_severity
from utils.advice import ADVICE

# -------------------------------
# FastAPI App Config
# -------------------------------
app = FastAPI(
    title="SkinAI API",
    description="AI-powered skin disease detection + skincare recommendations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = r"C:\Users\rajpu\Desktop\SKINAI\backend\uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------
# PATHS FOR SKINCARE PIPELINE
# -------------------------------
SKINCARE_VENV_PYTHON = r"C:\Users\rajpu\Desktop\SKINAI\backend\skincare\venv\Scripts\python.exe"
SKINCARE_PIPELINE = r"C:\Users\rajpu\Desktop\SKINAI\backend\skincare\run_pipeline.py"


# =========================================================
#               DISEASE DETECTION ENDPOINT
# =========================================================
@app.post("/api/detect")
async def api_detect(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.jpg"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_disease(file_path)

    os.remove(file_path)

    disease = result["class"]
    confidence = result["confidence"]
    severity = get_severity(confidence)
    advice = ADVICE.get(disease, {}).get(severity, "Advice unavailable.")

    return {
        "disease": disease,
        "confidence": confidence,
        "severity": severity,
        "advice": advice
    }


# =========================================================
#               SKINCARE PIPELINE ENDPOINT
# =========================================================
@app.post("/api/skincare/recommend")
async def skincare_recommend(
    image: UploadFile = File(...),
    profile: str = Form(...)
):

    # 1. Save uploaded image
    file_id = str(uuid.uuid4())
    image_path = f"{UPLOAD_DIR}/{file_id}.jpg"

    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # 2. Parse questionnaire JSON
    try:
        q_data = json.loads(profile)
    except:
        os.remove(image_path)
        return {"ok": False, "error": "Invalid JSON in 'profile' field"}

    payload = {
        "image_path": image_path,
        "questionnaire": q_data
    }

    # 3. Run skincare pipeline via subprocess
    process = subprocess.Popen(
        [
            SKINCARE_VENV_PYTHON,
            SKINCARE_PIPELINE
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(json.dumps(payload))

    os.remove(image_path)

    if process.returncode != 0:
        return {
            "ok": False,
            "error": "Skincare pipeline failed",
            "stderr": stderr
        }

    try:
        return json.loads(stdout)
    except:
        return {
            "ok": False,
            "error": "Failed to parse skincare response",
            "raw": stdout
        }


# =========================================================
#               RUN SERVER
# =========================================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

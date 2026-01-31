# 🌟 SKINSENSE - Your Personal AI Skin Care Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Project Status">
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-lightgrey" alt="Platform">
</p>

<p align="center">
  <strong>Your skin tells a story. Let AI help you read between the lines.</strong>
</p>

<p align="center">
  🧬 <strong>Disease Detection</strong> | ✨ <strong>Personalized Care</strong> | 🔒 <strong>Privacy First</strong>
</p>

Welcome to **SkinSense** - where cutting-edge artificial intelligence meets personalized skincare. This intelligent platform empowers you to understand your skin better, detect potential issues early, and receive customized care recommendations—all from the comfort of your home.

## 🎯 What Makes SkinSense Special?

<div align="center">

### 🧬 **Smart Disease Detection**
## UI/UX
![image alt](https://github.com/ABHI99RAJPUT/SKINAI/blob/3c836d7eb08de8d6d10527d5ae804c27570e63ce/skin%20ai%20pic%201.jpeg)
![image alt](https://github.com/ABHI99RAJPUT/SKINAI/blob/b67361a3865e808441f2f5237a836ae745f1362d/skin%20ai%20pic%203.jpeg)
![image alt](https://github.com/ABHI99RAJPUT/SKINAI/blob/b67361a3865e808441f2f5237a836ae745f1362d/skin%20ai%20pic2.jpeg)


```
📸 Photo Upload → 🤖 AI Analysis → 📋 Detailed Report
```

✅ **Detects 6 common skin conditions**
✅ **Provides confidence scores & severity levels**
✅ **Offers doctor-recommended next steps**
✅ **Gives personalized care advice**

### ✨ **Tailored Skincare Intelligence**

```
👤 Profile + 📸 Face Scan → 🧠 AI Processing → 📅 Custom Plan
```

✅ **Analyzes your unique skin characteristics**
✅ **Creates personalized daily routines**
✅ **Recommends suitable products**
✅ **Considers your lifestyle & goals**

</div>

## 🚀 Get Started in Minutes

<div align="center">

### 📦 **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

_Installs all necessary packages_

### 🧠 **Step 2: Add Your AI Model**

**Important**: Place `best_vgg19_skin_model.h5` in `ml_training/` directory

### ▶️ **Step 3: Launch SkinSense**

```bash
# Start the backend server
python backend/main.py

# Open frontend/index.html in your browser
```

🎯 **You're ready!** Your personal AI skin assistant is now running.

</div>

## 💡 How SkinSense Works

<div align="center">

```
📸 Capture → 🤖 Analyze → 🧠 Understand → ✨ Recommend
```

1. **📸 Capture**: Take a clear photo of your skin concern
2. **🤖 Analyze**: Our AI examines the image using advanced computer vision
3. **🧠 Understand**: We combine image analysis with your personal profile
4. **✨ Recommend**: Receive personalized, actionable skincare guidance

</div>

## 🛠️ Technical Architecture

<div align="center">

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Models     │
│   (Vanilla JS)  │◄──►│   (FastAPI)     │◄──►│ (TensorFlow)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       │                       │                       │
   🎨 UI/UX              🔌 API Endpoints        🧬 Deep Learning
   📱 Responsive         🖼️ Image Processing    📊 Predictions

```

### 🔧 Core Technology Stack

| Layer                | Technology         | Purpose                         |
| -------------------- | ------------------ | ------------------------------- |
| **Frontend**         | HTML/CSS/JS        | Clean, intuitive user interface |
| **Backend**          | FastAPI            | RESTful API handling            |
| **AI Engine**        | VGG19 + TensorFlow | Skin disease detection          |
| **Recommendation**   | Gemini API         | Personalized skincare advice    |
| **Image Processing** | OpenCV/MediaPipe   | Face detection & analysis       |

</div>

## 📱 User Experience

### Disease Detection Flow

1. Navigate to "Skin Disease Detection"
2. Upload a clear image of the affected area
3. Click "Analyze" and wait ~5-10 seconds
4. View results: disease name, confidence, severity, and medical advice

### Skincare Recommendation Flow

1. Go to "Skin Care Recommendation"
2. Upload a face photo
3. Complete the 10-question skin profile:
   - Skin type (Oily/Dry/Combination/Normal)
   - Sensitivity level
   - Product usage frequency
   - Sun exposure habits
   - Sleep quality
   - Skincare goals
   - Diet habits
   - Current routine
   - Medication information
4. Get your personalized skincare plan

## 🎨 Beautiful & Intuitive Interface

<div align="center">

✨ **Clean & Modern Design** - Minimal, distraction-free interface
📱 **Fully Responsive** - Works seamlessly on all devices
⚡ **Real-time Feedback** - Instant loading indicators and updates
📋 **Clear Results** - Easy-to-understand, actionable recommendations

</div>

## 🌟 Why Choose SkinSense?

<div align="center">

| Feature                             | Benefit                                       |
| ----------------------------------- | --------------------------------------------- |
| 🧬 **AI-Powered Detection**         | Accurate identification of 6 skin conditions  |
| ✨ **Personalized Recommendations** | Custom plans based on your unique profile     |
| 🔒 **Privacy First**                | All processing happens locally on your device |
| 🚀 **Lightning Fast**               | Results in seconds, not minutes               |
| 💡 **Expert Guidance**              | Doctor-recommended advice and safety notes    |
| 🌍 **Cross-Platform**               | Works on Windows, Mac, and Linux              |

</div>

## 🔒 Privacy & Security

- **Local Processing**: All analysis happens on your machine
- **No Data Storage**: Images are processed and deleted immediately
- **No Internet Required**: Works offline after initial setup
- **Your Data, Your Control**: Nothing is sent to external servers

## 🗂️ Complete Project Structure

```
Skin Care/
├── backend/                    # FastAPI Backend Server
│   ├── main.py                 # Main server entry point
│   ├── disease_model/          # Skin disease detection pipeline
│   │   ├── inference.py        # Prediction pipeline orchestration
│   │   ├── model.py            # VGG19 feature extractor loading
│   │   └── preprocess.py       # Image preprocessing utilities
│   ├── skincare/               # Personalized recommendation engine
│   │   ├── analysis.py         # Image analysis (tone, oiliness, acne detection)
│   │   ├── preprocess.py       # Face detection and ROI extraction
│   │   ├── questionnaire.py    # Profile validation and processing
│   │   ├── recommend.py        # LLM-powered recommendation generation
│   │   ├── run_pipeline.py     # Main recommendation pipeline entry
│   │   ├── test.py             # Unit tests for skincare modules
│   │   └── test_image.jpg      # Sample test image
│   └── utils/                  # Shared utilities and constants
│       ├── advice.py           # Medical advice for 6 skin conditions
│       ├── constants.py        # Severity mapping functions
│       └── helpers.py          # Helper functions
│
├── frontend/                   # Web User Interface
│   ├── index.html              # Main HTML structure
│   ├── style.css               # Dark-themed responsive styling
│   └── app.js                  # Client-side logic and API integration
│
├── ml_training/                # Machine Learning Components
│   ├── dataset.py              # Dataset loading and preprocessing
│   ├── model.py                # Model architecture definitions
│   └── train.py                # Training script and pipeline
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 📁 Detailed Component Breakdown

### 🧠 **Backend Architecture**

#### `main.py` - API Server

- FastAPI application with CORS enabled
- Two main endpoints: `/api/detect` and `/api/skincare/recommend`
- Handles file uploads and JSON processing
- Uses subprocess to run skincare pipeline

#### `disease_model/` - Disease Detection

- **`inference.py`**: Main prediction pipeline

  - Loads pre-trained VGG19 feature extractor
  - Loads custom classifier model
  - Processes images and returns predictions
  - Supports 6 skin conditions: Acne, Atopic, Eczema, Melanoma, Psoriasis, Tinea

- **`model.py`**: Model loading utilities

  - VGG19 feature extractor (frozen weights)
  - Custom dense classifier loader

- **`preprocess.py`**: Image preprocessing
  - Resize to 180×180
  - RGB conversion and normalization
  - Batch dimension handling

#### `skincare/` - Recommendation Engine

- **`analysis.py`**: Image-based skin analysis

  - Face region detection
  - Skin tone estimation
  - Oiliness level detection
  - Acne detection and counting
  - Blackhead detection

- **`preprocess.py`**: Face preprocessing

  - MediaPipe face detection (primary)
  - Haar cascade fallback
  - Face region cropping with padding

- **`questionnaire.py`**: User profile handling

  - Profile validation
  - Questionnaire normalization
  - Risk flag generation
  - Profile-image metrics combination

- **`recommend.py`**: LLM-powered recommendations

  - Gemini API integration
  - Prompt engineering for skincare advice
  - JSON response parsing and validation

- **`run_pipeline.py`**: Pipeline orchestrator
  - Reads input from stdin
  - Executes analysis → profile creation → recommendation
  - Outputs JSON results

#### `utils/` - Shared Utilities

- **`advice.py`**: Medical advice database

  - Condition-specific advice for 3 severity levels
  - Human-readable recommendations

- **`constants.py`**: Configuration

  - Confidence-to-severity mapping

- **`helpers.py`**: Helper functions
  - LLM prompt templates

### 🎨 **Frontend Components**

#### `index.html`

- Landing page with two main options
- Disease detection interface
- Skincare recommendation form
- Results display sections

#### `style.css`

- Dark theme design
- Responsive layout
- Card-based components
- Smooth animations

#### `app.js`

- Page navigation logic
- Image preview functionality
- API communication
- Dynamic result rendering
- Form data handling

### 🤖 **ML Training Pipeline**

#### `dataset.py`

- Dataset loading utilities
- Image preprocessing
- Class label handling
- Dataset statistics

#### `model.py`

- VGG19 feature extractor builder
- Custom classifier architecture
- Transfer learning setup

#### `train.py`

- Complete training pipeline
- Data loading and splitting
- Feature extraction
- Model training and evaluation
- Model saving

## 🔄 Data Flow

### Disease Detection Flow:

```
User Upload → FastAPI (/api/detect) → Preprocess → VGG19 Features → Classifier → Results
```

### Skincare Recommendation Flow:

```
User Upload + Profile → FastAPI (/api/skincare/recommend) → Subprocess →
Image Analysis + Profile Processing → LLM Recommendation → JSON Response
```

## 🔧 Configuration Files

### `.gitignore`

- Python cache files
- Virtual environments
- ML model files (.h5, .pkl, etc.)
- Dataset directories
- OS-specific files
- Environment files

### `requirements.txt`

- fastapi - Web framework
- uvicorn - ASGI server
- python-multipart - File upload support
- numpy - Numerical computing
- tensorflow - Deep learning
- pillow - Image processing

## 📚 API Documentation

Once the backend is running, visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### Core Endpoints

- `POST /api/detect` - Skin disease analysis
- `POST /api/skincare/recommend` - Personalized recommendations

## 🤝 Join Our Community

<div align="center">

We ❤️ contributions from the community! Here's how you can help:

### 🎯 Ways to Contribute

- 🧠 **Improve AI Models** - Enhance detection accuracy
- 🎨 **Enhance UI/UX** - Make the interface even more beautiful
- 📚 **Add Documentation** - Help others understand the project
- 🐛 **Report Issues** - Found a bug? Let us know!
- 💡 **Suggest Features** - What would make SkinSense better?

### 🚀 Getting Started

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

</div>

## 📄 License

This project is open source and available under the **MIT License**.

## 🙏 Acknowledgments

<div align="center">

Built with ❤️ using:

[**FastAPI**](https://fastapi.tiangolo.com/) • [**TensorFlow**](https://www.tensorflow.org/) • [**OpenCV**](https://opencv.org/) • [**MediaPipe**](https://mediapipe.dev/)

</div>

---

<div align="center">

### 🌟 **SkinSense**

**Because your skin deserves personalized care, powered by AI.**

[Report Issue](../../issues) • [Request Feature](../../issues)

</div>

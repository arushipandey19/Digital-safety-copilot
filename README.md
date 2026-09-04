# 🛡️ Digital Safety Copilot

Digital Safety Copilot is an AI-powered digital safety assistant that analyzes suspicious messages, URLs, and screenshots to identify potential phishing and scam indicators.

Instead of simply labeling something as "safe" or "unsafe", the system combines rule-based security checks, machine-learning signals, OCR, QR analysis, and LLM-based reasoning to provide an explainable risk assessment with recommended safe actions.

## 🚨 Problem

Digital scams are becoming increasingly convincing through social engineering, deceptive URLs, impersonation, QR codes, and realistic-looking screenshots.

Users often have to manually decide whether a message or link is trustworthy, while many existing detection tools provide only a simple binary result without explaining the reasoning behind it.

Digital Safety Copilot aims to make this process more understandable by showing the evidence behind a risk assessment and guiding users toward safer actions.

## 💡 Solution

Digital Safety Copilot uses a multi-layer analysis pipeline:

- Extracts text, URLs, entities, and QR data from user input
- Detects phishing and social-engineering patterns using deterministic rules
- Analyzes URLs for suspicious characteristics
- Uses a machine-learning model to estimate scam probability from text
- Combines multiple signals into an overall risk score
- Uses an LLM to correlate the evidence and generate a human-readable explanation
- Provides recommended safe actions
- Displays an evidence chain explaining the assessment

The system follows an evidence-first approach, where the final reasoning is grounded in signals produced by the analysis pipeline.

## ✨ Key Features

### 💬 Text Analysis

Analyze suspicious messages for signals such as:

- Urgency and pressure
- Credential requests
- Threatening language
- Reward or prize bait
- Excessive punctuation
- ML-based scam probability

### 🔗 URL Analysis

Analyze URLs for security indicators including:

- Domain verification
- Organization/domain mismatch
- Possible typosquatting
- Suspicious top-level domains
- Raw IP addresses
- Excessive subdomains

### 🖼️ Screenshot Analysis

Upload screenshots and extract useful security information using:

- OCR text extraction
- URL extraction
- Entity/organization extraction
- QR-code detection and decoding

### 📱 QR Code Analysis

QR codes detected inside screenshots can be decoded. If the QR code contains a URL, it can be passed through the URL security analysis pipeline.

### 🧠 Multi-Signal Risk Assessment

The system combines deterministic security rules and ML signals to produce an overall risk score and classify the result as:

- LOW
- MEDIUM
- HIGH

### 🤖 Evidence-Grounded AI Reasoning

The reasoning layer uses Qwen 2.5 7B through Ollama.

It receives the collected analysis evidence and generates:

- Risk explanation
- Safe actions
- Evidence chain

The LLM is instructed to base its reasoning on the supplied evidence rather than independently inventing security findings.

### 🌗 Light / Dark Mode

The frontend includes a responsive light/dark theme toggle with consistent styling across the application.

## 🔄 How It Works

```text
                         USER INPUT

                             │

              ┌──────────────┼──────────────┐
              │              │              │
            TEXT             URL        SCREENSHOT
              │              │              │
              └──────────────┼──────────────┘
                             │
                      EXTRACTION LAYER
                    ┌────────┼────────┐
                    │        │        │
                   OCR    URL Parse   QR
                    │        │        │
                    └────────┼────────┘
                             │
                     SECURITY ANALYSIS
                    ┌────────┴────────┐
                    │                 │
              ML Text Signal     Rule Engine
                    │                 │
                    │          ┌──────┴──────┐
                    │          │             │
                    │     Phishing Rules  URL Analysis
                    │          │             │
                    │          └──────┬──────┘
                    │                 │
                    └─────────────────┘
                             │
                       RISK SCORING
                             │
                       EVIDENCE MERGE
                             │
                       LLM REASONING
                             │
                 ┌───────────┼───────────┐
                 │           │           │
            EXPLANATION   SAFE ACTIONS  EVIDENCE
```

## 🏗️ Architecture

### Frontend

Built using:

- React
- Vite
- JavaScript
- CSS
- Lucide React

The frontend provides the main interface for entering messages, URLs, and screenshots, viewing analysis results, navigating the workflow, and switching between light and dark themes.

### Backend

Built using:

- Python
- FastAPI
- Uvicorn
- Pydantic

The backend exposes the analysis API and connects the different extraction and security-analysis components.

### AI / Analysis Layer

The analysis pipeline combines:

- Rule-based phishing detection
- URL security analysis
- Machine-learning text classification
- OCR
- QR detection
- Entity extraction
- LLM-based reasoning

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Uvicorn |
| Validation | Pydantic |
| OCR | Tesseract / pytesseract |
| Image Processing | Pillow, OpenCV |
| QR Detection | OpenCV QRCodeDetector |
| Machine Learning | scikit-learn, TF-IDF, Multinomial Naive Bayes |
| Model Persistence | joblib |
| LLM | Qwen 2.5 7B, Ollama |
| Version Control | Git, GitHub |

## 📁 Project Structure

```text
Digital-safety-copilot/
│
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   └── package.json
│
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── requirements.txt
│   └── test_*.py
│
├── ai_engine/             # AI reasoning and analysis
├── ml_engine/             # ML classifier and QR processing
├── security_engine/       # Phishing and URL security rules
├── reasoning/             # LLM client
│
├── requirements.txt
└── .gitignore
```

## ⚙️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/arushipandey19/Digital-safety-copilot.git
cd Digital-safety-copilot
```

### 2. Backend

Create a virtual environment.

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install the backend requirements:

```bash
pip install -r backend/requirements.txt
```

Run the backend:

```bash
uvicorn backend.app.main:app --reload
```

The backend runs at:

```text
http://localhost:8000
```

### 3. Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

## 🤖 LLM Setup

The default reasoning layer uses Ollama with Qwen 2.5 7B.

The default configuration is:

```text
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=qwen2.5:7b
```

Ollama must be running locally with the configured model available for the LLM reasoning stage.

## 🧪 Testing

The backend includes focused tests for major components such as:

- Entity extraction
- OCR processing
- URL extraction
- End-to-end analysis pipeline

Example:

```bash
python backend/test_entities.py
python backend/test_ocr.py
python backend/test_url.py
python backend/test_pipeline.py
```

The ML engine also contains scripts for model testing and comparison.

## 🔐 Explainability & Safety

Digital Safety Copilot follows an evidence-first approach:

- URL findings come from explicit URL security checks.
- Phishing findings come from defined security rules.
- ML predictions act as supporting evidence.
- The risk engine combines the available signals.
- The LLM receives the collected evidence and generates the explanation.
- Recommended actions focus on safer alternatives such as independently verifying information through an official website, application, or known contact method.

The system is intended as a decision-support tool and does not guarantee that a message or URL is completely safe or malicious.

## 🚧 Future Scope

Possible future improvements include:

- Deployment of the application
- Expanded and more diverse scam datasets
- Multilingual scam detection
- Improved OCR and screenshot analysis
- Additional security and threat-intelligence signals
- More extensive model evaluation
- Production-grade authentication, rate limiting, and monitoring

## 👥 Team

Developed collaboratively by:
- Anshika
- Arushi
- Asmi
- Aiza
# JobShield AI

AI-powered fake job and scam detection system built using Machine Learning, FastAPI, React, and Vite.

## Live Demo

https://job-shield-ai-olive.vercel.app

---

## Features

- Fake job detection using Machine Learning
- Scam keyword and red-flag analysis
- URL-based job analysis
- Confidence score prediction
- AI-generated explanation
- Responsive modern UI
- Reset functionality
- FastAPI backend API
- Cloud deployment using Render and Vercel

---

## Tech Stack

### Frontend
- React.js
- Vite
- CSS

### Backend
- FastAPI
- Python

### Machine Learning
- Scikit-learn
- LightGBM
- NLP

### Deployment
- Vercel
- Render

---

## Screenshots

## Screenshots

### Home UI
![Home UI](screenshots/Home%20UI.png)

### Fake Job Detection
![Fake Job](screenshots/Fake%20Job.png)

### Real Job Detection
![Real Job](screenshots/Real%20Job.png)



---

## How It Works

1. User pastes a job description or job URL
2. Backend extracts and analyzes job content
3. Machine Learning model predicts whether the job is real or fake
4. Scam flags and confidence score are generated
5. AI explanation is displayed to the user

---

## Installation

### Clone Repository

```bash
git clone https://github.com/kvsaidattasrinath/JobShield-AI.git
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Future Improvements

- Chrome extension integration
- Resume-job matching
- Company legitimacy verification
- Dashboard analytics
- Authentication system
- PDF and image upload support
- Advanced NLP and LLM integration

---

## Author

K V Sai Datta Srinath

GitHub:
https://github.com/kvsaidattasrinath

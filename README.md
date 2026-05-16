# ✨ Moeen | AI CV-Agent

### Intelligent AI-Powered Recruitment & Career Assistant

Moeen is an AI-powered recruitment and career support platform designed to help both job seekers and HR professionals make smarter hiring decisions using Artificial Intelligence.

The system analyzes CVs, compares them with job descriptions, identifies missing skills, generates interview questions, ranks candidates automatically, and provides personalized career recommendations using OpenAI models and intelligent agent workflows.

---

# 🚀 Features

## 👤 Job Seeker Portal
- Upload CVs (PDF / DOCX)
- AI-powered CV analysis
- Match score calculation
- Missing skills detection
- Personalized improvement recommendations
- AI-generated interview questions
- Interactive AI career assistant chatbot
- Email delivery for analysis reports

---

## 💼 HR / Recruiter Portal
- Upload multiple CVs simultaneously
- AI-based candidate ranking
- Automatic candidate comparison
- Best-fit candidate identification
- Smart recruitment insights
- AI-powered HR chatbot assistant
- Email summaries for recruiters

---

# 🧠 AI Technologies Used

- OpenAI API
- GPT-4o-mini
- Natural Language Processing (NLP)
- Multi-Agent Architecture
- Python
- Streamlit
- SMTP Email Integration

---

# 🏗️ System Architecture

The project follows a modular AI-agent workflow:

```text
Parser Agent
     ↓
Analyzer Agent
     ↓
Matcher Agent
     ↓
HR / Candidate Dashboards
```

---

## The system includes:

- 3 Core AI Agents
- 1 Base Agent Architecture
- 1 Orchestrator Controller


# 🔹 Agents Overview

## Parser Agent
Responsible for extracting and processing text from uploaded CV files.

## Analyzer Agent
Uses OpenAI models to analyze CVs against job descriptions and generate intelligent feedback.

## Matcher Agent
Ranks and compares candidates based on AI-generated scores and compatibility.

---

# 📂 Project Structure

```text
CV-Agent/
│
├── src/
│   ├── cv_agent/
│   │   ├── agents/
│   │   ├── services/
│   │   ├── frontends/
│   │   ├── model.py
│   │   └── config.py
│
├── data/
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone <repository_url>
cd CV-Agent
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure Environment Variables

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-4o-mini

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

---

## 4️⃣ Run the Application

```bash
streamlit run src/cv_agent/frontends/web/app.py
```

---

# 📧 Email Integration

The system supports automatic email delivery for:
- Candidate CV analysis reports
- HR ranking summaries

Implemented using:
- Gmail SMTP
- App Password Authentication

---

# 🎯 Project Objectives

- Improve recruitment efficiency
- Assist candidates in CV optimization
- Automate candidate screening
- Reduce manual HR workload
- Enhance hiring accuracy using AI

---

# 🖥️ User Experience

The platform provides:
- Interactive dashboards
- AI-generated insights
- Real-time feedback
- Conversational AI assistance
- Modern and user-friendly UI

---

# 👩‍💻 Team Members

- Hajer
- Seba
- Shaima
- Sahad

---

# 📌 Future Improvements

- ATS compatibility scoring
- LinkedIn profile analysis
- AI-generated cover letters
- Voice interview simulation
- Advanced analytics dashboard
- Cloud deployment

---

# 📜 License

This project was developed for educational and academic purposes.

---

# 💚 Moeen | مُعين

### Empowering Careers with Artificial Intelligence ✨
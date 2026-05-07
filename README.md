# CV-Agent 📄🤖

AI-powered CV Analysis and Matching System using Agentic AI Architecture.

---

# 📌 Overview

CV-Agent is an intelligent system designed to analyze resumes (CVs), compare them with job descriptions, and generate professional AI-based evaluations and recommendations.

The project follows an MVC-inspired architecture to separate:
- AI logic
- Services
- Frontend interfaces

This makes the system modular, scalable, and easy to extend.

---

# 🎯 Project Goals

The system aims to:

- Analyze CVs automatically
- Extract important candidate information
- Compare CVs with job descriptions
- Measure candidate-job compatibility
- Generate AI-based recommendations
- Help recruiters and applicants make better decisions

---

# 🧠 Features

✅ Upload CV files (PDF / DOCX)

✅ Extract text automatically

✅ AI-powered resume analysis

✅ Compare CV with job description

✅ Match score generation

✅ Skill extraction

✅ Missing skills detection

✅ Web chatbot interface

✅ Modular Agentic AI architecture

---

# 🏗️ Project Architecture

The project uses a modular structure inspired by the MVC Pattern.

```txt
CV-Agent/
│
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
│
├── data/
│   ├── cvs/
│   └── job_descriptions/
│
└── src/
    └── cv_agent/
        ├── model.py
        ├── main.py
        ├── config.py
        │
        ├── services/
        │   ├── llm.py
        │   └── parser.py
        │
        └── frontends/
            ├── cli/
            │   └── main.py
            │
            └── web/
                └── app.py
```

---

# 📂 File Structure Explanation

## model.py
Contains the AI workflow and business logic.

Responsible for:
- CV analysis
- Job matching
- Recommendation generation

---

## config.py
Loads environment variables and API keys.

---

## services/parser.py
Handles:
- PDF reading
- DOCX reading
- Text extraction

---

## services/llm.py
Handles communication with the AI model provider.

Examples:
- OpenAI
- OpenRouter
- Claude
- DeepSeek

---

## frontends/web/app.py
Web interface for interacting with the system.

Possible frameworks:
- Chainlit
- Streamlit

---

# ⚙️ Technologies Used

- Python
- LangGraph
- Chainlit
- OpenAI / OpenRouter APIs
- PyPDF
- python-docx

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/CV-Agent.git
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Download Dataset

The dataset is **not included** in the repository due to its size. Download it manually from Kaggle:

1. Go to: [Resume Dataset on Kaggle](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
2. Download and extract the zip file
3. Place the extracted folder inside `dataset/` so the structure looks like:

```
CV-Agent/
└── dataset/
    └── Resume_Dataset/
        ├── Resume/
        │   └── Resume.csv
        └── data/
            └── data/
                ├── ACCOUNTANT/
                ├── ENGINEER/
                └── ...
```

---

## 4. Create Environment Variables

Create `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
MODEL_NAME=deepseek/deepseek-chat
```

---

# ▶️ Run Web Interface

```bash
python src/cv_agent/frontends/web/app.py
```

---

# 📊 Example Workflow

1. Upload CV
2. Upload Job Description
3. Extract text
4. Analyze skills and experience
5. Compare with job requirements
6. Generate match score and recommendations

---

# 🔮 Future Improvements

- Vector database integration
- RAG pipeline
- Interview question generation
- Multi-agent workflow
- Dashboard analytics
- Telegram integration

---

# 👩‍💻 Team

Graduation Project — AI & Data Track

Developed using Agentic AI concepts and modern AI application architecture.

---

# 📄 License

This project is for educational and academic purposes.
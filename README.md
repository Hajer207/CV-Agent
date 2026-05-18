# ✨ Moeen | معين  
### **Agentic AI Recruitment Intelligence & Context-Aware RAG Platform**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Architecture-Agentic_AI_&_RAG-10B981?style=for-the-badge" alt="Architecture">
</p>

<p align="center">
 Intelligent AI-powered recruitment platform combining <b>Agentic AI</b>, <b>Multi-Job RAG</b>, candidate intelligence, and HR automation.
</p>

---

# 🎯 Project Overview

**Moeen (معين)** is an enterprise-grade AI recruitment intelligence platform designed to modernize and automate the hiring workflow for both recruiters and job seekers.

Traditional recruitment processes often suffer from:
- Manual CV screening bottlenecks
- Inconsistent candidate evaluation
- Time-consuming shortlisting
- Limited recruitment intelligence
- Generic chatbot responses disconnected from real job requirements

Moeen solves these challenges through a modern **Agentic AI architecture** combined with a **Multi-Job Retrieval-Augmented Generation (RAG)** system.

The platform automates:
- CV parsing and analysis
- Candidate ranking
- Skills gap detection
- Recruitment insights generation
- Role-specific HR conversations
- Context-aware recruitment intelligence

---

# 🚀 Core System Features

## 👤 Job Seeker Portal

- 📄 Intelligent CV Parsing (`PDF` / `DOCX`)
- 📊 AI-Powered Match Scoring
- 🧠 Skills & Missing Skills Detection
- 🎯 Personalized Improvement Recommendations
- 💬 AI-Generated Interview Questions
- 📧 Automated Email Reports
- 📈 Candidate Readiness Insights

---

## 💼 HR & Recruiter Portal

- 📂 Multi-CV Upload Engine
- 🏆 Dynamic Candidate Leaderboard
- 🤖 HR Intelligence Chatbot
- 📊 Recruitment Insights & Recommendations
- 🎯 Candidate-to-Role Alignment Analysis
- 🔎 Context-Aware Multi-Job RAG Retrieval
- ⚡ Real-Time Candidate Comparison

---

# 🧠 High-Level Agentic Workflow

```text
       ┌────────────────────────────────────────────────────────┐
       │                 User Upload / Input                    │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │        Parser Agent           │
                   │      (Text Extraction)        │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │       Analyzer Agent          │
                   │   (Skills & Profile Analysis) │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │        Matcher Agent          │
                   │    (Scoring & Benchmarking)  │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
        ┌───────────────────────────────────────────────────────┐
        │                 Orchestration Layer                   │
        └───────┬───────────────────────────────────────┬───────┘
                │                                       │
                ▼                                       ▼
   ┌───────────────────────────┐           ┌───────────────────────────┐
   │ Candidate Intelligence    │           │ Candidate Leaderboard     │
   │ & Interview Generation    │           │ & Hiring Insights         │
   └───────────────────────────┘           └────────────┬──────────────┘
                                                        │
                                                        ▼
                                           ┌───────────────────────────┐
                                           │    RAG Retrieval Agent    │
                                           │  (Dynamic Context Switch) │
                                           └────────────┬──────────────┘
                                                        │
                                                        ▼
                                           ┌───────────────────────────┐
                                           │  HR Intelligence Agent    │
                                           │ (Grounded AI Chatbot)     │
                                           └───────────────────────────┘
```

---

# 🤖 Core AI Agents

## 🧠 CV Analysis Agent
Responsible for:
- Extracting structured resume text
- Detecting technical and soft skills
- Identifying missing competencies
- Generating match scores
- Building candidate intelligence profiles

---

## 📊 Candidate Ranking Agent
Responsible for:
- Comparing applicants
- Evaluating candidate-job alignment
- Ranking candidates dynamically
- Generating hiring insights
- Supporting HR decision-making

---

## 🔎 RAG Retrieval Agent
Responsible for:
- Retrieving role-specific job offer context
- Dynamically switching operational contexts
- Reducing hallucination
- Injecting retrieved context into AI prompts
- Grounding chatbot responses using real documents

---

## 💬 HR Intelligence Agent
Responsible for:
- Answering recruiter questions
- Generating professional HR reasoning
- Explaining candidate suitability
- Producing context-aware responses
- Supporting recruitment decisions

---

# 🔎 Multi-Job RAG Architecture

To reduce hallucination and improve response accuracy, Moeen uses a **Multi-Job Retrieval-Augmented Generation (RAG)** workflow.

Instead of relying only on static LLM memory, the system dynamically retrieves real job-offer documents based on the selected role before generating responses.

## 📁 Job Offer Repository

```text
data/job_offers/
```

### Supported Roles

- 📊 Data Analyst
- 💰 Accountant
- 👩‍💼 HR Specialist
- 💻 Information Technology
- 👩‍🏫 Teacher

### Example Files

```text
data_analyst.txt
accountant.txt
hr.txt
information_technology.txt
teacher.txt
```

---

# ⚡ RAG Execution Pipeline

### 1️⃣ Role Selection
Recruiter selects a target operational role.

### 2️⃣ Context Retrieval
The system dynamically retrieves the matching job-offer document.

### 3️⃣ Prompt Injection
Retrieved requirements, salary information, and responsibilities are injected into the AI prompt.

### 4️⃣ Grounded Response Generation
The chatbot answers only using the retrieved job context.

If information is unavailable, the system explicitly states:

> “Information not found within the selected job profile documents.”

This prevents unsupported hallucinated answers.

---

# 🎯 Business Impact

Moeen significantly improves recruitment workflows by reducing manual screening effort and increasing hiring intelligence.

The platform enhances:
- ⚡ Recruitment efficiency
- 📊 Candidate evaluation quality
- 🤖 HR automation
- 🧠 Context-aware decision support
- 🎯 Candidate-job alignment
- 📈 Recruitment scalability

By combining Agentic AI workflows with Multi-Job RAG retrieval, Moeen creates a modern AI-powered hiring ecosystem.

---

# 🛠️ Tech Stack & Dependencies

| Category | Technologies |
|---|---|
| Programming Language | Python 3.11 |
| Frontend Framework | Streamlit |
| AI Engine | OpenAI API |
| Data Processing | Pandas & NumPy |
| CV Parsing | PyPDF2 / Docx2txt |
| AI Architecture | Agentic AI + RAG |
| Communication Layer | SMTP Email Integration |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
CV-Agent/
│
├── data/
│   ├── cvs/
│   ├── job_descriptions/
│   └── job_offers/
│
├── dataset/
│   ├── Job_description_dataset/
│   └── Resume_Dataset/
│
├── src/
│   └── cv_agent/
│       ├── agents/
│       ├── frontends/
│       │   └── web/
│       │       └── app.py
│       ├── services/
│       ├── config.py
│       └── model.py
│
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <repository_url>
cd CV-Agent
```

---

## 2️⃣ Create Virtual Environment

```bash
py -3.11 -m venv .venv
```

---

## 3️⃣ Activate Environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-4o-mini

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

---

## 6️⃣ Run Application

```bash
streamlit run src/cv_agent/frontends/web/app.py
```

---

# 💬 Example HR Questions

```text
What is the salary range for this role?
```

```text
Does this role require SAP experience?
```

```text
What skills should the strongest candidate have?
```

```text
Does this role require Power BI experience?
```

```text
What responsibilities are included in this role?
```

---

# 📌 Future Roadmap

- [ ] Semantic Vector Retrieval (ChromaDB / Pinecone)
- [ ] Arabic NLP Support
- [ ] Embedding-Based Candidate Matching
- [ ] Admin Analytics Dashboard
- [ ] Custom Job Offer Uploading
- [ ] Advanced Hiring Metrics Visualization
- [ ] Database Integration
- [ ] Fine-Tuned Recruitment Models

---

# 👩‍💻 Development Team

| Developer |
|---|
| Hajer |
| Seba |
| Shaima |
| Shahad |

---

# 📜 License

This project was developed for educational, academic, and applied AI engineering purposes.

---

# ✨ Final Statement

**Moeen (معين)** represents a modern AI-driven recruitment ecosystem that combines Agentic AI workflows, Multi-Job RAG retrieval, and recruitment intelligence into one scalable platform capable of supporting both recruiters and job seekers through intelligent automation.

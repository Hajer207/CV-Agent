import os
import sys
import re
import tempfile
from pathlib import Path

import streamlit as st
import pandas as pd

# Make src available so imports work when running Streamlit directly
ROOT_DIR = Path(__file__).resolve().parents[4]
SRC_DIR = ROOT_DIR / "src"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from cv_agent.agents.orchestrator import Orchestrator
except Exception:
    Orchestrator = None

try:
    from cv_agent.services.email_service import send_report_to_candidate, send_summary_to_hr
except Exception:
    send_report_to_candidate = None
    send_summary_to_hr = None

try:
    from cv_agent.services.llm import ask_ai
except Exception:
    ask_ai = None

try:
    from cv_agent.services.rag_service import retrieve_job_context, load_job_description
except Exception:
    retrieve_job_context = None
    load_job_description = None


st.set_page_config(
    page_title="Moeen | AI CV-Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background-color: #F8F9FA;
    color: #334155;
}

[data-testid="stSidebar"] {
    background-color: #006C35 !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.header-banner {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    border: 1px solid #E2E8F0;
}

.stButton > button {
    background: #00A3E0 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    border: none !important;
    height: 3rem;
}

.analysis-box {
    background: white;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

.email-note {
    background: #ECFDF5;
    color: #006C35;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #BBF7D0;
    margin-top: 10px;
}

.sidebar-title {
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 28px;
    color: white;
}

.sidebar-spacer {
    height: 24px;
}
</style>
""", unsafe_allow_html=True)


def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "hr_chat_history" not in st.session_state:
        st.session_state.hr_chat_history = []

    if "candidate_result" not in st.session_state:
        st.session_state.candidate_result = None

    if "hr_result" not in st.session_state:
        st.session_state.hr_result = None

    if "hr_job_requirements" not in st.session_state:
        st.session_state.hr_job_requirements = ""

    if "candidate_about" not in st.session_state:
        st.session_state.candidate_about = False

    if "hr_about" not in st.session_state:
        st.session_state.hr_about = False


def go_home():
    st.session_state.page = "landing"
    st.session_state.candidate_result = None
    st.session_state.hr_result = None
    st.session_state.candidate_about = False
    st.session_state.hr_about = False


def get_job_description_template(role):
    templates = {
        "Accountant": "We are looking for an Accountant with experience in financial reporting, budgeting, accounts payable, accounts receivable, Excel, and accounting systems.",
        "HR": "We are looking for an HR Specialist with experience in recruitment, employee relations, onboarding, HR policies, performance management, and communication skills.",
        "Information Technology": "We are looking for an IT Specialist with experience in technical support, networks, troubleshooting, system administration, cybersecurity basics, and user support.",
        "Teacher": "We are looking for a Teacher with strong classroom management, lesson planning, student assessment, communication skills, and subject knowledge.",
        "Software Engineer": "We are looking for a Software Engineer with experience in Python, APIs, databases, Git, software design, testing, and problem solving.",
        "Data Analysis": "We are looking for a Data Analyst with experience in SQL, Power BI, Python, data cleaning, visualization, reporting, and business insights.",
        "Healthcare Administrator": "We are looking for a Healthcare Administrator with experience in healthcare operations, patient services, scheduling, compliance, reporting, and administrative coordination."
    }
    return templates.get(role, "")


JOB_ROLES = [
    "Accountant",
    "HR",
    "Information Technology",
    "Teacher",
    "Software Engineer",
    "Data Analysis",
    "Healthcare Administrator"
]

# Upload safety settings
# Keep files reasonably small to avoid browser freezing during upload/processing.
MAX_CV_SIZE_MB = 10
MAX_HR_CVS = 5


def validate_uploaded_file(uploaded_file, max_size_mb=MAX_CV_SIZE_MB):
    """Return (is_valid, message) for an uploaded Streamlit file."""
    if uploaded_file is None:
        return False, "No file uploaded."

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > max_size_mb:
        return (
            False,
            f"File '{uploaded_file.name}' is too large ({file_size_mb:.1f} MB). "
            f"Please upload a file smaller than {max_size_mb} MB."
        )

    if not uploaded_file.name.lower().endswith((".pdf", ".docx")):
        return False, f"File '{uploaded_file.name}' must be PDF or DOCX."

    return True, ""


def save_uploaded_file_to_temp(uploaded_file):
    """Save uploaded file to a temporary path only after the user clicks Analyze/Ranking."""
    suffix = ".pdf" if uploaded_file.name.lower().endswith(".pdf") else ".docx"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name


def get_demo_candidate_result():
    return {
        "score": 84,
        "skills": {
            "Python": 90,
            "SQL": 70,
            "Data Visualization": 30
        },
        "missing": [
            "Cloud Deployment",
            "Advanced Machine Learning",
            "A/B Testing"
        ],
        "questions": [
            "Explain a data project you worked on.",
            "How do you clean missing values?",
            "How do you build a dashboard for business users?"
        ],
        "tips": [
            "Add measurable achievements to your CV.",
            "Tailor your summary to the target role.",
            "Add more keywords from the job description."
        ],
        "summary": "Your CV shows strong potential for the selected role, especially in Python and SQL. Improving data visualization and adding measurable achievements will increase your readiness."
    }


def get_demo_hr_result():
    df_hr = pd.DataFrame({
        "Rank": ["#1", "#2", "#3", "#4"],
        "Candidate": ["Sarah J.", "Ahmed M.", "Lina K.", "Omar F."],
        "Match": ["94%", "89%", "82%", "78%"],
        "Top Skill": ["Machine Learning", "Data Science", "Python", "SQL"]
    })

    return {
        "total_cvs": 4,
        "top_match": 94,
        "verified_fits": 3,
        "best_candidate": "Sarah J.",
        "best_reason": "Sarah J. is the best CV match for this role because her profile shows the strongest alignment with Machine Learning and Data Science requirements.",
        "leaderboard": df_hr
    }



def _extract_lines_from_section(text, start_title, end_titles):
    """Extract bullet-like lines from a plain text AI report section."""
    if not text:
        return []

    end_pattern = "|".join([re.escape(title) + r"\s*:" for title in end_titles])
    pattern = re.escape(start_title) + r"\s*:\s*(.*?)(?=" + end_pattern + r"|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if not match:
        return []

    content = match.group(1).strip()
    lines = []

    for line in content.splitlines():
        cleaned = line.strip()
        cleaned = re.sub(r"^[\-\*\u2022\s]*", "", cleaned)
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", cleaned).strip()

        if cleaned:
            lines.append(cleaned)

    return lines


def _extract_score_from_report(report, fallback=0):
    """Extract Match Score safely from an AI report."""
    if not report:
        return fallback

    patterns = [
        r"Match\s*Score\s*:\s*(\d{1,3})\s*%",
        r"Overall\s*Match\s*:\s*(\d{1,3})\s*%",
        r"Score\s*:\s*(\d{1,3})\s*%",
    ]

    for pattern in patterns:
        match = re.search(pattern, report, re.IGNORECASE)
        if match:
            return min(int(match.group(1)), 100)

    return fallback


def normalize_candidate_result(result):
    """
    Convert the real AI output into the same structure the old demo UI expects.
    This keeps the old design/templates unchanged while replacing demo data with AI.
    """
    if not isinstance(result, dict):
        report = str(result)
        score = _extract_score_from_report(report, 0)
        questions = []
    else:
        report = result.get("report", "") or result.get("summary", "") or str(result)
        score = result.get("score", 0) or _extract_score_from_report(report, 0)
        questions = result.get("questions", result.get("interview_questions", []))

    if isinstance(questions, str):
        questions = [
            re.sub(r"^\d+[\.\)]\s*", "", q.strip())
            for q in questions.splitlines()
            if q.strip()
        ]

    skills_found = _extract_lines_from_section(
        report,
        "Skills Found",
        ["Missing Skills", "Strengths", "Weaknesses", "Recommendations", "Interview Questions"]
    )

    missing = _extract_lines_from_section(
        report,
        "Missing Skills",
        ["Strengths", "Weaknesses", "Recommendations", "Interview Questions"]
    )

    tips = _extract_lines_from_section(
        report,
        "Recommendations",
        ["Interview Questions"]
    )

    # If the model used different labels, keep the UI safe
    if isinstance(result, dict):
        skills = result.get("skills", {})
        if not skills and skills_found:
            skills = {skill: 80 for skill in skills_found}
        missing = result.get("missing", missing)
        tips = result.get("tips", tips)
    else:
        skills = {skill: 80 for skill in skills_found}

    summary = report

    return {
        "score": int(score) if str(score).isdigit() else 0,
        "skills": skills if isinstance(skills, dict) else {},
        "missing": missing if isinstance(missing, list) else [],
        "questions": questions if isinstance(questions, list) else [],
        "tips": tips if isinstance(tips, list) else [],
        "summary": summary,
        "report": report,
    }

def landing_page():
    st.markdown(
        "<h1 style='text-align: center; color: #006C35; font-size: 60px; font-weight: 800;'>Moeen | مُعين</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; color: #64748B; font-size: 20px;'>Your Intelligent Career & Hiring Agent</p>",
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style='background: white; padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #E2E8F0;'>
                <h2 style='color: #006C35;'>👤 Job Seeker</h2>
                <p>Optimize your CV and gap analysis.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Enter as Job Seeker", key="nav_cand", use_container_width=True):
            st.session_state.page = "candidate"
            st.session_state.candidate_result = None
            st.session_state.candidate_about = False
            st.rerun()

    with col2:
        st.markdown("""
            <div style='background: white; padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #E2E8F0;'>
                <h2 style='color: #334155;'>💼 Employer / HR</h2>
                <p>Manage and rank candidates efficiently.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Enter as HR", key="nav_hr", use_container_width=True):
            st.session_state.page = "hr"
            st.session_state.hr_result = None
            st.session_state.hr_about = False
            st.rerun()


def candidate_metrics(result):
    result = normalize_candidate_result(result)

    score = result.get("score", 0)
    missing = result.get("missing", [])

    if score >= 75:
        readiness = "Strong 🔥"
    elif score >= 50:
        readiness = "Moderate"
    else:
        readiness = "Needs Work"

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f'<div class="metric-card"><b>Overall Match</b><br><h2 style="color:#006C35;">{score}%</h2></div>',
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f'<div class="metric-card"><b>Missing Skills</b><br><h2 style="color:#F59E0B;">{len(missing)} Gaps</h2></div>',
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f'<div class="metric-card"><b>Readiness</b><br><h2 style="color:#00A3E0;">{readiness}</h2></div>',
            unsafe_allow_html=True
        )


def render_clean_sidebar(role):
    st.markdown('<div class="sidebar-title">Moeen | مُعين</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    if st.button("ⓘ About", use_container_width=True, key=f"about_{role}"):
        if role == "candidate":
            st.session_state.candidate_about = True
        else:
            st.session_state.hr_about = True
        st.rerun()

    st.divider()

    if st.button("Logout", use_container_width=True, key=f"logout_{role}"):
        go_home()
        st.rerun()
def about_page(user_type):
    st.markdown("""
    <div style="text-align:center; margin-top:20px; margin-bottom:10px;">
        <h1 style="color:#1E293B; font-size:54px; font-weight:800; margin-bottom:5px;">
            عن مُعين | Moeen CV-Agent
        </h1>
        <p style="color:#64748B; font-size:22px; margin-bottom:40px;">
            منصة ذكية لتحليل السير الذاتية ودعم قرارات التوظيف
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h2 style='color:#006C35;'>🎯 كيف يساعد مُعين الباحث عن عمل؟</h2>", unsafe_allow_html=True)
        st.write("""
يقوم مُعين بتحليل السيرة الذاتية ومقارنتها بالوصف الوظيفي المستهدف،
ثم يحدد المهارات المفقودة ونقاط التحسين، ويقدم توصيات ذكية تساعد الباحث
على رفع نسبة التوافق وزيادة جاهزيته المهنية.
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h2 style='color:#006C35;'>🏢 كيف يساعد مُعين مسؤولي التوظيف؟</h2>", unsafe_allow_html=True)
        st.write("""
يساعد مُعين فرق التوظيف على فرز وتحليل السير الذاتية بشكل أسرع وأكثر دقة،
عبر مقارنة المرشحين مع متطلبات الوظيفة وترتيبهم بناءً على نسبة التوافق،
مما يختصر وقت المراجعة اليدوية ويحسن جودة الاختيار.
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h2 style='color:#006C35;'>🤖 ماذا يقدم مُعين؟</h2>", unsafe_allow_html=True)
        st.write("""
• تحليل ذكي للسيرة الذاتية  
• قياس نسبة التوافق الوظيفي  
• اكتشاف الفجوات المهارية  
• توليد توصيات احترافية  
• توليد أسئلة مقابلات مخصصة  
• ترتيب المرشحين للـ HR  
• دعم اتخاذ القرار في التوظيف
        """)

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("← Back to Dashboard", use_container_width=True):
        if user_type == "candidate":
            st.session_state.candidate_about = False
        else:
            st.session_state.hr_about = False
        st.rerun()

def candidate_portal():
    with st.sidebar:
        render_clean_sidebar(role="candidate")

    if st.session_state.candidate_about:
        about_page("candidate")
        return

    st.markdown("""
        <div class="header-banner">
            <h2 style="margin:0;">Welcome, <b>Job Seeker!</b> Let's start your journey.</h2>
            <span style="color: #64748B;">Monday, May 11, 2026</span>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.candidate_result is None:
        st.info("Upload your CV and choose or paste a job description, then start the analysis to generate your smart report.")
    else:
        candidate_metrics(st.session_state.candidate_result)

    st.write("")

    left_col, right_col = st.columns([1.5, 1])

    with right_col:
        st.subheader("📥 Inputs")

        with st.container(border=True):
            uploaded_cv = st.file_uploader(
                "Upload your CV (PDF or DOCX)",
                type=["pdf", "docx"],
                key="candidate_cv_uploader",
                help=f"Recommended file size: under {MAX_CV_SIZE_MB} MB."
            )

            if uploaded_cv is not None:
                is_valid_cv, cv_message = validate_uploaded_file(uploaded_cv)
                if is_valid_cv:
                    st.success(f"Selected: {uploaded_cv.name}")
                else:
                    st.error(cv_message)

            target_role = st.selectbox("Target Role", JOB_ROLES)

            jd_source = st.radio(
                "Job Description Source",
                ["Use ready template", "Write custom description"],
                horizontal=True
            )

            if jd_source == "Use ready template":
                job_description = st.text_area(
                    "Job Description",
                    value=get_job_description_template(target_role),
                    height=130
                )
            else:
                job_description = st.text_area(
                    "Job Description",
                    placeholder="Paste target JD here...",
                    height=130
                )

            candidate_email = st.text_input(
                "Email Address",
                placeholder="example@email.com",
                key="candidate_email"
            )

            if st.button("Start AI Analysis ✨", use_container_width=True):
                if not uploaded_cv or not job_description:
                    st.warning("Please upload your CV and enter the job description.")
                    return

                is_valid_cv, cv_message = validate_uploaded_file(uploaded_cv)
                if not is_valid_cv:
                    st.error(cv_message)
                    return

                if Orchestrator is None:
                    st.error("AI Orchestrator is not available. Please check import paths.")
                    return

                with st.spinner("Moeen AI is analyzing your CV..."):
                    cv_path = save_uploaded_file_to_temp(uploaded_cv)

                    ai_result = Orchestrator().run_single(
                        cv_path=cv_path,
                        job_description=job_description,
                        cv_id=uploaded_cv.name
                    )

                    ai_result = normalize_candidate_result(ai_result)
                    st.session_state.candidate_result = ai_result

                    if candidate_email and send_report_to_candidate is not None:
                        send_report_to_candidate(
                            candidate_email=candidate_email,
                            candidate_name="Candidate",
                            report=ai_result.get("report", ai_result.get("summary", "")),
                            score=ai_result.get("score", 0)
                        )

                st.success("AI analysis completed successfully.")
                st.rerun()

            if st.session_state.candidate_result is not None and candidate_email:
                st.markdown(
                    f"<div class='email-note'>📩 Report sent to: <b>{candidate_email}</b></div>",
                    unsafe_allow_html=True
                )

        st.subheader("🧠 Moeen Thinking")

        with st.container(border=True):
            if st.session_state.candidate_result is None:
                st.info("Waiting for CV and job description...")
            else:
                st.success("Parser Agent extracted the CV text.")
                st.success("Analyzer Agent compared the CV with the job description.")
                st.success("Career Coach Agent prepared recommendations.")

    with left_col:
        st.subheader("📊 Moeen Smart Report")

        if st.session_state.candidate_result is None:
            st.markdown("""
            <div class="analysis-box">
                <h4>No analysis yet</h4>
                <p>Your skills analysis, interview preparation, and improvement tips will appear here after analysis.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            result = normalize_candidate_result(st.session_state.candidate_result)

            tab1, tab2, tab3 = st.tabs(["Skills Analysis", "Interview Prep", "Tips"])

            with tab1:
                st.write(result.get("summary", "No summary available."))

                skills = result.get("skills", {})
                if skills:
                    for skill, value in skills.items():
                        st.write(f"**{skill}**")
                        try:
                            st.progress(int(value))
                        except Exception:
                            st.write(value)
                else:
                    st.info("No skills breakdown available.")

            with tab2:
                questions = result.get("questions", [])
                if questions:
                    for question in questions:
                        st.write(f"- {question}")
                else:
                    st.info("No interview questions available.")

            with tab3:
                tips = result.get("tips", [])
                if tips:
                    for tip in tips:
                        st.write(f"- {tip}")
                else:
                    st.info("No tips available.")

            st.subheader("💬 Chat with Moeen")

            with st.container(border=True):
                st.write("**Moeen:** Do you have any question about your CV analysis?")
                user_message = st.text_input("Ask Moeen a question...", key="chat_input")

                if st.button("Send Message", key="candidate_chat_btn"):
                    if user_message:
                        st.session_state.chat_history = [("You", user_message)]

                        if ask_ai is not None:
                            report_context = result.get("report", result.get("summary", ""))

                            bot_reply = ask_ai(f"""
You are Moeen, an AI career coach.

Answer the user's question based on this CV analysis report.

CV Analysis Report:
{report_context}

User Question:
{user_message}

Give a helpful, specific, and concise answer.
""")
                        else:
                            bot_reply = "I cannot connect to the AI service right now. Please check the OpenAI setup."

                        st.session_state.chat_history = [
                         ("You", user_message),
                         ("Moeen", bot_reply)
                     ]
                        st.rerun()

                for sender, message in st.session_state.chat_history:
                    st.write(f"**{sender}:** {message}")



def build_hr_ai_result(ranked_results):
    """Convert real AI ranked results into the same structure the old HR UI expects."""
    ranked_results = [normalize_candidate_result(item) | {"cv_id": item.get("cv_id", f"Candidate {i + 1}") if isinstance(item, dict) else f"Candidate {i + 1}"} for i, item in enumerate(ranked_results)]
    ranked_results = sorted(ranked_results, key=lambda item: item.get("score", 0), reverse=True)

    rows = []
    for index, item in enumerate(ranked_results, start=1):
        skills = item.get("skills", {})
        top_skill = "AI Analysis"
        if isinstance(skills, dict) and skills:
            top_skill = next(iter(skills.keys()))

        rows.append({
            "Rank": f"#{index}",
            "Candidate": item.get("cv_id", f"Candidate {index}"),
            "Match": f"{item.get('score', 0)}%",
            "Top Skill": top_skill,
        })

    leaderboard = pd.DataFrame(rows, columns=["Rank", "Candidate", "Match", "Top Skill"])
    best = ranked_results[0] if ranked_results else {}

    return {
        "total_cvs": len(ranked_results),
        "top_match": best.get("score", 0),
        "verified_fits": len([item for item in ranked_results if item.get("score", 0) >= 70]),
        "best_candidate": best.get("cv_id", "Best Candidate"),
        "best_reason": best.get("report", best.get("summary", "No report available.")),
        "leaderboard": leaderboard,
        "ranked_results": ranked_results,
    }

def hr_metrics(result):
    h1, h2, h3 = st.columns(3)

    with h1:
        st.markdown(
            f'<div class="metric-card"><b>Total CVs</b><br><h2 style="color:#006C35;">{result["total_cvs"]}</h2></div>',
            unsafe_allow_html=True
        )

    with h2:
        st.markdown(
            f'<div class="metric-card"><b>Top Match</b><br><h2 style="color:#00A3E0;">{result["top_match"]}%</h2></div>',
            unsafe_allow_html=True
        )

    with h3:
        st.markdown(
            f'<div class="metric-card"><b>Verified Fits</b><br><h2 style="color:#F59E0B;">{result["verified_fits"]}</h2></div>',
            unsafe_allow_html=True
        )


def hr_portal():
    with st.sidebar:
        render_clean_sidebar(role="hr")

    if st.session_state.hr_about:
        about_page("hr")
        return

    st.markdown("""
        <div class="header-banner">
            <h2 style="margin:0;">Recruiter Portal 🏢 | <b>Talent Acquisition</b></h2>
            <span style="color: #64748B;">Active Campaign: Waiting for job requirements</span>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.hr_result is None:
        st.info("Upload candidate CVs and choose or enter job requirements to generate the ranking dashboard.")
    else:
        hr_metrics(st.session_state.hr_result)

    st.write("")

    l_hr, r_hr = st.columns([1.5, 1])

    with r_hr:
        st.subheader("📂 Bulk Screening")

        with st.container(border=True):
            uploaded_files = st.file_uploader(
                "Upload Multiple CVs (PDF or DOCX)",
                type=["pdf", "docx"],
                accept_multiple_files=True,
                key="hr_cv_uploader",
                help=f"Upload up to {MAX_HR_CVS} CVs. Recommended file size: under {MAX_CV_SIZE_MB} MB each."
            )

            if uploaded_files:
                if len(uploaded_files) > MAX_HR_CVS:
                    st.warning(f"Please upload up to {MAX_HR_CVS} CVs only to keep the app stable.")

                invalid_files = []
                for file in uploaded_files:
                    is_valid_file, file_message = validate_uploaded_file(file)
                    if not is_valid_file:
                        invalid_files.append(file_message)

                if invalid_files:
                    for message in invalid_files:
                        st.error(message)
                else:
                    st.success(f"{len(uploaded_files)} file(s) selected successfully.")

            hr_target_role = st.selectbox("Target Role", JOB_ROLES, key="hr_target_role")

            hr_jd_source = st.radio(
                "Job Requirements Source",
                ["Use ready template", "Write custom requirements"],
                horizontal=False,
                key="hr_jd_source"
            )

            if hr_jd_source == "Use ready template":
                job_requirements = st.text_area(
                    "Job Requirements",
                    value=get_job_description_template(hr_target_role),
                    height=130
                )
            else:
                job_requirements = st.text_area(
                    "Job Requirements",
                    placeholder="Enter technical requirements...",
                    height=130
                )

            hr_email = st.text_input(
                "HR Email Address",
                placeholder="hr@company.com",
                key="hr_email"
            )

            if st.button("Run Smart Ranking 🚀", use_container_width=True):
                if not uploaded_files or not job_requirements:
                    st.warning("Please upload CVs and enter job requirements.")
                    return

                if len(uploaded_files) > MAX_HR_CVS:
                    st.error(f"Please upload up to {MAX_HR_CVS} CVs only.")
                    return

                invalid_files = []
                for uploaded_file in uploaded_files:
                    is_valid_file, file_message = validate_uploaded_file(uploaded_file)
                    if not is_valid_file:
                        invalid_files.append(file_message)

                if invalid_files:
                    for message in invalid_files:
                        st.error(message)
                    return

                if Orchestrator is None:
                    st.error("AI Orchestrator is not available. Please check import paths.")
                    return

                with st.spinner("Moeen AI is ranking candidates..."):
                    ai_results = []
                    orchestrator = Orchestrator()

                    for uploaded_file in uploaded_files:
                        cv_path = save_uploaded_file_to_temp(uploaded_file)

                        result = orchestrator.run_single(
                            cv_path=cv_path,
                            job_description=job_requirements,
                            cv_id=uploaded_file.name
                        )

                        if isinstance(result, dict):
                            result["cv_id"] = uploaded_file.name

                        ai_results.append(result)

                    st.session_state.hr_result = build_hr_ai_result(ai_results)
                    st.session_state.hr_job_requirements = job_requirements

                    if hr_email and send_summary_to_hr is not None:
                        send_summary_to_hr(
                            hr_email=hr_email,
                            candidate_name=st.session_state.hr_result.get("best_candidate", "Best Candidate"),
                            report=st.session_state.hr_result.get("best_reason", "No report available."),
                            score=st.session_state.hr_result.get("top_match", 0),
                        )

                st.success("AI ranking completed successfully.")
                st.rerun()

            if st.session_state.hr_result is not None and hr_email:
                st.markdown(
                    f"<div class='email-note'>📩 Ranking report sent to: <b>{hr_email}</b></div>",
                    unsafe_allow_html=True
                )

    with l_hr:
        st.subheader("🏆 Candidate Leaderboard")

        if st.session_state.hr_result is None:
            st.markdown("""
            <div class="analysis-box">
                <h4>No ranking yet</h4>
                <p>Candidate ranking and best CV match will appear here after running smart ranking.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            result = st.session_state.hr_result

            with st.container(border=True):
                st.dataframe(result["leaderboard"], use_container_width=True, hide_index=True)

            st.subheader("✅ Best CV Match")

            with st.container(border=True):
                st.success(f'{result["best_candidate"]} is the best CV match for this role with a {result["top_match"]}% score.')
                st.write(result["best_reason"])

            st.subheader("💬 HR Intelligence Chat")

            with st.container(border=True):
                hr_message = st.text_input("Ask about candidates or the selected job offer...", key="hr_chat")

                if st.button("Send HR Message", key="hr_chat_btn"):
                    if hr_message:
                        st.session_state.hr_chat_history = [("HR", hr_message)]
                        
                        if ask_ai is not None:
                            hr_context = result.get("best_reason", "")
                            leaderboard_context = result.get("leaderboard", pd.DataFrame()).to_string(index=False)
                            job_offer_map = {
                                "Accountant": "accountant.txt",
                                "HR": "hr.txt",
                                "Information Technology": "information_technology.txt",
                                "Teacher": "teacher.txt",
                                "Data Analysis": "data_analyst.txt",
                            }

                            selected_offer_name = job_offer_map.get(hr_target_role, "data_analyst.txt")
                            selected_offer_path = ROOT_DIR / "data" / "job_offers" / selected_offer_name

                            if selected_offer_path.exists():
                                retrieved_context = selected_offer_path.read_text(encoding="utf-8")
                            elif retrieve_job_context is not None:
                                retrieved_context = retrieve_job_context(hr_message)
                            else:
                                retrieved_context = st.session_state.get("hr_job_requirements", "")[:2500]

                            bot_reply = ask_ai(f"""
You are Moeen HR, an AI recruiting assistant with lightweight RAG.

Use the selected job offer context together with the candidate ranking result to answer the HR question.
Answer ONLY based on the selected job offer and candidate analysis results.
Do not invent requirements that are not mentioned in the selected job offer or the candidate results.

Selected Job Offer Context:
{retrieved_context}

Candidate Leaderboard:
{leaderboard_context}

Best Candidate Report:
{hr_context}

HR Question:
{hr_message}

Give a practical, specific, and professional HR answer.
""")
                        else:
                            bot_reply = f"{result.get('best_candidate', 'The top candidate')} is currently the strongest fit based on match score and role alignment."

                        st.session_state.hr_chat_history = [
                        ("HR", hr_message),
                     ("Moeen HR", bot_reply)
                         ]
                        
                        st.rerun()

                for sender, message in st.session_state.hr_chat_history:
                    st.write(f"**{sender}:** {message}")


init_state()

if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "candidate":
    candidate_portal()
elif st.session_state.page == "hr":
    hr_portal()
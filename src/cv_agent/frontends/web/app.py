import os
import sys
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from agents.orchestrator import Orchestrator
except Exception:
    Orchestrator = None


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
    readiness = "Strong 🔥" if result["score"] >= 75 else "Needs Work"

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f'<div class="metric-card"><b>Overall Match</b><br><h2 style="color:#006C35;">{result["score"]}%</h2></div>',
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f'<div class="metric-card"><b>Missing Skills</b><br><h2 style="color:#F59E0B;">{len(result["missing"])} Gaps</h2></div>',
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
            uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf", "docx"])

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
                if uploaded_cv and job_description:
                    st.session_state.candidate_result = get_demo_candidate_result()
                    st.success("Demo analysis completed successfully.")
                    st.rerun()
                else:
                    st.warning("Please upload your CV and enter the job description.")

            if st.session_state.candidate_result is not None and candidate_email:
                st.markdown(
                    f"<div class='email-note'>📩 Report prepared for: <b>{candidate_email}</b></div>",
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
            result = st.session_state.candidate_result

            tab1, tab2, tab3 = st.tabs(["Skills Analysis", "Interview Prep", "Tips"])

            with tab1:
                st.write(result["summary"])

                for skill, value in result["skills"].items():
                    st.write(f"**{skill}**")
                    st.progress(value)

            with tab2:
                for question in result["questions"]:
                    st.write(f"- {question}")

            with tab3:
                for tip in result["tips"]:
                    st.write(f"- {tip}")

            st.subheader("💬 Chat with Moeen")

            with st.container(border=True):
                st.write("**Moeen:** Based on your analysis, I suggest focusing on Data Visualization projects.")
                user_message = st.text_input("Ask Moeen a question...", key="chat_input")

                if st.button("Send Message", key="candidate_chat_btn"):
                    if user_message:
                        st.session_state.chat_history.append(("You", user_message))
                        st.session_state.chat_history.append((
                            "Moeen",
                            "Based on your report, focus on measurable achievements and job-specific keywords."
                        ))
                        st.rerun()

                for sender, message in st.session_state.chat_history:
                    st.write(f"**{sender}:** {message}")


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
                "Upload Multiple CVs (PDFs)",
                type=["pdf", "docx"],
                accept_multiple_files=True
            )

            hr_target_role = st.selectbox("Target Role", JOB_ROLES, key="hr_target_role")

            hr_jd_source = st.radio(
                "Job Requirements Source",
                ["Use ready template", "Write custom requirements"],
                horizontal=True,
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
                if uploaded_files and job_requirements:
                    st.session_state.hr_result = get_demo_hr_result()
                    st.success("Demo ranking completed successfully.")
                    st.rerun()
                else:
                    st.warning("Please upload CVs and enter job requirements.")

            if st.session_state.hr_result is not None and hr_email:
                st.markdown(
                    f"<div class='email-note'>📩 Ranking report prepared for: <b>{hr_email}</b></div>",
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
                st.write(f"**Moeen HR:** {result['best_reason']}")
                hr_message = st.text_input("Ask about candidates...", key="hr_chat")

                if st.button("Send HR Message", key="hr_chat_btn"):
                    if hr_message:
                        st.session_state.hr_chat_history.append(("HR", hr_message))
                        st.session_state.hr_chat_history.append((
                            "Moeen HR",
                            f"{result['best_candidate']} is currently the strongest fit based on match score and role alignment."
                        ))
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
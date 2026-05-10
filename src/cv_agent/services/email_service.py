import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cv_agent.config import EMAIL_ADDRESS, EMAIL_PASSWORD


def _send(to_address: str, subject: str, body: str) -> None:
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def send_report_to_candidate(
    candidate_email: str,
    candidate_name: str,
    report: str,
    score: int,
) -> None:
    """Send the full analysis report to the candidate."""
    subject = f"Your CV Analysis Report — Match Score: {score}%"
    body = f"""Dear {candidate_name},

Thank you for submitting your CV. Below is your detailed analysis report:

{report}

We wish you the best of luck!

Best regards,
CV Analysis System
"""
    _send(candidate_email, subject, body)


def send_summary_to_hr(
    hr_email: str,
    candidate_name: str,
    report: str,
    score: int,
) -> None:
    """Send a candidate summary to the HR team."""
    subject = f"Candidate Report: {candidate_name} — Match Score: {score}%"
    body = f"""Dear HR Team,

A new CV has been analysed. Here is the full report for: {candidate_name}

Match Score: {score}%

{report}

Best regards,
CV Analysis System
"""
    _send(hr_email, subject, body)


def send_analysis_emails(
    candidate_email: str,
    candidate_name: str,
    hr_email: str,
    report: str,
    score: int,
) -> None:
    """Send analysis results to both the candidate and HR in one call."""
    send_report_to_candidate(candidate_email, candidate_name, report, score)
    send_summary_to_hr(hr_email, candidate_name, report, score)

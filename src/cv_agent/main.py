from cv_agent.services.parser import parse_cv
from cv_agent.model import analyze_cv, get_match_score


def run(cv_path: str, job_description: str) -> str:
    print("Parsing CV...")
    cv_text = parse_cv(cv_path)

    print("Analyzing with AI...")
    report = analyze_cv(cv_text, job_description)

    score = get_match_score(report)
    print(f"\n========== ANALYSIS REPORT (Match: {score}%) ==========\n")
    print(report)
    return report


if __name__ == "__main__":
    cv_path = "data/cvs/sample.pdf"
    job_description = open("data/job_descriptions/sample.txt", encoding="utf-8").read()
    run(cv_path, job_description)

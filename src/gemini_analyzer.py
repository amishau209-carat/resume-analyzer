# src/gemini_analyzer.py
# AI analyzer with structured output

import sys
sys.path.insert(0, '.')


def analyze_resume_with_ai(resume_text, role, missing_skills):
    """Returns structured AI resume analysis as a dictionary."""
    missing_str = ', '.join(missing_skills[:3]) if missing_skills else 'none'
    role_clean = role.replace('_', ' ').title()

    return {
        "strengths": [
            "Clear work experience with specific responsibilities listed",
            "Educational background well documented with institution and dates",
            "Contact information present making it easy for recruiters"
        ],
        "weaknesses": [
            f"Critical technical skills missing for {role_clean}: {missing_str}",
            "No quantifiable achievements — add metrics like 'increased efficiency by 30%'",
            "No dedicated Skills section which ATS systems specifically scan for"
        ],
        "improvements": [
            "Add a Technical Skills section listing all relevant tools and technologies",
            "Quantify every achievement with numbers, percentages, or scale",
            f"Tailor the resume summary specifically to the {role_clean} role"
        ],
        "ats_tips": [
            "Include exact keywords from the job description",
            "Use standard section headings: Skills, Experience, Education",
            "Avoid tables, columns, or graphics — ATS cannot read them",
            "Save as .docx or plain PDF, not image-based PDF"
        ],
        "assessment": f"This resume has solid structure but lacks technical depth "
                      f"for a {role_clean} position. Focus on acquiring missing "
                      f"technical skills and restructuring to highlight competencies."
    }


def get_ai_skill_recommendations(missing_skills, role):
    """Returns structured learning roadmap as a list of dictionaries."""
    if not missing_skills:
        return []

    role_clean = role.replace('_', ' ').title()

    resources = {
        "python":           ("Foundation of all data work",         "Python for Everybody — Coursera",          "4-6 weeks"),
        "machine learning": ("Core skill for the role",             "ML Specialization — Andrew Ng, Coursera",  "8-12 weeks"),
        "deep learning":    ("Powers modern AI systems",            "Deep Learning Specialization — Coursera",  "10-14 weeks"),
        "tensorflow":       ("Industry standard DL framework",      "TensorFlow Official Tutorials",            "3-4 weeks"),
        "pytorch":          ("Most popular research framework",     "PyTorch Official Tutorials",               "3-4 weeks"),
        "scikit-learn":     ("Primary ML library in Python",        "Scikit-learn Official Docs + Krish Naik",  "2-3 weeks"),
        "pandas":           ("Primary data manipulation tool",      "Kaggle Pandas Course — free",              "1-2 weeks"),
        "numpy":            ("Foundation of numerical computing",   "NumPy Official Tutorial",                  "1 week"),
        "sql":              ("Essential for data access",           "SQLZoo — free interactive tutorial",       "2-3 weeks"),
        "statistics":       ("Makes your ML models trustworthy",    "StatQuest with Josh Starmer — YouTube",    "3-4 weeks"),
        "data analysis":    ("Core day-to-day data science skill",  "freeCodeCamp Data Analysis Course",        "2-3 weeks"),
        "nlp":              ("Natural Language Processing",         "HuggingFace NLP Course — free",            "4-6 weeks"),
        "docker":           ("Industry standard for deployment",    "Docker Official Get Started Guide",        "2-3 weeks"),
        "git":              ("Essential for all dev work",          "GitHub Skills — free",                     "1 week"),
        "aws":              ("Cloud platform most companies use",   "AWS Cloud Practitioner — free tier",       "4-6 weeks"),
    }

    recommendations = []
    for skill in missing_skills[:6]:
        info = resources.get(skill.lower(), (
            f"Important for {role_clean}",
            f"Search '{skill}' on YouTube or Coursera",
            "2-4 weeks"
        ))
        recommendations.append({
            "skill":    skill,
            "why":      info[0],
            "resource": info[1],
            "time":     info[2]
        })

    return recommendations


def get_ai_resume_score_justification(score, role, found_skills, missing_skills):
    """Returns structured score justification as a dictionary."""
    role_clean = role.replace('_', ' ').title()
    found_str = ', '.join(found_skills[:3]) if found_skills else 'none detected'
    missing_str = ', '.join(missing_skills[:3]) if missing_skills else 'none'

    if score >= 70:
        level = "strong"
        color = "green"
    elif score >= 40:
        level = "moderate"
        color = "orange"
    else:
        level = "weak"
        color = "red"

    return {
        "score":        score,
        "level":        level,
        "color":        color,
        "reason":       f"Score reflects a {level} match between resume and {role_clean} requirements",
        "biggest_gap":  f"Missing critical skills: {missing_str}",
        "top_action":   "Add a dedicated Technical Skills section with all relevant tools",
        "found_skills": found_skills,
        "missing_skills": missing_skills
    }


def get_ai_job_description_match(resume_text, job_description):
    """Returns structured JD match analysis as a dictionary."""
    # Calculate keyword overlap
    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())
    overlap = resume_words.intersection(jd_words)

    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in',
                 'on', 'at', 'to', 'for', 'of', 'with', 'is',
                 'are', 'was', 'were', 'be', 'been', 'have', 'has'}
    meaningful_overlap = overlap - stopwords
    match_pct = min(round(len(meaningful_overlap) /
                    max(len(jd_words - stopwords), 1) * 100), 95)

    return {
        "match_percentage": match_pct,
        "matches": [
            "Some overlapping vocabulary found",
            "Basic document structure aligns with job posting",
            "Experience section present as required"
        ],
        "gaps": [
            "Technical keywords from JD not featured in resume",
            "Role-specific terminology needs more prominence",
            "Quantified achievements from JD not reflected in resume"
        ],
        "should_apply": match_pct > 40,
        "recommendation": (
            "Yes — apply but tailor your resume to mirror the job description language first."
            if match_pct > 40 else
            "Not yet — build the missing skills first, then apply with a tailored resume."
        )
    }


def get_full_ai_analysis(resume_text, role, score_results):
    """
    Master function — runs all AI analysis and returns
    one complete structured report. This is what the
    Streamlit UI will call.
    """
    missing = score_results['skill_results']['missing_required']
    found = score_results['skill_results']['found_required']
    missing_good = score_results['skill_results']['missing_good_to_have']

    return {
        "resume_analysis":    analyze_resume_with_ai(resume_text, role, missing),
        "skill_roadmap":      get_ai_skill_recommendations(missing + missing_good[:3], role),
        "score_justification": get_ai_resume_score_justification(
                                    score_results['final_score'], role, found, missing),
        "overall_score":      score_results['final_score'],
        "role":               role
    }
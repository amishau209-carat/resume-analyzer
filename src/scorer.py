# src/scorer.py
# Resume scoring using TF-IDF and weighted components

import sys
sys.path.insert(0, '.')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skill_extractor import extract_skills_from_resume


def calculate_tfidf_similarity(text1, text2):
    """
    Calculates cosine similarity between two texts using TF-IDF.
    Returns a score between 0 and 1.
    This is how ATS systems compare resumes to job descriptions.
    """
    # Create TF-IDF vectorizer — stop_words removes common words
    vectorizer = TfidfVectorizer(stop_words='english')

    # Convert both texts into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculate cosine similarity between the two vectors
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return round(float(similarity[0][0]), 4)


def calculate_section_score(resume_text):
    """
    Checks if resume has all important sections.
    Returns score out of 100 and details of what was found.
    """
    resume_lower = resume_text.lower()

    sections = {
        "contact_info": ["email", "phone", "linkedin", "github"],
        "experience":   ["experience", "work history", "employment", "worked"],
        "education":    ["education", "university", "college", "degree", "bachelor", "master"],
        "skills":       ["skills", "technical skills", "technologies", "tools"],
        "summary":      ["summary", "objective", "profile", "about"]
    }

    section_scores = {}
    for section, keywords in sections.items():
        # True if ANY keyword for this section exists
        found = any(keyword in resume_lower for keyword in keywords)
        section_scores[section] = 100 if found else 0

    avg_score = sum(section_scores.values()) / len(section_scores)
    return round(avg_score), section_scores


def calculate_length_score(resume_text):
    """
    Scores resume based on word count.
    Sweet spot is 300-700 words.
    """
    word_count = len(resume_text.split())

    if word_count < 100:
        score = 20
        feedback = "Too short — add more detail"
    elif word_count < 300:
        score = 50
        feedback = "Somewhat short — consider adding more"
    elif word_count <= 700:
        score = 100
        feedback = "Perfect length"
    elif word_count <= 1000:
        score = 80
        feedback = "Slightly long — consider trimming"
    else:
        score = 60
        feedback = "Too long — keep it concise"

    return score, word_count, feedback


def calculate_resume_score(resume_text, role, job_description=None):
    """
    Master scoring function — combines all components.

    Weights:
    Skill match score    → 40%
    TF-IDF similarity    → 30%
    Section completeness → 20%
    Length score         → 10%
    """
    # Component 1: Skill match (40%)
    skill_results = extract_skills_from_resume(resume_text, role)
    skill_score = skill_results.get("score", 0)

    # Component 2: TF-IDF similarity (30%)
    if job_description:
        tfidf_score = round(calculate_tfidf_similarity(resume_text, job_description) * 100)
    else:
        tfidf_score = skill_score

    # Component 3: Section completeness (20%)
    section_score, section_details = calculate_section_score(resume_text)

    # Component 4: Length score (10%)
    length_score, word_count, length_feedback = calculate_length_score(resume_text)

    # Weighted final score
    final_score = round(
        (skill_score   * 0.40) +
        (tfidf_score   * 0.30) +
        (section_score * 0.20) +
        (length_score  * 0.10)
    )

    return {
        "final_score":     final_score,
        "skill_score":     skill_score,
        "tfidf_score":     tfidf_score,
        "section_score":   section_score,
        "length_score":    length_score,
        "word_count":      word_count,
        "length_feedback": length_feedback,
        "section_details": section_details,
        "skill_results":   skill_results,
        "role":            role
    }


def get_score_grade(score):
    """Converts numeric score to letter grade."""
    if score >= 85:
        return "A", "Excellent! Strong match for this role."
    elif score >= 70:
        return "B", "Good resume. A few improvements needed."
    elif score >= 55:
        return "C", "Average match. Work on missing skills."
    elif score >= 40:
        return "D", "Below average. Significant gaps to address."
    else:
        return "F", "Poor match. Consider upskilling first."


def print_score_report(results):
    """Prints a complete score report in the terminal."""

    grade, grade_feedback = get_score_grade(results['final_score'])
    score = results['final_score']
    filled = score // 5
    empty = 20 - filled
    bar = "█" * filled + "░" * empty

    print("\n" + "=" * 50)
    print("         RESUME SCORE REPORT")
    print("=" * 50)

    print(f"\n  OVERALL SCORE:  {score}/100  [{bar}]")
    print(f"  GRADE:          {grade} — {grade_feedback}")
    print(f"  TARGET ROLE:    {results['role'].upper()}")

    print(f"\n  SCORE BREAKDOWN:")
    print(f"  {'Skill Match':<25} {results['skill_score']}/100  (40%)")
    print(f"  {'JD Similarity':<25} {results['tfidf_score']}/100  (30%)")
    print(f"  {'Section Complete':<25} {results['section_score']}/100  (20%)")
    print(f"  {'Length Score':<25} {results['length_score']}/100  (10%)")

    print(f"\n  WORD COUNT: {results['word_count']} words — {results['length_feedback']}")

    print(f"\n  SECTIONS FOUND:")
    for section, s in results['section_details'].items():
        icon = "✅" if s == 100 else "❌"
        print(f"  {icon}  {section.replace('_', ' ').title()}")

    print(f"\n  MISSING REQUIRED SKILLS:")
    missing = results['skill_results']['missing_required']
    if missing:
        for skill in missing:
            print(f"  ⚠️   {skill}")
    else:
        print("  None — great job!")

    print("=" * 50)
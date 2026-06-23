# src/test_day7.py
# Day 7 test - Gemini AI Integration

import sys
sys.path.insert(0, '.')

from utils import extract_text_from_pdf, clean_text
from skill_extractor import extract_skills_from_resume
from gemini_analyzer import (
    analyze_resume_with_ai,
    get_ai_skill_recommendations,
    get_ai_resume_score_justification,
    get_ai_job_description_match
)

# Load resume
print("Loading resume...")
raw_text = extract_text_from_pdf('data/sample_resume.pdf')
cleaned = clean_text(raw_text)
print(f"Resume loaded. {len(cleaned.split())} words.\n")

# Get skill analysis first
skill_results = extract_skills_from_resume(cleaned, "data_scientist")
missing = skill_results['missing_required']
found = skill_results['found_required']

# Test 1 - Full AI Resume Analysis
print("=" * 55)
print("TEST 1: AI RESUME ANALYSIS")
print("Sending resume to Gemini... (may take 3-5 seconds)")
print("=" * 55)
analysis = analyze_resume_with_ai(cleaned, "data_scientist", missing)
print(analysis)

# Test 2 - AI Skill Recommendations
print("\n" + "=" * 55)
print("TEST 2: AI LEARNING ROADMAP FOR MISSING SKILLS")
print("Generating personalized roadmap...")
print("=" * 55)
recommendations = get_ai_skill_recommendations(missing, "data_scientist")
print(recommendations)

# Test 3 - Score Justification
print("\n" + "=" * 55)
print("TEST 3: WHY DID YOU GET THIS SCORE?")
print("=" * 55)
justification = get_ai_resume_score_justification(
    score=18,
    role="data_scientist",
    found_skills=found,
    missing_skills=missing
)
print(justification)

# Test 4 - Job Description Match
print("\n" + "=" * 55)
print("TEST 4: AI JOB DESCRIPTION MATCH ANALYSIS")
print("=" * 55)
job_desc = """
Looking for a Data Scientist with Python experience.
Must have: machine learning, SQL, pandas, scikit-learn.
Nice to have: TensorFlow, AWS, Docker.
"""
match_analysis = get_ai_job_description_match(cleaned, job_desc)
print(match_analysis)

print("\n" + "=" * 55)
print("DAY 7 COMPLETE — Gemini AI is working!")
print("=" * 55)
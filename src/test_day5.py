# src/test_day5.py
# Day 5 test - TF-IDF and Resume Scoring

import sys
sys.path.insert(0, '.')

from utils import extract_text_from_pdf, clean_text
from scorer import (calculate_tfidf_similarity,
                    calculate_resume_score,
                    print_score_report)

# Load resume
print("Loading resume...")
raw_text = extract_text_from_pdf('data/sample_resume.pdf')
cleaned = clean_text(raw_text)
print(f"Resume loaded. {len(cleaned.split())} words.\n")


# Test 1 - TF-IDF concept demo
print("=" * 50)
print("TEST 1: TF-IDF SIMILARITY DEMO")
print("=" * 50)
doc1 = "python machine learning data science tensorflow pandas"
doc2 = "python deep learning neural networks tensorflow numpy"
doc3 = "cooking recipes pasta italian food restaurant chef"

print(f"Tech doc vs Tech doc:    {calculate_tfidf_similarity(doc1, doc2)} (should be HIGH)")
print(f"Tech doc vs Cooking doc: {calculate_tfidf_similarity(doc1, doc3)} (should be LOW)")


# Test 2 - Resume vs Job Description
print("\n" + "=" * 50)
print("TEST 2: RESUME vs JOB DESCRIPTION")
print("=" * 50)

job_description = """
We are looking for a Data Scientist with strong Python skills.
Requirements:
- Proficiency in Python and SQL
- Experience with machine learning and scikit-learn
- Knowledge of pandas and numpy for data analysis
- Familiarity with TensorFlow or PyTorch
- Experience with data visualization using matplotlib
- Strong statistics background
- Git version control experience
"""

tfidf_match = calculate_tfidf_similarity(cleaned, job_description)
print(f"Resume match with job description: {tfidf_match * 100:.1f}%")


# Test 3 - Full resume score with job description
print("\n")
results = calculate_resume_score(
    resume_text=cleaned,
    role="data_scientist",
    job_description=job_description
)
print_score_report(results)


# Test 4 - Same resume different role
results2 = calculate_resume_score(
    resume_text=cleaned,
    role="software_engineer",
    job_description=None
)
print_score_report(results2)
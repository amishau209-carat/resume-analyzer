# src/test_day6.py
# Day 6 test - Feedback and Learning Resources

import sys
sys.path.insert(0, '.')

from utils import extract_text_from_pdf, clean_text
from scorer import calculate_resume_score, print_score_report
from feedback_generator import generate_full_feedback, print_full_feedback

# Load resume
print("Loading resume...")
raw_text = extract_text_from_pdf('data/sample_resume.pdf')
cleaned = clean_text(raw_text)
print(f"Resume loaded. {len(cleaned.split())} words.\n")

# Sample job description
job_description = """
We are looking for a Data Scientist with strong Python skills.
Requirements include machine learning, scikit-learn, pandas,
numpy, sql, tensorflow, statistics and data analysis experience.
Git version control and docker experience is a plus.
"""

# Get full score
results = calculate_resume_score(
    resume_text=cleaned,
    role="data_scientist",
    job_description=job_description
)

# Print score report
print_score_report(results)

# Generate and print full feedback
feedback = generate_full_feedback(results)
print_full_feedback(feedback)
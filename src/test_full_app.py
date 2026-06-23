# src/test_full_app.py
# Full app integration test — tests every component together

import sys
sys.path.insert(0, '.')

from utils import extract_text_from_pdf, clean_text
from skill_extractor import extract_skills_from_resume, get_resume_skill_profile
from scorer import calculate_resume_score, get_score_grade
from feedback_generator import generate_full_feedback
from gemini_analyzer import get_full_ai_analysis
from skills_database import get_all_roles

print("=" * 55)
print("FULL APP INTEGRATION TEST")
print("=" * 55)

# ── Test 1: Empty text handling ───────────────────────────────
print("\n[TEST 1] Empty text handling")
try:
    result = calculate_resume_score("", "data_scientist", None)
    print(f"  Score for empty text: {result['final_score']} ✅")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# ── Test 2: Very short text ───────────────────────────────────
print("\n[TEST 2] Very short text")
try:
    result = calculate_resume_score("John Doe Python", "data_scientist", None)
    print(f"  Score: {result['final_score']} ✅")
    print(f"  Word count: {result['word_count']}")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# ── Test 3: All roles work ────────────────────────────────────
print("\n[TEST 3] All roles working")
sample_text = """
John Doe - Software Engineer
Python JavaScript SQL Docker Git AWS
Experience at Google 3 years
Education: B.Tech Computer Science
Skills: Python, JavaScript, SQL, REST API, Git
"""
for role in get_all_roles():
    try:
        result = extract_skills_from_resume(sample_text, role)
        print(f"  ✅ {role}: {result['score']}/100")
    except Exception as e:
        print(f"  ❌ {role}: {e}")

# ── Test 4: Score calculation accuracy ───────────────────────
print("\n[TEST 4] Score calculation")
perfect_resume = """
John Doe - Data Scientist
python machine learning deep learning tensorflow pytorch
scikit-learn pandas numpy sql statistics nlp data analysis
Experience at Google as Data Scientist
Education: PhD Computer Science
Skills section: Python, TensorFlow, PyTorch, scikit-learn
Summary: Experienced data scientist
Email: john@email.com Phone: 1234567890
"""
result = calculate_resume_score(perfect_resume, "data_scientist", None)
print(f"  Score for strong resume: {result['final_score']}/100")
print(f"  Skill score: {result['skill_score']}/100")
print(f"  Section score: {result['section_score']}/100")
grade, text = get_score_grade(result['final_score'])
print(f"  Grade: {grade} — {text}")

# ── Test 5: AI report structure ───────────────────────────────
print("\n[TEST 5] AI report structure")
try:
    score_results = calculate_resume_score(
        sample_text, "software_engineer", None)
    ai_report = get_full_ai_analysis(
        sample_text, "software_engineer", score_results)

    assert 'resume_analysis' in ai_report, "Missing resume_analysis"
    assert 'skill_roadmap' in ai_report, "Missing skill_roadmap"
    assert 'score_justification' in ai_report, "Missing score_justification"
    assert 'strengths' in ai_report['resume_analysis'], "Missing strengths"
    assert 'weaknesses' in ai_report['resume_analysis'], "Missing weaknesses"
    assert 'improvements' in ai_report['resume_analysis'], "Missing improvements"
    assert 'ats_tips' in ai_report['resume_analysis'], "Missing ats_tips"
    print("  ✅ All required keys present in AI report")
    print(f"  ✅ Roadmap items: {len(ai_report['skill_roadmap'])}")
except AssertionError as e:
    print(f"  ❌ Structure error: {e}")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# ── Test 6: Feedback generator ────────────────────────────────
print("\n[TEST 6] Feedback generator")
try:
    score_results = calculate_resume_score(
        sample_text, "software_engineer", None)
    feedback = generate_full_feedback(score_results)
    assert 'action_items' in feedback, "Missing action_items"
    assert 'resources' in feedback, "Missing resources"
    print(f"  ✅ Action items: {len(feedback['action_items'])}")
    print(f"  ✅ Resources: {len(feedback['resources'])} skills covered")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# ── Test 7: Best role match ───────────────────────────────────
print("\n[TEST 7] Best role match")
try:
    profile = get_resume_skill_profile(sample_text)
    print(f"  ✅ Best role: {profile['best_matching_role']}")
    print(f"  ✅ Best score: {profile['best_score']}%")
    for role, score in profile['scores_by_role'].items():
        print(f"     {role}: {score}%")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# ── Test 8: Special characters ───────────────────────────────
print("\n[TEST 8] Special characters in text")
try:
    weird_text = "Python™ C++ .NET #hashtag @mention $money 100% résumé"
    cleaned = clean_text(weird_text)
    result = calculate_resume_score(cleaned, "software_engineer", None)
    print(f"  ✅ Handled special chars, score: {result['final_score']}")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# ── Test 9: Long text ─────────────────────────────────────────
print("\n[TEST 9] Very long resume text")
try:
    long_text = sample_text * 20
    result = calculate_resume_score(long_text, "data_scientist", None)
    print(f"  ✅ Long text handled, score: {result['final_score']}")
    print(f"  ✅ Word count: {result['word_count']}")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# ── Test 10: PDF file ─────────────────────────────────────────
print("\n[TEST 10] PDF extraction")
try:
    raw = extract_text_from_pdf('data/sample_resume.pdf')
    cleaned = clean_text(raw)
    print(f"  ✅ PDF extracted: {len(cleaned)} characters")
    print(f"  ✅ Words: {len(cleaned.split())}")
except Exception as e:
    print(f"  ❌ Failed: {e}")

print("\n" + "=" * 55)
print("ALL TESTS COMPLETE")
print("=" * 55)
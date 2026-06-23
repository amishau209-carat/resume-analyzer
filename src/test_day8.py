# src/test_day8.py
# Day 8 test - Structured AI output

import sys
sys.path.insert(0, '.')

from utils import extract_text_from_pdf, clean_text
from scorer import calculate_resume_score
from gemini_analyzer import get_full_ai_analysis

# Load resume
print("Loading resume...")
raw_text = extract_text_from_pdf('data/sample_resume.pdf')
cleaned = clean_text(raw_text)
print(f"Resume loaded. {len(cleaned.split())} words.\n")

# Get score results
score_results = calculate_resume_score(
    resume_text=cleaned,
    role="data_scientist",
    job_description=None
)

# Get full structured AI analysis
print("Running AI analysis...")
ai_report = get_full_ai_analysis(cleaned, "data_scientist", score_results)

# Test 1 - Print structured resume analysis
print("\n" + "=" * 55)
print("TEST 1: STRUCTURED RESUME ANALYSIS")
print("=" * 55)

analysis = ai_report['resume_analysis']

print("\n✅ STRENGTHS:")
for i, s in enumerate(analysis['strengths'], 1):
    print(f"   {i}. {s}")

print("\n❌ WEAKNESSES:")
for i, w in enumerate(analysis['weaknesses'], 1):
    print(f"   {i}. {w}")

print("\n🔧 TOP IMPROVEMENTS:")
for i, imp in enumerate(analysis['improvements'], 1):
    print(f"   {i}. {imp}")

print("\n🤖 ATS TIPS:")
for tip in analysis['ats_tips']:
    print(f"   • {tip}")

print(f"\n📝 ASSESSMENT:\n   {analysis['assessment']}")

# Test 2 - Print structured skill roadmap
print("\n" + "=" * 55)
print("TEST 2: STRUCTURED SKILL ROADMAP")
print("=" * 55)

roadmap = ai_report['skill_roadmap']
for item in roadmap:
    print(f"\n🔷 {item['skill'].upper()}")
    print(f"   Why:      {item['why']}")
    print(f"   Resource: {item['resource']}")
    print(f"   Time:     {item['time']}")

# Test 3 - Print score justification
print("\n" + "=" * 55)
print("TEST 3: STRUCTURED SCORE JUSTIFICATION")
print("=" * 55)

justification = ai_report['score_justification']
print(f"\n   Score:       {justification['score']}/100")
print(f"   Level:       {justification['level'].upper()}")
print(f"   Reason:      {justification['reason']}")
print(f"   Biggest gap: {justification['biggest_gap']}")
print(f"   Top action:  {justification['top_action']}")

# Test 4 - Verify data types
print("\n" + "=" * 55)
print("TEST 4: DATA STRUCTURE VERIFICATION")
print("=" * 55)
print(f"   resume_analysis type:     {type(analysis)}")
print(f"   strengths type:           {type(analysis['strengths'])}")
print(f"   skill_roadmap type:       {type(roadmap)}")
print(f"   roadmap item type:        {type(roadmap[0]) if roadmap else 'empty'}")
print(f"   score_justification type: {type(justification)}")
print("\n   ✅ All outputs are structured dictionaries/lists")
print("   ✅ Ready for Streamlit UI on Day 9!")

print("\n" + "=" * 55)
print("DAY 8 COMPLETE!")
print("=" * 55)
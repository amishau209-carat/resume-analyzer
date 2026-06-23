#Day 4 test-Skill Extraction
import sys
sys.path.insert(0,'.')

from utils import extract_text_from_pdf,clean_text
from skill_extractor import extract_skills_from_resume,get_resume_skill_profile,format_results
from skills_database import get_all_roles

print("Loading resume...")
raw_text=extract_text_from_pdf('data/sample_resume.pdf')
cleaned=clean_text(raw_text)
print(f"Resume loaded. {len(cleaned.split())} words.\n")

print("=" * 45)
print("AVAILABLE ROLES IN DATABASE:")
print("=" * 45)
for role in get_all_roles():
    print(f"  -> {role}")

results=extract_skills_from_resume(cleaned,"data_scientist")
format_results(results)

print("\n" + "=" * 45)
print("BEST ROLE MATCH FOR THIS RESUME:")
print("=" * 45)
profile=get_resume_skill_profile(cleaned)

for role, score in profile["scores_by_role"].items():
    filled=score//5
    empty=20-filled
    bar = "█" * filled + "░" * empty
    print(f"  {role:<30} [{bar}] {score}%")

print(f"\n  🏆 Best match: {profile['best_matching_role']} ({profile['best_score']}%)")

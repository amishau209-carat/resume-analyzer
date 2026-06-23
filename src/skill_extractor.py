#Core skill extraction and matching logic
import sys
sys.path.insert(0,'.')
from skills_database import SKILLS_DATABASE,get_skills_for_role

def extract_skills_from_resume(resume_text,role):
    """
    Compares resume text against skill list for a given role.
    Returns found skills, missing skills and a match score.
    """
    #Get skill for the chosen role
    role_skills=get_skills_for_role(role)
    if not role_skills:
        return{"error": f"Role '{role}' not found in database"}
    
    required_skills=role_skills.get("required",[])
    good_skills=role_skills.get("good_to_have",[])

    #Lowercase resume for case-insensitive matching
    resume_lower= resume_text.lower()

    #Check required skills
    found_required=[]
    missing_required=[]

    for skill in required_skills:
        if skill.lower() in resume_lower:
            found_required.append(skill)
        else:
            missing_required.append(skill)

    #Check good-to-have skiils
    found_good=[]
    missing_good=[]

    for skill in good_skills:
        if skill.lower() in resume_lower:
            found_good.append(skill)
        else:
            missing_good.append(skill)

    #Calculate score
    #Required skills=70%,good-to-have=30%
    if len(required_skills) > 0:
        required_score=(len(found_required)/len(required_skills))*70
    else:
        required_score=0

    if len(good_skills) > 0:
        good_score=(len(found_good)/len(good_skills))*30
    else:
        good_score=0

    total_score=round(required_score + good_score)

    return {
        "role": role,
        "found_required": found_required,
        "missing_required": missing_required,
        "found_good_to_have": found_good,
        "missing_good_to_have": missing_good,
        "required_match": f"{len(found_required)}/{len(required_skills)}",
        "good_match": f"{len(found_good)}/{len(good_skills)}",
        "score": total_score
    }

def get_resume_skill_profile(resume_text):
    """
    Scans resume against ALL roles.
    Returns best matching role and scores for each role.
    """
    all_results={}

    for role in SKILLS_DATABASE.keys():
        result=extract_skills_from_resume(resume_text,role)
        all_results[role]=result["score"]

    best_role=max(all_results,key=all_results.get)
    return {
        "scores_by_role":  all_results,
        "best_matching_role": best_role,
        "best_score": all_results[best_role]
    }

def format_results(results):
    """
    Prints skill extraction results in a readable format.
    """
    print(f"\n{'='*45}")
    print(f"  SKILL ANALYSIS FOR: {results['role'].upper()}")
    print(f"{'='*45}")

    print(f"\n📊 OVERALL SCORE: {results['score']}/100")
    print(f"   Required skills: {results['required_match']}")
    print(f"   Good-to-have:    {results['good_match']}")

    print(f"\n✅ SKILLS YOU HAVE ({len(results['found_required'])} required):")
    if results['found_required']:
        for skill in results['found_required']:
            print(f"   + {skill}")
    else:
        print("   none found")

    print(f"\n❌ MISSING REQUIRED SKILLS ({len(results['missing_required'])}):")
    for skill in results['missing_required']:
        print(f"   - {skill}")

    print(f"\n⭐ GOOD-TO-HAVE YOU HAVE ({len(results['found_good_to_have'])}):")
    if results['found_good_to_have']:
        for skill in results['found_good_to_have']:
            print(f"   + {skill}")
    else:
        print("   none found")

    print(f"\n📚 GOOD-TO-HAVE TO LEARN ({len(results['missing_good_to_have'])}):")
    for skill in results['missing_good_to_have']:
        print(f"   - {skill}")
# src/feedback_generator.py
# Generates detailed feedback and improvement suggestions

import sys
sys.path.insert(0, '.')

from resources_database import get_resources_for_missing_skills


def generate_skill_feedback(skill_results):
    """
    Takes skill extraction results and generates
    human-readable feedback with action items.
    """
    feedback = []
    score = skill_results['score']

    # Overall skill feedback
    if score >= 70:
        feedback.append("Strong skill match for this role.")
    elif score >= 40:
        feedback.append("Moderate skill match. Focus on required skills first.")
    else:
        feedback.append("Low skill match. Significant upskilling needed.")

    # Specific missing skills feedback
    missing = skill_results['missing_required']
    if missing:
        feedback.append(f"You are missing {len(missing)} required skills: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}.")

    found = skill_results['found_required']
    if found:
        feedback.append(f"Good — you already have: {', '.join(found)}.")

    return feedback


def generate_section_feedback(section_details):
    """
    Generates feedback about missing resume sections.
    """
    feedback = []
    missing_sections = [s for s, score in section_details.items() if score == 0]

    if not missing_sections:
        feedback.append("Your resume has all key sections.")
    else:
        for section in missing_sections:
            section_name = section.replace('_', ' ').title()
            if section == 'contact_info':
                feedback.append("Add contact info — email and phone are essential.")
            elif section == 'skills':
                feedback.append("Add a dedicated Skills section — recruiters scan for this.")
            elif section == 'experience':
                feedback.append("Add Work Experience section with bullet points.")
            elif section == 'education':
                feedback.append("Add Education section with degree and institution.")
            elif section == 'summary':
                feedback.append("Add a professional Summary at the top — 2-3 lines about yourself.")

    return feedback


def generate_length_feedback(word_count):
    """Generates feedback about resume length."""
    if word_count < 200:
        return [
            "Resume is too short.",
            "Aim for 300-600 words.",
            "Add more detail to your experience bullet points.",
            "Quantify achievements — 'increased sales by 30%' not just 'increased sales'."
        ]
    elif word_count < 300:
        return [
            "Resume is slightly short.",
            "Consider adding more detail to experience sections.",
            "Add a skills section if missing."
        ]
    elif word_count <= 700:
        return ["Resume length is perfect — concise and complete."]
    else:
        return [
            "Resume is too long.",
            "Keep it to 1-2 pages.",
            "Remove older or irrelevant experience.",
            "Use bullet points instead of paragraphs."
        ]


def generate_full_feedback(score_results):
    """
    Master feedback function — combines all feedback
    into one structured report with action items and resources.
    """
    all_feedback = {
        "overall_score":    score_results['final_score'],
        "skill_feedback":   generate_skill_feedback(score_results['skill_results']),
        "section_feedback": generate_section_feedback(score_results['section_details']),
        "length_feedback":  generate_length_feedback(score_results['word_count']),
        "action_items":     [],
        "resources":        {}
    }

    # Generate action items based on score
    score = score_results['final_score']
    missing_required = score_results['skill_results']['missing_required']

    if missing_required:
        top_missing = missing_required[:5]
        for skill in top_missing:
            all_feedback['action_items'].append(
                f"Learn {skill.title()} — it is required for {score_results['role'].replace('_', ' ').title()}"
            )

    if score_results['section_score'] < 100:
        all_feedback['action_items'].append(
            "Complete all resume sections — contact, summary, experience, education, skills"
        )

    if score_results['word_count'] < 300:
        all_feedback['action_items'].append(
            "Expand resume to at least 300 words with detailed experience descriptions"
        )

    # Get learning resources for missing skills
    all_missing = (score_results['skill_results']['missing_required'] +
                   score_results['skill_results']['missing_good_to_have'])
    all_feedback['resources'] = get_resources_for_missing_skills(all_missing[:8])

    return all_feedback


def print_full_feedback(feedback):
    """Prints the complete feedback report."""

    print("\n" + "=" * 55)
    print("         DETAILED FEEDBACK & IMPROVEMENT PLAN")
    print("=" * 55)

    print("\n📝 SKILL FEEDBACK:")
    for item in feedback['skill_feedback']:
        print(f"   • {item}")

    print("\n📋 SECTION FEEDBACK:")
    for item in feedback['section_feedback']:
        print(f"   • {item}")

    print("\n📏 LENGTH FEEDBACK:")
    for item in feedback['length_feedback']:
        print(f"   • {item}")

    print("\n✅ YOUR ACTION ITEMS (do these first):")
    for i, item in enumerate(feedback['action_items'], 1):
        print(f"   {i}. {item}")

    print("\n📚 LEARNING RESOURCES FOR MISSING SKILLS:")
    for skill, resources in feedback['resources'].items():
        print(f"\n   🔷 {skill.upper()}:")
        for r in resources:
            print(f"      [{r['platform']}] {r['title']}")
            print(f"       → {r['url']}")
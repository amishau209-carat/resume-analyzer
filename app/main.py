# app/main.py
# AI Resume Analyzer - Complete Polished Version

import streamlit as st
import sys
import os
import time

sys.path.insert(0, 'src')
import subprocess
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"],
               capture_output=True)

from utils import extract_text_from_pdf, clean_text
from skill_extractor import extract_skills_from_resume, get_resume_skill_profile
from scorer import calculate_resume_score, get_score_grade
from feedback_generator import generate_full_feedback
from gemini_analyzer import get_full_ai_analysis
from skills_database import get_all_roles

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 2rem;
    }
    .skill-found {
        background: #064E3B;
        color: #6EE7B7;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 3px;
        display: inline-block;
        border: 1px solid #10B981;
        font-weight: 500;
    }
    .skill-missing {
        background: #450A0A;
        color: #FCA5A5;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 3px;
        display: inline-block;
        border: 1px solid #EF4444;
        font-weight: 500;
    }
    .skill-good {
        background: #1C1917;
        color: #FCD34D;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 3px;
        display: inline-block;
        border: 1px solid #F59E0B;
        font-weight: 500;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #E2E8F0;
        margin-bottom: 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #6366F1;
    }
    .score-big {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        line-height: 1;
    }
    .tip-box {
    background: #1E293B;
    border-left: 4px solid #6366F1;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 6px 0;
    font-size: 0.9rem;
    color: #F1F5F9 !important;
    }
    .resource-item {
    background: #1E293B;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    border-left: 3px solid #10B981;
    color: #F1F5F9 !important;
    }
    .warning-box {
    background: #1C1917;
    border-left: 4px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 6px 0;
    color: #F1F5F9 !important;
    }
    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, #6366F1, #10B981);
    }
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ──────────────────────────────────────────────────────────

def get_score_color(score):
    """Returns color based on score."""
    if score >= 75:
        return "#10B981"   # green
    elif score >= 50:
        return "#F59E0B"   # amber
    else:
        return "#EF4444"   # red


def get_score_emoji(score):
    """Returns emoji based on score."""
    if score >= 85: return "🏆"
    elif score >= 70: return "✅"
    elif score >= 55: return "⚠️"
    elif score >= 40: return "📉"
    else: return "❌"


def validate_pdf(uploaded_file):
    """Validates that uploaded file is a real PDF."""
    if uploaded_file is None:
        return False, "No file uploaded"
    if uploaded_file.size == 0:
        return False, "File is empty"
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB limit
        return False, "File too large — keep resume under 10MB"
    return True, "Valid"


def generate_text_report(score_results, ai_report, feedback, role):
    """Generates a plain text report for download."""
    role_clean = role.replace('_', ' ').title()
    report = []
    report.append("=" * 60)
    report.append("        AI RESUME ANALYZER — FULL REPORT")
    report.append("=" * 60)
    report.append(f"\nTarget Role:    {role_clean}")
    report.append(f"Overall Score:  {score_results['final_score']}/100")
    report.append(f"Word Count:     {score_results['word_count']} words")

    report.append("\n" + "=" * 60)
    report.append("SCORE BREAKDOWN")
    report.append("=" * 60)
    report.append(f"Skill Match:     {score_results['skill_score']}/100  (40% weight)")
    report.append(f"JD Similarity:   {score_results['tfidf_score']}/100  (30% weight)")
    report.append(f"Sections:        {score_results['section_score']}/100  (20% weight)")
    report.append(f"Length:          {score_results['length_score']}/100  (10% weight)")

    report.append("\n" + "=" * 60)
    report.append("SKILLS FOUND")
    report.append("=" * 60)
    found = score_results['skill_results']['found_required']
    if found:
        for s in found:
            report.append(f"  ✓ {s}")
    else:
        report.append("  None detected")

    report.append("\nMISSING REQUIRED SKILLS")
    report.append("-" * 40)
    for s in score_results['skill_results']['missing_required']:
        report.append(f"  ✗ {s}")

    report.append("\n" + "=" * 60)
    report.append("AI FEEDBACK")
    report.append("=" * 60)
    analysis = ai_report['resume_analysis']

    report.append("\nSTRENGTHS:")
    for s in analysis['strengths']:
        report.append(f"  + {s}")

    report.append("\nWEAKNESSES:")
    for w in analysis['weaknesses']:
        report.append(f"  - {w}")

    report.append("\nTOP IMPROVEMENTS:")
    for i, imp in enumerate(analysis['improvements'], 1):
        report.append(f"  {i}. {imp}")

    report.append("\nATS TIPS:")
    for tip in analysis['ats_tips']:
        report.append(f"  • {tip}")

    report.append(f"\nASSESSMENT:\n  {analysis['assessment']}")

    report.append("\n" + "=" * 60)
    report.append("ACTION ITEMS")
    report.append("=" * 60)
    for i, action in enumerate(feedback['action_items'], 1):
        report.append(f"  {i}. {action}")

    report.append("\n" + "=" * 60)
    report.append("LEARNING ROADMAP")
    report.append("=" * 60)
    for item in ai_report['skill_roadmap']:
        report.append(f"\n  {item['skill'].upper()}")
        report.append(f"  Why:      {item['why']}")
        report.append(f"  Resource: {item['resource']}")
        report.append(f"  Time:     {item['time']}")

    report.append("\n" + "=" * 60)
    report.append("Generated by AI Resume Analyzer")
    report.append("=" * 60)

    return "\n".join(report)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    roles = get_all_roles()
    role_labels = {
        "data_scientist":            "🔬 Data Scientist",
        "software_engineer":         "💻 Software Engineer",
        "web_developer":             "🌐 Web Developer",
        "devops_engineer":           "🔧 DevOps Engineer",
        "machine_learning_engineer": "🤖 ML Engineer"
    }

    selected_role = st.selectbox(
        "Target Role",
        options=roles,
        format_func=lambda x: role_labels.get(x, x),
        help="Select the job role you are targeting"
    )

    st.markdown("---")
    st.markdown("#### 📋 Job Description (Optional)")
    job_description = st.text_area(
        "Paste JD here for better matching",
        height=150,
        placeholder="Paste the job description here...",
        help="Improves TF-IDF similarity accuracy"
    )

    st.markdown("---")
    st.markdown("#### 💡 Tips for Better Score")
    st.markdown("""
    - Add a **Skills section** with keywords
    - **Quantify achievements** (e.g. 30% faster)
    - Keep resume **300-700 words**
    - Use **exact keywords** from job descriptions
    - Save as **PDF not image**
    """)

    st.markdown("---")
    st.markdown("#### 🛠️ Built With")
    st.markdown("""
    `Python` `spaCy` `scikit-learn`
    `TF-IDF` `PyPDF2` `Streamlit`
    """)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">📄 AI Resume Analyzer</p>',
            unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Get your resume score, missing skills, '
    'and AI-powered feedback in seconds</p>',
    unsafe_allow_html=True)

# ── File Upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📤 Upload your Resume (PDF only)",
    type=['pdf'],
    help="Maximum file size: 10MB"
)

# ── Instructions when no file ─────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("### 1️⃣ Upload\nUpload your resume PDF above")
    with c2:
        st.markdown("### 2️⃣ Select Role\nChoose target role in sidebar")
    with c3:
        st.markdown("### 3️⃣ Analyze\nGet instant score and feedback")
    with c4:
        st.markdown("### 4️⃣ Improve\nFollow action items and roadmap")

    st.markdown("---")
    st.info("👈 Select your target role from the sidebar, then upload your resume PDF")

    # Show sample metrics so user knows what to expect
    st.markdown("### 📊 What you'll get:")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Resume Score", "0-100", "Overall match")
    m2.metric("Skill Analysis", "Found/Missing", "Required skills")
    m3.metric("JD Match", "TF-IDF %", "Job description fit")
    m4.metric("AI Feedback", "Personalized", "Actionable tips")

else:
    # ── Validate file ─────────────────────────────────────────────────────────
    is_valid, validation_msg = validate_pdf(uploaded_file)

    if not is_valid:
        st.error(f"❌ {validation_msg}")
        st.stop()

    # ── Process Resume ────────────────────────────────────────────────────────
    progress_bar = st.progress(0)
    status = st.empty()

    try:
        status.text("📄 Reading PDF...")
        progress_bar.progress(15)

        # Save temp file
        temp_path = "data/temp_resume.pdf"
        os.makedirs("data", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        status.text("🔍 Extracting text...")
        progress_bar.progress(30)
        raw_text = extract_text_from_pdf(temp_path)
        cleaned_text = clean_text(raw_text)

        # Check if text was extracted
        if len(cleaned_text.strip()) < 50:
            st.error("""
            ❌ Could not extract text from this PDF.
            This usually means the PDF is image-based or scanned.
            **Please try:**
            - Export your resume from Word as PDF
            - Use a text-based PDF (not scanned)
            """)
            st.stop()

        status.text("🎯 Matching skills...")
        progress_bar.progress(50)
        score_results = calculate_resume_score(
            resume_text=cleaned_text,
            role=selected_role,
            job_description=job_description if job_description.strip() else None
        )

        status.text("🤖 Generating AI feedback...")
        progress_bar.progress(70)
        ai_report = get_full_ai_analysis(
            resume_text=cleaned_text,
            role=selected_role,
            score_results=score_results
        )

        status.text("📊 Building feedback report...")
        progress_bar.progress(85)
        feedback = generate_full_feedback(score_results)

        status.text("✅ Analysis complete!")
        progress_bar.progress(100)
        time.sleep(0.5)

        # Clear progress indicators
        progress_bar.empty()
        status.empty()

    except Exception as e:
        progress_bar.empty()
        status.empty()
        st.error(f"❌ An error occurred: {str(e)}")
        st.markdown("**Try:**")
        st.markdown("- Re-uploading the PDF")
        st.markdown("- Checking if the PDF has selectable text")
        st.stop()

    # ═══════════════════════════════════════════════════════════════════════════
    # RESULTS SECTION
    # ═══════════════════════════════════════════════════════════════════════════

    st.success(f"✅ Analysis complete for **{role_labels.get(selected_role, selected_role)}** role!")

    # ── Score Banner ──────────────────────────────────────────────────────────
    score = score_results['final_score']
    grade, grade_text = get_score_grade(score)
    score_color = get_score_color(score)
    score_emoji = get_score_emoji(score)

    st.markdown("---")

    # Big score display
    col_score, col_info = st.columns([1, 3])
    with col_score:
        st.markdown(
            f'<div style="text-align:center; padding: 20px; '
            f'background: #1E293B; border-radius: 12px; '
            f'border: 2px solid {score_color};">'
            f'<div style="font-size:0.9rem; color:#94A3B8; '
            f'margin-bottom:5px;">OVERALL SCORE</div>'
            f'<div style="font-size:3.5rem; font-weight:800; '
            f'color:{score_color}; line-height:1;">{score}</div>'
            f'<div style="font-size:1rem; color:#E2E8F0;">/100</div>'
            f'<div style="font-size:1.5rem; margin-top:8px;">Grade: {grade}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col_info:
        st.markdown(f"### {score_emoji} {grade_text}")
        st.markdown(
            f"**Target Role:** {role_labels.get(selected_role, selected_role)}")
        st.markdown(
            f"**Word Count:** {score_results['word_count']} words "
            f"— {score_results['length_feedback']}")
        st.progress(score / 100)

        # Score breakdown metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Skill Match", f"{score_results['skill_score']}/100",
                  score_results['skill_results']['required_match'] + " skills")
        m2.metric("JD Match", f"{score_results['tfidf_score']}/100",
                  "TF-IDF similarity")
        m3.metric("Sections", f"{score_results['section_score']}/100",
                  "Completeness")
        m4.metric("Length", f"{score_results['length_score']}/100",
                  f"{score_results['word_count']} words")

    st.markdown("---")

    # ── Skills Analysis ───────────────────────────────────────────────────────
    st.markdown("## 🎯 Skills Analysis")

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:
        found_req = score_results['skill_results']['found_required']
        found_good = score_results['skill_results']['found_good_to_have']

        st.markdown(
            f'<p class="section-header">✅ Skills Found ({len(found_req)} required)</p>',
            unsafe_allow_html=True)
        if found_req:
            html = "".join([f'<span class="skill-found">✓ {s}</span>'
                            for s in found_req])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.warning("No required skills detected")

        if found_good:
            st.markdown("<br>**Good-to-have skills found:**",
                        unsafe_allow_html=True)
            html = "".join([f'<span class="skill-good">★ {s}</span>'
                            for s in found_good])
            st.markdown(html, unsafe_allow_html=True)

    with skill_col2:
        missing_req = score_results['skill_results']['missing_required']
        missing_good = score_results['skill_results']['missing_good_to_have']

        st.markdown(
            f'<p class="section-header">❌ Missing Skills ({len(missing_req)} required)</p>',
            unsafe_allow_html=True)
        if missing_req:
            html = "".join([f'<span class="skill-missing">✗ {s}</span>'
                            for s in missing_req])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.success("🎉 All required skills found!")

        if missing_good:
            st.markdown("<br>**Good-to-have to learn:**",
                        unsafe_allow_html=True)
            html = "".join([f'<span class="skill-missing">✗ {s}</span>'
                            for s in missing_good[:5]])
            st.markdown(html, unsafe_allow_html=True)

    st.markdown("---")

    # ── Resume Sections + Breakdown ───────────────────────────────────────────
    sec_col, break_col = st.columns(2)

    with sec_col:
        st.markdown("### 📋 Resume Sections")
        for section, sec_score in score_results['section_details'].items():
            name = section.replace('_', ' ').title()
            if sec_score == 100:
                st.markdown(f"✅ **{name}** — found")
            else:
                st.markdown(f"❌ **{name}** — missing!")

    with break_col:
        st.markdown("### 📊 Score Breakdown")
        breakdown = [
            ("Skill Match", score_results['skill_score'], "40% weight"),
            ("JD Similarity", score_results['tfidf_score'], "30% weight"),
            ("Section Complete", score_results['section_score'], "20% weight"),
            ("Length Score", score_results['length_score'], "10% weight"),
        ]
        for label, value, weight in breakdown:
            st.markdown(f"**{label}** ({weight}): {value}/100")
            st.progress(value / 100)

    st.markdown("---")

    # ── AI Feedback ───────────────────────────────────────────────────────────
    st.markdown("## 🤖 AI-Powered Feedback")

    analysis = ai_report['resume_analysis']
    tab1, tab2, tab3, tab4 = st.tabs(
        ["✅ Strengths & Improvements",
         "❌ Weaknesses",
         "🤖 ATS Tips",
         "📝 Assessment"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### ✅ Strengths")
            for s in analysis['strengths']:
                st.markdown(
                    f'<div class="tip-box">✓ {s}</div>',
                    unsafe_allow_html=True)
        with c2:
            st.markdown("#### 🔧 Top Improvements")
            for i, imp in enumerate(analysis['improvements'], 1):
                st.markdown(
                    f'<div class="tip-box">{i}. {imp}</div>',
                    unsafe_allow_html=True)

    with tab2:
        for w in analysis['weaknesses']:
            st.markdown(
                f'<div class="warning-box">⚠️ {w}</div>',
                unsafe_allow_html=True)

    with tab3:
        st.markdown(
            "ATS = Applicant Tracking System. "
            "These systems filter resumes before humans see them.")
        for tip in analysis['ats_tips']:
            st.markdown(
                f'<div class="tip-box">💡 {tip}</div>',
                unsafe_allow_html=True)

    with tab4:
        st.info(f"📝 {analysis['assessment']}")
        justification = ai_report['score_justification']
        st.markdown(f"**Score Level:** {justification['level'].upper()}")
        st.markdown(f"**Reason:** {justification['reason']}")
        st.markdown(f"**Biggest Gap:** {justification['biggest_gap']}")
        st.markdown(f"**Top Action:** {justification['top_action']}")

    st.markdown("---")

    # ── Action Items ──────────────────────────────────────────────────────────
    st.markdown("## ✅ Your Action Items")
    st.markdown("*Do these in order — highest impact first*")

    for i, action in enumerate(feedback['action_items'], 1):
        col_num, col_action = st.columns([1, 10])
        with col_num:
            st.markdown(
                f'<div style="background:#6366F1; color:white; '
                f'border-radius:50%; width:28px; height:28px; '
                f'text-align:center; line-height:28px; '
                f'font-weight:bold;">{i}</div>',
                unsafe_allow_html=True)
        with col_action:
            st.markdown(action)

    st.markdown("---")

    # ── Learning Roadmap ──────────────────────────────────────────────────────
    st.markdown("## 📚 Personalized Learning Roadmap")
    st.markdown("*Free resources for every missing skill*")

    roadmap = ai_report['skill_roadmap']
    if roadmap:
        r_cols = st.columns(min(3, len(roadmap)))
        for i, item in enumerate(roadmap[:6]):
            with r_cols[i % 3]:
                st.markdown(
                    f'<div class="resource-item">'
                    f'<strong style="color:#6366F1">'
                    f'{item["skill"].upper()}</strong><br>'
                    f'<small style="color:#94A3B8">{item["why"]}</small><br><br>'
                    f'<span style="color:#F1F5F9;">📖 {item["resource"]}</span><br>'
                    f'<span style="color:#F1F5F9;">⏱️ {item["time"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True)
    else:
        st.success("🎉 No missing skills — great job!")

    st.markdown("---")

    # ── Best Role Match ───────────────────────────────────────────────────────
    st.markdown("## 🏆 Best Role Match for Your Resume")

    profile = get_resume_skill_profile(cleaned_text)
    sorted_roles = sorted(profile['scores_by_role'].items(),
                          key=lambda x: x[1], reverse=True)

    for role_key, role_score in sorted_roles:
        label = role_labels.get(role_key, role_key)
        color = get_score_color(role_score)
        is_best = role_key == profile['best_matching_role']
        prefix = "🏆 " if is_best else ""
        st.markdown(f"**{prefix}{label}** — {role_score}%")
        st.progress(role_score / 100)

    st.markdown("---")

    # ── Download Report ───────────────────────────────────────────────────────
    st.markdown("## 📥 Download Your Report")

    report_text = generate_text_report(
        score_results, ai_report, feedback, selected_role)

    st.download_button(
        label="📄 Download Full Report (.txt)",
        data=report_text,
        file_name=f"resume_analysis_{selected_role}.txt",
        mime="text/plain",
        help="Download your complete analysis as a text file"
    )

    st.markdown("---")
    st.markdown(
        "<center><small>Built with Python · spaCy · "
        "scikit-learn · TF-IDF · Streamlit</small></center>",
        unsafe_allow_html=True)
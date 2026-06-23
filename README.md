# 📄 AI Resume Analyzer

An intelligent resume analysis tool that scores your resume,
identifies missing skills, and provides AI-powered feedback
for your target job role.

🔗 **Live Demo:** [your-app-url.streamlit.app](https://your-app-url.streamlit.app)

---

## ✨ Features

- **Resume Scoring** — Get a score out of 100 based on skill match,
  JD similarity, section completeness, and length
- **Skill Analysis** — See exactly which skills you have and which
  ones are missing for your target role
- **AI Feedback** — Intelligent strengths, weaknesses, and
  improvement suggestions
- **Learning Roadmap** — Personalized resources for every missing skill
- **ATS Optimization** — Tips to pass automated screening systems
- **Downloadable Report** — Full analysis saved as text file

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| PyPDF2 | PDF text extraction |
| spaCy | NLP processing & NER |
| scikit-learn | TF-IDF vectorization & cosine similarity |
| Pandas | Data handling |
| Streamlit | Web UI framework |
| Google Gemini API | AI-powered feedback |

---

## 📊 How Scoring Works

The resume score is calculated using a weighted formula:Score = (Skill Match × 40%) +

(JD Similarity × 30%) +

(Section Complete × 20%) +

(Length Score × 10%)

- **Skill Match** — Keywords matched against role-specific skill database
- **JD Similarity** — TF-IDF cosine similarity against job description
- **Section Complete** — Checks for Skills, Experience, Education, Contact, Summary
- **Length Score** — Optimal range is 300-700 words

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the app
streamlit run app/main.py
```

---

## 📁 Project Structure

---

## 🧠 Key Concepts Used

- **TF-IDF** (Term Frequency-Inverse Document Frequency) for
  measuring resume-JD similarity
- **Cosine Similarity** for comparing document vectors
- **Named Entity Recognition** (NER) using spaCy
- **Keyword Matching** for skill extraction
- **Weighted Scoring** system for overall resume evaluation
- **Prompt Engineering** for structured AI feedback

---

## 🔮 Future Improvements

- Semantic skill matching using Sentence Transformers
- Multi-language resume support
- LinkedIn profile analysis
- Interview question generator based on resume gaps
- Resume rewriting suggestions

---

## 👨‍💻 Built By

Built as a learning project covering Python, NLP,
Machine Learning, APIs, and deployment.
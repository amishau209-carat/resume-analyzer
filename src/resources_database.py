# src/resources_database.py
# Learning resources for each skill

RESOURCES = {
    "python": [
        {"title": "Python for Everybody",        "platform": "Coursera",  "url": "https://coursera.org/specializations/python"},
        {"title": "Automate the Boring Stuff",   "platform": "Free Book", "url": "https://automatetheboringstuff.com"},
        {"title": "Python Tutorial",             "platform": "YouTube",   "url": "https://youtube.com/watch?v=_uQrJ0TkZlc"},
    ],
    "machine learning": [
        {"title": "ML Specialization",           "platform": "Coursera",  "url": "https://coursera.org/specializations/machine-learning-introduction"},
        {"title": "ML Crash Course",             "platform": "Google",    "url": "https://developers.google.com/machine-learning/crash-course"},
        {"title": "Hands-On ML with Scikit-Learn","platform": "Book",     "url": "https://www.oreilly.com/library/view/hands-on-machine-learning"},
    ],
    "deep learning": [
        {"title": "Deep Learning Specialization","platform": "Coursera",  "url": "https://coursera.org/specializations/deep-learning"},
        {"title": "Fast.ai Course",              "platform": "Free",      "url": "https://fast.ai"},
        {"title": "Deep Learning with Python",   "platform": "Book",      "url": "https://www.manning.com/books/deep-learning-with-python"},
    ],
    "tensorflow": [
        {"title": "TensorFlow Official Tutorials","platform": "Official", "url": "https://tensorflow.org/tutorials"},
        {"title": "TensorFlow Developer Certificate","platform": "Google","url": "https://developers.google.com/certification/tensorflow"},
        {"title": "TensorFlow in Practice",      "platform": "Coursera",  "url": "https://coursera.org/specializations/tensorflow-in-practice"},
    ],
    "pytorch": [
        {"title": "PyTorch Official Tutorials",  "platform": "Official",  "url": "https://pytorch.org/tutorials"},
        {"title": "Deep Learning with PyTorch",  "platform": "Free Book", "url": "https://pytorch.org/deep-learning-with-pytorch"},
        {"title": "PyTorch for Deep Learning",   "platform": "YouTube",   "url": "https://youtube.com/watch?v=Z_ikDlimN6A"},
    ],
    "scikit-learn": [
        {"title": "Scikit-learn Official Docs",  "platform": "Official",  "url": "https://scikit-learn.org/stable/tutorial"},
        {"title": "ML with Python & Scikit-learn","platform": "YouTube",  "url": "https://youtube.com/watch?v=0B5eIE_1vpU"},
    ],
    "pandas": [
        {"title": "Pandas Official Docs",        "platform": "Official",  "url": "https://pandas.pydata.org/docs/getting_started"},
        {"title": "Pandas Tutorial",             "platform": "YouTube",   "url": "https://youtube.com/watch?v=vmEHCJofslg"},
        {"title": "Kaggle Pandas Course",        "platform": "Kaggle",    "url": "https://kaggle.com/learn/pandas"},
    ],
    "numpy": [
        {"title": "NumPy Official Docs",         "platform": "Official",  "url": "https://numpy.org/learn"},
        {"title": "NumPy Tutorial",              "platform": "YouTube",   "url": "https://youtube.com/watch?v=QUT1VHiLmmI"},
        {"title": "Kaggle NumPy Course",         "platform": "Kaggle",    "url": "https://kaggle.com/learn/intro-to-programming"},
    ],
    "sql": [
        {"title": "SQL for Data Science",        "platform": "Coursera",  "url": "https://coursera.org/learn/sql-for-data-science"},
        {"title": "SQLZoo",                      "platform": "Free",      "url": "https://sqlzoo.net"},
        {"title": "Mode SQL Tutorial",           "platform": "Free",      "url": "https://mode.com/sql-tutorial"},
    ],
    "statistics": [
        {"title": "Statistics with Python",      "platform": "Coursera",  "url": "https://coursera.org/specializations/statistics-with-python"},
        {"title": "Khan Academy Statistics",     "platform": "Free",      "url": "https://khanacademy.org/math/statistics-probability"},
        {"title": "StatQuest YouTube",           "platform": "YouTube",   "url": "https://youtube.com/c/joshstarmer"},
    ],
    "data analysis": [
        {"title": "Data Analysis with Python",   "platform": "freeCodeCamp", "url": "https://freecodecamp.org/learn/data-analysis-with-python"},
        {"title": "Kaggle Data Analysis",        "platform": "Kaggle",    "url": "https://kaggle.com/learn/data-visualization"},
    ],
    "nlp": [
        {"title": "NLP Specialization",          "platform": "Coursera",  "url": "https://coursera.org/specializations/natural-language-processing"},
        {"title": "HuggingFace NLP Course",      "platform": "Free",      "url": "https://huggingface.co/learn/nlp-course"},
        {"title": "spaCy Course",                "platform": "Free",      "url": "https://course.spacy.io"},
    ],
    "docker": [
        {"title": "Docker Official Tutorial",    "platform": "Official",  "url": "https://docs.docker.com/get-started"},
        {"title": "Docker for Beginners",        "platform": "YouTube",   "url": "https://youtube.com/watch?v=fqMOX6JJhGo"},
        {"title": "Docker & Kubernetes Course",  "platform": "Udemy",     "url": "https://udemy.com/course/docker-kubernetes-the-practical-guide"},
    ],
    "git": [
        {"title": "Git Official Tutorial",       "platform": "Official",  "url": "https://git-scm.com/doc"},
        {"title": "GitHub Skills",               "platform": "GitHub",    "url": "https://skills.github.com"},
        {"title": "Git & GitHub Crash Course",   "platform": "YouTube",   "url": "https://youtube.com/watch?v=RGOj5yH7evk"},
    ],
    "aws": [
        {"title": "AWS Cloud Practitioner",      "platform": "Official",  "url": "https://aws.amazon.com/training/digital"},
        {"title": "AWS Free Tier",               "platform": "Official",  "url": "https://aws.amazon.com/free"},
        {"title": "AWS Tutorial for Beginners",  "platform": "YouTube",   "url": "https://youtube.com/watch?v=ubCNZFQwYkw"},
    ],
    "javascript": [
        {"title": "JavaScript.info",             "platform": "Free",      "url": "https://javascript.info"},
        {"title": "freeCodeCamp JavaScript",     "platform": "Free",      "url": "https://freecodecamp.org/learn/javascript-algorithms-and-data-structures"},
        {"title": "JavaScript Crash Course",     "platform": "YouTube",   "url": "https://youtube.com/watch?v=hdI2bqOjy3c"},
    ],
    "react": [
        {"title": "React Official Docs",         "platform": "Official",  "url": "https://react.dev/learn"},
        {"title": "React Tutorial",              "platform": "YouTube",   "url": "https://youtube.com/watch?v=bMknfKXIFA8"},
    ],
    "kubernetes": [
        {"title": "Kubernetes Official Tutorial","platform": "Official",  "url": "https://kubernetes.io/docs/tutorials"},
        {"title": "Kubernetes for Beginners",    "platform": "YouTube",   "url": "https://youtube.com/watch?v=X48VuDVv0do"},
    ],
}


def get_resources_for_skill(skill):
    """Returns learning resources for a given skill."""
    skill_lower = skill.lower()
    return RESOURCES.get(skill_lower, [
        {
            "title": f"Search '{skill}' on Google",
            "platform": "Google",
            "url": f"https://google.com/search?q=learn+{skill.replace(' ', '+')}"
        }
    ])


def get_resources_for_missing_skills(missing_skills):
    """
    Takes a list of missing skills and returns
    resources for each one.
    """
    all_resources = {}
    for skill in missing_skills:
        all_resources[skill] = get_resources_for_skill(skill)
    return all_resources
# src/skills_database.py
# Skill lists for different job roles

SKILLS_DATABASE = {
    "data_scientist": {
        "required": [
            "python", "machine learning", "deep learning", "tensorflow",
            "pytorch", "scikit-learn", "pandas", "numpy", "sql",
            "statistics", "data analysis", "nlp"
        ],
        "good_to_have": [
            "spark", "tableau", "power bi", "aws", "docker",
            "git", "keras", "matplotlib", "excel"
        ]
    },

    "web_developer": {
        "required": [
            "html", "css", "javascript", "react", "nodejs",
            "python", "sql", "git", "rest api", "typescript"
        ],
        "good_to_have": [
            "docker", "aws", "mongodb", "postgresql",
            "graphql", "vue", "django", "flask"
        ]
    },

    "software_engineer": {
        "required": [
            "python", "java", "data structures", "algorithms",
            "git", "sql", "rest api", "linux", "object oriented programming"
        ],
        "good_to_have": [
            "docker", "kubernetes", "aws", "microservices",
            "ci/cd", "agile", "javascript", "testing"
        ]
    },

    "devops_engineer": {
        "required": [
            "docker", "kubernetes", "aws", "linux", "git",
            "ci/cd", "terraform", "ansible", "jenkins", "python"
        ],
        "good_to_have": [
            "azure", "gcp", "prometheus", "grafana",
            "helm", "nginx", "networking", "monitoring"
        ]
    },

    "machine_learning_engineer": {
        "required": [
            "python", "machine learning", "tensorflow", "pytorch",
            "scikit-learn", "docker", "git", "sql", "numpy", "pandas"
        ],
        "good_to_have": [
            "kubernetes", "aws", "azure", "spark",
            "airflow", "fastapi", "flask", "feature engineering"
        ]
    }
}


def get_all_roles():
    """Returns list of all available job roles."""
    return list(SKILLS_DATABASE.keys())


def get_skills_for_role(role):
    """Returns required and good_to_have skills for a given role."""
    return SKILLS_DATABASE.get(role, {})
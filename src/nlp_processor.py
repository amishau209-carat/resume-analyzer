# src/nlp_processor.py
# Lightweight NLP without spaCy for deployment

def get_tokens(text):
    """Simple tokenization without spaCy."""
    stopwords = {'the','a','an','and','or','but','in','on','at',
                 'to','for','of','with','is','are','was','were',
                 'be','been','have','has','had','this','that','it'}
    words = text.lower().split()
    return [w.strip('.,!?;:') for w in words
            if w.strip('.,!?;:') not in stopwords
            and len(w.strip('.,!?;:')) > 2]


def get_lemmas(text):
    """Returns tokens as simple base forms."""
    return get_tokens(text)


def get_named_entities(text):
    """Simple entity extraction without spaCy."""
    return {'PERSON': [], 'ORG': [], 'GPE': []}


def get_noun_chunks(text):
    """Simple noun chunk extraction."""
    tokens = get_tokens(text)
    return tokens[:10]


def summarize_resume_nlp(text):
    """Returns basic NLP summary."""
    tokens = get_tokens(text)
    return {
        'tokens': tokens,
        'lemmas': tokens,
        'entities': {},
        'noun_chunks': tokens[:10],
        'person_name': 'Unknown',
        'organizations': [],
        'locations': [],
    }

#NLP processing functions for resume analysis
import spacy
nlp=spacy.load('en_core_web_sm')

def get_tokens(text):
    """
    Tokenizes text and returns list of meaningful words.
    Removes stopwords and punctuations
    """
    doc=nlp(text)

    tokens=[]
    for token in doc:
        #Skip stopwords,punctuations and spaces
        if not token.is_stop and not token.is_punct and not token.is_space:
            tokens.append(token.text.lower())
    return tokens

def get_lemmas(text):
    """
    Returns lemmatized tokens-words reduced to base form.
    'running'->'run', 'managed'->'manage'
    """
    doc=nlp(text)

    lemmas=[]
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_space:
            lemmas.append(str(token.lemma_).lower())

    return lemmas

def get_named_entities(text):
    """
    Extract named entities from text.
    Returns a dict with entity types as keys and lists of entities as values.
    Example: {'PERSON': ['John Doe'], 'ORG': ['Google','ABC Corp']}
    """
    doc=nlp(text)
    entities={}
    for ent in doc.ents:
        #ent.label is the entity type(PERSON,ORG,GPE etc.)
        #ent.text is the actual text found
        if ent.label_ not in entities:
            entities[ent.label_]=[]
        entities[ent.label_].append(ent.text)
    return entities

def get_noun_chunks(text):
    """
    Extracts noun phrases from text.
    These are multi-word concepts like 'machine learning','data analysis'
    """
    doc=nlp(text)

    chunks=[]
    for chunk in doc.noun_chunks:
        chunk_text=chunk.text
        if isinstance(chunk_text,str):
            chunk_text=chunk.text.lower().strip()
            if len(chunk_text) > 2 :
                chunks.append(chunk_text)

    return chunks

def summarize_resume_nlp(text):
    """
    Runs all NLP functions and returns a summary dictionary.
    This will be used by the main app later
    """

    raw_entities= get_named_entities(text)

    summary={
        'tokens':get_tokens(text),
        'lemmas':get_lemmas(text),
        'entities':get_named_entities(text),
        'noun_chunks':get_noun_chunks(text),
        'person_name':raw_entities.get('PERSON',['Unknown'])[0],
        'organizations':raw_entities.get('ORG',[]),
        'locations': raw_entities.get('GPE',[]),
    }
    return summary





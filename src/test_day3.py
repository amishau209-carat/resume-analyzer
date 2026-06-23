import sys
sys.path.insert(0,'.')

from utils import extract_text_from_pdf,clean_text
from nlp_processor import get_tokens, get_lemmas,get_named_entities,get_noun_chunks

#Load and clean resume
print("Loading resume...")
raw_text= extract_text_from_pdf('data/sample_resume.pdf')
cleaned=clean_text(raw_text)

print(f"Resume loaded. {len(cleaned)} characters.\n")

#Test 1- Tokenization
print("="*40)
print("TEST 1: TOKENS(meaningful words only)")
print("="*40)
tokens=get_tokens(cleaned)
print(f"Total meaningful tokens: {len(tokens)}")
print(f"First 20 tokens: {tokens[:20]}")

#Test 2- Lemmatization
print("\n" + "="*40)
print("TEST 2: LEMMAS (base forms of words)")
print("=" * 40)
lemmas=get_lemmas(cleaned)
print(f"Total lemmas: {len(lemmas)}")
print(f"First 20 lemmas: {lemmas[:20]}")

# Test 3 - Named Entities
print("\n" + "=" * 40)
print("TEST 3: NAMED ENTITIES")
print("=" * 40)
entities=get_named_entities(raw_text) #use raw text for better NER
for entity_type, entity_list in entities.items():
    print(f"{entity_type}:{entity_list}")

# Test 4 - Noun Chunks
print("\n" + "=" * 40)
print("TEST 4: NOUN CHUNKS (multi-word concepts)")
print("=" * 40)
chunks=get_noun_chunks(cleaned)
print(f"Total chunks: {len(chunks)}")
print(f"Chunks found: {chunks[:15]}")

# Test 5 - Unique words (vocabulary of this resume)
print("\n" + "=" * 40)
print("TEST 5: UNIQUE WORDS IN RESUME")
print("=" * 40)
unique_words=set(tokens)
print(f"Unique meaningful words:{len(unique_words)}")
print(sorted(unique_words)[:30])

# Test 6 - Full summary
print("\n" + "=" * 40)
print("TEST 6: FULL NLP SUMMARY")
print("=" * 40)
from nlp_processor import summarize_resume_nlp
summary = summarize_resume_nlp(raw_text)
print(f"Candidate name:  {summary['person_name']}")
print(f"Organizations:   {summary['organizations']}")
print(f"Locations:       {summary['locations']}")
print(f"Total tokens:    {len(summary['tokens'])}")
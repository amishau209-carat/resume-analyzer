#Day 1 test-making sure everything works!
import sys
sys.path.insert(0, '.')
from utils import clean_text,read_text_file

#read the sample resume
resume_text=read_text_file('data/sample_resume.txt')
print("=== RAW TEXT ===")
print(resume_text[:200])

print("\n=== CLEANED TEXT ===")
cleaned=clean_text(resume_text)
print(cleaned[:200])

print("\n=== BASIC STATS ===")
words=cleaned.split()
print(f"Total words: {len(words)}")
print(f"Unique words: {len(set(words))}")
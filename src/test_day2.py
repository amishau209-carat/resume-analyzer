import sys
sys.path.insert(0,'.')

from utils import extract_text_from_pdf, clean_text, save_text_to_file

#Step 1: Extract raw text from pdf
print("===EXTRACTING FROM PDF===")
raw_text=extract_text_from_pdf('data/sample_resume.pdf')
print(f"Characters extracted:{len(raw_text)}")
print("\n First 300 characters of raw text:")
print(raw_text[:300])

#Step 2:Cleanthe extracted data
print("\n===CLEANING TEXT===")
cleaned_text=clean_text(raw_text)
print("\nFirst 300 characters of cleaned text:")
print(cleaned_text[:300])

#Compare raw vs cleaned
print("\n===BEFORE vs AFTER CLEANING===")
print(f"Raw length:  {len(raw_text)} characters")
print(f"Cleaned length:  {len(cleaned_text)} characters")
print(f"Words found:  {len(cleaned_text.split())}")

#Save cleaned text to file
save_text_to_file(cleaned_text,'data/cleaned_resume.txt')
print("\nDone! Check data/cleaned_resume.txt")

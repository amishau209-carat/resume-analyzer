import PyPDF2
import re


def clean_text(text):
    """Cleans raw text extracted from a PDF resume."""
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.replace('\n', ' ')
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\@\+\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = text.lower()
    return text


def read_text_file(filepath):
    """Opens a .txt file and returns its content as a string."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def extract_text_from_pdf(pdf_path):
    """Takes a path to a PDF file and returns all text inside it."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    if len(text.strip()) < 50:
        print("WARNING: Very little text extracted. PDF might be scanned.")
    return text


def save_text_to_file(text, output_path):
    """Saves a string to a .txt file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Text saved to {output_path}")


if __name__ == "__main__":
    sample = "    Hello     World!\n\nThis   is   a      test.     "
    print("Before:", repr(sample))
    print("After: ", repr(clean_text(sample)))


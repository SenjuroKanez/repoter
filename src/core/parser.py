# core/parser.py

import re

def parse_questions(text: str):
    """
    Detect and split questions from raw Lab Task text.
    It matches patterns like:
    Question 1:
    Question 2:
    etc...
    Returns a list of dicts with title and empty images list.
    """
    if not text.strip():
        return []

    # Use regex to split text into question chunks
    pattern = re.compile(r"(?i)(?=Question\s+\d+\s*:)" )
    chunks = pattern.split(text)
    questions = []

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        # Extract the first line as the title
        lines = chunk.splitlines()
        title = lines[0].strip() if lines else "Untitled Question"
        questions.append({"title": title, "images": []})

    return questions

if __name__ == "__main__":
    sample = """Lab Tasks:
    Question 1:
    Create a class Shape with a function draw() that prints.

    Question 2:
    Create a base class Publication.

    Question 3:
    Create a class Book.
    """
    print(parse_questions(sample))

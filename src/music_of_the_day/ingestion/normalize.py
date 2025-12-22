import re

def normalize_text(text: str) -> str:
    """
    Cleans up raw article text:
    - Remove HTML tags
    - Remove extra whitespace
    - Remove unusual characters
    """
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text

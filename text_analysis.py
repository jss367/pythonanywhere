import re
import nltk
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup

def analyze_text(text):
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)
    results = sorted(
        raw_word_count.items(),
        reverse=True
        )
    return results
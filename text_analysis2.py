import re
import nltk
from collections import Counter
from bs4 import BeautifulSoup

def analyze_text2(text):
    tokens = clean_text(text)
    num_words = word_count(tokens)
    ave_word = ave_word_size(tokens)
    
    results = sorted(
        num_words.items(),
        reverse=True
        )
    results.append(('Average word size', ave_word))

    results2=[]
    results2.append(('Average word size', ave_word))

    return results

def clean_text(raw_text):
    tokens = nltk.word_tokenize(raw_text)
    return tokens

def word_count(tokens):
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in tokens if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)
    return raw_word_count

def ave_word_size(tokens):
    return float(sum(map(len, tokens))) / len(tokens)
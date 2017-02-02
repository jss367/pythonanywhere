import re
import nltk
import pandas as pd
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


#Let's load that list of all words by freqeuncy of use to see what your rarest words are:
all_words = pd.read_csv('corpora/all_words')
def find_rank(word):
    #print out the Rank of the word:
    return all_words.loc[all_words['Word'] == word]['Rank']
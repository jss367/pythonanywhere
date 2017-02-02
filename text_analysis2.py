import re
import nltk
from collections import Counter
from bs4 import BeautifulSoup

def analyze_text2(text):
    tokens = clean_text(text)
    num_words = word_count(tokens)
    ave_word = ave_word_size(tokens)
    tags = tagger(tokens)
    #Let's look at all the verbs and sort them by most common:
    word_tag_fd = nltk.FreqDist(tags)
    verb_types = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    ranked_verbs = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] in verb_types]
    results = sorted(
        num_words.items(),
        reverse=True
        )
    #results.append(('Average word size', ave_word))

    results2=[]
    results2.append(('Average word size', ave_word))
    verbs=[]
    verbs.append(ranked_verbs)
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

def tagger(text):
    tags = nltk.pos_tag(text)
    return tags
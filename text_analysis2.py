import re
import nltk
from collections import Counter
from bs4 import BeautifulSoup


# pre-load and pre-compile required variables and methods
html_div_br_div_re = re.compile('</div><div><br></div>')
html_newline_re = re.compile('(<br|</div|</p)')
quotation_re = re.compile(u'[\u00AB\u00BB\u201C\u201D\u201E\u201F\u2033\u2036\u301D\u301E]')
apostrophe_re = re.compile(u'[\u02BC\u2019\u2032]')
punct_error_re = re.compile('^(["\]\)\}]+)(?:[ \n]|$)')
ellipsis_re = re.compile('\.\.\.["\(\)\[\]\{\} ] [A-Z]')
newline_re = re.compile('\n["\(\[\{ ]*[A-Z]')
empty_sent_re = re.compile('^[\n ]*$')
nominalization_re = re.compile('(?:ion|ions|ism|isms|ty|ties|ment|ments|ness|nesses|ance|ances|ence|ences)$')

def analyze_text2(text):


    tokens = clean_text(text)
    #Let's find the number of each different word in the count
    num_words = word_count(tokens)
    total_word_count = sum(num_words.values())
    ave_word = ave_word_size(tokens)
    tags = tagger(tokens)
    num_sent = count_sentences(text)
    #Let's look at all the verbs and sort them by most common:
    word_tag_fd = nltk.FreqDist(tags)
    verb_types = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    ranked_verbs = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] in verb_types]
    results = sorted(
        num_words.items(),
        reverse=True
        )
    
    results2=[]
    results2.append(('Average word size', ave_word))
    results2.append(('Number of words', total_word_count))
    results2.append(('Number of sentences', num_sent))
    num_sent = 3#Right now we're assuming it's three sentences cuase it's late
    results2.append(('Ave words per sentence', total_word_count/num_sent))
    verbs=tuple(ranked_verbs)
    #verbs.append(ranked_verbs)
    return (results, results2, verbs)

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


def count_sentences(text):
    # tokenize text into sentences
    text_eg_ie = text.replace('e.g.', 'e.---g.').replace('i.e.', 'i.---e.')
    sents_draft = nltk.sent_tokenize(text_eg_ie)
    for idx, sent in enumerate(sents_draft[:]):
        sents_draft[idx] = sents_draft[idx].replace('e.---g.', 'e.g.').replace('i.---e.', 'i.e.')
        if idx > 0:
            punct_error = punct_error_re.findall(sent)
            if punct_error:
                sents_draft[idx-1] += punct_error[0]
                sents_draft[idx] = sents_draft[idx][len(punct_error[0])+1:]

    # separate sentences at ellipsis characters correctly
    sents_draft_2 = []
    for sent in sents_draft:
        idx = 0
        for ellipsis_case in ellipsis_re.finditer(sent):
            sents_draft_2.append(sent[idx:(ellipsis_case.start() + 3)])
            idx = ellipsis_case.start() + 3
        sents_draft_2.append(sent[idx:])

    # separate sentences at newline characters correctly
    sents = []
    for sent in sents_draft_2:
        idx = 0
        for newline_case in newline_re.finditer(sent):
            sents.append(sent[idx:(newline_case.start() + 1)])
            idx = newline_case.start() + 1
        sents.append(sent[idx:])

    # delete empty sentences
    sents = [sent for sent in sents if not empty_sent_re.match(sent)]

    num_sent = len(sents)
    return num_sent
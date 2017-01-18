from __future__ import division
import os
import re
from bs4 import BeautifulSoup
#import operator
from numpy import std
import nltk
import matplotlib.pyplot as plt
#%matplotlib inline

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
stopset = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.PorterStemmer()
#tagger = nltk.data.load(nltk.tag._POS_TAGGER)
tagger = nltk.download('averaged_perceptron_tagger')
lemmatizer = nltk.WordNetLemmatizer()
dict_cmu = nltk.corpus.cmudict.dict()
dict_wn = nltk.corpus.wordnet
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/vulgar-words')) as f:
    dict_vulgar_words = f.read().splitlines()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/weak-verbs')) as f:
    dict_weak_verbs = f.read().splitlines()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/entity-substitutions')) as f:
    dict_entity_substitutions = f.read().splitlines()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/fillers')) as f:
    dict_fillers = f.read().splitlines()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/irregular-stems')) as f:
    dict_irregular_stems_lines = f.read().splitlines()
    dict_irregular_stems_draft = [line.split(',') for line in dict_irregular_stems_lines]
    dict_irregular_stems = {}
    for stem_old, stem_new in dict_irregular_stems_draft:
        dict_irregular_stems[stem_old] = stem_new

    
def analyze_textz(html):
    word_count = find_word_count('three')
    metrics = dict()
    data = dict()
    metrics['word_count'] = word_count
    original_text = "This is what you originally wrote"
    return original_text, data, metrics
    

def find_word_count(text):
    '''
    This function takes in text that has/hasn't been tokenized
    It returns the word count, which is fed back into metrics['word count']
    '''
    word_count = 3
    return(word_count)
    
def label_parts_of_speech(text):
    #Labeling parts of speech
    tokened = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokened)   #POS_tag is part of speech; JJ is adjective
    return(tagged)

def POS_visual():
    #Look at the frequency of different parts of speech
    tag_fd = nltk.FreqDist(tag for (word, tag) in tagged)
    #print(tag_fd.most_common())
    nouns = tag_fd['NN'] + tag_fd['NNS'] + tag_fd['NNP'] + tag_fd['NNPS'] #singular and plural and proper
    prep_con = tag_fd['IN'] #preposition or conjunction
    determiner = tag_fd['DT']
    commas = tag_fd[','] #Find if they are over or under using commas?
    adverbs = tag_fd['RB'] + tag_fd['RBR'] + tag_fd['RBS']
    verbs = tag_fd['VB'] + tag_fd['VBD'] + tag_fd['VBG'] + tag_fd['VBN'] + tag_fd['VBP'] + tag_fd['VBZ'] 
    adjectives = tag_fd['JJ']
    #Pie chart of different parts of speech, compare to famous works and warn if it is significantly different
    values = [nouns, verbs, adverbs, adjectives]
    labels = ['nouns', 'verbs', 'adverbs', 'adjectives']
    plt.pie(values, labels=labels)
    plt.show()



def stem_better(word):
    stem = stemmer.stem(word.lower())
    if stem in dict_irregular_stems:
        stem = dict_irregular_stems[stem]
    return stem


with open(os.path.join('corpora/word-freq')) as f:
    dict_word_freq_lines = f.read().splitlines()
    dict_word_freq_draft = [line.split(',') for line in dict_word_freq_lines]
    dict_word_freq_draft = [(stem_better(word), float(freq)) for word, pos, freq in dict_word_freq_draft]
    dict_word_freq = {}
    for stem, freq in dict_word_freq_draft:
        if stem in dict_word_freq.keys():
            dict_word_freq[stem] += freq
        else:
            dict_word_freq[stem] = freq


def analyze_text(html):

#     create data and metrics dictionaries
    data = dict()
    '''
    data (and metrics?) will hold all my results and be returned in this function
    
    '''
    metrics = dict()

    ### parse text/html string

    # strip html tags
    html = html_div_br_div_re.sub(r'</div>\n', html)
    html = html_newline_re.sub(lambda m: '\n'+m.group(0), html)
    soup = BeautifulSoup(html)
    original_text = soup.get_text().rstrip('\n')

    # standardize all quotation marks
    text = quotation_re.sub('"', original_text)
    text = apostrophe_re.sub("'", text)

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

    # tokenize sentences into words and punctuation marks
    sents_tokens = [nltk.word_tokenize(sent) for sent in sents]
    tokens = [token for sent in sents_tokens for token in sent]
    data['values'] = tokens
    data['sentence_numbers'] = [(idx+1) for idx, sent in enumerate(sents_tokens) for token in sent]

    # find words
    sents_words = [[token.lower() for token in sent if (token[0].isalnum() or (token in
                    ["'m", "'re", "'ve", "'d", "'ll"]))] for sent in sents_tokens]
    words = []
    word2token_map = []
    for idx, token in enumerate(tokens):
        if token[0].isalnum() or (token in ["'m", "'re", "'ve", "'d", "'ll"]):
            words.append(token.lower())
            word2token_map.append(idx)

    # find word stems
    stems = [stem_better(word) for word in words]
    data['stems'] = [None] * len(tokens)
    for idx, stem in enumerate(stems):
        data['stems'][word2token_map[idx]] = stem

    data['parts_of_speech'] = 'VBD'

    # fix symbol and apostrophed verb tags
    for idx, token in enumerate(tokens):
        if not token[0].isalnum():
            if token in ["'m", "'re", "'ve"]:
                data['parts_of_speech'][idx] = 'VBP'
            elif token == "'s":
                if data['parts_of_speech'][idx] != 'POS':
                    data['parts_of_speech'][idx] = 'VBP'
            elif token == "'d":
                data['parts_of_speech'][idx] = 'VBD'
            elif token == "'ll":
                data['parts_of_speech'][idx] = 'MD'


    # find verb groups
    data['verb_groups'] = [None] * len(tokens)
    verb_group_stack = []
    verb_group_count = 0
    for idx, token in enumerate(tokens):
        if not verb_group_stack:
            if token in ["be", "am", "'m", "is", "'s", "are", "'re", "was", "were", "will", "'ll", "wo", "have", "'ve", "has", "had"]:
                verb_group_stack.append(idx)
        elif token in ['be', 'been', 'being', 'have', 'had']:
            verb_group_stack.append(idx)
        else: #I added this
		#elif data['parts_of_speech'][idx][:2] == 'VB':
        #    verb_group_stack.append(idx)
        #    verb_group_count += 1
        #    for i in verb_group_stack:
        #        data['verb_groups'][i] = verb_group_count
            verb_group_stack = []
        #elif data['parts_of_speech'][idx][:2] not in ['RB', 'PD']:
        #    if len(verb_group_stack) > 1:
        #        verb_group_count += 1
        #        for i in verb_group_stack:
        #            data['verb_groups'][i] = verb_group_count
        #    verb_group_stack = []

    # find expected word frequencies
    data['expected_word_frequencies'] = [None] * len(tokens)
    unmatched_stems = []
    for idx_word, stem in enumerate(stems):
        idx = word2token_map[idx_word]
        if stem in dict_word_freq.keys():
            data['expected_word_frequencies'][idx] = dict_word_freq[stem]
        else:
            data['expected_word_frequencies'][idx] = 0
            unmatched_stems.append(stem)

    # find synonyms
    data['synonyms'] = [None] * len(tokens)
    for idx_word, word in enumerate(words):
        idx = word2token_map[idx_word]
        synonyms = []
        pos_map = {'NN': ['n'], 'JJ': ['a', 's'], 'VB': ['v'], 'RB': ['r']}
        #if data['parts_of_speech'][idx][:2] in pos_map.keys():
        #    if data['values'][idx][0].islower() or (idx == 0) or ((idx > 0) and
        #                                        (data['values'][idx-1] in ['.', '?', '!', '"', '``', '(', '[', '{'])):
        #        pos = pos_map[data['parts_of_speech'][idx][:2]]
        #        for synset in dict_wn.synsets(word):
        #            if synset.pos in pos:
        #               not_curse_word = [False if syn in dict_vulgar_words else True for syn in synset.lemma_names]
        #               if all(not_curse_word):
        #                   synonyms.extend(synset.lemma_names)
        #       synonyms = list(set(synonyms) - set([lemmatizer.lemmatize(word, pos=pos[0])]))
        #       synonyms = [syn for syn in synonyms if ('_' not in syn)]
        #       #syn_stems = [stem_better(syn) for syn in synonyms]
        #       #syn_freqs = [(syn, dict_word_freq[syn_stems[i]]) if (syn_stems[i] in dict_word_freq.keys()) else (syn, 0)
        #       #             for i, syn in enumerate(synonyms)]
        #       #syn_freqs = sorted(syn_freqs, key=lambda x: x[1])
        #       #syn_freqs.reverse()
        #       #synonyms = [syn for syn, freq in syn_freqs]
        data['synonyms'][idx] = []#synonyms


    ### compute metrics on parsed data

    # count number of sentences
    metrics['sentence_count'] = len(sents)

    # count number of words
    metrics['word_count'] = len(words)

    # count number of words per sentence and its standard deviation
    sents_length = [len(sent) for sent in sents_words]
    if len(sents_length):
        metrics['words_per_sentence'] = sum(sents_length) / len(sents_length)
    else:
        metrics['words_per_sentence'] = 0
    if len(sents_length) >= 10:
        metrics['std_of_words_per_sentence'] = std(sents_length)
    else:
        metrics['std_of_words_per_sentence'] = -1

    # find extra long and short sentences
    if len(sents_length):
        metrics['long_sentences_ratio'] = len([1 for sent_length in sents_length if sent_length >= 40]) / len(sents_length)
        metrics['short_sentences_ratio'] = len([1 for sent_length in sents_length if sent_length <= 6]) / len(sents_length)
    else:
        metrics['long_sentences_ratio'] = 0
        metrics['short_sentences_ratio'] = 0

    # find vocabulary size
    metrics['vocabulary_size'] = len(set(stems))

    # count sentence types based on ending punctuation mark
    sents_end_punct = []
    for sent in sents_tokens:
        sents_end_punct.append('')
        for token in reversed(sent):
            if token in ['.', '...', '?', '!']:
                sents_end_punct[-1] = token
            elif token[0].isalnum():
                break
    data['sentence_end_punctuations'] = [sents_end_punct[idx] for idx, sent in enumerate(sents_tokens) for token in sent]
    if metrics['sentence_count']:
        metrics['declarative_ratio'] = (sents_end_punct.count('.') + sents_end_punct.count('...')) \
                                       / metrics['sentence_count']
        metrics['interrogative_ratio'] = sents_end_punct.count('?') / metrics['sentence_count']
        metrics['exclamative_ratio'] = sents_end_punct.count('!') / metrics['sentence_count']
    else:
        metrics['declarative_ratio'] = metrics['interrogative_ratio'] = metrics['exclamative_ratio'] = 0

    # count number of characters in the whole text
    metrics['character_count'] = len(text)

    # count number of stopwords
    metrics['stopword_ratio'] = 0
    data['stopwords'] = [None] * len(tokens)
    for idx, word in enumerate(words):
        if word in stopset:
            metrics['stopword_ratio'] += 1
            data['stopwords'][word2token_map[idx]] = True
        else:
            data['stopwords'][word2token_map[idx]] = False
    if metrics['word_count']:
        metrics['stopword_ratio'] /= metrics['word_count']

    # count number of syllables per word
    cmu_words_count = 0
    cmu_syllables_count = 0
    data['number_of_syllables'] = [None] * len(tokens)
    for idx, word in enumerate(words):
        if word in dict_cmu:
            cmu_words_count += 1
            syll_num = len([phoneme for phoneme in dict_cmu[word][0] if phoneme[-1].isdigit()])
            cmu_syllables_count += syll_num
            data['number_of_syllables'][word2token_map[idx]] = syll_num
    if cmu_words_count:
        metrics['syllables_per_word'] = cmu_syllables_count / cmu_words_count
    else:
        metrics['syllables_per_word'] = 0

    # count number of characters per word
    char_count = [len(word) for word in words]
    if metrics['word_count']:
        metrics['characters_per_word'] = sum(char_count) / metrics['word_count']
    else:
        metrics['characters_per_word'] = 0
    data['number_of_characters'] = [len(token) if token[0].isalnum() else None for token in tokens]

    # estimate test readability using Flesch-Kincaid Grade Level test
    if (metrics['word_count'] >= 100) and metrics['words_per_sentence'] and metrics['syllables_per_word']:
        metrics['readability'] = 0.39 * metrics['words_per_sentence'] + 11.8 * metrics['syllables_per_word'] - 15.59
    else:
        metrics['readability'] = 0

    # count number of different parts of speech
    noun_count = 0
    pronoun_count = 0
    pronoun_nonpossesive_count = 0
    verb_count = 0
    adjective_count = 0
    adverb_count = 0
    for tag in data['parts_of_speech']:
        if tag[:2] == 'NN':
            noun_count += 1
        elif tag[:2] in ['PR', 'WP', 'EX']:
            pronoun_count += 1
            if tag in ['PRP', 'WP', 'EX']:
                pronoun_nonpossesive_count += 1
        elif tag[:2] in ['VB', 'MD']:
            verb_count += 1
        elif tag[:2] == 'JJ':
            adjective_count += 1
        elif tag[:2] == 'RB':
            adverb_count += 1
    if metrics['word_count']:
        metrics['noun_ratio'] = noun_count / metrics['word_count']
        metrics['pronoun_ratio'] = pronoun_count / metrics['word_count']
        metrics['verb_ratio'] = verb_count / metrics['word_count']
        metrics['adjective_ratio'] = adjective_count / metrics['word_count']
        metrics['adverb_ratio'] = adverb_count / metrics['word_count']
        metrics['other_pos_ratio'] = 1 - metrics['noun_ratio'] - metrics['pronoun_ratio'] - metrics['verb_ratio'] \
                                       - metrics['adjective_ratio'] - metrics['adverb_ratio']
    else:
        metrics['noun_ratio'] = 0
        metrics['pronoun_ratio'] = 0
        metrics['verb_ratio'] = 0
        metrics['adjective_ratio'] = 0
        metrics['adverb_ratio'] = 0
        metrics['other_pos_ratio'] = 0

    # count number of modals
    modal_count = data['parts_of_speech'].count('MD')
    if metrics['word_count']:
        metrics['modal_ratio'] = modal_count / metrics['word_count']
    else:
        metrics['modal_ratio'] = 0

    # find auxiliary verbs
    auxiliary_verbs = [False] * len(tokens)
    for i in range(verb_group_count):
        verb_group_stack = [idx for idx in range(len(tokens)) if data['verb_groups'][idx] == i+1]
        for j in verb_group_stack[:-1]:
            auxiliary_verbs[j] = True

    # find nominalizations, weak verbs, entity substitutes, and filler words
    data['nominalizations'] = [None] * len(tokens)
    data['weak_verbs'] = [None] * len(tokens)
    data['entity_substitutions'] = [None] * len(tokens)
    data['filler_words'] = [None] * len(tokens)
    #for idx_word, word in enumerate(words):
    #    idx = word2token_map[idx_word]
    #    data['nominalizations'][idx] = (data['number_of_characters'][idx] > 7) and (data['parts_of_speech'][idx] != 'NNP')\
    #                                    and (nominalization_re.search(word) is not None)
    #    data['weak_verbs'][idx] = (data['parts_of_speech'][idx][:2] == 'VB') and (data['stems'][idx] in dict_weak_verbs)
    #    if data['weak_verbs'][idx] and auxiliary_verbs[idx]:
    #        data['weak_verbs'][idx] = False
    #    data['entity_substitutions'][idx] = (word in dict_entity_substitutions) and (not data['values'][idx].isupper() or (word == 'i'))
    #    if word in ['this', 'that']:
    #        if (idx > 0) and (data['parts_of_speech'][idx-1][:2] in ['NN', 'PR']):
    #            data['entity_substitutions'][idx] = False
     #       if (idx < len(tokens)) and ((data['parts_of_speech'][idx+1][:2] in ['NN', 'PR', 'WP', 'JJ', 'DT', 'WD', 'WP'])
     #                                   or (tokens[idx+1] in ['there', 'that', 'this', 'here'])):
     #           data['entity_substitutions'][idx] = False
     #   data['filler_words'][idx] = (word in dict_fillers)
    if (noun_count + pronoun_nonpossesive_count) > 0:
        metrics['nominalization_ratio'] = data['nominalizations'].count(True) / (noun_count + pronoun_nonpossesive_count)
        metrics['entity_substitution_ratio'] = data['entity_substitutions'].count(True) / (noun_count +
                                                                                           pronoun_nonpossesive_count)
    else:
        metrics['nominalization_ratio'] = 0
        metrics['entity_substitution_ratio'] = 0
    if verb_count > 0:
        metrics['weak_verb_ratio'] = data['weak_verbs'].count(True) / verb_count
    else:
        metrics['weak_verb_ratio'] = 0
    if len(words) > 0:
        metrics['filler_ratio'] = data['filler_words'].count(True) / len(words)
    else:
        metrics['filler_ratio'] = 0

    # find and count negations
    data['negations'] = [None] * len(tokens)
    for idx_word, word in enumerate(words):
        idx = word2token_map[idx_word]
        if word in ["not", "n't", "no", "neither", "nor", "nothing", "nobody", "nowhere", "never"]:
            data['negations'][idx] = True
        elif (word[:2] == 'un') and (word[2:] in dict_cmu) and (data['stems'][idx] not in ['unit', 'under', 'union']):
            data['negations'][idx] = True
        elif (word[:3] == 'mis') and (word[3:] in dict_cmu) and (data['stems'][idx] != 'miss'):
            data['negations'][idx] = True
        else:
            data['negations'][idx] = False
    if metrics['sentence_count']:
        metrics['negation_ratio'] = data['negations'].count(True) / metrics['sentence_count']
    else:
        metrics['negation_ratio'] = 0

    # find and count noun clusters
    data['noun_clusters'] = [None] * len(tokens)
    #noun_cluster_count = 0
    #noun_count_in_cluster = 0
    total_noun_count_in_cluster = 0
    #noun_cluster_span = [None, None]
    #for idx, token in enumerate(tokens):
    #    if data['parts_of_speech'][idx][:2] == 'NN':
    #        if noun_cluster_span[0] is None:
    #            noun_cluster_span = [idx, idx+1]
    #            noun_count_in_cluster = 1
    #        else:
    #            noun_cluster_span[1] = idx+1
    #            noun_count_in_cluster += 1
    #    elif token not in ["'s", "of"]:
    #        if noun_count_in_cluster >= 3:
    #            noun_cluster_count += 1
    #            data['noun_clusters'][noun_cluster_span[0]:noun_cluster_span[1]] = \
    #                [noun_cluster_count] * (noun_cluster_span[1] - noun_cluster_span[0])
    #            total_noun_count_in_cluster += noun_count_in_cluster
    #        noun_cluster_span = [None, None]
    #        noun_count_in_cluster = 0
    if noun_count > 0:
        metrics['noun_cluster_ratio'] = total_noun_count_in_cluster / noun_count
    else:
        metrics['noun_cluster_ratio'] = 0

    # find and count passive voice cases
    data['passive_voice_cases'] = [None] * len(tokens)
    passive_voice_count = 0
    for i in range(verb_group_count):
        verb_group_stack = [idx for idx in range(len(tokens)) if data['verb_groups'][idx] == i+1]
        if data['parts_of_speech'][verb_group_stack[-1]] in ['VBN', 'VBD']:
            for j in verb_group_stack[:-1]:
                if tokens[j] in ["am", "'m", "is", "'s", "are", "'re", "was", "were", "be", "been", "being"]:
                    passive_voice_count += 1
                    data['passive_voice_cases'][j] = passive_voice_count
                    data['passive_voice_cases'][verb_group_stack[-1]] = passive_voice_count
                    break
    if metrics['sentence_count']:
        metrics['passive_voice_ratio'] = passive_voice_count / metrics['sentence_count']
    else:
        metrics['passive_voice_ratio'] = 0

    # count rare words
    if len(words):
        metrics['rare_word_ratio'] = data['expected_word_frequencies'].count(0) / len(words)
    else:
        metrics['rare_word_ratio'] = 0

    # count word, bigram, and trigram frequencies
    bcf = nltk.TrigramCollocationFinder.from_words(stems)
    word_freq = bcf.word_fd
    bigram_freq = bcf.bigram_fd
    trigram_freq = bcf.ngram_fd

    metrics['word_freq'] = []
    metrics['bigram_freq'] = []
    metrics['trigram_freq'] = []


    return original_text, data, metrics
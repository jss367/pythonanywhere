import re
import nltk
import os
import pandas as pd
from collections import Counter

# Load the stemmer
stemmer = nltk.PorterStemmer()

verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        
        
def open_corpora(filename, csv=False):
    try:
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corpora/' + filename)
    except NameError:
        file = 'corpora/' + filename
    if not csv:
        with open(file) as f:
            return f.read().splitlines()
    else:
        return pd.read_csv(file, index_col=0) 
    
    
dict_light_verbs = open_corpora('light_verbs')
all_words_df = open_corpora('all_words2.csv', csv=True)

def analyze_text(text):
    # results is where we'll hold and send our final product
    results = {}
    # First we tokenize the text
    
    # Doing the part for bad sent
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = tokenizer.tokenize(text)
    tagged_texts = nltk.pos_tag_sents(map(nltk.word_tokenize, sents))
    
    weak_sent_num = []
    weak_sent = []
    for i in range(len(tagged_texts)):
        bad_sent, nominalization, light_verb = find_weak_wording(tagged_texts[i])
        if bad_sent:
            # Check if the nominalization occurs at the end or is a common word
            if nominalization != tagged_texts[i][-2][0] and not is_common(nominalization.lower()):
                weak_sent_num.append(i+1)
                weak_sent.append(sents[i] + '                ')
                
    results['weak_sent_num'] = weak_sent_num
    results['weak_sent'] = weak_sent
    
    # Doing the part for bad sent
    flat_tagged = [item for sublist in tagged_texts for item in sublist]
    tokens = [tags for (tags, pos) in flat_tagged]

    # Then find the number of each different word in the count and add it to results
    num_words, total_word_count, unique_words = word_count(tokens)
    results['num_words'] = total_word_count
    results['num_unique_words'] = len(unique_words)
    results['lexical_diversity'] = len(unique_words) / total_word_count
    # Then find the average word size
    results['Ave word size'] = ave_word_size(tokens)
    tags = nltk.pos_tag(tokens)
    # Count the sentences and add sentence count to results
    num_sent = sent_count(text)
    results['num_sentences'] = num_sent
    # Let's look at all the verbs and sort them by most common:
    parts_of_speech = find_pos(tokens)
    
    # results = sorted(
    #     num_words.items(),
    #     reverse=True
    #     )


    # We'll need to get the number of characters per word
    # count number of characters per word
    results['number_of_characters'] = [len(token) if token[0].isalnum() else None for token in tokens]
    # We'll also need all the parts of speech
    results['parts_of_speech'] = nltk.pos_tag(tokens)

    ease, grade = flesch_kincaid(text, sentences=num_sent, tokens=tokens,
                                 words=total_word_count)  # syllables is not sent
    results['Flesch Kincaid'] = grade

    return results

def check_nom(word_pos_tuple):
    """
    Accepts a tuple (word, pos_tag)
    """
    nominalization_re = re.compile('(?:ion|ions|ism|isms|ize|ty|ties|ment|ments|ness|nesses|ance|ances|ence|ences)$')
    nominalization_re_2 = re.compile('(?:tion|ment|ence|ance)$')
    if len(word_pos_tuple[0]) > 7 and nominalization_re.search(word_pos_tuple[0]) and word_pos_tuple[1] != 'NNP': # and check that it's not a proper noun
        return True
    else:
        return False
    
def check_light(word_pos_tuple):
    """
    Accepts a tuple (word, pos_tag)
    """
    if stemmer.stem(word_pos_tuple[0]) in dict_light_verbs and word_pos_tuple[1] in verb_pos:
        return True
    else:
        return False

def find_weak_wording(sentence):
    '''
    This function accepts a list of sentences where each word in the sentences has been tokenized and tagged
    '''

    has_nom = False
    has_light = False
    bad_sent = False
    nominalization = None
    light_verb = None
    # Now let's enumerate over words
    for idx, word_pos_tuple in enumerate(sentence):
        if check_nom(word_pos_tuple):
            has_nom = True
            nominalization = word_pos_tuple[0]
        if check_light(word_pos_tuple):
            has_light = True
            light_verb = word_pos_tuple[0]
    if has_nom and has_light:
        bad_sent = True
    return(bad_sent, nominalization, light_verb)

def word_count(tokens):
    '''This takes a string of tokenized texts as an input and returns a collections.Counter of the words and 
    the total word count'''
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in tokens if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)
    total_word_count = sum(raw_word_count.values())
    unique_words = set(raw_words)
    return raw_word_count, total_word_count, unique_words


def is_common(word, threshold=1500):
    if word in all_words_df['Word'].tolist():
        if all_words_df[all_words_df['Word']==word].index.values[0] < threshold:
            return True
    else:
        return False

def ave_word_size(tokens):
    if len(tokens) > 0:
        return round(float(sum(map(len, tokens))) / len(tokens), 2)
    else:
        return 0

# def bold(word, sentence):
#     if word in sentence:
#         return sentence.split(word)[0] + '\033[1m' + word + '\033[0m' + sentence.split(word)[1]
    
# def bold(word, sentence):
#     if word in sentence:
#         return sentence.split(word)[0] + '<p><b>' + word + '</b></p>' + sentence.split(word)[1]


def sent_count(text):
    '''This has to input raw text so that it can look at the punctuation'''
    # tokenize text into sentences
    get_sent_count = lambda text: len(nltk.sent_tokenize(text))
    sent_count = get_sent_count(text)
    return sent_count


''' Now we're going to try to count the number of syllables. We do so by mixing a lookup method (CMUdict) with a algorithmic method'''


# Method 1:
# This is temporarily commented out becase I can't get cmudict to load
# d = nltk.corpus.cmudict.dict()


def nsyl(word):
    raise KeyError
    # return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]


# Method 2:
# Note: I can probably delete many of these exceptions and make this much simplier in the case of the words.
# Most/all of these exceptions will be covered by the cmu corpus


def sylco(word):
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    # exception_add = ['serious','crucial']
    # exception_del = ['fortunately','unfortunately']

    co_one = ['coif', 'coign', 'coiffe', 'coof']
    co_two = ['coapt', 'coinci']

    pre_one = ['preach']

    syls = 0  # added syllable number
    disc = 0  # discarded syllable number

    # 1) if letters < 3 : return 1
    if len(word) <= 3:
        syls = 1
        return syls

    # 2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like
    # "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed":
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]', word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]', word)) > 1:
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[
                                                                                                       -3:] == "ies":
                pass
            else:
                disc += 1

    # 3) discard trailing "e", except where ending is "le"

    if word[-1:] == "e":
        if word[-2:] == "le":
            pass

        else:
            disc += 1

    # 4) check if consecutive vowels exists, triplets or pairs, count them as
    # one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]', word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]', word))
    disc += doubleAndtripple + tripple

    # 5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]', word))

    # 6) add one if starts with "mc"
    if word[:2] == "mc":
        syls += 1

    # 7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui":
        syls += 1

    # 8) add one if "y" is surrounded by non-vowels and is not in the last
    # word.

    for i, j in enumerate(word):
        if j == "y":
            if (i != 0) and (i != len(word) - 1):
                if word[i - 1] not in "aeoui" and word[i + 1] not in "aeoui":
                    syls += 1

    # 9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui":
        syls += 1

    if word[:2] == "bi" and word[2] in "aeoui":
        syls += 1

    # 10) if ends with "-ian", should be counted as two syllables, except for
    # "-tian" and "-cian"

    if word[-3:] == "ian":
        # and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian":
            pass
        else:
            syls += 1

    # 11) if starts with "co-" and is followed by a vowel, check if exists in
    # the double syllable dictionary, if not, check if in single dictionary
    # and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui':

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two:
            syls += 1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one:
            pass
        else:
            syls += 1

    # 12) if starts with "pre-" and is followed by a vowel, check if exists in
    # the double syllable dictionary, if not, check if in single dictionary
    # and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui':
        if word[:6] in pre_one:
            pass
        else:
            syls += 1

    # 13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't", "wouldn't"]

    if word[-3:] == "n't":
        if word in negative:
            syls += 1
        else:
            pass

    # 14) Handling the exceptional words.

    #     if word in exception_del :
    #         disc+=1

    #     if word in exception_add :
    #         syls+=1

    # calculate the output
    return numVowels - disc + syls


# Combining the methods


def syl_count(text):
    # This uses both methods to determine the number of syllables
    # remove all the punctuation
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    syl = []
    for x in range(len(raw_words)):
        try:
            # Let's just to use lesser syl count to make it easier
            syl.append(min(nsyl(raw_words[x])))
        except KeyError:
            syl.append(sylco(raw_words[x]))
    tot_syl_count = sum(syl)
    return tot_syl_count


def flesch_kincaid(text, sentences=None, tokens=None, words=None, syllables=None):
    '''This inputs that raw text. It is necessary for raw because the sentence count relies on it. The text will be tokenized
    inside. It returns the reading ease and the reading grade.'''
    if sentences is None:
        sentences = sent_count(text)
    if tokens is None:
        tokens = nltk.word_tokenize(text)
    if words is None:
        words = word_count(tokens)[1]
    if syllables is None:
        syllables = syl_count(tokens)
    ease = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
    return round(ease, 2), round(grade, 1)


# This function is from the Part of Speech Finder notebook
def find_pos(tokens):
    '''This function accepts tokens as an input and returns a list of all the parts of speech.
    Note that some words are return twice:
    -Nouns are separated into common and proper as well as grouped together
    -Modals are added to verbs are well as returned separately'''

    tagged = nltk.pos_tag(tokens)

    # Now we devide them into groups
    # Note that IN can be either a preposition or a conjunction, for now we're going to list it with the prepositions
    common_noun_pos = ['NN', 'NNS']
    common_nouns = []
    verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    verbs = []
    adjective_pos = ['JJ', 'JJR', 'JJS']
    adjectives = []
    pronoun_pos = ['PRP', 'PRP$', 'WP', 'WP$']
    pronouns = []
    adverb_pos = ['RB', 'RBR', 'RBS', 'WRB']
    adverbs = []
    proper_noun_pos = ['NNP', 'NNPS']
    proper_nouns = []
    conjunction_pos = ['CC']
    conjunctions = []
    preposition_pos = ['IN', 'TO']
    prepositions = []
    interjection_pos = ['UH']
    interjections = []
    modal_pos = ['MD']  # But these are also verbs, so let's make sure they show up as such
    modals = []
    tagged_other_pos = ['CD', 'DT', 'EX', 'FW', 'LS', 'PDT', 'POS', 'RP', 'SYM', 'WDT']
    tagged_others = []
    other = []

    for idx, token in enumerate(tagged):
        if token[1] in common_noun_pos:
            common_nouns.append(token)
        elif token[1] in verb_pos:
            verbs.append(token)
        elif token[1] in adjective_pos:
            adjectives.append(token)
        elif token[1] in pronoun_pos:
            pronouns.append(token)
        elif token[1] in adverb_pos:
            adverbs.append(token)
        elif token[1] in proper_noun_pos:
            proper_nouns.append(token)
        elif token[1] in conjunction_pos:
            conjunctions.append(token)
        elif token[1] in preposition_pos:
            prepositions.append(token)
        elif token[1] in interjection_pos:
            interjections.append(token)
        elif token[1] in modal_pos:
            modals.append(token)
        elif token[1] in tagged_other_pos:
            tagged_others.append(token)
        else:
            other.append(token)

    verbs.append(modals)
    nouns = common_nouns + proper_nouns
    parts_of_speech = [nouns, common_nouns, verbs, adjectives, pronouns, adverbs, proper_nouns, conjunctions,
                       prepositions, interjections, modals]
    return parts_of_speech

import nltk



def analyze_text(html):
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
def analyze_text(text):
	nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)
    results = sorted(
        raw_word_count.items(),
        reverse=True
        )
    return results
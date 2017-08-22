# Importing libraries
from nltk import ngrams


# Function to extract top 5 high frequency terms other than stopwords
def get_high_freq_terms(score, stopwords):
    unigrams = []
    term_freq = {}
    final_list = []
    for items in score:
        for each_item in ngrams((open("Corpus/" + str(items[0]), 'r').read()).split(), 1):
            unigrams.append(each_item[0])

    for items in unigrams:
        if term_freq.has_key(items):
            term_freq[items] += 1
        else:
            term_freq[items] = 1

    sorted_term_freq = sorted(term_freq.items(), key=lambda (x): x[1], reverse=True)
    for each in sorted_term_freq:
        if each[0] not in stopwords:
            final_list.append(each[0])
    return final_list[:5]

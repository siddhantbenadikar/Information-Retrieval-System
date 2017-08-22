# Importing libraries
import math


# Function to calculate TFIDF score of documents
def tfidf(index, query, n, doc_length, tfidf_score, stopwords):
    for term in query:
        if term not in stopwords and index.has_key(term):
            ni = len(index[term])
            idf = math.log10(float(n) / ni)
            for items in index[term]:
                tf = float(items[1]) / doc_length[items[0]]
                if tfidf_score.has_key(items[0]):
                    tfidf_score[items[0]] += tf * idf
                else:
                    tfidf_score[items[0]] = tf * idf
    return tfidf_score

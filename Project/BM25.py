# Importing libraries
import math

# Defining global variables
corpus_length = 0


# Function to get BM25 score of each document for a query
def bm25(index, qid, query, relevance_judgement, doc_length, total_length, bm25_score, stopwords):
    global corpus_length
    corpus_length = total_length
    already_cal = []
    for term in query:
        if term not in stopwords and term not in already_cal and index.has_key(term):
            already_cal.append(term)
            qfi = getqfi(term, query)  # Calling a function to get qfi of the term
            if len(relevance_judgement) == 0:
                ri = 0
                for i in range(0, len(index[term]), 1):
                    bm25_score[index[term][i][0]] += getbm25(index[term][i][1],
                                                             len(index[term]),
                                                             doc_length[index[term][i][0]],
                                                             qfi,
                                                             0,
                                                             ri)  # Calling a function to calculate BM25 score of a doc
            else:
                ri = get_ri(relevance_judgement[str(qid)], index[term])  # Calling a function to get ri value
                for i in range(0, len(index[term]), 1):
                    bm25_score[index[term][i][0]] += getbm25(index[term][i][1],
                                                             len(index[term]),
                                                             doc_length[index[term][i][0]],
                                                             qfi,
                                                             len(relevance_judgement[str(qid)]),
                                                             ri)  # Calling a function to calculate BM25 score of a doc

    return bm25_score


# Applying formula of BM25 to get BM25 score of a document
def getbm25(fi, ni, dl, qfi, r, ri):
    total_docs = 3204
    avg_doc_len = float(corpus_length) / total_docs
    k1 = 1.2
    b = 0.75
    k2 = 100
    num = float(ri + 0.5) / (r - ri + 0.5)
    den = float(ni - ri + 0.5) / (total_docs - ni - r + ri + 0.5)
    part1 = (math.log(float(num) / den))
    part2 = ((fi * (k1 + 1)) / (fi + (k1 * ((1 - b) + (b * (dl / avg_doc_len))))))
    part3 = ((qfi * (k2 + 1)) / (qfi + k2))
    final = part1 * part2 * part3
    return final


# Function to get number of occurrence of a query term in the query
def getqfi(term, queries):
    count = 0
    for words in queries:
        if term == words:
            count += 1
    return count


# Function to get count of relevant documents which contains the given query term
def get_ri(relevant_docs, docs_with_term):
    ri = 0
    for items in docs_with_term:
        if items[0] in relevant_docs:
            ri += 1
    return ri

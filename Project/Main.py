# Importing libraries
import CorpusGeneration
import IndexCreation
import QueryRead
import BM25
import TFIDF
import HighFreqTerms
import StemmedCorpus
import os

# Defining global variables
index = {}
stemmed_index = {}
query = {}
stemmed_query = {}
stopwords = []
relevance_judgement = {}
document_list = []
tfidf_score = {}
bm25_score = {}
doc_length = {}


# Function to generate index from corpus
def main():
    global index, document_list, stopwords, relevance_judgement, stemmed_index, stemmed_query
    print "Generating Corpus from given HTML files..."
    CorpusGeneration.get_content()  # Calling a function to generate corpus from given HTML files
    print "Generating Inverted index for the corpus..."
    index = IndexCreation.create_index("Corpus/")   # Calling a function to create index for the corpus

    # Creating a document list containing name of all the documents
    for each in index:
        for items in index[each]:
            if items[0] not in document_list:
                document_list.append(items[0])

    print "Reading stopwords file..."
    stopwords = QueryRead.stop_words()  # Reading stopwords file
    print "Reading relevance judgement file..."
    relevance_judgement = QueryRead.relevant_set()  # Reading relevance judgement file

    term_freq = IndexCreation.get_term_freq(index)  # Calling a function to calculate term frequencies in the corpus

    # Adding top 5 words in list of stopwords as they have very low TFIDF values
    count = 0
    for items in term_freq[:50]:
        if items[0] not in stopwords:
            if count < 5:
                stopwords.append(items[0])
                count += 1

    perform_tasks()  # Calling a function to perform tasks


def perform_tasks():

    global bm25_score, tfidf_score, doc_length, query, stopwords, stemmed_index, stemmed_query

    query = QueryRead.read_query_file()  # Reading query file

    task_input = raw_input("Please enter the task number to be performed (1, 2 or 3): ")
    if task_input == "1":
        model_input = raw_input("Please enter retrieval model\n"
                                "a for TFIDF\n"
                                "b for BM25: ")

        # Calculating the total length of corpus and document length of all documents in the corpus
        total_length = 0
        doc_length = {}
        for items in index:
            for each in index[items]:
                total_length += each[1]
                if doc_length.has_key(each[0]):
                    doc_length[each[0]] += each[1]
                else:
                    doc_length[each[0]] = each[1]

        n = len(doc_length)  # Calculating number of documents

        # Calculating TFIDF score of each document for each query
        if model_input == "a":
            for qid in query:
                print "Calculating TFIDF score for query:", qid
                for each_doc in document_list:
                    tfidf_score[each_doc] = 0.0

                # Calling function to calculate TFIDF score
                tfidf_score = TFIDF.tfidf(index, query[qid], n, doc_length, tfidf_score, [])
                sorted_tfidf_score = sorted(tfidf_score.items(), key=lambda (z): z[1], reverse=True)
                write_to_file(qid, sorted_tfidf_score[:100], "Task_1_TFIDF", "tfidf")  # Writing top 100 list in file

            cont_fun()  # Calling exit function

        # Calculating BM25 score of each document for each query
        elif model_input == "b":

            for qid in query:
                print "Calculating BM25 score for query:", qid
                for each_doc in document_list:
                    bm25_score[each_doc] = 0.0

                # Calling function to calculate BM25 score
                bm25_score = BM25.bm25(index, qid, query[qid], relevance_judgement, doc_length, total_length,
                                       bm25_score, [])
                sorted_bm25_score = sorted(bm25_score.items(), key=lambda (z): z[1], reverse=True)
                write_to_file(qid, sorted_bm25_score[:100], "Task_1_BM25", "bm25")  # Writing top 100 list in file

            cont_fun()  # Calling exit function

        else:
            print "Incorrect input..."
            cont_fun()  # Calling exit function

    elif task_input == "2":
        print "Performing Pseudo relevance feedback..."
        model_input = raw_input("Please enter retrieval model\n"
                                "a for TFIDF\n"
                                "b for BM25: ")

        # Calculating the total length of corpus and document length of all documents in the corpus
        total_length = 0
        doc_length = {}
        for items in index:
            for each in index[items]:
                total_length += each[1]
                if doc_length.has_key(each[0]):
                    doc_length[each[0]] += each[1]
                else:
                    doc_length[each[0]] = each[1]

        n = len(doc_length)  # Calculating number of documents

        # Calculating TFIDF score of each document for each query
        if model_input == "a":
            for qid in query:
                print "Calculating TFIDF score for query:", qid
                for each_doc in document_list:
                    tfidf_score[each_doc] = 0.0

                # Calling function to calculate TFIDF score
                tfidf_score = TFIDF.tfidf(index, query[qid], n, doc_length, tfidf_score, [])
                sorted_tfidf_score = sorted(tfidf_score.items(), key=lambda (z): z[1], reverse=True)

                # Getting high freq terms from top 10 documents based on TFIDF score
                high_freq_terms = HighFreqTerms.get_high_freq_terms(sorted_tfidf_score[:10], stopwords)

                # Expanding the query by appending top 5 high freq terms in the query
                for each in high_freq_terms:
                    query[qid].append(each)

                for each_doc in document_list:
                    tfidf_score[each_doc] = 0.0

                # Calling function to calculate TFIDF score again with new query
                tfidf_score = TFIDF.tfidf(index, query[qid], n, doc_length, tfidf_score, [])
                sorted_tfidf_score = sorted(tfidf_score.items(), key=lambda (z): z[1], reverse=True)
                write_to_file(qid, sorted_tfidf_score[:100], "Task_2_TFIDF", "tfidf")  # Writing top 100 list in file

            cont_fun()  # Calling exit function

        # Calculating BM25 score of each document for each query
        elif model_input == "b":

            for qid in query:
                print "Calculating BM25 score for query:", qid
                for each_doc in document_list:
                    bm25_score[each_doc] = 0.0

                # Calling function to calculate BM25 score
                bm25_score = BM25.bm25(index, qid, query[qid], {}, doc_length,
                                       total_length, bm25_score, [])
                sorted_bm25_score = sorted(bm25_score.items(), key=lambda (z): z[1], reverse=True)

                # Getting high freq terms from top 10 documents based on BM25 score
                high_freq_terms = HighFreqTerms.get_high_freq_terms(sorted_bm25_score[:10], stopwords)

                # Expanding the query by appending top 5 high freq terms in the query
                for each in high_freq_terms:
                    query[qid].append(each)

                for each_doc in document_list:
                    bm25_score[each_doc] = 0.0

                # Calling function to calculate BM25 score again with new query
                bm25_score = BM25.bm25(index, qid, query[qid], {}, doc_length, total_length,
                                       bm25_score, [])
                sorted_bm25_score = sorted(bm25_score.items(), key=lambda (z): z[1], reverse=True)
                write_to_file(qid, sorted_bm25_score[:100], "Task_2_BM25", "bm25")  # Writing top 100 list in file

            cont_fun()  # Calling exit function

        else:
            print "Incorrect input..."
            cont_fun()  # Calling exit function

    elif task_input == "3":
        task_input2 = raw_input("Enter 'a' for Task 3 - Part a (Stopping)\n"
                                "and 'b' for Task 3 - Part b (Stemming): ")
        if task_input2 == "a":
            model_input = raw_input("Please enter retrieval model\n"
                                    "a for TFIDF\n"
                                    "b for BM25: ")

            # Calculating the total length of corpus and document length of all documents in the corpus
            total_length = 0
            doc_length = {}
            for items in index:
                if items not in stopwords:
                    for each in index[items]:
                        total_length += each[1]
                        if doc_length.has_key(each[0]):
                            doc_length[each[0]] += each[1]
                        else:
                            doc_length[each[0]] = each[1]

            n = len(doc_length)  # Calculating number of documents

            # Calling function to calculate TFIDF score
            if model_input == "a":
                for qid in query:
                    print "Calculating TFIDF score for query:", qid
                    for each_doc in document_list:
                        tfidf_score[each_doc] = 0.0

                    tfidf_score = TFIDF.tfidf(index, query[qid], n, doc_length, tfidf_score, stopwords)
                    sorted_tfidf_score = sorted(tfidf_score.items(), key=lambda (z): z[1], reverse=True)
                    write_to_file(qid, sorted_tfidf_score[:100], "Task_3a_TFIDF", "tfidf")  # Writing top 100 in file

                cont_fun()  # Calling exit function

            # Calling function to calculate BM25 score
            elif model_input == "b":
                for qid in query:
                    print "Calculating BM25 score for query:", qid
                    for each_doc in document_list:
                        bm25_score[each_doc] = 0.0

                    bm25_score = BM25.bm25(index, qid, query[qid], relevance_judgement, doc_length, total_length,
                                           bm25_score, stopwords)
                    sorted_bm25_score = sorted(bm25_score.items(), key=lambda (z): z[1], reverse=True)
                    write_to_file(qid, sorted_bm25_score[:100], "Task_3a_BM25", "bm25")  # Writing top 100 list in file

                cont_fun()  # Calling exit function

            else:
                print "Incorrect input..."
                cont_fun()  # Calling exit function

        elif task_input2 == "b":

            print "Generating Stemmed corpus..."
            StemmedCorpus.get_content()  # Calling a function to generate corpus from given stemmed docs
            print "Generating inverted index for stemmed corpus..."
            stemmed_index = IndexCreation.create_index("Stemmed_corpus/")  # Calling a function to create index

            # Reading query file
            i = [12, 13, 19, 23, 24, 25, 50]
            j = 0
            for each in open("cacm_stem.query.txt", 'r').readlines():
                stemmed_query[i[j]] = each.split(" ")
                j += 1

            for items in stemmed_query:
                stemmed_query[items] = stemmed_query[items][:len(stemmed_query[items])-1]

            # Calculating the total length of corpus and document length of all documents in the corpus
            total_length = 0
            doc_length = {}
            for items in stemmed_index:
                for each in stemmed_index[items]:
                    total_length += each[1]
                    if doc_length.has_key(each[0]):
                        doc_length[each[0]] += each[1]
                    else:
                        doc_length[each[0]] = each[1]

            model_input = raw_input("Please enter retrieval model\n"
                                    "a for TFIDF\n"
                                    "b for BM25: ")

            n = len(doc_length)  # Calculating number of documents

            # Calling function to calculate TFIDF score
            if model_input == "a":
                for qid in i:
                    print "Calculating TFIDF score for query:", qid
                    for each_doc in document_list:
                        tfidf_score[each_doc] = 0.0

                    tfidf_score = TFIDF.tfidf(stemmed_index, stemmed_query[qid], n, doc_length, tfidf_score, stopwords)
                    sorted_tfidf_score = sorted(tfidf_score.items(), key=lambda (z): z[1], reverse=True)
                    write_to_file(qid, sorted_tfidf_score[:100], "Task_3b_TFIDF", "tfidf")    # Writing top 100 in file

                cont_fun()  # Calling exit function

            # Calling function to calculate BM25 score
            elif model_input == "b":
                for qid in i:
                    print "Calculating BM25 score for query:", qid
                    for each_doc in document_list:
                        bm25_score[each_doc] = 0.0

                    bm25_score = BM25.bm25(stemmed_index, qid, stemmed_query[qid], relevance_judgement, doc_length,
                                           total_length, bm25_score, stopwords)
                    sorted_bm25_score = sorted(bm25_score.items(), key=lambda (z): z[1], reverse=True)
                    write_to_file(qid, sorted_bm25_score[:100], "Task_3b_BM25", "bm25")    # Writing top 100 in file

                cont_fun()  # Calling exit function

            else:
                print "Incorrect input..."
                cont_fun()  # Calling exit function

        else:
            print "Incorrect input entered..."
            cont_fun()  # Calling exit function

    else:
        print "Incorrect input..."
        cont_fun()  # Calling exit function


# Writing the score of documents for each query in file in a specific format
def write_to_file(qid, values, name, sys_name):
    if not os.path.exists("Phase_1_Output"):
        os.makedirs("Phase_1_Output")
    rank = 1
    for items in values:
        doc = str(items[0])[:len(items[0])-4]
        if qid == 1 and rank == 1:
            with open("Phase_1_Output/" + name + ".txt", 'w') as f:
                f.write(str(qid) + " Q0 " + doc + " " + str(rank) + " " + str(items[1]) + " " + sys_name + "\n")
        else:
            with open("Phase_1_Output/" + name + ".txt", 'a') as f:
                f.write(str(qid) + " Q0 " + doc + " " + str(rank) + " " + str(items[1]) + " " + sys_name + "\n")
        rank += 1


# Function to ask whether to continue or stop the program
def cont_fun():
    cont = raw_input("Do you wish to continue (y or n): ")
    if cont == "y" or cont == "Y":
        perform_tasks()


main()  # Calling the main function

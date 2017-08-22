# Importing libraries
from os.path import exists
import traceback
import os

# Defining global variables
relevant_dict = {}
rank_dict = {}
no_of_queries = 0
files = []


# Function to construct the relevant_dict and ranked_dict by reading in the files
def construct_dict(file_name):
    global no_of_queries
    if exists("Phase_1_Output/" + file_name):
        file_relevant = open('cacm.rel', 'r')
        file_ranked_list = open("Phase_1_Output/" + file_name, 'r')

        # goes through each line in the cacm.rel and adds it to  the relevant_dict
        for line in file_relevant.readlines():
            query_id = line.split()[0]
            if query_id not in relevant_dict:
                relevant_dict[query_id] = [line[:-1]]
            else:
                content = relevant_dict[query_id]
                content.append(line[:-1])
        file_relevant.close()

        # goes through each line in the ranked_list and adds it to  the rank_dict
        for line in file_ranked_list.readlines():
            query_id = line.split()[0]
            if query_id not in rank_dict:
                rank_dict[query_id] = [line[:-1]]
            else:
                content = rank_dict.get(query_id)
                content.append(line[:-1])

        no_of_queries = len(rank_dict)
        file_ranked_list.close()
    else:
        print file_name, 'file does not exist...'


# Function to calculate the precision & recall given a filename
def calculate_precision_recall(file_name, f):
    try:
        precision_dict = {}
        recall_dict = {}
        sum_average_precision = 0
        # removes the extension from the file
        file_without_ext = file_name[:file_name.rindex('.')]

        output_file = open("Phase_2_Output/" + file_without_ext + '_precision_recall.txt', 'w')
        output_file_avg = open("Phase_2_Output/" + file_without_ext + "_average_precision.txt", 'w')

        # goes through each item of the rank_dict
        for item in xrange(1, len(rank_dict) + 1):
            query = str(item)
            average_precision = 0
            document_count = 0
            document_found_count = 0
            precision_sum = 0

            # checks if the query is present in the relevant_dict
            # if not present print the required result
            if query not in relevant_dict:
                precision_dict[query] = []
                recall_dict[query] = []
                output_file.write('The query number ' + query + ' has no relevant set, hence P & R is 0\n')
                continue

            # else perform the following
            relevant_doc_list = relevant_dict[query]
            relevant_doc_count = len(relevant_doc_list)
            precision_dict[query] = []
            recall_dict[query] = []

            # assigns all attributes like id, rank etc. to each variable
            for doc in rank_dict[query]:
                document_count += 1
                doc_id = doc.split()[2]
                doc_rank = doc.split()[3]
                doc_score = doc.split()[4]
                doc_found_flag = False  # initilaizes a flag to false
                for relevant_doc in relevant_doc_list:
                    if doc_id == relevant_doc.split()[2]:
                        doc_found_flag = True
                        break

                # if relevant doc_found while retrieval do the following
                if doc_found_flag:
                    document_found_count += 1
                    precision = float(document_found_count) / float(document_count)
                    precision_sum += precision
                    precision_dict[query].append({doc_id: precision})
                    recall = float(document_found_count) / float(relevant_doc_count)
                    recall_dict[query].append({doc_id: recall})
                    output_file.write(
                        str(query) + " Q0 " + doc_id + " " + str(doc_rank) + " " + str(doc_score) + " R " + str(
                            precision) + " " + str(recall) + "\n")

                # if non relevant doc found while retrieval then do the following
                else:
                    precision = float(document_found_count) / float(document_count)
                    precision_dict[query].append({doc_id: precision})
                    recall = float(document_found_count) / float(relevant_doc_count)
                    recall_dict[query].append({doc_id: recall})
                    output_file.write(
                        str(query) + " Q0 " + doc_id + " " + str(doc_rank) + " " + str(doc_score) + " NR " + str(
                            precision) + " " + str(recall) + "\n")

            if document_found_count != 0:
                average_precision += float(precision_sum) / float(document_found_count)
            else:
                average_precision = 0
            output_file_avg.write(str(query) + " " + str(average_precision) + "\n")
            # adds each avg_precision to find total avg_precision
            sum_average_precision += average_precision

        # calculates and writes the mean average precision
        mean_average_precision = float(sum_average_precision) / float(no_of_queries)

        f.write(file_name.replace(".txt", "") + ": " + str(mean_average_precision) + '\n')
        output_file_avg.close()
        output_file.close()

    except Exception as e:
        print(traceback.format_exc())


# Function to calculate the Mean Reciprocal Rank of the system
def calculate_mrr(file_name, f1):
    query_id = 1
    reciprocal_rank = 0
    # traverses through all the queries
    while query_id != no_of_queries + 1:
        # checks if query_id is in the relevant dictionary
        if str(query_id) not in relevant_dict:
            reciprocal_rank += 0
            query_id += 1
            continue

        relevant_doc_list = relevant_dict[str(query_id)]
        ranked_doc_list = rank_dict[str(query_id)]
        for doc in ranked_doc_list:
            flag_break = False
            doc_id = doc.split()[2]
            for relevant_doc in relevant_doc_list:
                if doc_id == relevant_doc.split()[2]:
                    reciprocal_rank += 1.0 / float(doc.split()[3])
                    flag_break = True
                    break
            if flag_break:
                break
        query_id += 1

    mean_reciprocal_rank = reciprocal_rank / float(no_of_queries)

    f1.write(file_name.replace(".txt", "") + ": " + str(mean_reciprocal_rank) + '\n')


# Function to calculate the p@k values for system
def calculate_pak(file_name):
    try:
        pa5_dict = {}
        pa20_dict = {}
        query_id = 1
        file_without_ext = file_name[:file_name.rindex('.')]

        output_file_pa5 = open("Phase_2_Output/" + file_without_ext + "_p@5_score.txt", 'w')
        output_file_pa20 = open("Phase_2_Output/" + file_without_ext + "_p@20_score.txt", 'w')

        # traverses through all the queries
        while query_id != no_of_queries + 1:

            if not relevant_dict.get(str(query_id)):
                pa5_dict[query_id] = 0.0
                pa20_dict[query_id] = 0.0
                query_id += 1
                continue

            relevant_doc_list = relevant_dict[str(query_id)]
            top_5_ranked_doc_list = rank_dict[str(query_id)][:5] # limits the dict to only top 5
            top_20_ranked_doc_list = rank_dict[str(query_id)][:20] # limits the dict to only top 20

            # calculates the precision value @ 5th position
            rel_doc_counter_top5 = 0
            for doc in top_5_ranked_doc_list:
                docid = doc.split()[2]
                for rel_doc in relevant_doc_list:
                    if docid == rel_doc.split()[2]:
                        rel_doc_counter_top5 += 1

            pa5_dict[query_id] = rel_doc_counter_top5 / 5.0
            output_file_pa5.write(str(query_id) + " " + str(pa5_dict[query_id]) + " pk_5_Model\n")

            # calculates the precision value @ 20th position
            rel_doc_counter_top20 = 0
            for doc in top_20_ranked_doc_list:
                docid = doc.split()[2]
                for rel_doc in relevant_doc_list:
                    if docid == rel_doc.split()[2]:
                        rel_doc_counter_top20 += 1

            pa20_dict[query_id] = rel_doc_counter_top20 / 20.0
            output_file_pa20.write(str(query_id) + " " + str(pa20_dict[query_id]) + " pk_20_Model\n")
            query_id += 1
        output_file_pa5.close()
        output_file_pa20.close()

    except Exception as e:
        print(traceback.format_exc())


def main():
    global files, rank_dict, relevant_dict

    # this file contains all the file name we want to perform evaluation on
    # make changes to this file only if you want to perform evaluation on a different ranked list
    files = ["Task_1_TFIDF.txt", "Task_2_TFIDF.txt", "Task_3a_TFIDF.txt", "Task_1_BM25.txt",
             "Task_2_BM25.txt", "Task_3a_BM25.txt", "Task_1_Lucene.txt"]

    if not os.path.exists("Phase_2_Output"):
        os.makedirs("Phase_2_Output")
    f = open("Phase_2_Output/MAP_of_models.txt", 'w')
    f1 = open("Phase_2_Output/MRR_of_models.txt", 'w')

    # runs the evaluation process on each of the files in the list files
    for each in files:
        construct_dict(each)
        calculate_mrr(each, f1)
        calculate_pak(each)
        calculate_precision_recall(each, f)
        rank_dict = {}
        relevant_dict = {}

    f.close()
    f1.close()

main()  # Calling main function

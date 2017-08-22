# Importing libraries
import math
import os
import numpy as np
from scipy import stats

# Defining global variables
task = {}
model_a = {}
model_b = {}
model_b_a = {}
t_val = {}
p_val = {}


# Function to calculate t-value and p-value for set of retrieval models
def t_test():
    global task, model_a, model_b, model_b_a, t_val

    # Writing all the possible combinations of retrieval models to perform t-test
    task["Task_1_TFIDF_vs_Task_2_TFIDF"] = ["Task_1_TFIDF_average_precision.txt",
                                            "Task_2_TFIDF_average_precision.txt"]
    task["Task_1_TFIDF_vs_Task_3a_TFIDF"] = ["Task_1_TFIDF_average_precision.txt",
                                             "Task_3a_TFIDF_average_precision.txt"]
    task["Task_1_TFIDF_vs_Task_1_BM25"] = ["Task_1_TFIDF_average_precision.txt",
                                           "Task_1_BM25_average_precision.txt"]
    task["Task_1_TFIDF_vs_Task_1_Lucene"] = ["Task_1_TFIDF_average_precision.txt",
                                             "Task_1_Lucene_average_precision.txt"]
    task["Task_1_BM25_vs_Task_2_BM25"] = ["Task_1_BM25_average_precision.txt",
                                          "Task_2_BM25_average_precision.txt"]
    task["Task_1_BM25_vs_Task_3a_BM25"] = ["Task_1_BM25_average_precision.txt",
                                           "Task_3a_BM25_average_precision.txt"]
    task["Task_1_BM25_vs_Task_1_Lucene"] = ["Task_1_BM25_average_precision.txt",
                                            "Task_1_Lucene_average_precision.txt"]
    task["Task_1_Lucene_vs_Task_2_TFIDF"] = ["Task_1_Lucene_average_precision.txt",
                                             "Task_2_TFIDF_average_precision.txt"]
    task["Task_1_Lucene_vs_Task_2_BM25"] = ["Task_1_Lucene_average_precision.txt",
                                            "Task_2_BM25_average_precision.txt"]
    task["Task_1_Lucene_vs_Task_3a_TFIDF"] = ["Task_1_Lucene_average_precision.txt",
                                              "Task_3a_TFIDF_average_precision.txt"]
    task["Task_1_Lucene_vs_Task_3a_BM25"] = ["Task_1_Lucene_average_precision.txt",
                                             "Task_3a_BM25_average_precision.txt"]

    # Finding t-value and p-value for each pair
    for items in task:
        for lines in open("Phase_2_Output/" + task[items][0], 'r').readlines():
            temp_list = lines.split(" ")
            temp_list[1] = temp_list[1].strip("\n")
            model_a[temp_list[0]] = float(temp_list[1])

        for lines in open("Phase_2_Output/" + task[items][1], 'r').readlines():
            temp_list = lines.split(" ")
            temp_list[1] = temp_list[1].strip("\n")
            model_b[temp_list[0]] = float(temp_list[1])

        for i in model_a:
            model_b_a[i] = model_b[i] - model_a[i]

        # Calling a function to calculate average of difference in avg precision of 2 models
        avg = calculate_avg()

        # Calling a function to calculate standard deviation of difference in avg precision of 2 models
        std_dev = calculate_std_dev(avg)

        # Finding square root of number of queries, N
        sqrt_n = math.sqrt(len(model_b_a))

        # Calculating t-value
        t_val[items] = (float(avg)/std_dev)*sqrt_n

        # Calculating p-value
        p_val[items] = stats.t.sf(np.abs(t_val[items]), len(model_b_a)-1)

    if not os.path.exists("Bonus_tasks_Output"):
        os.makedirs("Bonus_tasks_Output")

    with open("Bonus_tasks_Output/t-test_results.txt", "w+") as f:
        f.write("Null Hypothesis : There is no difference in effectiveness between retrieval Model A and Model B\n")
        f.write("If null hypothesis is false for a pair of retrieval model,\n")
        f.write("it means Model B is more effective than Model A\n\n")
        f.write("Model A".center(15) + "Model B".center(15) + "t-value".center(20) + "p-value".center(20) +
                "Null hypothesis (True/False)".center(28) + "\n\n")
        f.close()

    # Checking whether Null hypothesis is rejected or not and writing the output in the file
    for items in t_val:
        if p_val[items] <= 0.05:
            hyp = "False"
        else:
            hyp = "True"
        tasks = items.split("_vs_")
        with open("Bonus_tasks_Output/t-test_results.txt", "a") as f:
            f.write(tasks[0].ljust(15) + tasks[1].ljust(15) + str(t_val[items]).ljust(20)
                    + str(p_val[items]).ljust(20) + hyp.center(28) + "\n")


# Function to calculate average of difference in avg precision of 2 models
def calculate_avg():
    sum = 0
    for i in model_b_a:
        sum += model_b_a[i]
    avg = float(sum)/len(model_b_a)
    return avg


# Function to calculate standard deviation of difference in avg precision of 2 models
def calculate_std_dev(avg):
    sum = 0
    for i in model_b_a:
        sum += math.pow((model_b_a[i] - avg), 2)
    std_dev = math.sqrt(float(sum)/len(model_b_a))
    return std_dev


t_test()  # Calling main function

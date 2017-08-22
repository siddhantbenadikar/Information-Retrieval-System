# Importing libraries
import os
from nltk import ngrams

# Defining global variables
unigrams = []
index = {}
term_freq = {}


# Main Function to create and return index
def create_index(directory):
    global unigrams, index
    index = {}
    for files in os.listdir(directory):   # Reading the Files from given corpus
        if ".DS_Store" not in files:
            for each_item in ngrams((open(directory + files, 'r').read()).split(), 1):  # Extracting unigrams from doc
                unigrams.append(each_item[0])

            indexing(files, unigrams)  # Calling function to generate inverted index
            unigrams = []

    return index


# Function to make inverted index
def indexing(file_name, grams):
    temp_grams = grams
    for items in grams:
        if index.has_key(items):
            for each in index[items]:
                match = 1
                if file_name == each[0]:
                    match *= 0
                else:
                    match *= 1
            if match == 1:
                index[items] += [[file_name, find_count(items, temp_grams)]]
                # temp_index[items] += [file_name, find_count(items, temp_grams)]
        else:
            index[items] = [[file_name, find_count(items, temp_grams)]]
            # temp_index[items] = [file_name, find_count(items, temp_grams)]


# Function to find count of occurence of a word in a given document
def find_count(word, grams):
    count = 0
    for item in grams:
        if word == item:
            count += 1
    return count


# Function to get term frequency of a term in corpus
def total_terms(index_terms):
    n = 0
    for l in range(1, len(index_terms), 1):
        n += index_terms[l][1]
    return n


# Function to get term frequency of all the terms in the corpus
def get_term_freq(temp_index):
    for each_item in temp_index:
        term_freq[each_item] = total_terms(temp_index[each_item])  # Calling function to get term frequency table
    sorted_term_freq = sorted(term_freq.items(), key=lambda (z): z[1], reverse=True)  # Sorting it based on frequency
    return sorted_term_freq


# main()  # Calling main function

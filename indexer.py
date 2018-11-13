import os
from nltk.stem.porter import PorterStemmer
import math
import pprint

'''
Created by: Buaron Tal and Semida Andreicha
Date: 20/10/18
'''

# Create a stemmer
stemmer = PorterStemmer()

def stem_all_files(files_path, stop_words):
    # declaring a dictionary for counting the words
    inverted = {}
    # words in files will be written as strings
    files_as_string = ''
    # dictionary to hold lengths of files
    dict_lengths = {}
    for filename in os.listdir(files_path):
        filepath = path + filename
        f = open(filepath, "r")
        for line in f:
            files_as_string += line
        # all words in the list
        data = files_as_string
        # removing punctuations from the data
        data = data.replace('\n', ' ')
        data = data.replace('|', ' ')
        data = data.replace('(', ' ')
        data = data.replace(')', ' ')
        data = data.replace('?', ' ')
        data = data.replace(',', ' ')
        data = data.replace(':', ' ')
        data = data.replace('!', ' ')
        data = data.replace('-', ' ')
        data = data.replace('.', ' ')
        data = data.replace("'", ' ')
        data = data.replace("  ", ' ')
        data = data.replace("/", ' ')
        data = data.replace("@", ' ')
        data = data.replace("%", ' ')
        data = data.replace("...", ' ')
        data = data.replace("=", ' ')
        data = data.replace('"', ' ')
        data = data.split()

        stemwords = []
        # reading the stop_words file to exclude them from stemming
        fi = open(stop_words, 'r')
        # split each word in the stop_words file
        stop_words_ = fi.read().split('\n')
        # iterate over the words we collected
        for word in data:
            # if a word is not a stop word
            if word not in stop_words_:
                # and if it is not a number
                if not word.isdigit():
                    # then append it to the list and stem the word
                    stemwords.append(stemmer.stem(word))
        word_count = len(stemwords)
        print(filename, word_count)
        dict_lengths['%s' % filename] = word_count
        files_as_string = ''
        if True:
            # make the list of stemmed words as set (remove duplicates)
            for i in set(stemwords):
                # checking for the word if it is in the inverted keys list
                if i in inverted.keys():
                    # if exist then increment count and write the file it exist in
                    inverted[i].append((filename, stemwords.count(i)))
                else:
                    # create new entry of the word and the file it exist in
                    inverted[i] = [(filename, stemwords.count(i))]
    return inverted, dict_lengths

def write_to_file(inverted_dict):
    stemmed_words = open('inverted.txt', 'w')
    for j in inverted_dict.keys():
        stemmed_words.write(str(j) + '\t\t')  # writing the word in the file
        stemmed_words.write(str(inverted_dict.get(j)) + '\n')
    return

def calculateTF(inverted_dict, dict_lengths):
    tfDictionary = {}
    # length of the total word count
    for word, cnt in inverted_dict.items():
        for i in range(len(cnt)):
            for filename, length in dict_lengths.items():
                if filename in cnt[i][0]:
                    if word not in tfDictionary.keys():
                        tfDictionary[word] = [(filename, cnt[i][1] / length)]
                    else:
                        tfDictionary[word].append((filename, cnt[i][1] / length))
    return tfDictionary

def calculateIDF(dictionary, counter):
    idf_values = {}
    for word, cnt in dictionary.items():
        term_counter = 0
        for i in range(len(cnt)):
            term_counter += cnt[i][1]
            if word not in idf_values.keys():
                idf_values[word] = [(cnt[i][0], term_counter)]
            else:
                idf_values[word].append((cnt[i][0], term_counter))
    new_dict = {}
    for word, frequency in idf_values.items():
        for i in range(len(frequency)):
            idf = math.log(1 + counter / frequency[i][1])
            if idf < 0:
                print(word, frequency[i], idf)
            if word not in new_dict.keys():
                new_dict[word] = [(frequency[i][0], idf)]
            else:
                new_dict[word].append((frequency[i][0], idf))
    return new_dict

def calculateTF_IDF(tf, idfs):
    tfidf = {}
    for word, value in tf.items():
        for i in range(len(idfs[word])):
            score = value[i][1] * idfs[word][i][1]
            if word not in tfidf.keys():
                tfidf[word] = [(value[0][0], score)]
            else:
                tfidf[word].append((value[i][0], score))
    return tfidf

def calculateQueryTF(query):
    data = query.split()
    stemmed_query = []
    for word in data:
        # if a word is not a stop word
        if word not in stop_words:
            # and if it is not a number
            if not word.isdigit():
                # then append it to the list and stem the word
                stemmed_query.append(stemmer.stem(word))
    word_counter = {}
    # length of the total word count
    for word in stemmed_query:
        wordCount = stemmed_query.count(word)
        query_tf = 1 + math.log(wordCount)
        word_counter[word] = query_tf
    return word_counter

def calculateQueryTF_IDF(tf_query, idfs):
    query_tfidf = {}
    for word, value in tf_query.items():
        if word not in idfs.keys():
            score = 0
        else:
            for i in range(len(idfs[word])):
                score = value * idfs[word][i][1]
        query_tfidf[word] = score
    return query_tfidf

def dotProduct(query_vector, document_vector):
    scores_dict = {}
    score = 0
    some_score = 0
    new_score = 0
    other_score = 0
    for word, value in query_vector.items():
        if word not in document_vector.keys():
            some_score += query_vector[word] * 0
        else:
            for i in range(len(document_vector[word])):
                score += query_vector[word] * document_vector[word][i][1]
                new_score += query_vector[word]**2
                other_score += document_vector[word][i][1]**2
                final = score / (math.sqrt(new_score) * math.sqrt(other_score))
                scores_dict[document_vector[word][i][0]] = final
    return scores_dict

def ranking(score_dictionary):
    sorted_dict = sorted(score_dictionary.items(),  key=lambda x: x[1], reverse=True)
    pprint.pprint(sorted_dict)
    return sorted_dict

def get_user_input():
    query = input('Please Enter a Query: ')
    query_tf = calculateQueryTF(query=query)
    query_tfidf = calculateQueryTF_IDF(query_tf, idfs)
    scores_ = dotProduct(query_tfidf, tf_idf)
    print('ranked documents')
    ranking(scores_)
    get_user_input()
    return

path = input('Please Enter path to files: ')
stop_words = input('Please Enter path to stop_words.txt: ')
inverted_dict, dict_lengths = stem_all_files(files_path=path, stop_words=stop_words)
write_to_file(inverted_dict)
tf = calculateTF(inverted_dict, dict_lengths)
idfs = calculateIDF(inverted_dict, len(dict_lengths))
tf_idf = calculateTF_IDF(tf, idfs)
get_user_input()

'''
files location example: C:/Users/Home/Desktop/Data_Disclosure_Code_IR_Assignment/words/
stop_words location example: C:/Users/Home/Desktop/Data_Disclosure_Code_IR_Assignment/stop_eng.txt
'''
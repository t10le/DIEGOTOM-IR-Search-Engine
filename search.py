import ast
import time
import math
import numpy as np
import collections
import helper_func as diegotom
from typing import *


class InvalidStopPorterOptions(Exception):
    """Raised when the input value is not any of the following:
    0 0
    1 0
    0 1
    1 1"""
    pass


def welcome_msg():
    print('\ntest.py initiated.\n')
    print('==================================')
    print("Welcome to Diegotom Search Engine!")
    print('==================================')
    print('Type either of the following combinations to apply towards your query and our database:')
    print('\n\t\'0 0\'\t--> No stopword; No Porter stemming')
    print('\n\t\'1 0\'\t--> Apply stopword; No Porter stemming')
    print('\n\t\'0 1\'\t--> No stopword; Apply Porter stemming')
    print('\n\t\'1 1\'\t--> Apply stopword; Apply Porter stemming')

    stop_porter_options(input('\n> '))


def read_file(cache: str):
    """Initializes the document and vocabulary dictionaries by splitting up the string literal versions
    of the dictionary formats inside the cache text file.
    """
    global document_dict
    global vocab_dict

    with open(cache, 'r') as f:
        text = f.read()
        delim = text.find('/diegotom/')
        document_dict = text[:delim]
        vocab_dict = text[delim+10:]

    document_dict = ast.literal_eval(document_dict)
    vocab_dict = ast.literal_eval(vocab_dict)


def stop_porter_options(string):
    global stop
    global stem
    try:
        if string == '0 0':
            stop, stem = False, False
            read_file(cache='cache-0-0.txt')
            print('Selected: No stopword; No Porter stemming\nPlease wait...')
        elif string == '1 0':
            stop, stem = True, False
            read_file(cache='cache-1-0.txt')
            print('Selected: Apply stopword; No Porter stemming\nPlease wait...')
        elif string == "0 1":
            stop, stem = False, True
            read_file(cache='cache-0-1.txt')
            print('Selected: No stopword; Apply Porter stemming\nPlease wait...')
        elif string == "1 1":
            stop, stem = True, True
            read_file(cache='cache-1-1.txt')
            print('Selected: Apply stopword; Apply Porter stemming\nPlease wait...')
        else:
            raise InvalidStopPorterOptions

    except InvalidStopPorterOptions:
        print('Invalid entry...please restart test.py')
        quit()


def pre_process(string: str) -> list:
    # Tokenization and case-folding are applied to string by default.
    # Stopword removal and Porter stemming are optional, defined by
    # the user.
    return diegotom.stop_and_port(False, string, stop, stem)


def vector_space_pipeline(string_list: list) -> float:
    """ Returns the weight of the query vector.
    Assumes that W=TF, not W=TF*IDF.

    :return: the weight of query vector, while establishing global query vector
    """
    global set_terms
    global q_vector
    global relevant_doc_ids

    set_terms = sorted(set(string_list))
    q_vector = [0] * len(set_terms)
    relevant_doc_ids = []  # The list of ALL relevant document ids relatve to query
    q_weight = 0

    # print(f'{document_dict}\n')
    for i in range(len(set_terms)):
        if set_terms[i] in vocab_dict:
            q_tf = 1+math.log(string_list.count(set_terms[i]))
            q_weight += (q_tf)**2
            # Note: This is technically the q_weight, since we do W = TF, not W = TF * IDF
            q_vector[i] = q_tf

            # Store the document ID
            relevant_doc_ids += vocab_dict[set_terms[i]]
    q_weight = math.sqrt(q_weight)

    print(f'\n>>> relevant_doc_ids <<<\n\t {set(relevant_doc_ids)}')
    result_docs = {}
    d_weight = 0
    N = len(document_dict)
    for docID in set(relevant_doc_ids):
        d_vector = [0] * len(set_terms)
        for i in range(len(set_terms)):
            if set_terms[i] in document_dict[docID]:
                d_tf = 1+math.log(document_dict[docID].count(set_terms[i]))
                d_weight = d_tf*math.log(N/len(vocab_dict[set_terms[i]]))
                d_vector[i] = d_weight
        result_docs[docID] = d_vector
    print(f'\n>>> resulting document collection <<<\n\t {result_docs}')

    cosine_sim = {}

    for document in result_docs.items():
        cosine_sim[document[0]] = np.dot(document[1], q_vector) / (
            (math.sqrt(sum(i * i for i in document[1]))) * (math.sqrt(q_weight)))

    final_results = sorted(
        cosine_sim.items(), key=lambda x: x[1], reverse=True)
    print(
        f'\n>>> cosine sim list <<<\n\t {final_results}')

    print(f'\n\nset_terms: {set_terms}')
    print(f'query vector: {q_vector}')
    print(f'query weight: {q_weight}')

    return final_results


# Greet and process user filter request
welcome_msg()
print('\nREADY!')

# Process user query and use search.py
print('\nEnter your query below; to exit, type \'ZZEND\' and hit enter.')

avg_time = 0
count = 0
while True:
    user = input('> ')
    if user == 'ZZEND':
        break
    start = time.time()
    # --- Enter task below ---
    ranked_list = vector_space_pipeline(pre_process(user))
    print(f'ORIGINAL QUERY: "{user}"')
    # ------------------------
    end = time.time()

    elapsed = end-start
    avg_time += elapsed
    count += 1
    print(f"\nElasped Time to Retrieve: {elapsed}")
print("\ntest.py has been terminated by 'ZZEND'")
if count == 0:
    print(f"Averaged time of retrieval: 0.0")
else:
    print(f"Averaged time of retrieval: {avg_time/count}")
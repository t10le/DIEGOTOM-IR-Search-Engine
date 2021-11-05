import ast
import math
import numpy as np
import helper_func as diegotom
from typing import *


class InvalidStopPorterOptions(Exception):
    """Raised when the input value is not any of the following:
    0 0
    1 0
    0 1
    1 1"""
    pass


def do_tests(collection_of_queries: dict, cachefile: str) -> list:
    global stop
    global stem
    if cachefile == 'cache-1-1.txt':
        stop = True
        stem = True
    elif cachefile == 'cache-0-0.txt':
        stop = False
        stem = False
    elif cachefile == 'cache-0-1.txt':
        stop = False
        stem = True
    elif cachefile == 'cache-1-0.txt':
        stop = True
        stem = False
    else:
        print("error")

    read_file(cachefile)

    result = []
    for doc in collection_of_queries.items():
        query = diegotom.stop_and_port(False, ' '.join(doc[1]), stop, stem)
        collection_of_relevant_docs = vector_space_pipeline(query)
        list_of_ids = [e[0] for e in collection_of_relevant_docs]
        result.append(list_of_ids)

    return result


def welcome_msg():
    print('\ntest.py initiated.\n')
    print('==================================')
    print("Welcome to Diegotom Search Engine!")
    print('==================================')
    print('Type either of the following combinations to apply towards your query and the CACM database:')
    print('\n\t\'0 0\'\t--> No stopword; No Porter stemming')
    print('\n\t\'1 0\'\t--> Apply stopword; No Porter stemming')
    print('\n\t\'0 1\'\t--> No stopword; Apply Porter stemming')
    print('\n\t\'1 1\'\t--> Apply stopword; Apply Porter stemming')

    stop_porter_options(input('\n> '))


def read_metadata() -> dict:
    """Returns the both the author and title dictionary as a tuple.
    Use tuple[0] for author and tuple[1] for title dictionary.
    """
    with open("metadata.txt", "r") as f:
        text = f.read()
        delim = text.find('/diegotom/')
        author_dict = ast.literal_eval(text[:delim])
        title_dict = ast.literal_eval(text[delim+10:])

    return (author_dict, title_dict)


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


def stop_porter_options(string: str):
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


def vector_space_pipeline(string_list: list) -> list:
    """ Returns the list of relevant documents based on cosine similarity scoring.
    Assumes that W=TF*IDF.

    :return: the relevance list of documents while establishing global variables
    """
    global set_terms
    global q_vector
    global relevant_doc_ids

    set_terms = sorted([term for term in set(
        string_list) if term in vocab_dict])
    q_vector = [0] * len(set_terms)
    relevant_doc_ids = []  # The list of ALL relevant document ids relatve to query
    q_weight = 0
    N = len(document_dict)

    # print(f'{document_dict}\n')

    for i in range(len(set_terms)):
        q_tf = 1+math.log(string_list.count(set_terms[i]))
        a = q_tf*math.log(N/(len(vocab_dict[set_terms[i]])))
        q_weight += (a)**2
        q_vector[i] = a

        # Store the document ID
        relevant_doc_ids += vocab_dict[set_terms[i]]
    # print(f'q_weight: {math.sqrt(q_weight)}')
    # print(
    #     f'\n>>> relevant_doc_ids (NOT ORDERED YET BY COSINE SIM)<<<\n\t {set(relevant_doc_ids)}')
    result_docs = {}

    for docID in set(relevant_doc_ids):
        d_weight = 0
        d_vector = [0] * len(set_terms)
        for i in range(len(set_terms)):
            if set_terms[i] in document_dict[docID]:
                d_tf = 1+math.log(document_dict[docID].count(set_terms[i]))
                d_weight = d_tf*math.log(N/len(vocab_dict[set_terms[i]]))
                d_vector[i] = d_weight
        result_docs[docID] = d_vector
    # print(f'\n>>> resulting document collection <<<\n\t {result_docs}')

    cosine_sim = {}

    for document in result_docs.items():
        cosine_sim[document[0]] = np.dot(document[1], q_vector) / (
            (math.sqrt(sum(i * i for i in document[1]))) * math.sqrt(q_weight))

    K = 10
    final_results = sorted(
        cosine_sim.items(), key=lambda x: x[1], reverse=True)[:K]
    # print(
    #     f'\n>>> cosine sim list <<<\n\t {final_results}')

    # print(f'\n\nset_terms: {set_terms}')
    # print(f'query vector: {q_vector}')
    # print(f'query weight: {q_weight}')

    return final_results

    # --- OLD QUERY VECTOR ---
    q_weight_normalized = 0
    only_terms = [key[0] for key in vocab_dict.items()]
    qq_vector = [0] * len(only_terms)
    set_terms_indices = [only_terms.index(
        term) for term in set_terms]
    for i in range(len(set_terms)):
        q_tf = 1+math.log(string_list.count(set_terms[i]))
        q_idf = math.log(N/(len(vocab_dict[set_terms[i]])))
        q_weight = q_tf*q_idf
        qq_vector[set_terms_indices[i]] = q_weight
        q_weight_normalized += q_weight

        # Store the list of document IDs to the list of relevant doc IDs.
        relevant_doc_ids += vocab_dict[set_terms[i]]
    q_weight_normalized = math.sqrt(q_weight_normalized)
    # print(qq_vector)
    # print(q_weight_normalized)
    # print(f'\n\nRELEVANT DOC IDS:\n{relevant_doc_ids}')
    # -------------------------

    # --- OLD DOC VECTORS ---
    result_docs = {}
    for docID in set(relevant_doc_ids):
        d_weight = 0
        dd_vector = [0] * len(vocab_dict)
        for i in range(len(set_terms)):
            # print(f'i: {i}\tset_terms[i]: {set_terms[i]}')
            if set_terms[i] in document_dict[docID]:
                d_tf = 1+math.log(document_dict[docID].count(set_terms[i]))
                d_idf = math.log(N/(len(vocab_dict[set_terms[i]])))
                d_weight = d_tf*d_idf
                dd_vector[int(docID)] = d_weight
        result_docs[docID] = dd_vector
    # -----------------------

    # for key in result_docs.items():
    #     print(f'key: {key[0]} val: {key[1]}\n')

    # --- NEW COSINE SIM ---
    cosine_sim = {}
    for document in result_docs.items():
        cosine_sim[document[0]] = np.dot(document[1], qq_vector) / (
            (math.sqrt(sum(i * i for i in document[1]))) * q_weight_normalized)

    K = 10
    final_results = sorted(
        cosine_sim.items(), key=lambda x: x[1], reverse=True)[:K]

    return final_results

    # ----------------------

from typing_extensions import final
from typing import *
from nltk.tokenize import word_tokenize
import search as dt

with open('qrels.text', 'r') as file:
    # qrels.text file is transformed into a collection of lists
    # key = query number
    # value = [docID, docID, ...]
    # dict = { value: (docID), value: (docID, ...)}
    query_results = file.read()
    query_results = query_results.split(" 0 0\n")

with open('query.text', 'r') as f:
    text = f.read()
    text = text.split('.I')


def get_ID(string):
    """Returns the document ID.
    :param string: A long pre-formatted string.
        Example input:
        "20\n.T\nAccelerating Convergence of Iterative
        Processes\n.W\nA technique is discussed which,
        when applied\nto an iterative procedure for the
        solution of\nan equation.\n.B\nCACM June, 1958"
    :rtype: str
        Example output:
        "20"
    """
    return string[1:string.find("\n")]


def get_abstract(string):
    """Returns the document abstract (if applicable).
    :param string: A long pre-formatted string.
        Example input:
        "20\n.T\nAccelerating Convergence of Iterative
        Processes\n.W\nA technique is discussed which,
        when applied\nto an iterative procedure for the
        solution of\nan equation.\n.B\nCACM June, 1958"
    :rtype: str, None
        Example output:
        "A technique is discussed which, when applied
        to an iterative procedure for the solution of
        an equation."
    """
    START = string.find(".W")
    if START != -1:
        END = string.find("\n.", START)
        return string[START+4:END]
    return None


def get_query(document):
    '''
    :param text document
    :rtype dictionary
    '''
    query_dict = {}
    for i in range(1, len(document)):

        query = get_abstract(document[i]).replace("\n", " ").lower()
        id = get_ID(document[i])

        if id not in query_dict:
            query_dict[id] = query

    for key, value in query_dict.items():
        value = [word for word in word_tokenize(value)]  # if word.isalpha()
        query_dict[key] = value

    return query_dict


def qrels(document: list) -> dict:
    q_results = {}
    for i in range(len(document)):
        document[i] = word_tokenize(document[i])
        document[i] = [id.lstrip('0') for id in document[i]]

        query_number = document[i][0]
        docID = document[i][1]

        if query_number not in q_results:
            q_results[query_number] = [docID]
        else:
            q_results[query_number].append(docID)

    # (Key: rel_doc_ID Val: rel_doc_list)
    return q_results


# Dictionary
relevant_doc_collection = qrels(query_results)


# print(relevant_doc_collection)

# SET K=len(query_results) to keep it the same.
# result_11 = dt.do_tests(get_query(text), 'cache-1-1.txt')   # <list>
caches = ['cache-1-1.txt',
          'cache-0-1.txt',
          'cache-1-0.txt',
          'cache-0-0.txt']
results = [dt.do_tests(get_query(text), x) for x in caches]

i = 0
for li in results:
    print(f'{caches[i]} results:\n')
    for key in relevant_doc_collection.items():
        ID = int(key[0]) - 1
        R_LIST = set([int(x) for x in key[1]])
        R_LENGTH = len(key[1])
        A = set([int(x) for x in li[ID][:R_LENGTH]])
        # print(A)
        # print(R_LIST)

        R_PRECISION = len(A.intersection(R_LIST)) / R_LENGTH
        print(
            f'DOC_ID:\t{key[0]}\nR-precision score:\t{R_PRECISION}\n')
    i += 1
    print('\n\n\n')

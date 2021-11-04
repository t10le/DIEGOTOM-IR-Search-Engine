from typing_extensions import final
from nltk.tokenize import word_tokenize
import search as dt
import helper_func as diegotom

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


def qrels(document):

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
    return q_results


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


def mean_average_precision(query_result, set_relevant_docs):
    '''
    :param query_result -> 2D list
    :param set_relevant_docs -> 2D list

    :return type Mean Average Precision -> float
    '''
    position_found = 0
    precision_found = 0
    precision_query = 0
    length_query_result = 0
    FINAL_MAP = 0

    for i in range(len(query_result)):
        for j in range(len(query_result[i])):
            if query_result[i][j] in set_relevant_docs[i]:
                position_found = set_relevant_docs[i].index(
                    query_result[i][j])+1
                precision_found += 1
                precision_query = (position_found/precision_found)
                length_query_result = len(query_result[i])
                FINAL_MAP += (precision_query/length_query_result)
        precision_found = 0

    return round(FINAL_MAP/len(query_result), 4)


# all relevant documents from qrels in a DICTIONARY
final_qrels = qrels(query_results)

# QUERY RESULTS
relevant_qrels_docs = [v for v in final_qrels.values()]
final_retrieved_docs_0_0 = dt.do_tests(
    get_query(text), 'cache-0-0.txt')   # SET OF RELEVANT DOCS
final_retrieved_docs_0_1 = dt.do_tests(
    get_query(text), 'cache-0-1.txt')   # SET OF RELEVANT DOCS
final_retrieved_docs_1_0 = dt.do_tests(
    get_query(text), 'cache-1-0.txt')   # SET OF RELEVANT DOCS
final_retrieved_docs_1_1 = dt.do_tests(
    get_query(text), 'cache-1-1.txt')   # SET OF RELEVANT DOCS

print(
    f"MAP (No Stopword, No Stemming): {mean_average_precision(relevant_qrels_docs, final_retrieved_docs_1_1)}")
print(
    f"\nMAP (No Stopword, Yes Stemming): {mean_average_precision(relevant_qrels_docs, final_retrieved_docs_0_1)}")
print(
    f"\nMAP (Yes Stopword, No Stemming): {mean_average_precision(relevant_qrels_docs, final_retrieved_docs_1_0)}")
print(
    f"\nMAP (Yes Stopword, Yes Stemming): {mean_average_precision(relevant_qrels_docs, final_retrieved_docs_1_1)}")

import re
import nltk
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


def show_list(arr):
    for doc in range(len(arr)):
        print(f"index: {doc}\n\"{arr[doc]}\"\n")


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
    return string[:string.find("\n")]


def get_title(string):
    """Returns the document title.

    :param string: A long pre-formatted string.
        Example input:
        "20\n.T\nAccelerating Convergence of Iterative
        Processes\n.W\nA technique is discussed which,
        when applied\nto an iterative procedure for the
        solution of\nan equation.\n.B\nCACM June, 1958"
    :rtype: str
        Example output:
        "Accelerating Converge of Iterative Processes
    """
    START = string.find(".T")+2
    END = string.find("\n.", START+1)
    return string[START:END]


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
        END = string.find("\n.", START+1)
        return string[START+2:END+1]
    return None


def build_vocabulary(string, stop_state, porter_state):
    porter = PorterStemmer()
    # Set improves performance somehow, according to stackoverflow.
    # 'english' -> ~150 stopwords
    # 'en'      -> ~900 stopwords
    STOP_WORDS = set(stopwords.words('english'))

    temp = string
    if stop_state:
        temp = [w for w in temp if not w in STOP_WORDS]
    if porter_state:
        for i in range(len(temp)):
            temp[i] = PorterStemmer().stem(temp[i])
    print(sorted(set(temp)))
    # return result


def getKeysByValue(dictionary, target_word):
    linked_list = list()
    for key in dictionary.items():
        print(key)
        print("\n")
        if len(key[1]) == 2:
            if target_word in key[1][0] or target_word in key[1][1]:
                linked_list.append(key[0])
        else:
            if target_word in key[1]:
                linked_list.append(key[0])

    print(linked_list)


def pre_processing(document):
    vocabulary = []
    doc_corpus = {}
    for i in range(1, len(document)):
        # Document essentials
        id = get_ID(document[i])
        title = get_title(document[i]).lower().split()
        abstract = get_abstract(document[i])

        # Build the super long string, vocabulary
        vocabulary += title
        if abstract != None:
            a = abstract.lower().split()
            vocabulary += a
            doc_corpus[id] = (title, a)
        else:
            doc_corpus[id] = (title)

    getKeysByValue(doc_corpus, "of")
    # build_vocabulary(vocabulary, True, True)

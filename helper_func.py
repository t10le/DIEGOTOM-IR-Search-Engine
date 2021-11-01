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
    """Returns the vocabulary set of terms.
    :param string:
    :param stop_state:
    :param porter_state:
    :rtype:
    """
    # Set improves performance somehow, according to stackoverflow.
    # 'english' -> ~150 stopwords
    # 'en'      -> ~900 stopwords
    STOP_WORDS = set(stopwords.words('english'))

    # Tokenize the string
    string_list = word_tokenize(string)

    # Apply stopword removal (if applicable)
    if stop_state:
        string_list = [w for w in string_list if not w in STOP_WORDS]
    # Apply Porter stemming (if applicable)
    if porter_state:
        for i in range(len(string_list)):
            string_list[i] = PorterStemmer().stem(string_list[i])
    print(sorted(set(string_list)))
    # return result


def getKeysByValue(dictionary, term):
    """Returns the posting list representing the document IDs 
    relative to the term.

    :param dictionary: A dictionary (HashMap) containing the document
                       corupus. Each tuple has the format: (Key, Value),
                       where type(Key)=str and type(Value) = list.
    :param term: 
        Example input:
        {('1', (['This','is','a','title'],['This','is','abstract'])),
        ('4', (['This','one','only','has','title'])),
        .
        .
        ('x', ([key], [listOfTermsInTitleAndAbstract]))}
    :rtype: list
        Example output:
        ['2','4','6','3201','3204']
    """
    linked_list = list()
    for key in dictionary.items():
        # Document has a title and abstract
        if len(key[1]) == 2:
            if term in key[1][0] or term in key[1][1]:
                linked_list.append(key[0])
        # Document only has a title
        else:
            if term in key[1]:
                linked_list.append(key[0])

    print(linked_list)


def pre_processing(document):
    vocabulary = ''
    doc_corpus = {}
    for i in range(1, len(document)):
        # Document essentials
        id = get_ID(document[i])
        title = get_title(document[i]).lower()
        abstract = get_abstract(document[i])

        # Build the vocabulary and document corpus
        vocabulary += title
        if abstract != None:
            a = abstract.lower()
            vocabulary += a
            doc_corpus[id] = (title.split(), a.split())
        else:
            doc_corpus[id] = (title.split())
    # print(vocabulary)
    build_vocabulary(vocabulary, True, True)
    # getKeysByValue(doc_corpus, "of")

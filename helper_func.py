from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from typing import *


def show_list(arr):
    for doc in range(len(arr)):
        print(f"index: {doc}\n\"{arr[doc]}\"\n")


def set_flags(stop: bool, stem: bool):
    """Sets the stopflag and stemflag.
    """
    global stopflag
    global stemflag
    stopflag = stop
    stemflag = stem


def get_ID(string: str) -> str:
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


def get_title(string: str) -> str:
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


def get_abstract(string: str) -> str:
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


def get_author(string: str) -> str:
    """Returns the document author(s).
    """
    START = string.find(".A")
    if START != -1:
        END = string.find("\n.", START+1)
        return string[START+2:END+1]
    return None


def build_postings(dictionary: dict, term: str) -> list:
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
        ('key', ([listOfTermsAsTitle], [maybeAbstractToo]))}
    :rtype: list
        Example output:
        ['1','4','6','3201','3204']
    """
    linked_list = list()
    for key in dictionary.items():
        if term in key[1]:
            linked_list.append(key[0])
    return linked_list


def stop_and_port(flag: bool, string: str, stop_state: bool, porter_state: bool) -> list:
    """Returns the tokenized vocabulary set of terms (if applicable, with
    stopword removal and Porter stemming applied).
    :param string: A long pre-formatted string containing all document 
                   titles and abstracts, with \n and \t preserved.
        Example input:
        "updating mean and variance estimates: an improved method
        a method of improved efficiency
        is given for updating the mean and variance of weighted sampled data
        when an additional data value is included in the set.  evidence
        is presented that the method is stable and at least
        as accurate as the best existing updating method. 

        eigenvalues and eigen vectors of a
        real general matrix (algorithm 343 $f))"
    :param stop_state:
    :param porter_state:
    :rtype: list
        Example output:
        ['$', '(', ')', '.', '343', ':', 'accur', 'addit', 'algorithm', 'best', 
        'data', 'effici', 'eigen', 'eigenvalu', 'estim', 'evid', 'exist', 'f', 
        'gener', 'given', 'improv', 'includ', 'least', 'matrix', 'mean', 'method', 
        'present', 'real', 'sampl', 'set', 'stabl', 'updat', 'valu', 'varianc', 
        'vector', 'weight']
    """
    # Set improves performance somehow, according to stackoverflow.
    # 'english' -> ~150 stopwords
    # 'en'      -> ~900 stopwords
    STOP_WORDS = set(stopwords.words('english'))
    porter = PorterStemmer()

    # Tokenize the string (converts string into list).
    string_list = word_tokenize(string)

    # Stopword removal and Porter stemming requires a list.
    # Apply stopword removal (if applicable)
    if stop_state:
        string_list = [w for w in string_list if not w in STOP_WORDS]
    # Apply Porter stemming (if applicable); overwrite string_list
    if porter_state:
        for i in range(len(string_list)):
            string_list[i] = porter.stem(string_list[i])

    if flag:
        return sorted(set(string_list))  # vocabulary only
    return string_list


def build_vocab(dictionary: dict) -> dict:
    """Returns the tokenized vocabulary set of terms (if applicable, with
    stopword removal and Porter stemming applied).
    """
    # Build the set of all terms
    vocabulary = []
    for key in dictionary.items():
        vocabulary += key[1]
    vocabulary = sorted(set(vocabulary))

    # Build the vocabulary dictionary: {term, (df, [postings])}
    vocab_dict = {}
    for term in vocabulary:
        vocab_dict[term] = build_postings(dictionary, term)
    return vocab_dict


def authors_collection(document: list) -> dict:
    doc_authors = {}

    for i in range(1, len(document)):
        # Document essential
        id = get_ID(document[i])
        author = get_author(document[i])

        if author != None:
            # Build document authors (Key: docID -> Val: Authors)
            doc_authors[id] = author.split()
        else:
            doc_authors[id] = ['None']

    return doc_authors


def titles_collection(document: list) -> dict:
    doc_titles = {}

    for i in range(1,  len(document)):
        # Document essentials
        id = get_ID(document[i])
        title = get_title(document[i])

        # Build document authors (Key: docID -> Val: Authors)
        doc_titles[id] = title.split()
    return doc_titles


def pre_processing(document: list) -> dict:
    doc_corpus = {}

    for i in range(1, len(document)):
        # Document essentials
        id = get_ID(document[i])
        title = get_title(document[i])
        abstract = get_abstract(document[i])

        # Build document corpus (Key: docID -> Val: Terms)
        if abstract != None:
            doc_corpus[id] = (stop_and_port(
                False, title.lower()+abstract.lower(), stopflag, stemflag))
        else:
            doc_corpus[id] = (stop_and_port(
                False, title.lower(), stopflag, stemflag))

    return doc_corpus

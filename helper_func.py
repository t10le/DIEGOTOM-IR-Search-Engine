import math
import pprint
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


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


def build_postings(dictionary, term):
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
        # print(f"CURRENTLY AT: {key[0]} \n\n{key} \nLEN:{len(key[1])}\n\n")

        # Document has a title and abstract
        if len(key[1]) == 3 and term in key[1][2]:
            linked_list.append(key[0])

        # Document only has a title
        elif term in key[1][1]:
            linked_list.append(key[0])

    return linked_list
    # print(f"linkedlist: {linked_list}")


def stop_and_port(flag, string, stop_state, porter_state):
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

    # Tokenize the string
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
        return sorted(set(string_list))
    return string_list


stopflag = True
stemflag = True


def build_vocab(dictionary):
    """Returns the tokenized vocabulary set of terms (if applicable, with
    stopword removal and Porter stemming applied).
    """
    # Build the set of all terms
    vocabulary = []
    for key in dictionary.items():
        if len(key[1]) == 3:
            vocabulary += key[1][2]
        else:
            vocabulary += key[1][1]
    vocabulary = sorted(set(vocabulary))

    # Build the vocabulary dictionary: {term, (df, [postings])}
    vocab_dict = {}
    for term in vocabulary:
        vocab_dict[term] = build_postings(dictionary, term)
    return vocab_dict


def pre_processing(document):
    doc_corpus = {}
    for i in range(1, len(document)):
        # Document essentials
        id = get_ID(document[i])
        title = get_title(document[i])
        abstract = get_abstract(document[i])

        # Build document corpus
        if abstract != None:
            doc_corpus[id] = (' '.join(title.split()),
                              ' '.join(abstract.split()),
                              stop_and_port(False, title.lower()+abstract.lower(), stopflag, stemflag))
        else:
            doc_corpus[id] = (' '.join(title.split()),
                              stop_and_port(False, title.lower(), stopflag, stemflag))

    return doc_corpus

    # pprint.pprint(all_terms)

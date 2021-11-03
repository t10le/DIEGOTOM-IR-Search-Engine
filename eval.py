from nltk.tokenize import word_tokenize

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
    query_dict = {}
    for i in range(1, len(document)):

        query = get_abstract(document[i]).replace("\n", " ").lower()
        id = get_ID(document[i])

        if id not in query_dict:
            query_dict[id] = query

    for key, value in query_dict.items():
        value = [word for word in word_tokenize(value) if word.isalpha()]
        query_dict[key] = value

    return query_dict


t = get_query(text)
# print(t.get('2'))


for key in t.items():
    print(key[1])

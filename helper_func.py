def show_list(arr):
    for doc in range(len(arr)):
        print(f"index: {doc}\n\"{arr[doc]}\"\n")


def pre_processing(document):
    for i in range(1, len(document)):
        print(get_ID(document[i]))
        print(get_title(document[i]))
        print(get_abstract(document[i]))


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

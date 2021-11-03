import ast
import time
import helper_func as diegotom


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


def read_file(cache):
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


def pre_process(string):
    return diegotom.stop_and_port(False, string, stop, stem)


# Greet and process user filter request
welcome_msg()
print('\nREADY!')

# Process user query and use search.py
print('\nEnter your query below; to exit, type \'ZZEND\' and hit enter.')
user = input('> ')
avg_time = 0
count = 0
while user != "ZZEND":
    start = time.time()
    # --- Enter task below ---
    query = pre_process(user)
    # ------------------------
    end = time.time()

    elapsed = end-start
    avg_time += elapsed
    count += 1
    print(f"\nElasped Time to Retrieve: {elapsed}")
    user = input('> ')
print("\ntest.py has been terminated by 'ZZEND'")
print(f"Averaged time of retrieval: {avg_time/count}")

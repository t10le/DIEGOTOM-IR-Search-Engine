import ast
import time
import invert as inversion
import os


class InvalidStopPorterOptions(Exception):
    """Raised when the input value is not any of the following:
    0 0
    1 0
    0 1
    1 1"""
    pass


def welcome_msg():
    global stop
    global stem
    print('\ntest.py initiated.\n')
    if os.path.isfile('dictionary.txt') and os.path.isfile('postings.txt'):
        print('Existing \'dictionary.txt\' and \'postings.txt\' found.\n')
        print('Would you like to make any changes to these files by applying stopword and/or Porter stemming? (y/n)')
        user = input('> ')
        if user == 'y':
            return True
        return False
    else:
        print('\n \'dictionary.txt\' and \'postings.txt\' were not found in current directory..\n')
        return False


def stop_porter_options(string):
    try:
        if string == '0 0':
            stop = False
            stem = False
            print('Selected: No stopword; No Porter stemming\nPlease wait...')
        elif string == '1 0':
            stop = True
            stem = False
            print('Selected: Apply stopword; No Porter stemming\nPlease wait...')
        elif string == "0 1":
            stop = False
            stem = True
            print('Selected: No stopword; Apply Porter stemming\nPlease wait...')
        elif string == "1 1":
            stop = True
            stem = True
            print('Selected: Apply stopword; Apply Porter stemming\nPlease wait...')
        else:
            raise InvalidStopPorterOptions

        # Establish user settings for stopword and Porter stemming.
        inversion.diegotom.set_flags(stop, stem)

        # Create new dictionary and posting textfiles.
        inversion.makeChanges(True)

    except InvalidStopPorterOptions:
        print('Invalid entry...please restart test.py')
        quit()


def pre_process(string):
    return inversion.diegotom.stop_and_port(False, string, stop, stem)


if welcome_msg():
    print('\nType either of the following combinations:')
    print('\n\t\'0 0\'\t--> No stopword; No Porter stemming')
    print('\n\t\'1 0\'\t--> Apply stopword; No Porter stemming')
    print('\n\t\'0 1\'\t--> No stopword; Apply Porter stemming')
    print('\n\t\'1 1\'\t--> Apply stopword; Apply Porter stemming')

    user = input('\n> ')
    stop_porter_options(user)


print('\nEnter your query below; to exit, type \'ZZEND\' and hit enter.')
user = input('> ')
avg_time = 0
count = 0
while user != "ZZEND":
    start = time.time()
    # Enter task below
    print(pre_process(user))
    end = time.time()

    elapsed = end-start
    avg_time += elapsed
    count += 1
    print(f"\nElasped Time to Retrieve: {elapsed}")
    user = input('> ')
print("\ntest.py has been terminated by 'ZZEND'")
print(f"Averaged time of retrieval: {avg_time/count}")

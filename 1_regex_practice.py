import re

# --- String method ---
string = "A computer !was or ! computerized from the compu computation of all computees working at Computeron Inc."
# string = "$ for $$$ or $$ and $F but a$a should not"
# print(re.findall(rf'{re.escape(term)}.', string))


wordlist = ["color", "colour", "work", "working",
            "fox", "worker", '$f', '$', 'a$', '$ff', 'comput', 'computer', 'computerization', 'acomputer']

wordlist = "Eigenvalues and Eigen vectors of a Real General Matrix (Algorithm 343 $F))".split(
)
# wordlist = ['eigenvalues', 'and', 'eigen', 'vectors', 'of', 'a',
#             'real', 'general', 'matrix', '(algorithm', '343', '$f))']
print(wordlist)
term = '('

# calculate TF
index_of_found = [i for i, x in enumerate(wordlist)
                  if re.match(rf'{re.escape(term)}', x)]

if index_of_found != []:
    print(index_of_found)
    print(len(index_of_found))

# --- List method ---
# Add or remove the words in this list to vary the results
# wordlist = ["color", "colour", "work", "working",
#             "fox", "worker", '$f', '$', 'a$', '$ff', 'comput', 'computer', 'computerization', 'acomputer']

# term2 = '$'
# special_chars = ['.', '^', '$', '*', '+',
#                  '?', '{', '}', '[', ']', '(', ')', '|', '\\']

# # Use re.match instead of re.search to force prefix-only
# # The .+ symbol is used in place of * symbol
# if term2 in special_chars:
#     print('entered 1')
#     print([i for i, x in enumerate(wordlist)
#            if re.match(f'(\{term2}.+)|({term2})', x)])
# else:
#     print('entered 2')
#     print([i for i, x in enumerate(wordlist)
#           if re.match(f'({term2}.+)|(/^b{term2}$/)', x)])

print('\n\n')
# Suppose we have a text with many email addresses
string = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'

# Here re.findall() returns a list of all the found email strings
# ['alice@google.com', 'bob@abc.com']
emails = re.findall(r'[\w\.-]+@[\w\.-]+', string)

print(emails)
for email in emails:
    # do something with each found email string
    print(email)
